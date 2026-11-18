#!/usr/bin/env python3
"""Ask AI engines the frozen question set and save every raw answer.

Stdlib only. Uses whichever keys are set; skips the rest:
    OPENAI_API_KEY      ChatGPT-style answer with web search (Responses API)
    GEMINI_API_KEY      Gemini with Google Search grounding
    PERPLEXITY_API_KEY  Perplexity Sonar
    ANTHROPIC_API_KEY   Claude with web search
Model names are env-overridable (OPENAI_MODEL, GEMINI_MODEL,
PERPLEXITY_MODEL, ANTHROPIC_MODEL). Defaults live in DEFAULT_MODELS and
in references/engines.md; check that file's date before trusting them.

Usage:
    python3 probe_engines.py questions.json --business "Acme Dental" \
        --domain acmedental.com --out captures.json [--runs 1] [--location "Phoenix, AZ"]

questions.json is a JSON list of strings (the frozen set).

Output captures.json: one record per (question, engine, run) with
status ok | failed, the raw answer text, the source URLs, and two
mechanical flags:
    named:  the business name (or a close variant) appears in the text
    cited:  the business domain appears in the sources
The agent still reads every answer: name matching misses nicknames and
catches false positives. A failed capture is never a finding.

Keys are read from the environment and never printed or written.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

DEFAULT_MODELS = {
    "chatgpt": "gpt-5-mini",
    "gemini": "gemini-2.5-flash",
    "perplexity": "sonar",
    "claude": "claude-sonnet-5-5",
}

SYSTEM_HINT = (
    "Answer the way you would for a real person asking. If they are asking "
    "for a business or provider, name specific ones and say why."
)


def post(url: str, payload: dict, headers: dict, timeout: int = 90) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def ask_chatgpt(q: str, loc: str) -> tuple[str, list[str]]:
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODELS["chatgpt"])
    tool: dict = {"type": "web_search"}
    if loc:
        tool["user_location"] = {"type": "approximate", "city": loc.split(",")[0].strip()}
    body = post("https://api.openai.com/v1/responses",
                {"model": model, "tools": [tool], "instructions": SYSTEM_HINT, "input": q},
                {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"})
    text, urls = [], []
    for item in body.get("output", []):
        if item.get("type") != "message":
            continue
        for c in item.get("content", []):
            if c.get("type") == "output_text":
                text.append(c.get("text", ""))
                for ann in c.get("annotations", []) or []:
                    if ann.get("url"):
                        urls.append(ann["url"])
    return "\n".join(text), urls


def ask_gemini(q: str, loc: str) -> tuple[str, list[str]]:
    model = os.getenv("GEMINI_MODEL", DEFAULT_MODELS["gemini"])
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    prompt = f"{q}\n\n(I am in {loc}.)" if loc else q
    body = post(url, {"contents": [{"parts": [{"text": prompt}]}], "tools": [{"google_search": {}}]},
                {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    cand = (body.get("candidates") or [{}])[0]
    text = "\n".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
    urls = []
    for ch in (cand.get("groundingMetadata") or {}).get("groundingChunks", []) or []:
        web = ch.get("web") or {}
        # Gemini returns redirect URIs; the title is usually the domain.
        urls.append(web.get("title") or web.get("uri") or "")
    return text, [u for u in urls if u]


def ask_perplexity(q: str, loc: str) -> tuple[str, list[str]]:
    model = os.getenv("PERPLEXITY_MODEL", DEFAULT_MODELS["perplexity"])
    prompt = f"{q} (I am in {loc}.)" if loc else q
    body = post("https://api.perplexity.ai/chat/completions",
                {"model": model, "messages": [{"role": "system", "content": SYSTEM_HINT},
                                              {"role": "user", "content": prompt}]},
                {"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"})
    text = body["choices"][0]["message"]["content"]
    urls = list(body.get("citations") or [])
    urls += [r.get("url") for r in body.get("search_results") or [] if r.get("url")]
    return text, urls


def ask_claude(q: str, loc: str) -> tuple[str, list[str]]:
    model = os.getenv("ANTHROPIC_MODEL", DEFAULT_MODELS["claude"])
    prompt = f"{q} (I am in {loc}.)" if loc else q
    body = post("https://api.anthropic.com/v1/messages",
                {"model": model, "max_tokens": 2000, "system": SYSTEM_HINT,
                 "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
                 "messages": [{"role": "user", "content": prompt}]},
                {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"})
    text, urls = [], []
    for block in body.get("content", []):
        if block.get("type") == "text":
            text.append(block.get("text", ""))
            for c in block.get("citations") or []:
                if c.get("url"):
                    urls.append(c["url"])
        elif block.get("type") == "web_search_tool_result":
            for r in block.get("content") or []:
                if isinstance(r, dict) and r.get("url"):
                    urls.append(r["url"])
    return "\n".join(text), urls


ENGINES = {
    "chatgpt": ("OPENAI_API_KEY", ask_chatgpt),
    "gemini": ("GEMINI_API_KEY", ask_gemini),
    "perplexity": ("PERPLEXITY_API_KEY", ask_perplexity),
    "claude": ("ANTHROPIC_API_KEY", ask_claude),
}

SUFFIX_RX = re.compile(r"\b(llc|inc|pllc|pc|pa|ltd|co|corp|group|the)\b\.?", re.I)


def name_variants(name: str) -> list[str]:
    base = SUFFIX_RX.sub("", name).strip(" ,.&")
    out = {name.lower(), base.lower()}
    out.add(base.lower().replace("&", "and"))
    return [v for v in out if len(v) >= 4]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("questions")
    ap.add_argument("--business", required=True)
    ap.add_argument("--domain", default="")
    ap.add_argument("--location", default="")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--engines", default="", help="comma list to limit, e.g. chatgpt,perplexity")
    ap.add_argument("--out", default="captures.json")
    a = ap.parse_args()

    with open(a.questions) as f:
        questions = json.load(f)
    wanted = {e.strip() for e in a.engines.split(",") if e.strip()} or set(ENGINES)
    active = {k: v for k, v in ENGINES.items() if k in wanted and os.getenv(v[0])}
    skipped = sorted(wanted - set(active))
    if not active:
        print("No engine keys set. Use the manual path in SKILL.md (paste answers).", file=sys.stderr)
        return 2

    variants = name_variants(a.business)
    domain = a.domain.lower().replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
    captures = []
    for q in questions:
        for eng, (_key, fn) in active.items():
            for run in range(1, a.runs + 1):
                rec = {"question": q, "engine": eng, "run": run,
                       "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                try:
                    text, urls = fn(q, a.location)
                    if not text.strip():
                        raise ValueError("empty answer")
                    low = text.lower()
                    rec.update(status="ok", text=text, sources=sorted(set(urls)),
                               named=any(v in low for v in variants),
                               cited=bool(domain) and any(domain in (u or "").lower() for u in urls))
                except urllib.error.HTTPError as e:
                    rec.update(status="failed", error=f"HTTP {e.code}")
                except Exception as e:  # noqa: BLE001
                    rec.update(status="failed", error=type(e).__name__ + ": " + str(e)[:160])
                captures.append(rec)
                print(f"[{rec['status']}] {eng} r{run}: {q[:70]}", file=sys.stderr)
                time.sleep(0.5)

    with open(a.out, "w") as f:
        json.dump({"business": a.business, "domain": domain, "location": a.location,
                   "engines_used": sorted(active), "engines_skipped": skipped,
                   "questions": questions, "captures": captures}, f, indent=2)
    ok = sum(1 for c in captures if c["status"] == "ok")
    print(f"wrote {a.out}: {ok}/{len(captures)} captures ok; skipped engines: {skipped or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

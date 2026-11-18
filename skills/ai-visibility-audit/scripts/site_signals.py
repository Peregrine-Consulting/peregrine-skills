#!/usr/bin/env python3
"""Scan a website for the machine-readable signals AI engines rely on.

Stdlib only. No keys. Read-only GET requests to the site you name.

Usage:
    python3 site_signals.py https://www.example.com [--out signals.json] [--pages /about,/services]

Checks:
  - robots.txt: is each AI crawler allowed to fetch the homepage?
  - llms.txt and sitemap.xml present
  - homepage: server-rendered text vs an empty JS shell
  - JSON-LD schema types found (LocalBusiness, Organization, FAQPage, ...)
  - phone numbers and street addresses visible in the HTML (NAP)
  - title, meta description, H1, visible dateModified hints

Every check records "ok", "missing", "blocked" or "not_observed".
A fetch that fails is "not_observed", never "missing": your network
failing is not the site's fault.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib import robotparser
from urllib.parse import urljoin, urlparse

AI_AGENTS = (
    "GPTBot",            # OpenAI training
    "OAI-SearchBot",     # ChatGPT search index
    "ChatGPT-User",      # ChatGPT fetching a page for a user
    "ClaudeBot",
    "Claude-User",
    "PerplexityBot",
    "Perplexity-User",
    "Google-Extended",   # Gemini training opt-out token
    "Bingbot",           # feeds Copilot and some ChatGPT search
    "CCBot",
)
# Agents whose block actually removes the site from live AI answers.
# Blocking training-only agents (GPTBot, Google-Extended, CCBot) is a
# business choice, not an answer-visibility problem.
ANSWER_AGENTS = {"OAI-SearchBot", "ChatGPT-User", "Claude-User",
                 "PerplexityBot", "Perplexity-User", "Bingbot"}

UA = "Mozilla/5.0 (compatible; VisibilityAudit/1.0)"
CSR_HINTS = ('id="root"', 'id="app"', 'id="__next"', "data-reactroot", "ng-version")
PHONE_RX = re.compile(r"(?:\+?1[\s.-]?)?\(?\b[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b")
STREET_RX = re.compile(
    r"\b\d{2,6}\s+(?:[NSEW]\.?\s+)?[A-Z][A-Za-z0-9.' ]{1,40}\s"
    r"(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|Lane|Way|Pkwy|Parkway|Ct|Court|Hwy|Highway|Suite|Ste|Pl|Place)\b"
)


def fetch(url: str, timeout: int = 12) -> tuple[int | None, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            body = r.read(3_000_000).decode(r.headers.get_content_charset() or "utf-8", "replace")
            return r.status, body
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return None, ""


class _Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []
        self.jsonld: list[str] = []
        self.title = ""
        self.h1: list[str] = []
        self.meta_desc = ""
        self._in: list[str] = []
        self._ld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._in.append(tag)
        if tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._ld = True
            self.jsonld.append("")
        if tag == "meta" and (a.get("name") or "").lower() == "description":
            self.meta_desc = a.get("content") or ""

    def handle_endtag(self, tag):
        if tag == "script":
            self._ld = False
        if self._in and self._in[-1] == tag:
            self._in.pop()

    def handle_data(self, data):
        if self._ld:
            self.jsonld[-1] += data
            return
        cur = self._in[-1] if self._in else ""
        if cur in ("script", "style", "noscript"):
            return
        if cur == "title":
            self.title += data.strip()
        if cur == "h1" and data.strip():
            self.h1.append(data.strip())
        if data.strip():
            self.text.append(data.strip())


def schema_types(blocks: list[str]) -> list[str]:
    found: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, str):
                found.add(t)
            elif isinstance(t, list):
                found.update(x for x in t if isinstance(x, str))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for b in blocks:
        try:
            walk(json.loads(b))
        except Exception:
            found.add("INVALID_JSON_LD")
    return sorted(found)


def scan_page(url: str) -> dict:
    status, html = fetch(url)
    if status is None or not html:
        return {"url": url, "status": "not_observed", "http": status}
    p = _Page()
    try:
        p.feed(html)
    except Exception:
        pass
    text = " ".join(p.text)
    csr_shell = len(text) < 800 and any(h in html for h in CSR_HINTS)
    return {
        "url": url,
        "status": "ok",
        "http": status,
        "title": p.title[:200],
        "meta_description": p.meta_desc[:300],
        "h1": p.h1[:3],
        "visible_text_chars": len(text),
        "rendering": "client_side_shell" if csr_shell else "server_rendered",
        "schema_types": schema_types(p.jsonld),
        "phones": sorted(set(m.group(0).strip() for m in PHONE_RX.finditer(text)))[:5],
        "street_addresses": sorted(set(m.group(0).strip() for m in STREET_RX.finditer(text)))[:5],
        "has_date_modified": bool(re.search(r"dateModified|Last updated|Updated on", html, re.I)),
        "has_faq_block": "FAQPage" in html or bool(re.search(r">\s*(FAQ|Frequently asked)", html, re.I)),
    }


def robots_check(site: str) -> dict:
    url = urljoin(site, "/robots.txt")
    status, body = fetch(url)
    if status is None:
        return {"status": "not_observed", "agents": {}}
    if status >= 400 or not body.strip():
        return {"status": "missing", "agents": {a: "allowed" for a in AI_AGENTS},
                "note": "No robots.txt, so every crawler is allowed by default."}
    rp = robotparser.RobotFileParser()
    rp.parse(body.splitlines())
    agents = {a: ("allowed" if rp.can_fetch(a, site) else "blocked") for a in AI_AGENTS}
    return {"status": "ok", "agents": agents,
            "answer_agents_blocked": sorted(a for a, v in agents.items() if v == "blocked" and a in ANSWER_AGENTS),
            "has_sitemap_line": "sitemap:" in body.lower()}


def exists(site: str, path: str) -> str:
    status, body = fetch(urljoin(site, path))
    if status is None:
        return "not_observed"
    if status == 200 and body.strip() and "<html" not in body[:500].lower():
        return "ok"
    return "missing"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--out", default="")
    ap.add_argument("--pages", default="", help="comma-separated extra paths to scan")
    a = ap.parse_args()
    site = a.site if a.site.startswith("http") else "https://" + a.site
    parsed = urlparse(site)
    root = f"{parsed.scheme}://{parsed.netloc}/"

    pages = [scan_page(site)]
    for path in [p.strip() for p in a.pages.split(",") if p.strip()]:
        pages.append(scan_page(urljoin(root, path)))

    sitemap = exists(root, "/sitemap.xml")
    if sitemap == "missing":
        sitemap = exists(root, "/sitemap_index.xml")
    result = {
        "site": root,
        "robots": robots_check(root),
        "llms_txt": exists(root, "/llms.txt"),
        "sitemap": sitemap,
        "pages": pages,
    }
    out = json.dumps(result, indent=2)
    if a.out:
        with open(a.out, "w") as f:
            f.write(out)
        print(f"wrote {a.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

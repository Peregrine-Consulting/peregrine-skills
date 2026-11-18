#!/usr/bin/env python3
"""Score an audit and render the client-ready HTML report.

Stdlib only. Input is audit.json, assembled by the agent from
captures.json, signals.json and its own reading of the answers.
Schema: references/audit-schema.md.

Usage:
    python3 build_report.py audit.json --out report.html [--brand-name "Your Agency"] [--accent "#2563eb"]

Scoring (0-100) only counts what was checked. Anything null or
not_observed drops out of both earned and possible points, and the
report says which parts were not checked. Weights:
    AI answers         60  cited = 1.0, mentioned = 0.7, absent = 0, per observed answer
    Site readiness     25  answer crawlers allowed 8, server-rendered 5,
                           business schema 5, FAQ schema 2, llms.txt 2,
                           sitemap 1, phone + address on page 2
    Reputation/entity  15  Google Business Profile 5, 10+ reviews 3,
                           directories (2 each, max 4), knowledge panel or Wikidata 3
"""

from __future__ import annotations

import argparse
import html
import json
import sys

BANDS = ((76, "Strong", "well represented"), (51, "Moderate", "partially visible"),
         (26, "Weak", "barely visible"), (0, "Critical", "nearly invisible"))
STATE_PTS = {"cited": 1.0, "mentioned": 0.7, "absent": 0.0}
STATE_LABEL = {"cited": "Cited", "mentioned": "Named", "absent": "Not named", "not_observed": "Not checked"}
ENGINE_LABEL = {"chatgpt": "ChatGPT", "gemini": "Gemini", "perplexity": "Perplexity",
                "claude": "Claude", "google_ai": "Google AI", "copilot": "Copilot"}


def e(s) -> str:
    return html.escape(str(s if s is not None else ""))


def score(audit: dict) -> dict:
    parts = {}
    # AI answers
    observed = [r for q in audit.get("questions", []) for r in q.get("results", [])
                if r.get("state") in STATE_PTS]
    if observed:
        rate = sum(STATE_PTS[r["state"]] for r in observed) / len(observed)
        named = sum(1 for r in observed if r["state"] in ("cited", "mentioned"))
        parts["answers"] = {"earned": 60 * rate, "possible": 60, "named": named, "observed": len(observed)}
    # Site readiness
    sig = audit.get("signals") or {}
    earned = possible = 0.0
    robots = sig.get("robots") or {}
    if robots.get("status") in ("ok", "missing"):
        possible += 8
        earned += 0 if robots.get("answer_agents_blocked") else 8
    home = (sig.get("pages") or [{}])[0]
    if home.get("status") == "ok":
        possible += 5 + 5 + 2 + 2
        earned += 5 if home.get("rendering") == "server_rendered" else 0
        types = set()
        for p in sig.get("pages", []):
            types.update(p.get("schema_types") or [])
        biz = {"LocalBusiness", "Organization", "Dentist", "MedicalBusiness", "LegalService",
               "Attorney", "HomeAndConstructionBusiness", "ProfessionalService", "MedicalClinic",
               "Physician", "Plumber", "Electrician", "RoofingContractor", "HVACBusiness"}
        earned += 5 if types & biz else 0
        earned += 2 if "FAQPage" in types else 0
        earned += 2 if home.get("phones") and home.get("street_addresses") else 0
    for key, pts in (("llms_txt", 2), ("sitemap", 1)):
        if sig.get(key) in ("ok", "missing"):
            possible += pts
            earned += pts if sig[key] == "ok" else 0
    if possible:
        parts["site"] = {"earned": earned, "possible": possible}
    # Reputation / entity
    rep = audit.get("reputation") or {}
    earned = possible = 0.0
    if rep.get("gbp_found") is not None:
        possible += 5
        earned += 5 if rep["gbp_found"] else 0
        if rep.get("gbp_reviews") is not None:
            possible += 3
            earned += 3 if rep["gbp_reviews"] >= 10 else 0
    if rep.get("directories_found") is not None:
        possible += 4
        earned += min(4, 2 * len(rep["directories_found"]))
    if rep.get("knowledge_panel") is not None or rep.get("wikidata") is not None:
        possible += 3
        earned += 3 if (rep.get("knowledge_panel") or rep.get("wikidata")) else 0
    if possible:
        parts["reputation"] = {"earned": earned, "possible": possible}

    total_possible = sum(p["possible"] for p in parts.values())
    total = round(100 * sum(p["earned"] for p in parts.values()) / total_possible) if total_possible else None
    grade = qual = None
    if total is not None:
        for cut, g, q in BANDS:
            if total >= cut:
                grade, qual = g, q
                break
    unchecked = [k for k in ("answers", "site", "reputation") if k not in parts]
    return {"score": total, "grade": grade, "qualifier": qual, "parts": parts,
            "unchecked": unchecked, "max_possible_checked": total_possible}


CSS = """
:root{--ink:#0f172a;--muted:#475569;--line:#e2e8f0;--bg:#ffffff;--soft:#f8fafc;--accent:ACCENT;
--good:#15803d;--mid:#b45309;--bad:#b91c1c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:880px;margin:0 auto;padding:40px 20px 64px}
header{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;
padding-bottom:20px;border-bottom:1px solid var(--line)}
.brand{font-weight:700;letter-spacing:-.01em}.meta{color:var(--muted);font-size:14px}
.hero{display:grid;grid-template-columns:180px 1fr;gap:32px;align-items:center;padding:36px 0}
@media(max-width:640px){.hero{grid-template-columns:1fr}}
.ring{position:relative;width:180px;height:180px}.ring svg{transform:rotate(-90deg)}
.ring .num{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.ring b{font-size:48px;line-height:1;letter-spacing:-.03em}.ring small{color:var(--muted);font-size:13px;margin-top:4px}
h1{font-size:30px;line-height:1.2;letter-spacing:-.02em;margin:0 0 12px}
h1 span{color:var(--accent)}h2{font-size:20px;letter-spacing:-.01em;margin:40px 0 12px}
p{margin:0 0 12px}.muted{color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:10px 8px;
border-bottom:1px solid var(--line);vertical-align:top}th{font-size:12px;text-transform:uppercase;
letter-spacing:.06em;color:var(--muted);font-weight:600}
.chip{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap}
.cited{background:#dcfce7;color:var(--good)}.mentioned{background:#fef3c7;color:var(--mid)}
.absent{background:#fee2e2;color:var(--bad)}.not_observed{background:var(--soft);color:var(--muted)}
.q{padding:16px 0;border-bottom:1px solid var(--line)}.q h3{font-size:16px;margin:0 0 8px}
.eng{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:14px}.eng div{min-width:220px}
.instead{color:var(--muted);font-size:13px}
ol.fixes{padding-left:20px}ol.fixes li{margin:0 0 14px}ol.fixes b{display:block}
.tag{font-size:12px;color:var(--muted);margin-left:6px}
.cta{margin-top:40px;padding:24px;background:var(--soft);border-radius:14px}
.cta a{display:inline-block;margin-top:8px;background:var(--accent);color:#fff;text-decoration:none;
padding:12px 18px;border-radius:10px;font-weight:600}
footer{margin-top:48px;color:var(--muted);font-size:12px}
@media print{.cta a{color:#fff}.wrap{padding:0}}
"""


def ring(score_val: int | None, accent: str) -> str:
    c = 2 * 3.14159 * 80
    pct = (score_val or 0) / 100
    return (f'<svg width="180" height="180" viewBox="0 0 180 180">'
            f'<circle cx="90" cy="90" r="80" fill="none" stroke="#e2e8f0" stroke-width="14"/>'
            f'<circle cx="90" cy="90" r="80" fill="none" stroke="{e(accent)}" stroke-width="14" '
            f'stroke-linecap="round" stroke-dasharray="{c:.1f}" stroke-dashoffset="{c * (1 - pct):.1f}"/></svg>')


def render(audit: dict, s: dict, brand_name: str, accent: str) -> str:
    b = audit.get("business", {})
    out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<meta name='robots' content='noindex'>"
           f"<title>AI visibility report: {e(b.get('name'))}</title>"
           f"<style>{CSS.replace('ACCENT', accent)}</style></head><body><div class='wrap'>"]
    out.append(f"<header><div class='brand'>{e(brand_name)}</div><div class='meta'>"
               f"{e(b.get('name'))} · {e(b.get('location'))} · {e(b.get('date'))}</div></header>")
    sc = s["score"]
    head = audit.get("headline") or (
        f"{e(b.get('name'))} is <span>{e(s['qualifier'])}</span> to the AI assistants your buyers use."
        if sc is not None else "We could not observe enough answers to score this business.")
    out.append("<section class='hero'><div class='ring'>" + ring(sc, accent) +
               f"<div class='num'><b>{sc if sc is not None else 'n/a'}</b><small>{e(s['grade'] or 'Not scored')}</small></div></div>"
               f"<div><h1>{head}</h1><p class='muted'>{e(audit.get('summary'))}</p></div></section>")

    a = s["parts"].get("answers")
    used = ", ".join(ENGINE_LABEL.get(x, x) for x in audit.get("engines_used", []))
    notes = []
    if a:
        notes.append(f"Named in {a['named']} of {a['observed']} AI answers we observed ({e(used)}).")
    if audit.get("engines_not_checked"):
        notes.append("Not checked: " + e(", ".join(ENGINE_LABEL.get(x, x) for x in audit["engines_not_checked"])) + ".")
    if s["unchecked"]:
        notes.append("Score excludes: " + e(", ".join(s["unchecked"])) + " (not checked).")
    out.append("<h2>What this means</h2><p>" + " ".join(notes) + "</p>")
    if audit.get("what_this_means"):
        out.append(f"<p>{e(audit['what_this_means'])}</p>")

    out.append("<h2>The questions your buyers ask</h2>")
    for q in audit.get("questions", []):
        out.append(f"<div class='q'><h3>{e(q.get('question'))}</h3><div class='eng'>")
        for r in q.get("results", []):
            st = r.get("state", "not_observed")
            inst = r.get("named_instead") or []
            out.append(f"<div><b>{e(ENGINE_LABEL.get(r.get('engine'), r.get('engine')))}</b> "
                       f"<span class='chip {e(st)}'>{e(STATE_LABEL.get(st, st))}</span>"
                       + (f"<div class='instead'>Named instead: {e(', '.join(inst[:4]))}</div>" if inst and st == 'absent' else "")
                       + "</div>")
        out.append("</div></div>")

    comps = audit.get("competitors") or []
    if comps:
        out.append("<h2>Who AI recommends instead</h2><table><tr><th>Business</th><th>Times named</th><th>Why they show up</th></tr>")
        out.append(f"<tr><td><b>{e(b.get('name'))}</b></td><td>{a['named'] if a else 'n/a'}</td><td class='muted'>Your business</td></tr>")
        for c in comps[:6]:
            out.append(f"<tr><td>{e(c.get('name'))}</td><td>{e(c.get('times_named'))}</td><td>{e(c.get('why_they_win'))}</td></tr>")
        out.append("</table>")

    if audit.get("findings"):
        out.append("<h2>What we found</h2><ul>")
        for f in audit["findings"]:
            out.append(f"<li><b>{e(f.get('title'))}.</b> {e(f.get('detail'))}</li>")
        out.append("</ul>")

    if audit.get("fixes"):
        out.append("<h2>Fix these first</h2><ol class='fixes'>")
        for f in audit["fixes"]:
            out.append(f"<li><b>{e(f.get('title'))}<span class='tag'>impact {e(f.get('impact'))} · effort {e(f.get('effort'))}</span></b>"
                       f"{e(f.get('why'))}</li>")
        out.append("</ol>")

    cta = audit.get("cta") or {}
    if cta.get("url"):
        out.append(f"<div class='cta'><b>{e(cta.get('headline') or 'Want these fixed?')}</b>"
                   f"<p class='muted'>{e(cta.get('text'))}</p><a href='{e(cta['url'])}'>{e(cta.get('button') or 'Book a call')}</a></div>")

    out.append(f"<footer>Method: {e(len(audit.get('questions', [])))} buyer questions asked to {e(used) or 'AI engines'} on "
               f"{e(b.get('date'))}{' from ' + e(b.get('location')) if b.get('location') else ''}. AI answers vary between runs; "
               f"this report describes the answers we observed, not every possible answer. Unchecked items are excluded from the score.</footer>")
    out.append("</div></body></html>")
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audit")
    ap.add_argument("--out", default="report.html")
    ap.add_argument("--brand-name", default="AI Visibility Report")
    ap.add_argument("--accent", default="#2563eb")
    a = ap.parse_args()
    with open(a.audit) as f:
        audit = json.load(f)
    s = score(audit)
    with open(a.out, "w") as f:
        f.write(render(audit, s, a.brand_name, a.accent))
    print(json.dumps({k: s[k] for k in ("score", "grade", "unchecked")}))
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

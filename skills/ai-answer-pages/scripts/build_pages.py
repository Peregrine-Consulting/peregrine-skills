#!/usr/bin/env python3
"""Build answer pages (static HTML) from one JSON source file.

Stdlib only. Writes plain HTML that every AI fetcher can read without
JavaScript, with Article + FAQPage + BreadcrumbList JSON-LD, a
questions index, sitemap.xml and llms.txt. If the user's site runs on a
CMS, use --snippets to emit only the JSON-LD and body HTML per page for
pasting into the CMS instead.

Usage:
    python3 build_pages.py pages.json --out site/ [--snippets]

Source format: references/pages-schema.md.

Body text supports a tiny markup: blank line = new paragraph,
lines starting "- " = bullet list, [text](url) = link, **bold**.
Everything else is escaped.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import date

LINK_RX = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD_RX = re.compile(r"\*\*([^*]+)\*\*")


def inline(s: str) -> str:
    s = html.escape(s)
    s = LINK_RX.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return BOLD_RX.sub(r"<strong>\1</strong>", s)


def blocks(text: str) -> str:
    out = []
    for para in re.split(r"\n\s*\n", (text or "").strip()):
        lines = [ln.strip() for ln in para.splitlines() if ln.strip()]
        if not lines:
            continue
        if all(ln.startswith("- ") for ln in lines):
            out.append("<ul>" + "".join(f"<li>{inline(ln[2:])}</li>" for ln in lines) + "</ul>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "\n".join(out)


def plain(text: str) -> str:
    t = LINK_RX.sub(r"\1", text or "")
    return BOLD_RX.sub(r"\1", t).replace("\n- ", " ").strip()


def jsonld(obj: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=1).replace("</", "<\\/") + "</script>"


CSS = """:root{--ink:#0f172a;--muted:#475569;--line:#e2e8f0;--soft:#f8fafc;--accent:ACCENT;--bg:#fff}
@media (prefers-color-scheme:dark){:root{--ink:#e2e8f0;--muted:#94a3b8;--line:#1e293b;--soft:#0f172a;--bg:#020617}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.notice{background:var(--soft);border-bottom:1px solid var(--line);font-size:13px;color:var(--muted);padding:8px 16px;text-align:center}
header,main,footer{max-width:760px;margin:0 auto;padding:0 16px}header{display:flex;justify-content:space-between;align-items:center;padding-top:18px;padding-bottom:18px;border-bottom:1px solid var(--line)}
header a{color:var(--ink);text-decoration:none;font-weight:700}nav a{font-weight:500;color:var(--muted);margin-left:16px;font-size:15px}
.crumbs{font-size:13px;color:var(--muted);margin:24px 0 8px}.crumbs a{color:var(--muted)}
h1{font-size:34px;line-height:1.15;letter-spacing:-.02em;margin:0 0 16px}h2{font-size:22px;letter-spacing:-.01em;margin:36px 0 10px}
.answer{background:var(--soft);border-left:4px solid var(--accent);padding:16px 18px;border-radius:8px;margin:0 0 12px}
.answer b{display:block;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:4px}
.byline{font-size:14px;color:var(--muted);margin-bottom:24px}a{color:var(--accent)}
.cta{margin:32px 0;padding:20px;border-radius:12px;background:var(--soft)}.cta a.btn{display:inline-block;margin-top:8px;background:var(--accent);color:#fff;padding:11px 16px;border-radius:9px;text-decoration:none;font-weight:600}
details{border-bottom:1px solid var(--line);padding:12px 0}summary{font-weight:600;cursor:pointer}
.related a{display:block;margin:6px 0}footer{margin-top:56px;padding-top:20px;padding-bottom:40px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
ul.qlist{padding:0;list-style:none}ul.qlist li{padding:14px 0;border-bottom:1px solid var(--line)}ul.qlist p{margin:4px 0 0;color:var(--muted);font-size:15px}"""


def shell(site: dict, title: str, desc: str, canonical: str, body: str, ld: list[dict], noindex: bool = False) -> str:
    notice = f"<div class='notice'>{inline(site['disclosure'])}</div>" if site.get("disclosure") else ""
    nav = "".join(f"<a href='{html.escape(n['url'])}'>{html.escape(n['label'])}</a>" for n in site.get("nav", []))
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{html.escape(title)}</title><meta name='description' content='{html.escape(desc)}'>"
        f"<link rel='canonical' href='{html.escape(canonical)}'>"
        + ("<meta name='robots' content='noindex'>" if noindex else "")
        + f"<meta property='og:title' content='{html.escape(title)}'><meta property='og:description' content='{html.escape(desc)}'>"
        + f"<style>{CSS.replace('ACCENT', site.get('accent', '#2563eb'))}</style>"
        + "".join(jsonld(x) for x in ld)
        + f"</head><body>{notice}<header><a href='{html.escape(site['base_url'])}'>{html.escape(site['name'])}</a><nav>{nav}</nav></header>"
        + f"<main>{body}</main><footer>{inline(site.get('footer', ''))}"
        + (f"<p>{inline(site['disclosure'])}</p>" if site.get("disclosure") else "")
        + "</footer></body></html>"
    )


def page_ld(site: dict, p: dict, url: str) -> list[dict]:
    org = {"@type": "Organization", "name": site["publisher"], "url": site.get("publisher_url", site["base_url"])}
    author = p.get("author") or site.get("author") or {"name": site["publisher"], "url": site.get("publisher_url", site["base_url"])}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p["question"],
           "description": p.get("meta_description") or plain(p["short_answer"])[:300],
           "datePublished": p.get("published", site.get("updated")), "dateModified": p.get("updated", site.get("updated")),
           "author": {"@type": "Person" if author.get("person") else "Organization", "name": author["name"], "url": author.get("url")},
           "publisher": org, "mainEntityOfPage": url}
    faqs = [{"@type": "Question", "name": p["question"], "acceptedAnswer": {"@type": "Answer", "text": plain(p["short_answer"])}}]
    faqs += [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": plain(f["a"])}} for f in p.get("faqs", [])]
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": site["name"], "item": site["base_url"]},
        {"@type": "ListItem", "position": 2, "name": "Questions", "item": site["base_url"].rstrip("/") + "/questions/"},
        {"@type": "ListItem", "position": 3, "name": p["question"], "item": url}]}
    return [art, {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faqs}, crumbs]


def page_body(site: dict, p: dict, by_slug: dict) -> str:
    base = site["base_url"].rstrip("/")
    upd = p.get("updated", site.get("updated", ""))
    parts = [f"<div class='crumbs'><a href='{base}/'>{html.escape(site['name'])}</a> / <a href='{base}/questions/'>Questions</a></div>",
             f"<h1>{html.escape(p['question'])}</h1>",
             f"<div class='answer'><b>Short answer</b>{inline(p['short_answer'])}</div>",
             f"<div class='byline'>By {inline((p.get('author') or site.get('author') or {}).get('name', site['publisher']))} · Updated {html.escape(upd)}</div>"]
    cta = p.get("cta") or site.get("cta")
    for i, sec in enumerate(p.get("sections", [])):
        parts.append(f"<h2>{html.escape(sec['heading'])}</h2>{blocks(sec['body'])}")
        if i == 0 and cta and cta.get("url"):
            parts.append(f"<div class='cta'><strong>{inline(cta.get('headline', ''))}</strong><p>{inline(cta.get('text', ''))}</p>"
                         f"<a class='btn' href='{html.escape(cta['url'])}'>{html.escape(cta.get('button', 'Learn more'))}</a></div>")
    if p.get("faqs"):
        parts.append("<h2>Related questions</h2>" + "".join(
            f"<details><summary>{html.escape(f['q'])}</summary>{blocks(f['a'])}</details>" for f in p["faqs"]))
    rel = [by_slug[s] for s in p.get("related", []) if s in by_slug]
    if rel:
        parts.append("<h2>Keep reading</h2><div class='related'>" + "".join(
            f"<a href='{base}/questions/{r['slug']}.html'>{html.escape(r['question'])}</a>" for r in rel) + "</div>")
    if p.get("sources"):
        parts.append("<h2>Sources</h2><ul>" + "".join(f"<li>{inline(s)}</li>" for s in p["sources"]) + "</ul>")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", default="site")
    ap.add_argument("--snippets", action="store_true")
    a = ap.parse_args()
    with open(a.source) as f:
        src = json.load(f)
    site, pages = src["site"], src["pages"]
    site.setdefault("updated", date.today().isoformat())
    base = site["base_url"].rstrip("/")
    by_slug = {p["slug"]: p for p in pages}
    qdir = os.path.join(a.out, "questions")
    os.makedirs(qdir, exist_ok=True)

    for p in pages:
        url = f"{base}/questions/{p['slug']}.html"
        ld = page_ld(site, p, url)
        body = page_body(site, p, by_slug)
        if a.snippets:
            with open(os.path.join(qdir, p["slug"] + ".snippet.html"), "w") as f:
                f.write("<!-- paste into <head> -->\n" + "\n".join(jsonld(x) for x in ld) + "\n\n<!-- page body -->\n" + body + "\n")
            continue
        title = p.get("title") or f"{p['question']} | {site['name']}"
        with open(os.path.join(qdir, p["slug"] + ".html"), "w") as f:
            f.write(shell(site, title, p.get("meta_description") or plain(p["short_answer"])[:155], url, body, ld, p.get("noindex", False)))

    if not a.snippets:
        groups: dict[str, list[dict]] = {}
        for p in pages:
            groups.setdefault(p.get("group", "Questions"), []).append(p)
        body = [f"<h1>{html.escape(site.get('hub_title', 'Questions buyers ask'))}</h1><p>{inline(site.get('hub_intro', ''))}</p>"]
        for g, ps in groups.items():
            body.append(f"<h2>{html.escape(g)}</h2><ul class='qlist'>" + "".join(
                f"<li><a href='{base}/questions/{p['slug']}.html'>{html.escape(p['question'])}</a><p>{html.escape(plain(p['short_answer'])[:220])}</p></li>"
                for p in ps if not p.get("noindex")) + "</ul>")
        with open(os.path.join(qdir, "index.html"), "w") as f:
            f.write(shell(site, f"{site.get('hub_title', 'Questions')} | {site['name']}", site.get("hub_intro", "")[:155],
                          f"{base}/questions/", "\n".join(body), []))
        urls = [f"{base}/questions/"] + [f"{base}/questions/{p['slug']}.html" for p in pages if not p.get("noindex")]
        with open(os.path.join(a.out, "sitemap-questions.xml"), "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    + "".join(f"  <url><loc>{html.escape(u)}</loc><lastmod>{site['updated']}</lastmod></url>\n" for u in urls)
                    + "</urlset>\n")
        lines = [f"# {site['name']}", "", f"> {plain(site.get('summary', site.get('hub_intro', '')))}", ""]
        if site.get("disclosure"):
            lines += [plain(site["disclosure"]), ""]
        lines += ["## Questions", ""]
        lines += [f"- [{p['question']}]({base}/questions/{p['slug']}.html): {plain(p['short_answer'])}" for p in pages if not p.get("noindex")]
        with open(os.path.join(a.out, "llms.txt"), "w") as f:
            f.write("\n".join(lines) + "\n")
    print(f"wrote {len(pages)} pages to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

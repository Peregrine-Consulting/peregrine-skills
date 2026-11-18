#!/usr/bin/env python3
"""Find local businesses, enrich them, rank them, write a CSV.

Stdlib only. Every paid step is optional and reads its key from an env var:
  APIFY_TOKEN              Google Maps search (actor compass~crawler-google-places)
  PROSPEO_API_KEY          decision maker + email at the business's domain
  MILLIONVERIFIER_API_KEY  email verification
  TELNYX_API_KEY           phone line type (mobile / landline / voip)

Usage
  # 1. Search Google Maps through Apify (needs APIFY_TOKEN)
  python3 maps_leads.py search --query "dentist" --location "Phoenix, AZ" \
      --location "Mesa, AZ" --per-location 60 --max-usd 5 --out raw.json

  # 2. Enrich + rank (works on Apify output OR a hand-built CSV/JSON list)
  python3 maps_leads.py rank --in raw.json --out leads.csv \
      --min-reviews 10 --skip-chains --scan-sites --known done.csv

Nothing here sends a message or calls anyone. Keys are never printed.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

APIFY = "https://api.apify.com/v2"
ACTOR = os.environ.get("APIFY_MAPS_ACTOR", "compass~crawler-google-places")
UA = "Mozilla/5.0 (compatible; lead-research/1.0)"

ROLE_LOCALS = {
    "info", "office", "contact", "hello", "admin", "sales", "support", "service",
    "team", "mail", "help", "billing", "frontdesk", "reception", "appointments",
}
SENIORITY = [
    r"owner|founder|co-founder|president|ceo|chief executive|principal",
    r"managing partner|managing attorney|managing member|partner|medical director",
    r"general manager|director|vp|vice president|coo|cfo|administrator",
    r"office manager|practice manager|manager|operations",
]
JUNIOR = re.compile(r"\b(assistant|coordinator|associate|intern|specialist|representative)\b")

# What a homepage gives away. Pattern -> label. Lowercase match on raw HTML.
SITE_SIGNALS = {
    "meta_pixel": [r"connect\.facebook\.net", r"fbq\("],
    "google_ads": [r"googleadservices\.com", r"gtag\([^)]*['\"]aw-", r"\baw-\d{6,}"],
    "google_analytics": [r"googletagmanager\.com", r"google-analytics\.com"],
    "online_booking": [
        r"calendly\.com", r"zocdoc", r"nexhealth", r"localmed", r"acuityscheduling",
        r"squareup\.com/appointments", r"housecallpro", r"servicetitan", r"jobber",
        r"vagaro", r"mindbody", r"setmore", r"booksy", r"schedulicity", r"opencare",
        r"weave", r"book online", r"book now", r"schedule online", r"request an appointment",
    ],
    "chat_widget": [r"podium", r"birdeye", r"intercom", r"drift\.com", r"tidio",
                    r"livechat", r"hubspot.*conversations", r"tawk\.to"],
    "call_tracking": [r"callrail", r"calltrackingmetrics", r"invoca", r"whatconverts"],
    "ai_or_answering": [r"smith\.ai", r"ruby\.com", r"answering service", r"24/7 live"],
}


# ---------------------------------------------------------------- http

def _req(method: str, url: str, *, headers: dict | None = None, body: dict | None = None,
         timeout: int = 30) -> tuple[int, bytes]:
    data = json.dumps(body).encode() if body is not None else None
    h = {"User-Agent": UA}
    if data is not None:
        h["Content-Type"] = "application/json"
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, b""


def _json(raw: bytes):
    try:
        return json.loads(raw.decode("utf-8", "replace"))
    except ValueError:
        return None


# ---------------------------------------------------------------- search

def apify_search(query: str, location: str, per_location: int, max_usd: float) -> tuple[list, float]:
    token = os.environ.get("APIFY_TOKEN", "").strip()
    if not token:
        sys.exit("APIFY_TOKEN is not set. Use the no-key path in SKILL.md instead.")
    auth = {"Authorization": f"Bearer {token}"}
    params = urllib.parse.urlencode({"maxTotalChargeUsd": f"{max_usd:.2f}", "timeout": "900"})
    run_input = {
        "searchStringsArray": [query],
        "locationQuery": location if location.lower().endswith("usa") else f"{location}, USA",
        "maxCrawledPlacesPerSearch": per_location,
        "language": "en",
        "skipClosedPlaces": True,
        "scrapeContacts": True,
    }
    status, raw = _req("POST", f"{APIFY}/acts/{ACTOR}/runs?{params}", headers=auth, body=run_input)
    run = (_json(raw) or {}).get("data") or {}
    if status >= 400 or not run.get("id"):
        print(f"  Apify refused the run for {location} (HTTP {status}).", file=sys.stderr)
        return [], 0.0
    run_id, dataset = run["id"], run.get("defaultDatasetId")
    while str(run.get("status")) not in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
        time.sleep(6)
        status, raw = _req("GET", f"{APIFY}/actor-runs/{run_id}", headers=auth)
        run = (_json(raw) or {}).get("data") or run
    cost = float(run.get("usageTotalUsd") or 0)
    if run.get("status") in ("FAILED", "ABORTED"):
        print(f"  Run for {location} ended {run.get('status')} (spent ${cost:.2f}).", file=sys.stderr)
        return [], cost
    q = urllib.parse.urlencode({"clean": "true", "format": "json", "limit": str(per_location * 2)})
    status, raw = _req("GET", f"{APIFY}/datasets/{run.get('defaultDatasetId') or dataset}/items?{q}",
                       headers=auth, timeout=120)
    items = _json(raw) or []
    return (items if isinstance(items, list) else []), cost


def cmd_search(a) -> None:
    out, spent, seen = [], 0.0, set()
    for loc in a.location:
        left = a.max_usd - spent
        if left < 0.05:
            print("  Spend cap reached, stopping.", file=sys.stderr)
            break
        print(f"  Searching '{a.query}' in {loc} ...", file=sys.stderr)
        items, cost = apify_search(a.query, loc, a.per_location, min(left, a.max_usd_per_location))
        spent += cost
        for it in items:
            pid = it.get("placeId")
            if pid and pid not in seen and not it.get("permanentlyClosed"):
                seen.add(pid)
                out.append(it)
        print(f"  {len(items)} places, ${cost:.2f}", file=sys.stderr)
    with open(a.out, "w") as f:
        json.dump(out, f)
    print(f"Wrote {len(out)} unique places to {a.out}. Total Apify spend ${spent:.2f}.")


# ---------------------------------------------------------------- normalize

def e164(phone: str) -> str:
    raw = (phone or "").strip()
    if raw.startswith("+") and not raw.startswith("+1"):
        return ""
    d = re.sub(r"\D", "", raw)
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return "+1" + d if len(d) == 10 and d[0] not in "01" else ""


def domain_of(url: str) -> str:
    try:
        host = urllib.parse.urlparse(url if "://" in url else "http://" + url).hostname or ""
    except ValueError:
        return ""
    return host.lower().removeprefix("www.")


def _first(v):
    return v[0] if isinstance(v, list) and v else (v or "")


def normalize(item: dict) -> dict:
    """Accepts an Apify place or a hand-built row (name, phone, website, city, ...)."""
    g = lambda *ks: next((item.get(k) for k in ks if item.get(k) not in (None, "")), "")
    website = str(g("website", "url_site", "site"))
    if re.match(r"^[a-z][a-z0-9+.-]*:", website, re.I) and not website.lower().startswith(("http://", "https://")):
        website = ""  # javascript:, mailto:, tel: and friends are not websites
    elif website and not website.lower().startswith(("http://", "https://")):
        website = "https://" + website
    emails = item.get("emails") if isinstance(item.get("emails"), list) else [g("email")]
    emails = [str(e).strip().lower() for e in emails if e and "@" in str(e)]
    dist = item.get("reviewsDistribution") or {}
    low = (dist.get("oneStar") or 0) + (dist.get("twoStar") or 0) if isinstance(dist, dict) else 0
    hours = item.get("openingHours") or []
    weekend_closed = False
    if isinstance(hours, list) and hours:
        weekend = [h for h in hours if str(h.get("day", "")).lower() in ("saturday", "sunday")]
        weekend_closed = bool(weekend) and all("closed" in str(h.get("hours", "")).lower() for h in weekend)
    rating = g("totalScore", "rating")
    reviews = g("reviewsCount", "review_count", "reviews")
    return {
        "name": str(g("title", "name", "company")).strip(),
        "category": str(g("categoryName", "category")),
        "address": str(g("address")),
        "city": str(g("city")),
        "state": str(g("state")),
        "phone": e164(str(g("phoneUnformatted", "phone"))),
        "website": website,
        "domain": domain_of(website),
        "maps_url": str(g("url", "maps_url")) if "google" in str(g("url", "maps_url")) else "",
        "place_id": str(g("placeId", "place_id")),
        "rating": float(rating) if str(rating).replace(".", "", 1).isdigit() else "",
        "reviews": int(reviews) if str(reviews).isdigit() else "",
        "low_star_reviews": low or "",
        "unclaimed": bool(item.get("claimThisBusiness")),
        "weekend_closed": weekend_closed,
        "emails": emails[:5],
        "linkedin": str(_first(item.get("linkedIns"))),
        "facebook": str(_first(item.get("facebooks"))),
        "instagram": str(_first(item.get("instagrams"))),
    }


def load_rows(path: str) -> list[dict]:
    if path.endswith(".json"):
        data = json.load(open(path))
        return data if isinstance(data, list) else []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- enrich

def scan_site(url: str) -> dict:
    if not url:
        return {}
    status, raw = _req("GET", url, timeout=12)
    if status == 0 or status >= 400:
        return {"site_status": f"unreachable ({status or 'no response'})"}
    html = raw[:600_000].decode("utf-8", "replace").lower()
    found = {k: any(re.search(p, html) for p in pats) for k, pats in SITE_SIGNALS.items()}
    found["site_status"] = "ok"
    found["mobile_viewport"] = 'name="viewport"' in html
    m = re.findall(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", html)
    found["site_emails"] = sorted({e for e in m if not e.endswith((".png", ".jpg", ".webp"))})[:5]
    return found


def prospeo(domain: str) -> dict:
    key = os.environ.get("PROSPEO_API_KEY", "").strip()
    if not key or not domain:
        return {}
    status, raw = _req("POST", "https://api.prospeo.io/domain-search",
                       headers={"X-KEY": key}, body={"company": domain, "limit": 10}, timeout=20)
    if status >= 400 or status == 0:
        return {}
    items = ((_json(raw) or {}).get("response") or {}).get("email_list") or []
    best, best_rank = None, 99
    for it in items:
        name = f"{it.get('first_name') or ''} {it.get('last_name') or ''}".strip()
        title = str(it.get("position") or "").lower()
        if not name or "@" not in str(it.get("email") or ""):
            continue
        rank = len(SENIORITY) if JUNIOR.search(title) else next(
            (i for i, p in enumerate(SENIORITY) if re.search(rf"\b({p})\b", title)), len(SENIORITY))
        verified = str((it.get("verification") or {}).get("status") or "").upper() == "VALID"
        rank = rank * 2 + (0 if verified else 1)
        if rank < best_rank:
            best, best_rank = (name, it.get("position") or "", it["email"].lower(),
                               it.get("linkedin") or "", verified), rank
    if not best:
        return {}
    return {"contact_name": best[0], "contact_title": best[1], "email": best[2],
            "contact_linkedin": best[3], "email_status": "valid" if best[4] else ""}


def verify_email(email: str) -> str:
    key = os.environ.get("MILLIONVERIFIER_API_KEY", "").strip()
    if not key or not email:
        return ""
    q = urllib.parse.urlencode({"api": key, "email": email, "timeout": "10"})
    status, raw = _req("GET", f"https://api.millionverifier.com/api/v3/?{q}", timeout=20)
    result = str((_json(raw) or {}).get("result") or "").lower()
    return {"ok": "valid", "catch_all": "catch_all", "invalid": "invalid",
            "disposable": "invalid"}.get(result, "unknown")


def phone_type(num: str) -> str:
    key = os.environ.get("TELNYX_API_KEY", "").strip()
    if not key or not num:
        return ""
    status, raw = _req("GET", f"https://api.telnyx.com/v2/number_lookup/{urllib.parse.quote(num)}?type=carrier",
                       headers={"Authorization": f"Bearer {key}"}, timeout=15)
    data = (_json(raw) or {}).get("data") or {}
    if data.get("valid_number") is False:
        return "invalid"
    kind = str((data.get("carrier") or {}).get("type") or "").lower()
    return {"mobile": "mobile", "fixed line": "landline", "landline": "landline",
            "voip": "voip"}.get(kind, kind or "unknown")


# ---------------------------------------------------------------- rank

def reach_score(r: dict) -> int:
    s = 0
    if r.get("email") and r.get("email_status") == "valid":
        s += 40
    elif r.get("email") and r.get("email_status") == "catch_all":
        s += 20
    elif r.get("email") and r.get("email_status") != "invalid":
        s += 10
    if r.get("contact_name"):
        s += 20
    if r.get("phone"):
        s += 10 if r.get("phone_type") == "mobile" else 5
    return min(s, 70)


def need_signals(r: dict) -> list[str]:
    """Signals that the business is losing customers it already paid to get."""
    out = []
    rating, reviews = r.get("rating"), r.get("reviews")
    if isinstance(rating, float) and isinstance(reviews, int) and reviews >= 20 and rating < 4.2:
        out.append(f"rating {rating} on {reviews} reviews")
    elif isinstance(reviews, int) and reviews < 15:
        out.append(f"only {reviews} Google reviews")
    if isinstance(r.get("low_star_reviews"), int) and r["low_star_reviews"] >= 5:
        out.append(f"{r['low_star_reviews']} one and two star reviews")
    if r.get("unclaimed"):
        out.append("Google profile not claimed")
    if not r.get("website"):
        out.append("no website")
    if r.get("site_status", "").startswith("unreachable"):
        out.append("website down or blocking")
    if r.get("site_status") == "ok":
        if not r.get("online_booking"):
            out.append("no online booking on homepage")
        if (r.get("meta_pixel") or r.get("google_ads")) and not r.get("call_tracking"):
            out.append("pays for ads, no call tracking")
        if not r.get("mobile_viewport"):
            out.append("site not mobile ready")
    if r.get("weekend_closed"):
        out.append("closed weekends (calls go to voicemail)")
    return out


def cmd_rank(a) -> None:
    rows = [normalize(x) for x in load_rows(a.input)]
    rows = [r for r in rows if r["name"]]
    known = set()
    if a.known:
        for k in load_rows(a.known):
            n = normalize(k)
            known.update(v for v in (n["place_id"], n["domain"], n["phone"]) if v)
    kept, seen = [], set(known)
    for r in rows:
        keys = [v for v in (r["place_id"], r["domain"], r["phone"]) if v]
        if any(k in seen for k in keys):
            continue
        seen.update(keys)
        kept.append(r)
    chain = Counter(re.sub(r"[^a-z0-9]", "", r["name"].lower()) for r in kept)
    kept = [r for r in kept
            if not (a.min_reviews and isinstance(r["reviews"], int) and r["reviews"] < a.min_reviews)
            and not (a.require_website and not r["website"])
            and not (a.skip_chains and chain[re.sub(r"[^a-z0-9]", "", r["name"].lower())] >= 3)]
    print(f"{len(kept)} businesses after dedupe and filters.", file=sys.stderr)

    for i, r in enumerate(kept, 1):
        if a.scan_sites:
            r.update(scan_site(r["website"]))
        r.update(prospeo(r["domain"]))
        if not r.get("email"):
            pool = r["emails"] + r.get("site_emails", [])
            named = [e for e in pool if e.split("@")[0] not in ROLE_LOCALS]
            r["email"] = (named or pool or [""])[0]
            r["email_is_role"] = bool(r["email"]) and r["email"].split("@")[0] in ROLE_LOCALS
        if r["email"] and r.get("email_status") != "valid":
            r["email_status"] = verify_email(r["email"]) or r.get("email_status", "")
        r["phone_type"] = phone_type(r["phone"])
        if i % 10 == 0:
            print(f"  enriched {i}/{len(kept)}", file=sys.stderr)

    out = []
    for r in kept:
        reach_ok = (r.get("email") and r.get("email_status") != "invalid") or \
                   (r.get("phone") and r.get("phone_type") != "invalid")
        if not reach_ok:
            continue
        needs = need_signals(r)
        r["reach_score"] = reach_score(r)
        r["need_score"] = min(len(needs) * 10, 30)
        r["priority"] = r["reach_score"] + r["need_score"]
        r["grade"] = "A" if r["priority"] >= 70 else "B" if r["priority"] >= 40 else "C"
        r["signals"] = "; ".join(needs)
        out.append(r)
    out.sort(key=lambda r: r["priority"], reverse=True)

    cols = ["grade", "priority", "name", "contact_name", "contact_title", "email", "email_status",
            "email_is_role", "phone", "phone_type", "website", "city", "state", "category",
            "rating", "reviews", "signals", "meta_pixel", "google_ads", "online_booking",
            "chat_widget", "call_tracking", "maps_url", "place_id", "contact_linkedin",
            "linkedin", "facebook", "instagram"]
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in out:
            w.writerow({c: r.get(c, "") for c in cols})
    grades = Counter(r["grade"] for r in out)
    print(f"Wrote {len(out)} reachable leads to {a.out}: "
          f"{grades['A']} A, {grades['B']} B, {grades['C']} C.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.add_argument("--location", action="append", required=True)
    s.add_argument("--per-location", type=int, default=60)
    s.add_argument("--max-usd", type=float, default=5.0, help="hard cap across all locations")
    s.add_argument("--max-usd-per-location", type=float, default=3.0)
    s.add_argument("--out", default="raw.json")
    r = sub.add_parser("rank")
    r.add_argument("--in", dest="input", required=True, help="Apify JSON or a CSV/JSON list you built")
    r.add_argument("--out", default="leads.csv")
    r.add_argument("--known", help="CSV of leads you already have; they are skipped")
    r.add_argument("--min-reviews", type=int, default=0)
    r.add_argument("--require-website", action="store_true")
    r.add_argument("--skip-chains", action="store_true", help="drop names that appear 3+ times")
    r.add_argument("--scan-sites", action="store_true", help="fetch each homepage for pixels/booking/chat")
    a = p.parse_args()
    cmd_search(a) if a.cmd == "search" else cmd_rank(a)


if __name__ == "__main__":
    main()

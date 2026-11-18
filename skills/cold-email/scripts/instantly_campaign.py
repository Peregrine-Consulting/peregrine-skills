#!/usr/bin/env python3
"""Check a cold email sequence and, if asked, create it in Instantly as a DRAFT.

Stdlib only. Default is a dry run: lint the copy and print the API payload.
Nothing is ever activated or sent. Activating the campaign is a human click
inside Instantly, after the user has read every email.

  python3 instantly_campaign.py sequence.json                  # lint + print payload
  python3 instantly_campaign.py sequence.json --create         # needs INSTANTLY_API_KEY

sequence.json:
{
  "name": "dentists-az angle-missed-calls v1",
  "timezone": "America/Phoenix",
  "window": ["08:00", "16:30"],
  "daily_limit": 60,
  "sending_accounts": ["sam@trynorthline.com", "sam@getnorthline.com"],
  "steps": [
    {"day": 0, "subject": "calls after 5 at {{companyName}}", "body": "Hi {{firstName|there}},\\n\\n..."},
    {"day": 3, "subject": "", "body": "..."}
  ],
  "footer": "Not a fit? Reply \\"no thanks\\" and I'll stop.\\nNorthline, 100 Main St, Phoenix, AZ 85004"
}

The Instantly v2 campaign schema was read in November 2026. If the API
rejects the payload, read https://api.instantly.ai/openapi/api_v2.json and
fix the field, do not guess.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.instantly.ai/api/v2"

SPAM_WORDS = [
    "free", "guarantee", "guaranteed", "act now", "limited time", "risk-free", "risk free",
    "100%", "no obligation", "click here", "buy now", "cash", "earn", "$$$", "winner",
    "urgent", "exclusive deal", "special promotion", "increase sales", "double your",
]
OPENER_CLICHES = ["hope this finds you", "hope you're well", "hope you are well",
                  "my name is", "i wanted to reach out", "quick question", "touching base",
                  "just following up", "circle back", "bump"]


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9'{}|]+", text))


def lint(seq: dict) -> list[str]:
    problems: list[str] = []
    steps = seq.get("steps") or []
    footer = seq.get("footer") or ""
    if not steps:
        return ["no steps"]
    if not re.search(r"(reply|unsubscribe|opt out|stop)", footer, re.I):
        problems.append("footer: needs an opt-out line (reply 'no thanks' or similar)")
    if not re.search(r"\d{5}", footer):
        problems.append("footer: needs a physical mailing address (CAN-SPAM)")
    days = [s.get("day", 0) for s in steps]
    if days != sorted(days) or days[0] != 0:
        problems.append("steps: days must start at 0 and increase")
    if len(steps) > 5:
        problems.append(f"steps: {len(steps)} emails; 4 or 5 is the useful range, more mostly adds complaints")
    for i, s in enumerate(steps, 1):
        body, subj = s.get("body") or "", s.get("subject") or ""
        tag = f"email {i}"
        n = words(body)
        if n > 110:
            problems.append(f"{tag}: {n} words; keep cold emails under about 90")
        if "—" in body + subj or "–" in body + subj:
            problems.append(f"{tag}: long dash; use a comma or full stop")
        if i == 1 and re.search(r"https?://|www\.|\{\{[^}]*link[^}]*\}\}", body, re.I):
            problems.append(f"{tag}: links in the first email hurt inbox placement; move them to email 2+")
        if i == 1 and not subj:
            problems.append(f"{tag}: first email needs a subject")
        if i > 1 and subj:
            problems.append(f"{tag}: leave the subject blank so it sends in the same thread (unless this is a deliberate new thread)")
        if subj and (len(subj.split()) > 7 or subj != subj.lower() and not re.search(r"\{\{", subj)):
            problems.append(f"{tag}: subject should be short and lowercase, like a colleague would write")
        low = (subj + " " + body).lower()
        for w in SPAM_WORDS:
            if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", low):
                problems.append(f"{tag}: spam-trigger phrase '{w}'")
        for c in OPENER_CLICHES:
            if c in low:
                problems.append(f"{tag}: cliche '{c}'")
        if re.search(r"\$\s?\d", body) and i == 1:
            problems.append(f"{tag}: no prices in a first touch")
        if re.search(r"<[a-z][^>]*>", body, re.I):
            problems.append(f"{tag}: HTML found; send plain text")
        for var in re.findall(r"\{\{\s*(firstName|first_name)\s*\}\}", body):
            problems.append(f"{tag}: {{{{{var}}}}} has no fallback; write {{{{firstName|there}}}}")
    return problems


def payload(seq: dict) -> dict:
    footer = seq.get("footer") or ""
    steps = seq["steps"]
    api_steps = []
    for idx, s in enumerate(steps):
        nxt = steps[idx + 1]["day"] if idx + 1 < len(steps) else s["day"]
        body = (s.get("body") or "").rstrip() + ("\n\n" + footer if footer else "")
        api_steps.append({
            "type": "email",
            # Instantly's delay is the wait in days before the NEXT step is sent.
            "delay": max(nxt - s["day"], 0),
            "variants": [{"subject": s.get("subject") or "", "body": body}],
        })
    start, end = seq.get("window") or ["08:00", "16:30"]
    return {
        "name": seq["name"],
        "campaign_schedule": {"schedules": [{
            "name": "Weekdays",
            "timing": {"from": start, "to": end},
            "days": {"0": False, "1": True, "2": True, "3": True, "4": True, "5": True, "6": False},
            "timezone": seq.get("timezone") or "America/Chicago",
        }]},
        "sequences": [{"steps": api_steps}],
        "email_list": seq.get("sending_accounts") or [],
        "daily_limit": int(seq.get("daily_limit") or 50),
        "stop_on_reply": True,
        "stop_on_auto_reply": False,
        "link_tracking": False,
        "open_tracking": False,
        "text_only": True,
        "insert_unsubscribe_header": True,
    }


def create(body: dict) -> None:
    key = os.environ.get("INSTANTLY_API_KEY", "").strip()
    if not key:
        sys.exit("INSTANTLY_API_KEY is not set. The dry-run payload above can be pasted into Instantly by hand.")
    req = urllib.request.Request(f"{API}/campaigns", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            out = json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        sys.exit(f"Instantly refused the campaign (HTTP {e.code}): {detail}")
    print(f"Created DRAFT campaign '{out.get('name')}' id {out.get('id')}. "
          "It is not active. Review it in Instantly, add leads, then activate by hand.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sequence")
    p.add_argument("--create", action="store_true", help="create as a draft in Instantly")
    p.add_argument("--force", action="store_true", help="create even with lint problems")
    a = p.parse_args()
    seq = json.load(open(a.sequence))
    problems = lint(seq)
    if problems:
        print("Copy problems:")
        for x in problems:
            print("  - " + x)
    else:
        print("Copy check: clean.")
    body = payload(seq)
    print(json.dumps(body, indent=2))
    if a.create:
        if problems and not a.force:
            sys.exit("Not creating: fix the problems above or pass --force with the user's OK.")
        create(body)


if __name__ == "__main__":
    main()

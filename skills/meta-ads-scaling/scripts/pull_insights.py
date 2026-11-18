#!/usr/bin/env python3
"""Read-only pull of Meta ad account data for the meta-ads-scaling skill.

Stdlib only. Reads META_ACCESS_TOKEN and META_AD_ACCOUNT_ID (with or without
the act_ prefix) from the environment. Never prints the token.

  python3 pull_insights.py --days 30 --out insights.csv
  python3 pull_insights.py --activities --days 14 --out activities.csv

The API version defaults to META_API_VERSION or the value below; check
references/meta-fields.md for the date it was last verified.
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_VERSION = os.environ.get("META_API_VERSION", "v23.0")
BASE = f"https://graph.facebook.com/{API_VERSION}"

INSIGHT_FIELDS = [
    "campaign_id", "campaign_name", "adset_id", "adset_name", "ad_id", "ad_name",
    "spend", "impressions", "reach", "frequency", "inline_link_clicks", "clicks",
    "actions", "action_values", "cost_per_action_type",
]
# Action types flattened into their own columns. Everything else stays in actions_json.
ACTION_COLUMNS = {
    "lead": "leads",
    "onsite_conversion.lead_grouped": "leads_onsite",
    "offsite_conversion.fb_pixel_lead": "leads_pixel",
    "landing_page_view": "landing_page_views",
    "purchase": "purchases",
    "add_to_cart": "add_to_cart",
    "initiate_checkout": "initiate_checkout",
}


def die(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def get(url, params, token):
    params = dict(params)
    params["access_token"] = token
    full = url + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(full, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            # Rate limit codes: back off and retry.
            if e.code in (400, 429, 500, 503) and ('"code":17' in body or '"code":4' in body or e.code >= 500):
                time.sleep(2 ** attempt * 5)
                continue
            die(f"Meta API error {e.code}: {body[:500]}")
        except urllib.error.URLError as e:
            time.sleep(2 ** attempt)
            last = e
    die("Meta API kept failing after retries.")


def paged(url, params, token):
    data = get(url, params, token)
    while True:
        for row in data.get("data", []):
            yield row
        nxt = data.get("paging", {}).get("next")
        if not nxt:
            return
        # The next URL already carries the token and params.
        with urllib.request.urlopen(nxt, timeout=60) as r:
            data = json.loads(r.read().decode())


def pull_insights(account, token, days, out):
    until = dt.date.today() - dt.timedelta(days=1)  # today is never complete
    since = until - dt.timedelta(days=days - 1)
    rows = []
    for level in ("ad", "adset", "campaign"):
        params = {
            "level": level,
            "fields": ",".join(INSIGHT_FIELDS),
            "time_range": json.dumps({"since": since.isoformat(), "until": until.isoformat()}),
            "time_increment": 1,
            "use_unified_attribution_setting": "true",
            "limit": 500,
        }
        for r in paged(f"{BASE}/{account}/insights", params, token):
            actions = {a["action_type"]: a.get("value") for a in r.get("actions", [])}
            values = {a["action_type"]: a.get("value") for a in r.get("action_values", [])}
            out_row = {
                "level": level,
                "day": r.get("date_start"),
                "campaign_id": r.get("campaign_id"), "campaign_name": r.get("campaign_name"),
                "adset_id": r.get("adset_id", ""), "adset_name": r.get("adset_name", ""),
                "ad_id": r.get("ad_id", ""), "ad_name": r.get("ad_name", ""),
                "spend": r.get("spend"), "impressions": r.get("impressions"),
                "reach": r.get("reach"), "frequency": r.get("frequency"),
                "link_clicks": r.get("inline_link_clicks"), "clicks_all": r.get("clicks"),
                "purchase_value": values.get("purchase") or values.get("offsite_conversion.fb_pixel_purchase", ""),
                "actions_json": json.dumps(actions, sort_keys=True),
            }
            for atype, col in ACTION_COLUMNS.items():
                out_row[col] = actions.get(atype, "")
            rows.append(out_row)
    write_csv(out, rows)
    print(f"Wrote {len(rows)} rows ({since} to {until}) to {out}")


def pull_activities(account, token, days, out):
    since = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).timestamp())
    params = {
        "fields": "event_time,event_type,object_id,object_name,object_type,extra_data,actor_name",
        "since": since,
        "limit": 500,
    }
    keep = ("budget", "status", "create", "run_status", "bid")
    rows = []
    for r in paged(f"{BASE}/{account}/activities", params, token):
        et = r.get("event_type", "")
        if not any(k in et for k in keep):
            continue
        rows.append({
            "time": r.get("event_time"),
            "event_type": et,
            "object_type": r.get("object_type"),
            "object_id": r.get("object_id"),
            "object_name": r.get("object_name"),
            "extra_data": r.get("extra_data", ""),
            # Names of people are not needed for decisions; keep only whether a person acted.
            "actor": "person" if r.get("actor_name") else "meta_or_system",
        })
    write_csv(out, rows)
    print(f"Wrote {len(rows)} activity rows to {out}")


def write_csv(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if not rows:
        open(path, "w").close()
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--out", required=True)
    p.add_argument("--activities", action="store_true", help="pull the change history instead of insights")
    a = p.parse_args()
    token = os.environ.get("META_ACCESS_TOKEN")
    account = os.environ.get("META_AD_ACCOUNT_ID")
    if not token or not account:
        die("Set META_ACCESS_TOKEN and META_AD_ACCOUNT_ID, or use an Ads Manager CSV export instead.")
    if not account.startswith("act_"):
        account = "act_" + account
    if a.activities:
        pull_activities(account, token, a.days, a.out)
    else:
        pull_insights(account, token, a.days, a.out)


if __name__ == "__main__":
    main()

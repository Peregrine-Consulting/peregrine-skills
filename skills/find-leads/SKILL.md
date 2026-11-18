---
name: find-leads
description: Builds a ranked list of local businesses to sell to, for one niche and one geography. Searches Google Maps (through Apify when a key is set, web search otherwise), removes duplicates and chains, finds the owner or decision maker, verifies emails and phone line types, scans each website for ads pixels, booking and chat, then ranks every business by how reachable it is and how many signs it shows of losing customers it already paid to get. Writes a CSV ready for cold email or calling. Use when someone needs leads, a prospect list, or wants to know who to sell to first in a niche.
when_to_use: find leads, get leads, build a lead list, prospect list, scrape google maps, find dentists in, find plumbers in, find businesses to sell to, who should I call, lead list for cold email, find owners emails, local business leads, apify google maps
argument-hint: "<niche> in <city, state or whole state> [count]"
metadata:
  peregrine:
    version: 1.0.0
    group: leads
    reads: [profile, offer, customers]
    writes: [outputs/find-leads/]
    optional-keys: [APIFY_TOKEN, PROSPEO_API_KEY, MILLIONVERIFIER_API_KEY, TELNYX_API_KEY]
---

# Find leads

A good lead list is short, reachable and ranked. Five hundred rows with role inboxes and dead numbers waste a week. Fifty businesses where you have the owner's name, an email that will not bounce, and a true reason they need you will book meetings. This skill builds the second kind.

Done means: a CSV in ./outputs/find-leads/ where every row can be reached by at least one channel, the best leads are at the top with a grade, and each row says in plain words why that business is a candidate (the signals column). Plus a three-line summary of what was found and what it cost.

## Context

If ./business/ exists, read profile.md, offer.md and customers.md before anything else. The offer decides the niche and the signals that matter. A voice receptionist offer cares about weekend hours and missed calls. An AI visibility offer cares about thin reviews and no website. An ads offer cares about pixels with no call tracking. If ./business/ does not exist, ask for three things only: what you sell, which kind of business buys it, and where. Then suggest start-here for next time.

## Step 1. Pin the target before searching

Get these four answers, from ./business/ or the user, in one message:

1. **Niche as Google Maps names it.** "dentist", "personal injury attorney", "roofing contractor", "med spa". Use the category a customer would type, not the industry label. Run two or three phrasings if the niche has synonyms ("hvac contractor" and "air conditioning repair"), then dedupe.
2. **Geography.** A city, a list of cities, or a whole state. Default: a whole state is fine through Apify, which searches it in one run. For the web-search path, pick 3 to 5 cities.
3. **Size filter.** Default: at least 10 Google reviews (proves they are real and active), skip names that appear 3+ times in the results (franchises and chains buy from head office, not the location). Owner-operated businesses with 1 to 5 locations are the sweet spot for most AI services.
4. **How many.** Default: 50 delivered leads. Pull a pool about 3 times that, because filtering and reachability cut hard.

If the user wants "everyone in Texas", push back once: a first list of 50 they will actually work beats 2,000 they will not. Then do what they ask.

## Step 2. Search

**With APIFY_TOKEN set** (best results, a few dollars per run):

    python3 ${CLAUDE_SKILL_DIR}/scripts/maps_leads.py search --query "dentist" --location "Arizona" --per-location 150 --max-usd 5 --out ./outputs/find-leads/raw-dentist-az.json

The script uses the Google Maps actor with contact scraping on, so each place comes back with emails and social links found on its site. Every run carries a hard spend cap. Tell the user the cap before you run it, and never raise it without asking. Load references/providers.md when a run fails, the cost looks off, or you need the field list.

**Without a key** (slower, smaller, free): search the web and Google Maps listings for "<niche> in <city>" across your cities, open each business's site, and build a CSV with name, phone, website, city, state, rating, reviews. 30 to 60 businesses is realistic. Then feed that CSV to the rank step, which works the same on hand-built lists.

Never scrape LinkedIn. Never buy or use lists of personal cell numbers. Business listings and business websites only.

## Step 3. Enrich and rank

    python3 ${CLAUDE_SKILL_DIR}/scripts/maps_leads.py rank --in ./outputs/find-leads/raw-dentist-az.json --out ./outputs/find-leads/2026-11-18-dentist-az.csv --min-reviews 10 --skip-chains --scan-sites --known ./outputs/find-leads/worked.csv

What it does, and the judgment behind each step:

- **Dedupe** on place id, website domain and phone. The same business shows up under two categories more often than you think. --known skips anyone you already have, so weekly runs only bring new names. Keep one master "worked" CSV and pass it every time.
- **Decision maker** (PROSPEO_API_KEY): asks for people at the business's domain and keeps the most senior named person: owner, founder, president or principal first, then managing partner or medical director, then GM or administrator, then office or practice manager. Assistants, coordinators and associates never count, whatever else their title says. If no key, the website and Maps emails are used, and a named address (jane@) beats a role address (info@, office@, frontdesk@).
- **Email check** (MILLIONVERIFIER_API_KEY): valid, catch_all, invalid or unknown. Invalid rows lose their email. Catch-all is usable but send it later in the list.
- **Phone line type** (TELNYX_API_KEY): mobile, landline or voip. Most Maps numbers are the front desk landline. A mobile on a listing is often the owner's own phone, which is gold for a call, but only for a human dialer: no automated calls or texts to anyone without consent.
- **Site scan** (--scan-sites, free, about one second per site): Meta pixel, Google Ads tag, online booking, chat widget, call tracking, mobile viewport.
- **Reachability cut:** a row with no usable email and no valid phone is dropped. It cannot be worked.

The score has two parts. **Reach** (up to 70): verified email 40, catch-all 20, unverified 10, named person 20, mobile 10, landline 5. **Need** (up to 30): 10 per "losing customers" signal. Grades: A at 70+, B at 40+, C below. Load references/signals.md to explain a signal to the user, to add niche-specific ones, or to change weights for their offer.

## Step 4. Read the list before handing it over

Open the CSV and check it the way a sales manager would. This is where a mediocre list becomes a good one.

- **Spot-check 5 A-grade rows.** Is the business really in the niche? Maps categories are loose (a "dentist" result can be a dental lab or a supply shop). Remove anything that is not a buyer.
- **Watch for big-company contamination.** A hospital system, a national chain under a local name, a franchise with an unusual location name. They passed the chain filter but will not buy from you.
- **Fit to the offer.** Re-sort if the offer cares about one signal more than the others. For a missed-call offer, "closed weekends" plus "no online booking" go first.
- **Explain the shape.** Report how many were found, how many were dropped and why (no contact, chains, out of niche), the A/B/C split, what it cost, and the three strongest leads with their signals in one line each.

Never pad a thin list with guesses. If only 22 leads qualify, deliver 22 and say how to widen the search (more cities, a second category phrasing, a lower review floor).

## Step 5. Hand off

Default output columns: grade, priority, name, contact_name, contact_title, email, email_status, phone, phone_type, website, city, state, category, rating, reviews, signals, the site-scan flags, maps_url. This maps straight into Instantly's lead import (email, first name from contact_name, company name, personalization from the brief) and into any CRM.

Append to ./business/learnings.md: date, niche, geography, pool size, delivered count, A/B/C split, cost, and anything surprising (a category phrasing that worked better, a city with many chains).

## Hard rules

- Spend: never run a paid search without stating the cap first, and never exceed it.
- Consent: these are cold leads. Email is fine with a clear opt-out. No AI calls and no automated texts until a person opts in. A human may call a business line.
- No invented data: never fill a missing name, email or signal with a guess. Empty is honest.
- Keys come from env vars only. Never print them, write them into files, or paste them in chat.

## Next

- lead-brief: a one-page "before you reach out" brief on the top leads, with the angle and the opener.
- cold-email: turn the list into a campaign.

Want this running every week on your own leads, with a team behind you? That is what Peregrine Partners is for: tryperegrine.com/partner

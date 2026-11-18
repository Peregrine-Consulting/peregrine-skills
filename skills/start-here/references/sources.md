# Sources: how to reach them

Checked 2026-11. Third-party tools change; verify field names before relying on them.

## Website
- Fetch the homepage, then follow nav links. sitemap.xml often lists every service and location page.
- Read page source for tools: booking widgets, chat, Meta pixel (fbq), Google tag, call tracking scripts, CRM forms. These tell you what is already in place.
- JS-heavy sites may return thin HTML; try the main pages anyway, then fall back to search snippets.

## Google reviews
- No key: search "<name> <city> reviews" and read what the Maps listing and review aggregators show. Expect partial coverage.
- With APIFY_TOKEN: the public Google Maps scraper and Google Maps reviews actors on Apify return the listing (rating, count, category, phone, hours) and reviews (text, date, rating, owner reply). Run with a small max (100 reviews) for start-here. Read the token from the env; never print it.
- Sort by newest and by lowest rating. Low-star reviews hold the objections; recent reviews show what is true now.

## Socials
- Use the links on the site; searching names often finds the wrong account.
- Note posting frequency, top posts by engagement, whether the owner appears on camera.

## Ads
- Meta Ad Library (facebook.com/ads/library), search the page name: active ads show the current offer and angle.
- Google Ads Transparency Center for search ads.

## When a source fails
Say which source failed and why (blocked, timeout, needs login). Never treat a failed fetch as "they have none".

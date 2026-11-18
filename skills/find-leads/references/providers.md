# Lead providers: endpoints, fields, costs

Checked November 2026. APIs change. If a call returns an unexpected shape, read the provider's current docs before guessing.

Load this when a run fails, a cost looks wrong, or you need to map a field.

## Apify, Google Maps (APIFY_TOKEN)

- Actor: compass~crawler-google-places (override with APIFY_MAPS_ACTOR).
- Start: POST https://api.apify.com/v2/acts/{actor}/runs?maxTotalChargeUsd={cap}&timeout=900, header Authorization: Bearer {token}, JSON input.
- Poll: GET /v2/actor-runs/{runId} until status is SUCCEEDED, FAILED, ABORTED or TIMED-OUT. usageTotalUsd is the spend so far. A failed run still bills what it spent.
- Items: GET /v2/datasets/{datasetId}/items?clean=true&format=json&limit=N
- Input used: searchStringsArray [niche], locationQuery ("Arizona, USA" searches the whole state), maxCrawledPlacesPerSearch, language en, skipClosedPlaces true, scrapeContacts true (adds emails and socials from the website, costs a little more).
- Fields used: title, placeId, address, city, state, phoneUnformatted, website, url (Maps link), categoryName, totalScore, reviewsCount, reviewsDistribution (oneStar..fiveStar), openingHours, claimThisBusiness, permanentlyClosed, emails, linkedIns, facebooks, instagrams. Not every field appears on every place.
- Cost: pay per result. Budget a few dollars per 100 to 200 places with contacts on. maxTotalChargeUsd is the real ceiling; set it every time.
- Why Apify and not the Google Places API: Places terms restrict storing results in your own database and CRM. A Maps scraper over public listings is the common path for lead lists.

## Prospeo, decision maker at a domain (PROSPEO_API_KEY)

- POST https://api.prospeo.io/domain-search, header X-KEY, body {"company": "<domain>", "limit": 10}.
- Response: response.email_list[] with first_name, last_name, position, email, linkedin, verification.status (VALID when verified).
- A 400 with error true and NO_RESULT means nobody found. Not a failure, do not retry.
- Small local businesses often return nobody. Expect 30 to 50 percent fill on trades and clinics, more on firms with LinkedIn presence.
- Optional second step in the waterfall: LeadMagic (email finder by name + domain) for rows where Prospeo found the company but no named person. Add it only if the user has a key.

## MillionVerifier, email check (MILLIONVERIFIER_API_KEY)

- GET https://api.millionverifier.com/api/v3/?api={key}&email={email}&timeout=10
- result: ok -> valid, catch_all -> catch_all, invalid or disposable -> invalid, anything else -> unknown.
- The key travels in the URL. Never log the URL or paste it into an error message.
- Bulk lists: their file upload is cheaper per check than single calls for 5,000+ rows.

## Telnyx Number Lookup, line type (TELNYX_API_KEY)

- GET https://api.telnyx.com/v2/number_lookup/{+1E164}?type=carrier, Bearer auth.
- data.valid_number false -> invalid. data.carrier.type: mobile, fixed line, voip.
- Small per-lookup fee. Skip it for email-only campaigns.

## Free fallbacks

- Web search "<niche> <city>" and the Maps listing in a browser give name, phone, site, rating, review count.
- The business's own site: /contact, /about, /team pages usually name the owner or doctor or attorney. Footer emails are common on trades sites.
- State licensing boards (dentists, attorneys, contractors, med spas) list licensees and sometimes owners. Good for confirming a name, never for scraping personal contact details.

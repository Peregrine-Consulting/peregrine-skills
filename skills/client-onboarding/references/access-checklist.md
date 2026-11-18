# Access checklist by offer

Load this when building access.csv. Pick the sections for what was sold. Every item is granted to us as a user or partner on the client's own account. The client keeps ownership of everything; we never create ad accounts, domains or phone numbers in our name for them unless the agreement says so.

Last checked: 2026-11. Platform menus move; if a path below is wrong, describe the goal ("add us as a partner with ad account access") and let the client find it.

## Paid ads (Meta)

- Meta Business Manager: client adds our business as a Partner (Business settings, Partners) with access to the ad account, Page, Instagram account, pixel / dataset. Partner access beats adding individuals: it survives staff changes on our side.
- Ad account: payment method on file and owned by the client; confirm the daily spend limit they are comfortable with.
- Pixel / dataset and Conversions API: who installed it, which events fire, whether the domain is verified.
- Customer list for exclusions (CSV, or a synced audience).
- Verify: we can see the ad account, create a draft ad, and see events in Events Manager.

## Google (ads, analytics, search console, business profile)

- Google Ads: link our manager account (MCC) or add our user with Standard access.
- Google Analytics 4: add our user as Editor on the property.
- Search Console: add our user as Full on the domain property.
- Google Business Profile: add us as Manager (not Owner).
- Tag Manager: Publish access if we will install tracking.
- Verify: we can see the last 30 days in each.

## Website and domain

- Domain registrar and DNS: either a delegate/user invite, or the client makes DNS changes we send them. Record which; DNS changes often need a code sent to the owner's phone, so plan for the owner to be reachable.
- Website platform (WordPress, Webflow, Shopify, Squarespace, a code repository): our own user with editor or developer role.
- Hosting: only if we will deploy.
- Verify: make a harmless draft change and delete it.

## AI voice and phones

- Phone system (RingCentral, Dialpad, a carrier, a PBX): admin user or a named contact who can set forwarding and transfers.
- Numbers: list each with its job and a decision per number: keep, forward to the AI line, port to a new provider, or retire. Porting needs the account number, PIN and a recent bill from the client; it takes days to weeks, so start it in week 1 if needed.
- Business texting registration (US 10DLC): legal business name, EIN, business address, website, sample messages and how consent is collected. Registration can take 1 to 3 weeks; start it in week 1. No texts from a new number until it is approved.
- Transfer targets: who takes live transfers, their direct numbers, hours, and the fallback when nobody answers.
- Calendar or scheduling system the AI books into, with a test calendar or test provider for setup.
- Practice management or EHR (medical): only through an integration the vendor supports, and only with a signed BAA covering every vendor that will touch patient information.
- Verify: place a test call end to end, including a transfer and an after-hours call.

## CRM and automations

- CRM (HubSpot, GoHighLevel, Salesforce, Pipedrive, a practice system): our user with the lowest role that can do the work, plus an API key created by the client for our integration in their own account, stored in their vault or ours, never in a doc.
- Calendar: booking link, or calendar sharing for the people who take calls.
- Verify: create a test contact, move it through a stage, delete it.

## Email outreach

- Separate sending domains (never cold email from the client's main domain), bought in the client's name or ours per the agreement.
- Mailboxes on those domains, warmed for 2 to 3 weeks before real sends.
- The client's main domain DNS: SPF, DKIM and DMARC set up correctly even if we never send from it.
- Verify: test send to a seed list, check it lands in the inbox.

## AI visibility and SEO

- Search Console and analytics (above), Business Profile (above), website editor (above).
- Review platforms they care about: login or a contact who can reply to reviews.

## For every client

- Shared folder or channel for files.
- Who receives updates, and who must never be contacted by AI calls or texts.
- Where invoices go.

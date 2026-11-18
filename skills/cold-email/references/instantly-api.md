# Instantly API v2 notes

Read from Instantly's public docs in November 2026. Load when creating a campaign through the API, importing leads, or wiring reply webhooks. If a call fails, check the OpenAPI spec at https://api.instantly.ai/openapi/api_v2.json before changing anything.

## Basics

- Base URL: https://api.instantly.ai/api/v2
- Auth: header Authorization: Bearer <INSTANTLY_API_KEY>. v1 keys do not work on v2.
- A 402 means the workspace has no active paid plan. Webhooks need a higher plan tier.
- Rate limit: about 100 requests a second and 6,000 a minute per workspace. Listing emails is much tighter (about 20 a minute).

## Campaigns

- POST /campaigns creates a campaign. It is created inactive. The script in this skill never calls the activate endpoint. Activation is a human action in the app after review.
- Fields used by the script: name, campaign_schedule.schedules[] (name, timing.from, timing.to, days 0-6, timezone), sequences[0].steps[] (type email, delay in days before the next step, variants[] with subject and body), email_list (sending inboxes), daily_limit, stop_on_reply, link_tracking, open_tracking, text_only, insert_unsubscribe_header.
- Timezone must be one of Instantly's accepted values. If it is rejected, pick the nearest listed zone from the spec.
- A blank subject on steps 2+ sends them as replies in the same thread.

## Leads

- POST /leads/add adds leads in bulk to a campaign or list (up to 1,000 per call; send an idempotency key so a retry does not duplicate).
- Standard fields: email, first_name, last_name, company_name, website, phone, personalization.
- Anything else goes in custom variables with the same name you use in the copy ({{persona_line}}, {{demo_link}}).
- Only add leads after the copy is approved and the user says go. Adding leads to an active campaign starts sending.

## Replies and status

- Webhooks: create one for reply_received and lead_interested events, pointed at the user's own endpoint. Payloads carry the lead email, campaign and an email id.
- POST /emails/reply replies in thread (reply_to_uuid from the webhook's email id, eaccount = the sending inbox).
- GET /emails?lead=<email>&email_type=received finds the latest reply when a webhook had no email id.
- POST /leads/update-interest-status sets interest by lead email: 1 interested, 2 meeting booked, 3 meeting completed, 4 won, 0 out of office, -1 not interested, -2 wrong person, -3 lost.
- POST /block-lists-entries stops all sending to an address workspace-wide. Use it for every unsubscribe.

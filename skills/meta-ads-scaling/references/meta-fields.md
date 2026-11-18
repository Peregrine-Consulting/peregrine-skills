# Meta fields and export columns

Last checked: 2026-11. Load this when mapping an Ads Manager export or the API's action types, or when the pull script errors on a field. Meta renames things; if a field is missing, check the current Marketing API Insights reference and update this file and the script's API_VERSION.

## Token

A System User token from Business Settings with ads_read on the ad account is enough. Never use a personal token that expires in an hour for a recurring review. Write access (ads_management) is not needed for this skill.

## Export column to metric

| Ads Manager column | Metric | API field / action type |
|---|---|---|
| Amount spent | spend | spend |
| Impressions | impressions | impressions |
| CPM (cost per 1,000 impressions) | computed: spend / impressions x 1000 | compute, do not trust the rounded column |
| Link clicks | link clicks | inline_link_clicks |
| Clicks (all) | all clicks, includes likes and profile taps | clicks. Do not use for the funnel |
| Landing page views | landing page views | action landing_page_view |
| Leads | leads | action lead (rollup); else onsite_conversion.lead_grouped + offsite_conversion.fb_pixel_lead. Pick one rule and keep it |
| Purchases | purchases | action purchase |
| Purchase conversion value | revenue (ecommerce) | action_values purchase |
| Adds to cart | add to cart | action add_to_cart |
| Checkouts initiated | initiate checkout | action initiate_checkout |
| Instant form opens | form opens | not one documented name; look in the actions the account actually returns and pick the form-open type there. Never guess |

## Attribution

use_unified_attribution_setting=true makes numbers match Ads Manager. Incremental attribution, where the account has it, is a separate attribution setting; when an account does not return it, the skill says "not available" instead of filling it in.

## Audience segments

The new / engaged / existing split comes from the user_segment_key breakdown, documented for Advantage+ shopping and sales campaigns. Lead-gen accounts usually do not return it. Report "not available for this account" rather than estimating.

## Activities (change history)

GET act_<id>/activities returns budget, status and creation events with event_time. Daily budgets arrive in the account currency's minor unit (cents) inside extra_data. Changes made by Meta's own automation show without a person actor.

## Gotchas

- Today's row is always partial. Reviews use complete days only.
- Days are in the ad account's time zone (date_start), not UTC.
- Deleted ads disappear from the structure but keep their insights rows; keep names from the insights pull.
- Campaign budget (Advantage campaign budget) means the campaign is the budget owner, not the ad set.

# Fix library

Load this in Phase 4 (diagnosis and fixes). Each fix lists the evidence that justifies it. Recommend a fix only when the audit shows that evidence. A generic list of every AEO tactic is the mark of a weak audit.

Order fixes by leverage: blockers first (nothing else matters until they are gone), then fixes that copy what the winners demonstrably have, then slow authority work.

## Tier 1: blockers (hours, huge payoff)

| Evidence | Fix |
|---|---|
| robots.txt blocks OAI-SearchBot, ChatGPT-User, PerplexityBot or Bingbot | Allow them. Show the exact lines to change. Leave training-bot choices to the owner. |
| Homepage or service pages are a client-side shell (little visible text in raw HTML) | Server-render or pre-render the money pages. Most AI fetchers do not run JavaScript. |
| Site returns 403 to non-browser user agents (Cloudflare bot fight mode, WAF rules) | Allow verified AI and search bots in the firewall. Verify by re-running site_signals.py. Note: if YOUR fetch was blocked, that is evidence only after a second check with a normal browser UA. |
| No sitemap, or sitemap missing service pages | Generate it, submit to Google Search Console and Bing Webmaster Tools. Bing feeds Copilot and parts of ChatGPT search. |
| Name, address or phone differ between site, Google profile and directories | Pick one canonical form and fix every listing. Engines merge entities by these fields. |

## Tier 2: copy what the winners have

Read 3 to 5 of the pages the engines actually cited for the questions the business lost. Name the specific pattern, then prescribe it.

| Winner pattern | Fix |
|---|---|
| A page that answers the exact question in its first two sentences | Write that page. Answer first, then detail. See the ai-answer-pages skill. |
| Pages that name things: insurance plans, brands installed, procedures, neighborhoods, prices or price ranges | Replace marketing language with named facts. "We accept most insurance" loses to "We accept Delta Dental PPO, Cigna DPPO and MetLife." |
| FAQ blocks with FAQPage schema | Add a real FAQ (questions buyers ask, from customers.md or call notes) with schema that matches the visible text. |
| Comparison or "best X in city" articles on third-party sites that list the winner | Get on those lists: find the cited listicles, contact the publishers, offer facts, a quote or an interview. This is the highest-leverage off-site move for local businesses. |
| Listed on the directories the engines cite (Yelp, Healthgrades, Avvo, Angi, BBB, industry associations) | Claim and complete those exact directories. Only the ones that appear in the sources, not every directory on earth. |
| Many recent Google reviews that mention the service and the city | Review ask after every job, with a prompt that invites specifics ("what did we fix, and where?"). Reply to every review. |
| Reddit / forum threads that recommend the winner | Do not astroturf. Identify the threads, have the owner answer genuinely where it is allowed, and earn real mentions over time. |
| Organization / LocalBusiness schema with sameAs links | Add schema with sameAs to the Google profile, social profiles and directory listings. |

## Tier 3: authority (weeks to months)

- Local press, association pages, sponsorships, partner pages that link with the business name.
- Original data the business owns (a price survey, a wait-time study) that others cite.
- Wikidata entry only if the business meets notability in good faith. Never fabricate references.

## What not to recommend

- Keyword stuffing, hidden text, AI-written pages at scale with no new facts. Engines down-weight them and buyers bounce.
- Fake reviews, review gating, or paying for listicle placement without disclosure.
- "Submit your site to ChatGPT." There is no such form.
- llms.txt as the headline fix. It is a small, cheap extra.

## Writing each fix

Title (imperative, specific), why (the evidence from this audit in one or two sentences), impact (high / med / low), effort (low / med / high), owner (owner, web, marketing, front desk). Five to eight fixes. If you have twenty, you have not prioritized.

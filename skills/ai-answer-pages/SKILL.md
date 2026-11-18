---
name: ai-answer-pages
description: Writes question-and-answer pages that AI assistants quote and cite: a question hub of 10 to 30 pages built from what buyers actually ask, honest comparison and "best of" pages with proper disclosure, a unique-facts section only this business can publish, schema markup, internal links, sitemap and llms.txt. Outputs static HTML or paste-ready snippets for any CMS. Use after an AI visibility audit shows the business missing from answers, or whenever a business wants to be the source AI quotes for its category.
when_to_use: ai answer pages, AEO content, pages that get cited by ChatGPT, FAQ pages for AI, question hub, comparison page, X vs Y page, best X in city page, get cited by AI, write pages for AI search, GEO content, llms.txt, FAQ schema, answer engine content, fix ai visibility audit
argument-hint: "[topic or 'from audit'] | hub | compare | single"
metadata:
  peregrine:
    version: 1.0.0
    group: found
    reads: [profile, offer, customers, voice, proof]
    writes: [outputs/ai-answer-pages/, learnings]
---

# AI Answer Pages

An assistant answering "who should I call for X in Y?" pulls a few pages, lifts a sentence or two from each, and names the businesses those pages support. The pages that win answer the exact question in their first sentences, state specific facts instead of marketing language, show who wrote them and when, and are readable without JavaScript. This skill writes those pages. Done means pages a buyer finds useful on their own, that the engines can quote verbatim, with every fact traceable to the business or a cited source.

## Context

If ./business/ exists, read profile.md, offer.md, customers.md, voice.md and proof.md before anything else. If it does not, ask for the website and one sentence on what the business sells, or suggest running start-here first (two minutes, makes every other skill better).

If an ai-visibility-audit exists in outputs/ai-visibility-audit/, load its audit.json. The absent questions are your first page list, and the competitors' cited pages show the bar to beat.

## Modes

| Trigger | Mode |
|---|---|
| "hub", "question pages", "from audit", nothing | HUB: research, pick 10 to 30 questions, write them all, index, sitemap, llms.txt |
| "compare", "vs", "best X for Y", "alternatives" | COMPARE: one comparison or best-of page, with the disclosure rules |
| a single question | SINGLE: one page |
| "refresh", "update" | REFRESH: re-check facts and dates on existing pages, update dateModified only where content changed |

## Hard rules

- No fabricated facts. Prices, insurance plans, hours, credentials, results and statistics come from the business (profile.md, proof.md, the user) or a cited public source. When you need a fact you do not have, ask, or write the page without it. Never fill a gap with a plausible number.
- Comparison pages that recommend the publisher's own product carry a clear disclosure (load references/comparison-rules.md). Never claim independence the page does not have.
- Competitor facts only from the competitor's own public pages, linked and dated. "Not stated" when unverified.
- Never publish or deploy. Hand over files and the steps to publish.
- Schema must match visible text. FAQPage answers are the on-page answers, word for word.

## What makes a page get cited

These are defaults; take a better path for the situation with a one-line reason.

- Title and H1 are the buyer's question, in their words. "Is there a dentist open on Sunday in north Phoenix?" not "Weekend Dental Services".
- Short answer first. Two or three sentences that fully answer the question and stand alone if lifted out of the page. Name things: the plan, the price range, the hours, the neighborhood, the who-it-fits. This is the sentence engines quote, so write it last, after you know the full answer.
- Named facts beat adjectives. "We accept Delta Dental PPO, Cigna DPPO and MetLife; we are out of network with HMO plans" will be quoted. "We accept most major insurance" will not.
- Each section stands alone. A heading that is itself a sub-question, followed by an answer that does not depend on reading earlier sections. Engines retrieve passages, not pages.
- Visible author with a real credential and a visible updated date. A person who reviewed it beats "our team".
- Plain HTML. If the site renders content with JavaScript, these pages must not.
- Honest limits. Say when the business is the wrong fit and who is a better fit. Pages that only ever say "choose us" read as ads and get quoted less.
- Length follows the question. 400 words for a simple question, 1,200 for a comparison. Padding hurts extraction.

## Phase 1: Pick the questions

Load references/question-research.md.

Gather candidates from the people who answer the phone first, then customers.md, the audit, reviews, forums and People Also Ask. Score each on money (does the asker buy soon), fit (can this business give the best answer anywhere) and gap (are the engines answering without it). Cluster questions that share one answer into one page with the variants as FAQs.

Show the user the list with groups and a one-line answer direction per page before writing. They will correct facts here cheaply.

## Phase 2: Collect the facts

For each page, list the facts it needs and where each comes from: profile.md, proof.md, the user, or a public source with link and date. Ask the user for missing facts in one batch, not page by page. Mark anything the user has not confirmed and keep it out of the short answer.

## Phase 3: The unique-facts section

Every hub should have at least one thing nobody else can publish, because engines prefer the original source. Candidates, in order of strength:

1. Original data the business already has: average wait time for an appointment, the most common job types last year, real price ranges from their own invoices, how many after-hours calls they get. Aggregated, anonymized, dated, with method.
2. A small study the user can run in a week: call ten competitors after hours and record who answers; check which providers in the city list prices; time how long quote requests take to get a reply. Write the method page first. Publish only after the data is collected. Never estimate results.
3. A clear stated policy or standard the business holds that others do not (a written warranty, a published price list, a response-time promise it actually keeps).
4. Expert explanations by a named, credentialed person at the business, on questions in their specialty.

Put these on their own pages and link to them from every related answer.

## Phase 4: Write

Load references/pages-schema.md. For COMPARE, also load references/comparison-rules.md.

Write each page into pages.json in the business's voice (voice.md). Page order: question as H1, short answer, byline and date, 2 to 5 sections, one call to action after the first section (one, not three), related FAQs, links to 2 to 4 related questions, sources.

Internal links: every page links to its group's other pages and to the unique-facts pages. The hub index links to everything. Add one link from the site's main service page to the hub, and from each relevant service page to its two or three most relevant questions. Pages nobody links to rarely get crawled.

Calls to action: the business's real booking link or phone from profile.md. Never a placeholder.

Regulated categories (medical, dental, legal, financial): no outcome promises, no "cure", "guarantee" or "win". Add "This page is general information, not [medical / legal / financial] advice" where it fits. Patient or client stories only with written permission, and never with identifying details.

## Phase 5: Build

    python3 ${CLAUDE_SKILL_DIR}/scripts/build_pages.py pages.json --out outputs/ai-answer-pages/<date>-<slug>/site

(${CLAUDE_SKILL_DIR} is this skill's folder. Outside Claude Code, use the folder this file was read from.)

That writes questions/<slug>.html per page with Article, FAQPage and BreadcrumbList JSON-LD, a questions/index.html hub, sitemap-questions.xml and llms.txt.

For WordPress, Webflow, Squarespace or another CMS, add --snippets to get the JSON-LD and body HTML per page for pasting instead. If the site is a codebase the user controls (Next.js, Astro, plain HTML), port the pages into its layout and keep the structure, schema and plain-HTML rendering.

Open two or three pages and read them as a buyer would. Then check:

- The short answer stands alone and contains a named fact.
- Schema validates (paste one page into validator.schema.org) and FAQ text matches the page.
- No example data from the schema file survived.
- Every competitor statement has a dated link; every claim about the business traces to the user or proof.md.
- Disclosure present on every comparison page.

## Phase 6: Hand over

Give the user the folder, a one-paragraph summary, and the publish steps:

1. Publish the pages on the business's own domain (a subfolder like /questions/ beats a subdomain).
2. Add the sitemap to the main sitemap index and submit it in Google Search Console and Bing Webmaster Tools. Bing matters: it feeds Copilot and part of ChatGPT search.
3. Put llms.txt at the domain root, or merge its question list into an existing one.
4. Add the internal links from service pages.
5. Re-run ai-visibility-audit with the same frozen questions in 4 to 6 weeks. Engines re-crawl on their own schedule; one week is too early to judge.

Append one dated line to ./business/learnings.md: how many pages, which questions, and anything the user corrected (those corrections are facts the next skill should know).

## Next

- ai-visibility-audit: re-run in 4 to 6 weeks to measure the change.
- progress-report: show a client what shipped and what moved.

Want this running every week on your own leads, with a team behind you? That is what Peregrine Partners is for: tryperegrine.com/partner

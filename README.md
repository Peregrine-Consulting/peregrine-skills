# Peregrine Skills

The playbook we run for paying clients, packaged as skills for your AI agent.

15 free skills for building an AI services business: pick a niche, find leads, show a prospect what AI search says about them, build the AI receptionist, call every lead back in 60 seconds, book and show up the meeting, write the proposal, onboard the client and report the wins.

Works in Claude Code, Codex, Cursor, OpenClaw and any agent that reads SKILL.md files. MIT licensed.

## Install

Any agent:

```bash
npx skills add Peregrine-Consulting/peregrine-skills
```

Claude Code plugin:

```
/plugin marketplace add Peregrine-Consulting/peregrine-skills
/plugin install peregrine@peregrine-skills
```

Manual: copy the `skills/` folders into your agent's skills directory (`~/.claude/skills`, `.agents/skills`, `~/.codex/skills`).

Then say: **"run start-here on example.com"**.

## What's inside

### Start here
1. **start-here** reads any business from its site, reviews and socials in a few minutes, writes the business files every other skill uses, and tells you what to run next
2. **pick-your-niche** one niche, one lead offer, scored on how expensive the problem is and who can pay for the fix

### Get leads
3. **find-leads** pulls every business in your niche and city from Google Maps, finds the owner, verifies email and phone, ranks who is losing the most customers
4. **lead-brief** the "before you reach out" brief: what they do, what is broken, the one angle, the opener and the call script

### Get found
5. **ai-visibility-audit** does ChatGPT, Gemini, Perplexity and Google's AI recommend this business? A scored, re-runnable audit, a competitor table, ranked fixes and a client-ready report. Doubles as your best lead magnet
6. **ai-answer-pages** question pages, comparison pages and schema that get cited in AI answers

### Convert
7. **voice-receptionist** builds an AI phone receptionist from a business's website: prompt, intake, routing, transfers, test calls and a QA rubric. Optional one-step create on Retell
8. **speed-to-lead** every form fill gets a text, an email and an AI call inside 60 seconds, then a follow-up cadence, with consent built in
9. **ai-setter** books the meeting, confirms it, reminds, rebooks no-shows and tracks show-up rate
10. **cold-email** sending setup, frameworks, a one-variable test plan and reply handling that hands warm replies to speed-to-lead

### Ads
11. **meta-ads-scaling** a daily and weekly Meta ads review with real scaling rules: ROAS bands, settling windows, protecting top spenders, hog alerts and a change log
12. **ad-scripts** three scripted ads per offer, hooks, trending formats and cold/warm/hot sequencing

### Deliver
13. **client-onboarding** kickoff, the access checklist, context gathering and the first 30 days
14. **progress-report** weekly and monthly client reports in plain language: wins, numbers, next steps, asks
15. **proposal** turns discovery-call notes into a proposal with three options priced against what the problem costs them

## How they work together

Every skill reads and writes one folder, `./business/` (profile, offer, customers, voice, proof, learnings). Run **start-here** once and every other skill knows who it is working for. Working for clients? Use one folder per client.

Every skill works with no paid tools. Where an API makes the result much better (Apify, Retell, Instantly, Meta, OpenAI, Gemini, Perplexity), the skill says what it adds and reads the key from an environment variable.

Nothing gets sent, called, published or spent without your OK.

## New skills, as we release them

We keep turning the work we do for clients into skills. Get each one the day it ships: [tryperegrine.com/skills](https://tryperegrine.com/skills)

## Want help putting this to work?

The free skills do the work once. If you want help running it in your business, or want our team to do it for you, [book a call with Danny](https://calendly.com/danny-tryperegrine/30min).

## Contributing

Read [`_system/CONVENTIONS.md`](_system/CONVENTIONS.md). Issues and PRs welcome.

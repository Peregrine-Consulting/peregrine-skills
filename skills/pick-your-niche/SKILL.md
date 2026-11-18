---
name: pick-your-niche
description: Helps someone starting or refocusing an AI services business pick ONE niche and ONE lead offer, using a scoring rubric for buyer value, pain cost, reachability and proof, then lays out the wedge-then-expand ladder from the first offer to bigger contracts. Writes the decision into ./business/ so every other skill targets the same buyer. Use when an agency sells to everyone, is just starting, or keeps getting small, price-shopping clients.
when_to_use: pick a niche, choose my niche, who should I sell AI to, what niche for my AI agency, I sell to everyone, niche down, which industry, what offer should I lead with, my clients are too small, refocus my agency, best niche for AI voice agents
argument-hint: "[candidate niches, or nothing]"
metadata:
  peregrine:
    version: 1.0.0
    group: start
    reads: [profile, offer, proof, learnings]
    writes: [business/offer.md, business/customers.md, business/learnings.md, outputs/pick-your-niche/]
---

# Pick your niche

Most new AI agencies stall for the same reason: they sell "AI automation" to anyone with a pulse, so every message is generic, every call starts from zero, and the clients they do close are small businesses that cannot pay enough to make the work worth it. Picking one niche fixes all three at once. The copy gets specific, the demo gets reused, the proof compounds, and referrals happen because owners in a niche talk to each other.

Done means: one niche (an industry plus a size band plus a region if relevant), one lead offer that solves an expensive problem in that niche, the first three rungs of the expansion ladder, and a one-week plan to test the choice with real conversations. Written to ./business/ so find-leads, cold-email and the rest all aim at the same buyer.

## Context

If ./business/ exists, read profile, offer, proof and learnings. Existing clients and proof are the strongest input here: a niche where you already have one result beats a better-looking niche where you have none. If nothing exists, ask three things only: what you have built or sold so far (even for free), any industry you have worked in or have contacts in, and how much you need a client to pay per month for this to be worth it.

## The core idea: sell to expensive problems, not to industries

The niche is not "dentists". The niche is a buyer with an expensive, recurring, measurable problem that AI fixes well today, who has money and a reason to decide quickly. Start from the problem.

Problems AI fixes well right now, roughly in order of how easy they are to prove:

1. **Missed and slow responses.** Calls to voicemail, form fills answered next morning, after-hours leads lost. Voice agents and instant follow-up fix this, and the proof is a number the owner can see within weeks (calls answered, leads contacted in under a minute, bookings).
2. **Front-desk load.** Scheduling, rescheduling, reminders, intake questions, insurance or eligibility questions, referral intake. This replaces or relieves payroll, which makes pricing easy to justify.
3. **Being invisible in AI answers and search.** Buyers ask ChatGPT and Gemini who to hire. An audit is a perfect door-opener; the ongoing fix is a retainer.
4. **Lead conversion and nurture.** Leads that never book, no-shows, dead leads in the CRM that nobody re-contacts.
5. **Back-office money.** Billing, collections, claims, accounts receivable, prior authorizations. Highest value, slowest to prove, needs trust first. This is usually the expansion, not the wedge.

## Scoring rubric

Score each candidate niche 1 to 5 on each line. Load references/niche-scorecard.md for the anchors and a worked example.

| Factor | Weight | What a 5 looks like |
|---|---|---|
| Value of one customer to them | 3 | One new customer or one saved case is worth thousands (surgery, legal cases, high-ticket home services) |
| Cost of the problem | 3 | You can point to payroll, lost cases or lost revenue in the tens of thousands a year |
| Ability to pay | 2 | Multi-location, multi-provider, or $3M+ revenue; owner already pays for staff and software |
| Reachability | 2 | You can find every one of them on Google Maps or a directory, the decision maker is findable, and they answer email or phone |
| Your unfair advantage | 2 | You have worked in it, know people in it, or already have a result in it |
| Speed of proof | 1 | A visible win inside 30 days |
| Compliance drag | 1 | 5 = light. Healthcare, finance and legal score lower here but often higher everywhere else |

Multiply, add, compare. The number is a conversation tool, not an oracle. When two niches are within about 10%, pick the one with the unfair advantage; it will close faster.

## Red flags

Walk away from or deprioritize a niche when:

- **Average ticket is small and volume is low.** A business that makes $80 a job and gets 15 calls a week cannot pay $1,500 a month for anything.
- **The owner is the whole staff.** No payroll to replace, no budget line, and every change waits on one exhausted person.
- **Every agency is already there with the same pitch.** Generic restaurants and generic gyms get pitched AI daily. You can still win, but only with a sharper problem.
- **The buyer is not the user.** Selling to a franchise brand when locations decide, or to a practice manager who cannot sign.
- **You need data you cannot legally touch.** Patient data without a BAA-capable stack, financial records without the right agreements. Healthcare is a great niche when you set this up properly, a liability when you do not.
- **You picked it because it sounds interesting.** Interest does not pay; an expensive, provable problem does.

## Picking the lead offer

The lead offer is the first thing you sell. It is not your whole menu. Good lead offers share four traits: one sentence, a visible result in 30 days, low setup risk for the client, and a natural next step.

The four offer families most AI services businesses build from:

- **AI Visibility:** audit whether AI assistants and search recommend them, then fix it monthly. Best door-opener because the audit itself is valuable and you can run it before the first call.
- **Lead Conversion:** speed-to-lead, voice receptionist, AI setter, reminders, no-show rebooking. Best wedge for businesses with inbound volume.
- **Ads + Content:** creative, ad management, posting. Easy to sell, hard to differentiate, and results depend on the offer more than on you. Better as an add-on than a lead.
- **AI Overhaul:** a full operating system for the business (CRM, intake, follow-up, internal tools). Biggest contract, longest sales cycle. Sell it after a smaller win, not cold.

Default pairing: **AI Visibility as the door-opener, Lead Conversion as the first paid offer.** Change it with a reason (e.g. the niche has little inbound volume, so lead with visibility as the paid offer).

## The wedge-then-expand ladder

Plan three rungs before your first sales call, so every call knows where it is heading.

1. **Wedge (month 1-2):** a narrow, fast, low-risk win. Example: an AI receptionist that answers after-hours calls for one location, or a 60-second callback on every web form.
2. **Expand (month 3-6):** the same system across the whole business. All locations, business hours too, scheduling and reminders, referral intake. Price moves from "a tool" to "part of the front office".
3. **Own a department (month 6+):** take over a costly back-office function with AI plus light human review. In medical, this is insurance verification, prior authorizations, billing and patient balances. In legal, intake through signed engagement. In home services, dispatch and follow-up on unsold estimates.

A worked shape, illustrative: specialty medical groups and surgery centers. They lose referrals and cases to phone tag, run several schedulers per location, and fight insurance on every case. The wedge is a voice agent answering and scheduling. Once it works and staff trust it, the expansion is referral intake and insurance checks, and the big contract is authorizations and billing recovery, where one recovered claim can pay for months of service. The niche scored high because a single case is worth thousands and the payroll being relieved is visible.

## Test it in one week

A niche is a hypothesis. Before building anything big:

1. Pull 50 real businesses in the niche (find-leads).
2. Run the door-opener on five of them (e.g. ai-visibility-audit) so you have something specific to say.
3. Send 50 personalized emails or make 20 calls (cold-email, lead-brief).
4. Count replies and conversations, not opens. Note the exact objections.

If after 100 well-targeted touches nobody in the niche wants to talk, change the offer before changing the niche. If they talk but say "we do not have budget", the niche fails the ability-to-pay line; move up a size band.

## Output

Write:
- outputs/pick-your-niche/<date>-decision.md with the scorecard for every candidate, the pick, the lead offer, the three-rung ladder, and the one-week test plan.
- Update business/offer.md with the lead offer (who it is for, the problem, the result, who it is not for).
- Update business/customers.md "Who buys" with the niche definition and the decision maker title.
- Append to business/learnings.md: "<date> pick-your-niche: chose <niche> / <offer> over <runner-up> because <reason>."

## Next

Run find-leads for the chosen niche, then ai-visibility-audit on five of those leads.

Want this running every week on your own leads, with a team behind you? That is what Peregrine Partners is for: tryperegrine.com/partner

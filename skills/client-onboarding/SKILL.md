---
name: client-onboarding
description: Runs the first 30 days after a client signs with an AI or marketing agency. Builds the client's onboarding pack (welcome email, kickoff agenda, access checklist, intake questions, how-we-work page), tracks what has been received and verified, chases what is missing with short follow-ups, turns everything the client shares into a working context folder, and writes the 30-day plan with clear deliverables the client confirms. Use right after a deal closes, when an onboarding has stalled waiting on the client, or to set up a repeatable onboarding for a new offer.
when_to_use: onboard a new client, client just signed, kickoff call agenda, client onboarding checklist, what access do I need from the client, client is not sending logins, welcome email for new client, 30 day plan for client, onboarding form, agency onboarding process
argument-hint: "[client name] [offer]"
metadata:
  peregrine:
    version: 1.0.0
    group: deliver
    reads: [profile, offer, voice]
    writes: [clients/<client>/onboarding/, clients/<client>/business/, outputs/client-onboarding/]
---

# Client onboarding

The week after a client signs decides whether they stay a year. They are at peak excitement and peak doubt at the same time. Every day they wait on you feeds the doubt. Every day you wait on them (for a login, a logo, a call list) quietly becomes your fault in their memory. Good onboarding is mostly about removing waiting on both sides: ask for everything once, in one place, in plain words, then chase only what is missing.

Done means: the client has one page that tells them what happens next and what you need, every access item is verified (not just "sent"), the client has confirmed in writing what you are delivering, and a context folder exists that any teammate or agent can read to do the work.

## Context

Here ./business/ is your agency (profile, offer, voice). If it does not exist, ask what you sold this client, at what scope, and how your team communicates, or suggest running start-here first.

The client gets their own folder: clients/<client-slug>/. Their business memory goes in clients/<client-slug>/business/ (same files as yours: profile, offer, customers, voice, proof), so every other skill can be run for them later from that folder.

## Hard rules

- Never ask a client to paste a password, API key or card number into email, chat, a form or a doc. Access is granted by invitation to their own accounts (add us as a user, partner, or admin) or through a password manager share. The checklist records whether we have access, never the secret itself.
- Nothing reaches the client without the user reading it first. You draft; they send.
- Deliverables are what was sold. Do not add scope to the plan to look generous; list extras separately as "suggested later".

## Step 1. Gather what was sold

Before writing anything to the client, collect: the signed proposal or agreement, the offer and price, the start date, promised timelines, the client contacts, and notes from sales calls. Ask the user for anything missing. Write clients/<slug>/onboarding/deal.md with:

- What we are delivering (each item in plain words with how both sides will know it is done).
- What is explicitly not included.
- Dates promised, by whom, in what call or document.
- Who on the client side decides, who does the work, who pays, who must never be called.

Promises made on a sales call that are not in the agreement go on a list for the user to confirm or walk back now, not in week 3.

## Step 2. The onboarding pack

Write these into clients/<slug>/onboarding/:

**welcome-email.md.** Short. Thanks them, names the one person who is their contact, gives the kickoff time (or two options), links the onboarding page, says the first visible thing they will get and when. No list of 20 asks in the welcome email.

**onboarding-page.md** (send as a doc, a page, or a form, whatever the agency uses). Sections, each marked who fills it:

| Section | Filled by | Holds |
|---|---|---|
| Company profile | client | legal name, brand name, website, locations, hours, time zone, logo |
| People | client | who we talk to, who approves, who receives updates, who must never get calls or texts, best channel for each |
| Brand | client | logo files, colors, fonts, brand guide, words they love and hate, past ads or content they liked |
| Access | client grants, we verify | see Step 3 |
| Lead and customer data | client | lead sources, lead lists (CSV with name, phone, email, source; consent basis for each source), customer list for ad exclusions |
| Voice and phone (if voice or AI calling is in scope) | client | current numbers and what to keep or port, call recordings or transcripts of their best staff on the phone (with consent), FAQs and prices callers ask about, transfer rules and who takes transfers, after-hours rules, things the AI must never say |
| Deliverables | we write, client confirms | the list from deal.md, with done-criteria |
| How we work | we write, client reads | see Step 5 |

Everything is skippable except the legal name and the people section. A client who can skip a hard section will finish the form; one who is blocked on question 4 abandons it.

**kickoff-agenda.md.** 45 minutes:

1. 5 min: introductions, who does what on both sides.
2. 10 min: their goal in their words. Ask "What would make you say this was the best decision you made this year, 90 days from now?" Write the answer down verbatim; it becomes the yardstick for every report.
3. 10 min: walk the deliverables and confirm them out loud.
4. 10 min: access, live. Grant as much as possible on the call: screen share and add us to Meta Business Manager, Google, the domain registrar, the phone system. The thing they will not do later, they will do while you watch.
5. 5 min: the first 14 days, dates included.
6. 5 min: questions, and "Is there anything you were worried about when you signed?"

## Step 3. Access checklist

clients/<slug>/onboarding/access.csv with columns: item, system, what we need it for, how granted, status, verified on, verified by, note.

Status runs: needed, requested, provided, verified, not needed, revoked. "Provided" and "verified" are separate on purpose: a login that was handed over and does not work is the most common onboarding failure, and it always surfaces a week later when work is blocked. Verify within 24 hours of receiving.

Load references/access-checklist.md for the standard items per offer type (ads, website and SEO, AI voice and phones, CRM and automations, email outreach, AI visibility) and how each is granted without sharing a password.

The access list doubles as the offboarding list. When the engagement ends, it is the list of what to hand back or revoke.

## Step 4. Context acquisition and follow-up

Everything the client sends (form answers, files, call recordings, the kickoff transcript, links) becomes their business memory. After each batch:

1. Update clients/<slug>/business/profile.md, offer.md, customers.md, voice.md and proof.md. Quote the client's words where you can. Mark anything you inferred as inferred.
2. Write clients/<slug>/onboarding/gaps.md: what is still missing, why it matters (which deliverable it blocks), and the exact question to ask.
3. Draft the follow-up.

Follow-up rules:

- One message, at most 3 asks, the blocking one first. "To get your phone line live by Thursday we need one thing: add us as a user in your phone system (2 minutes, steps below)."
- Every ask says what it unblocks and how long it takes.
- Cadence: day 2 after the kickoff, then every 2 business days while something is blocking. After the third chase on the same item, the user calls the decision maker; do not send a fourth email.
- When something arrives: thank them in one line and tell them what you did with it. Clients send faster when they see their last send turn into progress.
- Never chase with guilt ("we're still waiting on you"). Chase with momentum ("we're ready to launch the moment this is in").

## Step 5. How we work (the page that saves the most email)

Write it once per agency, adjust per client:

- Who is on the team, names and roles, and who their one main contact is.
- Where to send requests and where to talk, and which is for what.
- How fast we reply, on what days and hours.
- When the regular update lands (day and channel) and what it contains.
- How progress is measured: done items out of total, always with the total.
- What we will never do: send anything on their behalf without their OK, spend over the agreed ad budget, call or text anyone without consent, store their passwords.
- Who to escalate to, by name.
- How we handle their access: granted per person, removed the day someone leaves the project.

## Step 6. The 30-day plan

clients/<slug>/onboarding/30-day-plan.md:

- Week by week, what ships and what the client sees. Something visible in the first 7 days, even small (a demo call they can make, a draft ad, the audit report). Momentum beats completeness in month one.
- Each item: owner, date, depends on (which access or file), done when.
- Items blocked by the client are marked as such, so a slip is visible as theirs before it becomes yours.
- The goal from the kickoff, verbatim, at the top, with the one or two numbers that will show progress toward it and their starting value (baseline). Without a baseline, every later report is opinion.

Ask the client to confirm the deliverables in writing (a reply "confirmed" is enough). Save the confirmed version with the date; if scope changes later, write a new version rather than editing the old one.

## Output

clients/<slug>/onboarding/ containing deal.md, welcome-email.md, onboarding-page.md, kickoff-agenda.md, access.csv, gaps.md, 30-day-plan.md, and a status line at the top of a README.md: "Onboarding: 7 of 11 access items verified, deliverables confirmed 2026-03-04, blocked on: phone system admin." Re-run the skill any time to refresh gaps and draft the next follow-up.

Onboarding is done when: deliverables are confirmed, every access item in scope is verified or marked not needed, the context folder can answer "who is the customer and what do they want" without asking the client again, and the first visible deliverable has shipped.

## Next

Weekly and monthly updates to the client: progress-report. If voice is in scope, voice-receptionist uses the context folder you just built.

Want this running every week on your own leads, with a team behind you? That is what Peregrine Partners is for: tryperegrine.com/partner

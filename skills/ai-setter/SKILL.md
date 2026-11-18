---
name: ai-setter
description: Builds the booking-to-show-up flow an AI setter runs end to end. Books the meeting on a real calendar, places a confirmation call that gets the invite accepted, sends confirmation texts and 24-hour and 1-hour reminders, connects or reminds right before the meeting, rebooks no-shows once, books callbacks when "now isn't good", tracks who actually showed up, and alerts the owner at every step. Use when booked calls don't show, when a business wants an AI appointment setter, or when leads book but nobody confirms them.
when_to_use: ai appointment setter, ai setter, no shows, show up rate, appointment reminders, confirm appointments, booking confirmation call, rebook no shows, calendar invite accepted, callback booking, sales call show rate, setter script, retell setter
argument-hint: "[plan | build | script | report]"
metadata:
  peregrine:
    version: 1.0.0
    group: convert
    reads: [profile, offer, customers, voice, proof]
    writes: [outputs/ai-setter/]
    optional-keys: [RETELL_API_KEY, GOOGLE_SERVICE_ACCOUNT_JSON, CALENDLY_TOKEN, TELNYX_API_KEY, TWILIO_AUTH_TOKEN]
---

# AI setter

A booked call that doesn't show is worth nothing, and an unconfirmed booking shows far less often than a confirmed one. The setter's job is not to book more; it's to turn bookings into people on the call. The single biggest lever we've found is small and boring: a short call right after booking that gets the person to open the calendar invite and click Yes. An accepted invite sits on their calendar and pings them. An ignored one is an email they'll never see again.

Done means: the full after-booking sequence written (every call, text and email with timing), the setter prompt, the tool list, the stop and skip rules, the owner alerts, a show-up report, and in build mode a running flow in DRY_RUN with a test allowlist.

## Context

If ./business/ exists, read profile.md, offer.md, customers.md, voice.md and proof.md before anything else. If it does not, ask for the website and one sentence on what the business sells, or suggest running start-here first (two minutes, makes every other skill better).

Ask, if not known:
1. What gets booked? (sales call with the owner, a consult, an appointment, a group call or webinar)
2. Which calendar? (Google Calendar, Calendly, the practice's scheduler, a CRM's calendar)
3. Who runs the meeting, and is it phone, video or in person?
4. Should the setter live-transfer hot leads, or only book?

## Modes

| Ask | Mode |
|---|---|
| "plan", default | Sequence, copy, prompt, rules, alerts. No code. |
| "build" | Plan, then wire it (Step 7). |
| "script" | Only the setter prompt and tools, for an existing system. |
| "report" | Show-up analysis from existing bookings and outcomes (Step 8). |

## Hard rules

- No AI call or automated text without consent that covers it (see speed-to-lead). Bookings made on a calendar page get texts and calls only if the booking form asked for that consent.
- The setter says it is an AI assistant in its first sentence on outbound calls, and says the call is recorded. It never claims to be human.
- Never say a time is booked unless the booking tool confirmed it. Never invent open times.
- STOP and "don't call me" end everything, including a booked callback.
- Nothing goes to real people until the owner says go. Builds ship in DRY_RUN with a test allowlist.

## Step 1. The sequence (default)

| When | Channel | What | Skip if |
|---|---|---|---|
| Booking created | Owner alert | Who, when, source, their answers | never |
| +60 to 90 s | AI confirm call | Thank, confirm time, get the invite accepted, offer the link by text | spoke to them in the last 20 min; meeting under 20 min away; quiet hours and next window is more than 2 h out; no call consent |
| When the call ends (or at once if no call) | Text + email | Date, time in their zone, "open the calendar invite and click Yes", meeting link, reschedule link, STOP | no text consent (email only) |
| 24 h before | Text (+ email) | Reminder, reschedule link | in quiet hours (skip, don't delay); within 45 min of the confirmation text |
| 1 h before | Text | "We talk in an hour" | quiet hours |
| 1 to 2 min before (optional) | AI call | Phone meeting: "they're ready, connecting you" and transfer. Video: "starts in a minute, need the link?" | someone already called them in the last 10 min |
| Meeting time + 10 min, no-show | AI call, then one text | "Looks like we missed each other, no problem." Offer a new time once. | they canceled; the host hasn't marked it |
| Reschedule | Text + email | "New time: ..." New reminders. No second confirm call. | |
| Cancel | Text | One polite text with the booking link. Nothing more. | |

For a recurring group call (a weekly call, a webinar), the shape changes: invite per person to the recurring event, a confirmation the day they register, 24 h and 1 h reminders before their first session, "we're live now, here's the link" at start, and a replay text after if they didn't join. Give each person their own invite: a shared invite link doesn't land on their calendar.

## Step 2. The confirm call

This call is under two minutes and has one job.

1. "Hi Maria, it's Ava, an AI assistant with Lakeside, calling to confirm your call with Sam. This call is recorded. Got thirty seconds?"
2. Confirm the time, spoken in their time zone: "You're set for Thursday at two in the afternoon your time. Does that still work?"
3. The ask: "Could you open the calendar invite in your email and click Yes so it holds on your calendar?" If they can't find it: it came from [sender] to the email they booked with, check spam or promotions. With a get_invite_status tool, the setter can check live and offer resend_invite.
4. Link: with text consent, "I'll text you the link and details right after we hang up." Without, "It's in the invite and your confirmation email." Don't read URLs aloud.
5. Time doesn't work: send the reschedule link, or rebook on the call with booking tools. Never say a new time is set before the tool confirms.
6. Questions: answer in one sentence from the approved facts, else "That's a great one for Sam on the call." Log it so Sam sees it before the meeting.
7. Thank them, end.

Voicemail: one fixed sentence, set in config, not improvised. "Hi Maria, it's Ava with Lakeside, confirming your call with Sam on Thursday at 2. Please accept the calendar invite in your email. Talk soon."

## Step 3. Callbacks when now isn't good

"Not now" is not a no. When the person says it's not a good time, or asks for a real person, the setter offers a short call with the owner, reads two or three open times and books the one they pick. Rules that keep this safe:

- One time format everywhere: the person's local wall time, "2026-03-12 10:00". Tools refuse anything with an offset or "Z" rather than guess. The availability tool's answer starts with "Today is Wednesday, March 11 in your time" so the model works out "tomorrow" from the person's day, not the server's.
- Open time = inside the owner's working hours, inside 8 AM to 8 PM for the person in every zone their number could be in, not busy on the owner's calendar (all-day busy events block the day), not already booked by another call. Starts on the half hour, at least an hour out, up to 7 days ahead for offers, 14 for a time they name.
- Offer a spread: the earliest open time, then the first of a later morning or afternoon. Three at most.
- Book under a lock and re-check before confirming, so two calls never take the same slot. If the time isn't open, the tool answers with the nearest open times. At most three tries per call.
- The setter calls the person 60 seconds before the callback and connects them to the owner, skipping if a person called them in the last 10 minutes.

## Step 4. Live transfer (optional)

Only when the person is the decision maker, clearly interested, and wants to talk now, and only after asking. Ring several people at once if you have a team (first to answer gets a one-line brief from a handoff agent). If nobody picks up: "Looks like they just stepped away," then book a callback. An owner whose phone screens unknown numbers must save the transfer number as a contact or every transfer fails silently. Record the transfer outcome on the lead.

## Step 5. The prompt

Load references/setter-prompt.md for the full template with all call types (booking_confirm, no_show_rebook, connect_remind, connect_transfer, callback_offer). The traits that matter:

- **Warm, calm, brief. Not pushy.** The best setters sound like an assistant who's glad you booked. Improve show-up with timing and wording, never with pressure. No stacked urgency, no repeating an ask after a no, no persistence after "I'll think about it". A pushy setter books more and shows fewer, and gets the number flagged.
- **One job per call.** The confirm call confirms. It doesn't sell, it doesn't qualify again.
- **Approved facts only.** A short list of things it may say. Never prices, commissions, earnings, results, other clients' details, or the owner's personal number.
- **Questions it can't answer get logged**, not improvised.
- Dynamic variables: call_type, first_name, company, meeting_time_local (written to be spoken), meeting_link, reschedule_url, booking_link, sms_ok, lead_id (never spoken).

## Step 6. Tools and alerts

Load references/tools-and-alerts.md. Tools: get_invite_status, resend_invite, send_links (text, consent-gated), get_callback_times, book_callback, transfer, log_question, set_do_not_call (scope: calls or everything; also cancels a booked callback), end_call. All signed, all scoped to the person in this call, each with a plain failure sentence.

Owner alerts by text (business details only, nothing sensitive): new booking, reschedule, cancel, no-show, missed transfer, a question the setter couldn't answer, and a morning sheet of today's meetings with each person's status (confirmed on call, invite accepted, reminded, no contact). Missed transfers matter most: a ready buyer who heard ringing and then nothing.

## Step 7. Build (build mode)

Reuse the speed-to-lead service shape (steps table, worker, single outbox with DRY_RUN and TEST_ALLOWLIST, quiet hours). Add:

- Calendar webhooks: booked, canceled, rescheduled (cancel and create can arrive in either order; ignore a stale cancel), no-show marked. Match bookings to leads by the lead id in the booking link, then email, then phone.
- A runs model: pre_booking, booked, rebook, no_show. A booking cancels every pre-booking step.
- Each step happens once per person: unique on person and reason. A late step is dropped rather than sent out of context (any call after the meeting started; a text more than 2 hours late).
- A pause switch that pauses, not ends: with the setter off, new steps are still planned and wait; turning it on resumes, with the stale rules dropping anything out of date.
- Calendar access for invites and callbacks through a service account with only the events scope it needs, impersonating the owner's calendar or a dedicated scheduling account. Never invite the owner's personal address to client events unless asked.

## Step 8. Show-up tracking

Show-up rate is the number that matters. Track it per booking:

- For video calls: match the meeting's attendee list to bookings (by email, then name), with a person confirming fuzzy matches. For phone calls: the connect call or the rep's logged call. For in-person: the scheduler's arrived status.
- Report weekly: booked, confirmed on call, invite accepted, reminded, showed, no-show, rebooked, showed after rebook. Split by source and by whether the confirm call connected. The confirmed-vs-not split is how you prove the setter's value.
- Write the report to ./outputs/ai-setter/<date>-show-up.md and add a dated line to ./business/learnings.md.

## Output

./outputs/ai-setter/<YYYY-MM-DD>-<slug>/: sequence.md, messages.json, setter-prompt.md, first-sentences.txt, voicemails.txt, tools.json, post-call-fields.json, alerts.md, rules.md (skips, stale, caps), and in build mode the service changes with a README and .env.example.

## Next

- speed-to-lead: get more of them booked in the first place.
- progress-report: show the client the show-up numbers every month.

Want this running every week on your own leads, with a team behind you? That is what Peregrine Partners is for: tryperegrine.com/partner

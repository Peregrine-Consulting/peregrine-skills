# Speed-to-lead service architecture

Load in Step 6 (build mode). Stack-neutral; the example is Node + Postgres, but the shape is what matters.

    lead sources ──POST /leads/:source──▶ intake ──▶ leads + steps (Postgres)
      (site form, lead ads,                │                ▲
       missed call, quiz)                  │        worker (every ~10 s, plus a kick on each new lead)
                                           │        claims one due step, re-checks rules, sends
                                           ▼                │
    calendar ─▶ /webhooks/calendar     outbox (DRY_RUN / TEST_ALLOWLIST gate)
    SMS      ─▶ /webhooks/sms            ├─ SMS provider (Telnyx, Twilio...)
    voice    ─▶ /webhooks/voice          ├─ voice platform create-call (Retell, Vapi...)
    agent tool ─▶ /tools/send-booking-link
                                         └─ email (Resend, Postmark, SES)
    owner ─▶ /admin (auth)

## Tables

- leads: id, source, name, email, phone_e164, company, state, timezone, answers (json), sms_consent, call_consent, consent_text, consent_at, status (open, booked, stopped, opted_out), created_at
- steps: id, lead_id, run (pre_booking, booked, rebook, no_show), key (first_text, call_1...), channel, due_at, status (pending, running, sent, skipped, failed, canceled), result (json). Unique (lead_id, run, key).
- events: inbound webhooks and replies, raw, for audit
- opt_outs: phone or email, scope, at, source

## Intake

- Validate and normalize the phone to E.164. Reject obviously fake numbers.
- Dedupe: a lead_id from the form makes posts idempotent. The same phone or email in the same source within N days updates the existing lead rather than starting a second sequence.
- Public forms: CORS to the business's domains, a honeypot field, rate limit per IP. A secret in a static page's JS is not a secret; it only labels the source.
- Plan every step of the pre-booking run at intake, with due times computed from the cadence and quiet hours.

## Worker

- Claim with SELECT ... FOR UPDATE SKIP LOCKED, set running, commit, then send.
- Re-check at send time: lead status, opt-outs, consent for this channel, quiet hours, call cap, spacing. Anything failing becomes skipped with a reason, or moves to the next allowed time.
- A step still running ten minutes after it was claimed means the process died mid-send: mark failed, never retry. Pass the step id as an idempotency key to providers that support it.
- Run one replica unless your intake dedupe lock is in the database.

## Outbox

The only code that talks to providers.

    gate(recipient):
      if DRY_RUN: log exactly what would go out; return dry_run
      if TEST_ALLOWLIST and recipient not in it: log blocked; return blocked
      else: send live

DRY_RUN defaults to true. Ship with it on. Turning it off with an allowlist of the owner's and your own numbers is the test phase. Removing the allowlist is going live, and it's the owner's decision.

## Webhooks

Verify every signature (calendar signing key, SMS provider public key, voice platform signature). Match a booking to its lead by the lead id carried in the booking link (utm_content or a hidden field), then by email, then by phone. A booking that matches nothing is created as a lead only if the booking form asked for text/call consent.

## Admin

A page behind auth: leads with their step timeline, a Stop button per lead, Mark no-show, and the current mode (dry_run, allowlist, live) shown at the top in a color nobody can miss.

## Tests worth having

Quiet hours per state and split zone, STOP across sequences, dedupe, booking cancels pending steps, cancel triggers rebook, reschedule ordering (cancel and create can arrive in either order), no double send after a simulated crash, outbox never sends in DRY_RUN.

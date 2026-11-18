# Setter tools and owner alerts

Load in Step 6. Every tool is a signed POST to your service (shared secret header, or the voice platform's request signature), acts only on the person named in the call's metadata, and returns one plain sentence the agent can say. Timeouts 10 s, 20 s for booking.

## Tools

| Tool | Params | Returns (examples) |
|---|---|---|
| get_invite_status | none | "Accepted." / "Not accepted yet." / "No invite found." (reads the RSVP live from the calendar) |
| resend_invite | none | "Sent again to maria@... It may take a minute." |
| send_links | type: meeting, reschedule, booking | "Texted." Only with text consent, no opt-out, not declined. Otherwise "Can't text this person; they'll get it by email." |
| get_callback_times | from_date (optional, YYYY-MM-DD, person's day) | "Today is Wednesday, March 11 in your time. Open: Thursday 10:00 (start 2026-03-12 10:00), Thursday 3:30 (start 2026-03-12 15:30), Friday 9:00 (start 2026-03-13 09:00)." |
| book_callback | start (person's local wall time YYYY-MM-DD HH:MM) | "Booked: Thursday March 12 at 10 AM your time." / "That time isn't open. Nearest: ..." |
| transfer | reason | bridges to the host or ring group with a one-line brief |
| log_question | question | "Saved for Sam." |
| set_do_not_call | scope: calls or everything | "Done." Also cancels any booked callback. |
| end_call | | |

Implementation notes:
- Times: refuse any value with an offset or "Z". Never guess a zone. Zone comes from the phone number narrowed by the city on the form; if several zones remain, a time must be inside 8 AM to 8 PM in every one; if none, use the host's zone and say it out loud.
- book_callback runs under a lock shared with cancels and re-checks the live calendar and other bookings before answering "Booked". Creating the calendar event uses a deterministic id so a retry finds the existing event instead of making two.
- Every tool call is logged with its inputs and answer on the lead's timeline.

## Owner alerts (text, business details only)

| Event | Example |
|---|---|
| New booking | "Booked: Maria Lopez, Lopez Dental (3 locations), Thu 2:00 PM PT. Source: Meta lead form. Pain: missed calls." |
| Confirmed | Optional, or rolled into the morning sheet |
| Reschedule / cancel | "Rescheduled: Maria Lopez, now Fri 10:00 AM PT." |
| No-show | "No-show: Maria Lopez (Thu 2:00 PM). Ava calling to rebook." |
| Missed transfer | "Missed transfer: Maria Lopez wanted to talk now, nobody picked up at 2:14 PM. Call back: [link to lead]." |
| Open question | "Maria asked: does this work with Dentrix? (for Thursday's call)" |
| Morning sheet (8 AM host time) | Today's meetings, each with: confirmed on call / invite accepted / reminded / no contact, and open questions |

Never include medical details, case facts, card data or anything a person wouldn't want on a lock screen. Link to the lead in the CRM instead.

## Calendar access

- Google Calendar: a service account with domain-wide delegation, scope calendar.events (plus calendar.readonly for free/busy), impersonating a dedicated scheduling account or the host. Each person gets their own event so it lands on their calendar.
- Calendly: webhooks for invitee.created, invitee.canceled, invitee_no_show.created and invitee_no_show.deleted (paid plan). Carry the lead id in utm_content on every booking link so a booking finds its lead.
- Practice schedulers and CRMs: use their API if it exists; otherwise the setter books into Google Calendar and a person enters it, which is fine to start.

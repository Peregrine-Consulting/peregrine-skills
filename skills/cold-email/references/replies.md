# Reply handling

Load in replies mode, or when setting up automation on replies.

## Classify, negative first

Read only the new text, not the quoted thread below it (quoted text contains your own words, which will trigger false matches).

Check in this order and stop at the first match:

1. **Unsubscribe / not interested.** Patterns: not interested, no thanks, no thank you, unsubscribe, remove me or us, take me off, stop emailing or contacting, don't email, opt out, not a fit, leave me alone, spam. Action: do-not-contact on every channel (email, phone, text, LinkedIn), mark it in the sending tool's block list and in the CRM. Do not reply, except a one-line "Done, you won't hear from me again" if the user wants that.
2. **Wrong person.** wrong person, not the right person, no longer here or with the company. If they name someone else, that is a referral: draft a short email to the named person mentioning who pointed you there. If they do not, stop for this contact.
3. **Bounce / auto-reply with no person.** Remove the address.
4. **Out of office.** Let the sequence continue if the return is within a week. Otherwise pause until the return date.
5. **Interested.** yes, sure, interested, tell me more, send more info, send times, let's talk, set up a call, open to, what times, how does it work, call me.
6. **Question.** Anything asking about price, how it works, who else uses it, integrations, compliance.
7. **Not now.** "Maybe next quarter", "busy season", "check back in January". Set a dated follow-up and say so.
8. **Unclear.** Everything else goes to a human.

A simple regex set catches most obvious yes and no replies before an AI or human looks. Use it as a first pass, never as the only one. When regex and the model disagree, a human decides.

## Answering

- **Interested:** answer within the hour in business hours. Thank them in five words, give two specific times and the booking link, and one line of what the call covers. No new pitch.
- **"Send more info":** one short paragraph and one link (a demo, a two-minute video, or a one-page summary). End with a time.
- **Price question:** the honest range from offer.md if it exists, the main thing it depends on, and an offer to size it on a short call. Never invent a price.
- **Compliance question (HIPAA, call recording, data):** answer only from what is true in offer.md and profile.md. If unsure, say you will confirm in writing and flag it for the user.
- **Not now:** "Makes sense. I'll check back in <month>." Then actually schedule it.

## Auto-replies

Only for clear "interested" replies, only with a template the user approved word for word, and only if one reply per lead is guaranteed (a reply and a label arriving together must not send twice). Everything else is drafted for a human.

## Log it

For each reply: date, campaign, angle, step that got the reply, classification, outcome. Weekly, roll up positive reply rate per angle and per step into ./business/learnings.md. The step that gets the most positive replies tells you where your best argument is.

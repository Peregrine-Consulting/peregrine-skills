# Speed-to-lead compliance

Checked: 2026-11. Not legal advice. Have the business's counsel confirm the consent wording, the state hour table and any state telemarketing registration before going live.

## Consent block for the form

Unchecked by default. Separate from agreeing to terms. Example:

    [ ] I agree that Lakeside Dental may contact me at the number I provided with texts and calls,
        including automated and AI-generated calls and texts, about my request and appointments.
        Consent is not a condition of purchase. Msg frequency varies. Msg & data rates may apply.
        Reply HELP for help, STOP to opt out. See our Terms and Privacy Policy.

Store with each lead: the exact text shown, checked true/false, timestamp, page URL, IP. If the business wants calls but not texts (or the reverse), use two boxes and honor each separately.

Why both words: the FCC's 2024 ruling treats AI-generated voices as artificial voice calls under the TCPA, so the consent has to cover automated/AI calls, not just "we'll contact you".

## Quiet hours (local time of the lead)

| Rule | Window |
|---|---|
| Federal default | 8:00 AM to 9:00 PM |
| Florida, Oklahoma, Maryland, Washington | end 8:00 PM |
| Texas | start 9:00 AM; Sunday start noon |

Other states have holiday bans or registration rules; check for the states you call. Resolving the zone: browser time zone sent by the form, else the state, else the area code. Split states (Florida panhandle, Indiana, Kentucky, Tennessee, Texas around El Paso, Idaho, Oregon, Kansas, Nebraska, the Dakotas, Michigan's west edge) and area codes that cross zones: the step must be inside the window in every candidate zone. Unknown: use the intersection of every US zone and every state rule (roughly 2 PM to 8 PM Eastern).

Pre-booking steps outside the window wait for the next allowed time. Reminders for a booked meeting that fall in quiet hours are skipped (a 1-hour reminder at 7 AM is pointless after the meeting time has passed).

## Keywords

- Opt-out: STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, QUIT, plus OPTOUT, REVOKE. Treat a message starting with one of these as an opt-out too, and flag it for a human.
- Help: HELP, INFO.
- Opt-in: START, UNSTOP.

If the SMS provider's own keyword auto-replies are on, turn yours off (or theirs) so people don't get two replies.

## 10DLC registration (US local numbers)

1. Brand: exact legal name, EIN, entity type, address, website, support email and phone. Wait for verification. Standard vetting improves throughput.
2. Campaign: use case usually "Mixed" or "Customer Care" plus "Marketing" depending on content. Description in plain words: who gets texts, why, how they opted in.
3. Message flow (opt-in): describe each form and its checkbox, with URLs and screenshots. Reviewers open the site; campaigns fail most often because the live form lacks the consent language or the privacy policy lacks the no-sharing line.
4. Privacy policy must say mobile numbers and opt-in data are not shared with or sold to third parties for marketing.
5. Sample messages: 3 to 5 real ones from your templates, filled in.
6. Embedded links: yes (your domain). Phone numbers in messages: yes if used. Age-gated: no.
7. Keywords and the HELP/STOP replies, exactly as you send them.
8. After approval, assign the number to the campaign. Until then, texts to real numbers will be filtered or blocked.

Toll-free numbers have a separate verification process; it's often faster for low volume.

## Email

One-click unsubscribe link, List-Unsubscribe and List-Unsubscribe-Post headers, a physical mailing address, honest subject lines (CAN-SPAM). Send follow-up email from a domain with SPF, DKIM and DMARC set. Never send cold email from the business's main domain.

## Health and other sensitive data

Keep texts and call variables about booking, not about the condition. If the business is a HIPAA covered entity and any message or call touches patient information, every vendor (SMS, email, voice, LLM, your service's host and database) needs a BAA first.

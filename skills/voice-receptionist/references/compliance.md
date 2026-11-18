# Voice compliance notes

Checked: 2026-11. Not legal advice. Laws change; have the business's counsel confirm before a live launch.

## Call recording consent

Most US states are one-party consent: the business (a party) consents. These states generally require all parties to consent to recording: California, Delaware, Florida, Illinois, Maryland, Massachusetts, Michigan (interpretations differ), Montana, Nevada (phone calls), New Hampshire, Oregon (in-person; phone is one-party), Pennsylvania, Washington. Callers can be anywhere, so the safe default is to say "this call may be recorded" in the first sentence on every call.

## AI disclosure

- The FCC (2024 declaratory ruling) treats AI-generated voices as "artificial or prerecorded voice" under the TCPA. Outbound AI calls to cell phones need prior express consent, and prior express written consent for marketing calls. Inbound calls (they called you) are not covered by that rule.
- California's bot disclosure law (SB 1001) requires disclosing a bot when it is used to incentivize a sale or influence a vote. Several other states have passed or are considering AI-disclosure rules for calls. Default: outbound calls always disclose in the first sentence; inbound agents answer honestly when asked and never claim to be human.

## Health information (HIPAA)

- A covered entity (practice, surgery center) needs a Business Associate Agreement with every vendor that receives patient information: the voice platform, the LLM provider behind it, the transcription/recording store, the texting provider, and any tool endpoint you host.
- Turn on the platform's PII/PHI redaction for transcripts and logs where offered, and set data retention to the shortest the practice's policy allows.
- Demos with fictional practices and fictional callers involve no PHI.

## Texts from the agent

Texts need prior consent and a 10DLC-registered number in the US. See the speed-to-lead skill for consent language, quiet hours and stop words.

## Telemarketing hours (outbound and callbacks)

Federal window is 8 AM to 9 PM in the called person's local time. Some states are stricter (examples: Florida, Oklahoma, Maryland and Washington end at 8 PM; Texas starts at 9 AM and noon on Sunday). See speed-to-lead's quiet-hours reference.

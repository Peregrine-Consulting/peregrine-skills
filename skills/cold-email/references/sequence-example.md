# Example sequence (illustrative)

Load when writing a sequence, to see the shape and tone. Everything here is made up: Northline is a fictional AI receptionist company, Sam a fictional sender, the address fictional. Replace every specific with the user's real business, proof and address. Do not copy the proof line in email 3 unless the user has a real result like it in proof.md.

Angle: missed calls. Niche: independent dental practices. Variables: {{firstName}}, {{companyName}}, {{persona_line}}, {{demo_link}}, {{booking_link}}.

## Persona lines (set per lead by job title at import)

- Owner or dentist: "Every new patient call that reaches voicemail is a chair you paid to fill."
- Office manager: "Phones are usually the part of the day the office manager never gets ahead of."
- Anyone else: "A quick question about how calls are handled at your practice."

## Email 1, day 0, no links

Subject: calls after 5 at {{companyName}}

    Hi {{firstName|there}},

    {{persona_line}}

    Most people look for a new dentist after work, and the ones who reach voicemail usually call the next office on the list.

    We set up a receptionist that answers every call, day and night, and books straight into your schedule.

    Worth a look?

    Sam

## Email 2, day 3

Subject: (blank, same thread)

    {{firstName|Hi}}, one thing I left out.

    It only books into the openings you allow, and anything clinical or unusual goes straight to your team with a summary. Your front desk stays in charge.

    Want to hear it? It can call your cell in about a minute: {{demo_link}}

    Sam

## Email 3, day 6

Subject: (blank, same thread)

    {{firstName|Hi}}, a three-office practice we work with was sending about a third of evening calls to voicemail. Now every one is answered and new patients book that night.

    Worth 20 minutes to see how it would run at {{companyName}}?

    Sam

## Email 4, day 10

Subject: (blank, same thread)

    {{firstName|Hi}}, the other half of it is the lunch hour and the Monday morning rush, when two lines ring and one person can answer.

    Overflow calls get picked up instead of going to hold.

    Hear it on your own phone: {{demo_link}}

    Sam

## Email 5, day 14

Subject: (blank, same thread)

    {{firstName|Hi}}, I'll close the loop here.

    If missed calls aren't a problem at {{companyName}}, no reply needed.

    If they are, pick any 30 minutes: {{booking_link}}

    Sam

## Footer (every email)

    Not a fit? Reply "no thanks" and I'll stop.
    Northline, 100 Main St, Phoenix, AZ 85004

## Notes on why it is built this way

- Email 1 has no link and no ask beyond a reply. Replies are the strongest inbox-placement signal.
- The demo link in email 2 is the consent bridge: the prospect asks for the call themselves on a page with a consent checkbox. Nobody gets an AI call without that.
- Email 3 is the only one with proof, and it is one sentence.
- Every email is short enough to read on a phone without scrolling.

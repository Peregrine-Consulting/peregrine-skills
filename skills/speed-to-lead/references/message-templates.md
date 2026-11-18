# Message templates

Load in Step 2. Fictional business (Lakeside Dental, assistant "Ava", owner "Sam"). Swap names, offer and voice from ./business/. Keep texts under 160 characters where possible. Every text carries an opt-out line until the person has replied at least once.

## Pre-booking

```json
{
  "first_text": "Hi {{first_name}}, Ava with Lakeside Dental. Got your request. I'll call you in a minute, or book here: {{booking_link}} Reply STOP to opt out",
  "first_email": {
    "subject": "Got your request, {{first_name}}",
    "body": "Hi {{first_name}},\n\nThanks for reaching out to Lakeside Dental. Ava from our team will give you a quick call in the next minute.\n\nIf it's easier, pick a time that suits you here: {{booking_link}}\n\nSam\nLakeside Dental"
  },
  "pre_call_text": "{{first_name}}, Ava from Lakeside Dental calling you now about your request.",
  "missed_call_text": "Tried you just now, {{first_name}}. Grab a time here: {{booking_link}} or reply with a good time to call. STOP to opt out",
  "plus_1h_text": "{{first_name}}, most new patients are seen within the week. Pick a time that works: {{booking_link}} Ava, Lakeside Dental",
  "next_morning_text": "Morning {{first_name}}, still happy to get you in. Times are here whenever you're ready: {{booking_link}} Ava, Lakeside Dental. STOP to opt out",
  "day_3": {
    "text": "{{first_name}}, a question we get a lot: yes, we take most PPO plans and check yours before your visit. Book here: {{booking_link}} Ava, Lakeside Dental",
    "email_subject": "Quick answer on insurance",
    "email_body": "Hi {{first_name}},\n\nThe question we hear most: we take most PPO plans and check yours before your first visit, so there are no surprises.\n\nWhen you're ready, pick a time here: {{booking_link}}\n\nSam"
  },
  "day_7_email": {
    "subject": "Should I close your request?",
    "body": "Hi {{first_name}},\n\nI haven't heard back, so I'll assume the timing isn't right and close your request for now. If you still want to come in, just reply or book here: {{booking_link}}\n\nSam"
  }
}
```

## Rebook after a cancel

- +5 min: "Hi {{first_name}}, saw your appointment got canceled, no problem. Pick a new time whenever it suits: {{booking_link}} STOP to opt out"
- Next day 10 AM: "{{first_name}}, still happy to find a time that works: {{booking_link}} Ava, Lakeside Dental"

## Keyword replies

- HELP: "Lakeside Dental: texts about your appointment request. Help: hello@lakesidedental.example or 555 0100. Msg freq varies. Msg & data rates may apply. Reply STOP to opt out."
- STOP: "Lakeside Dental: you're unsubscribed and won't get more texts or calls from us. Reply START to resubscribe."
- START: "Lakeside Dental: you're resubscribed. Reply HELP for help, STOP to opt out."

## B2B variant (selling to a business owner)

- First text: "Hi {{first_name}}, it's Ava with {{your_company}}. Got your request about {{company}}. I'll call in a minute, or grab 30 min with Sam: {{booking_link}} STOP to opt out"
- Day 3 answers the top objection for the offer ("works with your current phone system, nothing to install").
- The call qualifies: role, size (locations, volume), what hurts most, decision maker, budget fit without a number ("If the numbers work, are you in a position to invest in fixing this?"). One gentle timing reason, said once.

## What not to write

- "URGENT", "FINAL NOTICE", "ACT NOW", "!!!"
- Anything about a medical condition, a legal matter's details or money owed in a text
- A shared link shortener (bit.ly and similar get filtered)
- A reply that claims a call or action that didn't happen ("as we discussed") when no call connected

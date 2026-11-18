# Tool definitions

Load in Step 4. These are platform-neutral JSON Schema shapes. On Retell they become "custom" tools (URL, POST, headers, parameters). On other platforms the same shape goes in their function/tool config.

Every tool:
- POSTs to your endpoint with a shared secret header (x-tool-secret). The endpoint rejects anything without it.
- Acts only on the caller in this call (the platform passes call id and metadata). Never let a tool take an arbitrary phone number or customer id from the model and act on it.
- Returns a short plain sentence the agent can say, not raw JSON. "Booked: Tuesday, March 4 at 10 AM with Doctor Cole at Lakeside Main." beats {"ok":true,"slot":"..."}.
- Has a timeout (10 s default, 20 s for booking) and a failure sentence in the prompt.

```json
[
  {
    "name": "find_openings",
    "description": "Find open appointment times. Pass the visit type and the location the caller chose, and a provider if they named one.",
    "parameters": {
      "type": "object",
      "properties": {
        "kind": {"type": "string", "enum": ["new", "follow_up", "estimate", "consult"]},
        "location": {"type": "string"},
        "provider": {"type": "string"},
        "after": {"type": "string", "description": "Optional earliest day the caller wants, YYYY-MM-DD in the caller's local time"}
      },
      "required": ["kind"]
    },
    "speak_during": "Let me check the schedule."
  },
  {
    "name": "book_appointment",
    "description": "Book one slot that find_openings returned.",
    "parameters": {
      "type": "object",
      "properties": {
        "slot_id": {"type": "string"},
        "caller_name": {"type": "string"},
        "reason": {"type": "string", "description": "The caller's reason in a few words"},
        "cell_phone": {"type": "string", "description": "Read back and confirmed"},
        "priority": {"type": "boolean"}
      },
      "required": ["slot_id", "caller_name"]
    },
    "speak_during": "Booking that now.",
    "timeout_ms": 20000
  },
  {
    "name": "lookup_customer",
    "description": "Find an existing customer by name and date of birth, or by the number they're calling from.",
    "parameters": {
      "type": "object",
      "properties": {
        "full_name": {"type": "string"},
        "date_of_birth": {"type": "string", "description": "YYYY-MM-DD"}
      },
      "required": ["full_name"]
    },
    "speak_during": "Let me pull that up."
  },
  {
    "name": "transfer_to_staff",
    "description": "Hand the caller to a team: clinical or technical questions, billing, a person on request, or a hot lead who wants to talk now.",
    "parameters": {
      "type": "object",
      "properties": {
        "team": {"type": "string", "enum": ["front_desk", "clinical", "billing", "sales", "on_call"]},
        "reason": {"type": "string", "description": "One line the person picking up will hear"}
      },
      "required": ["team", "reason"]
    }
  },
  {
    "name": "send_text",
    "description": "Text the caller a confirmation, directions or a form link. Only if they agreed to texts.",
    "parameters": {
      "type": "object",
      "properties": {
        "type": {"type": "string", "enum": ["confirmation", "directions", "intake_form", "booking_link"]}
      },
      "required": ["type"]
    },
    "speak_during": "Sending that now."
  },
  {
    "name": "take_message",
    "description": "Save a message for the team with a callback number and how urgent it is.",
    "parameters": {
      "type": "object",
      "properties": {
        "caller_name": {"type": "string"},
        "callback_number": {"type": "string"},
        "message": {"type": "string"},
        "urgent": {"type": "boolean"}
      },
      "required": ["message"]
    }
  },
  {
    "name": "log_safety_event",
    "description": "Record that you told the caller to hang up and call 911 (or 988). Use right after saying it.",
    "parameters": {
      "type": "object",
      "properties": {"reason": {"type": "string", "description": "Two or three words"}},
      "required": ["reason"]
    }
  }
]
```

## Transfers in practice

- Prefer a warm transfer: a second short agent (or the platform's warm-transfer feature) briefs the person who picks up in one sentence ("New patient, Maria Lopez, leg pain when walking, wants Thursday, priority") before bridging. Closers and front desks pick up faster and convert better when they know who's on the line.
- Ring several people at once for sales transfers (a ring group), first to answer gets the brief. One person's phone is a single point of failure.
- If a transfer target is a cell phone, the person must save the transfer number as a contact or their phone's call screening will eat the call.
- Record what happened: transfer attempted, connected or not, who took it. A transfer that silently fails is the most expensive bug in voice.

## Demo tools

For a demo agent, the endpoints can serve a fake schedule: a JSON file of open slots for the next 10 business days that regenerates each night, a fake customer list where any name and date of birth "is found", and a send_text that shows the text on the demo web page instead of sending it. Same voice experience, zero risk.

# Retell notes

Checked: 2026-11. Retell's API changes often. Confirm field names against docs.retellai.com before running anything; update this file's date when you do.

## Objects

- A Retell LLM holds the prompt (general_prompt), begin_message (the first sentence), general_tools (custom tools and end_call), and the model choice.
- An agent holds the voice, the response_engine (pointing at the LLM), interruption sensitivity, voicemail handling, pronunciation dictionary, post_call_analysis_data, webhook_url and data retention.
- Phone numbers point at agents. As of late 2026 the phone number API takes inbound_agents and outbound_agents arrays (older docs show single inbound_agent_id/outbound_agent_id fields).

## Versions

Agents and LLMs are versioned. Edits happen on a draft version; calls use the published version a number is bound to. The safe flow for changing a live agent: create a new version from the current one, edit the LLM at that version, publish it, then bind the number to the new version. Never edit the version a live number is using in place.

## Endpoints used by scripts/create_retell_agent.mjs

- POST https://api.retellai.com/create-retell-llm
- POST https://api.retellai.com/create-agent
- Auth: Authorization: Bearer $RETELL_API_KEY

The script only creates. It never calls update, publish or any phone-number endpoint.

## Things that bite

- Custom tool URLs must be reachable from Retell (public HTTPS). Use a shared secret header and check it.
- Dynamic variables ({{first_name}}) only resolve if the call is created with retell_llm_dynamic_variables. On inbound calls, use the inbound webhook to supply them for known callers.
- Voicemail: enable voicemail detection on outbound agents and give a fixed voicemail message, so the model doesn't improvise one.
- A warm transfer creates a second call (the handoff agent's call). Whether the transfer connected shows on that second call, not the first. Check both when you measure transfers.
- Numbers bought on your own carrier and imported into Retell over SIP keep their texting on the carrier side; numbers bought in Retell may not have SMS approval.

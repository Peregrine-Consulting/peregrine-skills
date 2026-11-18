#!/usr/bin/env node
// Creates a NEW draft Retell LLM + agent from the voice-receptionist output folder.
// Default is a dry run: prints the request bodies and sends nothing.
// It never updates or publishes an existing agent and never touches phone numbers.
//
// Usage:
//   node create_retell_agent.mjs <output-folder> [--create] [--name "Mia, Lakeside Dental (draft)"]
//     [--voice <voice_id>] [--model <llm model>] [--tool-base https://your-tools.example.com]
//
// Needs RETELL_API_KEY in the environment for --create. TOOL_SECRET (optional) is sent as the
// x-tool-secret header on every custom tool. Field names: see references/retell-notes.md.

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const args = process.argv.slice(2);
const dir = args.find((a) => !a.startsWith("--"));
const flag = (name) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};
const CREATE = args.includes("--create");

if (!dir) {
  console.error("Usage: node create_retell_agent.mjs <output-folder> [--create]");
  process.exit(1);
}

const read = (f, fallback) => {
  const p = join(dir, f);
  if (!existsSync(p)) {
    if (fallback !== undefined) return fallback;
    console.error(`Missing ${p}`);
    process.exit(1);
  }
  return readFileSync(p, "utf8").trim();
};

const prompt = read("prompt.md");
const firstSentence = read("first-sentence.txt");
const voicemail = read("voicemail.txt", "");
const tools = JSON.parse(read("tools.json", "[]"));
const postCall = JSON.parse(read("post-call-fields.json", "[]"));

const toolBase = (flag("tool-base") || process.env.TOOL_BASE_URL || "").replace(/\/$/, "");
const toolSecret = process.env.TOOL_SECRET || "";

const END = { type: "end_call", name: "end_call", description: "End the call after saying goodbye, or if the caller asks to end it." };
const custom = tools
  .filter((t) => t.name !== "end_call")
  .map((t) => ({
    type: "custom",
    name: t.name,
    description: t.description,
    url: toolBase ? `${toolBase}/tools/${t.name}` : `https://REPLACE-ME.example.com/tools/${t.name}`,
    method: "POST",
    headers: toolSecret ? { "x-tool-secret": toolSecret } : {},
    parameters: t.parameters,
    speak_during_execution: Boolean(t.speak_during),
    ...(t.speak_during ? { execution_message_type: "static_text", execution_message_description: t.speak_during } : {}),
    speak_after_execution: true,
    timeout_ms: t.timeout_ms || 10000,
  }));

const llmBody = {
  model: flag("model") || process.env.RETELL_MODEL || undefined,
  general_prompt: prompt,
  begin_message: firstSentence,
  general_tools: [END, ...custom],
};

const agentBody = (llmId) => ({
  agent_name: flag("name") || "Receptionist (draft, not on a number)",
  voice_id: flag("voice") || process.env.RETELL_VOICE || "REPLACE-WITH-VOICE-ID",
  response_engine: { type: "retell-llm", llm_id: llmId },
  interruption_sensitivity: 0.8,
  enable_backchannel: false,
  voice_speed: 0.97,
  ...(voicemail ? { voicemail_option: { action: { type: "static_text", text: voicemail } } } : {}),
  post_call_analysis_data: postCall,
});

if (!CREATE) {
  console.log("DRY RUN. Nothing sent. Add --create to create a new draft agent.\n");
  console.log("POST /create-retell-llm\n" + JSON.stringify(llmBody, null, 2));
  console.log("\nPOST /create-agent\n" + JSON.stringify(agentBody("<llm_id from step 1>"), null, 2));
  if (!toolBase) console.log("\nNote: no --tool-base given, tool URLs are placeholders.");
  process.exit(0);
}

const key = process.env.RETELL_API_KEY;
if (!key) {
  console.error("Set RETELL_API_KEY to use --create.");
  process.exit(1);
}

async function api(path, body) {
  const r = await fetch("https://api.retellai.com" + path, {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const text = await r.text();
  let data;
  try { data = JSON.parse(text); } catch { data = text; }
  if (!r.ok) throw new Error(`${path} -> ${r.status}: ${typeof data === "string" ? data : JSON.stringify(data)}`);
  return data;
}

const llm = await api("/create-retell-llm", llmBody);
console.log(`Created LLM ${llm.llm_id}`);
const agent = await api("/create-agent", agentBody(llm.llm_id));
console.log(`Created draft agent ${agent.agent_id}. It is not attached to any phone number.`);
console.log("Test it with a web call in the Retell dashboard. Attaching a number is a separate, manual step.");

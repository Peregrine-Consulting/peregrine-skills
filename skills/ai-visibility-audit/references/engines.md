# Engines, endpoints and crawlers

Checked: 2026-11-18. These facts go stale. If this date is more than about three months old, confirm model names and endpoints with a quick web search before a paid run, then update this file.

Load this before running probe_engines.py, or when a probe fails with a 400/404.

## What each engine is, for this audit

| Engine key | What it stands in for | Env vars | Default model | Notes |
|---|---|---|---|---|
| chatgpt | ChatGPT with search | OPENAI_API_KEY, OPENAI_MODEL | gpt-5-mini | Responses API with the web_search tool. Answers via API are close to, not identical to, the ChatGPT app. Say "ChatGPT (API, with search)" in the report method line. |
| gemini | Gemini app / Google grounding | GEMINI_API_KEY, GEMINI_MODEL | gemini-2.5-flash | generateContent with the google_search tool. Source URIs come back as redirect links; the chunk title is usually the domain, which is what the script records. |
| perplexity | Perplexity | PERPLEXITY_API_KEY, PERPLEXITY_MODEL | sonar | Chat completions; sources in citations and search_results. |
| claude | Claude with web search | ANTHROPIC_API_KEY, ANTHROPIC_MODEL | claude-sonnet-5-5 | Messages API with the web search server tool. |
| google_ai | Google AI Overviews / AI Mode | none in this script | n/a | No clean public API. Check by hand in a logged-out browser, or through a SERP API (SerpApi, DataForSEO) if the user has one. Otherwise list it under engines_not_checked. |
| copilot | Microsoft Copilot | none | n/a | Manual only. Draws heavily on Bing; Bing Places and Bing Webmaster Tools matter. |

Cost: a 12-question set across three engines with one run is 36 calls, usually well under a few dollars with the default small models. Say the estimate before running and get an OK if the user is paying.

## Manual capture (no keys)

Open each engine logged out (or in a fresh profile), set location if the engine allows it, paste each question verbatim, and save the full answer text plus every source link into captures.json in the same shape probe_engines.py writes. Screenshots are good evidence for the report appendix. Ask the user to paste answers if you cannot open a browser.

## AI crawlers in robots.txt

Blocking these removes the site from live answers: OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, Claude-User, Bingbot.

These are training-only. Blocking them is a policy choice, not a visibility bug: GPTBot, ClaudeBot, Google-Extended, CCBot. Flag it, explain the trade, and let the owner decide.

Googlebot governs AI Overviews. Never recommend blocking it.

## llms.txt

A plain-markdown map of the site at /llms.txt. Cheap to add and harmless. Treat it as a small signal, not a fix that moves rankings on its own; no major engine has committed to using it as a ranking input. Score weight is 2 of 100 for that reason.

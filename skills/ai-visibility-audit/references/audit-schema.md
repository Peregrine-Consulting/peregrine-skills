# audit.json schema

Load this when assembling audit.json for scripts/build_report.py.

The agent writes this file. It combines captures.json (from probe_engines.py or pasted answers), signals.json (from site_signals.py) and the agent's own reading. Any field you did not check is null or omitted, never guessed. The script drops unchecked parts from the score and says so on the report.

    {
      "business": {
        "name": "Desert Ridge Family Dental",
        "domain": "desertridgedental.example",
        "location": "Phoenix, AZ",
        "category": "family dentist",
        "date": "2026-11-18"
      },
      "engines_used": ["chatgpt", "gemini", "perplexity"],
      "engines_not_checked": ["google_ai"],
      "headline": null,
      "summary": "Two or three plain sentences. What the buyer sees today, in their words.",
      "what_this_means": "Optional paragraph. Name the competitors that win and the one reason they win.",
      "questions": [
        {
          "question": "Who is the best family dentist in north Phoenix?",
          "results": [
            {"engine": "chatgpt", "state": "absent", "named_instead": ["Bright Smile Dental", "Cactus Family Dentistry"]},
            {"engine": "gemini", "state": "mentioned", "named_instead": []},
            {"engine": "perplexity", "state": "not_observed", "named_instead": []}
          ]
        }
      ],
      "competitors": [
        {"name": "Bright Smile Dental", "times_named": 9, "why_they_win": "FAQ pages answer insurance questions by plan name; 400+ Google reviews; listed on the three directories the engines cite."}
      ],
      "signals": { "...": "paste the full output of site_signals.py here" },
      "reputation": {
        "gbp_found": true,
        "gbp_reviews": 38,
        "gbp_rating": 4.7,
        "directories_found": ["Yelp", "Healthgrades"],
        "knowledge_panel": null,
        "wikidata": false
      },
      "findings": [
        {"title": "ChatGPT cannot read your services page", "detail": "The page is an empty JavaScript shell until it runs in a browser.", "evidence": "signals.pages[1].rendering = client_side_shell"}
      ],
      "fixes": [
        {"title": "Add an insurance FAQ page", "why": "Four of the twelve questions were about insurance and every winning answer cited a page that names the plans accepted.", "impact": "high", "effort": "low", "owner": "web"}
      ],
      "cta": {
        "headline": "Want these fixed in the next 30 days?",
        "text": "One sentence on what happens on the call.",
        "button": "Book a 15-minute call",
        "url": "https://cal.example/your-link"
      }
    }

States, per answer: cited (the business's own site is a source), mentioned (named, but its site is not a source), absent (answer observed, business not named), not_observed (no answer captured, for any reason).

The example names above are illustrative. Never ship a report with example data in it.

# pages.json schema

Load this when writing the source file for scripts/build_pages.py.

    {
      "site": {
        "name": "North Phoenix Family Dental",
        "base_url": "https://www.example-dental.com",
        "publisher": "North Phoenix Family Dental",
        "publisher_url": "https://www.example-dental.com",
        "author": {"name": "Dr. Jane Rivera, DDS", "url": "https://www.example-dental.com/about", "person": true},
        "accent": "#0f766e",
        "updated": "2026-11-18",
        "hub_title": "Questions patients ask",
        "hub_intro": "Straight answers about insurance, emergencies, costs and treatment, from our dentists.",
        "summary": "One sentence that says who publishes this and what it covers.",
        "disclosure": "",
        "nav": [{"label": "Book", "url": "https://www.example-dental.com/book"}],
        "footer": "North Phoenix Family Dental · 1234 W Example Rd, Phoenix, AZ · (602) 555-0100",
        "cta": {"headline": "Need to be seen this week?", "text": "We keep same-day slots for emergencies.", "button": "Book a visit", "url": "https://www.example-dental.com/book"}
      },
      "pages": [
        {
          "slug": "emergency-dentist-sunday",
          "group": "Emergencies",
          "question": "Is there a dentist open on Sunday in north Phoenix?",
          "short_answer": "Yes. We see emergency patients on Sundays from 9am to 1pm at our Example Rd office; call before you come so we can hold a chair.",
          "meta_description": "",
          "updated": "2026-11-18",
          "sections": [
            {"heading": "What counts as a dental emergency", "body": "Paragraphs. Blank line between paragraphs.\n\n- bullets start with a dash\n- [links](https://example.com) and **bold** work"},
            {"heading": "What a Sunday visit costs", "body": "..."}
          ],
          "faqs": [{"q": "Do you take walk-ins on Sunday?", "a": "Yes, but callers are seen first."}],
          "related": ["cracked-tooth-what-to-do"],
          "sources": ["[ADA: dental emergencies](https://www.ada.org/...), checked 2026-11-18"],
          "noindex": false
        }
      ]
    }

Every name, address and number above is illustrative. Replace all of it with the user's real facts, or leave the field empty.

disclosure: required on any page that compares the publisher's own product with others (see comparison-rules.md). It shows as a strip at the top and again in the footer.

author: a real person with real credentials beats "Our team". Use a person only if that person reviewed the page. Never invent a credential.

--snippets writes <slug>.snippet.html per page (JSON-LD for the head, body HTML) for WordPress, Webflow, Squarespace or any CMS. Paste the JSON-LD into the page head (or a header-code block) and the body into the editor in HTML mode.

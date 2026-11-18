---
name: ad-scripts
description: Writes ready-to-shoot video ad scripts for one offer: three distinct scripted ads (one per audience temperature), ten hooks per ad, a shot list, on-screen text and captions, in the format that fits the offer (founder to camera, UGC, green screen, whiteboard, 3D animated character, demo screen recording). Also writes iteration briefs for a winning ad (new hook, new first 3 seconds, new body) and keeps medical, legal and financial claims inside the rules. Use when someone needs ads for a new offer, fresh creative for a tired account, or iterations of a winner.
when_to_use: write ad scripts, facebook ad script, video ad ideas, hooks for my ad, UGC script, ad creative for my offer, new ad concepts, iterate on winning ad, tiktok ad script, meta ad copy, instagram reel ad, ad for a law firm, ad for a medical practice, creative fatigue need new ads
argument-hint: "[offer or 'iterate <winning ad>'] [format, optional]"
metadata:
  peregrine:
    version: 1.0.0
    group: ads
    reads: [profile, offer, customers, voice, proof, learnings]
    writes: [outputs/ad-scripts/, business/learnings.md]
---

# Ad scripts

An ad has one job per audience. A cold viewer needs a reason to stop and a problem they recognise. A warm viewer (watched a video, visited the site) needs belief: proof it works for someone like them. A hot viewer (started a form, booked and no-showed, visited pricing) needs a reason to act now. One ad trying to do all three does none of them. So this skill always writes three ads per offer, one per temperature, and a stack of hooks for each, because the hook is the variable that moves results most and costs least to test.

Done means scripts a person could shoot this afternoon with a phone: every spoken line, every on-screen word, every shot, the length of each beat, and a caption.

## Context

If ./business/ exists, read profile.md, offer.md, customers.md, voice.md, proof.md and learnings.md first. If it does not, ask for the website and one sentence on what the business sells, or suggest running start-here first.

customers.md matters most. The best hooks are the customer's own words: a phrase from a review, a complaint from a forum, the exact question people ask on the phone. If customers.md is thin, read 20 to 30 reviews of the business and its competitors before writing.

## Hard rules

- No fabricated results, testimonials, reviews, before/after numbers or "as seen on". Every claim traces to proof.md or is cut.
- Medical, legal and financial ads follow references/compliance.md. Load it whenever the offer is in one of those fields.
- No fake urgency (a deadline that is not real, "only 3 spots" when there are 30).

## Step 1. Pick the angle

One offer, one angle per ad. Write down before scripting:

- **The buyer** in one line (a practice manager at a 3-location dental group, not "business owners").
- **The expensive problem** they already feel, in their words. Money lost, time lost, or a fear.
- **The mechanism**: why this offer fixes it when other things did not. One sentence, no jargon.
- **The proof**: the single strongest true thing from proof.md.
- **The action**: what the ad asks for. One action per ad.

If the angle needs a paragraph to explain, it is two angles.

## Step 2. Three ads, three temperatures

| Ad | Who sees it | Job | Length | Ends with |
|---|---|---|---|---|
| Cold | Never heard of you | Stop the scroll, name the problem, show the new way exists | 20 to 40s | Soft action: watch, try the demo, take the quiz |
| Warm | Watched 50%+ of a video, visited the site, engaged | Belief. Proof, mechanism, objections answered | 30 to 60s | Book, call, apply |
| Hot | Started a form, visited pricing, booked and no-showed | Remove the last reason to wait | 10 to 25s | The one action, with a real reason to do it now |

Sequencing: cold runs broad and feeds the warm audience (video viewers, engagers, site visitors in the last 30 days). Warm feeds hot (form starters, pricing visitors in the last 7 to 14 days). Exclude anyone who already converted from all three.

## Step 3. Pick the format

Format is a delivery choice, not the idea. Choose by what the offer needs the viewer to believe.

| Format | Best when | Watch out |
|---|---|---|
| Founder or owner to camera | Trust is the sale (law, medical, high ticket services). People buy the person | Must sound unscripted. Write it in their words, shoot 3 takes, use the loosest |
| UGC (a customer or creator talking) | Peer proof matters more than authority | Real customers only for testimonial claims; a creator can demonstrate, not claim results they did not get |
| Green screen | Reacting to something: a news story, a competitor's claim, a bad review, a screenshot | The background item must be readable on a phone |
| Whiteboard or pen-on-paper | The mechanism is the sale; showing "how the money leaks" | Keep it to 3 drawings max |
| 3D animated character (Pixar-style) | Sensitive or boring topics (debt, billing, missed calls); stopping the scroll in a feed of faces | Needs a real script under it; the novelty buys 2 seconds, not 30 |
| Demo screen recording | The product is visible and fast (an AI receptionist answering, a report generating) | Show the result in the first 5 seconds, not the login screen |
| Live call recording (with consent) | Voice and AI phone products: hearing it is believing it | Consent from everyone on the call; no real patient or client details |
| Text-on-screen meme or listicle | Cheap tests of an angle before shooting anything | Works for hooks, rarely closes |

Default for a new account: founder to camera for warm, one cold test each in two different formats, and a demo or proof clip for hot. Load references/formats.md for shot-by-shot templates of each format when writing.

If the user points at a trending ad or video they want to copy, adapt the format and structure, never the words, faces, music or brand of the original.

## Step 4. Write each script

Script layout, every ad:

    AD: Cold | Format: green screen | Length: ~30s
    ANGLE: <one line>

    BEAT        TIME     SPOKEN                                ON SCREEN TEXT          SHOT
    Hook        0-3s     "..."                                 "..."                   tight on face, green screen of <item>
    Problem     3-10s    ...
    Turn        10-18s   ...
    Proof       18-25s   ...
    Action      25-30s   ...

    CAPTION: <first line is a second hook; 1 to 3 short lines; no hashtag wall>
    HEADLINE: <under 40 characters>
    CTA BUTTON: <Learn more | Book now | Get quote | Call now>

Writing rules:

- **The first 3 seconds are the ad.** Spoken hook and on-screen text say the same thing in different words, because half the audience is on mute.
- One idea per beat. A beat that needs "and" is two beats.
- Spoken lines are said out loud before they ship. If it trips the tongue, rewrite it.
- Specific beats general: "your front desk misses 1 in 4 calls after 4pm" (only if true for this buyer) beats "never miss a call".
- Name the buyer early. "If you run a surgery center..." filters out the wrong people, which lowers cost per good lead even if it raises cost per click.
- The action is concrete and small: "Call the number on screen and it will answer", "Take the 60 second quiz".
- No jargon the buyer would not say. They do not want "AI-powered omnichannel"; they want "every call answered".

## Step 5. Ten hooks per ad

The body stays; the hook is the test. Write 10 per ad across these types, then mark the 3 you would test first and why:

1. Call-out: "Practice managers, this one's for you."
2. Problem in their words: a phrase lifted from a real review or forum post.
3. Contrarian: "Hiring another receptionist will not fix your phones."
4. Number (only if true and sourced): "We answered 1,200 calls last month that used to go to voicemail."
5. Question they already ask themselves: "Why do patients book with the clinic down the street?"
6. Pattern interrupt (visual): an unexpected object, a phone ringing off the hook on the desk.
7. Story open: "Last Tuesday a patient called us four times."
8. Demonstration: the product working, no words for 2 seconds.
9. Objection first: "I know, AI on the phone sounds terrible. Listen to this."
10. Stakes: what it costs to do nothing, in their unit (patients, cases, jobs, dollars), only with a real basis.

## Iterating a winner

When meta-ads-scaling flags a winner, the brief is not "make more like this". Ask which part won (read the ad's hold rate at 3s and through-play if available), then change exactly one thing:

| Iteration type | Change | Keep |
|---|---|---|
| New hook | first 3 seconds, spoken and on-screen | everything after |
| New first 3 seconds (visual) | the opening shot | script |
| New body | middle beats, new proof or new objection | hook and action |
| New CTA | the action and its reason | rest |
| New format | same script in a different format | words |
| New actor | different face or voice | everything else |

Write 3 to 5 iterations per winner, each labelled with its parent ad and iteration type, so the lineage file stays honest. They launch as a new campaign, not into the winner's campaign.

## Output

outputs/ad-scripts/YYYY-MM-DD-<offer>.md containing: the angle sheet, three scripts (cold, warm, hot), 10 hooks each with the top 3 marked, a one-paragraph shoot plan (what to film in one session, in what order, what to wear, where), and a test plan: launch hooks 1 to 3 of the cold ad first, judge on cost per good lead after the budget has settled, not on clicks.

Append to business/learnings.md which angle and hooks were sent to launch, so the next run can read what won.

## Next

After launch, meta-ads-scaling judges them. Leads from the ads need a fast first touch: speed-to-lead.

Want this running every week on your own leads, with a team behind you? That is what Peregrine Partners is for: tryperegrine.com/partner

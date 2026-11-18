# Deliverability checklist

Load in setup mode, or when replies drop, bounces rise, or the user says emails go to spam. Tool names and prices checked November 2026; check current pricing before quoting it.

## Domains

- Buy 2 to 3 lookalike domains per brand: try<brand>.com, get<brand>.com, <brand>hq.com. Short and believable beats clever. Avoid hyphens and odd TLDs.
- 301 redirect each one to the main site, so a curious prospect lands somewhere real.
- Never send cold email from the main domain or from the inbox the team uses for clients. A complaint spike should only ever hurt a domain you can throw away.
- New domains need a few weeks before they carry volume. Buy them before the copy is written.

## Inboxes

- 2 to 3 per sending domain. More than 3 on one domain raises risk without much gain.
- Real names (sam@, sam.lee@). Same person across domains is fine.
- Google-style or Microsoft-style inboxes from a cold-email inbox reseller (Mailforge, Maildoso and similar) are usually cheaper per inbox than buying Workspace seats directly. Any reputable provider works.
- Profile photo and a plain signature: name, title, business name. No images, no links in the signature.

## DNS (every sending domain)

- SPF: one record that includes the mail provider.
- DKIM: enabled at the provider, record published.
- DMARC: start at p=none with a rua reporting address. Move to p=quarantine after about a month of clean reports.
- Test with a mail-tester style service before warmup. Aim for a clean score.

## Warmup and ramp

- Connect inboxes to the sending tool and turn warmup on. 2 to 3 weeks before the first cold send. Leave warmup on during campaigns.
- Week 1: about 10 cold sends per inbox per day.
- Add about 5 per inbox per day each week.
- Hold at about 30 per inbox per day. Scale by adding inboxes, not by pushing one inbox past 30 to 40.
- Example math (illustrative): 3 domains x 3 inboxes x 30 a day = 270 a day, about 1,350 a week.

## Campaign settings

- Send window: weekdays, business hours in the prospect's time zone.
- Plain text only. No images, no HTML templates.
- Open tracking off. Link tracking off for at least the first month on a new domain.
- List-Unsubscribe header on.
- Stop on reply on. Stop for the whole company on reply on, so one reply from a business stops everyone there.
- Emails 2+ in the same thread (blank subject).
- No links in email 1.

## List hygiene

- Verify every address before import. Drop invalid. Send catch-all addresses last and watch their bounce rate separately.
- Role addresses (info@, office@) are fine for small local businesses, where the owner often reads them, but they reply less. Prefer a named address.
- Dedupe against everyone you have emailed in the last 90 days and the do-not-contact list.

## Watch weekly, per inbox

- Bounce rate under 2 percent. Over 3 percent: pause the campaign and re-verify the list.
- Spam complaints: any spike, pause that inbox.
- Reply rate falling on one inbox while others hold: that inbox is landing in spam. Pause it, let warmup run alone for 1 to 2 weeks.
- Placement test monthly with a seed-list tool if available.

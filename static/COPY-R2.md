# Static Meta ads, round 2: one sentence per image (Oct 12, 2026)

Each image carries the logo and one sentence: a hook with a concrete outcome (Hormozi pass, Oct 13). Nothing else goes on the image, because Meta's own button ("Book now") carries the CTA. The primary text follows one shape: hook, then what you get and how fast, then the free offer and the next step.

- **Singles:** 12 ads (MB1–MB6, LB1–LB6) at 4:5 Feed and 9:16 Stories/Reels. Each 9:16 is outpainted from the same photo.
- **Carousels:** 2 carousels of 5 cards each (MC1–MC5, LC1–LC5) at 4:5, one sentence per card.
- **Photos:** Higgsfield `gpt_image_2_5` (high, 2K). The in-clinic shots used real clinic photos as references. Outpaints were done with Higgsfield `outpaint`. That's 15 generations and 18 outpaints; the balance went from 1,719 to 1,502 credits during this session.
- **Re-render:** `python3 render.py --page round2` (copy lives in `round2.js`). `gen/prep.py` rebuilds the backgrounds from the downloads in `gen/`.

Use the same destinations, neutral UTMs and ad-set structure as round 1 (see COPY.md). Name the ads by their IDs so `utm_content={{ad.name}}` stays readable.

## Menopause singles

| Ad | On the image | Primary text | Headline |
|---|---|---|---|
| MB1 | Wide awake at 3 a.m., again. | Night sweats and 3 a.m. wake-ups are common in perimenopause, and they're treatable. Start within days with our NP-led team in Barrie: no referral, and your first call is free. | Free 15-min call · No referral |
| MB2 | Brain fog can be perimenopause, not just a busy life. | Brain fog, lost words, keys in the fridge: these can be perimenopause, not just a busy life. Find out with comprehensive labs and a 60-minute NP visit. Book your free 15-minute call. | Labs + a 60-minute NP visit |
| MB3 | Start menopause care in Barrie within days. | Menopause and perimenopause care in Barrie, led by a Nurse Practitioner who keeps a small panel of patients. Start within days, no referral needed. Book your free 15-minute call. | Start within days |
| MB4 | Hot flashes don't wait, and neither should you. | Hot flashes, night sweats and broken sleep are common in perimenopause, and worth treating. Start within days with our NP-led team in Barrie. Book your free 15-minute call. | Free 15-min call · No referral |
| MB5 | No referral, no family doctor, and you start within days. | No referral and no family doctor needed. Start menopause care in Barrie within days, with the same Nurse Practitioner at every visit. Book your free 15-minute call. | No referral needed |
| MB6 | Your first NP visit is a full 60 minutes. | Your first Nurse Practitioner visit is a full 60 minutes, one-on-one, once your labs are back. Then you keep the same NP at every visit. Book your free 15-minute call. | A 60-minute first visit |

## Longevity singles

| Ad | On the image | Primary text | Headline |
|---|---|---|---|
| LB1 | Your own Nurse Practitioner in Barrie, with same or next-day visits. | Your own Nurse Practitioner in Barrie: same or next-day visits when something can't wait, unlimited in-person and virtual appointments, and a full longevity assessment every year. $1,495 a year. Book a free 15-minute intro call. | Your own NP · $1,495/yr |
| LB2 | Sick today, seen tomorrow, by an NP who knows you. | Members get same or next-day visits for time-sensitive concerns, with the same Nurse Practitioner every time. $1,495 a year, everything included. Book a free 15-minute intro call. | Same or next-day visits |
| LB3 | See what's working, every 90 days. | An InBody scan every 90 days shows exactly what's changing: muscle, body fat and visceral fat, reviewed with your NP. Included in the $1,495 membership. Book a free 15-minute intro call. | Body scans every 90 days |
| LB4 | Know exactly what to do for your health this year. | Every member gets a 60-minute longevity assessment and a written 12-month plan, so you know exactly what to focus on this year. $1,495 a year, everything included. Book a free 15-minute intro call. | Your 12-month health plan |
| LB5 | Your own Nurse Practitioner for about $4 a day. | Your own Nurse Practitioner, unlimited visits, an annual longevity assessment and body scans every 90 days: $1,495 a year, about $4 a day, HSA eligible. Book a free 15-minute intro call. | About $4 a day, all included |
| LB6 | OHIP still covers your medically necessary labs. | Optimal is private, but OHIP still covers the medically necessary labs, imaging and specialist visits your NP orders. The advanced markers OHIP doesn't cover are included. Book a free 15-minute intro call. | OHIP still covers your labs |

## Menopause carousel (MC1 → MC5)

**Primary text:** Menopause care in Barrie, in 3 simple steps. Swipe to see exactly how it works, then book your free 15-minute call. No referral needed.

| Card | On the image | Card headline |
|---|---|---|
| MC1 | Menopause care in Barrie starts with a free 15-minute call. | Free 15-min call |
| MC2 | Your hormone lab panel is covered by OHIP. | OHIP-covered labs |
| MC3 | Then a full hour with your Nurse Practitioner. | 60-minute NP visit |
| MC4 | You get a written plan and the same NP every visit. | Same NP, written plan |
| MC5 | No referral needed: book your free call at beoptimal.ca. | Book your free call |

## Longevity carousel (LC1 → LC5)

**Primary text:** Everything $1,495 a year gets you, about $4 a day and HSA eligible. Swipe, then book a free 15-minute intro call. No commitment.

| Card | On the image | Card headline |
|---|---|---|
| LC1 | Here's everything $1,495 a year gets you. | About $4 a day |
| LC2 | Your own Nurse Practitioner, with unlimited visits. | Unlimited visits |
| LC3 | A 60-minute assessment and a written plan, every year. | Annual assessment |
| LC4 | A body composition scan every 90 days. | Scans every 90 days |
| LC5 | Start with a free 15-minute call, no commitment. | Free 15-min intro call |

## Notes

- **People and settings:** everyone pictured is AI-generated, and no clinician's face is shown. The waiting room in MB5, MC5 and LC1 is the real clinic; LC1 is an unedited real photo.
- **Facts checked against the landing pages:**
  - MB6 says "first NP visit", because the first clinic visit is the 30-minute orientation.
  - MC2 says "hormone lab panel", because vitamin D and SHBG are paid add-ons.
- **Carousels:** they're rendered as 4:5 cards. If Ads Manager forces 1:1 for a carousel placement, re-render them as 1:1. Don't let Meta crop them, because the crop would cut the sentence.

# Static Meta ads, round 2: one sentence per image (Oct 12, 2026)

Each image carries the logo and one sentence. Nothing else goes on the image, because Meta's own button ("Book now") carries the CTA. The primary text stays just as short: two sentences at most.

- **Singles:** 12 ads (MB1–MB6, LB1–LB6) at 4:5 Feed and 9:16 Stories/Reels. Each 9:16 is outpainted from the same photo.
- **Carousels:** 2 carousels of 5 cards each (MC1–MC5, LC1–LC5) at 4:5, one sentence per card.
- **Photos:** Higgsfield `gpt_image_2_5` (high, 2K). The in-clinic shots used real clinic photos as references. Outpaints were done with Higgsfield `outpaint`. Total spend was about 70 credits.
- **Re-render:** `python3 render.py --page round2` (copy lives in `round2.js`). `gen/prep.py` rebuilds the backgrounds from the downloads in `gen/`.

Use the same destinations, neutral UTMs and ad-set structure as round 1 (see COPY.md). Name the ads by their IDs so `utm_content={{ad.name}}` stays readable.

## Menopause singles

| Ad | On the image | Primary text | Headline |
|---|---|---|---|
| MB1 | Wide awake at 3 a.m., again. | Night sweats and broken sleep are common in perimenopause. Book a free 15-minute call with our NP-led team in Barrie. | Menopause care in Barrie |
| MB2 | Brain fog is a common perimenopause symptom. | Brain fog, poor sleep and mood changes can all be part of perimenopause. Book a free 15-minute call to see if our program fits. | NP-led menopause care |
| MB3 | Menopause care in Barrie, led by a Nurse Practitioner. | Our menopause and perimenopause program is led by a Nurse Practitioner, here in Barrie. Book a free 15-minute call. | No referral needed |
| MB4 | Hot flashes don't wait for a good time. | Hot flashes are one of the most common signs of perimenopause. Book a free 15-minute call with our NP-led team. | Menopause care in Barrie |
| MB5 | No referral or family doctor needed. | Start menopause care in Barrie without a referral or a family doctor. Book a free 15-minute call. | Free 15-min intro call |
| MB6 | Your first NP visit is a full 60 minutes. | Your first Nurse Practitioner visit is 60 minutes, one-on-one. Book a free 15-minute call to get started. | A 60-minute first visit |

## Longevity singles

| Ad | On the image | Primary text | Headline |
|---|---|---|---|
| LB1 | Barrie has a new kind of health clinic. | Optimal is a private, NP-led membership clinic in Barrie. Book a free 15-minute intro call. | A new kind of health clinic |
| LB2 | Same or next-day visits when something can't wait. | Members get same or next-day appointments for time-sensitive concerns. $1,495 a year, everything included. | Same or next-day visits |
| LB3 | Your body composition, measured every 90 days. | Every membership includes an InBody body composition scan every 90 days. Book a free 15-minute intro call. | Scans every 90 days, included |
| LB4 | Every member gets a written 12-month plan. | Your annual longevity assessment ends with a written plan for the next 12 months. Book a free 15-minute intro call. | Your 12-month health plan |
| LB5 | Your own Nurse Practitioner for $1,495 a year. | Your own Nurse Practitioner and unlimited in-person and virtual visits for $1,495 a year. HSA eligible. | Unlimited visits, one annual fee |
| LB6 | Medically necessary labs are still covered by OHIP. | Optimal is private, but OHIP still covers the medically necessary labs, imaging and specialist visits your NP orders. | OHIP still covers your labs |

## Menopause carousel (MC1 → MC5)

**Primary text:** How menopause care works at Optimal, one step at a time. No referral needed.

| Card | On the image | Card headline |
|---|---|---|
| MC1 | It starts with a free 15-minute call. | Free 15-min call |
| MC2 | Your hormone lab panel is covered by OHIP. | OHIP-covered labs |
| MC3 | Then a full hour with your Nurse Practitioner. | 60-minute NP visit |
| MC4 | You get a written treatment plan. | Written treatment plan |
| MC5 | Book your free call at beoptimal.ca. | Book your free call |

## Longevity carousel (LC1 → LC5)

**Primary text:** What the Optimal membership includes, one card at a time. $1,495 a year, HSA eligible.

| Card | On the image | Card headline |
|---|---|---|
| LC1 | Here's what $1,495 a year includes. | $1,495 a year |
| LC2 | Your own Nurse Practitioner, with unlimited visits. | Unlimited visits |
| LC3 | A 60-minute assessment and a written plan, every year. | Annual assessment |
| LC4 | A body composition scan every 90 days. | Scans every 90 days |
| LC5 | Book a free intro call at beoptimal.ca. | Book a free intro call |

## Notes

- **People and settings:** everyone pictured is AI-generated, and no clinician's face is shown. The waiting room in MB5, MC5 and LC1 is the real clinic; LC1 is an unedited real photo.
- **Facts checked against the landing pages:**
  - MB6 says "first NP visit", because the first clinic visit is the 30-minute orientation.
  - MC2 says "hormone lab panel", because vitamin D and SHBG are paid add-ons.
- **Carousels:** they're rendered as 4:5 cards. If Ads Manager forces 1:1 for a carousel placement, re-render them as 1:1. Don't let Meta crop them, because the crop would cut the sentence.

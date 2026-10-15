# Video ads, Oct 12, 2026: Meta ads + Instagram

There are four ads. LV1, LV2 and MV1 were shot with Cheryl Cairns (care coordinator), and LV3 (added Oct 15) with Rubeana Deol, NP (Clinical Director):

| ID | Ad | Meta ad cuts | Instagram reel |
|---|---|---|---|
| **LV1** | Longevity, "3 things to know before you book." | LV1-T, 35.3 s | Tight, 35.3 s |
| **LV2** | Longevity, "A full hour. Every year." | LV2-T, 36.5 s | Tight, 36.5 s |
| **MV1** | Menopause, "I just don't feel like myself." | MV1-T, 33.8 s (music only on the end card) | Tight, 33.8 s |
| **LV3** | Longevity, "An hour with an NP who listens." (Oct 15) | LV3-T | n/a (Meta ad only) |

The two sets differ only in the end card. The **Meta ad** end card says "Book your free intro call", because Meta's own *Book now* button carries the click. The **Instagram** end card says "Comment LONGEVITY" / "Comment MENOPAUSE" instead, because a button drawn on an organic reel can't be tapped and the keyword triggers the existing auto-DM.

Re-render: `python3 studio.py ads/longevity_ad2_full_hour.py` (Meta, both cuts) · `… --channel=ig` (Instagram reel) · `… --channel=ig --cover` (cover).

---

## 1 · Meta ads

Only the Tight cuts run as Meta ads (Peter, Oct 12). The Full cuts stay in `out/` but are not handed off.

### Setup (same as the static rounds, see `static/COPY.md`)

| | LV2 Longevity | MV1 Menopause |
|---|---|---|
| Ad set | The Longevity membership ad set (alongside L1–L6 / LB1–LB6) | The Menopause ad set (alongside M1–M6 / MB1–MB6) |
| Ad names | `LV1-T`, `LV2-T`, `LV3-T` | `MV1-T` |
| Destination | `https://www.beoptimal.ca/membership` | `https://www.beoptimal.ca/services/menopause-and-perimenopause-care` |
| URL parameters | `utm_source=meta&utm_medium=paid&utm_campaign=opt-b-q4&utm_content={{ad.name}}` | `utm_source=meta&utm_medium=paid&utm_campaign=opt-a-q4&utm_content={{ad.name}}` |
| CTA button | Book now | Book now |

**How to upload each ad.** Upload both files as one ad: the **4x5 Feed** file and the **9x16 Stories+Reels** file. Turn on *placement asset customization* so Meta serves the 9:16 file in Stories and Reels and the 4:5 file in Feed.

- **Thumbnail:** use the matching `thumbnail` jpg. It is the hook frame.
- **Captions:** they are burned in, so leave Meta's auto-generated captions **off** or they'll double up. The `.srt` is only needed if you ever turn them on.

### LV1 · Longevity · "3 things to know before you book."

**Primary text (short)**
3 things to know before you book, from Cheryl, our care coordinator. Your own Nurse Practitioner, unhurried visits and fast appointments for $1,495 a year. Book a free 15-minute intro call.

**Primary text (long)**
Three things to know before you book, from Cheryl, our care coordinator:

1. Every member gets a 60-minute annual longevity assessment with their Nurse Practitioner, including comprehensive bloodwork.
2. Thorough, unrushed appointments. We cap membership to keep it that way.
3. Faster appointment times, so you're seen when you need to be.

$1,495 a year, about $4 a day, everything included and HSA eligible. Book a free 15-minute intro call. No commitment.

**Headline:** 3 things to know before you book · **Description:** About $4 a day, all included

### LV2 · Longevity · "A full hour. Every year."

**Primary text (short)**
When did anyone last spend a full hour on your health? Every Optimal member gets one, every year, with their Nurse Practitioner. Book a free 15-minute intro call.

**Primary text (long)**
A full hour with your Nurse Practitioner, every year.

Every Optimal member gets an annual longevity assessment: 60 minutes on your labs, your body composition and your goals, then a written plan for the next 12 months.

$1,495 a year, about $4 a day, everything included. We cap membership so visits stay unhurried. Book a free 15-minute intro call.

**Headline:** A full hour. Every year. · **Description:** About $4 a day, all included

### LV3 · Longevity · "An hour with an NP who listens."

**Primary text (short)**
Want to optimize your health? Every Optimal member gets a one-hour annual physical with a Nurse Practitioner who listens, then labs to check the biomarkers that matter. Book a free 15-minute intro call.

**Primary text (long)**
Optimizing your health starts with an hour.

Every Optimal member gets a one-hour annual physical with their Nurse Practitioner: a detailed assessment, then labs to check the biomarkers that matter for your overall health.

$1,495 a year, about $4 a day, everything included. We cap membership so visits stay unhurried. Book a free 15-minute intro call. No commitment.

**Headline:** An hour with an NP who listens · **Description:** About $4 a day, all included

### MV1 · Menopause · "I just don't feel like myself."

**Primary text (short)**
"I just don't feel like myself." It's what our care coordinator hears most. You don't need a diagnosis to reach out: book a free 15-minute call. No referral needed.

**Primary text (long)**
"I just don't feel like myself." It's what our care coordinator hears most often.

Brain fog, broken sleep, mood changes, cycles that have suddenly shifted. You don't need a diagnosis to reach out.

Our NP-led menopause and perimenopause program in Barrie starts within days, with labs and a 60-minute visit with the same NP every time. Your first step is a free 15-minute call. No referral needed.

It's a private program: $895 + HST for the first 3 months, and your bloodwork is OHIP-covered.

**Headline:** Menopause care in Barrie · **Alt headline:** You don't need a diagnosis · **Description:** Free 15-min call · No referral

---

## 2 · Instagram (organic): post as a Reel

On Instagram every video now posts as a Reel. It plays in the Reels tab and in followers' feeds, and the profile grid shows the centre 3:4 of the cover. The covers are built for that crop, in the same style as the grid's other reel covers (C4, C1).

**How to post (Meta Business Suite, on a computer)**
1. Make sure the keyword auto-replies from `optimal-instagram/pack/auto-dm.txt` are live first. The reels end on "Comment LONGEVITY" / "Comment MENOPAUSE".
2. Create a reel and upload the `.mp4`.
3. Upload the `cover.jpg` as the cover.
4. Paste `caption.txt`.
5. Leave **Share to Facebook** off for now, as with the rest of the grid.
6. Don't add Instagram music. The reel already has the quiet brand bed under the voice.

### LV1 caption
Three things to know before you book, from Cheryl, our care coordinator.

1. Every member gets a 60-minute annual longevity assessment with their nurse practitioner, including comprehensive bloodwork.
2. Thorough, unrushed appointments.
3. Faster appointment times, so you're seen when you need to be.

Comment LONGEVITY and we'll send you the details.

#Barrie #BarrieOntario #SimcoeCounty #longevity #preventivehealth #healthspan

### LV2 caption
When's the last time anyone spent a full hour on your health?

Every Optimal member gets an annual longevity assessment: a full hour with their Nurse Practitioner, bloodwork, a body composition scan and a written plan for the year ahead.

Comment LONGEVITY and we'll send you the details.

#Barrie #BarrieOntario #SimcoeCounty #longevity #preventivehealth #nursepractitioner

### MV1 caption
"I just don't feel like myself."

It's the thing Cheryl hears most often on the phone. Brain fog, broken sleep, mood changes, cycles that have suddenly shifted. You don't need a diagnosis to reach out.

Comment MENOPAUSE and we'll send you the details.

Educational content only. Not medical advice.

#Barrie #BarrieOntario #SimcoeCounty #menopause #perimenopause #womenshealth

---

## Open item

- **Marker count.** Cheryl says "40-plus biomarkers across 10 health domains" in LV2. The grid's L5 post and the LONGEVITY auto-DM both say **26 markers**, and the ALE report counts 39 markers across 11 systems. The ad copy above avoids naming a number. The on-screen chip says "Comprehensive bloodwork". Her spoken line and its caption still say 40-plus, so settle the number before LV2 runs next to L5.

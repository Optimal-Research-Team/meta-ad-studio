# Static Meta ads, round 3: AI concepts (Oct 13, 2026)

Four concepts from Ad Lab slate 01 (`optimal-ad-lab/creative/briefs/2026-10-13-slate-01.md`). Each has one sentence on the image, plus the logo. Backgrounds are Higgsfield generations: three engraved plates in the brand's sage-on-cream style, and one macro photo.

```
python3 gen/prep3.py           # rebuild assets/r3 from optimal-ad-lab/creative/concepts/raw
python3 render.py --page round3 # renders out/r3/<meno|long>/<ID>_4x5.png + _9x16.png, QA on the Reels safe zone
```

## Setup (same ad sets as rounds 1–2)

| | Menopause (MA1, MA2) | Longevity (LA1, LA2) |
|---|---|---|
| Destination | `https://www.beoptimal.ca/services/menopause-and-perimenopause-care` | `https://www.beoptimal.ca/membership` |
| URL parameters | `utm_source={{site_source_name}}&utm_medium=paid&utm_campaign={{campaign.id}}&utm_term={{adset.id}}&utm_content={{ad.id}}` | same |
| Ad name | `MA1`, `MA2` | `LA1`, `LA2` |
| CTA button | Book now | Book now |
| Upload | 4:5 for Feed + 9:16 for Stories/Reels, one ad, placement asset customization | same |
| AI label | **On** (realistic AI imagery) | **On** |

Use the id-based URL parameters above, not `{{ad.name}}`, because Ad Lab joins each booking to its ad by `ad.id`. Names can be edited; ids never change.

### MA1 · "Three months, one Nurse Practitioner, one price: $895."
**Primary text:** Menopause care in Barrie with the price up front. The Foundation Program (months 1–3) is $895 + HST: labs, a body composition scan, a 60-minute NP visit and two follow-ups. Bloodwork is OHIP-covered. Book a free 15-minute call to see if it fits.
**Headline:** $895 for your first 3 months · **Description:** Free 15-min call · No referral
**Why:** Meta's menopause bookings rarely become appointments (10% vs 24% from Google). Putting the price on the image pre-qualifies the people who book.

### MA2 · "Midlife is a stage, and stages can be planned for."
**Primary text:** Perimenopause often starts in the 40s, years before periods stop. Our NP-led program in Barrie starts with labs and a full 60-minute visit, and you can start within days. Book a free 15-minute call. No referral needed.
**Headline:** A plan for midlife, in Barrie · **Description:** Free 15-min call · No referral

### LA1 · "Your own Nurse Practitioner for about two toonies a day."
**Primary text:** $1,495 a year is about $4 a day for your own Nurse Practitioner, unlimited visits, same or next-day appointments and an hour-long assessment every year. HSA eligible. We cap membership so visits stay unhurried. Book a free 15-minute intro call.
**Headline:** About $4 a day, all included · **Description:** HSA eligible · Free intro call

### LA2 · "Normal is a range. We talk about where you sit in it."
**Primary text:** A lab result can be "normal" and still be worth a conversation. Where you sit in the range, and which way you're moving, is what we look at. Members get a 60-minute longevity assessment every year with their own NP, plus a scan every 90 days. $1,495 a year. Book a free 15-minute intro call.
**Headline:** Where you sit in the range · **Description:** About $4 a day · Free intro call

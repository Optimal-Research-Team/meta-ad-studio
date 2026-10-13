# Static Meta ads, round 1 (Oct 12, 2026)

There are 12 concepts: 6 for menopause and 6 for the Longevity membership. Each one is rendered at 4:5 (1080×1350, Feed) and 9:16 (1080×1920, Stories/Reels). Upload both sizes as **one ad** and use placement asset customization, so Meta serves the 9:16 version in Stories and Reels.

```
python3 render.py          # renders out/meno/*.png, out/long/*.png and out/_sheet.jpg, then runs QA
python3 render.py M1 L3    # renders only the ads you name
```

Copy lives in `content.js` and layouts live in `ads.html`. The QA step fails the render when text spills outside a frame or, on 9:16, outside the Reels safe zone (top 269 px / bottom 672 px / sides 65 px).

## Campaign setup

| | Menopause | Longevity membership |
|---|---|---|
| Destination | `https://www.beoptimal.ca/services/menopause-and-perimenopause-care` | `https://www.beoptimal.ca/membership` |
| URL parameters | `utm_source=meta&utm_medium=paid&utm_campaign=opt-a-q4&utm_content={{ad.name}}` | `utm_source=meta&utm_medium=paid&utm_campaign=opt-b-q4&utm_content={{ad.name}}` |
| Ad names | `M1` … `M6` | `L1` … `L6` |
| Audience | Women 35–60, about 40 km around Barrie, no interests (broad) | Adults 35–70, about 40 km around Barrie, broad |
| CTA button | Book now | Book now |

- **Keep UTM values neutral.** Meta restricts health advertisers whose URLs or events reveal a condition, so never put words like "menopause" in a parameter.
- **Put all 6 ads in one ad set per service.** Each concept is a different format (list, stat, price card, photo, diagram, objection), so Meta's similarity grouping (Andromeda) treats them as separate creatives. Let it allocate the spend, and judge after 7 days.
- **Optimization:** health advertisers mostly can't optimize on website bookings anymore. Run Landing page views as the baseline and test an Instant Form ("Request your free intro call", with one qualifying question) against it.

---

## Menopause

### M1 · Perimenopause is more than hot flashes
**Primary text**
Perimenopause is more than hot flashes. 3 a.m. wake-ups, brain fog, joint aches and mood changes can all be part of it, often years before periods stop.

Our NP-led program in Barrie starts with comprehensive labs and a 60-minute visit, and you can start within days.

Book your free 15-minute call. No referral needed.

**Headline:** More than hot flashes · **Description:** Free 15-min call · No referral

### M2 · 60 minutes
**Primary text**
60 minutes. That's your first visit with our Nurse Practitioner: one-on-one, once your labs are back, with time to tell the whole story.

Then follow-ups at weeks 6 and 12 with the same NP. Bloodwork is OHIP-covered.

Book your free 15-minute call. No referral needed.

**Headline:** A 60-minute first visit · **Description:** Same NP every visit

### M3 · Know the cost before you start
**Primary text**
Menopause care with the price up front:

Free 15-minute call
Foundation Program (months 1–3): $895 + HST, covering labs, a body scan, a 60-minute NP visit and 2 follow-ups
Ongoing Care (month 4 on): $795 a year

Bloodwork is OHIP-covered. No referral needed. Book your free call to see if it fits.

**Headline:** Know the cost before you start · **Description:** Free 15-min call · No referral

### M4 · No referral. No family doctor needed.
**Primary text**
No referral and no family doctor needed. Menopause and perimenopause care in Barrie, led by a Nurse Practitioner, for women 35 and older.

You can start within days, and you see the same NP at every visit.

Book your free 15-minute call.

**Headline:** No referral needed · **Description:** Start within days in Barrie

### M5 · A clear plan, start to finish
**Primary text**
Here's exactly how it works:
1. A free 15-minute call. No commitment.
2. Months 1–3: labs, a body scan, a 60-minute NP visit and 2 follow-ups.
3. Ongoing care with the same NP, 3 visits a year.

No referral needed. Book your free call.

**Headline:** A clear plan, start to finish · **Description:** Free 15-min call · No referral

### M6 · 3 a.m. Wide awake. Again.
**Primary text**
3 a.m. Wide awake. Again.

Night sweats and broken sleep are common in perimenopause, and they're treatable. Our NP-led program in Barrie starts with labs and a 60-minute visit, and you can start within days.

Book your free 15-minute call. No referral needed.

**Headline:** Perimenopause care in Barrie · **Description:** Free 15-min call · No referral

**Extra headlines to rotate:** Start within days · No referral needed · Free 15-min call, no commitment

---

## Longevity membership

### L1 · One price. Everything included.
**Primary text**
One price, everything included: your own Nurse Practitioner, unlimited in-person and virtual visits, a 60-minute longevity assessment every year, body scans every 90 days and a written 12-month plan.

$1,495 a year, about $4 a day. HSA eligible.

We cap membership so visits stay unhurried. Book a free 15-minute intro call.

**Headline:** One price. Everything included. · **Description:** About $4 a day · HSA eligible

### L2 · Keep your family doctor
**Primary text**
Keep your family doctor. Our Nurse Practitioners don't bill OHIP, so there's no outside-use penalty for you or your doctor.

Then add a team with time: same or next-day visits, longer appointments and a longevity plan every year.

Book a free 15-minute intro call. No commitment.

**Headline:** Keep your family doctor · **Description:** Add an NP team with time

### L3 · Unwell on Monday? Seen by Tuesday.
**Primary text**
Unwell on Monday? Seen by Tuesday.

Members get same or next-day visits for time-sensitive concerns, and routine visits within a week, with their own Nurse Practitioner, in person or virtual.

$1,495 a year, everything included. Book a free 15-minute intro call.

**Headline:** Seen same or next day · **Description:** $1,495/yr · all included

### L4 · See what's working, every 90 days
**Primary text**
See what's working. An InBody scan every 90 days tracks your muscle, body fat and visceral fat, and your NP reviews it with you.

Included in the $1,495 membership, with unlimited visits and an annual longevity assessment.

Book a free 15-minute intro call.

**Headline:** Body scans every 90 days · **Description:** Included in membership

### L5 · An hour with your NP. Every year.
**Primary text**
An hour with your Nurse Practitioner, every year. We go through your advanced biomarkers line by line, then write your plan for the next 12 months.

Included in the $1,495 membership, along with unlimited visits.

Book a free 15-minute intro call.

**Headline:** A 60-minute assessment, every year · **Description:** Advanced biomarkers included

### L6 · OHIP still covers your labs
**Primary text**
Optimal is private, but OHIP still covers the medically necessary labs, imaging and specialist visits your NP orders. The advanced longevity markers OHIP doesn't cover are included in your membership.

$1,495 a year, HSA eligible. Book a free 15-minute intro call to ask about your coverage.

**Headline:** OHIP still covers your labs · **Description:** $1,495/yr · HSA eligible

**Extra headlines to rotate:** About $4 a day, all included · Your own NP in Barrie · We cap membership

---

## Guardrails used in this round

| Rule | Source | What it changed |
|---|---|---|
| Don't assert or imply that the viewer has a health condition ("you have…", "your symptoms") | Meta personal-attributes policy | Symptoms are written in the third person or as general facts |
| No client testimonials | CNO advertising guidance | No member quotes in any ad |
| No comparisons with other providers | CNO advertising guidance | No walk-in / GP / "standard clinic" tables |
| Claims must be verifiable | CNO, Competition Act | Every fact matches the live landing page; no "$3,260 value" total; no unsourced stats |
| Promote the service, not a prescription drug | Health Canada | No HRT or hormone names on the images |

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
Perimenopause can begin years before periods stop, and hot flashes are only one part of it. Sleep, mood, focus, joints and energy can all shift.

Our NP-led program in Barrie starts with a 60-minute assessment and comprehensive labs. No referral needed.

Book a free 15-minute call to see if it's a fit.

**Headline:** Menopause care in Barrie · **Description:** Free 15-min intro call

### M2 · 60 minutes
**Primary text**
The first visit with our Nurse Practitioner is 60 minutes, one-on-one, booked after the bloodwork is back. Then structured follow-ups at weeks 6 and 12 with the same NP.

Comprehensive bloodwork is OHIP-covered. No referral needed.

Book a free 15-minute call with our care coordinator.

**Headline:** A 60-minute first visit · **Description:** Same NP every visit

### M3 · Know the cost before you start
**Primary text**
Menopause care with the price up front:

Free 15-minute intro call
Foundation Program (months 1–3): $895 + HST
Ongoing Care (month 4 on): $795 a year

Bloodwork is OHIP-covered, and NP receipts may be claimable on extended health plans. Book your free call.

**Headline:** Menopause care, priced up front · **Description:** No referral needed

### M4 · No referral. No family doctor needed.
**Primary text**
No referral or family doctor needed. Our menopause and perimenopause program is led by a Nurse Practitioner, for women 35 and older, at our clinic in Barrie, with appointments within days.

Book a free 15-minute call to see if the program is right for you.

**Headline:** No referral needed · **Description:** 630 Huronia Rd, Barrie

### M5 · A clear plan, start to finish
**Primary text**
How it works:
1. A free 15-minute call with our care coordinator
2. Foundation Program (months 1–3): labs, an InBody scan, a 60-minute NP intake and two follow-ups
3. Ongoing care with the same NP: three visits a year, prescriptions managed

Book your free call. No commitment.

**Headline:** A clear plan, start to finish · **Description:** Free 15-min intro call

### M6 · 3 a.m. Wide awake. Again.
**Primary text**
3 a.m. Wide awake. Again.

Night sweats and broken sleep are common in perimenopause. Our NP-led program in Barrie starts with a 60-minute assessment and comprehensive labs.

Book a free 15-minute call. No referral needed.

**Headline:** Perimenopause care in Barrie · **Description:** Free 15-min intro call

**Extra headlines to rotate:** Seen in days, no referral · NP-led menopause care · 60-minute first visit

---

## Longevity membership

### L1 · One price. Everything included.
**Primary text**
Your own Nurse Practitioner, unlimited in-person and virtual visits, an annual 60-minute longevity assessment with advanced biomarkers, quarterly InBody scans and a written 12-month plan.

$1,495 a year. HSA eligible.

Book a free 15-minute intro call with our care coordinator.

**Headline:** One price. Everything included. · **Description:** HSA eligible

### L2 · Keep your family doctor
**Primary text**
Joining Optimal doesn't mean leaving your family doctor. Our Nurse Practitioners don't bill OHIP, so there's no outside-use penalty for you or your doctor.

Many members keep their GP and use Optimal for same or next-day visits, longer appointments and a longevity plan.

Book a free 15-minute intro call.

**Headline:** Keep your family doctor · **Description:** Private NP membership, Barrie

### L3 · Unwell on Monday? Seen by Tuesday.
**Primary text**
Same or next-day appointments for time-sensitive concerns, and routine visits with your own NP within a week, in person in Barrie or virtually.

Optimal is a private membership clinic: $1,495 a year, everything included.

Book a free 15-minute intro call.

**Headline:** Same or next-day visits in Barrie · **Description:** $1,495/yr, all included

### L4 · See what's working, every 90 days
**Primary text**
Every 90 days, an InBody scan tracks muscle mass, body fat and visceral fat, so you and your NP can see what's working between annual assessments.

Included in the Optimal membership: $1,495 a year.

Book a free 15-minute intro call.

**Headline:** Body scans every 90 days, included · **Description:** Optimal membership

### L5 · An hour with your NP. Every year.
**Primary text**
Once a year, your Nurse Practitioner spends 60 minutes with you on your labs, your goals and what's changed, then writes your plan for the next 12 months.

Advanced biomarkers that OHIP doesn't cover are included in the $1,495 membership.

Book a free 15-minute intro call.

**Headline:** A 60-minute assessment, every year · **Description:** Advanced biomarkers included

### L6 · OHIP still covers your labs
**Primary text**
Optimal is a private membership, but OHIP still covers the medically necessary labs, imaging and specialist visits your NP orders.

The membership itself is $1,495 a year and HSA eligible.

Book a free 15-minute intro call to ask about your coverage.

**Headline:** Private care. OHIP still covers labs. · **Description:** $1,495/yr · HSA eligible

**Extra headlines to rotate:** Your own NP in Barrie · Seen this week · Unlimited visits, one annual fee

---

## Guardrails used in this round

| Rule | Source | What it changed |
|---|---|---|
| Don't assert or imply that the viewer has a health condition ("you have…", "your symptoms") | Meta personal-attributes policy | Symptoms are written in the third person or as general facts |
| No client testimonials | CNO advertising guidance | No member quotes in any ad |
| No comparisons with other providers | CNO advertising guidance | No walk-in / GP / "standard clinic" tables |
| Claims must be verifiable | CNO, Competition Act | Every fact matches the live landing page; no "$3,260 value" total; no unsourced stats |
| Promote the service, not a prescription drug | Health Canada | No HRT or hormone names on the images |

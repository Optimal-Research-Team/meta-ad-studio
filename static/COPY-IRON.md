# IV iron ads: three ideas for a pre-launch test (Oct 14, 2026)

IV iron isn't live yet, so these ads sell **only the founding waitlist**: there's nothing to book yet, and no price is set. There are three ideas, each a different format so Meta treats them as separate creatives. The third also has the one AI video.

| Ad | Idea | Format | On the image |
|---|---|---|---|
| IR1 | Two routes | Engraved plate (sage on cream) | Two routes to your iron stores, and one skips the gut. |
| IR2 | Hidden deficiency | Lab-range graphic | Low iron doesn't always look like anemia. |
| IR3 | The clinic, the waitlist | People-free infusion-room photo + capsule | IV iron is coming to Barrie, and the founding waitlist is open. |
| IRV1 | IR3 in motion | 6.5 s AI video (Kling 3.0 push-in) + end card | Same line, then "Join the founding waitlist." |

```
python3 render.py --page iron   # renders out/r4/iron/IR1–IR3 _4x5 + _9x16, QA (safe zone + measured contrast)
```

Backgrounds:
- **IR1:** a Higgsfield engraving, style-matched to the IV iron page's engravings; the 9:16 is outpainted.
- **IR2:** rendered from `gen/r4/ir2_bg.html`, no AI.
- **IR3:** a people-free room generated from the real exam room. It's also IRV1's start frame.

IRV1 lives at `out/r4/iron/IRV1_9x16.mp4` and `IRV1_4x5.mp4`, with thumbnails. It's built from `gen/r4/video/`.

## Setup

**There's no live landing page yet.** `beoptimal.ca/iv-iron` returns the 404 page. So the test runs on a **Meta Instant Form**: the waitlist form opens inside Facebook and Instagram, and nothing on the website is needed. When the waitlist page ships, switch the destination to it.

| | IV iron (pre-launch) |
|---|---|
| Campaign objective | Leads → Instant Form |
| Audience | Adults 25–64, about 40 km around Barrie, broad (no interests) |
| Ads | IR1, IR2, IR3 and IRV1 in one ad set; placement asset customization (4:5 Feed, 9:16 Stories/Reels) |
| CTA button | Sign up |
| AI label | **On** for all four (AI-generated engraving, room and video) |
| URL parameters (only once a website destination exists) | `utm_source={{site_source_name}}&utm_medium=paid&utm_campaign={{campaign.id}}&utm_term={{adset.id}}&utm_content={{ad.id}}` |

**Instant Form ("Join the IV iron founding waitlist")**

1. **Intro:** IV iron is coming to Optimal in Barrie. Join the founding waitlist for first access, in signup order, and founding pricing. No referral needed.
2. **Questions:**
   - First name, email, phone number (prefilled).
   - One custom question: "Do you have private or workplace drug coverage?" (Yes / No / Not sure). The iron itself is a pharmacy prescription, so this sorts out likely buyers.
   - Don't ask health questions (ferritin, symptoms, diagnoses). Meta's lead-ad rules restrict them, and the NP covers this at assessment.
3. **Privacy policy:** https://www.beoptimal.ca/privacy
4. **Thank-you screen:** "You're on the list. We'll email you when booking opens. Questions? Call (437) 370-0291."

**Budget and reading the test:**
- Run $20–30 a day for 7 days and leave the ads alone.
- Judge on cost per waitlist signup and on the share of signups who answer "Yes" on drug coverage.
- Keep the winning idea, and replace the weakest with a new variation of the winner.
- Download the leads every few days. Founding access is in signup order.

## Copy

### IR1 · "Two routes to your iron stores, and one skips the gut."
**Primary text:** There are two routes to your iron stores. Pills are absorbed through the gut, a little at a time. An IV infusion skips the gut and refills iron stores directly, usually in one or two monitored visits. IV iron is coming to Optimal in Barrie: no referral needed, and we order your bloodwork first. Join the founding waitlist for first access and founding pricing.
**Headline:** Skip the gut: IV iron in Barrie · **Description:** Founding waitlist · No referral

### IR2 · "Low iron doesn't always look like anemia."
**Primary text:** Low iron doesn't always look like anemia. Hemoglobin can sit in range while iron stores, measured as ferritin, run low. IV iron is coming to Optimal in Barrie, led by a Nurse Practitioner who reviews your bloodwork before anything else. No referral needed. Join the founding waitlist for first access and founding pricing.
**Headline:** Iron stores, checked properly · **Description:** Founding waitlist · Barrie

### IR3 · "IV iron is coming to Barrie, and the founding waitlist is open."
**Primary text:** IV iron is coming to Optimal in Barrie. No referral needed: we order your bloodwork, a Nurse Practitioner assesses you first, and an NP is on site for every infusion. Join the founding waitlist for first access, in signup order, and founding pricing.
**Headline:** Founding waitlist now open · **Description:** First access in signup order

### IRV1 · "IV iron is coming to Barrie, and the founding waitlist is open." (video)
**Primary text:** IV iron is coming to Optimal in Barrie. No referral needed: we order your bloodwork, a Nurse Practitioner assesses you first, and an NP is on site for every infusion. Join the founding waitlist for first access and founding pricing.
**Headline:** Founding waitlist now open · **Description:** IV iron · Barrie

## Guardrails used

- **Waitlist only.** No booking language, because the service isn't live.
- **No price numbers.** The founding rate is set at launch. There's no "regular $595" either: a reference price for a service that has never sold at that price is a Competition Act risk.
- **No drug brand names** (the iron is a separate prescription). No feel-better timelines. No "1 in 4 women".
- **Third person only.** No "Exhausted by low iron?" or "you have…" phrasing (Meta's personal-attributes policy).
- **No provider comparisons** (CNO): no drip bars, no other clinics. **Pills vs IV is described neutrally**, since pills are the right first step for many people. The NP decides whether IV iron fits, after bloodwork.
- **AI label on.** Every visual is AI-generated: an engraving, an empty room and a video with no people.

// Static Meta ads, round 1 (Oct 12, 2026).
// Each ad renders twice: "post" = 1080x1350 feed, "story" = 1080x1920 Stories/Reels.
// Copy syntax: *word* = italic accent, [[word]] = hand-drawn ring.
// Facts come from the live landing pages (Oct 12, 2026):
//   menopause  https://www.beoptimal.ca/services/menopause-and-perimenopause-care
//   longevity  https://www.beoptimal.ca/membership
// Kept out on purpose: testimonials (CNO), comparisons with other clinics or GPs (CNO),
// "value" totals (Competition Act), "you have X" phrasing (Meta personal-attributes policy).

const CALL = "Book a free 15-min call";

window.ADS = [
  // ---------------- MENOPAUSE ----------------
  {
    id: "M1", svc: "meno", t: "symptoms", tag: "Perimenopause",
    eb: "It can start in your 40s",
    h: "Perimenopause is more than [[hot flashes]].",
    items: ["3 a.m. wake-ups", "Brain fog", "Night sweats", "Mood changes", "Joint aches", "Low energy", "Irregular periods", "Low libido", "Weight changes", "Vaginal dryness"],
    storyItems: 8,
    body: "Symptoms often begin years before periods stop. Our NP-led program starts with a full assessment and labs.",
    cta: CALL
  },
  {
    id: "M2", svc: "meno", t: "stat", tag: "Menopause care",
    eb: "Your first NP visit",
    num: "60", unit: "minutes",
    h: "to tell the whole story, with an NP who has the *time*.",
    body: "Then follow-ups at weeks 6 and 12, with the same NP. Comprehensive bloodwork is OHIP-covered.",
    cta: CALL
  },
  {
    id: "M3", svc: "meno", t: "price", tag: "Menopause care",
    eb: "Transparent fees",
    h: "Know the cost *before* you start.",
    rows: [
      { l: "Intro call", s: "15 minutes with our care coordinator", p: "Free" },
      { l: "Foundation Program", s: "Months 1–3 · labs, InBody, {60-min} NP intake, {2 follow-ups}", p: "$895", u: "+ HST" },
      { l: "Ongoing Care", s: "From month 4 · {3 NP visits a year}, prescriptions managed", p: "$795", u: "/ yr" }
    ],
    note: "Bloodwork is OHIP-covered. NP receipts may be claimable on extended health plans.",
    cta: CALL
  },
  {
    id: "M4", svc: "meno", t: "photo", tag: "Menopause care",
    img: "assets/B3w.jpg", pos: { post: "22% 50%", story: "21% 50%" }, at: "bottom", storyAt: "top", storyZoom: 1.26,
    eb: "Menopause &amp; perimenopause care",
    h: "No referral.|No family doctor *needed*.",
    body: "NP-led care for women 35+ at our clinic in Barrie. Appointments within days.",
    cta: CALL
  },
  {
    id: "M5", svc: "meno", t: "steps", tag: "Menopause care",
    eb: "How it works",
    h: "A clear plan, [[start]] to finish.",
    steps: [
      { n: "1", t: "Free 15-minute call", d: "With our care coordinator. No commitment." },
      { n: "2", t: "Foundation · months 1–3", d: "Labs, InBody scan, a 60-minute NP intake and two follow-ups." },
      { n: "3", t: "Ongoing care · month 4+", d: "The same NP, three visits a year, prescriptions managed." }
    ],
    cta: CALL
  },
  {
    id: "M6", svc: "meno", t: "photo", tag: "Perimenopause",
    img: "assets/B1v.jpg", pos: { post: "50% 62%", story: "50% 50%" }, at: "top",
    eb: "Perimenopause",
    h: "3 a.m. Wide awake.|*Again.*",
    body: "Night sweats and broken sleep are common in perimenopause. A 60-minute NP assessment is a good place to start.",
    cta: CALL
  },

  // ---------------- LONGEVITY MEMBERSHIP ----------------
  {
    id: "L1", svc: "long", t: "ledger", tag: "Longevity membership",
    eb: "Optimal membership · Barrie",
    h: "One price. *Everything* included.",
    items: ["Your own Nurse Practitioner", "Unlimited in-person &amp; virtual visits", "Annual 60-min longevity assessment", "Advanced biomarker panel", "InBody scan every 90 days", "Written 12-month health plan", "Care coordinator &amp; secure messaging"],
    storyItems: ["Your own Nurse Practitioner", "Unlimited in-person &amp; virtual visits", "Annual longevity assessment + labs", "InBody scan every 90 days", "Written 12-month health plan"],
    price: "$1,495", per: "/ year", chip: "HSA eligible",
    cta: CALL
  },
  {
    id: "L2", svc: "long", t: "venn", tag: "Longevity membership",
    eb: "Good to know",
    h: "Keep your family doctor.|Add a team with [[time]].",
    body: "Our NPs don’t bill OHIP, so there’s no outside-use penalty for you or your doctor.",
    cta: CALL
  },
  {
    id: "L3", svc: "long", t: "week", tag: "Longevity membership",
    eb: "Same or next-day visits",
    h: "Unwell on Monday? Seen by [[Tuesday]].",
    body: "Same or next-day appointments for time-sensitive concerns. Routine visits within a week, in person or virtual.",
    cta: CALL
  },
  {
    id: "L4", svc: "long", t: "inbody", tag: "Longevity membership",
    eb: "Included with membership",
    h: "See what’s working, *every 90 days*.",
    body: "A quarterly InBody scan tracks muscle, body fat and visceral fat between visits.",
    cta: CALL
  },
  {
    id: "L5", svc: "long", t: "plate", tag: "Longevity membership",
    eb: "Annual longevity assessment",
    h: "An hour with your NP. *Every year.*",
    body: "Advanced biomarkers, reviewed with you line by line, then a written plan for the next 12 months.",
    cta: CALL
  },
  {
    id: "L6", svc: "long", t: "photo", tag: "Longevity membership",
    img: "assets/A1v.jpg", pos: { post: "50% 58%", story: "50% 50%" }, at: "bottom",
    eb: "Private membership · $1,495 a year",
    h: "OHIP still covers your *labs*.",
    body: "Medically necessary labs, imaging and specialist visits ordered by your NP stay OHIP-covered.",
    cta: CALL
  }
];

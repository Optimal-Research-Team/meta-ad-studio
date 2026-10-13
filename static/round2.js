// Round 2 (Oct 12, 2026; Hormozi pass Oct 13): one sentence per image, each a hook with a concrete outcome. Logo + sentence only; Meta's own button carries the CTA.
// Photos are Higgsfield (gpt_image_2_5) generations in assets/r2/; in-clinic shots used real clinic photos as references.
// *word* = italic accent. tone: "light" text on dark photos, "dark" text on light photos.
// Singles render at 4:5 (feed) and 9:16 (stories/reels, outpainted from the same photo). Carousel cards render at 4:5.

window.R2 = [
  // ---------------- MENOPAUSE singles ----------------
  { id: "MB1", svc: "meno", img: "MB1", tone: "light", s: "Wide awake at 3 a.m., *again*." },
  { id: "MB2", svc: "meno", img: "MB2", tone: "dark",  s: "Brain fog can be *perimenopause*,|not just a busy life.", align: "center", fs: 78 },
  { id: "MB3", svc: "meno", img: "MB3", tone: "dark",  s: "Start menopause|care in Barrie|*within days*.", align: "right", w: 820, fs: 84 },
  { id: "MB4", svc: "meno", img: "MB4", tone: "dark",  s: "Hot flashes don’t wait,|and *neither should you*.", fs: 80 },
  { id: "MB5", svc: "meno", img: "MB5", tone: "light", s: "No referral, no family doctor, and you start *within days*.", box: true, fs: 72 },
  { id: "MB6", svc: "meno", img: "MB6", tone: "dark",  s: "Your first NP visit is a full *60 minutes*." },

  // ---------------- LONGEVITY singles ----------------
  { id: "LB1", svc: "long", img: "LB1", tone: "dark",  s: "Your own Nurse Practitioner in Barrie, with *{same or next-day}* visits.", align: "center", fs: 80 },
  { id: "LB2", svc: "long", img: "LB2", tone: "dark",  s: "Sick today,|seen tomorrow,|by an NP who *{knows you}*.", align: "right", w: 910, fs: 80 },
  { id: "LB3", svc: "long", img: "LB3", tone: "dark",  s: "See what’s working,|*every 90 days*." },
  { id: "LB4", svc: "long", img: "LB4", tone: "light", s: "Know exactly what to do for your health *this year*." },
  { id: "LB5", svc: "long", img: "LB5", tone: "dark",  s: "Your own Nurse Practitioner for about *$4 a day*.", align: "right", w: 700, veil: true, st: 470 },
  { id: "LB6", svc: "long", img: "LB6", tone: "dark",  s: "OHIP still covers your|*medically necessary* labs.", align: "center" },

  // ---------------- MENOPAUSE carousel (swipe order) ----------------
  { id: "MC1", svc: "meno-carousel", img: "MC1", tone: "dark",  s: "Menopause care in Barrie starts with a *free 15-minute call*.", card: 1 },
  { id: "MC2", svc: "meno-carousel", img: "LB6", tone: "dark",  s: "Your hormone lab panel is covered by *OHIP*.", card: 2, align: "center" },
  { id: "MC3", svc: "meno-carousel", img: "MB6", tone: "dark",  s: "Then a full hour with your *Nurse Practitioner*.", card: 3 },
  { id: "MC4", svc: "meno-carousel", img: "MC4", tone: "dark",  s: "You get a written plan and the *same NP* every visit.", card: 4 },
  { id: "MC5", svc: "meno-carousel", img: "WAIT", tone: "light", s: "No referral needed:|book your free call at *beoptimal.ca*.", card: 5, box: true },

  // ---------------- LONGEVITY carousel (swipe order) ----------------
  { id: "LC1", svc: "long-carousel", img: "RECEPTION", tone: "dark", s: "Here’s everything *$1,495 a year* gets you.", card: 1, w: 760, veil: true },
  { id: "LC2", svc: "long-carousel", img: "LC2", s: "Your own Nurse Practitioner, with *unlimited visits*.", card: 2, box: true, tone: "light" },
  { id: "LC3", svc: "long-carousel", img: "LB4", tone: "light", s: "A 60-minute assessment and a written plan, *every year*.", card: 3 },
  { id: "LC4", svc: "long-carousel", img: "LB3", tone: "dark",  s: "A body composition scan *every 90 days*.", card: 4 },
  { id: "LC5", svc: "long-carousel", img: "LB1", tone: "dark",  s: "Start with a *free 15-minute call*,|no commitment.", card: 5, align: "center" }
];

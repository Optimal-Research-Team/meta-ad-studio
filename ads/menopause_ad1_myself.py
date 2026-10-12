"""Menopause ad 1, "I don't feel like myself": Cheryl (care coordinator) seated in the lounge, medium close-up.

Source: iPhone 1080x1920 H.264, Display-P3, 59.94 fps, full range, 51.0 s, one take; mic on the LEFT channel only.
Speech 1.78-46.19 s, then an outtake ("Yeah, that one felt like a winner.") at 49 s that is never used.

Tight (~34 s): hook, intro, symptoms, "you don't need a diagnosis", the two-step start, CTA.
Full (~42 s): adds "after somebody has told them that it's just stress" and "Many women carry these alone
for over a year before they reach out."
"""
NAME = "MenopauseMyself"
SRC = "inbox/menopause-ad1.mov"
WORK = "work/menopause-ad1"
OUT = "out/menopause-ad1"

FIX = {
    4.25: "“I",                 # the caller's words, set as a quotation
    5.25: "myself.”",
    26.21: "You",
}

# name: (source start, source end, punch-in). A start equal to the previous end = zoom cut on continuous speech.
SEGS = {
    "hook": (1.65, 5.82, 1.00),       # The thing I hear most often on the phone, "I just don't feel like myself."
    "stress": (6.51, 10.36, 1.24),    # And usually this is after somebody has told them that it's just stress.
    "intro": (10.88, 14.81, 1.12),    # I'm Cheryl, I'm a care coordinator at the Optimal Clinic in Barrie.
    "fog": (15.56, 16.63, 1.00),      # Brain fog,          staccato punch-ins, one per symptom (continuous audio)
    "sleep": (16.63, 17.73, 1.10),    # broken sleep,
    "mood": (17.73, 18.91, 1.20),     # mood changes,
    "cycles": (18.91, 21.00, 1.00),   # cycles that have suddenly shifted.
    "alone": (21.55, 26.10, 1.12),    # Many women carry these alone for over a year before they reach out.
    "diag": (26.81, 28.80, 1.24),     # You don't need a diagnosis.
    "reach": (29.61, 30.65, 1.00),    # Reach out.
    "enough": (30.93, 33.42, 1.12),   # Feeling like something is off is enough.
    "step1": (34.60, 39.02, 1.00),    # We start with a free phone information session to make sure that we are a good fit,
    "step2": (39.23, 43.98, 1.12),    # followed by a free orientation, no cost, no commitment.
    "cta": (44.41, 46.80, 1.24),      # Let's see if this is the right program for you.
}
VARIANTS = {
    "Tight": ["hook", "intro", "fog", "sleep", "mood", "cycles", "diag", "reach", "enough", "step1", "step2", "cta"],
    "Full": ["hook", "stress", "intro", "fog", "sleep", "mood", "cycles", "alone", "diag", "reach", "enough",
             "step1", "step2", "cta"],
}

HOOK = dict(eyebrow="MENOPAUSE & PERIMENOPAUSE CARE",
            lines=[[("“I just don’t feel ", False), ("like myself.”", True)]],
            top=282, size=56, until=3.9)
KEEP = [("free", "orientation"), ("make", "sure"), ("most", "often"), ("followed", "by")]   # caption lines never split these
EMPH = ["myself", "stress", "Cheryl", "fog", "sleep", "mood", "cycles", "alone", "diagnosis", "enough", "free", "right"]
MUSIC = "brand/audio/bed_built_upon_a_path.wav"
TAGS = [  # chapter chips (top of frame): how it starts
    (["step1"], 1, "Free phone information session"),
    (["step2"], 2, "Free orientation, no commitment"),
]
END = dict(eyebrow="MENOPAUSE & PERIMENOPAUSE CARE", headline=["You deserve", "to be *heard.*"],
           sub=["Free 15-minute intro call.", "No obligation. We call you."],
           cta="Book a free intro call  →")
END_DUR = 3.2
THUMB_AT = 1.0
COVER = dict(lines=[[("\u201cI just don\u2019t feel", False)], [("like myself.", True), ("\u201d", False)]])    # Instagram cover headline (reel-cover style)
COVER_AT = 0.5    # source s: a clean frame before the first word, for the Instagram cover

# Organic Instagram: same edit, Tight only, 9:16 only. The end card swaps the (untappable) Book button for the
# keyword that triggers the Meta Business Suite auto-DM.  python3 studio.py ads/menopause_ad1_myself.py --channel=ig
CHANNELS = {
    "ig": dict(VARIANTS={"Tight": VARIANTS["Tight"]}, RATIOS=("9x16",),
               END=dict(END, sub=["Comment MENOPAUSE and we\u2019ll", "send you the details."],
                        cta="Comment MENOPAUSE", url="@beoptimal.ca  \u00b7  Barrie, ON")),
}

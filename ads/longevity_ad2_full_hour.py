"""Longevity ad 2, "A full hour": Cheryl (care coordinator) seated in the lounge, medium close-up.

Source: iPhone 1080x1920 H.264, Display-P3, 59.94 fps, full range, 45.7 s, one take; mic on the LEFT channel only.
Speech 3.25-41.77 s, then an outtake ("That one felt much better.") at 44.9 s that is never used.
Her hair reaches y~466 at 1x, so the hook is one compact line above it and punch-ins stay <= 1.24.

Compliance (see memory project_ad_review_oct12): "not everything that fits on a brochure" reads as an implied
comparison with other clinics (CNO), so the Tight cut drops it at the natural pause before "because"; Full keeps it.
She says "40-plus biomarkers across 10 health domains"; the ALE project defines the panel as 39 markers across
11 body systems, so the on-screen chip says "Comprehensive bloodwork" until the count is confirmed.
"""
NAME = "LongevityFullHour"
SRC = "inbox/longevity-ad2.mov"
WORK = "work/longevity-ad2"
OUT = "out/longevity-ad2"

# whisper word start (source s) -> caption text; None drops the word. Punctuation = phrase breaks.
FIX = {
    6.60: "health?",
    32.66: "brochure,",
}

# name: (source start, source end, punch-in). A start equal to the previous end = zoom cut on continuous speech.
SEGS = {
    "hook": (3.12, 7.05, 1.00),       # When is the last time anyone spent a full hour on your health?
    "intro": (7.66, 12.61, 1.12),     # Hi, I'm Cheryl. I am a care coordinator at the Optimal Clinic here in Barrie.
    "exam": (12.78, 16.35, 1.00),     # Every member gets an annual longevity exam every year,
    "hour": (16.35, 19.20, 1.14),     # a full hour with your nurse practitioner where we are   (zoom cut, no time cut)
    "labs": (19.62, 23.08, 1.00),     # looking at 40-plus biomarkers across 10 different health domains.
    "body": (23.35, 26.72, 1.14),     # We're doing a body composition scan and we're testing your grip strength.
    "clin": (27.33, 30.37, 1.00),     # We test what is clinically appropriate,
    "why": (33.30, 37.55, 1.10),      # because results only matter if we can turn them into action.
    "why_full": (30.83, 37.55, 1.10), # not everything that fits on a brochure, because results ... action.
    "cta": (38.52, 42.40, 1.24),      # Book your free phone information session with us now.
}
VARIANTS = {
    "Tight": ["hook", "intro", "exam", "hour", "labs", "body", "clin", "why", "cta"],
    "Full": ["hook", "intro", "exam", "hour", "labs", "body", "clin", "why_full", "cta"],
}

HOOK = dict(eyebrow="OPTIMAL LONGEVITY MEMBERSHIP",
            lines=[[("A full hour. ", True), ("Every year.", False)]],
            top=282, size=62, until=3.5)
EMPH = ["hour", "Cheryl", "40-plus", "strength", "clinically", "action", "free"]
MUSIC = "brand/audio/bed_built_upon_a_path.wav"
TAGS = [  # chapter chips (top of frame): what is inside the annual exam
    (["hour"], 1, "A full hour with your nurse practitioner"),
    (["labs"], 2, "Comprehensive bloodwork"),
    (["body"], 3, "Body composition + grip strength"),
]
END_DUR = 3.2
THUMB_AT = 1.0
COVER = dict(lines=[[("A full hour.", False)], [("Every year.", True)]])    # Instagram cover headline (reel-cover style)
COVER_AT = 2.4    # source s: a clean frame before the first word, for the Instagram cover

# Organic Instagram: same edit, Tight only, 9:16 only. The end card swaps the (untappable) Book button for the
# keyword that triggers the Meta Business Suite auto-DM.  python3 studio.py ads/longevity_ad2_full_hour.py --channel=ig
CHANNELS = {
    "ig": dict(VARIANTS={"Tight": VARIANTS["Tight"]}, RATIOS=("9x16",),
               END=dict(sub=["Comment LONGEVITY and we\u2019ll", "send you the details."],
                        cta="Comment LONGEVITY", url="@beoptimal.ca  \u00b7  Barrie, ON")),
}

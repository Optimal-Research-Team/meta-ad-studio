"""Longevity membership core ad v2: Cheryl (care coordinator) walk-and-talk, lounge -> reception.

Source: iPhone 1080x1920 H.264, Display-P3, 59.94 fps, full range, 49.5 s, one continuous take.
Speech 3.06-46.90 s; silences from silencedetect (-42 dB); timings below are source seconds.
"""
NAME = "LongevityCore"
SRC = "inbox/longevity-core-v2.mov"
WORK = "work/longevity-core-v2"
OUT = "out/longevity-core-v2"

# whisper word start (source s) -> caption text; None drops the word. Punctuation = phrase breaks.
FIX = {
    6.40: "Barrie,", 9.62: "simple:", 14.00: "lives.",
    18.56: "One:", 20.42: "year,",
    22.38: None,                      # "access to [in] a 60-minute" -> stumble dropped from captions
    27.88: "Two:", 31.00: "thorough,", 32.30: "unrushed", 32.78: "appointments.",
    34.28: "three:", 37.66: "times", 44.36: "now,",
}

# name: (source start, source end, punch-in). Handles ~0.13 s around speech; zoom alternates at every cut.
SEGS = {
    "intro": (2.90, 7.22, 1.00),        # Hi, I'm Cheryl ... Optimal Clinic in Barrie
    "intro_full": (2.90, 14.80, 1.00),  # ... + our mission ... live longer and healthier lives
    "three": (15.55, 17.98, 1.10),      # Three important things you should know about us
    "one": (18.72, 19.45, 1.25),
    "p1": (20.08, 27.80, 1.00),         # 60-min annual longevity assessment + bloodwork
    "p2": (28.40, 33.66, 1.12),         # Two: thorough, unrushed appointments
    "and3": (33.96, 35.10, 1.25),
    "p3": (35.58, 41.10, 1.00),         # faster appointment times
    "cta": (42.50, 47.40, 1.15),        # Book a free information call with me now ...
}
VARIANTS = {
    "Tight": ["intro", "three", "one", "p1", "p2", "and3", "p3", "cta"],
    "Full": ["intro_full", "three", "one", "p1", "p2", "and3", "p3", "cta"],
}

HOOK = dict(eyebrow="OPTIMAL LONGEVITY MEMBERSHIP",
            lines=[[("3 things to know", False)], [("before you book.", True)]],
            top=290, until=3.4)
# words set in Castoro Italic inside the captions (the design system's emphasis device) — one per phrase at most
EMPH = ["Cheryl", "60-minute", "unrushed", "faster", "free", "longer", "healthier"]
MUSIC = "brand/audio/bed_built_upon_a_path.wav"   # Fionnlagh - Built Upon a Path, steady section (brand film bed)
TAGS = [  # chapter chips (top of frame) over these segments
    (["one", "p1"], 1, "60-min annual longevity assessment"),
    (["p2"], 2, "Thorough, unrushed appointments"),
    (["and3", "p3"], 3, "Faster appointment times"),
]
END_DUR = 3.2
THUMB_AT = 1.0

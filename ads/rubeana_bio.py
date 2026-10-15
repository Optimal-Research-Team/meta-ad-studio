"""Rubeana bio (social only): Rubeana Deol, NP, Clinical Director, introduces herself. Instagram/Facebook reel, 9:16.

Source: iPhone 1080x1920 H.264, Display-P3, 59.94 fps, full range, 35.9 s, one take; mic on the LEFT channel only.
Cut: the 2 s silent start, "A little bit about me", the stumble "a little… my background includes teaching" (the
next line, "I've taught at U of T as well as Seneca College", carries it), and the false start "We often see".
She sits low in the frame, so the captions go below her chin (CAP_Y) and the hook can take two lines.
"""
NAME = "RubeanaBio"
SRC = "inbox/rubeana-bio.mov"
WORK = "work/rubeana-bio"
OUT = "out/rubeana-bio"
RATIOS = ("9x16",)
KEEP = [("as", "well"), ("well", "as"), ("clinical", "director")]
CAP_Y = 1330

FIX = {
    3.40: "Rubeana", 5.90: "Optimal.", 10.04: "medicine.", 14.58: "well-informed.",
    18.32: "U of T", 20.06: "College.", 24.34: "health.", 25.38: "nutrition,", 26.04: "sleep,",
    29.64: "diseases.", 31.06: "Book", 33.08: "health.",
    30.02: None, 30.22: None, 30.48: None,   # false start "We often see" (cut from the audio too)
}

SEGS = {
    "intro": (2.19, 6.40, 1.00),      # Hi, my name is Rubeana and I'm the new clinical director here at Optimal.
    "focus": (7.99, 10.35, 1.10),     # My focus is always focused on prevention medicine.
    "love": (10.92, 15.30, 1.00),     # I love when patients take a proactive approach in their health and they come to me being well-informed.
    "taught": (17.64, 20.48, 1.12),   # I've taught at U of T as well as Seneca College.
    "engage": (20.50, 24.68, 1.00),   # I often engage my patients in looking at the core elements to their health.
    "inc1": (24.72, 26.80, 1.12),     # This includes nutrition, sleep,
    "inc2": (27.12, 30.08, 1.00),     # as well as a focus on prevention for these chronic diseases.
    "cta": (30.93, 33.80, 1.12),      # Book in with me to talk more about your health.
}
VARIANTS = {"Reel": ["intro", "focus", "love", "taught", "engage", "inc1", "inc2", "cta"]}

HOOK = dict(eyebrow="MEET YOUR CARE TEAM",
            lines=[[("Rubeana Deol, NP", False)], [("Clinical Director", True)]],
            top=290, size=66, until=4.0)
EMPH = ["Rubeana", "prevention", "proactive", "core", "nutrition"]
MUSIC = "brand/audio/bed_built_upon_a_path.wav"
TAGS = [
    (["focus", "love"], 1, "Prevention-first care"),
    (["taught"], 2, "Taught at U of T and Seneca College"),
    (["inc1", "inc2"], 3, "Nutrition, sleep and prevention"),
]
END = dict(eyebrow="MEET YOUR CARE TEAM", headline=["Meet", "*Rubeana.*"],
           sub=["Rubeana Deol, NP, Clinical Director.", "Book a free intro call."],
           cta="Link in bio", url="@beoptimal.ca  ·  Barrie, ON")
END_DUR = 3.2
THUMB_AT = 1.0
COVER = dict(lines=[[("Meet Rubeana,", False)], [("Clinical Director.", True)]])
COVER_AT = 1.0

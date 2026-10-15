"""Longevity ad 3, "Optimize your health" (LV3): Rubeana Deol, NP, close-up against the green tile wall.

Source: iPhone 1080x1920 H.264, Display-P3, 59.94 fps, full range, 30.1 s, one take; mic on the LEFT channel only.
"Are" (0.8 s) is followed by a 1.5 s pause before "you looking…", which is cut. Very close framing (face ~35% of
the width), so the punch-ins stop at 1.12 and the hook is one compact line above her head.
"""
NAME = "LongevityOptimize"
SRC = "inbox/health-optimizer.mov"
WORK = "work/health-optimizer"
OUT = "out/health-optimizer"

FIX = {}
FLOW = [("are", "hook")]                 # only a pause was cut there: "Are you looking…" reads as one phrase
KEEP = [("nurse", "practitioner-led")]

SEGS = {
    "are": (0.63, 1.40, 1.00),        # Are
    "hook": (2.66, 4.79, 1.10),       # you looking to optimize your health?
    "intro": (5.19, 8.29, 1.00),      # Here at Optimal, we're a nurse practitioner-led clinic.
    "hour": (8.60, 12.11, 1.12),      # You will receive a one-hour annual physical appointment
    "listen": (12.20, 17.80, 1.00),   # in which the nurse practitioner listens, evaluates, and also completes a detailed assessment.
    "labs": (18.12, 20.61, 1.12),     # In this assessment, we will then order labs.
    "bio": (20.72, 25.79, 1.00),      # These labs will allow us to look at the biomarkers that are necessary to evaluate your overall health.
    "cta": (26.12, 28.10, 1.12),      # Book in for an info call.
}
VARIANTS = {"Tight": ["are", "hook", "intro", "hour", "listen", "labs", "bio", "cta"]}

HOOK = dict(eyebrow="OPTIMAL LONGEVITY MEMBERSHIP",
            lines=[[("An hour", True), (" with an NP who listens.", False)]],
            top=282, size=54, until=3.6)
EMPH = ["optimize", "one-hour", "listens", "biomarkers", "info"]
MUSIC = "brand/audio/bed_built_upon_a_path.wav"
TAGS = [
    (["hour"], 1, "A one-hour annual physical"),
    (["listen"], 2, "An NP who listens and assesses"),
    (["labs", "bio"], 3, "Labs for your key biomarkers"),
]
END_DUR = 3.2
THUMB_AT = 1.0
COVER = dict(lines=[[("An hour with an NP", False)], [("who listens.", True)]])
COVER_AT = 0.3

CHANNELS = {
    "ig": dict(VARIANTS={"Tight": VARIANTS["Tight"]}, RATIOS=("9x16",),
               END=dict(sub=["Book a free intro call to ask", "about the Longevity Membership."],
                        cta="Link in bio", url="@beoptimal.ca  ·  Barrie, ON")),
}

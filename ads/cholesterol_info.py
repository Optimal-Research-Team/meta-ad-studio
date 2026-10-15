"""Cholesterol explainer (social only): HDL/LDL → Lp(a) and ApoB → treatment. Instagram reel, 9:16, ~72 s.

Source: iPhone 1080x1920 H.264, Display-P3, 59.94 fps, full range, 133.1 s, one take; mic on the LEFT channel only.
Cut: 50.0–97.0 s, where Peter interrupts (statins, PCSK9, "it's gonna auto play") and she restarts.
Medical accuracy trims (Reel): the Lp(a) line "looks at whether high LDL is familial or due to your lifestyle"
(Lp(a) is an independent, genetically set marker) and "injections… given once every three months" (inclisiran
is every 6 months after the first two doses; other injectables are every 2–4 weeks). Verbatim keeps both.
Engraving cards (brand/engravings, from the IG ApoB carousel) sit above her head; captions sit below her chin.
"""
NAME = "CholesterolInfo"
SRC = "inbox/cholesterol-info.mov"
WORK = "work/cholesterol-info"
OUT = "out/cholesterol-info"
RATIOS = ("9x16",)
CAP_Y = 1330

FIX = {
    18.67: "ApoB.", 35.21: "at", 36.11: "ApoB.", 46.79: "ApoB", 49.25: "ApoB",
    103.64: "as", 103.76: "nurse", 103.98: "practitioners", 123.44: "ezetimibe", 124.78: "injections.",
}
KEEP = [("lipoprotein", "a"), ("cardiovascular", "health"), ("cardiovascular", "risk"), ("nurse", "practitioners"),
        ("plaque", "buildup"), ("treatment", "options")]

SEGS = {
    "old": (1.89, 9.40, 1.00),        # So previously … HDL, the good cholesterol, LDL, the bad cholesterol.
    "markers": (9.40, 14.50, 1.10),   # And look at specifically these two markers … cardiovascular health.
    "newtests": (14.50, 19.42, 1.00), # We now have two new tests, one being lipoprotein A and the second being ApoB.
    "lpa": (19.42, 21.78, 1.12),      # Lipoprotein A is a genetic marker.
    "lpa_full": (19.42, 32.85, 1.12), # … + "This marker specifically looks at … or is it really due to your lifestyle?"
    "lifestyle": (32.96, 36.88, 1.00),# When we look at your lifestyle, we're gonna look more in detail at something like the ApoB.
    "apob": (36.88, 44.85, 1.12),     # ApoB is a direct marker of the plaque buildup … cardiovascular risk.
    "optimal": (44.85, 50.05, 1.00),  # Here at Optimal, we will look at the ApoB and we're gonna treat specifically that ApoB level.
    "ask": (97.05, 101.18, 1.12),     # So you might ask me, what are some treatment options? Well, the first treatment should always be lifestyle.
    "diet": (101.18, 107.75, 1.00),   # So your diet and exercise is the first thing that us as nurse practitioners will assess …
    "omega": (107.75, 111.95, 1.12),  # After this, we have various options. A supplement might include an omega-3.
    "meds": (111.95, 119.05, 1.00),   # The other options are then looking at medications and pharmaceuticals …
    "statins": (119.05, 125.36, 1.12),# We've all heard of statins … We can also use ezetimibe or even injections.
    "statins_full": (119.05, 127.05, 1.12),  # … + "that are given once every three months."
    "close": (127.10, 130.95, 1.00),  # There are many options that we can utilize to help guide your health.
}
VARIANTS = {
    "Reel": ["old", "markers", "newtests", "lpa", "lifestyle", "apob", "optimal", "ask", "diet", "omega", "meds",
             "statins", "close"],
    "Verbatim": ["old", "markers", "newtests", "lpa_full", "lifestyle", "apob", "optimal", "ask", "diet", "omega",
                 "meds", "statins_full", "close"],
}

HOOK = dict(eyebrow="CHOLESTEROL, EXPLAINED", lines=[[("Beyond ", False), ("HDL and LDL.", True)]],
            top=282, size=64, until=3.9)
EMPH = ["HDL", "LDL", "genetic", "plaque", "Optimal", "lifestyle", "omega-3", "statins", "ezetimibe"]
MUSIC = "brand/audio/bed_built_upon_a_path.wav"
# engraving cards, timed in SOURCE seconds (mapped through the cuts)
CARDS = [
    dict(at=(6.30, 9.30), img="apob-particles-cream.png", eyebrow="THE OLD STANDARD",
         lines=[[("HDL ", False), ("&", True), (" LDL", False)], [("Good vs bad cholesterol", False)]]),
    dict(at=(14.90, 21.70), img="plate-heart-cream.png", eyebrow="TWO NEWER TESTS",
         lines=[[("Lp(a) ", False), ("and", True), (" ApoB", False)], [("Sharper reads on heart risk", False)]]),
    dict(at=(37.20, 44.60), img="apob-plaque-cream.png", eyebrow="APOB",
         lines=[[("Particles build ", False), ("plaque.", True)], [("ApoB counts them.", False)]]),
    dict(at=(45.00, 49.95), img="apob-particles-cream.png", eyebrow="AT OPTIMAL",
         lines=[[("We test ", False), ("and treat", True)], [("your ApoB.", False)]]),
]
TAGS = [
    (["ask", "diet"], 1, "Lifestyle first: diet and exercise"),
    (["omega"], 2, "Supplements, like omega-3"),
    (["meds", "statins", "statins_full"], 3, "Medications, when needed"),
]
END = dict(eyebrow="OPTIMAL LONGEVITY MEMBERSHIP", headline=["Know your", "*ApoB.*"],
           sub=["ApoB and Lp(a) are part of", "our longevity bloodwork."],
           cta="Link in bio", url="@beoptimal.ca  ·  Barrie, ON")
END_DUR = 3.2
THUMB_AT = 1.0
COVER = dict(lines=[[("Beyond", False)], [("HDL and LDL.", True)]])
COVER_AT = 1.0

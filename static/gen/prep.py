"""Turn Higgsfield downloads in gen/ into ad-ready backgrounds in assets/r2/ (1080x1350 and 1080x1920 JPGs)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "r2")
PH = os.path.expanduser("~/Downloads/Optimal Clinic/Marketing & Sales/Photography & Images/Optimal_Clinic_Landscape_and_Portrait_Set")
SRC45 = {"MB1": "p00", "MB2": "p01", "MB3": "p02", "MB4": "p03", "MB5": "p04", "MB6": "p05", "MC1": "p06",
         "LB6": "p07", "MC4": "p08", "LB1": "p09", "LB2": "p10", "LB3": "p11", "LB4": "p12", "LB5": "p13", "LC2": "p14"}
EXTRA45 = {"WAIT": os.path.join(HERE, "..", "assets", "A1v.jpg"), "RECEPTION": os.path.join(PH, "reception_wide_portrait_4x5.jpg")}

def cover(im, w, h, ay=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))

for k, p in SRC45.items():
    cover(Image.open(os.path.join(HERE, p + ".png")).convert("RGB"), 1080, 1350).save(os.path.join(OUT, f"{k}_4x5.jpg"), quality=92, subsampling=0)
for k, p in EXTRA45.items():
    cover(Image.open(p).convert("RGB"), 1080, 1350, 0.35).save(os.path.join(OUT, f"{k}_4x5.jpg"), quality=92, subsampling=0)
for k in SRC45:
    f = os.path.join(HERE, f"{k}_9x16.png")
    if os.path.exists(f):
        cover(Image.open(f).convert("RGB"), 1080, 1920).save(os.path.join(OUT, f"{k}_9x16.jpg"), quality=92, subsampling=0)
print(sorted(os.listdir(OUT)))

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

# Retouch (output coordinates): remove a sneaker swoosh in LB5 by cloning nearby black mesh with a
# feathered ellipse, and mute the tongue label. Third-party logos don't belong in our ads.
RETOUCH = {
    ("LB5", "4x5"):  [("clone", (360, 1203, 394, 1239), 36, 4), ("mute", (400, 1164, 422, 1180))],
    ("LB5", "9x16"): [("patch", "gen/LB5_9x16_shoe.png", (330, 1370))],   # Higgsfield inpaint of the shoe crop
}


def retouch(im, ops):
    from PIL import ImageDraw, ImageFilter
    for op in ops:
        if op[0] == "clone":
            (x0, y0, x1, y1), dx, dy = op[1], op[2], op[3]
            patch = im.crop((x0 + dx, y0 + dy, x1 + dx, y1 + dy))
            m = Image.new("L", patch.size, 0)
            ImageDraw.Draw(m).ellipse((2, 2, patch.width - 3, patch.height - 3), fill=255)
            im.paste(patch, (x0, y0), m.filter(ImageFilter.GaussianBlur(3)))
        elif op[0] == "patch":   # paste a pre-made fix (same size as the crop it came from), feathered
            fix = Image.open(os.path.join(HERE, "..", op[1])).convert("RGB")
            m = Image.new("L", fix.size, 0)
            ImageDraw.Draw(m).rectangle((24, 24, fix.width - 25, fix.height - 25), fill=255)
            im.paste(fix, op[2], m.filter(ImageFilter.GaussianBlur(12)))
        elif op[0] == "fill":   # paint the area with the sampled mesh colour plus matching grain
            import numpy as np
            box, src = op[1], op[2]
            sample = np.asarray(im.crop(src), dtype=np.float32).reshape(-1, 3)
            w, h = box[2] - box[0], box[3] - box[1]
            rng = np.random.default_rng(7)
            tex = np.median(sample, 0) + rng.normal(0, sample.std(0).mean() * .8, (h, w, 1))
            patch = Image.fromarray(np.clip(tex, 0, 255).astype("uint8"), "RGB").filter(ImageFilter.GaussianBlur(.6))
            m = Image.new("L", (w, h), 0)
            ImageDraw.Draw(m).ellipse((3, 3, w - 4, h - 4), fill=255)
            im.paste(patch, box[:2], m.filter(ImageFilter.GaussianBlur(4)))
        else:   # mute: pull the area toward the dark mesh around it
            box = op[1]
            area = im.crop(box)
            dark = Image.new("RGB", area.size, tuple(int(v) for v in sorted(area.getdata(), key=sum)[len(area.getdata()) // 6]))
            m = Image.new("L", area.size, 0)
            from PIL import ImageDraw as D
            D.Draw(m).ellipse((1, 1, area.width - 2, area.height - 2), fill=200)
            im.paste(dark, box[:2], m.filter(ImageFilter.GaussianBlur(2)))
    return im


for k, p in SRC45.items():
    im = cover(Image.open(os.path.join(HERE, p + ".png")).convert("RGB"), 1080, 1350)
    retouch(im, RETOUCH.get((k, "4x5"), [])).save(os.path.join(OUT, f"{k}_4x5.jpg"), quality=92, subsampling=0)
for k, p in EXTRA45.items():
    cover(Image.open(p).convert("RGB"), 1080, 1350, 0.35).save(os.path.join(OUT, f"{k}_4x5.jpg"), quality=92, subsampling=0)
for k in SRC45:
    f = os.path.join(HERE, f"{k}_9x16.png")
    if os.path.exists(f):
        im = cover(Image.open(f).convert("RGB"), 1080, 1920)
        retouch(im, RETOUCH.get((k, "9x16"), [])).save(os.path.join(OUT, f"{k}_9x16.jpg"), quality=92, subsampling=0)
print(sorted(os.listdir(OUT)))

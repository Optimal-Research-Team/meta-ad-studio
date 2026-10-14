"""Round 3 backgrounds: Ad Lab AI concepts (optimal-ad-lab/creative/concepts/raw) -> assets/r3/<ID>_4x5.jpg / _9x16.jpg."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "optimal-ad-lab", "creative", "concepts", "raw")
OUT = os.path.join(HERE, "..", "assets", "r3")
os.makedirs(OUT, exist_ok=True)


def cover(im, w, h, ay=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


# 9:16 only: push the art down (px) where the sentence would touch it; the top band is mirrored paper.
SHIFT9 = {"LA2": 120}


def shift_down(im, n):
    w, h = im.size
    out = Image.new("RGB", (w, h))
    out.paste(im.crop((0, 0, w, h - n)), (0, n))
    out.paste(im.crop((0, 0, w, n)).transpose(Image.FLIP_TOP_BOTTOM), (0, 0))
    return out


for k in ("MA1", "MA2", "LA1", "LA2"):
    cover(Image.open(os.path.join(SRC, f"{k}.png")).convert("RGB"), 1080, 1350).save(os.path.join(OUT, f"{k}_4x5.jpg"), quality=92, subsampling=0)
    s9 = os.path.join(SRC, f"{k}_9x16.png")
    if os.path.exists(s9):
        im9 = cover(Image.open(s9).convert("RGB"), 1080, 1920)
        (shift_down(im9, SHIFT9[k]) if k in SHIFT9 else im9).save(os.path.join(OUT, f"{k}_9x16.jpg"), quality=92, subsampling=0)
print(sorted(os.listdir(OUT)))

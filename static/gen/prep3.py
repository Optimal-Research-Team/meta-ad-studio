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


for k in ("MA1", "MA2", "LA1", "LA2"):
    cover(Image.open(os.path.join(SRC, f"{k}.png")).convert("RGB"), 1080, 1350).save(os.path.join(OUT, f"{k}_4x5.jpg"), quality=92, subsampling=0)
    s9 = os.path.join(SRC, f"{k}_9x16.png")
    if os.path.exists(s9):
        cover(Image.open(s9).convert("RGB"), 1080, 1920).save(os.path.join(OUT, f"{k}_9x16.jpg"), quality=92, subsampling=0)
print(sorted(os.listdir(OUT)))

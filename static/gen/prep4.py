# Round 4 (IV iron, Oct 14, 2026): rebuilds assets/r4 from the Higgsfield downloads in gen/r4.
#   IR1  engraving   gen/r4/IR1_raw.png (gpt_image_2_5) + IR1_9x16_raw.png (outpaint 1792x3184)
#   IR2  lab ranges  rendered from gen/r4/ir2_bg.html (no AI)
#   IR3  room        gen/r4/IR3_raw.png (9:16 generation; 4:5 is cropped from it). Also IRV1's start frame.
# Then: python3 render.py --page iron   and   sh gen/r4/video/build.sh
import asyncio, os
from PIL import Image
from playwright.async_api import async_playwright

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def cover(im, w, h, ay=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))

async def ir2():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1200, "height": 2000})
        await pg.goto("file://" + os.path.abspath("gen/r4/ir2_bg.html")); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        for el in await pg.query_selector_all(".f"):
            await el.screenshot(path=f"gen/r4/{await el.get_attribute('data-out')}.png")
        await b.close()

asyncio.run(ir2())
os.makedirs("assets/r4", exist_ok=True)
for s in ("4x5", "9x16"):
    Image.open(f"gen/r4/IR2_{s}.png").convert("RGB").save(f"assets/r4/IR2_{s}.jpg", quality=93, subsampling=0)
r = Image.open("gen/r4/IR3_raw.png").convert("RGB")
cover(r, 1080, 1920).save("assets/r4/IR3_9x16.jpg", quality=92, subsampling=0)
cover(r, 1080, 1350, 0.62).save("assets/r4/IR3_4x5.jpg", quality=92, subsampling=0)
cover(Image.open("gen/r4/IR1_raw.png").convert("RGB"), 1080, 1350).save("assets/r4/IR1_4x5.jpg", quality=92, subsampling=0)
cover(Image.open("gen/r4/IR1_9x16_raw.png").convert("RGB"), 1080, 1920).save("assets/r4/IR1_9x16.jpg", quality=92, subsampling=0)
print("assets/r4 rebuilt")

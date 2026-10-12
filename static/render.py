"""Render the static Meta ads in content.js to PNG, then QA them.

python3 render.py                   # every round-1 ad (ads.html)
python3 render.py M1 L3             # only these
python3 render.py --page round2     # round 2: one sentence per image (round2.html)

Writes out/<meno|long>/<ID>_4x5.png (1080x1350, feed) and <ID>_9x16.png (1080x1920, Stories/Reels),
plus out/_sheet.jpg. QA fails loudly if text spills out of a frame or, on 9:16, out of the
Reels safe zone (top 269px / bottom 672px / sides 65px).
"""
import asyncio, os, sys
from PIL import Image
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TOP, BOTTOM, SIDE = 269, 672, 65

QA_JS = """(f) => {
  const fr = f.getBoundingClientRect();
  const story = f.classList.contains('story');
  const H = fr.height, issues = [];
  const sel = 'h2,h4,p,li,.cta,.addr,.eyebrow,.mark,.tag,.chip,.pill,.amt,.stat,.unit,.ev,.d,.lab';
  for (const el of f.querySelectorAll(sel)) {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const top = r.top - fr.top, bot = r.bottom - fr.top, l = r.left - fr.left, rt = r.right - fr.left;
    const name = el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : '');
    if (bot > H - 40 || top < 40 || l < 40 || rt > fr.width - 40) issues.push(`${name} outside frame (${Math.round(top)}-${Math.round(bot)})`);
    if (story && (top < %d || bot > H - %d || l < %d || rt > fr.width - %d)) issues.push(`${name} outside safe zone (${Math.round(top)}-${Math.round(bot)})`);
  }
  const c = f.querySelector('.content');
  if (c && c.scrollHeight > c.clientHeight + 1) issues.push(`content overflows by ${c.scrollHeight - c.clientHeight}px`);
  return issues;
}""" % (TOP, BOTTOM, SIDE, SIDE)


async def main(only, page="ads"):
    q = ("?only=" + ",".join(only)) if only else ""
    problems = []
    shots = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 2000}, device_scale_factor=1)
        await pg.goto("file://" + os.path.join(HERE, page + ".html") + q)
        await pg.evaluate("""async () => {
            await document.fonts.ready;
            await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
        }""")
        await pg.wait_for_timeout(400)
        for el in await pg.query_selector_all(".frame"):
            out = await el.get_attribute("data-out")
            path = os.path.join(OUT, out + ".png")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            await el.scroll_into_view_if_needed()
            await el.screenshot(path=path)
            issues = await pg.evaluate(QA_JS, el)
            for i in issues:
                problems.append(f"{out}: {i}")
            shots.append(path)
            print("ok" if not issues else "!!", out)
        await b.close()
    sheet(shots, os.path.join(OUT, "_sheet.jpg" if page == "ads" else f"_sheet_{page}.jpg"))
    if problems:
        print("\nQA problems:")
        print("\n".join("  " + x for x in problems))
        sys.exit(1)
    print("\nQA clean:", len(shots), "frames")


def sheet(paths, dest, w=360):
    """Contact sheet: each ad's 4:5 and 9:16 side by side, with the Reels safe zone drawn on the 9:16."""
    from PIL import ImageDraw
    pairs = {}
    for pth in paths:
        k = os.path.basename(pth).split("_")[0]
        pairs.setdefault(k, {})["story" if "9x16" in pth else "post"] = pth
    tiles = []
    for k in sorted(pairs, key=lambda s: (s[0] != "M", s)):
        row = []
        for kind in ("post", "story"):
            if kind not in pairs[k]:
                continue
            im = Image.open(pairs[k][kind]).convert("RGB")
            s = w / im.width
            t = im.resize((w, int(im.height * s)))
            if kind == "story":
                d = ImageDraw.Draw(t, "RGBA")
                d.rectangle([0, 0, w, TOP * s], fill=(255, 0, 80, 40))
                d.rectangle([0, t.height - BOTTOM * s, w, t.height], fill=(255, 0, 80, 40))
            row.append(t)
        tiles.append((k, row))
    cols = 4
    cw = 2 * w + 16
    ch = int(1920 * w / 1080) + 30
    rows = (len(tiles) + cols - 1) // cols
    S = Image.new("RGB", (cols * (cw + 30), rows * ch), "white")
    d = ImageDraw.Draw(S)
    for i, (k, row) in enumerate(tiles):
        x0, y0 = (i % cols) * (cw + 30), (i // cols) * ch
        x = x0
        for t in row:
            S.paste(t, (x, y0))
            x += t.width + 16
        d.text((x0 + 4, y0 + ch - 24), k, fill="black")
    S.save(dest, quality=85)


if __name__ == "__main__":
    args = sys.argv[1:]
    page = "ads"
    if args[:1] == ["--page"]:
        page, args = args[1], args[2:]
    asyncio.run(main(args, page))

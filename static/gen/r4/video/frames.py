# IRV1 stills: the IR3 capsule as a transparent overlay (ov_*.png) and the end card (end_*.png).
import asyncio, os
from playwright.async_api import async_playwright

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))  # static/

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1200, "height": 2000})
        await pg.goto("file://" + os.path.abspath("iron.html") + "?only=IR3"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        await pg.add_style_tag(content=".bg{display:none!important} .frame{background:transparent!important} html,body{background:transparent!important}")
        for el in await pg.query_selector_all(".frame"):
            out = await el.get_attribute("data-out")
            await el.screenshot(path=f"gen/r4/video/ov_{out.split('_')[-1]}.png", omit_background=True)
        await pg.goto("file://" + os.path.abspath("gen/r4/endcard.html")); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        for el in await pg.query_selector_all(".card"):
            await el.screenshot(path=f"gen/r4/video/{await el.get_attribute('data-out')}.png")
        await b.close()

asyncio.run(main())

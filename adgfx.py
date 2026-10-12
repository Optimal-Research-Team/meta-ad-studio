"""Optimal ad graphics for talking-head Meta ads (9:16 master at 1080x1920; 4:5 is cropped from it).

System (Optimal Health Design System tokens, see brand/gfxlib.py):
  glass      frosted panel re-sampled from the live frame every frame: blur 26, forest-black tint, cream hairline
  captions   one line, Public Sans 600 @ 62px, typographic apostrophes; spoken words brighten as they are said
             (upcoming words sit at 50%), emphasis words switch to Castoro Italic (the brand's emphasis device);
             the capsule eases its width between phrases instead of jumping
  chapter    numbered glass chip at the top (structure up top, speech at the bottom)
  hook       glass panel with tracked-caps eyebrow + Castoro headline; on screen from frame 0
  end card   cream canvas, staggered reveal: logo, headline, offer, pill CTA, URL
Safe geometry: overlays live in y 290..1248 (Reels keeps the top 14% / bottom 35% clear).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand"))
from gfxlib import (BODY, CAPSULE, CREAM, FOREST, castoro, draw_run, draw_runs, logo, pill,  # noqa: E402
                    public, run_width, runs_width, serif_runs, tracked_caps)

W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 269, 1248
CAP_Y = 1160
CHIP_Y = 336
BLUR = 26
TINT = 150
CAP_SIZE, EMPH_SIZE = 62, 70        # Castoro italic runs ~12% smaller on the x-height
MAX_CAP_PX = 840
DIM = 0.50                          # upcoming words
CAP_TINT = 172                      # captions sit over bright walls: denser glass than the panels


def ease_out(u):
    u = min(max(u, 0.0), 1.0)
    return 1 - (1 - u) ** 3


def ease_in_out(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def fade(img, a):
    if a >= 0.999:
        return img
    c = img.copy()
    c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
    return c


def glass(frame, x0, y0, w, h, radius, alpha=1.0, tint=TINT):
    """Frosted-glass panel on the live frame (RGB, in place)."""
    if alpha <= 0.003 or w < 2 or h < 2:
        return
    x0, y0, w, h = int(round(x0)), int(round(y0)), int(round(w)), int(round(h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=int(255 * alpha))
    p = 3 * BLUR
    box = (max(x0 - p, 0), max(y0 - p, 0), min(x0 + w + p, frame.width), min(y0 + h + p, frame.height))
    reg = frame.crop(box).filter(ImageFilter.GaussianBlur(BLUR))
    ox, oy = x0 - box[0], y0 - box[1]
    frame.paste(reg.crop((ox, oy, ox + w, oy + h)), (x0, y0), mask)
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(t).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=CAPSULE + (int(tint * alpha),),
                                        outline=CREAM + (int(38 * alpha),), width=2)
    frame.paste(t, (x0, y0), t)


class Panel:
    """Static glass panel + artwork (hook, chapter chip); animated by alpha and a vertical offset."""

    def __init__(self, x0, y0, w, h, radius, sprite):
        self.x0, self.y0, self.w, self.h, self.radius, self.sprite = x0, y0, w, h, radius, sprite

    def draw(self, frame, alpha=1.0, dy=0.0):
        if alpha <= 0.003:
            return
        y = self.y0 + dy
        glass(frame, self.x0, y, self.w, self.h, self.radius, alpha)
        s = fade(self.sprite, alpha)
        frame.paste(s, (int(round(self.x0)), int(round(y))), s)


def hook(eyebrow, lines, top=290, size=74):
    """lines: list of runs [(text, italic)]; the panel hangs from `top`, clear of the subject's head."""
    ef = public(24, 700)
    lh = int(size * 1.04)
    lw = [sum(run_width(castoro(size, it), t) for t, it in ln) for ln in lines]
    ew = run_width(ef, eyebrow, extra=24 * 0.18)
    pw = int(max(max(lw), ew) + 2 * 58)
    ph = int(48 + len(lines) * lh + 42)
    spr = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(spr)
    tracked_caps(d, pw / 2, 54, eyebrow, ef, CREAM + (205,), 0.18)
    for i, (ln, w) in enumerate(zip(lines, lw)):
        x, bl = (pw - w) / 2, 48 + (i + 1) * lh - 6
        for t, it in ln:
            f = castoro(size, it)
            draw_run(d, x, bl, t, f, CREAM + (255,))
            x += run_width(f, t)
    return Panel((W - pw) / 2, top, pw, ph, 40, spr)


def chip(num, text, cy=CHIP_Y):
    nf, tf = castoro(44), public(39, 500)
    disc, gap, ph = 60, 18, 80
    tw = run_width(tf, text)
    pw = int(10 + disc + gap + tw + 34)
    spr = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(spr)
    d.ellipse([10, 10, 10 + disc, 10 + disc], fill=CREAM + (255,))
    s = str(num)
    nasc = nf.getmetrics()[0]
    draw_run(d, 10 + (disc - run_width(nf, s)) / 2 - 1, 10 + disc / 2 + nasc * 0.34, s, nf, FOREST + (255,))
    tasc = tf.getmetrics()[0]
    draw_run(d, 10 + disc + gap, ph / 2 + tasc * 0.36, text, tf, CREAM + (255,))
    return Panel((W - pw) / 2, cy - ph / 2, pw, ph, ph / 2, spr)


# ------------------------------------------------------------------ captions
def _disp(text, last):
    t = text.replace("'", "’")
    return t.rstrip(".,:;!?") if last else t.rstrip(".:;!?")


def _key(text):
    return text.lower().strip("\u201c\u201d\"").rstrip(".,:;!?\u201d").replace("\u2019", "'")


class Captions:
    """chunks: [{tokens: [{text, s, e}], s, e}] on the output timeline; emph: lowercase words set in Castoro Italic."""

    def __init__(self, chunks, emph=()):
        self.emph = {e.lower() for e in emph}
        self.items = [self._layout(c) for c in chunks]

    def _layout(self, c):
        sans, serif = public(CAP_SIZE, 600), castoro(EMPH_SIZE, True)
        asc, desc = sans.getmetrics()
        lh = asc + desc
        toks = c["tokens"]
        words = []
        for i, tk in enumerate(toks):
            txt = _disp(tk["text"], i == len(toks) - 1)
            f = serif if _key(tk["text"]) in self.emph else sans
            words.append(dict(txt=txt, f=f, w=run_width(f, txt), s=tk["s"]))
        sp = CAP_SIZE * 0.30
        tw = sum(w["w"] for w in words) + sp * (len(words) - 1)
        px, py = 34, 17
        cw, ch = int(tw + 2 * px), int(lh + 2 * py)
        full = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        dim = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        df, dd = ImageDraw.Draw(full), ImageDraw.Draw(dim)
        x = px
        for w in words:
            w["x0"], w["x1"] = int(max(x - sp / 2, 0)), int(min(x + w["w"] + sp / 2, cw))
            draw_run(df, x, py + asc, w["txt"], w["f"], CREAM + (255,))
            draw_run(dd, x, py + asc, w["txt"], w["f"], CREAM + (int(255 * DIM),))
            x += w["w"] + sp
        return dict(s=c["s"], e=c["e"], w=cw, h=ch, words=words, full=full, dim=dim)

    def _text(self, it, t):
        img = it["dim"].copy()
        for w in it["words"]:
            a = (t - w["s"] + 0.03) / 0.09
            if a <= 0:
                continue
            box = (w["x0"], 0, w["x1"], it["h"])
            seg = it["full"].crop(box) if a >= 1 else Image.blend(it["dim"].crop(box), it["full"].crop(box), a)
            img.paste(seg, box[:2])
        return img

    def draw(self, frame, t, cy=CAP_Y):
        items = self.items
        ci = next((i for i, it in enumerate(items) if it["s"] <= t < it["e"]), None)
        if ci is None:
            return
        it = items[ci]
        joined_prev = ci > 0 and abs(items[ci - 1]["e"] - it["s"]) < 0.02
        joined_next = ci + 1 < len(items) and abs(items[ci + 1]["s"] - it["e"]) < 0.02
        u = t - it["s"]
        if joined_prev:
            w = items[ci - 1]["w"] + (it["w"] - items[ci - 1]["w"]) * ease_out(u / 0.16)
            alpha, ta, dy = 1.0, ease_out(u / 0.12), 6 * (1 - ease_out(u / 0.16))
        else:
            w = it["w"] * (0.94 + 0.06 * ease_out(u / 0.14))
            alpha = ease_out(u / 0.14)
            ta, dy = alpha, 0.0
        if not joined_next:
            out = (it["e"] - t) / 0.14
            alpha, ta = alpha * min(out, 1), ta * min(out, 1)
        x0, y0 = (W - w) / 2, cy - it["h"] / 2
        glass(frame, x0, y0, w, it["h"], it["h"] / 2, alpha, tint=CAP_TINT)
        txt = fade(self._text(it, t), ta)
        tx = (W - it["w"]) / 2
        if w < it["w"]:                                    # clip to the capsule while it is still widening
            cut = int((it["w"] - w) / 2)
            txt = txt.crop((cut, 0, it["w"] - cut, it["h"]))
            tx += cut
        frame.paste(txt, (int(round(tx)), int(round(y0 + dy))), txt)


# ------------------------------------------------------------------ end card
LONGEVITY_END = dict(eyebrow=None, headline=["Live a better,", "*longer* life."],
                     sub=["Free 15-minute intro call.", "No obligation. We call you."],
                     cta="Book your free intro call  →", url="beoptimal.ca  ·  Barrie, ON")


def endcard(w, h, top=None, copy=None):
    """Cream background + staggered layers [(sprite, (x, y), delay_s)]. `copy` overrides LONGEVITY_END;
    top=None centres the block (4:5). Default geometry matches the approved end_A_ad."""
    c = dict(LONGEVITY_END, **(copy or {}))
    eb = 125 if c["eyebrow"] else 0                      # eyebrow pushes the headline down
    y_head = [225 + eb + 128 * i for i in range(len(c["headline"]))]
    y_sub = [y_head[-1] + 82 + 50 * i for i in range(len(c["sub"]))]
    y_pill = y_sub[-1] + 45
    block = y_pill + 96 + 58 + 10                        # pill height + url line
    if top is None:
        top = (h - block) // 2
    bg = Image.new("RGB", (w, h), CREAM)
    layers = []

    def layer(draw_fn, delay):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw_fn(im)
        bb = im.getbbox()
        layers.append((im.crop(bb), bb[:2], delay))

    def serif(im, baseline, spec, size):
        runs = serif_runs(spec, size)
        draw_runs(ImageDraw.Draw(im), (w - runs_width(runs)) / 2, baseline, runs, FOREST)

    def sans(im, baseline, text, font, fill):
        draw_run(ImageDraw.Draw(im), (w - run_width(font, text)) / 2, baseline, text, font, fill)

    lg = logo("green", 300)
    layer(lambda im: im.alpha_composite(lg, ((w - lg.width) // 2, top)), 0.0)
    if c["eyebrow"]:
        layer(lambda im: tracked_caps(ImageDraw.Draw(im), w / 2, top + 140, c["eyebrow"], public(23, 700), FOREST, 0.14), 0.05)
    for i, (y, ln) in enumerate(zip(y_head, c["headline"])):
        layer(lambda im, y=y, ln=ln: serif(im, top + y, ln, 128 if len(c["headline"]) < 3 else 112), 0.08 + 0.07 * i)
    f = public(38, 400)
    layer(lambda im: [sans(im, top + y, ln, f, BODY) for y, ln in zip(y_sub, c["sub"])], 0.26)
    box = {}
    layer(lambda im: box.setdefault("b", pill(im, w / 2, top + y_pill, c["cta"], public(40, 500), 48, 26, FOREST, CREAM)), 0.34)
    layer(lambda im: sans(im, box["b"] + 58, c["url"], public(32, 500), FOREST), 0.42)
    return bg, layers


def endcard_frame(base, bg, layers, tau, xfade):
    """tau: seconds since the end-card transition began. base: the footage frame (ignored once faded)."""
    img = Image.blend(base, bg, min(tau / xfade, 1.0)) if tau < xfade else bg.copy()
    for spr, (x, y), delay in layers:
        u = (tau - xfade - delay) / 0.45            # reveal starts once the cream is fully up
        if u <= 0:
            continue
        a = ease_out(u)
        s = fade(spr, a)
        img.paste(s, (x, int(round(y + 18 * (1 - a)))), s)
    return img


def safe_overlay(img, win45):
    """QA view: shaded Reels no-go zones + dashed 4:5 window."""
    o = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(o)
    d.rectangle([0, 0, W, SAFE_TOP], fill=(220, 60, 50, 90))
    d.rectangle([0, SAFE_BOTTOM, W, H], fill=(220, 60, 50, 90))
    for y in win45:
        for x in range(0, W, 40):
            d.line([x, y, x + 22, y], fill=(255, 255, 255, 230), width=4)
    return Image.alpha_composite(img.convert("RGBA"), o).convert("RGB")

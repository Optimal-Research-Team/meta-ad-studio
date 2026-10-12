"""Shared drawing helpers built on the Optimal Health Design System tokens.

Tokens (Optimal Health Design System README / colors_and_type.css):
  cream #FFFCF7 canvas · forest #2C4E25 · deep accent #1A500F · sage #87A482
  Castoro display (tracking -0.04em, lh 1.0, italic = emphasised noun) · Public Sans UI (-0.02em)
  48px pill CTAs · dark capsules (not gradient scrims) for text over imagery · no grain filter.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ROOT, "fonts")
LOGOS = os.path.join(ROOT, "ds/assets/logos")

CREAM = (255, 252, 247)
FOREST = (44, 78, 37)
DEEP = (26, 80, 15)
SAGE = (135, 164, 130)
INK = (4, 5, 4)
BODY = (62, 70, 60)
MUTED = (140, 138, 130)
CAPSULE = (16, 24, 14)  # forest-black used for text capsules over footage

_fonts = {}


def castoro(size, italic=False):
    k = ("c", size, italic)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(os.path.join(FONTS, "Castoro-Italic.ttf" if italic else "Castoro-Regular.ttf"), size)
    return _fonts[k]


def public(size, weight=400):
    k = ("p", size, weight)
    if k not in _fonts:
        f = ImageFont.truetype(os.path.join(FONTS, "PublicSans.ttf"), size)
        f.set_variation_by_axes([weight])
        _fonts[k] = f
    return _fonts[k]


def _track(font):
    """Design-system letter-spacing in px: Castoro -0.04em, Public Sans -0.02em."""
    return (-0.04 if "Castoro" in font.getname()[0] else -0.02) * font.size


def run_width(font, text, extra=0.0):
    if not text:
        return 0.0
    return font.getlength(text) + (_track(font) + extra) * (len(text) - 1)


def draw_run(d, x, baseline, text, font, fill, extra=0.0):
    """Draw with kerning-preserving advances plus tracking; returns the pen x after the run."""
    tr = _track(font) + extra
    for i, ch in enumerate(text):
        d.text((x, baseline), ch, font=font, fill=fill, anchor="ls")
        nxt = text[i + 1] if i + 1 < len(text) else ""
        adv = (font.getlength(ch + nxt) - font.getlength(nxt)) if nxt else font.getlength(ch)
        x += adv + (tr if nxt else 0)
    return x


def runs_width(runs, extra=0.0):
    """runs: [(text, font)] on one line."""
    return sum(run_width(f, t, extra) for t, f in runs)


def draw_runs(d, x, baseline, runs, fill, extra=0.0):
    for t, f in runs:
        x = draw_run(d, x, baseline, t, f, fill, extra)
    return x


def serif_runs(spec, size):
    """'Live a better, *longer* life.' -> runs with *italic* spans in Castoro italic."""
    out, ital = [], False
    for i, part in enumerate(spec.split("*")):
        if part:
            out.append((part, castoro(size, italic=(i % 2 == 1))))
    return out


def wrap_runs(spec, size, max_w):
    """Greedy word wrap preserving *italic* spans. Returns list of run-lines."""
    words, ital = [], False
    for i, part in enumerate(spec.split("*")):
        for w in part.split(" "):
            if w:
                words.append((w, i % 2 == 1))
    lines, cur = [], []
    for w, it in words:
        cand = cur + [(w, it)]
        runs = _merge(cand, size)
        if cur and runs_width(runs) > max_w:
            lines.append(_merge(cur, size))
            cur = [(w, it)]
        else:
            cur = cand
    if cur:
        lines.append(_merge(cur, size))
    return lines


def _merge(words, size):
    runs = []
    for j, (w, it) in enumerate(words):
        txt = (" " if j else "") + w
        if runs and runs[-1][2] == it:
            runs[-1] = (runs[-1][0] + txt, runs[-1][1], it)
        else:
            runs.append((txt, castoro(size, it), it))
    return [(t, f) for t, f, _ in runs]


def logo(variant, width):
    """variant: 'green' (on cream/light) | 'cream' (on dark) | 'symbol-green' | 'symbol-white'."""
    fn = {"green": "OptimalLogo-Green.png", "cream": "Optimal_Logo_Inverted.png",
          "symbol-green": "optimal-symbol-green.png", "symbol-white": "optimal-symbol-white.png"}[variant]
    im = Image.open(os.path.join(LOGOS, fn)).convert("RGBA")
    bbox = im.getbbox()
    im = im.crop(bbox)
    h = round(im.height * width / im.width)
    return im.resize((width, h), Image.LANCZOS)


def arrow_font(size):
    k = ("arrow", size)
    if k not in _fonts:
        f = ImageFont.truetype(os.path.join(FONTS, "Inter.ttf"), size)
        f.set_variation_by_axes([min(max(size, 14), 32), 500])
        _fonts[k] = f
    return _fonts[k]


def pill(img, cx, top, text, font, pad_x, pad_y, fill, text_fill, shadow=True):
    """Design-system CTA: full pill, Public Sans 500, optional elevated shadow 0 4 25 rgba(0,0,0,.16).
    A trailing '→' is set in Inter (Public Sans has no arrow glyph)."""
    d = ImageDraw.Draw(img)
    asc, desc = font.getmetrics()
    arrow = text.endswith("→")
    label = text[:-1].rstrip() if arrow else text
    af = arrow_font(font.size)
    gap = font.size * 0.45
    w = run_width(font, label) + ((gap + af.getlength("→")) if arrow else 0)
    h = asc + desc + 2 * pad_y
    box = [cx - w / 2 - pad_x, top, cx + w / 2 + pad_x, top + h]
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([box[0], box[1] + 4, box[2], box[3] + 4], radius=h / 2, fill=(0, 0, 0, 41))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
        d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=h / 2, fill=fill)
    x = draw_run(d, cx - w / 2, top + pad_y + asc, label, font, text_fill)
    if arrow:
        d.text((x + gap, top + pad_y + asc), "→", font=af, fill=text_fill, anchor="ls")
    return top + h


def tracked_caps(d, cx, baseline, text, font, fill, spacing_em):
    """All-caps eyebrow, centred, with positive tracking."""
    extra = spacing_em * font.size - _track(font)
    w = run_width(font, text, extra)
    draw_run(d, cx - w / 2, baseline, text, font, fill, extra)
    return w

"""Meta ad studio: an iPhone talking-head clip -> branded 9:16 + 4:5 ad cuts.

    python3 studio.py ads/longevity_core_v2.py            # every variant in the spec
    python3 studio.py ads/longevity_core_v2.py Tight      # one variant
    python3 studio.py ads/longevity_core_v2.py --audio    # rebuild only the soundtrack (video stream copied)

Per variant: frame-exact segment trims; each shot holds a face-anchored punch-in and drifts slowly in (sub-pixel,
so no zoompan jitter); P3/HDR -> Rec.709 + light grade; 30 fps; captions / chapter chips / hook / end card from
adgfx; voice chain to -14 LUFS over an optional flat music bed that lifts on the end card; metadata (GPS) stripped.
Outputs land in out/<ad>/: <Name>_<Variant>_9x16.mp4 and _4x5.mp4, thumbnails, .srt; QA sheets in work/<ad>/.
"""
import importlib.util
import json
import os
import re
import statistics
import subprocess
import sys

from PIL import Image

import adgfx as G

ROOT = os.path.dirname(os.path.abspath(__file__))
FF = os.path.join(ROOT, "tools/node_modules/ffmpeg-static/ffmpeg")
FP = os.path.join(ROOT, "tools/node_modules/ffprobe-static/bin/darwin/arm64/ffprobe")
FPS = 30
W, H = G.W, G.H
H45 = 1350
XFADE_END = 0.35            # body -> end card crossfade
PUSH = 0.03                 # slow drift-in across every shot (3% of frame)
TARGET_LUFS = -14.0
BED_LUFS, BED_END_LUFS = -44.0, -32.0   # music under the voice / lifted on the end card (Oct 12: halved, -6 dB)
DEFAULT_GRADE = ("colorbalance=rm=0.025:bm=-0.03:rh=0.01:bh=-0.015,"
                 "curves=m='0/0 0.25/0.235 0.75/0.77 1/1',vibrance=intensity=0.06")
VOICE = ("highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=4200:t=q:w=1.2:g=1.5,deesser=i=0.35,"
         "acompressor=threshold=0.05:ratio=3:attack=4:release=120:knee=4")
LIMITER = "alimiter=limit=0.75:attack=3:release=60:level=false"   # -2.5 dBFS: leaves room for AAC overshoot


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def load_spec(path):
    s = importlib.util.spec_from_file_location("adspec", path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ analysis (cached in work/)
def probe(src):
    d = json.loads(run([FP, "-v", "error", "-show_streams", "-show_format", "-of", "json", src]).stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    return dict(w=v["width"], h=v["height"], pix=v.get("pix_fmt", ""), prim=v.get("color_primaries", "bt709"),
                trc=v.get("color_transfer", "bt709"), mat=v.get("color_space", "bt709"),
                rng=v.get("color_range", ""), dur=float(d["format"]["duration"]))


ZPRIM = {"bt709": "709", "smpte432": "smpte432", "bt2020": "2020", "smpte170m": "170m", "bt470bg": "470bg"}
ZMAT = {"bt709": "709", "smpte170m": "170m", "bt470bg": "470bg", "bt2020nc": "2020_ncl"}


def color_chain(p):
    """Source colour -> full-range Rec.709 planar RGB. HDR (HLG/PQ) is tone-mapped; P3 is gamut-converted."""
    rin = "full" if p["pix"].startswith("yuvj") or p["rng"] == "pc" else "limited"
    pin, mat = ZPRIM.get(p["prim"], "709"), ZMAT.get(p["mat"], "709")
    if p["trc"] in ("arib-std-b67", "smpte2084"):
        return (f"zscale=pin={pin}:min={mat}:tin={p['trc']}:rin={rin}:t=linear:npl=203,format=gbrpf32le,"
                "zscale=p=709,tonemap=hable:desat=0,zscale=t=709:m=709:r=full,format=gbrp")
    return f"zscale=pin={pin}:p=709:min={mat}:m=709:tin=709:t=709:rin={rin}:r=full,format=gbrp"


def silences(src, work):
    path = os.path.join(work, "silences.json")
    if not os.path.exists(path):
        err = subprocess.run([FF, "-hide_banner", "-i", src, "-vn", "-af", "highpass=f=90,silencedetect=noise=-42dB:d=0.22",
                              "-f", "null", "-"], capture_output=True, text=True).stderr
        st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
        en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
        json.dump([[a, b] for a, b in zip(st, en)], open(path, "w"))
    merged = []
    for a, b in json.load(open(path)):          # full-band detection fragments pauses; re-join them
        if merged and a - merged[-1][1] < 0.1:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return merged


def words(work, sil, fixes):
    """Whisper words snapped to real pauses (whisper smears words across silences), then text fixes applied."""
    raw = json.load(open(os.path.join(work, "words.json")))["words"]
    toks, starts = [], []
    for w in raw:
        if w["w"].startswith("-") and toks:          # "60" + "-minute" -> "60-minute"
            toks[-1]["text"] += w["w"]; toks[-1]["e"] = w["e"]; continue
        toks.append(dict(text=w["w"], s=w["s"], e=w["e"])); starts.append(w["s"])
    for i, t in enumerate(toks):
        for a, b in sil:
            if a - 0.02 <= t["s"] < b - 0.05:                  # starts inside a pause -> starts at its end
                t["s"] = b
            elif t["s"] < a and t["e"] > b and b - a >= 0.25:  # spans a pause -> belongs after it
                t["s"] = b
                if i:
                    toks[i - 1]["e"] = max(toks[i - 1]["e"], a)
        for a, b in sil:
            if a < t["e"] <= b and t["e"] - a > 0.05 and a > t["s"]:
                t["e"] = a
    keep = []
    for t, s0 in zip(toks, starts):
        k = next((k for k in fixes if abs(k - s0) < 0.03), None)
        if k is None:
            keep.append(t)
        elif fixes[k] is not None:
            keep.append(dict(t, text=fixes[k]))
    return keep


def face_track(work):
    return [(r["t"], r["face"]) for r in json.load(open(os.path.join(work, "faces.json"))) if r["face"]]


def seg_anchor(track, s, e):
    pts = [f for t, f in track if s <= t <= e] or [f for _, f in track]
    return statistics.median(p[0] for p in pts), statistics.median(p[1] for p in pts)


# ------------------------------------------------------------------ timeline + captions
def timeline(spec, variant):
    """Segments quantized to whole output frames, so picture cuts, audio cuts and captions share one clock."""
    segs, t = [], 0.0
    for name in spec.VARIANTS[variant]:
        s, e, z = spec.SEGS[name]
        joined = bool(segs) and abs(s - spec.SEGS[segs[-1]["name"]][1]) < 0.05
        if joined:                                   # zoom cut on continuous speech: share the exact cut point
            s = segs[-1]["e"]
        n = round((e - s) * FPS)
        segs.append(dict(name=name, s=s, e=s + n / FPS, z=z, o=t, n=n, joined=joined))
        t += n / FPS
    return segs, t


def to_out(segs, toks):
    """Each word goes to the kept segment it overlaps most (clamped to it); words in cut pauses drop."""
    out = []
    for tk in toks:
        ov = [(min(tk["e"], g["e"]) - max(tk["s"], g["s"]), g) for g in segs]
        o, g = max(ov, key=lambda x: x[0])
        if o >= min(0.05, 0.5 * (tk["e"] - tk["s"])):
            s, e = max(tk["s"], g["s"]), min(tk["e"], g["e"])
            out.append(dict(tk, s=g["o"] + s - g["s"], e=g["o"] + e - g["s"], seg=g["name"]))
    return out


STOP = {"the", "a", "an", "to", "of", "in", "and", "or", "with", "for", "our", "at", "by", "on", "that", "their",
        "if", "so", "i'm", "we"}


KEEP = {("nurse", "practitioner"), ("body", "composition"), ("grip", "strength"), ("full", "hour"),
        ("care", "coordinator"), ("optimal", "clinic"), ("information", "session"), ("information", "call"),
        ("health", "domains"), ("blood", "work"), ("annual", "longevity"), ("longevity", "exam"),
        ("intro", "call"), ("free", "phone"), ("last", "time")}       # caption lines never break inside these pairs


def _bare(w):
    return w["text"].lower().rstrip(".,:;!?")


def _balanced(ws, keep=KEEP):
    sans, serif = G.public(G.CAP_SIZE, 600), G.castoro(G.EMPH_SIZE, True)
    sp = G.CAP_SIZE * 0.30

    def width(part):
        return sum(G.run_width(sans, w["text"].rstrip(".,:;!?")) for w in part) * 1.03 + sp * (len(part) - 1)

    def cost(part, last, nxt=None):
        px = width(part)
        if px > G.MAX_CAP_PX and len(part) > 1:
            return 1e9
        c = ((G.MAX_CAP_PX - px) / 40) ** 2 + 60
        if not last and part[-1]["text"].lower().rstrip(".,:;!?") in STOP:
            c += 400
        if len(part) == 1 and len(ws) > 1:
            c += 250
        if nxt is not None and (_bare(part[-1]), _bare(nxt)) in keep:
            c += 300
        return c
    n = len(ws)
    best, back = [0.0] + [1e18] * n, [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(j):
            c = best[i] + cost(ws[i:j], j == n, ws[j] if j < n else None)
            if c < best[j]:
                best[j], back[j] = c, i
    parts, j = [], n
    while j > 0:
        parts.append(ws[back[j]:j]); j = back[j]
    return parts[::-1]


def chunks(otoks, keep=KEEP):
    """Phrases break at punctuation and at every cut; each phrase is split into balanced one-line chunks."""
    phrases, cur = [], []
    for i, t in enumerate(otoks):
        cur.append(t)
        nxt = otoks[i + 1] if i + 1 < len(otoks) else None
        lone_comma = t["text"][-1] == "," and len(cur) == 1     # "Hi," alone would flash for a few frames
        if (t["text"][-1] in ",.:;?!" and not lone_comma) or nxt is None or nxt["seg"] != t["seg"]:
            phrases.append(cur); cur = []
    out = []
    for ph in phrases:
        for part in _balanced(ph, keep):
            out.append(dict(tokens=part, s=part[0]["s"] - 0.08, e=part[-1]["e"] + 0.25))
    out[0]["s"] = max(out[0]["s"], 0.0)
    for a, b in zip(out, out[1:]):
        if b["s"] - a["e"] < 0.6:
            a["e"] = b["s"]                     # hold through short pauses: no flicker
    return out


def write_srt(chs, path):
    def ts(t):
        ms = int(round(t * 1000))
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
    with open(path, "w") as f:
        for i, c in enumerate(chs, 1):
            text = " ".join(G._disp(t["text"], j == len(c["tokens"]) - 1) for j, t in enumerate(c["tokens"]))
            f.write(f"{i}\n{ts(c['s'])} --> {ts(c['e'])}\n{text}\n\n")


# ------------------------------------------------------------------ picture
def decode_cmd(src, p, g, grade):
    cover = "" if (p["w"], p["h"]) == (W, H) else \
        f",scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
    vf = f"fps={FPS},{color_chain(p)},{grade}{cover},format=rgb24"
    return [FF, "-v", "error", "-ss", f"{g['s']:.4f}", "-i", src, "-t", f"{g['n'] / FPS + 0.2:.4f}", "-vf", vf,
            "-frames:v", str(g["n"]), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]


def segment_frames(src, p, g, grade, anchor):
    """Yield the segment's frames with its punch-in plus a slow eased drift, scaled about the face."""
    dec = subprocess.Popen(decode_cmd(src, p, g, grade), stdout=subprocess.PIPE)
    fb, last = W * H * 3, None
    fx, fy = anchor[0] * W, anchor[1] * H
    for k in range(g["n"]):
        buf = dec.stdout.read(fb)
        if len(buf) < fb:
            buf = last                                 # decoder came up a frame short: hold the last one
        last = buf
        fr = Image.frombuffer("RGB", (W, H), buf, "raw", "RGB", 0, 1)
        z = g["z"] * (1 + PUSH * G.ease_in_out(k / max(g["n"] - 1, 1)))
        if z > 1.0005:
            ww, wh = W / z, H / z
            x0 = min(max(fx * (1 - 1 / z), 0), W - ww)
            y0 = min(max(fy * (1 - 1 / z), 0), H - wh)
            fr = fr.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + ww, y0 + wh))
        else:
            fr = fr.copy()
        yield fr
    dec.stdout.close()
    dec.wait()


def encoder(path, w, h):
    return subprocess.Popen([FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS),
                             "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                             "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high",
                             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", path],
                            stdin=subprocess.PIPE)


# ------------------------------------------------------------------ sound
def voice_pan(src):
    """Wireless mics into an iPhone often land on one channel only (the other is digital silence).
    Use the live channel(s) and centre the voice: dual mono in both ears."""
    err = subprocess.run([FF, "-hide_banner", "-i", src, "-vn", "-af",
                          "astats=measure_overall=none:measure_perchannel=RMS_level", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    rms = [float(x) if x not in ("-inf", "inf") else -200.0 for x in re.findall(r"RMS level dB: (-?[\w.]+)", err)]
    if len(rms) < 2:
        return "pan=stereo|c0=c0|c1=c0"
    live = [i for i, r in enumerate(rms) if r > max(rms) - 20]
    mix = "+".join(f"{1 / len(live):.3f}*c{i}" for i in live)
    return f"pan=stereo|c0={mix}|c1={mix}"


def audio(src, segs, body, total, path, music=None):
    parts, labels = [], []
    for i, g in enumerate(segs):
        d = g["e"] - g["s"]
        fin = "" if g.get("joined") else ",afade=t=in:d=0.012"            # no fades inside continuous speech
        fout = "" if i + 1 < len(segs) and segs[i + 1].get("joined") else f",afade=t=out:st={d - 0.025:.3f}:d=0.025"
        parts.append(f"[0:a]atrim=start={g['s']:.6f}:end={g['e']:.6f},asetpts=PTS-STARTPTS{fin}{fout}[a{i}]")
        labels.append(f"[a{i}]")
    voice = (";".join(parts) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=0:a=1,aresample=48000,"
             f"{voice_pan(src)}," + VOICE)

    def measure(extra):
        err = subprocess.run([FF, "-hide_banner", "-i", src, "-filter_complex", voice + extra + ",ebur128", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])

    # handheld mics are peaky: static gain + brick-wall limiter, re-measured after the limiter until on target
    gain = TARGET_LUFS - measure("")
    for _ in range(3):
        got = measure(f",volume={gain:.2f}dB,{LIMITER}")
        if abs(got - TARGET_LUFS) < 0.25:
            break
        gain += TARGET_LUFS - got
    graph = voice + f",volume={gain:.2f}dB,{LIMITER},apad=whole_dur={total:.3f}[v]"
    inputs = ["-i", src]
    if music:
        err = subprocess.run([FF, "-hide_banner", "-i", music, "-af", "ebur128", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        m_lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])
        g1, g2 = 10 ** ((BED_LUFS - m_lufs) / 20), 10 ** ((BED_END_LUFS - m_lufs) / 20)
        t0 = body - XFADE_END
        inputs += ["-i", music, "-i", music]           # second copy crossfaded on for cuts longer than the bed
        graph += (f";[1:a][2:a]acrossfade=d=3,aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.3f},"
                  f"volume=eval=frame:volume='if(lt(t,{t0:.3f}),{g1:.4f},{g1:.4f}+({g2:.4f}-{g1:.4f})*min((t-{t0:.3f})/0.6,1))',"
                  f"afade=t=in:d=0.4,afade=t=out:st={total - 1.1:.3f}:d=1.1[m];"
                  f"[v][m]amix=inputs=2:normalize=0:duration=first,{LIMITER}[out]")
    else:
        graph += ";[v]anull[out]"
    run([FF, "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]", "-t", f"{total:.3f}",
         "-c:a", "pcm_s16le", "-ar", "48000", path])


def mux(vpath, apath, out):
    run([FF, "-y", "-v", "error", "-i", vpath, "-i", apath, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-map_metadata", "-1",
         "-metadata", "title=", "-movflags", "+faststart", out])
    os.remove(vpath)


def music_path(spec):
    m = getattr(spec, "MUSIC", None)
    return os.path.join(ROOT, m) if m else None


# ------------------------------------------------------------------ render
def render(spec, variant):
    src = os.path.join(ROOT, spec.SRC)
    work, out_dir = os.path.join(ROOT, spec.WORK), os.path.join(ROOT, spec.OUT)
    os.makedirs(out_dir, exist_ok=True)
    p = probe(src)
    toks = words(work, silences(src, work), spec.FIX)
    track = face_track(work)
    segs, body = timeline(spec, variant)
    chs = chunks(to_out(segs, toks), KEEP | set(getattr(spec, "KEEP", ())))
    tag = f"{spec.NAME}_{variant}"
    write_srt(chs, os.path.join(out_dir, f"{tag}.srt"))
    grade = getattr(spec, "GRADE", DEFAULT_GRADE)

    face_y = statistics.median(f[1] for _, f in track) * H
    top45 = int(min(max(face_y - 0.36 * H45, 0), H - H45))
    win45 = (top45, top45 + H45)

    caps = G.Captions(chs, getattr(spec, "EMPH", ()))
    hook = G.hook(spec.HOOK["eyebrow"], spec.HOOK["lines"], top=spec.HOOK.get("top", 290), size=spec.HOOK.get("size", 74))
    hook_until = spec.HOOK.get("until", 3.4)
    chips = []
    for names, num, text in spec.TAGS:
        gs = [g for g in segs if g["name"] in names]
        if gs:
            chips.append((gs[0]["o"], gs[-1]["o"] + gs[-1]["n"] / FPS, G.chip(num, text)))
    bg916, lay916 = G.endcard(W, H, 350, getattr(spec, "END", None))
    bg45, lay45 = G.endcard(W, H45, None, getattr(spec, "END", None))

    v916, v45 = os.path.join(out_dir, f".{tag}_9x16.mp4"), os.path.join(out_dir, f".{tag}_4x5.mp4")
    e916, e45 = encoder(v916, W, H), encoder(v45, W, H45)
    n, thumbs = 0, {}

    def emit(fr, f45):
        nonlocal n
        e916.stdin.write(fr.tobytes()); e45.stdin.write(f45.tobytes())
        n += 1

    for g in segs:
        for fr in segment_frames(src, p, g, grade, seg_anchor(track, g["s"], g["e"])):
            t = n / FPS
            if t < hook_until + 0.35:                       # on screen from frame 0, lifts away at `until`
                u = max(t - hook_until, 0) / 0.35
                hook.draw(fr, 1 - G.ease_out(u), -14 * G.ease_out(u))
            for a, b, chp in chips:
                if a <= t < b:
                    u_in, u_out = (t - a) / 0.3, (b - t) / 0.18
                    chp.draw(fr, G.ease_out(u_in) * min(u_out, 1), -10 * (1 - G.ease_out(u_in)))
            caps.draw(fr, t)
            f45 = fr.crop((0, win45[0], W, win45[1]))
            tau = t - (body - XFADE_END)
            if tau > 0:
                fr, f45 = G.endcard_frame(fr, bg916, lay916, tau, XFADE_END), G.endcard_frame(f45, bg45, lay45, tau, XFADE_END)
            if n == int(spec.THUMB_AT * FPS):
                thumbs["9x16"], thumbs["4x5"], thumbs["qa"] = fr.copy(), f45.copy(), G.safe_overlay(fr, win45)
            emit(fr, f45)
    for k in range(int(round(spec.END_DUR * FPS))):
        tau = XFADE_END + k / FPS
        emit(G.endcard_frame(None, bg916, lay916, tau, XFADE_END), G.endcard_frame(None, bg45, lay45, tau, XFADE_END))
    for e in (e916, e45):
        e.stdin.close(); e.wait()

    total = n / FPS
    apath = os.path.join(work, f"{tag}.wav")
    audio(src, segs, body, total, apath, music_path(spec))
    mux(v916, apath, os.path.join(out_dir, f"{tag}_9x16.mp4"))
    mux(v45, apath, os.path.join(out_dir, f"{tag}_4x5.mp4"))
    for k, im in thumbs.items():
        im.save(os.path.join(out_dir if k != "qa" else work, f"{tag}_{k}_thumb.jpg"), quality=92)
    print(f"{tag}: {n} frames = {total:.2f}s  (body {body:.2f}s + end {spec.END_DUR}s), 4:5 window {win45}, "
          f"{len(chs)} caption chunks, music: {'yes' if music_path(spec) else 'no'}")
    return tag


def remix(spec, variant):
    """Audio-only pass: rebuild the soundtrack and swap it into the existing renders (video stream copied)."""
    src, work, out_dir = (os.path.join(ROOT, x) for x in (spec.SRC, spec.WORK, spec.OUT))
    segs, body = timeline(spec, variant)
    tag = f"{spec.NAME}_{variant}"
    apath = os.path.join(work, f"{tag}.wav")
    audio(src, segs, body, body + round(spec.END_DUR * FPS) / FPS, apath, music_path(spec))
    for ratio in ("9x16", "4x5"):
        final = os.path.join(out_dir, f"{tag}_{ratio}.mp4")
        tmp = os.path.join(out_dir, f".{tag}_{ratio}.mp4")
        run([FF, "-y", "-v", "error", "-i", final, "-map", "0:v", "-c", "copy", tmp])
        mux(tmp, apath, final)
    return tag


def qa(spec, tag):
    out_dir, work = os.path.join(ROOT, spec.OUT), os.path.join(ROOT, spec.WORK)
    for ratio in ("9x16", "4x5"):
        f = os.path.join(out_dir, f"{tag}_{ratio}.mp4")
        d = json.loads(run([FP, "-v", "error", "-show_streams", "-show_format", "-of", "json", f]).stdout)
        v = next(s for s in d["streams"] if s["codec_type"] == "video")
        a = next(s for s in d["streams"] if s["codec_type"] == "audio")
        err = subprocess.run([FF, "-hide_banner", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        i_ = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1]
        pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)[-1]
        tags = d["format"].get("tags", {})
        print(f"  {ratio}: {v['width']}x{v['height']} {v['codec_name']} {v['pix_fmt']} {v.get('color_primaries')} "
              f"{v['r_frame_rate']}fps | {a['codec_name']} {a['sample_rate']}Hz | {float(d['format']['duration']):.2f}s | "
              f"{int(d['format']['size']) / 1e6:.1f} MB | {i_} LUFS, peak {pk} dBTP | gps: {'YES' if any('location' in k for k in tags) else 'stripped'}")
        run([FF, "-y", "-v", "error", "-i", f, "-vf", "fps=1,scale=200:-2,tile=8x6:padding=4:color=black",
             "-frames:v", "1", "-q:v", "3", os.path.join(work, f"{tag}_{ratio}_sheet.jpg")])


if __name__ == "__main__":
    spec = load_spec(sys.argv[1])
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    step = remix if "--audio" in sys.argv else render
    for v in (args or list(spec.VARIANTS)):
        qa(spec, step(spec, v))

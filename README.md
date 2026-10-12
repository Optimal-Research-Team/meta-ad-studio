# Meta ad studio

iPhone talking-head clips → branded Meta ad cuts (9:16 Reels/Stories + 4:5 Feed), driven from chat.
Everything runs locally: no footage leaves the Mac unless a Higgsfield step is explicitly requested.

## Flow

1. **Drop** the clip in `inbox/` and give a one-line brief (offer, CTA, length).
2. **Prep + read** (automatic): probe → frames (`fps=2`) + contact sheets → word-level transcript
   (`transcribe.py`, faster-whisper; `WHISPER_MODEL=medium.en` for the cross-check) → on-screen text
   (`ocr.py`, Apple Vision) → face track (`vision.py`) → silences + loudness.
3. **Propose the cut** as an ad spec in `ads/<ad>.py`: segments with punch-ins, caption fixes, hook, point tags.
4. **Render** `python3 studio.py ads/<ad>.py [Variant] [--audio]` → `out/<ad>/`.
5. **Review + tweak**: edit the spec and re-render (no credits). `--audio` rebuilds only the voice track.

## What `studio.py` does per variant

| Stage | Detail |
|---|---|
| Trim | Segment list from the spec; ~0.13 s handles around speech; pauses in static shots become jump cuts |
| Motion | Alternating punch-in per cut (1.0–1.25×) plus a slow 3% eased drift-in on every shot, both scaled *about the detected face*, sub-pixel (no zoompan jitter); cuts are frame-exact |
| Colour | Display-P3 → Rec.709 gamut conversion; HLG/PQ HDR → SDR tone-map (hable); light warm grade + soft S-curve (`GRADE` in the spec overrides); 30 fps CFR |
| Captions | One line, Public Sans 600 @ 62 px on dense frosted glass with a cream hairline; spoken words brighten as said (upcoming at 50%); `EMPH` words switch to Castoro Italic; capsule eases its width between phrases; typographic apostrophes; whisper times snapped to real pauses |
| Graphics | Hook glass panel (eyebrow + Castoro) from frame 0; numbered chapter chips at the top; cream end card with a staggered reveal after the dissolve |
| Safe zones | Overlays live between y 290–1248 (Reels top 14% / bottom 35% clear); 4:5 window is placed from the face track |
| Audio | Voice: the live mic channel is detected and centred (wireless mics into an iPhone often record to the left channel only), highpass 80 Hz, −2 dB @ 250 Hz, +1.5 dB presence, de-esser, compressor, static gain re-measured after a brick-wall limiter until −14 LUFS. Optional flat music bed (`MUSIC`) at −44 LUFS, lifting to −32 on the end card |
| Delivery | H.264 High, yuv420p, BT.709 tags, AAC 192k/48k, `+faststart`, **all metadata stripped (iPhone GPS)** |
| QA | Specs, loudness and GPS check per file, contact sheets + safe-zone overlay frame in `work/<ad>/` |

## Layout

```
inbox/        source clips (never committed)
work/<ad>/    frames, sheets, words.json, ocr/, faces.json, silences.json, QA sheets
ads/<ad>.py   the edit decision list for one ad (segments, fixes, hook, chapters, variants)
out/<ad>/     <Name>_<Variant>_9x16.mp4 / _4x5.mp4, thumbnails, .srt
brand/        Optimal design-system fonts (OFL, see brand/fonts/FONTS.md), logos and gfxlib.py
brand/audio/  licensed music beds (never committed: drop your own licensed track here)
adgfx.py      graphics: glass panels, captions, hook, chapter chips, end card, safe-zone QA
studio.py     render pipeline (decode -> punch-ins -> overlays -> 9:16 + 4:5 encode -> soundtrack -> mux -> QA)
tools/        ffmpeg-static + ffprobe-static (npm i --prefix tools ffmpeg-static ffprobe-static)
```

## Setup

```bash
npm i --prefix tools ffmpeg-static ffprobe-static
python3 -m pip install --user faster-whisper pyobjc-framework-Vision pyobjc-framework-Quartz
```

Swift's Vision bridge is broken on this Command Line Tools install (duplicate `SwiftBridging` module), so OCR
and face detection go through PyObjC instead.

## Writing an ad spec

An ad is one Python file in `ads/`. All times are **source** seconds (take them from `work/<ad>/words.json`
and `silences.json`); the pipeline maps everything onto the output timeline.

| Field | Meaning |
|---|---|
| `NAME`, `SRC`, `WORK`, `OUT` | Output name prefix and paths |
| `SEGS` | `name: (start, end, punch_in)`; cut at pauses, ~0.13 s handles; alternate the punch-in at every cut so jump cuts read as intentional. A segment that starts where the previous one ends is a **zoom cut on continuous speech** (shared frame-exact cut point, no audio fades): use it to add beats inside a long unbroken sentence or a list |
| `VARIANTS` | `variant: [segment names]`; each variant renders 9:16 and 4:5 |
| `FIX` | `whisper word start: "caption text"` (`None` drops the word); punctuation marks phrase breaks |
| `EMPH` | Words set in Castoro Italic inside captions; at most one per phrase |
| `KEEP` | Extra word pairs a caption line must never split (adds to the built-in list: nurse practitioner, body composition, full hour…) |
| `HOOK` | `eyebrow`, `lines` (runs of `(text, italic)`), `top` (keep it clear of the head), `size` (Castoro px; 56–62 for one compact line over a close-up), `until` (s) |
| `TAGS` | `([segment names], number, label)`: the chapter chip shown over those segments |
| `MUSIC` | Path to a music bed (or omit for voice only) |
| `END` | End-card copy: `eyebrow`, `headline` (lines, `*italic*`), `sub`, `cta`, `url`; omitted keys fall back to the longevity card |
| `GRADE` | Optional ffmpeg RGB filter chain replacing the default warm grade |
| `END_DUR`, `THUMB_AT` | End-card hold (s), thumbnail time (s) |

Examples:
- `ads/longevity_core_v2.py`: walk-and-talk, three numbered points, two variants.
- `ads/longevity_ad2_full_hour.py`: seated close-up, spoken hook question, zoom cut inside a long sentence.
- `ads/menopause_ad1_myself.py`: staccato punch-ins on a symptom list, process-step chapters, menopause end card.

## Uploading to Meta

- Upload `*_9x16.mp4` for Reels and Stories placements and `*_4x5.mp4` for Feed (use asset customisation in one ad).
- Captions are burned in; the `.srt` is optional and only matters if Meta's own captions are switched on.
- Use `*_thumb.jpg` as the cover: it is the hook frame.
- Health ads: keep copy free of personal-attribute phrasing ("Are you struggling with…"); the studio flags lines like that when proposing a cut.


## Static ads (`static/`)

Branded Meta statics, built with the same tokens as the Instagram relaunch (Castoro + Public Sans, forest/cream/sage, engraved plates).

- `static/content.js`: one entry per ad (copy, facts, layout type). `*word*` gives an italic accent and `[[word]]` a hand-drawn ring.
- `static/ads.html`: the layouts (symptoms, stat, price, photo, steps, ledger, venn, week, inbody, plate). Each one renders at 4:5 (1080×1350) and 9:16 (1080×1920).
- `python3 static/render.py [IDs]`: Playwright renders to `static/out/<meno|long>/` and writes `_sheet.jpg`. The render fails if text leaves the frame or, on 9:16, the Reels safe zone (top 269 / bottom 672 / sides 65 px).
- `static/COPY.md`: primary text, headlines, URLs and campaign setup, plus the compliance guardrails (Meta personal attributes, CNO testimonials and comparisons, verifiable claims, no Rx drug names).

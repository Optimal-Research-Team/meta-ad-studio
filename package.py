"""Package rendered video ads into labelled hand-off folders: META ADS (paid) and INSTAGRAM (organic).

    python3 package.py "<destination folder>"

Edit ROUND for each round. Captions come from the "### <ID> caption" sections in VIDEO-ADS.md, and that file
is copied in as the README.
"""
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FP = os.path.join(ROOT, "tools/node_modules/ffprobe-static/bin/darwin/arm64/ffprobe")

ROUND = [  # ID, title, output folder, spec NAME
    ("LV2", "Longevity - A full hour", "out/longevity-ad2", "LongevityFullHour"),
    ("MV1", "Menopause - I don't feel like myself", "out/menopause-ad1", "MenopauseMyself"),
]
CUTS = {"T": "Tight", "F": "Full"}


def dur(path):
    s = float(json.loads(subprocess.run([FP, "-v", "error", "-show_format", "-of", "json", path],
                                        capture_output=True, text=True).stdout)["format"]["duration"])
    return f"{int(s // 60)}m{int(round(s % 60)):02d}s"


def put(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print("  " + os.path.relpath(dst, DEST))


def ig_caption(ad_id):
    doc = open(os.path.join(ROOT, "VIDEO-ADS.md")).read()
    m = re.search(rf"### {ad_id} caption\n(.*?)(?=\n### |\n---|\Z)", doc, re.S)
    return m.group(1).strip() + "\n"


if __name__ == "__main__":
    DEST = sys.argv[1]
    os.makedirs(DEST, exist_ok=True)
    shutil.copy2(os.path.join(ROOT, "VIDEO-ADS.md"), os.path.join(DEST, "README - Meta ads + Instagram.md"))
    for ad_id, title, out, name in ROUND:
        meta = os.path.join(DEST, "META ADS", f"{ad_id} {title}")
        for k, cut in CUTS.items():
            v916 = os.path.join(ROOT, out, f"{name}_{cut}_9x16.mp4")
            if not os.path.exists(v916):
                continue
            label = f"META AD - {ad_id}-{k} - {title} - {cut} {dur(v916)}"
            put(os.path.join(ROOT, out, f"{name}_{cut}_4x5.mp4"), os.path.join(meta, f"{label} - 4x5 Feed.mp4"))
            put(v916, os.path.join(meta, f"{label} - 9x16 Stories+Reels.mp4"))
            for r in ("4x5", "9x16"):
                put(os.path.join(ROOT, out, f"{name}_{cut}_{r}_thumb.jpg"),
                    os.path.join(meta, f"META AD - {ad_id}-{k} - thumbnail {r}.jpg"))
            put(os.path.join(ROOT, out, f"{name}_{cut}.srt"), os.path.join(meta, f"META AD - {ad_id}-{k} - captions (optional).srt"))
        reel = os.path.join(ROOT, out, f"{name}_IG_Tight_9x16.mp4")
        if os.path.exists(reel):
            ig = os.path.join(DEST, "INSTAGRAM (organic)", f"IG REEL - {ad_id} {title}")
            put(reel, os.path.join(ig, f"IG REEL - {ad_id} - {title} - {dur(reel)}.mp4"))
            put(os.path.join(ROOT, out, f"{name}_IG_cover_9x16.jpg"), os.path.join(ig, f"IG REEL - {ad_id} - cover.jpg"))
            with open(os.path.join(ig, "caption.txt"), "w") as f:
                f.write(ig_caption(ad_id))
            print("  " + os.path.relpath(os.path.join(ig, "caption.txt"), DEST))

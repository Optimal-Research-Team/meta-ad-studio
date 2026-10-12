"""Apple Vision (on-device) helpers: largest face per frame, for zoom anchors and overlay clearance."""
import glob
import json
import os
import sys

import Quartz
import Vision
from Foundation import NSURL


def _cg(path):
    src = Quartz.CGImageSourceCreateWithURL(NSURL.fileURLWithPath_(path), None)
    return Quartz.CGImageSourceCreateImageAtIndex(src, 0, None)


def face(path):
    """Largest face as normalized (cx, cy, w, h), top-left origin; None if no face."""
    req = Vision.VNDetectFaceRectanglesRequest.alloc().init()
    Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(_cg(path), None).performRequests_error_([req], None)
    best = None
    for o in req.results() or []:
        b = o.boundingBox()
        if best is None or b.size.width * b.size.height > best[2] * best[3]:
            best = (b.origin.x + b.size.width / 2, 1 - b.origin.y - b.size.height / 2, b.size.width, b.size.height)
    return best


def faces(frames_dir, fps=2.0):
    rows = []
    for p in sorted(glob.glob(os.path.join(frames_dir, "f_*.jpg"))):
        n = int(os.path.basename(p)[2:6])
        f = face(p)
        rows.append({"t": round((n - 1) / fps, 2), "face": [round(v, 4) for v in f] if f else None})
    return rows


if __name__ == "__main__":
    out = faces(sys.argv[1])
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    for r in out[::4]:
        print(r)

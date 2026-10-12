"""On-screen text per frame (Apple Vision, on-device). Frames are fps=2 -> t = (n-1)/2. Prints text runs with time spans."""
import glob, json, os, sys
import Quartz, Vision
from Foundation import NSURL

def read(path):
    src = Quartz.CGImageSourceCreateWithURL(NSURL.fileURLWithPath_(path), None)
    img = Quartz.CGImageSourceCreateImageAtIndex(src, 0, None)
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLevel_(0); req.setUsesLanguageCorrection_(True)
    Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None).performRequests_error_([req], None)
    out = []
    for o in req.results() or []:
        c = o.topCandidates_(1)[0]
        if c.confidence() >= 0.5:
            b = o.boundingBox()  # normalized, origin bottom-left
            out.append({"text": c.string(), "conf": round(c.confidence(), 2), "y": round(1 - b.origin.y - b.size.height, 2)})
    return out

frames_dir, out_json, fps = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
rows = []
for p in sorted(glob.glob(os.path.join(frames_dir, "f_*.jpg"))):
    n = int(os.path.basename(p)[2:6])
    rows.append({"t": round((n - 1) / fps, 2), "items": read(p)})
json.dump(rows, open(out_json, "w"), indent=1)
spans = {}
for r in rows:
    for it in r["items"]:
        s = spans.setdefault(it["text"], [r["t"], r["t"], 0, it["y"]]); s[1] = r["t"]; s[2] += 1
for text, (a, b, n, y) in sorted(spans.items(), key=lambda kv: kv[1][0]):
    print(f"{a:5.1f}–{b:5.1f}s  ({n:2} frames, y={y:.2f})  {text!r}")

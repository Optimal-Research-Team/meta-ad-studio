"""Make an Instagram cut from a finished Meta cut by swapping only the end card (frames after `body`).
The two versions are identical until the end-card reveal, and so is the soundtrack."""
import os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import studio, adgfx as G

spec = studio.load_spec(sys.argv[1]); variant = sys.argv[2]
meta = f"{spec.OUT}/{spec.NAME}_{variant}_9x16.mp4"
studio.apply_channel(spec, "ig")
segs, body = studio.timeline(spec, variant)
nb, ne = round(body * studio.FPS), round(spec.END_DUR * studio.FPS)
bg, lay = G.endcard(G.W, G.H, 350, spec.END)
end = f"work/.{spec.NAME}_end.mp4"
enc = studio.encoder(end, G.W, G.H)
for k in range(ne):
    enc.stdin.write(G.endcard_frame(None, bg, lay, studio.XFADE_END + k / studio.FPS, studio.XFADE_END).tobytes())
enc.stdin.close(); enc.wait()
out = f"{spec.OUT}/{spec.NAME}_{variant}_9x16.mp4"
studio.run([studio.FF, "-y", "-v", "error", "-i", meta, "-i", end, "-filter_complex",
            f"[0:v]trim=end_frame={nb},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,format=yuv420p[v]",
            "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "copy",
            "-map_metadata", "-1", "-movflags", "+faststart", out])
print(f"{out}: {nb} body + {ne} end-card frames")
studio.qa(spec, f"{spec.NAME}_{variant}")

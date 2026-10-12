"""Word-level transcript of a clip's audio -> words.json + transcript.txt + .srt (faster-whisper, local)."""
import json, os, sys
from faster_whisper import WhisperModel

wav, outdir = sys.argv[1], sys.argv[2]
model = WhisperModel(os.environ.get("WHISPER_MODEL", "small.en"), device="cpu", compute_type="int8")
segs, info = model.transcribe(wav, word_timestamps=True, vad_filter=True, beam_size=5)
words, lines = [], []
for s in segs:
    lines.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
    words += [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2), "p": round(w.probability, 2)} for w in s.words]
json.dump({"segments": lines, "words": words}, open(f"{outdir}/words.json", "w"), indent=1)

def ts(t):
    return f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
with open(f"{outdir}/transcript.txt", "w") as f:
    for l in lines:
        f.write(f"[{l['start']:6.2f}–{l['end']:6.2f}] {l['text']}\n")
with open(f"{outdir}/transcript.srt", "w") as f:
    for i, l in enumerate(lines, 1):
        f.write(f"{i}\n{ts(l['start'])} --> {ts(l['end'])}\n{l['text']}\n\n")
print(open(f"{outdir}/transcript.txt").read())
low = [w for w in words if w["p"] < 0.6]
print("low-confidence words:", [(w["w"], w["s"]) for w in low])

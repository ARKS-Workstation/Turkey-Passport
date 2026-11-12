"""Split a Seedance clip's speech by line, convert each speaker segment to the real Cartesia voice, rebuild the
dialogue track (same length as the clip) and write caption timings.
Usage: vc_shot.py CLIP.mp4 OUT_PREFIX 'VOICE|line text' ['VOICE|line text' ...]"""
import json, re, subprocess, sys, wave, numpy as np
from pathlib import Path
SR = 44100
clip, prefix, specs = sys.argv[1], Path(sys.argv[2]), [s.split("|", 1) for s in sys.argv[3:]]
prefix.parent.mkdir(parents=True, exist_ok=True)
src = prefix.with_name(prefix.name + "_src.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vn", "-ac", "1", "-ar", str(SR), str(src)], check=True)
import os
if os.environ.get("VC_PRECLEAN"):  # de-reverb + denoise the animation audio before voice conversion
    subprocess.run(["python3", str(Path(__file__).with_name("clean_voice.py")), str(src), str(src) + ".clean.wav", "--pre"], check=True)
    os.replace(str(src) + ".clean.wav", src)
def curl_json(args): return json.loads(subprocess.run(["curl", "-sS", "-m", "120"] + args, capture_output=True, text=True).stdout)
H = ["-H", "X-API-Key: proxy-injected", "-H", "Cartesia-Version: 2025-04-16"]
stt = curl_json(["https://api.cartesia.ai/stt"] + H + ["-F", f"file=@{src}", "-F", "model=ink-whisper", "-F", "language=en", "-F", "timestamp_granularities[]=word"])
words = stt.get("words") or []
print("STT:", stt.get("text"))
def wc(t): return max(1, len(re.findall(r"[A-Za-z0-9']+", t)))
exp = np.cumsum([wc(t) for _, t in specs]); exp = exp / exp[-1]
n = len(words); bounds = [0]
for i in range(len(specs) - 1):
    e = int(round(exp[i] * n)); best, bs = None, -1e9
    for j in range(max(bounds[-1] + 1, e - 3), min(n, e + 4)):
        gap = words[j]["start"] - words[j - 1]["end"]; score = gap * 4 - abs(j - exp[i] * n) * 0.15
        if score > bs: best, bs = j, score
    bounds.append(best if best is not None else e)
bounds.append(n)
lines = []
for i, (voice, text) in enumerate(specs):
    ws = words[bounds[i]:bounds[i + 1]]
    lines.append({"idx": i, "voice": voice, "text": text, "start": ws[0]["start"], "end": ws[-1]["end"], "words": ws})
    print(f"line {i}: {ws[0]['start']:.2f}-{ws[-1]['end']:.2f}  {' '.join(w['word'].strip() for w in ws)}")
# merge consecutive same-voice lines into segments
segs = []
for ln in lines:
    if segs and segs[-1]["voice"] == ln["voice"]: segs[-1]["end"] = ln["end"]
    else: segs.append({"voice": ln["voice"], "start": ln["start"], "end": ln["end"]})
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
out = np.zeros(int(dur * SR) + SR)
def readwav(p):
    with wave.open(str(p)) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768, w.getframerate()
for k, s in enumerate(segs):
    a = max(0.0, s["start"] - 0.12); b = (segs[k + 1]["start"] - 0.06) if k + 1 < len(segs) else min(dur, s["end"] + 0.5)
    cut = prefix.with_name(f"{prefix.name}_seg{k}.wav"); vc = prefix.with_name(f"{prefix.name}_seg{k}_vc.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ss", f"{a:.3f}", "-to", f"{b:.3f}", str(cut)], check=True)
    r = subprocess.run(["curl", "-sS", "-m", "120", "-w", "%{http_code}", "-o", str(vc), "https://api.cartesia.ai/voice-changer/bytes"] + H +
                       ["-F", f"clip=@{cut}", "-F", f"voice[id]={s['voice']}", "-F", "output_format[container]=wav",
                        "-F", f"output_format[sample_rate]={SR}", "-F", "output_format[encoding]=pcm_s16le"], capture_output=True, text=True)
    if r.stdout.strip() != "200": sys.exit(f"voice changer failed on seg {k}: HTTP {r.stdout} {vc.read_text()[:200]}")
    x, sr = readwav(vc); assert sr == SR
    f = int(0.012 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    i = int(a * SR); out[i:i + len(x)] += x[:len(out) - i]
    print(f"seg {k}: {a:.2f}-{b:.2f}s -> {len(x)/SR:.2f}s converted")
out = out[:int(dur * SR)]
dlg = prefix.with_name(prefix.name + "_dialogue.wav")
with wave.open(str(dlg), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump({"duration": dur, "lines": lines}, open(prefix.with_name(prefix.name + "_lines.json"), "w"), indent=1)
print("dialogue:", dlg)

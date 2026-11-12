"""Fit clean Cartesia takes to Seedance lip timing using matched-word anchors (rubberband per word group).
Usage: align_words.py LINES.json OUT.wav CART_LINE1.wav [CART_LINE2.wav ...]"""
import json, re, subprocess, sys, wave, difflib, numpy as np
SR = 44100; lines = json.load(open(sys.argv[1])); out_path = sys.argv[2]; carts = sys.argv[3:]
H = ["-H", "X-API-Key: proxy-injected", "-H", "Cartesia-Version: 2025-04-16"]
def stt_words(p):
    r = subprocess.run(["curl", "-sS", "-m", "120", "https://api.cartesia.ai/stt"] + H + ["-F", f"file=@{p}", "-F", "model=ink-whisper", "-F", "language=en", "-F", "timestamp_granularities[]=word"], capture_output=True, text=True)
    return json.loads(r.stdout).get("words") or []
SYN = {"thru": "through", "through": "through", "18000": "18000", "eighteen": "18000", "gpts": "gpt"}
def norm(w): w = re.sub(r"[^a-z0-9]", "", w.lower()); return SYN.get(w, w)
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def stretch(x, f):
    if abs(f - 1) < 0.03: return x
    a, b = out_path + ".i.wav", out_path + ".o.wav"
    with wave.open(a, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", f"rubberband=tempo={1/f:.5f}:pitchq=quality:transients=smooth", b], check=True)
    return load(b)
out = np.zeros(int((lines["duration"] + 2) * SR)); rep = []
for li, ln in enumerate(lines["lines"]):
    sw = ln["words"]; cw = stt_words(carts[li]); cx = load(carts[li])
    sm = difflib.SequenceMatcher(a=[norm(w["word"]) for w in sw], b=[norm(w["word"]) for w in cw], autojunk=False)
    pairs = [(blk.a + k, blk.b + k) for blk in sm.get_matching_blocks() for k in range(blk.size)]
    anchors = [(sw[0]["start"], cw[0]["start"])]
    for i, j in pairs:
        s, c = sw[i]["start"], cw[j]["start"]
        if s - anchors[-1][0] >= 0.4 and c > anchors[-1][1] + 0.1: anchors.append((s, c))
    anchors.append((sw[-1]["end"] + 0.06, cw[-1]["end"] + 0.06))
    fs = []
    for (s0, c0), (s1, c1) in zip(anchors[:-1], anchors[1:]):
        f = max(0.7, min(1.45, (s1 - s0) / max(0.05, c1 - c0))); fs.append(f)
        pre = 0.04 if (s0, c0) == anchors[0] else 0.0
        seg = cx[int(max(0, c0 - pre) * SR):int(c1 * SR)]; y = stretch(seg, f).copy()
        fd = min(len(y) // 4, int(0.015 * SR)); y[:fd] *= np.linspace(0, 1, fd); y[-fd:] *= np.linspace(1, 0, fd)
        i0 = int(max(0, s0 - pre * f) * SR); out[i0:i0 + len(y)] += y[:len(out) - i0]
    rep.append(f"line {li}: {len(anchors)-1} segments, stretch {min(fs):.2f}-{max(fs):.2f}, matched {len(pairs)}/{len(sw)} words")
out = out[:int(lines["duration"] * SR)]
with wave.open(out_path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("\n".join(rep)); print("aligned:", out_path)

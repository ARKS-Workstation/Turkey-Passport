"""Re-record each line at the pace the lips need, then place it whole at the lip onset (uniform tiny stretch).
Usage: fit_lines.py LINES.json OUT.wav 'VOICE|EMOTION|tts text' ..."""
import json, re, subprocess, sys, wave, numpy as np
SR = 44100; L = json.load(open(sys.argv[1])); out_path = sys.argv[2]; specs = [s.split("|", 2) for s in sys.argv[3:]]
H = ["-H", "X-API-Key: proxy-injected", "-H", "Cartesia-Version: 2025-04-16"]
def stt(p):
    r = subprocess.run(["curl", "-sS", "-m", "120", "https://api.cartesia.ai/stt"] + H + ["-F", f"file=@{p}", "-F", "model=ink-whisper", "-F", "language=en", "-F", "timestamp_granularities[]=word"], capture_output=True, text=True)
    d = json.loads(r.stdout); return d.get("words") or [], d.get("text", "")
def tts(voice, emo, text, speed, path):
    body = {"model_id": "sonic-3", "transcript": text, "voice": {"mode": "id", "id": voice}, "language": "en",
            "output_format": {"container": "wav", "encoding": "pcm_s16le", "sample_rate": SR}, "generation_config": {"speed": round(speed, 3), "emotion": emo}}
    subprocess.run(["curl", "-sS", "-m", "120", "-o", path, "https://api.cartesia.ai/tts/bytes"] + H + ["-H", "Content-Type: application/json", "-d", json.dumps(body)], check=True)
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
out = np.zeros(int((L["duration"] + 2) * SR)); base = out_path.rsplit(".", 1)[0]
for li, (ln, (voice, emo, text)) in enumerate(zip(L["lines"], specs)):
    s0, s1 = ln["words"][0]["start"], ln["words"][-1]["end"]; target = s1 - s0; speed = 1.0; best = None
    for it in range(4):
        p = f"{base}_l{li}_t{it}.wav"; tts(voice, emo, text, speed, p); ws, txt = stt(p)
        if not ws: continue
        c0, c1 = ws[0]["start"], ws[-1]["end"]; ratio = (c1 - c0) / target
        if best is None or abs(ratio - 1) < abs(best[3] - 1): best = (p, c0, c1, ratio, speed, txt)
        print(f"line {li} try {it}: speed {speed:.2f} -> take {c1-c0:.2f}s vs lips {target:.2f}s (x{ratio:.2f}) | {txt}")
        if abs(ratio - 1) < 0.07: break
        speed = max(0.6, min(1.5, speed * ratio))
    p, c0, c1, ratio, speed, txt = best
    x = load(p)[int(max(0, c0 - 0.05) * SR):int((c1 + 0.12) * SR)]
    f = 1 / ratio
    if abs(f - 1) > 0.02:
        tmp = f"{base}_l{li}_cut.wav"
        with wave.open(tmp, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"rubberband=tempo={ratio:.5f}:pitchq=quality:transients=smooth", tmp + ".s.wav"], check=True)
        x = load(tmp + ".s.wav")
    fd = int(0.012 * SR); x = x.copy(); x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd)
    i0 = int(max(0, s0 - 0.05 * f) * SR); out[i0:i0 + len(x)] += x[:len(out) - i0]
    print(f"line {li}: placed at {s0:.2f}s, speed {speed:.2f}, final stretch x{f:.2f}")
out = out[:int(L["duration"] * SR)]
with wave.open(out_path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("fitted:", out_path)

"""Speech clean-up: WPE de-reverb -> RNNoise (voice model) -> spectral gate -> de-click/EQ/de-ess/expander/levelling.
Usage: clean_voice.py IN.wav OUT.wav [--pre]   (--pre = light pass for the voice-changer input, no EQ/levelling)"""
import subprocess, sys, wave, numpy as np, noisereduce as nr
from nara_wpe.wpe import wpe
from nara_wpe.utils import stft, istft
SR = 44100; src, dst = sys.argv[1], sys.argv[2]; pre = "--pre" in sys.argv
MODEL = "/tmp/claude-0/-home-user-Turkey-Passport/d3529a6e-19ac-5ab0-8b77-cde3464aacdb/scratchpad/ext/rnnoise-models/beguiling-drafter-2018-08-30/bd.rnnn"
def load(p, sr=SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def save(p, x, sr=SR):
    with wave.open(p, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
x = load(src); n = len(x)
# 1) de-reverb (WPE, single channel)
Y = stft(x[None, :], size=1024, shift=256)            # (1, T, F)
Z = wpe(Y.transpose(2, 0, 1), taps=24, delay=2, iterations=5, statistics_mode="full").transpose(1, 2, 0)
x = istft(Z, size=1024, shift=256)[0][:n]
t1, t2 = dst + ".wpe.wav", dst + ".rnn.wav"; save(t1, x)
# 2) neural noise suppression (RNNoise, voice + recording-noise model)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", t1, "-af", f"aresample=48000,arnndn=m={MODEL}:mix={0.7 if pre else 0.75},aresample={SR}", t2], check=True)
x = load(t2)[int(0.010 * SR):]; x = np.pad(x, (0, max(0, n - len(x))))[:n]  # compensate RNNoise latency
# 3) residual hiss: stationary spectral gating (gentle)
x = nr.reduce_noise(y=x, sr=SR, stationary=True, prop_decrease=0.4 if pre else 0.5, n_fft=2048)
save(t1, x)
if pre:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", t1, "-af", "highpass=f=70,lowpass=f=12000", dst], check=True)
else:
    # 4) unwanted elements + voice enhancement
    chain = ("adeclick=w=55:o=75,highpass=f=85,lowpass=f=14500,"
             "equalizer=f=220:t=q:w=1.1:g=-2.5,equalizer=f=3800:t=q:w=1.0:g=2.2,highshelf=f=9500:g=1.5,"
             "deesser=i=0.35:m=0.5:f=0.5,"
                          "acompressor=threshold=-20dB:ratio=2.2:attack=8:release=140:knee=4:makeup=2")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", t1, "-af", chain, dst], check=True)
for t in (t1, t2):
    import os; os.remove(t)
print("cleaned:", dst)

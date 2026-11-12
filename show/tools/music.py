"""Original, license-free trailer bed: 120 BPM cinematic electronic. Usage: music.py OUT TOTAL TITLE_HIT END_HIT"""
import sys, numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve
SR = 44100; rng = np.random.default_rng(7)
out, TOTAL, HIT, END = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
BPM = 120; BEAT = 60 / BPM; N = int(TOTAL * SR)
L = np.zeros(N); R = np.zeros(N)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def put(sig, t, gl=1.0, gr=None):
    i = int(t * SR); 
    if i >= N: return
    s = sig[:N - i]; L[i:i+len(s)] += s * gl; R[i:i+len(s)] += s * (gl if gr is None else gr)
def env(n, a, d):
    t = np.arange(n) / SR; e = np.exp(-t / d); k = int(a * SR)
    if k: e[:k] *= np.linspace(0, 1, k)
    return e
def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR; f = 45 + 95 * np.exp(-t / 0.03)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.18); s[:200] += rng.normal(0, .3, 200) * np.linspace(1, 0, 200); return s
def clap():
    n = int(0.25 * SR); s = np.zeros(n); x = bp(rng.normal(0, 1, n), 900, 4000)
    for o in (0, .011, .022): k = int(o * SR); s[k:] += x[:n-k] * env(n - k, 0, .012 if o < .02 else .09)
    return s * .5
def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR); return hp(rng.normal(0, 1, n), 7000) * env(n, 0, .06 if open_ else .012) * .12
def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR; ph = (freq * (1 + detune)) * t + rng.random(); return 2 * (ph % 1) - 1
def note(m): return 440 * 2 ** ((m - 69) / 12)
# Am - F - C - G (2 bars each = 4 s)
chords = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [48, 52, 55]), (55, [55, 59, 62])]
# --- hook section: low drone + ticks (0 .. HIT)
n = int(HIT * SR); t = np.arange(n) / SR
drone = (saw(55, n) * .5 + saw(55, n, .004) * .5); drone = lp(drone, 220) * np.minimum(1, t / 1.0) * .22
put(drone, 0)
for k in np.arange(0, HIT - .5, BEAT / 2): put(hat() * .6, k, .7, .5)
# riser into the title hit
rl = 2.6; n = int(rl * SR); t = np.arange(n) / SR; nz = rng.normal(0, 1, n)
riser = np.zeros(n); 
for i, (a, b) in enumerate(np.linspace([300, 900], [3000, 9000], 8)):
    seg = slice(i * n // 8, (i + 1) * n // 8); riser[seg] = bp(nz, a, b)[seg]
sweep = np.sin(2 * np.pi * np.cumsum(200 * 2 ** (3 * t / rl)) / SR) * .15
riser = (riser * .35 + sweep) * (t / rl) ** 2
put(riser, HIT - rl, .9, 1.0)
# impacts
def impact(length=2.8):
    n = int(length * SR); t = np.arange(n) / SR; f = 32 + 40 * np.exp(-t / .08)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .9)
    crash = lp(rng.normal(0, 1, n), 3500) * env(n, .001, .35) * .4
    ir = rng.normal(0, 1, int(1.6 * SR)) * np.exp(-np.arange(int(1.6 * SR)) / SR / .45)
    tail = fftconvolve(crash, ir)[:n] * .03
    return sub * .9 + crash + tail
put(impact(), HIT); put(impact(3.5), END)
# --- groove from HIT to END-2
g0, g1 = HIT, END - 2 * BEAT
pad_ir = rng.normal(0, 1, int(1.2 * SR)) * np.exp(-np.arange(int(1.2 * SR)) / SR / .35)
tb = g0; bar = 0
while tb < g1:
    root, tones = chords[(bar // 2) % 4]
    for b in range(4):  # beats in bar
        tk = tb + b * BEAT
        if tk >= g1: break
        put(kick() * .9, tk)
        if b in (1, 3): put(clap(), tk, .8, .9)
        for s16 in range(4):
            th = tk + s16 * BEAT / 4
            if th < g1: put(hat(open_=(s16 == 2)), th, .45 if s16 % 2 else .6, .6 if s16 % 2 else .45)
        # bass: 8th notes, root (octave 1-2)
        for e8 in range(2):
            n8 = int(BEAT / 2 * SR); bs = lp(saw(note(root - 24), n8) + .5 * np.sin(2 * np.pi * note(root - 24) * np.arange(n8) / SR), 380) * env(n8, .004, .2) * .38
            put(bs, tk + e8 * BEAT / 2)
        # arp: 16ths over chord tones
        for s16 in range(4):
            m = tones[(b * 4 + s16) % 3] + 12; n16 = int(BEAT / 4 * SR * 1.6)
            pl = lp(saw(note(m), n16) + saw(note(m), n16, .006), 2600) * env(n16, .002, .07) * .15
            put(pl, tk + s16 * BEAT / 4, .6 + .4 * (s16 % 2), 1 - .4 * (s16 % 2))
            put(pl * .35, tk + s16 * BEAT / 4 + .375, 1 - .4 * (s16 % 2), .6 + .4 * (s16 % 2))  # dotted-8th echo
    # pad per bar
    nb = int(4 * BEAT * SR); padL = sum(saw(note(m), nb, -.005) for m in tones); padR = sum(saw(note(m), nb, .005) for m in tones)
    shp = np.minimum(1, np.arange(nb) / SR / .4) * np.minimum(1, (nb - np.arange(nb)) / SR / .3)
    put(lp(padL, 1400) * shp * .07, tb, 1, 0); put(lp(padR, 1400) * shp * .07, tb, 0, 1)
    tb += 4 * BEAT; bar += 1
# sidechain duck on the groove (pumping) except drums are already in; gentle global pump
pump = np.ones(N)
for tk in np.arange(g0, g1, BEAT):
    i = int(tk * SR); k = min(N - i, int(.3 * SR)); pump[i:i+k] *= 1 - .35 * np.exp(-np.arange(k) / SR / .08)
L *= pump; R *= pump
# light room reverb
ir = lp(rng.normal(0, 1, int(1.0 * SR)), 5000) * np.exp(-np.arange(int(1.0 * SR)) / SR / .25) * .03
L = L + fftconvolve(L, ir)[:N]; R = R + fftconvolve(R, ir[::-1].copy())[:N]
# fade out after END hit
fo = np.ones(N); fs = int((END + 0.2) * SR); fo[fs:] = np.linspace(1, 0, N - fs) if N > fs else 1
L *= fo; R *= fo
st = np.stack([L, R], 1); st /= np.abs(st).max() / 0.89
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("music:", out, f"{TOTAL}s hit@{HIT} end@{END}")

"""Assemble the ARKS Sharks trailer from a plan JSON. Usage: assemble.py PLAN.json OUT.mp4"""
import json, math, re, subprocess, sys, wave, numpy as np
from pathlib import Path
plan = json.load(open(sys.argv[1])); OUT = Path(sys.argv[2]); W = Path(plan["work"]); W.mkdir(parents=True, exist_ok=True)
SR, FPS = 44100, 24
def run(*a): subprocess.run([str(x) for x in a], check=True)
def ff(*a): run("ffmpeg", "-v", "error", "-y", *a)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
VF = "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=contrast=1.04:saturation=1.06,setsar=1,fps=24,format=yuv420p"
t0 = 0.0; vparts, dparts, sparts, events = [], [], [], []
for i, s in enumerate(plan["shots"]):
    a, b = s["in"], s["out"]; d = round((b - a) * FPS) / FPS
    v = W / f"v{i}.mp4"; vf = (f"setpts=PTS*{s['speed']}," if s.get("speed") else "") + VF
    ff("-ss", a, "-i", s["clip"], "-t", d, "-an", "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "16", v)
    ad = s.get("dialogue_in", a)
    def audio_slice(src, dst, gain=1.0):
        if src: ff("-ss", ad if src == s.get("dialogue") else a, "-i", src, "-t", d, "-ac", "1", "-ar", SR, "-af", f"apad,atrim=0:{d},volume={gain}", dst)
        else: ff("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", d, dst)
    dp, sp = W / f"d{i}.wav", W / f"s{i}.wav"
    audio_slice(s.get("dialogue"), dp); audio_slice(s.get("sfx"), sp, s.get("sfx_gain", 1.0))
    vparts.append(v); dparts.append(dp); sparts.append(sp)
    for ln in (json.load(open(s["lines"]))["lines"] if s.get("lines") else []):
        words = ln["words"]; disp = s["display"][ln["idx"]] if "display" in s else ln["text"]
        toks = disp.split(); nw, ns = len(toks), len(words); size = 3 if nw > 4 else nw
        chunks = [toks[k:k + size] for k in range(0, nw, size)]
        k0 = 0
        for c in chunks:
            k1 = k0 + len(c); ws = words[min(ns - 1, math.floor(k0 * ns / nw))]; we = words[min(ns - 1, max(0, math.ceil(k1 * ns / nw) - 1))]
            st, en = ws["start"] - ad + t0, we["end"] - ad + t0
            if en > t0 and st < t0 + d: events.append((max(st, t0), min(en + 0.15, t0 + d), " ".join(c), ln.get("who")))
            k0 = k1
    s["t0"] = t0; t0 += d
for k in range(len(events) - 1):  # hold each caption until the next one (no flicker)
    if events[k + 1][0] - events[k][1] < 0.35: events[k] = (events[k][0], events[k + 1][0], *events[k][2:])
TOTAL_MAIN = t0
# --- end card
ec = plan.get("endcard") or {"dur": 0}; ecv = W / "endcard.mp4"; logo = plan["logo"]
if ec["dur"] > 0: ff("-loop", "1", "-t", ec["dur"], "-i", ec["bg"], "-loop", "1", "-t", ec["dur"], "-i", logo,
   "-filter_complex", f"[0:v]scale=1080:1920,boxblur=18:2,eq=brightness=-0.32:saturation=0.8,format=yuv420p[bg];"
   f"[1:v]scale=900:-1,format=rgba,fade=in:st=0.15:d=0.5:alpha=1[lg];[bg][lg]overlay=(W-w)/2:620,fps=24,format=yuv420p",
   "-c:v", "libx264", "-crf", "16", ecv)
if ec["dur"] > 0: vparts.append(ecv); dparts.append(None); sparts.append(None)
TOTAL = TOTAL_MAIN + ec["dur"]
# --- concat video
lst = W / "v.txt"; lst.write_text("".join(f"file '{p}'\n" for p in vparts)); vall = W / "video_all.mp4"
ff("-f", "concat", "-safe", 0, "-i", lst, "-c", "copy", vall)
def cat_audio(parts, dst):
    xs = []
    for p in parts:
        if p is None: xs.append(np.zeros(int(ec["dur"] * SR))); continue
        with wave.open(str(p)) as w: xs.append(np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768)
    x = np.concatenate(xs)
    with wave.open(str(dst), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
dall, sall = W / "dialogue_all.wav", W / "sfx_all.wav"; cat_audio(dparts, dall); cat_audio(sparts, sall)
# --- music
HIT = plan["shots"][plan["title_shot"]]["t0"] + plan["title_hit_offset"] if plan.get("title_shot") is not None else 0.0
mus = W / "music.wav"
run("python3", plan["music_script"], mus, f"{TOTAL + 0.5:.2f}", f"{HIT:.2f}", f"{TOTAL_MAIN + 0.05:.2f}", *( ["bed"] if plan.get("music_mode") == "bed" else []))
# --- ASS overlays
def ts(t): t = max(0, t); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
CY = "&H00FFE500&"; KEY = set(plan.get("key_words", []))
def colorize(txt): return " ".join(("{\\c" + CY + "}" + w + "{\\c&H00FFFFFF&}") if re.sub(r"[^A-Z0-9,]", "", w.upper()) in KEY else w for w in txt.split())
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Cap,Inter Display Black,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,6,3,2,90,90,470,1",
       "Style: Hook,Inter Display Black,64,&H00000000,&H00000000,&H00FFE500,&H00FFE500,0,0,0,0,100,100,2,0,3,18,0,8,80,80,250,1",
       "Style: Name,Inter Display ExtraBold,46,&H00FFFFFF,&H00FFFFFF,&H00402010,&H00402010,0,0,0,0,100,100,3,0,3,12,0,1,0,0,0,1",
       "Style: Tag,Inter Display Black,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,6,0,1,4,2,8,60,60,0,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for st, en, txt, who in events:
    ass.append(f"Dialogue: 1,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\fad(40,40)\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{colorize(txt.upper())}")
for o in plan.get("overlays", []):
    sh = plan["shots"][o["shot"]]; st = sh["t0"] + o["start"]; en = sh["t0"] + o["end"]
    pos = f"\\pos({o['x']},{o['y']})" if "x" in o else ""
    ass.append(f"Dialogue: 2,{ts(st)},{ts(en)},{o['style']},,0,0,0,,{{\\fad(120,150){pos}}}{o['text']}")
for o in ec.get("texts", []):
    ass.append(f"Dialogue: 2,{ts(TOTAL_MAIN + o['start'])},{ts(TOTAL)},Tag,,0,0,0,,{{\\fad(300,0)\\pos(540,{o['y']})}}{o['text']}")
assf = W / "overlay.ass"; assf.write_text("\n".join(ass) + "\n")
# --- side widgets: slide + fade in, hold, fade out
wl = plan.get("widgets", [])
if wl:
    inputs, fc, last = [], [], "[0:v]"
    for k, w in enumerate(wl):
        st = plan["shots"][w["shot"]]["t0"] + w["start"]; en = plan["shots"][w["shot"]].get("t0", 0) + w["end"] if "shot_end" not in w else plan["shots"][w["shot_end"]]["t0"] + w["end"]
        inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", w["png"]]
        sc = plan.get("widget_width", 900)
        fc.append(f"[{k+1}:v]format=rgba,scale={sc}:-2,fade=in:st={st:.3f}:d=0.22:alpha=1,fade=out:st={en-0.2:.3f}:d=0.2:alpha=1[w{k}]")
        y0 = plan.get("widget_y", 70)
        fc.append(f"{last}[w{k}]overlay=x=(W-w)/2:y='{y0}+36*max(0\\,1-(t-{st:.3f})/0.3)':enable='between(t,{st:.3f},{en:.3f})'[v{k}]"); last = f"[v{k}]"
    vw = W / "video_widgets.mp4"
    ff("-i", vall, *inputs, "-filter_complex", ";".join(fc), "-map", last, "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", vw)
    vall = vw
# --- title logo slam on the title shot
lg_t = HIT
if plan.get("title_shot") is None:
    plan["title_shot"] = 0; plan["title_logo_out_offset"] = -1.0; lg_t = -10.0
plan["title_logo_out"] = plan["shots"][plan["title_shot"]]["t0"] + plan["title_logo_out_offset"]; vfin = W / "video_titled.mp4"
ff("-i", vall, "-loop", "1", "-t", TOTAL, "-i", logo, "-filter_complex",
   f"[1:v]format=rgba,scale=w='trunc(880*(1+0.5*exp(-max(0\,t-{lg_t:.3f})*9))/2)*2':h=-2:eval=frame,"
   f"fade=in:st={lg_t:.3f}:d=0.12:alpha=1,fade=out:st={plan['title_logo_out']:.3f}:d=0.25:alpha=1[lg];"
   f"[0:v][lg]overlay=x=(W-w)/2:y=(H-h)/2-260:enable='between(t,{lg_t:.3f},{plan['title_logo_out']+0.3:.3f})',"
   f"ass={assf}:fontsdir=/usr/share/fonts/opentype/inter,format=yuv420p",
   "-c:v", "libx264", "-preset", "medium", "-crf", "17", vfin)
# --- mix: dialogue + sfx + ducked music, -14 LUFS
mix = W / "mix.wav"
ff("-i", dall, "-i", sall, "-i", mus, "-filter_complex",
   "[0:a]volume=1.25,asplit=2[d][key];"
   "[2:a]volume=0.42[m];[m][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
   "[1:a]volume=0.8[s];[d][s][md]amix=inputs=3:normalize=0:duration=longest,loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.7dB,alimiter=limit=0.84:level=false",
   "-ar", SR, "-ac", 2, mix)
ff("-i", vfin, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT)
print("OUT", OUT, f"{dur(OUT):.2f}s", "| title hit", f"{HIT:.2f}", "| main", f"{TOTAL_MAIN:.2f}")
json.dump({"t0": [s["t0"] for s in plan["shots"]], "events": events}, open(W / "timeline.json", "w"), indent=1)

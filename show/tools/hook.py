"""ARKS Sharks 2.5 s hook (no opener): the strongest line of the video, cut from an existing clip, with a headline tag,
small logo and word-timed captions, then a sound-logo hit as it cuts into the main video.
Usage (from the repo root):
  python3 show/tools/hook.py --clip CLIP.mp4 --start S --dur 2.5 --dialogue CLEAN.wav --lines LINES.json --line 2 \
      --display "Habibi, you'd argue with the car!" --tag "WOULD YOU RIDE A DRIVERLESS TAXI?" --then MAIN.mp4 --out OUT.mp4
--dialogue / --lines are the voice-swapped, cleaned track and its line timings for --clip (same timebase as the clip)."""
import argparse, json, math, re, subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--clip", required=True); ap.add_argument("--start", type=float, required=True); ap.add_argument("--dur", type=float, default=2.5)
ap.add_argument("--dialogue", required=True); ap.add_argument("--lines", required=True); ap.add_argument("--line", type=int, required=True)
ap.add_argument("--display", required=True); ap.add_argument("--tag", required=True); ap.add_argument("--then", required=True)
ap.add_argument("--out", required=True); ap.add_argument("--keywords", default="AI,DUBAI,ARKS,SHARKS,TAXI,CAR,HABIBI,2030")
a = ap.parse_args()
ROOT = Path(__file__).resolve().parents[2]; W = (ROOT / "show/_work/hook").resolve(); W.mkdir(parents=True, exist_ok=True)
LOGO = ROOT / "show/brand/arks_sharks_logo_shadow.png"
def ff(*x): subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, x)], check=True)
def ts(t): t = max(0, t); return f"0:{int(t // 60):02d}:{t % 60:05.2f}"

# captions for the hook line (script text, timed to the clip's words), max 3 words per chunk
words = json.load(open(a.lines))["lines"][a.line]["words"]; toks = a.display.split(); nw, ns = len(toks), len(words)
size = 3 if nw > 4 else nw; KEY = set(a.keywords.upper().split(","))
def colour(t): return " ".join(("{\\c&H00FFE500&}" + w + "{\\c&H00FFFFFF&}") if re.sub(r"[^A-Z0-9,]", "", w.upper()).strip(",") in KEY else w for w in t.split())
ev, k0 = [], 0
for k in range(0, nw, size):
    c = toks[k:k + size]; k1 = k0 + len(c)
    st = words[min(ns - 1, math.floor(k0 * ns / nw))]["start"] - a.start; en = words[min(ns - 1, max(0, math.ceil(k1 * ns / nw) - 1))]["end"] - a.start
    ev.append([max(0, st), min(a.dur, en + 0.15), " ".join(c)]); k0 = k1
for i in range(len(ev) - 1): ev[i][1] = ev[i + 1][0]
ev[-1][1] = a.dur
ass = W / "hook.ass"
ass.write_text("\n".join([
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Cap,Inter Display Black,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,6,3,2,90,90,470,1",
    "Style: Hook,Inter Display Black,58,&H00000000,&H00000000,&H00FFE500,&H00FFE500,0,0,0,0,100,100,2,0,3,18,0,8,70,70,330,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    f"Dialogue: 2,{ts(0)},{ts(a.dur)},Hook,,0,0,0,,{{\\fad(0,120)\\fscx94\\fscy94\\t(0,120,\\fscx100\\fscy100)}}{a.tag.upper()}"]
    + [f"Dialogue: 1,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\fad(40,40)\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{colour(t.upper())}" for s, e, t in ev]) + "\n")

# hook video: clip segment, upscaled, small logo at the top, tag + captions; dialogue from the cleaned track
hook = W / "hook.mp4"
ff("-ss", a.start, "-t", a.dur, "-i", a.clip, "-ss", a.start, "-t", a.dur, "-i", a.dialogue, "-loop", "1", "-t", a.dur, "-i", LOGO, "-filter_complex",
   "[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=contrast=1.04:saturation=1.06,fps=24,setsar=1[bg];"
   "[2:v]format=rgba,scale=380:-2[lg];[bg][lg]overlay=x=(W-w)/2:y=50[v1];"
   f"[v1]ass={ass}:fontsdir=/usr/share/fonts/opentype/inter,format=yuv420p[v];"
   f"[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{a.dur},volume=1.25[a]",
   "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-c:a", "pcm_s16le", W / "hook.mkv")

# join hook + main video, add the sound-logo hit at the cut, master to -14 LUFS
sting = W / "sting.wav"; subprocess.run(["python3", str(ROOT / "show/tools/sting.py"), str(sting), "2.6", "0.35"], check=True)
hit = a.dur - 0.35
ff("-i", W / "hook.mkv", "-i", a.then, "-i", sting, "-filter_complex",
   "[1:v]scale=1080:1920,fps=24,setsar=1,format=yuv420p[mv];[0:v][0:a][mv][1:a]concat=n=2:v=1:a=1[v][a0];"
   f"[2:a]adelay={int(hit * 1000)}|{int(hit * 1000)},volume=0.55[st];[a0][st]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5[a]",
   "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-pix_fmt", "yuv420p",
   "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", a.out)
print("hook video:", a.out)

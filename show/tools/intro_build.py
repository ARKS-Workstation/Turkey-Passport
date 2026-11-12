"""ARKS Sharks episode intro: Seedance plate + logo reveal + sonic logo. Usage: intro_build.py PLATE.mp4 LOGO.png LOGO_T OUT.mp4"""
import subprocess, sys
from pathlib import Path
plate, logo, LT, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), Path(sys.argv[4]); W = out.parent / "_work"; W.mkdir(parents=True, exist_ok=True)
def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)
PD = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", plate], capture_output=True, text=True).stdout)
HOLD = 1.6; TOTAL = PD + HOLD
sting = W / "sting.wav"
subprocess.run(["python3", str(Path(__file__).with_name("sting.py")), str(sting), f"{TOTAL:.2f}", f"{LT:.2f}"], check=True)
ff("-i", plate, "-loop", "1", "-t", TOTAL, "-i", logo, "-i", sting, "-filter_complex",
   f"[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=contrast=1.04:saturation=1.06,fps=24,tpad=stop_mode=clone:stop_duration={HOLD},setsar=1[bg];"
   f"[1:v]format=rgba,scale=w='trunc(900*(1+0.35*exp(-(t-{LT:.3f})*7))/2)*2':h=-2:eval=frame,fade=in:st={LT:.3f}:d=0.25:alpha=1[lg];"
   f"[bg][lg]overlay=x=(W-w)/2:y=(H-h)/2-330:enable='gte(t,{LT:.3f})',fade=out:st={TOTAL-0.35:.3f}:d=0.35,format=yuv420p[v];"
   f"[0:a]apad,atrim=0:{TOTAL:.3f},volume=0.55[sfx];[2:a]volume=0.9[st];[sfx][st]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,afade=t=out:st={TOTAL-0.4:.3f}:d=0.4[a]",
   "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", out)
print("intro:", out, f"{TOTAL:.2f}s logo@{LT}")

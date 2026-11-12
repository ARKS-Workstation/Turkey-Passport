"""Final delivery pass: measure loudness, correct to -14 LUFS (true peak safe) and encode CRF 20 for posting.
Usage: finalize.py IN.mp4 OUT.mp4"""
import re, subprocess, sys
src, dst = sys.argv[1], sys.argv[2]
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]); gain = round(-14 - I, 2)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                "-af", f"volume={gain}dB,alimiter=limit=0.85:level=false", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                "-movflags", "+faststart", dst], check=True)
print(f"{src}: {I} LUFS -> gain {gain} dB -> {dst}")

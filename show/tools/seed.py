"""Seedance reference-to-video on ModelArk: local images/audio as base64 data URIs, poll, download, frames."""
import argparse, base64, json, subprocess, sys, time, importlib.util
from pathlib import Path
S = "/root/.claude/skills/synced/3b0eece3-fd12-43ee-866a-2402a8892024_d739a2fa-97f6-4152-aee6-295e2c60db28/modelark/scripts/ark.py"
spec = importlib.util.spec_from_file_location("ark", S); ark = importlib.util.module_from_spec(spec); spec.loader.exec_module(ark)
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".mp3": "audio/mpeg", ".wav": "audio/wav"}
def durl(p):
    p = Path(p); return f"data:{MIME[p.suffix.lower()]};base64," + base64.b64encode(p.read_bytes()).decode()
ap = argparse.ArgumentParser()
ap.add_argument("prompt_file"); ap.add_argument("--images", nargs="*", default=[]); ap.add_argument("--audios", nargs="*", default=[])
ap.add_argument("--first-frame"); ap.add_argument("--model", default="dreamina-seedance-2-5-260628")
ap.add_argument("--duration", type=int, default=5); ap.add_argument("--ratio", default="9:16"); ap.add_argument("--resolution", default="720p")
ap.add_argument("--no-audio", action="store_true"); ap.add_argument("--seed", type=int); ap.add_argument("--out", required=True)
a = ap.parse_args()
content = [{"type": "text", "text": Path(a.prompt_file).read_text().strip()}]
if a.first_frame: content.append({"type": "image_url", "image_url": {"url": durl(a.first_frame)}, "role": "first_frame"})
content += [{"type": "image_url", "image_url": {"url": durl(i)}, "role": "reference_image"} for i in a.images]
content += [{"type": "audio_url", "audio_url": {"url": durl(x)}, "role": "reference_audio"} for x in a.audios]
body = {"model": a.model, "content": content, "duration": a.duration, "ratio": a.ratio, "resolution": a.resolution,
        "generate_audio": not a.no_audio, "watermark": False}
if a.seed is not None: body["seed"] = a.seed
t0 = time.time(); task = ark.call("contents/generations/tasks", "POST", body, timeout=300)
tid = task["id"]; print("task  :", tid, flush=True)
task = ark.wait_for(tid, budget=1500)
print("status:", task.get("status"), "| model:", task.get("model"), "| tokens:", (task.get("usage") or {}).get("total_tokens"),
      "| seed:", task.get("seed"), "| dur:", task.get("duration"), "| res:", task.get("resolution"), "| ratio:", task.get("ratio"), f"| {time.time()-t0:.0f}s")
if task.get("status") != "succeeded": print("error :", task.get("error")); sys.exit(1)
out = Path(a.out); ark.download(task["content"]["video_url"], out); print("saved :", out)
fd = out.parent / (out.stem + "_frames"); fd.mkdir(exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(out),"-vf","fps=1.5,scale=270:-1,tile=6x2",str(fd/"sheet.jpg")])
print("sheet :", fd/"sheet.jpg")

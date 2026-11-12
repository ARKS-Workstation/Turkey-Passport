"""Seedream generation with local reference images (sent as base64 data URLs)."""
import argparse, base64, json, sys, importlib.util
from pathlib import Path
S = "/root/.claude/skills/synced/3b0eece3-fd12-43ee-866a-2402a8892024_d739a2fa-97f6-4152-aee6-295e2c60db28/modelark/scripts/ark.py"
spec = importlib.util.spec_from_file_location("ark", S); ark = importlib.util.module_from_spec(spec); spec.loader.exec_module(ark)

def data_url(p):
    p = Path(p); mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

ap = argparse.ArgumentParser()
ap.add_argument("prompt_file"); ap.add_argument("--refs", nargs="*", default=[])
ap.add_argument("--size", default="2K"); ap.add_argument("--model", default="seedream-5-0-260128")
ap.add_argument("--seed", type=int); ap.add_argument("--out", required=True)
a = ap.parse_args()
body = {"model": a.model, "prompt": Path(a.prompt_file).read_text().strip(), "size": a.size,
        "response_format": "url", "watermark": False, "sequential_image_generation": "disabled"}
if a.refs: body["image"] = [data_url(r) for r in a.refs] if len(a.refs) > 1 else data_url(a.refs[0])
if a.seed is not None: body["seed"] = a.seed
data = ark.call("images/generations", "POST", body, timeout=300)
print("model :", data.get("model"), "| tokens:", data.get("usage", {}).get("total_tokens"))
for item in data.get("data", []):
    if item.get("url"):
        ark.download(item["url"], Path(a.out)); print("saved :", a.out)
    else:
        print("item  :", json.dumps(item)[:300])

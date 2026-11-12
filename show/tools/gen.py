"""Seedream generation with local reference images (sent as base64 data URLs)."""
import argparse, base64, json, sys, importlib.util
from pathlib import Path
import glob, os
def _ark_path():
    """Locate the ModelArk skill's ark.py (env ARK_PY overrides)."""
    if os.environ.get("ARK_PY"): return os.environ["ARK_PY"]
    hits = sorted(glob.glob(os.path.expanduser("~/.claude/skills/**/modelark/scripts/ark.py"), recursive=True))
    if not hits: raise SystemExit("ModelArk skill not found: set ARK_PY=/path/to/ark.py")
    return hits[0]
S = _ark_path()
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

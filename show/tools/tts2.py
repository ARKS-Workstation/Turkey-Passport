import json, sys, urllib.request, urllib.error
voice, text, out = sys.argv[1], sys.argv[2], sys.argv[3]
emotion = sys.argv[4] if len(sys.argv) > 4 else None
speed = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
def call(body):
    req = urllib.request.Request("https://api.cartesia.ai/tts/bytes", data=json.dumps(body).encode(), method="POST")
    for k, v in {"X-API-Key": "proxy-injected", "Cartesia-Version": "2025-04-16", "Content-Type": "application/json"}.items(): req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=120) as r: return r.read()
body = {"model_id": "sonic-3", "transcript": text, "voice": {"mode": "id", "id": voice}, "language": "en",
        "output_format": {"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100}}
gc = {"speed": speed}
if emotion: gc["emotion"] = emotion
try:
    data = call({**body, "generation_config": gc}); note = f"gen_config={gc}"
except urllib.error.HTTPError as e:
    print("gen_config rejected:", e.code, e.read().decode()[:200]); data = call(body); note = "plain"
open(out, "wb").write(data); print("saved", out, note)

"""Render each script line to its own wav with Kokoro (hf_beta) so scenes can be timed exactly."""
import sys, json, os
import soundfile as sf
from kokoro_onnx import Kokoro
sys.path.insert(0, os.path.dirname(__file__))
from autolayout_script import SCRIPT
M = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
OUT = sys.argv[1]
k = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
meta = []
for i, (key, spoken, cap) in enumerate(SCRIPT):
    s, sr = k.create(spoken, voice="hf_beta", speed=1.05, lang="hi")
    p = f"{OUT}/{i:02d}_{key}.wav"; sf.write(p, s, sr)
    meta.append({"i": i, "key": key, "wav": p, "dur": len(s)/sr})
    print(f"{i:02d} {key:22s} {len(s)/sr:5.1f}s", flush=True)
json.dump(meta, open(f"{OUT}/meta.json", "w"), indent=1)
print("TOTAL", round(sum(m["dur"] for m in meta)/60, 2), "min")

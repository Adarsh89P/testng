"""Generate a NEW voice-over for a day's script, offline, in the approved reference voice (docs/voice_workflow.md).

The reference recording is declared in assets/voice/reference.json:
  {"file": "assets/voice/reference/<name>.wav", "owner": "...", "rights": "own voice" | "licensed for cloning"}
Refused as a reference: anything byte-identical to a registered day's voice-over (e.g. the Day 04 Tisha K master,
which is a third-party licensed ElevenLabs voice: kept only as a style/consistency reference, never cloned or reused).
"""
import json, os, subprocess, tempfile
import numpy as np, soundfile as sf
import engine, voice_check

REF_CFG = os.path.join(voice_check.ROOT, "assets", "voice", "reference.json")
VENV_PY = "/home/user/venv-tts/bin/python"
CLONE = os.path.join(voice_check.ROOT, "tools", "voice_clone.py")
GAP = 1.2                                   # silence between lines, so the render can split automatically


class RefError(Exception):
    pass


def reference():
    if not os.path.exists(REF_CFG):
        raise RefError("no reference voice configured (assets/voice/reference.json). Record ~30-60 s of your own voice "
                       "and declare it there; see docs/voice_workflow.md")
    cfg = json.load(open(REF_CFG))
    path = os.path.join(voice_check.ROOT, cfg["file"])
    if not os.path.exists(path): raise RefError(f"reference file missing: {cfg['file']}")
    if cfg.get("rights") not in ("own voice", "licensed for cloning"):
        raise RefError("reference.json must state rights: 'own voice' or 'licensed for cloning'")
    h = voice_check.sha256(path)
    for k, e in voice_check.load_registry().items():
        if e.get("sha256") == h:
            raise RefError(f"the reference is the {k} voice-over ({e['topic']}); a day's recording can't be the clone reference")
    return path, cfg, h


def generate(day, scenes, out=None):
    ref, cfg, h = reference()
    out = out or os.path.join(voice_check.ROOT, "assets", "voice", f"day{day:02d}", "full.wav")
    if os.path.exists(out): raise RefError(f"{out} already exists; not overwriting")
    d = tempfile.mkdtemp(); js = os.path.join(d, "lines.json")
    texts = [s.spoken for s in scenes]
    json.dump(texts, open(js, "w"), ensure_ascii=False)
    subprocess.run([VENV_PY, "-W", "ignore", CLONE, js, ref, d], check=True)
    parts, gap = [], np.zeros(int(GAP * engine.SR), np.float32)
    for i in range(len(texts)):
        y = voice_check._load(os.path.join(d, f"{i:03d}.wav"), engine.SR)
        parts += [y / max(1e-6, np.abs(y).max()) * 0.9, gap]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sf.write(out, np.concatenate(parts[:-1]), engine.SR)
    json.dump({"day": day, "engine": "Indic-TTS female -> FreeVC24", "reference": cfg["file"], "reference_sha256": h,
               "owner": cfg.get("owner"), "lines": texts}, open(out + ".json", "w"), ensure_ascii=False, indent=2)
    print("generated", out)
    return out

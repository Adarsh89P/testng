"""Strict voice-over verification for the daily reels (see docs/voice_workflow.md).

Before a day's video is rendered with a supplied voice-over:
  1. sha256 of the audio is compared with every registered day: an identical file registered to another day is rejected.
  2. Duration must be plausible for the script (0.6x - 1.8x of a TTS reading of the same lines).
  3. Voice: timbre similarity to the Day 04 master (Tisha K) must be >= VOICE_MIN (different words are expected).
  4. Content: the audio is aligned (MFCC + DTW) against a TTS reading of TODAY's script and of every other registered
     day's script. It must match today's script below COST_MAX and better than any other day's script.
     This is an acoustic alignment check, not a transcript (no speech-recognition model is reachable here).
After rendering, check_output() runs the same content check on the final video's audio track.
Verified files are recorded in assets/voice/registry.json.
"""
import hashlib, json, os, subprocess, importlib
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REG = os.path.join(ROOT, "assets", "voice", "registry.json")
COST_MAX = 0.55          # Day 04 audio vs its own script: 0.47; vs Day 05 script: 0.62
MASTER = os.path.join(ROOT, "assets", "voice", "day04", "full.mp3")   # master voice reference (Tisha K), never reused
VOICE_MIN = 0.96         # master half vs other half: 0.995; Kokoro hf_beta / hf_alpha vs master: 0.89 / 0.90


class VoiceError(Exception):
    pass


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def load_registry():
    return json.load(open(REG)) if os.path.exists(REG) else {}


def save_registry(reg):
    os.makedirs(os.path.dirname(REG), exist_ok=True)
    json.dump(reg, open(REG, "w"), indent=2, ensure_ascii=False)


def _load(path, sr):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def _feat(x, sr):
    import librosa
    m = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=20, hop_length=int(0.02 * sr))[1:]
    return (m - m.mean(1, keepdims=True)) / (m.std(1, keepdims=True) + 1e-6)


def _script_audio(scenes):
    import engine
    nat = engine.NATURAL; engine.NATURAL = False
    gap = np.zeros(int(0.3 * engine.SR), np.float32)
    out = np.concatenate([np.concatenate([engine.tts(s.spoken, voice="hf_beta", speed=1.05, lang="hi"), gap])
                          for s in scenes if s.spoken])
    engine.NATURAL = nat
    return out


def match_cost(y, scenes):
    import librosa, engine
    A, B = _feat(_script_audio(scenes), engine.SR), _feat(y, engine.SR)
    D, wp = librosa.sequence.dtw(A, B, metric="cosine")
    return float(D[-1, -1] / len(wp)), len(_script_audio(scenes)) / engine.SR


def voice_profile(y, sr):
    """Speaker timbre profile: MFCC mean + spread over the whole clip (content-independent enough for one speaker)."""
    import librosa
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)[1:]
    return np.concatenate([m.mean(1), m.std(1)])


def master_voice():
    """Voice the series must sound like: the configured clone reference if any, else the Day 04 master."""
    cfg = os.path.join(ROOT, "assets", "voice", "reference.json")
    return os.path.join(ROOT, json.load(open(cfg))["file"]) if os.path.exists(cfg) else MASTER


def voice_similarity(y, sr, master=None):
    master = master or master_voice()
    a, b = voice_profile(y, sr), voice_profile(_load(master, sr), sr)
    return float(a @ b / np.linalg.norm(a) / np.linalg.norm(b))


def _day_scenes(day):
    """SCENES of another registered day's module (for the 'better than other days' check)."""
    mod = load_registry().get(f"day{day:02d}", {}).get("module")
    return importlib.import_module(mod).SCENES if mod else None


def verify(day, topic, path, scenes, module):
    """Raise VoiceError unless `path` is a new, matching voice-over for this day. Returns a report dict."""
    import engine
    key = f"day{day:02d}"
    if not os.path.exists(path):
        raise VoiceError(f"{key} ({topic}): voice-over missing. Required file: {os.path.relpath(path, ROOT)}")
    h = sha256(path)
    for k, e in load_registry().items():
        if k != key and e.get("sha256") == h:
            raise VoiceError(f"{key} ({topic}): {os.path.basename(path)} is byte-identical to the {k} voice-over "
                             f"({e['topic']}). Refusing to reuse another day's recording.")
    y = _load(path, engine.SR)
    dur = len(y) / engine.SR
    cost, ref_dur = match_cost(y, scenes)
    if not (0.6 * ref_dur <= dur <= 1.8 * ref_dur):
        raise VoiceError(f"{key} ({topic}): audio is {dur:.1f}s but the script reads in ~{ref_dur:.1f}s; wrong file?")
    vsim = voice_similarity(y, engine.SR) if key != "day04" else 1.0
    others = {}
    for k in load_registry():
        if k != key:
            sc = _day_scenes(int(k[3:]))
            if sc: others[k] = match_cost(y, sc)[0]
    report = dict(day=key, topic=topic, file=os.path.relpath(path, ROOT), sha256=h, duration=round(dur, 2),
                  script_cost=round(cost, 3), voice_similarity=round(vsim, 3), other_days={k: round(v, 3) for k, v in others.items()})
    print("voice check:", report)
    if vsim < VOICE_MIN:
        raise VoiceError(f"{key} ({topic}): voice does not match the series reference voice (similarity {vsim:.3f} < "
                         f"{VOICE_MIN}). Wrong voice or settings?")
    if cost > COST_MAX:
        raise VoiceError(f"{key} ({topic}): audio does not match today's script (cost {cost:.3f} > {COST_MAX}).")
    better = [k for k, v in others.items() if v <= cost]
    if better:
        raise VoiceError(f"{key} ({topic}): audio matches the {', '.join(better)} script as well or better "
                         f"than today's ({report['other_days']} vs {cost:.3f}). Wrong topic?")
    reg = load_registry(); reg[key] = dict(report, module=module); save_registry(reg)
    return report


def check_output(video, scenes, key):
    """Post-render: the final video's audio track must still match the day's script."""
    import engine
    cost, _ = match_cost(_load(video, engine.SR), scenes)
    print(f"output check {key}: script cost {cost:.3f}")
    if cost > COST_MAX + 0.05:
        raise VoiceError(f"{key}: final video audio does not match the script (cost {cost:.3f}).")
    return cost

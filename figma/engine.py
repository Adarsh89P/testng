"""Generic scene engine: voice per scene -> timed frames piped to ffmpeg, + typing clicks, whoosh, ambient pad."""
import os, subprocess, math, random
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from dots import *

SR = 24000
BGM_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "bgm_default.mp3")
M = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
_K = None


VOICE = "hf_beta"           # default narrator: Kokoro hf_beta (native Hindi female)
DEFAULT_LANG = "hi"         # ...speaking Hindi (set None to follow the voice's own language)
LANGS = {"h": "hi", "a": "en-us", "b": "en-gb"}
NATURAL = True              # phrase-by-phrase synthesis with human-like, slightly varied pauses


WARM_FX = ("asetrate=24000*1.05,aresample=24000,atempo=0.952381,"
           "equalizer=f=220:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.5:g=2,equalizer=f=7500:t=q:w=2:g=-3")


def warm_hi(text, speed=None):
    """'warm_hi': 60/40 blend of Kokoro's hf_alpha + hf_beta styles, slightly slower with longer pauses,
    pitch +5% (duration kept), warm/sweet EQ. A new voice of its own - not a copy of any person."""
    style = (0.6 * _K.get_voice_style("hf_alpha") + 0.4 * _K.get_voice_style("hf_beta")).astype(np.float32)
    s, sr = _K.create(text, voice=style, speed=speed or 0.95, lang="hi", sentence_pause=0.35, clause_pause=0.15)
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", WARM_FX,
                          "-f", "f32le", "-ar", str(sr), "-ac", "1", "-"], input=s.astype(np.float32).tobytes(),
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()


VENV_PY = "/home/user/venv-tts/bin/python"
INDIC = os.path.join(os.path.dirname(__file__), "..", "tools", "indic_tts.py")


def indic_batch(texts, speaker="female"):
    """AI4Bharat Indic-TTS Hindi (native-speaker FastPitch + HiFi-GAN) via the isolated venv; resampled to SR."""
    import json, tempfile
    d = tempfile.mkdtemp(); js = os.path.join(d, "lines.json")
    json.dump([[speaker, t or "।"] for t in texts], open(js, "w"), ensure_ascii=False)
    subprocess.run([VENV_PY, "-W", "ignore", INDIC, "--batch", js, d], check=True, capture_output=True)
    out = []
    for i, t in enumerate(texts):
        if not t: out.append(np.zeros(1, np.float32)); continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(d, f"{i:03d}.wav"), "-af", "highpass=f=70",
                              "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        out.append(np.frombuffer(raw, np.float32).copy())
    return out


def natural_tts(text, voice, speed, lang):
    """Split at phrase boundaries and rejoin with varied pauses, so delivery breathes like a person talking."""
    import re
    parts = [p for p in re.split(r"(?<=[,।?!.])\s+", text.strip()) if p]
    rng = random.Random(hash(text) & 0xFFFF)
    out = []
    for i, p in enumerate(parts):
        s, sr = _K.create(p, voice=voice, speed=speed * rng.uniform(0.97, 1.03), lang=lang)
        s = np.trim_zeros(s.astype(np.float32), "fb")
        out.append(s)
        if i < len(parts) - 1:
            end = p[-1]
            gap = {"?": 0.42, "!": 0.36, "।": 0.34, ".": 0.34}.get(end, 0.17) * rng.uniform(0.85, 1.2)
            out.append(np.zeros(int(sr * gap), np.float32))
    return np.concatenate(out)


def tts(text, voice=VOICE, speed=None, lang=None):
    global _K
    if _K is None: _K = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
    if voice == "warm_hi":                      # custom warm, soft Indian-female Hindi voice (blend + gentle shaping)
        return warm_hi(text, speed)
    lang = lang or DEFAULT_LANG or LANGS.get(voice[0], "en-us")
    speed = speed or (0.97 if lang == "hi" else 1.0)
    if NATURAL:
        return natural_tts(text, voice, speed, lang)
    s, sr = _K.create(text, voice=voice, speed=speed, lang=lang)
    return s.astype(np.float32)


class Scene:
    """spoken: Devanagari for TTS. caption: Roman Hinglish. draw(cv, t, dur, st). type_spans: [(t0,t1)] for clicks."""
    def __init__(self, spoken, caption, draw, pad=0.6, min_dur=0, type_spans=(), whoosh=False, hold=0.0, clicks=(), sfx=()):
        self.spoken, self.caption, self.draw = spoken, caption, draw
        self.pad, self.min_dur, self.type_spans, self.whoosh, self.hold = pad, min_dur, list(type_spans), whoosh, hold
        self.clicks = list(clicks)
        self.sfx = list(sfx)          # [(t, kind)] kind in SFX


# ------------------------------------------------------------------ audio synth
def click(n=0.018):
    t = np.arange(int(SR * n)) / SR
    return (np.random.randn(len(t)) * np.exp(-t * 400) * 0.25).astype(np.float32)


def mouse_click():
    """Short two-part mouse click: sharp tick + soft body."""
    t = np.arange(int(SR * 0.04)) / SR
    tick = np.random.randn(len(t)) * np.exp(-t * 900) * 0.6
    body = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 300) * 0.25
    return (tick + body).astype(np.float32)


def _env(n, a=0.005, r=None):
    t = np.arange(n) / SR; r = r or n / SR
    return np.minimum(1, t / a) * np.exp(-t / (r / 4))


def sfx_pop(f=880):
    n = int(SR * 0.09); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (f + 900 * np.exp(-t * 40)) * t) * _env(n, 0.002, 0.09) * 0.5).astype(np.float32)


def sfx_ding(f=1320):
    n = int(SR * 0.9); t = np.arange(n) / SR
    w = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) + 0.25 * np.sin(2 * np.pi * f * 3.02 * t)
    return (w * np.exp(-t * 4.5) * 0.28).astype(np.float32)


def sfx_chime():
    a, b = sfx_ding(1046), sfx_ding(1568); out = np.zeros(len(a) + int(SR * 0.12), np.float32)
    out[:len(a)] += a; out[int(SR * 0.12):] += b; return out


def sfx_buzz():
    n = int(SR * 0.35); t = np.arange(n) / SR
    w = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 + np.sin(2 * np.pi * 220 * t) * 0.3
    return (w * np.minimum(1, t / 0.01) * np.exp(-t * 6) * 0.22).astype(np.float32)


def sfx_tick():
    n = int(SR * 0.03); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 300) * 0.35).astype(np.float32)


def sfx_riser(d=0.8):
    n = int(SR * d); t = np.arange(n) / SR
    x = np.convolve(np.random.randn(n), np.ones(12) / 12, "same")
    return (x * (t / d) ** 2 * 0.35 + np.sin(2 * np.pi * (200 + 900 * t / d) * t) * (t / d) * 0.08).astype(np.float32)


def sfx_drop():
    n = int(SR * 0.5); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (180 * np.exp(-t * 6) + 40) * t) * np.exp(-t * 5) * 0.6).astype(np.float32)


SFX = {"pop": sfx_pop, "pop_lo": lambda: sfx_pop(520), "pop_hi": lambda: sfx_pop(1200), "ding": sfx_ding,
       "chime": sfx_chime, "buzz": sfx_buzz, "tick": sfx_tick, "riser": sfx_riser, "drop": sfx_drop}


def whoosh(d=0.45):
    n = int(SR * d); x = np.random.randn(n)
    k = np.ones(40) / 40; x = np.convolve(x, k, "same")
    env = np.exp(-((np.arange(n) / n - 0.5) ** 2) / 0.03)
    return (x * env * 0.5).astype(np.float32)


def pad_music(dur, seed=3):
    """Calm ambient pad: slow minor-ish chord loop of soft sines + gentle shimmer."""
    n = int(SR * dur); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    chords = [(220.0, 261.63, 329.63), (196.0, 246.94, 293.66), (174.61, 220.0, 261.63), (196.0, 246.94, 329.63)]
    seg = 4.0
    for i in range(int(dur / seg) + 1):
        s0 = int(i * seg * SR); s1 = min(n, int((i + 1) * seg * SR) + SR)
        if s0 >= n: break
        tt = t[s0:s1] - t[s0]
        env = np.minimum(1, tt / 1.2) * np.minimum(1, np.maximum(0, (seg + 1 - tt)) / 1.2)
        for f in chords[i % 4]:
            out[s0:s1] += (np.sin(2 * np.pi * f * tt) * 0.5 + np.sin(2 * np.pi * f * 2 * tt) * 0.12) * env * 0.05
    return out


def load_bed(path, n, xfade=1.5):
    """Decode the background track to mono SR and loop it (with crossfade) to n samples."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    bed = np.frombuffer(raw, np.float32).copy()
    out, xf = bed.copy(), int(SR * xfade)
    while len(out) < n:
        ramp = np.linspace(0, 1, xf, dtype=np.float32)
        out[-xf:] = out[-xf:] * (1 - ramp) + bed[:xf] * ramp
        out = np.concatenate([out, bed[xf:]])
    return out[:n]


def duck(bed, vo, under_db=-23, gap_db=-14, win=0.25):
    """Scale the bed relative to voice loudness: quieter while the narrator talks, a bit up in gaps."""
    k = max(1, int(SR * win)); env = np.sqrt(np.convolve(vo ** 2, np.ones(k) / k, "same"))
    active = np.clip(env / (env.max() * 0.25 + 1e-9), 0, 1)
    active = np.convolve(active, np.ones(k) / k, "same")          # smooth the gain changes
    vo_rms = np.sqrt(np.mean(vo[vo != 0] ** 2)) if np.any(vo) else 0.1
    bed_rms = np.sqrt(np.mean(bed ** 2)) + 1e-9
    g_db = gap_db + (under_db - gap_db) * active
    return bed / bed_rms * vo_rms * 10 ** (g_db / 20)


def mix_into(buf, clip, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(clip)); buf[i:j] += clip[:j - i] * gain


# ------------------------------------------------------------------ render
def caption(cv, s, y, size=36):
    if not s: return
    cv.font(SANS, size, True)
    words, lines, cur = s.split(), [], ""
    for w in words:
        if cv.text_w(cur + " " + w) > cv.w - 140 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    # dark band so captions stay readable over zoomed-in content
    cv.c.set_source_rgba(*BG, 0.88); cv.c.rectangle(0, y - size * 1.2, cv.w, size * 1.3 * len(lines) + size * 0.9); cv.c.fill()
    for i, ln in enumerate(lines):
        x = cv.w / 2 - cv.text_w(ln) / 2
        cv.text(x, y + i * size * 1.3, ln, (0.85, 0.85, 0.88))


# warmth, de-harsh, gentle compression, very light room so the voice sounds less dry/robotic
VOICE_FX = ("highpass=f=75,equalizer=f=180:t=q:w=1.2:g=2.5,equalizer=f=3200:t=q:w=1.5:g=1.5,"
            "equalizer=f=7000:t=q:w=2:g=-4,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,"
            "aecho=0.85:0.6:22|37:0.06|0.04")


def split_audio(path, cuts):
    """Load a recorded / generated voice-over and split it at the given times (s) into per-scene clips."""
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-af", "highpass=f=60",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32).copy()
    edges = [0.0] + list(cuts) + [len(y) / SR]
    out = []
    for a, b in zip(edges, edges[1:]):
        seg = y[int(a * SR):int(b * SR)]
        nz = np.where(np.abs(seg) > 0.01)[0]                 # trim leading / trailing silence
        seg = seg[max(0, nz[0] - int(0.03 * SR)):nz[-1] + int(0.08 * SR)] if len(nz) else seg
        out.append(seg.astype(np.float32))
    return out


def render(scenes, out, W=1080, H=1920, FPS=30, voice=VOICE, cap_y=None, workdir=None, bgm=None, lang=None, natural=None, voice_fx=True,
           voice_clips=None):
    """voice_clips: optional list of float32 arrays (one per scene, at SR), e.g. from split_audio(), used instead of TTS."""
    workdir = workdir or os.path.dirname(out)
    os.makedirs(workdir, exist_ok=True)
    global NATURAL
    _nat = NATURAL
    if natural is not None: NATURAL = natural
    if voice_clips is not None:
        voices = list(voice_clips)
    elif voice.startswith("indic_"):
        voices = indic_batch([s.spoken for s in scenes], voice.split("_", 1)[1])
    else:
      voices = [tts(s.spoken, voice, speed=(1.05 if natural is False else None), lang=lang) if s.spoken else np.zeros(1, np.float32) for s in scenes]
    durs = [max(len(v) / SR + s.pad + s.hold, s.min_dur) for v, s in zip(voices, scenes)]
    total = sum(durs) + 0.8
    audio = np.zeros(int(SR * total) + SR, np.float32)
    vo_bus = np.zeros_like(audio)
    starts, t0 = [], 0.25
    for v, d, s in zip(voices, durs, scenes):
        starts.append(t0); mix_into(audio, v, t0 + 0.1); mix_into(vo_bus, v, t0 + 0.1)
        if s.whoosh: mix_into(audio, whoosh(), max(0, t0 - 0.15), 0.5)
        for c in s.clicks: mix_into(audio, mouse_click(), t0 + c, 0.7)
        for ft, kind in s.sfx: mix_into(audio, SFX[kind](), t0 + ft, 0.8)
        for a, b in s.type_spans:
            tt = t0 + a
            while tt < t0 + b: mix_into(audio, click(), tt, 0.5); tt += random.uniform(0.045, 0.085)
        t0 += d
    # bgm: None = no background (default), "synth" = generated pad, or a file path (e.g. BGM_DEFAULT) ducked under voice
    if bgm == "synth":
        audio += pad_music(len(audio) / SR)[:len(audio)]
    elif bgm and os.path.exists(bgm):
        audio += duck(load_bed(bgm, len(audio)), vo_bus)
    fade = int(SR * 0.6); audio[-fade:] *= np.linspace(1, 0, fade)
    audio /= max(1e-6, np.abs(audio).max()) / 0.95
    wav = os.path.join(workdir, "_audio.wav"); sf.write(wav, audio, SR)

    vid = os.path.join(workdir, "_video.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                          "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    cv = Canvas(W, H); nf = int(total * FPS); si = 0; state = {}
    for f in range(nf):
        t = f / FPS
        while si + 1 < len(scenes) and t >= starts[si + 1]: si += 1
        s = scenes[si]; lt = t - starts[si]
        cv.clear()
        s.draw(cv, max(0, lt), durs[si], state)
        if cap_y: caption(cv, s.caption, cap_y)
        p.stdin.write(cv.raw())
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-af", (VOICE_FX + "," if voice_fx else "") + "loudnorm=I=-14:TP=-1:LRA=11",
                    "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(vid)
    NATURAL = _nat
    return total

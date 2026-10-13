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
    lang = lang or DEFAULT_LANG or LANGS.get(voice[0], "en-us")
    speed = speed or (0.97 if lang == "hi" else 1.0)
    if NATURAL:
        return natural_tts(text, voice, speed, lang)
    s, sr = _K.create(text, voice=voice, speed=speed, lang=lang)
    return s.astype(np.float32)


class Scene:
    """spoken: Devanagari for TTS. caption: Roman Hinglish. draw(cv, t, dur, st). type_spans: [(t0,t1)] for clicks."""
    def __init__(self, spoken, caption, draw, pad=0.6, min_dur=0, type_spans=(), whoosh=False, hold=0.0, clicks=()):
        self.spoken, self.caption, self.draw = spoken, caption, draw
        self.pad, self.min_dur, self.type_spans, self.whoosh, self.hold = pad, min_dur, list(type_spans), whoosh, hold
        self.clicks = list(clicks)


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


def render(scenes, out, W=1080, H=1920, FPS=30, voice=VOICE, cap_y=None, workdir=None, bgm=None, lang=None):
    workdir = workdir or os.path.dirname(out)
    os.makedirs(workdir, exist_ok=True)
    voices = [tts(s.spoken, voice, lang=lang) if s.spoken else np.zeros(1, np.float32) for s in scenes]
    durs = [max(len(v) / SR + s.pad + s.hold, s.min_dur) for v, s in zip(voices, scenes)]
    total = sum(durs) + 0.8
    audio = np.zeros(int(SR * total) + SR, np.float32)
    vo_bus = np.zeros_like(audio)
    starts, t0 = [], 0.25
    for v, d, s in zip(voices, durs, scenes):
        starts.append(t0); mix_into(audio, v, t0 + 0.1); mix_into(vo_bus, v, t0 + 0.1)
        if s.whoosh: mix_into(audio, whoosh(), max(0, t0 - 0.15), 0.5)
        for c in s.clicks: mix_into(audio, mouse_click(), t0 + c, 0.7)
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
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-af", VOICE_FX + ",loudnorm=I=-14:TP=-1:LRA=11",
                    "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(vid)
    return total

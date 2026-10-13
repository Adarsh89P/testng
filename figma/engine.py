"""Generic scene engine: voice per scene -> timed frames piped to ffmpeg, + typing clicks, whoosh, ambient pad."""
import os, subprocess, math, random
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from dots import *

SR = 24000
M = os.path.join(os.path.dirname(__file__), "..", "assets", "models")
_K = None


def tts(text, voice="hf_beta", speed=1.05):
    global _K
    if _K is None: _K = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
    s, sr = _K.create(text, voice=voice, speed=speed, lang="hi")
    return s.astype(np.float32)


class Scene:
    """spoken: Devanagari for TTS. caption: Roman Hinglish. draw(cv, t, dur, st). type_spans: [(t0,t1)] for clicks."""
    def __init__(self, spoken, caption, draw, pad=0.6, min_dur=0, type_spans=(), whoosh=False, hold=0.0):
        self.spoken, self.caption, self.draw = spoken, caption, draw
        self.pad, self.min_dur, self.type_spans, self.whoosh, self.hold = pad, min_dur, list(type_spans), whoosh, hold


# ------------------------------------------------------------------ audio synth
def click(n=0.018):
    t = np.arange(int(SR * n)) / SR
    return (np.random.randn(len(t)) * np.exp(-t * 400) * 0.25).astype(np.float32)


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
    for i, ln in enumerate(lines):
        x = cv.w / 2 - cv.text_w(ln) / 2
        cv.text(x, y + i * size * 1.3, ln, (0.85, 0.85, 0.88))


def render(scenes, out, W=1080, H=1920, FPS=30, voice="hf_beta", cap_y=None, workdir=None):
    workdir = workdir or os.path.dirname(out)
    os.makedirs(workdir, exist_ok=True)
    voices = [tts(s.spoken, voice) if s.spoken else np.zeros(1, np.float32) for s in scenes]
    durs = [max(len(v) / SR + s.pad + s.hold, s.min_dur) for v, s in zip(voices, scenes)]
    total = sum(durs) + 0.8
    audio = np.zeros(int(SR * total) + SR, np.float32)
    starts, t0 = [], 0.25
    for v, d, s in zip(voices, durs, scenes):
        starts.append(t0); mix_into(audio, v, t0 + 0.1)
        if s.whoosh: mix_into(audio, whoosh(), max(0, t0 - 0.15), 0.5)
        for a, b in s.type_spans:
            tt = t0 + a
            while tt < t0 + b: mix_into(audio, click(), tt, 0.5); tt += random.uniform(0.045, 0.085)
        t0 += d
    audio += pad_music(len(audio) / SR)[:len(audio)]
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
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(vid)
    return total

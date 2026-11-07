"""Score + foley + your voice-over -> out/mix.wav. Pure numpy synthesis: tanpura drone, bansuri-like flute, dholak/frame drum, gongs, bells.
Run with the library's venv python:  $LIB/.venv/bin/python mix.py
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100
ev = json.load(open(os.path.join(HERE, 'events.json')))
DUR = float(ev['dur']); E = ev['ev']
N = int((DUR + 1) * SR)
AN = [[0, 0], [14.7, 7.2], [18.1, 10.8], [25.3, 18.0], [25.8, 18.4], [31.2, 24.0], [32.2, 25.0], [34.4, 28.0], [35.7, 29.3], [39.9, 32.7], [40.7, 33.5], [44.8, 38.0], [47.4, 41.4], [50.4, 43.0], [54.4, 46.4], [58.8, 51.4], [59.8, 52.2], [72.5, 56.0]]
def O2N(t):
    for i in range(len(AN) - 1):
        a, b = AN[i]; c, d = AN[i + 1]
        if t <= d: return a + (c - a) * (t - b) / (d - b)
    return AN[-1][0]
rng = np.random.default_rng(7)
T = lambda n: np.arange(n) / SR

def add(buf, sig, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += sig[:j - i] * g
def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, order=2): return sosfilt(butter(order, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, 'high', fs=SR, output='sos'), x)

# ---------- instruments ----------
def drone(f, dur, g=1):                       # tanpura pluck: harmonics with a slight buzz (jivari)
    t = T(int(dur * SR)); y = np.zeros_like(t)
    for h in range(1, 14):
        y += (h ** -1.15) * np.sin(2 * np.pi * f * h * t + .3 * h) * np.exp(-t / (2.8 / (1 + .08 * h)))
    y *= (1 + .25 * np.sin(2 * np.pi * 5 * t) * np.exp(-t / 1.5))
    return y * g * np.minimum(1, t * 90)
def flute(f, dur, vel=1., vib=5.4, breath=.07):
    n = int((dur + .25) * SR); t = T(n)
    a = np.minimum(1, t / .09) * np.exp(-np.maximum(0, t - dur) / .08)
    vibd = np.minimum(1, t / .5) * .004 * np.sin(2 * np.pi * vib * t)
    ph = 2 * np.pi * np.cumsum(f * (1 + vibd)) / SR
    y = np.sin(ph) + .28 * np.sin(2 * ph) + .1 * np.sin(3 * ph)
    y += breath * bp(rng.standard_normal(n), 1800, 5200)
    return y * a * vel * .5
def drum(g=1., lowf=150):                     # dholak-ish thump
    n = int(.5 * SR); t = T(n); f = lowf * np.exp(-t * 7) + 62
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .14)
    y += .35 * lp(rng.standard_normal(n), 900) * np.exp(-t / .03)
    return y * g
def heart(g=1.):
    n = int(.4 * SR); t = T(n); y = np.sin(2 * np.pi * 54 * t) * np.exp(-t / .12)
    y2 = np.zeros(n); k = int(.2 * SR); y2[k:] = (np.sin(2 * np.pi * 48 * t[:n - k]) * np.exp(-t[:n - k] / .1) * .7)
    return (y + y2) * g
def gong(f=98, dur=4.5, g=1.):
    n = int(dur * SR); t = T(n); y = np.zeros(n)
    for r, a, d in [(1, 1, 3.2), (1.47, .7, 2.6), (2.09, .6, 2.1), (2.76, .45, 1.6), (3.61, .3, 1.2), (4.7, .2, .8)]:
        y += a * np.sin(2 * np.pi * f * r * (1 - .012 * (1 - np.exp(-t * 2))) * t) * np.exp(-t / d)
    y += .15 * hp(rng.standard_normal(n), 2000) * np.exp(-t / .1)
    return y * g * .55 * np.minimum(1, t * 400)
def bell(f, g=1.):
    n = int(1.9 * SR); t = T(n)
    y = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d) for r, a, d in [(1, 1, 1.0), (2.76, .5, .5), (5.4, .25, .25), (8.9, .1, .12)])
    return y * g * .4
def swoosh(g=1., up=True):
    n = int(.5 * SR); t = T(n); x = bp(rng.standard_normal(n), 500, 2800)
    env = (np.sin(np.pi * np.minimum(1, t / .5)) ** 2); return x * env * g * .35
def creak(g=1.):
    n = int(.45 * SR); t = T(n); f = 95 + 22 * np.sin(2 * np.pi * 3 * t)
    y = ((2 * ((np.cumsum(f) / SR) % 1) - 1)) * .5; y = bp(y + .5 * rng.standard_normal(n), 120, 900)
    return y * np.sin(np.pi * t / .45) ** 1.5 * g * .5
def gulp(g=1.):
    n = int(.3 * SR); t = T(n); f = 220 * np.exp(-t * 8) + 70
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .1) * g * .7

def snapfx():
    n = int(.25 * SR); t = T(n); return (hp(rng.standard_normal(n), 1500) * np.exp(-t / .02) + .5 * np.sin(2 * np.pi * 180 * t) * np.exp(-t / .06)) * .8

# ---------- music: drone, flute (dread in a minor mode, grace in Bhupali), rhythm ----------
music = np.zeros(N)
SA = 146.83                                    # D3
MIN = [0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19]    # Bhairavi-like: for dread
PENT = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]          # Bhupali: for grace
nt = lambda sc, d, o=0: SA * 2 ** ((sc[d] + 12 * o) / 12)
def bed(t0, t1, vel=1.):
    t = t0
    for f, g in zip([SA * 1.5, SA * 2, SA * 2, SA / 2] * 40, [1, .8, .8, 1.1] * 40):
        if t >= t1: break
        add(music, drone(f, 3.4, g * vel * .22), t); t += 1.05
bed(0.0, 22.5, .9); bed(23.2, 35.0, .8); bed(35.5, DUR, 1.0)
add(music, drone(SA / 2, 8, .6), 22.8); add(music, drone(SA / 4, 8, .6), 25.0)
def phrase(t0, sc, notes, vel=1.):
    t = t0
    for d, o, ln in notes:
        add(music, flute(nt(sc, d, o), ln, vel), t); t += ln * .93
phrase(.9, PENT, [(4, 1, .9), (5, 1, .9), (7, 1, 1.3), (5, 1, 1.4)], .6)                      # opening: calm, Kailash
phrase(7.0, MIN, [(0, 1, 1.2), (1, 1, 1.0), (3, 1, 1.4)], .5)                                  # "the poison came first": uneasy
phrase(12.4, PENT, [(2, 1, .8), (3, 1, .6), (4, 1, 1.0), (3, 1, .7), (2, 1, 1.0)], .55)        # the churning: steady
phrase(18.4, PENT, [(4, 1, .6), (5, 1, .6), (4, 1, 1.0)], .5)
phrase(22.9, MIN, [(0, 0, 1.6), (1, 0, 1.2), (0, 0, 1.8), (3, 0, 1.0)], .65)                  # Halahala rises
phrase(30.8, MIN, [(3, 0, .7), (4, 0, .7), (3, 0, .7), (1, 0, 1.6)], .6)                       # they flee
phrase(35.8, PENT, [(2, 1, 1.0), (3, 1, .8), (4, 1, 1.4)], .6)                                 # they pray
phrase(39.9, PENT, [(4, 1, .8), (2, 1, .8), (0, 1, 1.6)], .7)                                  # Shiva drinks
phrase(43.4, PENT, [(2, 1, .9), (4, 1, .9), (5, 1, 1.0), (4, 1, 1.4)], .7)                     # Parvati
phrase(49.2, PENT, [(5, 1, .7), (7, 1, .7), (8, 1, 1.0), (7, 1, 2.0)], .85)                    # blue throat
phrase(55.3, PENT, [(7, 1, 1.0), (5, 1, 1.0), (4, 1, 1.0), (2, 1, 1.2)], .6)                  # water
phrase(61.6, PENT, [(4, 1, 1.0), (2, 1, 1.0), (0, 1, 2.8)], .45)                               # settle
def cut(a, b, fade=.04):
    i, j = int(a * SR), int(b * SR); music[i:j] *= 0
    k = int(fade * SR); music[i - k:i] *= np.linspace(1, 0, k)
cut(35.0, 35.5)

# ---------- foley / percussion ----------
fx = np.zeros(N)
for e in E:
    t, ty, v = e['t'], e['type'], e.get('v', 1.)
    if ty == 'drum': add(fx, drum(.7 * v), t)
    elif ty == 'gong': add(fx, gong(98 if v >= .9 else 110, 4.5, v), t)
    elif ty == 'heart': add(fx, heart(.7 * v), t)
    elif ty == 'tick': add(fx, bell(nt(PENT, min(e['i'], 9), 1) * 2, .8), t)
    elif ty == 'chime':
        for k, d in enumerate([4, 5, 6, 7, 8, 9]): add(fx, bell(nt(PENT, d, 1) * 2, .5), t + k * .09)
    elif ty == 'lift': add(fx, swoosh(v), t)
    elif ty == 'pull': add(fx, creak(v), t)
    elif ty == 'gulp': add(fx, gulp(), t)
    elif ty == 'snap': add(fx, snapfx(), t)

# ---------- voice (your recording) ----------
vo_src = os.path.join(HERE, 'audio', 'vo.mp3'); vo_wav = os.path.join(HERE, 'out', 'vo.wav')
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', vo_src, '-ar', str(SR), '-ac', '1', vo_wav], check=True)
vo, _ = sf.read(vo_wav)
vo = vo / (np.max(np.abs(vo)) + 1e-9)
# light "small theatre" room: short decaying-noise impulse, 12 % wet
ir = rng.standard_normal(int(.38 * SR)) * np.exp(-np.arange(int(.38 * SR)) / (.09 * SR)); ir /= np.sqrt((ir ** 2).sum())
wet = fftconvolve(vo, ir)[:len(vo)]
vo = vo * .9 + wet * .14
VOFF = [e['t'] for e in E if e['type'] == 'vo'][0]
voice = np.zeros(N); add(voice, vo, VOFF)

# ---------- ducking and balance ----------
win = int(.05 * SR); env = np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, 'same'))
env = np.maximum.accumulate(np.r_[env[:1], env])[1:] * 0 + env                       # keep as is
sig = np.clip(env / (env.max() * .25 + 1e-9), 0, 1)
k_att, k_rel = np.exp(-1 / (.08 * SR)), np.exp(-1 / (.45 * SR)); g = np.zeros(N); cur = 0.
for i in range(N):
    cur = k_att * cur + (1 - k_att) * sig[i] if sig[i] > cur else k_rel * cur + (1 - k_rel) * sig[i]
    g[i] = cur
duck = 10 ** (-12 * g / 20)
rms = lambda x: np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2) + 1e-12)
music *= (rms(voice) * .5) / rms(music)                                              # bed about 6 dB under the voice before ducking
fx *= (rms(voice) * .55) / (rms(fx) + 1e-9)
fx = np.clip(fx, -2, 2)
mix = voice * 1.0 + music * duck + fx * (10 ** (-4 * g / 20))
mix = np.tanh(mix * .9) / .9 * .85
n = int(DUR * SR) + SR // 2
fade = np.ones(N); k = int(1.6 * SR); fade[int(DUR * SR) - k:int(DUR * SR)] = np.linspace(1, 0, k); fade[int(DUR * SR):] = 0
mix = (mix * fade)[:n]
st = np.stack([mix, mix], 1)
sf.write(os.path.join(HERE, 'out', 'mix.wav'), st, SR, subtype='PCM_16')
print('mix', len(mix) / SR, 's  peak', float(np.max(np.abs(mix))))

"""Soundtrack for Short 4: the user's voice + a hand-made Indian palette (synthesised, no samples).
Run from the library root:  .venv/bin/python -I <project>/mix.py <project>
Writes <project>/audio/mix.wav (48 kHz stereo, float)."""
import sys, subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
sys.path.insert(0, str(Path.cwd() / 'core' / 'audio'))
import sfx
from sfx import SR, t_, noise, bp, lp, hp, norm, add

P = Path(sys.argv[1]); DUR = 57.6
rng = np.random.default_rng(11)

# —— voice ——
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(P / 'audio/voice.mp3'), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
voice = np.frombuffer(raw, np.float32).copy()

# —— instruments ——
SA = 138.6   # C#3
def tanpura_pluck(f, d=3.2):
    tt = t_(d); out = np.zeros_like(tt)
    for n in range(1, 22):
        bright = np.clip(tt / (0.25 + n * .06), 0, 1) * np.exp(-tt / (2.6 - n * .07))   # jawari: upper partials bloom then fade
        out += np.sin(2 * np.pi * f * n * tt * (1 + .0004 * n)) * bright / n ** .9
    return norm(out * np.exp(-tt / 3.0) * np.clip(tt / .01, 0, 1))
def ge(v=1.0, f0=88):   # bayan: low stroke with a rising pitch
    d = .55; tt = t_(d); f = f0 * (1 + .25 * np.clip(tt / .25, 0, 1))
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .2) + .25 * lp(noise(d), 300) * np.exp(-tt / .03)) * v
def na(v=1.0, f=520):   # dayan: ringing stroke
    d = .4; tt = t_(d); out = np.zeros_like(tt)
    for k, a, tau in [(1, 1, .16), (2.0, .5, .1), (3.0, .3, .07), (4.16, .2, .05)]: out += a * np.sin(2 * np.pi * f * k * tt) * np.exp(-tt / tau)
    return norm(out + .4 * bp(noise(d), 2000, 6000) * np.exp(-tt / .008)) * v
def bell(f=700, v=1.0, d=4.0):
    tt = t_(d); out = np.zeros_like(tt)
    for k, a, tau in [(1, 1, 2.4), (2.32, .6, 1.4), (4.25, .35, .8), (6.63, .2, .5), (.5, .3, 3.0)]: out += a * np.sin(2 * np.pi * f * k * tt + k) * np.exp(-tt / tau)
    return norm(out * (1 + .15 * np.sin(2 * np.pi * 3.2 * tt))) * v
def shankh(f=233, d=2.6, v=1.0):
    tt = t_(d); vib = 1 + .006 * np.sin(2 * np.pi * 5 * tt) + .03 * np.clip(1 - tt / .3, 0, 1) * -1
    ph = 2 * np.pi * np.cumsum(f * vib) / SR; saw = sum(np.sin(k * ph) / k for k in range(1, 30))
    x = bp(saw, 180, 2400) + .6 * bp(saw, 900, 1300) + .05 * bp(noise(d), 600, 3000)
    envl = np.clip(tt / .35, 0, 1) * np.clip((d - tt) / .7, 0, 1)
    return norm(x * envl) * v
def swish(d, v=1.0):
    return norm(bp(noise(d), 300, 1400) * (.5 + .5 * np.sin(np.pi * t_(d) / d))) * v
def leather(v=1.0):   # dry flap on lift-off
    d = .14; tt = t_(d); return norm(bp(noise(d), 500, 3000) * np.exp(-tt / .03)) * v
BHUPALI = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2]

mus = np.zeros((int(DUR * SR), 2), np.float32)   # music + fx bed (ducked under the voice)
fx = np.zeros_like(mus)                          # accents that stay on top
def chirp(v=1.0):   # a small forest bird
    d = .18; tt = t_(d); f = 2600 + 1400 * np.sin(np.pi * tt / d) + 300 * np.sin(2 * np.pi * 28 * tt)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 2) * v
def trumpet(v=1.0):   # Airavata
    d = 1.1; tt = t_(d); f = 260 + 340 * np.clip(tt / .35, 0, 1) - 60 * np.clip((tt - .7) / .4, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * (1 + .02 * np.sin(2 * np.pi * 9 * tt))) / SR; saw = sum(np.sin(k * ph) / k for k in range(1, 24))
    return norm(bp(saw, 400, 3200) * np.clip(tt / .08, 0, 1) * np.clip((d - tt) / .3, 0, 1)) * v
def crackle(d, v=1.0):   # fire
    n = np.zeros(int(d * SR))
    for k in range(int(d * 40)): s = int(rng.random() * (len(n) - 800)); n[s:s + 800] += bp(noise(800 / SR), 1500, 6000) * np.exp(-np.arange(800) / 90) * rng.random()
    return norm(n + .3 * lp(noise(d), 500)) * v

def crackle(d, v=1.0):   # fire
    n = np.zeros(int(d * SR))
    for k in range(int(d * 40)): s_ = int(rng.random() * (len(n) - 800)); n[s_:s_ + 800] += bp(noise(800 / SR), 1500, 6000) * np.exp(-np.arange(800) / 90) * rng.random()
    return norm(n + .3 * lp(noise(d), 500)) * v
def rainbed(d, v=1.0): return norm(hp(noise(d), 2500) * (.6 + .4 * np.sin(np.pi * t_(d) / d))) * v
# tanpura drone throughout, cut for the pause after head and tail are assigned
pat = [SA * .75, SA * 2, SA * 2, SA]
for i, t in enumerate(np.arange(0.2, DUR - 1.5, .62)):
    if 20.7 < t < 21.9: continue
    add(mus, tanpura_pluck(pat[i % 4]), t, .09, pan=-.3 + .2 * (i % 4))
# hook: the serpent, then its fire
add(fx, bell(760, 1), .15, .3); add(fx, ge(1, 60), .2, .45); add(fx, sfx.whoosh(.35), 1.45, .1)
add(fx, bp(noise(1.0), 2500, 7000) * np.exp(-t_(1.0) / .35), .4, .1)
add(fx, crackle(3.6), 3.9, .25); add(fx, ge(1, 55), 3.95, .35)
# the tableau
add(mus, lp(sfx.brown(3.0), 400) * np.sin(np.pi * t_(3.0) / 3.0), 8.4, .5); add(fx, sfx.whoosh(.5), 8.5, .1)
add(fx, ge(1, 66), 10.2, .45); add(fx, sfx.rumble(1.4), 10.2, .25)
add(fx, bp(noise(1.0), 2500, 7000) * np.exp(-t_(1.0) / .35), 12.6, .1)
add(fx, bell(SA * 3, 1, 3), 15.3, .18, pan=-.6); add(fx, na(1, 460), 15.3, .2)        # daityas to the head
add(fx, bell(SA * 4, 1, 3), 18.85, .18, pan=.6); add(fx, na(1, 540), 18.85, .2)       # devas to the tail
# the churning groove from "फिर मंथन शुरू हुआ"
beat = 60 / 92
for k in range(int((52.0 - 21.9) / beat * 2)):
    t = 21.9 + k * beat / 2; stroke = ['ge', 'na', 'na', 'ge', 'na', 'ge', 'na', 'na'][k % 8]
    add(mus, ge(1, 85) if stroke == 'ge' else na(1, 500 + 40 * (k % 3)), t, .22 if stroke == 'ge' else .09, pan=(-.2 if stroke == 'ge' else .2))
for k in range(int((52.0 - 22.1) / (1 / 1.1))):
    t = 22.1 + k / 1.1; add(mus, sfx.creak(.8), t, .08, pan=.1); add(mus, swish(.8), t + .1, .07, pan=-.2)
# fire with every breath (one burst every 1.6 s), the daityas scorched
for k in range(int((52.0 - 23.7) / 1.6)): add(mus, crackle(1.0), 23.7 + k * 1.6 + .2, .22, pan=-.6)
add(mus, sfx.rumble(3.2), 28.5, .3); add(fx, hp(noise(1.5), 2000) * np.exp(-t_(1.5) / .5), 28.6, .08)
# clouds and rain at the tail
add(mus, lp(noise(4.2), 600) * np.sin(np.pi * t_(4.2) / 4.2) * .6, 32.2, .35, pan=.3)
add(mus, rainbed(4.8), 36.7, .2, pan=.6)
for k in range(10): add(fx, bell(SA * 8 * BHUPALI[k % 6], 1, 1.4), 38.0 + k * .3, .04, pan=.6)   # the devas revive
# एक ओर अग्नि · दूसरी ओर वर्षा
add(fx, crackle(1.4), 43.2, .3, pan=-.7); add(fx, ge(1, 55), 43.2, .35)
add(fx, rainbed(1.6), 44.33, .3, pan=.7); add(fx, bell(SA * 6, 1, 2.5), 44.35, .12, pan=.7)
# the Lord's plan
add(fx, ge(1, 48), 45.9, .4); add(fx, bell(SA * 1.5, 1, 4.5), 45.95, .22)
for k in range(14): add(fx, bell(SA * 8 * BHUPALI[k % 6], 1, 1.2), 49.6 + k * .11, .035, pan=.5)
# end card
add(fx, sfx.whoosh(.5), 51.9, .1); add(fx, ge(1, 80), 52.31, .45); add(fx, bell(SA * 4, 1, 4), 52.35, .24)
for i, t in enumerate([53.7, 53.9, 54.1, 54.3]): add(fx, bell(SA * 4 * BHUPALI[i + 1], 1, 3), t, .12, pan=-.3 + i * .2)
add(fx, shankh(233, 1.6), 56.55, .34)

# hard silence 20.71–21.88: bed to digital zero (fx keeps its single tap)
s0, s1 = int(20.71 * SR), int(21.88 * SR); mus[s0:s1] = 0
# duck the bed under the voice (~9 dB)
env = np.abs(voice); k = int(.12 * SR); env = np.convolve(env, np.ones(k) / k, 'same'); env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
duck = np.ones(len(mus)); n = min(len(env), len(duck)); duck[:n] = 1 - .72 * env[:n]
mus *= duck[:, None]
out = mus * .32 + fx * .42
add(out, voice, 0.0, 1.0)
# fade-out with the lamp being carried away
f0 = int(57.0 * SR); out[f0:] *= np.linspace(1, 0, len(out) - f0)[:, None]
out = sfx.limit(out * .9, .95) if out.ndim == 1 else np.stack([sfx.limit(out[:, 0] * .9, .95), sfx.limit(out[:, 1] * .9, .95)], 1)
wavfile.write(P / 'audio/mix.wav', SR, out.astype(np.float32))
print('mix.wav', out.shape[0] / SR, 's  peak', float(np.abs(out).max()))

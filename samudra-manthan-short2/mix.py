"""Soundtrack for Short 2: the user's voice + a hand-made Indian palette (synthesised, no samples).
Run from the library root:  .venv/bin/python -I <project>/mix.py <project>
Writes <project>/audio/mix.wav (48 kHz stereo, float)."""
import sys, subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
sys.path.insert(0, str(Path.cwd() / 'core' / 'audio'))
import sfx
from sfx import SR, t_, noise, bp, lp, hp, norm, add

P = Path(sys.argv[1]); DUR = 65.6
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

# tanpura drone throughout, cut for the silence after the garland falls
pat = [SA * .75, SA * 2, SA * 2, SA]
for i, t in enumerate(np.arange(0.2, DUR - 1.5, .62)):
    if 31.8 < t < 33.0: continue
    add(mus, tanpura_pluck(pat[i % 4]), t, .09 if not (44.4 < t < 53.5) else .05, pan=-.3 + .2 * (i % 4))
# hook
add(fx, bell(760, 1), .15, .38); add(fx, ge(1), .18, .5); add(fx, sfx.whoosh(.35), 1.4, .1)
for i, t in enumerate([3.5, 3.75, 4.0, 4.25]): add(fx, bell(SA * 4 * BHUPALI[i + 1], 1, 2.5), t, .14, pan=-.3 + i * .2)
# the forest: wind, birds, footsteps
add(mus, lp(noise(37.5), 700) * .35, 6.0, .35); add(fx, sfx.whoosh(.6), 5.9, .12)
for k in range(14): add(mus, chirp(), 6.5 + k * 1.9 + rng.random() * .8, .08, pan=rng.random() * 1.6 - .8)
for k in range(5): add(fx, sfx.step(.7), 7.95 + k * .43, .22)
for i, t in enumerate([9.9, 10.1, 10.3, 10.5]): add(fx, bell(SA * 8 * BHUPALI[i + 1], 1, 2.2), t, .1, pan=.4)   # the Vidyadhari
for k in range(8): add(fx, tanpura_pluck(SA * 4 * BHUPALI[k % 6], 1.4), 13.6 + k * .32, .06, pan=-.5 + k * .14)  # the fragrance
add(fx, bell(SA * 6, 1, 2.5), 17.0, .16); add(fx, sfx.whoosh(.6), 18.2, .1)
for k in range(4): add(fx, ge(1, 52), 18.8 + k * .45, .3)                                # Airavata's steps
add(fx, trumpet(), 19.3, .2)
add(fx, bell(SA * 6, 1, 2.5), 20.6, .14); add(fx, na(1, 520), 22.3, .2); add(fx, bell(SA * 5, 1, 2.5), 24.5, .12)
add(fx, sfx.creak(1), 26.9, .2); add(fx, sfx.creak(1), 27.6, .16); add(fx, swish(.9), 28.4, .14)
add(fx, sfx.whoosh(.4), 30.7, .25); add(fx, ge(1, 70), 31.33, .5); add(fx, leather(), 31.36, .3)
# anger: fire, heartbeat, the curse
add(mus, crackle(10.4), 33.0, .3); add(mus, sfx.rumble(10.0), 33.2, .35)
for k in range(10): add(mus, ge(1, 58), 33.4 + k * .74, .18)
add(fx, ge(1, 62), 35.6, .45); add(fx, na(1, 460), 36.55, .22)
add(fx, ge(1, 50), 40.6, .4); add(fx, sfx.crash(.7), 40.62, .08); add(fx, sfx.rumble(2.5), 40.84, .22); add(fx, bell(SA * 2, 1, 4.5), 40.9, .22)
# the curse takes hold
add(fx, sfx.whoosh(.6), 44.2, .1)
add(fx, hp(noise(1.2), 2500) * np.exp(-t_(1.2) / .4), 45.85, .12)                      # the fire hisses out
for k in range(5): add(fx, tanpura_pluck(SA * 2 * BHUPALI[4 - k], 1.6), 47.2 + k * .22, .07)   # wilting: a falling line
add(fx, ge(1, 46), 49.0, .4)
for k in range(10): add(fx, ge(1, 70) if k % 2 == 0 else na(1, 420), 51.2 + k * .12, .2)   # the daityas charge
add(fx, ge(1, 55), 51.95, .45); add(fx, leather(), 52.0, .2)
# one garland… the ocean
add(fx, bell(SA * 4, 1, 4), 54.05, .26)
add(mus, lp(sfx.brown(3.2), 400) * np.sin(np.pi * t_(3.2) / 3.2), 56.25, .5); add(fx, sfx.rumble(1.6), 56.6, .3)
# end card
add(fx, ge(1, 80), 59.95, .5); add(fx, bell(SA * 4, 1, 4), 60.0, .25)
for i, t in enumerate([61.4, 61.6, 61.8, 62.0]): add(fx, bell(SA * 4 * BHUPALI[i + 1], 1, 3), t, .14, pan=-.3 + i * .2)
add(fx, shankh(233, 2.6), 63.4, .4); add(fx, bell(SA * 6, 1, 4), 63.45, .2)

# hard silence 31.84–32.98: bed to digital zero (fx keeps its single tap)
s0, s1 = int(31.84 * SR), int(32.98 * SR); mus[s0:s1] = 0
# duck the bed under the voice (~9 dB)
env = np.abs(voice); k = int(.12 * SR); env = np.convolve(env, np.ones(k) / k, 'same'); env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
duck = np.ones(len(mus)); n = min(len(env), len(duck)); duck[:n] = 1 - .72 * env[:n]
mus *= duck[:, None]
out = mus * .32 + fx * .42
add(out, voice, 0.0, 1.0)
# fade-out with the lamp being carried away
f0 = int(64.6 * SR); out[f0:] *= np.linspace(1, 0, len(out) - f0)[:, None]
out = sfx.limit(out * .9, .95) if out.ndim == 1 else np.stack([sfx.limit(out[:, 0] * .9, .95), sfx.limit(out[:, 1] * .9, .95)], 1)
wavfile.write(P / 'audio/mix.wav', SR, out.astype(np.float32))
print('mix.wav', out.shape[0] / SR, 's  peak', float(np.abs(out).max()))

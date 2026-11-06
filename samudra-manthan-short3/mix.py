"""Soundtrack for Short 3: the user's voice + a hand-made Indian palette (synthesised, no samples).
Run from the library root:  .venv/bin/python -I <project>/mix.py <project>
Writes <project>/audio/mix.wav (48 kHz stereo, float)."""
import sys, subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
sys.path.insert(0, str(Path.cwd() / 'core' / 'audio'))
import sfx
from sfx import SR, t_, noise, bp, lp, hp, norm, add

P = Path(sys.argv[1]); DUR = 60.0
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

# tanpura drone throughout, cut for the pause after the fourth form
pat = [SA * .75, SA * 2, SA * 2, SA]
for i, t in enumerate(np.arange(0.2, DUR - 1.5, .62)):
    if 43.2 < t < 44.3: continue
    add(mus, tanpura_pluck(pat[i % 4]), t, .09, pan=-.3 + .2 * (i % 4))
# hook
add(fx, bell(760, 1), .15, .38); add(fx, ge(1), .18, .5); add(fx, sfx.whoosh(.35), 1.35, .1)
for i, t in enumerate([3.6, 4.0, 4.4, 4.8]): add(fx, bell(SA * 4 * BHUPALI[i + 1], 1, 2.5), t, .15, pan=(-.6, .6, -.3, .3)[i])
# the churning gathers
add(mus, lp(sfx.brown(3.0), 400) * np.sin(np.pi * t_(3.0) / 3.0), 6.7, .5); add(fx, sfx.whoosh(.5), 6.8, .1)
for t in [8.6, 8.8, 9.2, 9.4]: add(fx, sfx.whoosh(.28), t, .07)
add(fx, ge(1, 66), 10.0, .5); add(fx, sfx.rumble(1.4), 10.0, .28)
add(fx, bp(noise(1.0), 2500, 7000) * np.exp(-t_(1.0) / .35), 11.95, .1)          # Vasuki's hiss
beat = 60 / 92
for k in range(int((54.2 - 14.5) / beat * 2)):
    t = 14.5 + k * beat / 2
    if 43.2 < t < 44.3: continue
    stroke = ['ge', 'na', 'na', 'ge', 'na', 'ge', 'na', 'na'][k % 8]
    add(mus, ge(1, 85) if stroke == 'ge' else na(1, 500 + 40 * (k % 3)), t, .24 if stroke == 'ge' else .1, pan=(-.2 if stroke == 'ge' else .2))
for k in range(int((54.2 - 14.7) / (1 / 1.1))):
    t = 14.7 + k / 1.1
    if 43.2 < t < 44.3: continue
    add(mus, sfx.creak(.8), t, .09, pan=.1); add(mus, swish(.8), t + .1, .08, pan=-.2)
for i, t in enumerate(np.linspace(16.8, 18.4, 7)): add(fx, bell(SA * 4 * BHUPALI[i % 6], 1, 2.2), t, .1, pan=-.6 + i * .2)   # the Lord takes charge
# the four forms: a stroke on each "रूप", a bell when each form appears
for t in [19.79, 29.28, 34.55, 37.79]: add(fx, na(1, 480), t, .22)
add(fx, ge(1, 52), 20.8, .38); add(fx, lp(noise(1.2), 900) * np.exp(-t_(1.2) / .3), 20.8, .16)   # Kurma rises: a deep splash
add(fx, bell(SA * 2, 1, 4), 21.0, .2)
add(fx, bell(SA * 4, 1, 3.5), 30.6, .18, pan=.5); add(fx, sfx.whoosh(.4), 30.5, .08)
add(fx, bell(SA * 3, 1, 3.5), 35.7, .18, pan=-.5); add(fx, sfx.whoosh(.4), 35.6, .08)
add(fx, ge(1, 48), 39.0, .5); add(fx, bell(SA * 1.5, 1, 4.5), 39.05, .24); add(fx, sfx.rumble(1.8), 39.0, .22)
# the unseen strength: a shower of tiny chimes
for k in range(40): add(fx, bell(SA * 8 * BHUPALI[k % 6] * (1 + (k % 3)), 1, 1.2), 44.3 + k * .13 + rng.random() * .05, .035, pan=rng.random() * 1.6 - .8)
# नीचे भी (low) · ऊपर भी (high) · दोनों ओर भी (left and right)
add(fx, bell(SA, 1, 3.5), 51.37, .26); add(fx, bell(SA * 8, 1, 3), 52.43, .2)
add(fx, bell(SA * 4, 1, 3), 53.33, .2, pan=-.8); add(fx, bell(SA * 4 * 1.5, 1, 3), 53.38, .2, pan=.8)
# end card
add(fx, sfx.whoosh(.5), 54.3, .1); add(fx, ge(1, 80), 54.76, .5); add(fx, bell(SA * 4, 1, 4), 54.8, .25)
for i, t in enumerate([56.1, 56.3, 56.5, 56.7]): add(fx, bell(SA * 4 * BHUPALI[i + 1], 1, 3), t, .13, pan=-.3 + i * .2)
add(fx, shankh(233, 1.8), 58.98, .36); add(fx, bell(SA * 6, 1, 3.5), 58.15, .14)

# hard silence 43.24–44.25: bed to digital zero (fx keeps its single tap)
s0, s1 = int(43.24 * SR), int(44.25 * SR); mus[s0:s1] = 0
# duck the bed under the voice (~9 dB)
env = np.abs(voice); k = int(.12 * SR); env = np.convolve(env, np.ones(k) / k, 'same'); env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
duck = np.ones(len(mus)); n = min(len(env), len(duck)); duck[:n] = 1 - .72 * env[:n]
mus *= duck[:, None]
out = mus * .32 + fx * .42
add(out, voice, 0.0, 1.0)
# fade-out with the lamp being carried away
f0 = int(59.5 * SR); out[f0:] *= np.linspace(1, 0, len(out) - f0)[:, None]
out = sfx.limit(out * .9, .95) if out.ndim == 1 else np.stack([sfx.limit(out[:, 0] * .9, .95), sfx.limit(out[:, 1] * .9, .95)], 1)
wavfile.write(P / 'audio/mix.wav', SR, out.astype(np.float32))
print('mix.wav', out.shape[0] / SR, 's  peak', float(np.abs(out).max()))

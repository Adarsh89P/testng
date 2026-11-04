"""Soundtrack for Short 1: the user's voice + a hand-made Indian palette (synthesised, no samples).
Run from the library root:  .venv/bin/python -I <project>/mix.py <project>
Writes <project>/audio/mix.wav (48 kHz stereo, float)."""
import sys, subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
sys.path.insert(0, str(Path.cwd() / 'core' / 'audio'))
import sfx
from sfx import SR, t_, noise, bp, lp, hp, norm, add

P = Path(sys.argv[1]); DUR = 57.0
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

# tanpura drone throughout (Pa · Sa' · Sa' · Sa), cut for the silence and the poison's darkest moment
pat = [SA * .75, SA * 2, SA * 2, SA]
for i, t in enumerate(np.arange(0.2, DUR - 1.5, .62)):
    if 45.6 < t < 46.8: continue
    add(mus, tanpura_pluck(pat[i % 4] / 1), t, .09 if not (30 < t < 34.5) else .05, pan=-.3 + .2 * (i % 4))

# hook
add(fx, bell(760, 1), .12, .38); add(fx, ge(1), .15, .6)
add(fx, sfx.whoosh(.35), .25, .12)
add(fx, ge(1.0, 80), 4.22, .4); add(fx, na(1, 480), 4.29, .35)          # "भगवान शिव ने नहीं"
add(fx, leather(), 6.25, .25); add(fx, sfx.whoosh(.3), 6.3, .1)
add(fx, na(.9, 560), 7.82, .3)                                           # "विष्णु पुराण"
add(fx, leather(), 9.75, .25)
# the churning: press-ons, then a keherwa groove and the creak of the mountain
for t in [10.0, 10.2, 10.8, 11.0]: add(fx, sfx.whoosh(.28), t, .08)
add(fx, ge(1, 70), 12.2, .55); add(fx, sfx.rumble(1.2), 12.2, .25)        # Mandara
add(fx, ge(1, 75), 14.0, .45)                                            # Vasuki
beat = 60 / 92
for k in range(int((21.3 - 15.6) / beat * 2)):
    t = 15.6 + k * beat / 2; stroke = ['ge', 'na', 'na', 'ge', 'na', 'ge', 'na', 'na'][k % 8]
    add(mus, ge(1, 85) if stroke == 'ge' else na(1, 500 + 40 * (k % 3)), t, .32 if stroke == 'ge' else .14, pan=(-.2 if stroke == 'ge' else .2))
for k in range(int((21.3 - 15.8) / (1 / 1.2))):
    t = 15.8 + k / 1.2; add(mus, sfx.creak(.8), t, .12, pan=.1); add(mus, swish(.8), t + .1, .1, pan=-.2)
add(mus, hp(noise(4.4), 3000) * .2, 16.9, .25)                                  # rain over the devas
add(fx, leather(), 21.3, .2)
# the treasures: a rising bell arpeggio, one note per treasure
for i, t in enumerate([21.79, 22.82, 24.11, 25.07]): add(fx, bell(SA * 4 * BHUPALI[i + 1], 1, 3.0), t, .26, pan=-.4 + i * .25); add(fx, sfx.whoosh(.4), t - .1, .07)
add(fx, ge(1, 82), 26.63, .5); add(fx, na(1, 450), 26.65, .25); add(fx, bell(SA * 8, 1, 3.5), 27.6, .2)   # moon on the trident
# the poison: lamps snuffed, a low rumble, heartbeat strokes, crash hits
for k in range(3): add(fx, leather(.8), 29.8 + k * .4, .18)
add(mus, sfx.rumble(4.8) * 1.0, 29.8, .35)
for k in range(8): add(mus, ge(1, 60), 30.0 + k * .62, .2 - k * .01)
add(fx, ge(1, 55), 31.82, .4); add(fx, ge(1, 55), 32.9, .4)
# most tellings: Shiva's trident, a bell; "नीलकंठ"
add(fx, sfx.whoosh(.35), 34.6, .1); add(fx, bell(SA * 3, 1, 3.5), 34.75, .22); add(fx, bell(SA * 6, 1, 3), 38.1, .2)
# but the Vishnu Purana: a decisive stroke, the Nagas rise, then a hard silence
add(fx, ge(1, 70), 39.78, .45); add(fx, na(1, 520), 39.84, .35); add(fx, leather(), 39.85, .25)
for k in range(5): add(fx, sfx.whoosh(.3), 43.5 + k * .14, .07, pan=-.6 + k * .3)
add(fx, ge(1, 65), 43.58, .6)
add(fx, na(.7, 600), 46.15, .2)                                          # the one sound inside the silence
# many Puranas, end card
for t in [46.8, 48.03, 49.22]: add(fx, na(1, 500), t, .22); add(fx, leather(.7), t, .12)
add(fx, ge(1, 80), 50.92, .6); add(fx, bell(SA * 4, 1, 4), 50.95, .3)
add(fx, shankh(233, 2.8), 54.3, .42); add(fx, bell(SA * 4 * 1.5, 1, 4), 54.35, .22)

# hard silence 45.64–46.77: bed to digital zero (fx keeps its single tap)
s0, s1 = int(45.64 * SR), int(46.77 * SR); mus[s0:s1] = 0
# duck the bed under the voice (~9 dB)
env = np.abs(voice); k = int(.12 * SR); env = np.convolve(env, np.ones(k) / k, 'same'); env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
duck = np.ones(len(mus)); n = min(len(env), len(duck)); duck[:n] = 1 - .72 * env[:n]
mus *= duck[:, None]
out = mus * .32 + fx * .42
add(out, voice, 0.0, 1.0)
# fade-out with the lamp being carried away
f0 = int(55.8 * SR); out[f0:] *= np.linspace(1, 0, len(out) - f0)[:, None]
out = sfx.limit(out * .9, .95) if out.ndim == 1 else np.stack([sfx.limit(out[:, 0] * .9, .95), sfx.limit(out[:, 1] * .9, .95)], 1)
wavfile.write(P / 'audio/mix.wav', SR, out.astype(np.float32))
print('mix.wav', out.shape[0] / SR, 's  peak', float(np.abs(out).max()))

"""Soundtrack for Shorts 5–9 (pass the episode number): the user's voice + a hand-made Indian palette (synthesised, no samples).
Run from the library root:  .venv/bin/python -I <project>/mix.py <project>
Writes <project>/audio/mix.wav (48 kHz stereo, float)."""
import sys, subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
sys.path.insert(0, str(Path.cwd() / 'core' / 'audio'))
import sfx
from sfx import SR, t_, noise, bp, lp, hp, norm, add

P = Path(sys.argv[1]); EP = sys.argv[2]; DUR = {'5': 57.9, '6': 56.0, '7': 60.2, '8': 56.0, '9': 51.0}[EP]
rng = np.random.default_rng(11)

# —— voice ——
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(P / f'audio/voice{EP}.mp3'), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
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
def trumpet(v=1.0):
    d = 1.1; tt = t_(d); f = 260 + 340 * np.clip(tt / .35, 0, 1) - 60 * np.clip((tt - .7) / .4, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * (1 + .02 * np.sin(2 * np.pi * 9 * tt))) / SR; saw = sum(np.sin(k * ph) / k for k in range(1, 24))
    return norm(bp(saw, 400, 3200) * np.clip(tt / .08, 0, 1) * np.clip((d - tt) / .3, 0, 1)) * v
def chimes(t0, t1, n=12, base=8, gain=.04, pan=0):
    for k in range(n): add(fx, bell(SA * base * BHUPALI[k % 6] * (1 + (k % 3)), 1, 1.3), t0 + (t1 - t0) * k / n + rng.random() * .05, gain, pan=pan + rng.random() * .8 - .4)
def arp(t0, step=.2, gain=.13, base=4, n=4):
    for i in range(n): add(fx, bell(SA * base * BHUPALI[i + 1], 1, 2.8), t0 + i * step, gain, pan=-.3 + i * .2)
def groove(t0, t1, gain=1.0):
    beat = 60 / 92
    for k in range(int((t1 - t0) / beat * 2)):
        t = t0 + k * beat / 2; st = ['ge', 'na', 'na', 'ge', 'na', 'ge', 'na', 'na'][k % 8]
        add(mus, ge(1, 85) if st == 'ge' else na(1, 500 + 40 * (k % 3)), t, (.22 if st == 'ge' else .09) * gain, pan=(-.2 if st == 'ge' else .2))
def churnfx(t0, t1):
    groove(t0, t1)
    for k in range(int((t1 - t0) / (1 / 1.1))): t = t0 + .2 + k / 1.1; add(mus, sfx.creak(.8), t, .08, pan=.1); add(mus, swish(.8), t + .1, .07, pan=-.2)
def endcard(t_title, t_vishnu, t_conch, dconch=1.6):
    add(fx, sfx.whoosh(.5), t_title - .3, .1); add(fx, ge(1, 80), t_title, .45); add(fx, bell(SA * 4, 1, 4), t_title + .04, .24)
    arp(t_vishnu); add(fx, shankh(233, dconch), t_conch, .34)
# tanpura drone throughout
pat = [SA * .75, SA * 2, SA * 2, SA]
for i, t in enumerate(np.arange(0.2, DUR - 1.2, .62)): add(mus, tanpura_pluck(pat[i % 4]), t, .09, pan=-.3 + .2 * (i % 4))
add(fx, bell(760, 1), .15, .3); add(fx, ge(1, 60), .2, .4)

if EP == '5':
    add(fx, sfx.whoosh(.35), 1.35, .1); churnfx(.2, 14.1); chimes(10.3, 13.8, 10)
    for t, b in [(15.4, 2), (25.68, 3), (28.11, 4), (34.75, 5), (38.93, 6)]: add(fx, bell(SA * b * 1.5, 1, 3.2), t, .22); add(fx, sfx.whoosh(.4), t - .1, .07)
    add(mus, lp(sfx.brown(1.2), 500), 15.3, .3)
    groove(20.97, 24.3, .8); add(fx, ge(1, 62), 42.19, .4); add(fx, bell(SA * 1.5, 1, 4), 42.25, .2); add(fx, bell(SA * 8, 1, 3), 44.0, .14)
    chimes(46.1, 49.4, 14); add(mus, lp(sfx.brown(2.4), 400) * np.sin(np.pi * t_(2.4) / 2.4), 49.8, .45); add(fx, bell(SA * 2, 1, 4.5), 50.0, .2)
    endcard(52.70, 54.06, 56.97, 1.0)
if EP == '6':
    add(fx, sfx.whoosh(.35), 1.4, .1); chimes(.8, 4.6, 10); churnfx(5.6, 14.2)
    add(mus, sfx.rumble(3.8), 9.9, .35); add(fx, hp(noise(1.2), 2500) * np.exp(-t_(1.2) / .4), 9.95, .08)
    for k in range(3): add(fx, sfx.whoosh(.3), 11.4 + k * .12, .07)
    add(fx, lp(noise(1.3), 900) * np.exp(-t_(1.3) / .35), 15.9, .25); add(fx, ge(1, 52), 15.9, .4); add(fx, bell(SA * 2, 1, 4.5), 16.0, .24); chimes(16.2, 19.6, 10)
    add(fx, bell(SA * 4, 1, 3.5), 26.5, .2); arp(23.6, .25, .08, 8)
    for k in range(10): add(fx, ge(1, 80) if k % 2 == 0 else na(1, 520), 29.0 + k * .12, .16)
    chimes(34.0, 39.2, 16)
    for k in range(6): add(fx, tanpura_pluck(SA * 4 * BHUPALI[k % 6], 1.4), 40.0 + k * .4, .05, pan=-.5 + k * .2)
    for k in range(5): add(mus, ge(1, 58), 46.1 + k * .74, .18)
    add(fx, na(1, 460), 47.65, .2)
    endcard(50.57, 51.98, 54.99, 1.0)
if EP == '7':
    add(fx, sfx.whoosh(.35), 1.45, .1); chimes(1.0, 6.8, 10); add(fx, bell(SA * 6, 1, 3), 5.2, .16)
    add(mus, lp(sfx.brown(3.0), 400) * np.sin(np.pi * t_(3.0) / 3.0), 7.2, .45)
    add(mus, lp(sfx.brown(1.6), 500), 10.3, .3); chimes(13.7, 17.4, 10)
    add(fx, ge(1, 50), 17.87, .45); add(fx, bell(SA * 1.5, 1, 5), 17.9, .26); arp(18.1, .2, .12, 4)
    add(fx, bell(SA * 2, 1, 4), 20.9, .16); add(fx, bell(SA * 3, 1, 4), 22.1, .12)
    groove(24.06, 27.2, 1.0)
    add(mus, lp(noise(3.0), 1200) * np.sin(np.pi * t_(3.0) / 3.0) * .7, 27.6, .3, pan=-.4)
    add(fx, trumpet(), 30.8, .14, pan=-.6); add(fx, trumpet(), 31.3, .14, pan=.6); add(mus, lp(noise(4.0), 1400) * np.sin(np.pi * t_(4.0) / 4.0) * .6, 31.5, .26)
    add(fx, bell(SA * 4, 1, 3.5), 35.8, .16); chimes(39.9, 42.3, 12)
    add(fx, ge(1, 62), 42.96, .35); arp(45.7, .5, .12, 4); add(fx, bell(SA * 2, 1, 4.5), 48.8, .22)
    add(mus, lp(sfx.brown(2.8), 300) * np.sin(np.pi * t_(2.8) / 2.8), 50.4, .4); add(fx, bell(SA * 8, 1, 3.5), 53.63, .22); chimes(53.7, 54.9, 8)
    endcard(55.16, 56.56, 59.45, .7)
if EP == '8':
    add(fx, sfx.whoosh(.35), 1.4, .1); chimes(4.3, 5.6, 10); add(fx, bell(SA * 6, 1, 3), 4.4, .18)
    add(fx, bell(SA * 4, 1, 3.5), 9.6, .16); chimes(10.0, 12.2, 8)
    add(mus, sfx.rumble(5.0), 12.6, .3); add(fx, ge(1, 55), 12.64, .4)
    add(fx, sfx.whoosh(.4), 15.9, .14); add(fx, na(1, 460), 17.4, .22)
    for k in range(9): add(mus, ge(1, 56), 20.0 + k * .74, .16)
    add(fx, bell(SA * 2, 1, 4), 26.6, .14); chimes(27.3, 28.6, 14); add(fx, bell(SA * 6, 1, 3.5), 27.5, .22)
    for k in range(10): add(fx, tanpura_pluck(SA * 4 * BHUPALI[(k * 2) % 6], 1.4), 31.8 + k * .3, .05, pan=-.6 + k * .12)
    add(fx, sfx.whoosh(.5), 35.9, .1); add(fx, bell(SA * 4, 1, 3), 38.0, .16)
    chimes(39.25, 41.7, 12)
    add(fx, ge(1, 58), 42.2, .4); add(fx, ge(1, 58), 43.1, .35); add(mus, sfx.rumble(2.4), 44.2, .32)
    add(fx, bell(SA * 1.5, 1, 4.5), 47.1, .2); add(fx, bell(SA * 6, 1, 3), 48.4, .16)
    endcard(50.68, 52.12, 55.14, .8)
if EP == '9':
    add(fx, sfx.whoosh(.35), 1.4, .1); chimes(1.0, 6.6, 12)
    for k in range(10): add(fx, ge(1, 80) if k % 2 == 0 else na(1, 520), 8.65 + k * .14, .16)
    add(fx, ge(1, 62), 11.73, .4); add(fx, bell(SA * 3, 1, 4), 11.8, .2)
    add(fx, bell(SA * 4, 1, 3.5), 15.0, .16); arp(19.7, .2, .12, 4); add(fx, bell(SA * 6, 1, 3), 21.75, .14)
    add(fx, na(1, 480), 23.1, .2)
    add(fx, bell(SA * 6, 1, 3), 25.96, .18); add(fx, bell(SA * 3, 1, 3.5), 26.8, .18); add(fx, bell(SA * 1.5, 1, 4), 27.6, .2)
    add(fx, bell(SA * 4, 1, 3.5), 30.6, .18); chimes(31.0, 35.0, 12)
    chimes(35.9, 37.6, 18, 8, .045)
    add(mus, lp(sfx.brown(3.0), 300) * np.sin(np.pi * t_(3.0) / 3.0), 38.2, .4)
    arp(41.3, .4, .12, 4); add(fx, bell(SA * 8, 1, 3.5), 43.0, .2); chimes(43.0, 45.2, 10)
    add(fx, ge(1, 70), 45.6, .45); add(fx, bell(SA * 2, 1, 5), 45.65, .24)
    add(fx, shankh(233, .8), 50.15, .32)

# hard silence 20.71–21.88: bed to digital zero (fx keeps its single tap)
pass
# duck the bed under the voice (~9 dB)
env = np.abs(voice); k = int(.12 * SR); env = np.convolve(env, np.ones(k) / k, 'same'); env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
duck = np.ones(len(mus)); n = min(len(env), len(duck)); duck[:n] = 1 - .72 * env[:n]
mus *= duck[:, None]
out = mus * .32 + fx * .42
add(out, voice, 0.0, 1.0)
# fade-out with the lamp being carried away
f0 = int((DUR - .7) * SR); out[f0:] *= np.linspace(1, 0, len(out) - f0)[:, None]
out = sfx.limit(out * .9, .95) if out.ndim == 1 else np.stack([sfx.limit(out[:, 0] * .9, .95), sfx.limit(out[:, 1] * .9, .95)], 1)
wavfile.write(P / f'audio/mix{EP}.wav', SR, out.astype(np.float32))
print('mix.wav', out.shape[0] / SR, 's  peak', float(np.abs(out).max()))

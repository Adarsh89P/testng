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

P = Path(sys.argv[1]); EP = sys.argv[2]; DUR = {'1': 48.6, '2': 52.3, '3': 48.1, '4': 47.9, '5': 49.5, '6': 51.5, '7': 47.7, '8': 45.8, '9': 51.3, '10': 54.2}[EP]
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

def crackle(d, v=1.0):   # fire: low roar + random pops
    x = lp(noise(d), 700) * .6
    for _ in range(int(d * 14)):
        i = int(rng.uniform(0, d - .05) * SR); n = int(.012 * SR); x[i:i + n] += hp(noise(.012), 2000)[:n] * rng.uniform(.5, 1.5)
    return x * v
def anger(t):   # the king's order: low drum hit + dark swell
    add(fx, ge(1, 48), t, .5); add(mus, lp(sfx.brown(1.6), 300) * np.sin(np.pi * t_(1.6) / 1.6), t - .2, .45); add(fx, sfx.whoosh(.4), t - .15, .1)
def crack(t, v=.3):   # something breaks
    add(fx, hp(noise(.25), 1800) * np.exp(-t_(.25) / .05), t, v); add(fx, ge(1, 70), t, .35)
if EP == '1':
    add(fx, sfx.whoosh(.35), 1.39, .1); anger(1.5); chimes(5.3, 8.2, 10); add(fx, bell(SA * 4, 1, 3.5), 5.3, .18)
    anger(9.0); groove(9.2, 14.5, .8); add(mus, lp(sfx.brown(5.0), 380), 15.2, .3)
    add(fx, bell(SA * 2, 1, 4.5), 22.27, .22); add(fx, shankh(233, .9), 24.96, .28); chimes(26.2, 30.5, 14); arp(27.2, .3, .1, 8)
    add(fx, ge(1, 52), 31.11, .4); chimes(33.7, 37.2, 12)
    add(fx, ge(1, 46), 39.49, .45); add(fx, bell(SA * 4, 1, 4), 40.41, .22); add(fx, sfx.whoosh(.4), 41.7, .08)
    endcard(46.6, 46.9, 47.75, .8)
if EP == '2':
    add(fx, sfx.whoosh(.35), 1.36, .1); chimes(4.5, 6.8, 10); add(fx, bell(SA * 4, 1, 3.5), 6.2, .18)
    for k in range(6): add(fx, tanpura_pluck(SA * 4 * BHUPALI[k % 6], 1.4), 7.8 + k * .5, .05, pan=-.5 + k * .2)
    add(fx, bell(SA * 1.5, 1, 4), 12.63, .18); add(fx, na(1, 520), 16.6, .16)
    add(fx, bell(SA * 2, 1, 4.5), 20.99, .2); chimes(23.4, 31.5, 18); arp(26.9, .3, .1, 8); add(fx, shankh(233, 1.0), 29.2, .22)
    anger(32.27); for_ = [add(mus, ge(1, 56), 34.8 + k * .74, .16) for k in range(5)]
    add(fx, bell(SA * 4, 1, 4), 42.93, .2); chimes(42.9, 45.5, 10)
    crack(47.84, .25); add(mus, sfx.rumble(2.0), 47.84, .3)
    endcard(50.4, 50.6, 51.3, .9)
if EP == '3':
    add(fx, sfx.whoosh(.35), 1.43, .1); anger(1.6)
    add(fx, bell(SA * 1.5, 1, 4), 6.93, .16); anger(14.76)
    groove(16.6, 20.0, 1.0); add(mus, lp(noise(3.4), 1200) * np.sin(np.pi * t_(3.4) / 3.4) * .7, 16.6, .3)
    for k in range(8): add(fx, hp(noise(.08), 3000) * np.exp(-t_(.08) / .02), 20.6 + k * .6, .12, pan=(-.5 if k % 2 else .5))
    chimes(20.6, 25.2, 12); add(fx, bell(SA * 4, 1, 4), 25.69, .2)
    add(fx, hp(noise(1.6), 3500) * np.sin(np.pi * t_(1.6) / 1.6), 29.1, .14)
    for k in range(4): add(fx, hp(noise(.5), 4000) * np.exp(-t_(.5) / .15), 31.4 + k * .5, .1, pan=-.6 + k * .4)
    crack(33.9); crack(34.3, .2); chimes(35.6, 37.3, 10)
    add(fx, bell(SA * 2, 1, 4.5), 37.95, .22); arp(38.0, .4, .1, 4)
    add(fx, trumpet(), 44.67, .12)
    endcard(46.2, 46.4, 47.0, .9)
if EP == '4':
    add(fx, sfx.whoosh(.35), 1.35, .1); add(fx, trumpet(), 1.6, .1, pan=-.5)
    add(fx, bell(SA * 1.5, 1, 4), 5.91, .16); anger(11.97)
    for k in range(4): add(mus, ge(1, 44), 17.64 + k * .5, .3)
    add(fx, trumpet(), 18.0, .14, pan=-.6); add(fx, trumpet(), 18.6, .14, pan=.6); add(mus, sfx.rumble(2.0), 20.2, .35)
    add(mus, lp(sfx.brown(4.0), 300) * np.sin(np.pi * t_(4.0) / 4.0), 21.0, .4)
    chimes(25.0, 29.0, 14); add(fx, bell(SA * 2, 1, 4.5), 27.17, .2)
    crack(30.37, .35); crack(30.6, .25); add(fx, trumpet(), 31.0, .12, pan=.4)
    add(fx, bell(SA * 4, 1, 4), 36.88, .18); arp(37.0, .4, .1, 4)
    crack(40.97, .15); add(fx, bell(SA * 4, 1, 4), 42.05, .22)
    add(mus, crackle(2.2, .6), 43.31, .25)
    endcard(45.9, 46.1, 46.95, .9)
if EP == '5':
    add(fx, sfx.whoosh(.35), 1.29, .1); add(mus, crackle(3.5, .5), 3.0, .2)
    add(fx, bell(SA * 1.5, 1, 4), 7.34, .16); anger(10.56); anger(14.21)
    groove(17.25, 20.0, .8); add(mus, crackle(8.0, 1.0) * np.minimum(1, t_(8.0) / 3)[:, None] if False else crackle(8.0, 1.0) * np.minimum(1, t_(8.0) / 3), 19.8, .45)
    add(mus, lp(noise(2.0), 900) * np.sin(np.pi * t_(2.0) / 2.0), 20.1, .3)
    add(fx, bell(SA * 2, 1, 4.5), 25.17, .2); chimes(27.5, 33.0, 20); arp(29.8, .35, .1, 8)
    add(fx, na(1, 460), 34.1, .16); add(fx, bell(SA * 4, 1, 4), 38.71, .2); chimes(40.3, 43.0, 12)
    for k in range(3): add(fx, bell(SA * (2, 3, 4)[k], 1, 3), 43.92 + k * .4, .14)
    endcard(47.5, 47.7, 48.6, .8)

if EP == '6':
    add(fx, sfx.whoosh(.35), 1.34, .1); add(mus, crackle(3.0, .6), 3.0, .2); chimes(5.9, 7.7, 10)
    add(fx, bell(SA * 1.5, 1, 4), 8.58, .16)
    for k in range(8): add(fx, ge(1, 66) if k % 2 == 0 else na(1, 480), 14.2 + k * .5, .14)
    add(mus, crackle(5.0, 1.0), 15.0, .4); anger(18.6); add(mus, sfx.rumble(2.0), 18.6, .3)
    add(fx, sfx.whoosh(.5), 20.4, .14); crack(23.7, .35); crack(24.3, .25); chimes(24.3, 27.0, 10)
    add(mus, crackle(13.0, 1.0), 28.5, .4); add(fx, sfx.whoosh(.4), 27.9, .12)
    add(fx, bell(SA * 2, 1, 4.5), 35.6, .2); arp(36.0, .4, .1, 6); chimes(40.9, 43.5, 16); add(fx, shankh(233, 1.0), 42.9, .24)
    chimes(45.7, 49.2, 12)
    endcard(49.6, 49.8, 50.6, .8)
if EP == '7':
    add(fx, sfx.whoosh(.6), 2.0, .12); chimes(4.4, 5.5, 8)
    add(fx, bell(SA * 1.5, 1, 4), 6.24, .16); anger(10.81); add(fx, na(1, 400), 12.5, .14)
    chimes(13.6, 18.6, 12); add(fx, bell(SA * 4, 1, 3.5), 16.33, .16)
    add(fx, sfx.whoosh(1.4), 21.0, .18); add(mus, lp(noise(3.0), 1100) * np.sin(np.pi * t_(3.0) / 3.0) * .7, 20.6, .25)
    add(fx, ge(1, 52), 23.99, .35); add(fx, bell(SA * 2, 1, 5), 24.0, .22); chimes(24.2, 27.8, 14)
    anger(28.67); add(mus, lp(sfx.brown(4.0), 260) * np.sin(np.pi * t_(4.0) / 4.0), 29.0, .45)
    add(fx, shankh(233, .9), 32.6, .24); add(fx, sfx.whoosh(.6), 32.7, .14)
    for k in range(6): add(fx, hp(noise(.2), 2500) * np.exp(-t_(.2) / .05), 33.6 + k * .7, .14); add(fx, bell(SA * 4 * BHUPALI[k % 6], 1, 1.4), 33.62 + k * .7, .08)
    add(mus, lp(noise(4.0), 1400) * np.sin(np.pi * t_(4.0) / 4.0) * .8, 38.5, .35)
    add(fx, bell(SA * 2, 1, 4.5), 41.4, .2); chimes(42.0, 45.3, 12)
    endcard(45.9, 46.1, 46.85, .8)
if EP == '8':
    add(fx, sfx.whoosh(.35), 1.35, .1); chimes(1.6, 5.8, 10)
    for k in range(6): add(fx, tanpura_pluck(SA * 4 * BHUPALI[k % 6], 1.4), 8.3 + k * .5, .05, pan=-.5 + k * .2)
    for k, tt in enumerate([17.44, 18.4, 19.2]): add(fx, bell(SA * (2, 1.5, 1)[k], 1, 3), tt, .14)
    add(mus, lp(sfx.brown(2.0), 300) * np.sin(np.pi * t_(2.0) / 2.0), 22.4, .3)
    add(fx, bell(SA * 2, 1, 4.5), 24.94, .2); chimes(25.0, 28.9, 14); arp(26.0, .4, .1, 4)
    add(fx, ge(1, 60), 29.61, .3); add(fx, na(1, 520), 32.19, .16)
    chimes(34.1, 38.5, 14); groove(39.2, 43.5, .7)
    endcard(44.0, 44.2, 45.0, .7)
if EP == '9':
    add(fx, sfx.whoosh(.35), 1.36, .1); add(mus, lp(noise(5.0), 600) * np.sin(np.pi * t_(5.0) / 5.0) * .7, 1.5, .3)
    add(fx, bell(SA * 1.5, 1, 4), 7.59, .16); anger(11.12)
    for k in range(3): add(fx, hp(noise(.5), 3500) * np.exp(-t_(.5) / .15), 14.0 + k * .5, .1)
    add(fx, lp(noise(1.2), 900) * np.exp(-t_(1.2) / .4), 18.7, .35); add(fx, ge(1, 46), 18.7, .4)
    for k in range(3): add(mus, sfx.rumble(1.4), 19.6 + k * .5, .3)
    add(mus, lp(noise(11.0), 400) * np.sin(np.pi * t_(11.0) / 11.0) * .8, 22.6, .35)
    for k in range(5): add(fx, bell(SA * 4 * BHUPALI[(k * 2) % 6], 1, 3), 25.9 + k * 1.4, .08)
    crack(34.69, .35); add(fx, shankh(233, .8), 35.0, .2)
    add(mus, sfx.rumble(3.0), 36.3, .4); add(mus, lp(noise(3.0), 1200) * np.sin(np.pi * t_(3.0) / 3.0), 36.3, .3)
    add(fx, sfx.whoosh(.8), 39.45, .14); add(fx, ge(1, 56), 41.57, .4); add(fx, bell(SA * 2, 1, 5), 41.6, .26); chimes(41.7, 45.5, 16)
    add(fx, na(1, 460), 46.14, .16)
    endcard(49.4, 49.6, 50.3, .8)
if EP == '10':
    add(fx, sfx.whoosh(.35), 1.40, .1); chimes(1.6, 5.7, 10)
    add(fx, bell(SA * 2, 1, 4.5), 6.63, .2); add(fx, shankh(233, 1.0), 10.96, .2); chimes(11.0, 12.6, 10)
    add(fx, na(1, 520), 13.53, .14); arp(16.1, .4, .1, 8); chimes(19.0, 22.2, 14)
    add(fx, na(1, 460), 23.04, .14); add(mus, lp(sfx.brown(4.0), 300) * np.sin(np.pi * t_(4.0) / 4.0), 24.4, .3)
    add(fx, bell(SA * 4, 1, 4), 26.83, .18); chimes(29.5, 34.9, 14)
    add(fx, bell(SA * 2, 1, 5), 35.67, .22); arp(36.0, .35, .1, 8)
    add(mus, sfx.rumble(2.0), 40.5, .3); crack(41.6, .4); add(fx, ge(1, 40), 41.6, .5); add(mus, lp(sfx.brown(2.0), 200), 41.6, .45)
    add(fx, shankh(233, 1.2), 44.6, .26); groove(44.8, 46.7, .9)
    add(fx, bell(SA * 4, 1, 4), 47.37, .18); chimes(49.5, 52.0, 12)
    endcard(52.4, 52.6, 53.4, .8)
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

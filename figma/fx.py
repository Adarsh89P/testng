"""Reference-reel effects: camera zoom, whole-scene dot break/form transitions, dot-assembled LAW cards.

Scenes draw their 'world' onto an offscreen canvas through a camera; transitions turn that frame into
particles with numpy (fast, deterministic per pixel), then the HUD is drawn crisp on top.
"""
import math
import numpy as np
import cairo
from dots import *


def arr(cv):
    """Writable (H, W, 4) uint8 BGRA view of a Canvas surface."""
    cv.surf.flush()
    return np.ndarray((cv.h, cv.w, 4), np.uint8, buffer=cv.surf.get_data(), strides=(cv.surf.get_stride(), 4, 1))


class Cam:
    def __init__(self, keys, anchor):
        self.keys, self.anchor = keys, anchor   # keys [(t, fx, fy, zoom)]

    def at(self, t):
        k = self.keys
        if t <= k[0][0]: return k[0][1:]
        for (t0, *a), (t1, *b) in zip(k, k[1:]):
            if t < t1:
                e = ease((t - t0) / max(1e-6, t1 - t0)); return tuple(lerp(p, q, e) for p, q in zip(a, b))
        return k[-1][1:]

    def apply(self, cv, t, punch=0.0):
        fx, fy, z = self.at(t); z *= 1 + punch
        cv.c.translate(*self.anchor); cv.c.scale(z, z); cv.c.translate(-fx, -fy)


def _hash(xs, ys, s):
    v = np.sin(xs * 12.9898 + ys * 78.233 + s * 37.719) * 43758.5453
    return v - np.floor(v)


def particles(src, dst, k, step=3, spread=260, drift=-120, seed=0, thresh=40):
    """Scatter bright pixels of src into dst. k=0 intact, k=1 fully blown away."""
    dst[:, :, :3] = (np.array(BG) * 255).astype(np.uint8)[::-1]
    dst[:, :, 3] = 255
    sub = src[::step, ::step, :3]
    lum = sub.max(axis=2)
    ys, xs = np.nonzero(lum > thresh)
    if len(xs) == 0: return
    col = sub[ys, xs].astype(np.float32)
    X, Y = xs * step, ys * step
    ang = _hash(X, Y, seed) * 6.2832
    rad = (0.25 + 0.75 * _hash(Y, X, seed + 1)) * spread * (k ** 1.3)
    nx = (X + np.cos(ang) * rad).astype(np.int32)
    ny = (Y + np.sin(ang) * rad + drift * k * (0.5 + _hash(X, X, seed + 2))).astype(np.int32)
    a = np.clip(1.0 - k * (0.7 + 0.6 * _hash(X, Y, seed + 3)), 0, 1)[:, None]
    h, w = dst.shape[:2]
    m = (nx >= 0) & (nx < w - 2) & (ny >= 0) & (ny < h - 2)
    nx, ny, c = nx[m], ny[m], (col[m] * a[m]).astype(np.uint8)
    for dy in (0, 1):
        for dx in (0, 1):
            cur = dst[ny + dy, nx + dx, :3]
            dst[ny + dy, nx + dx, :3] = np.maximum(cur, c)


class Stage:
    """Owns the offscreen world canvas; compose() handles camera + break/form transitions."""
    def __init__(self, w, h, anchor):
        self.world = Canvas(w, h); self.anchor = anchor
        self.tmp = Canvas(w, h)

    def compose(self, cv, t, d, draw_world, cam_keys, punch=0.0, form=0.55, brk=0.55, seed=0):
        wc = self.world; wc.clear()
        wc.c.save(); Cam(cam_keys, self.anchor).apply(wc, t, punch); draw_world(wc); wc.c.restore()
        src = arr(wc); dst = arr(cv)
        if form and t < form:
            particles(src, dst, ease(1 - t / form), seed=seed + 7, drift=120)
        elif brk and t > d - brk:
            particles(src, dst, ease((t - (d - brk)) / brk), seed=seed)
        else:
            dst[:] = src
        cv.surf.mark_dirty()


_text_cache = {}


def text_points(text, size, fam=SANS, bold=True, w=1080, h=1920, cx=540, cy=960, step=3):
    key = (text, size, cx, cy)
    if key not in _text_cache:
        t = Canvas(w, h); t.c.set_source_rgb(0, 0, 0); t.c.paint()
        t.font(fam, size, bold); tw = t.text_w(text)
        t.text(cx - tw / 2, cy + size * 0.36, text, (1, 1, 1))
        a = arr(t)[::step, ::step, 1]
        ys, xs = np.nonzero(a > 100)
        _text_cache[key] = (xs * step, ys * step)
    return _text_cache[key]


def dot_text(cv, text, size, cx, cy, k, seed=5, col=(1, 1, 1)):
    """Big text assembling from scattered dots (k=1 scattered -> 0 formed); crisp once formed."""
    if k <= 0.001:
        cv.font(SANS, size, True); tw = cv.text_w(text); cv.text(cx - tw / 2, cy + size * 0.36, text, col); return
    xs, ys = text_points(text, size, cx=cx, cy=cy)
    ang = _hash(xs, ys, seed) * 6.2832; rad = (0.3 + _hash(ys, xs, seed) * 0.7) * 420 * k
    c = cv.c; c.set_source_rgba(*col, 1 - 0.5 * k)
    for x, y, an, r in zip(xs[::2], ys[::2], ang[::2], rad[::2]):
        c.rectangle(x + math.cos(an) * r, y + math.sin(an) * r, 2.6, 2.6)
    c.fill()


def law_card(cv, t, t0, t1, num, name, line1, line2="", y=1040):
    """Dim the world and show a big dot-formed LAW title with definition (HUD layer)."""
    if not (t0 <= t < t1): return
    a = min(1, (t - t0) / 0.3) * min(1, (t1 - t) / 0.3)
    cv.c.set_source_rgba(0, 0, 0, 0.78 * a); cv.c.rectangle(0, 560, cv.w, 1100); cv.c.fill()
    lt = t - t0
    cv.pill(cv.w / 2, y - 150, f"LAW #{num}", size=26, fam=MONO, col=(0.02, 0.02, 0.03), bg=(0.95, 0.95, 0.96), bold=True, a=a)
    size = 92 if len(name) <= 12 else 74
    dot_text(cv, name, size, cv.w / 2, y - 30, ease(1 - lt / 0.7), col=(1, 1, 1))
    cv.font(MONO, 30); n = int(max(0, lt - 0.7) * 30)
    s1 = line1[:n]; cv.text(cv.w / 2 - cv.text_w(line1) / 2, y + 70, s1, (0.85, 0.85, 0.88), a)
    if line2:
        n2 = max(0, n - len(line1)); s2 = line2[:n2]
        cv.font(MONO, 26); cv.text(cv.w / 2 - cv.text_w(line2) / 2, y + 125, s2, GOOD, a)
    # scanning ring for emphasis
    r = 300 + 40 * math.sin(lt * 3)
    cv.dellipse(cv.w / 2, y + 20, r * 1.35, r * 0.75, spacing=14, r=1.3, col=DIM, a=0.6 * a)


def flash(cv, t, at, dur=0.18):
    if 0 <= t - at < dur:
        cv.c.set_source_rgba(1, 1, 1, 0.35 * (1 - (t - at) / dur)); cv.c.paint()


def ring(cv, x, y, t, at, col=(1, 1, 1)):
    """Expanding attention ring (in world space)."""
    lt = t - at
    if 0 <= lt < 1.2:
        for i in range(2):
            k = ((lt - i * 0.25) % 1.2) / 1.2
            if lt - i * 0.25 < 0: continue
            cv.dellipse(x, y, 30 + 90 * k, 30 + 90 * k, spacing=7, r=1.8, col=col, a=(1 - k))

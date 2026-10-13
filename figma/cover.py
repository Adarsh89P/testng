"""Reel cover (1080x1920) for the 45 Days · 45 UX Challenge: dot-matrix title + dotted app illustration.

usage: python3 cover.py OUT.png --day 1 --law "LABOR|ILLUSION" --app zomato --hook "UX designer ho?" --tease "30 min wait... chhota kyun lagta hai?"
Key content stays inside the centre 1080x1440 so Instagram's 3:4 grid crop keeps it.
"""
import argparse, math
import numpy as np
from dots import *
from fx import arr

W, H = 1080, 1920
ZRED = (0.886, 0.216, 0.267)


def dot_matrix(cv, text, cx, cy, size, pitch=12, r=4.4, col=(1, 1, 1), glow=True, fam=SANS):
    """Dotted-line font: rasterise text, then place round dots on a grid wherever the glyph is."""
    m = Canvas(W, H); m.c.set_source_rgb(0, 0, 0); m.c.paint()
    m.font(fam, size, True); tw = m.text_w(text)
    m.text(cx - tw / 2, cy + size * 0.36, text, (1, 1, 1))
    a = arr(m)[:, :, 1]
    ys, xs = np.mgrid[pitch // 2:H:pitch, pitch // 2:W:pitch]
    hit = a[ys, xs] > 128
    if glow:
        for x, y in zip(xs[hit], ys[hit]): cv.glow(x, y, r * 3.2, 0.10)
    for x, y in zip(xs[hit], ys[hit]): cv._dot(x, y, r, col, 1.0)


def bg_grid(cv, pitch=36):
    for y in range(pitch // 2, H, pitch):
        for x in range(pitch // 2, W, pitch):
            cv._dot(x, y, 1.2, (0.22, 0.22, 0.25), 1.0)


def wordmark(cv, cx, cy, name="zomato", size=58):
    """Red badge with the app name in bold slanted lowercase (stand-in; swap for the official logo if desired)."""
    cv.font(SANS, size, True); tw = cv.text_w(name)
    w, h = tw + size * 1.1, size * 1.55
    cv.fill_rrect(cx - w / 2, cy - h / 2, w, h, 18, ZRED)
    c = cv.c; c.save(); c.translate(cx, cy); c.transform(cairo.Matrix(1, 0, -0.18, 1, 0, 0))
    cv.font(SANS, size, True); c.set_source_rgb(1, 1, 1); c.move_to(-tw / 2, size * 0.34); c.show_text(name); c.restore()


def phone_track(cv, cx, cy, w=330, h=560):
    x, y = cx - w / 2, cy - h / 2
    cv.drrect(x, y, w, h, 56, spacing=7, r=2.2)
    cv.drrect(x + 12, y + 12, w - 24, h - 24, 46, spacing=8, r=1.4, col=DIM)
    cv.drrect(cx - 48, y + 26, 96, 20, 10, spacing=5, r=1.6)
    gx0, gy0, gw, gh = x + 40, y + 80, w - 80, 300
    for gx in range(int(gx0), int(gx0 + gw) + 1, 50): cv.dline(gx, gy0, gx, gy0 + gh, spacing=10, r=1.2, col=(0.3, 0.3, 0.33))
    for gy in range(int(gy0), int(gy0 + gh) + 1, 50): cv.dline(gx0, gy, gx0 + gw, gy, spacing=10, r=1.2, col=(0.3, 0.3, 0.33))
    route = [(gx0 + 10, gy0 + 20), (gx0 + 10, gy0 + 140), (gx0 + gw * 0.55, gy0 + 140), (gx0 + gw * 0.55, gy0 + gh - 30), (gx0 + gw - 10, gy0 + gh - 30)]
    cv.dots_path(route, spacing=9, r=2.6)
    rx, ry = gx0 + gw * 0.55, gy0 + 210
    cv.glow(rx, ry, 70, 1.0); cv._dot(rx, ry, 9, (1, 1, 1), 1)
    cv._dot(route[-1][0], route[-1][1], 9, (0.35, 0.85, 0.55), 1)
    sy = y + 410
    for i, (n, on) in enumerate([("Preparing", True), ("On the way", True), ("Arriving", False)]):
        yy = sy + i * 40; col = (0.35, 0.85, 0.55) if on else (0.35, 0.35, 0.38)
        cv.c.set_source_rgb(*col); cv.c.arc(x + 52, yy, 7, 0, 6.3); cv.c.fill()
        cv.font(SANS, 24, True); cv.text(x + 72, yy + 8, n, DOT if on else DIM)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--day", type=int, default=1)
    ap.add_argument("--law", default="LABOR|ILLUSION"); ap.add_argument("--app", default="zomato")
    ap.add_argument("--hook", default="UX designer ho?"); ap.add_argument("--tease", default="30 min wait... chhota kyun lagta hai?")
    a = ap.parse_args()
    cv = Canvas(W, H); cv.clear(); bg_grid(cv)
    # series header
    white_pill(cv, W / 2, 150, f"DAY {a.day:02d}/45 · UX CHALLENGE", 34)
    for i in range(45):
        x = 110 + (W - 220) * i / 44; on = i < a.day
        cv._dot(x, 222, 6 if on else 3.4, (1, 1, 1) if on else (0.38, 0.38, 0.42), 1)
        if on and i == a.day - 1: cv.glow(x, 222, 26, 0.9)
    # hook + dot-matrix title
    cv.font(MONO, 54); cv.text(W / 2 - cv.text_w(a.hook) / 2, 380, a.hook, (0.9, 0.9, 0.92))
    lines = a.law.split("|")
    for i, ln in enumerate(lines):
        size = 230 if len(ln) <= 6 else int(230 * 6.5 / len(ln))
        dot_matrix(cv, ln, W / 2, 560 + i * 225, size)
    # illustration + app badge
    py = 1300
    phone_track(cv, W / 2 - 150, py)
    wordmark(cv, W / 2 + 225, py - 170)
    cv.pill(W / 2 + 225, py - 70, "live tracking", size=30, fam=MONO, col=(0.35, 0.85, 0.55))
    cv.pill(W / 2 + 225, py + 10, "wait: 30 min", size=30, fam=MONO)
    # tease line
    white_pill(cv, W / 2, 1660, a.tease, 34)
    cv.png(a.out); print("saved", a.out)


if __name__ == "__main__":
    main()

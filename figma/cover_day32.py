"""Day 32 reel cover (1080x1920): Endowment Effect · Spotify Premium trial.

Dot-matrix law title + the "Premium kal khatam" pop-up as the hook. Key content stays inside the centre 1080x1440 so
Instagram's 3:4 grid crop keeps it. usage: python3 cover_day32.py OUT.png
"""
import sys, math
from dots import *
from cover import dot_matrix, bg_grid, W, H
import day32_endowment_effect as E

GOLD, SPOT, RED = E.GOLD, E.SPOT, (0.95, 0.30, 0.30)


def main(out):
    cv = Canvas(W, H); cv.c.set_source_rgb(0, 0, 0); cv.c.paint()
    bg_grid(cv)
    cv.pill(W / 2, 300, "DAY 32 / 45 · UX LAWS", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
    dot_matrix(cv, "ENDOWMENT", W / 2, 440, 138, pitch=10, r=3.7, col=GOLD)
    dot_matrix(cv, "EFFECT", W / 2, 610, 170, pitch=11, r=4.2, col=GOLD)
    cv.font(SANS, 46, True); hook = "\"Free\" trial ne paise kaise"
    cv.text(W / 2 - cv.text_w(hook) / 2, 780, hook, (1, 1, 1))
    hook2 = "nikalwa liye?"
    cv.text(W / 2 - cv.text_w(hook2) / 2, 840, hook2, (1, 1, 1))
    # phone with the trial-ending pop-up
    px, py, pw, ph = W / 2, 1230, 440, 640
    x0, y0 = px - pw / 2, py - ph / 2
    cv.fill_rrect(x0, y0, pw, ph, 46, (0.06, 0.06, 0.07))
    cv.drrect(x0, y0, pw, ph, 46, spacing=8, r=2.2, col=(0.85, 0.85, 0.88))
    E.spotify_logo(cv, x0 + 54, y0 + 70, 0.9)
    cv.font(SANS, 26, True); cv.text(x0 + 90, y0 + 80, "Meri playlist ♥", (1, 1, 1))
    for i, nm in enumerate(E.SONGS[:4]):
        y = y0 + 120 + i * 64
        cv.fill_rrect(x0 + 24, y, pw - 48, 54, 10, (0.13, 0.13, 0.15))
        cv.fill_rrect(x0 + 34, y + 8, 38, 38, 6, tuple(0.2 + cc * 0.5 for cc in E.COLS[i % 6]), 0.5)
        cv.font(SANS, 20, True); cv.text(x0 + 86, y + 35, nm, (0.55, 0.55, 0.6))
    cv.c.set_source_rgba(0, 0, 0, 0.55); cv.c.rectangle(x0 + 10, y0 + 100, pw - 20, ph - 120); cv.c.fill()
    cv.fill_rrect(x0 + 30, y0 + 330, pw - 60, 270, 22, (0.16, 0.16, 0.18))
    cv.font(SANS, 30, True); cv.text(x0 + 56, y0 + 385, "Premium kal khatam", RED)
    cv.font(SANS, 20, True); cv.text(x0 + 56, y0 + 422, "Aapke 48 downloads bhi jaayenge", (0.9, 0.9, 0.92))
    cv.fill_rrect(x0 + 56, y0 + 460, pw - 112, 70, 35, SPOT)
    cv.font(SANS, 26, True); cv.text(px - cv.text_w("Keep Premium") / 2, y0 + 505, "Keep Premium", (0.05, 0.05, 0.05))
    # tap cursor + ring
    cv.dellipse(px + 150, y0 + 530, 40, 40, spacing=6, r=2.2, col=(1, 1, 1))
    cv._dot(px + 150, y0 + 530, 12, (1, 1, 1), 1)
    cv.pill(W / 2, 1640, "Design with Rakhi · @rakhi.ux", size=30, fam=MONO, col=(0.85, 0.85, 0.88))
    cv.png(out)
    print("cover", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../output/reels/day32_endowment_effect_COVER.png")

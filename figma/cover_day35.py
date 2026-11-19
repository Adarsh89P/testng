"""Day 35 reel cover (1080x1920): Variable Reward · "Aapka phone = slot machine".

Dot-matrix law title + hook + a phone whose screen is a three-reel slot machine with a refresh spinner on top. Key
content stays inside the centre 1080x1440 (Instagram 3:4 grid crop). usage: python3 cover_day35.py OUT.png
"""
import sys, math
from dots import *
from cover import dot_matrix, bg_grid, W, H
import day35_variable_reward as V


def main(out):
    cv = Canvas(W, H); cv.c.set_source_rgb(0, 0, 0); cv.c.paint()
    bg_grid(cv)
    cv.pill(W / 2, 300, "DAY 35 / 45 · UX LAWS", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
    dot_matrix(cv, "VARIABLE", W / 2, 440, 140, pitch=10, r=3.7, col=V.IGP)
    dot_matrix(cv, "REWARD", W / 2, 590, 140, pitch=10, r=3.7, col=V.IGP)
    cv.font(SANS, 48, True)
    for i, ln in enumerate(["Aapka phone =", "ek slot machine"]):
        cv.text(W / 2 - cv.text_w(ln) / 2, 750 + i * 64, ln, (1, 1, 1))
    px, py, pw, ph = W / 2, 1240, 460, 600
    x0, y0 = px - pw / 2, py - ph / 2
    cv.fill_rrect(x0, y0, pw, ph, 46, (0.06, 0.06, 0.07))
    cv.drrect(x0, y0, pw, ph, 46, spacing=8, r=2.2, col=(0.85, 0.85, 0.88))
    V.spinner(cv, px, y0 + 90, 1.3, 1.0, r=26)
    cv.font(SANS, 22, True); cv.text(px - cv.text_w("pull to refresh") / 2, y0 + 150, "pull to refresh", (0.6, 0.6, 0.65))
    cv.fill_rrect(x0 + 30, y0 + 200, pw - 60, 220, 26, (0.20, 0.10, 0.16))
    for i, col in enumerate([V.GOLD, V.GOLD, V.IGP]):
        x = x0 + 30 + 70 + i * 130
        cv.fill_rrect(x - 55, y0 + 225, 110, 170, 16, (0.08, 0.08, 0.09))
        cv.c.new_path(); cv.c.set_source_rgba(*col, 1); cv.c.arc(x, y0 + 310, 40, 0, 6.2832); cv.c.fill()
    cv.pill(px, y0 + 480, "shaayad haan… shaayad nahi", size=21, fam=MONO, col=(0.9, 0.9, 0.92))
    cv.pill(W / 2, 1640, "Design with Rakhi · @rakhi.ux", size=30, fam=MONO, col=(0.85, 0.85, 0.88))
    cv.png(out)
    print("cover", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../output/reels/day35_variable_reward_COVER.png")

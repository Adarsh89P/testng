"""Day 33 reel cover (1080x1920): Reciprocity · Canva free templates with a Pro crown.

Dot-matrix law title + hook + a Canva screen whose FREE templates surround one crowned Pro template. Key content
stays inside the centre 1080x1440 (Instagram 3:4 grid crop). usage: python3 cover_day33.py OUT.png
"""
import sys
from dots import *
from cover import dot_matrix, bg_grid, W, H
import day33_reciprocity as R


def main(out):
    cv = Canvas(W, H); cv.c.set_source_rgb(0, 0, 0); cv.c.paint()
    bg_grid(cv)
    cv.pill(W / 2, 300, "DAY 33 / 45 · UX LAWS", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
    dot_matrix(cv, "RECIPROCITY", W / 2, 470, 132, pitch=10, r=3.6, col=R.CAN)
    cv.font(SANS, 46, True)
    for i, ln in enumerate(["Sab FREE diya…", "phir bhi log pay kyun karte hain?"]):
        cv.text(W / 2 - cv.text_w(ln) / 2, 660 + i * 62, ln, (1, 1, 1))
    px, py, pw, ph = W / 2, 1210, 500, 680
    x0, y0 = px - pw / 2, py - ph / 2
    cv.fill_rrect(x0, y0, pw, ph, 46, (0.06, 0.06, 0.07))
    cv.drrect(x0, y0, pw, ph, 46, spacing=8, r=2.2, col=(0.85, 0.85, 0.88))
    cv.fill_rrect(x0 + 16, y0 + 30, pw - 32, 70, 14, R.CPUR)
    cv.font(SANS, 32, True); cv.text(x0 + 40, y0 + 78, "Canva", (1, 1, 1))
    for i in range(6):
        R.template(cv, x0 + 30 + (i % 2) * 226, y0 + 130 + (i // 2) * 170, 212, 156, i, pro=(i == 3))
    cv.dellipse(x0 + 256 + 212 - 24, y0 + 300 + 24, 42, 42, spacing=6, r=2.2, col=R.GOLD)
    cv.pill(px + 180, y0 + 380, "Pro", size=30, fam=SANS, col=(0.05, 0.05, 0.05), bg=R.GOLD, bold=True)
    cv.pill(W / 2, 1640, "Design with Rakhi · @rakhi.ux", size=30, fam=MONO, col=(0.85, 0.85, 0.88))
    cv.png(out)
    print("cover", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../output/reels/day33_reciprocity_COVER.png")

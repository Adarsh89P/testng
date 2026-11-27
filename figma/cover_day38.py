"""Day 38 reel cover (1080x1920): Recognition over Recall · Zomato's veg / non-veg dot.

Dot-matrix law title + hook + a menu whose dish names are blurred but the green/red marks are clear. Key content
stays inside the centre 1080x1440 (Instagram 3:4 grid crop). usage: python3 cover_day38.py OUT.png
"""
import sys
from dots import *
from cover import dot_matrix, bg_grid, W, H
import day38_recognition_over_recall as R


def main(out):
    cv = Canvas(W, H); cv.c.set_source_rgb(0, 0, 0); cv.c.paint()
    bg_grid(cv)
    cv.pill(W / 2, 300, "DAY 38 / 45 · UX LAWS", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
    dot_matrix(cv, "RECOGNITION", W / 2, 440, 118, pitch=9, r=3.3, col=R.ZR)
    dot_matrix(cv, "OVER RECALL", W / 2, 570, 118, pitch=9, r=3.3, col=R.ZR)
    cv.font(SANS, 46, True)
    for i, ln in enumerate(["Bina padhe khaana", "kaise chun lete ho?"]):
        cv.text(W / 2 - cv.text_w(ln) / 2, 730 + i * 62, ln, (1, 1, 1))
    px, py, pw, ph = W / 2, 1230, 460, 620
    x0, y0 = px - pw / 2, py - ph / 2
    cv.fill_rrect(x0, y0, pw, ph, 46, (0.06, 0.06, 0.07))
    cv.drrect(x0, y0, pw, ph, 46, spacing=8, r=2.2, col=(0.85, 0.85, 0.88))
    cv.fill_rrect(x0 + 14, y0 + 30, pw - 28, 70, 14, (0.20, 0.06, 0.08))
    cv.font(SANS, 28, True); cv.text(x0 + 40, y0 + 76, "Menu", R.ZR)
    for j, (veg, w) in enumerate([(True, 210), (False, 170), (True, 240), (False, 190)]):
        y = y0 + 125 + j * 105
        cv.fill_rrect(x0 + 24, y, pw - 48, 88, 14, R.CARD)
        R.food_mark(cv, x0 + 64, y + 44, veg, 1.1)
        R.blur_bar(cv, x0 + 100, y + 26, w); R.blur_bar(cv, x0 + 100, y + 54, w * 0.5, 0.6)
        if veg:
            cv.rrect_path(x0 + 24, y, pw - 48, 88, 14); cv.c.set_source_rgba(*R.VEG, 0.9); cv.c.set_line_width(3); cv.c.stroke()
    cv.pill(px, y0 + 570, "naam nahi, bas dot", size=24, fam=MONO, col=(0.9, 0.9, 0.92))
    cv.pill(W / 2, 1640, "Design with Rakhi · @rakhi.ux", size=30, fam=MONO, col=(0.85, 0.85, 0.88))
    cv.png(out)
    print("cover", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../output/reels/day38_recognition_over_recall_COVER.png")

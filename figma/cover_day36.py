"""Day 36 reel cover (1080x1920): Progressive Disclosure · Google Maps hides the route.

Dot-matrix law title + counter-intuitive hook + a Maps screen showing only the next turn and "15 min · Start".
Key content stays inside the centre 1080x1440 (Instagram 3:4 grid crop). usage: python3 cover_day36.py OUT.png
"""
import sys
from dots import *
from cover import dot_matrix, bg_grid, W, H
import day36_progressive_disclosure as P


def main(out):
    cv = Canvas(W, H); cv.c.set_source_rgb(0, 0, 0); cv.c.paint()
    bg_grid(cv)
    cv.pill(W / 2, 300, "DAY 36 / 45 · UX LAWS", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
    dot_matrix(cv, "PROGRESSIVE", W / 2, 440, 118, pitch=9, r=3.3, col=P.GM)
    dot_matrix(cv, "DISCLOSURE", W / 2, 570, 118, pitch=9, r=3.3, col=P.GM)
    cv.font(SANS, 46, True)
    for i, ln in enumerate(["Google Maps poora raasta", "chhupaata hai… kyun?"]):
        cv.text(W / 2 - cv.text_w(ln) / 2, 730 + i * 62, ln, (1, 1, 1))
    # phone: Maps with only the next turn on top and a small summary sheet
    P.phone(cv, P.PX, 1230, 460, 620)
    x0, y0 = P.PX - 230, 1230 - 310
    cv.fill_rrect(x0 + 10, y0 + 40, 440, 560, 30, (0.10, 0.12, 0.14))
    for i in range(6):
        cv.c.set_source_rgba(0.20, 0.22, 0.25, 1); cv.c.rectangle(x0 + 10, y0 + 90 + i * 85, 440, 4); cv.c.fill()
    cv.dots_path([(x0 + 80, y0 + 440), (x0 + 150, y0 + 360), (x0 + 260, y0 + 340), (x0 + 330, y0 + 240)], spacing=10, r=4.2, col=P.GM)
    cv.fill_rrect(x0 + 20, y0 + 50, 420, 120, 20, P.GMG)
    cv.font(SANS, 36, True); cv.text(x0 + 60, y0 + 108, "200 m", (1, 1, 1))
    cv.font(SANS, 26, True); cv.text(x0 + 60, y0 + 148, "Turn right  →", (1, 1, 1))
    cv.fill_rrect(x0 + 10, y0 + 470, 440, 130, 26, (0.16, 0.16, 0.18))
    cv.font(SANS, 34, True); cv.text(x0 + 40, y0 + 530, "15 min", P.GMG)
    cv.font(SANS, 22, True); cv.text(x0 + 170, y0 + 528, "(6 km)", (0.9, 0.9, 0.92))
    cv.font(SANS, 22, True); cv.text(x0 + 40, y0 + 572, "Steps ›", P.GM)
    cv.pill(P.PX + 160, y0 + 30, "bas ek line", size=26, fam=SANS, col=(0.05, 0.05, 0.05), bg=P.GMG, bold=True)
    cv.pill(W / 2, 1640, "Design with Rakhi · @rakhi.ux", size=30, fam=MONO, col=(0.85, 0.85, 0.88))
    cv.png(out)
    print("cover", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../output/reels/day36_progressive_disclosure_COVER.png")

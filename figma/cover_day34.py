"""Day 34 reel cover (1080x1920): Commitment & Consistency · Duolingo "just 5 minutes".

Dot-matrix law title + hook + the onboarding screen with "5 min · casual" chosen and the owl. Key content stays inside
the centre 1080x1440 (Instagram 3:4 grid crop). usage: python3 cover_day34.py OUT.png
"""
import sys
from dots import *
from cover import dot_matrix, bg_grid, W, H
import day34_commitment as C


def main(out):
    cv = Canvas(W, H); cv.c.set_source_rgb(0, 0, 0); cv.c.paint()
    bg_grid(cv)
    cv.pill(W / 2, 300, "DAY 34 / 45 · UX LAWS", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
    dot_matrix(cv, "COMMITMENT", W / 2, 440, 128, pitch=10, r=3.5, col=C.DUO)
    dot_matrix(cv, "& CONSISTENCY", W / 2, 580, 104, pitch=9, r=3.2, col=C.DUO)
    cv.font(SANS, 46, True)
    for i, ln in enumerate(["Sirf 5 minute ka waada…", "aur aap roz seekhne lage?"]):
        cv.text(W / 2 - cv.text_w(ln) / 2, 740 + i * 62, ln, (1, 1, 1))
    px, py, pw, ph = W / 2, 1230, 480, 620
    x0, y0 = px - pw / 2, py - ph / 2
    cv.fill_rrect(x0, y0, pw, ph, 46, (0.06, 0.06, 0.07))
    cv.drrect(x0, y0, pw, ph, 46, spacing=8, r=2.2, col=(0.85, 0.85, 0.88))
    C.owl(cv, x0 + 80, y0 + 90, 0.65)
    cv.font(SANS, 28, True); cv.text(x0 + 136, y0 + 100, "Roz kitna time?", (1, 1, 1))
    for i, o in enumerate(["5 min · casual", "10 min · regular", "15 min · serious", "20 min · intense"]):
        C.option(cv, x0 + 30, y0 + 170 + i * 96, pw - 60, o, i == 0)
    cv.dellipse(x0 + pw - 90, y0 + 206, 40, 40, spacing=6, r=2.2, col=(1, 1, 1))
    cv._dot(x0 + pw - 90, y0 + 206, 12, (1, 1, 1), 1)
    cv.pill(px + 170, y0 + 140, "chhoti haan", size=28, fam=SANS, col=(0.05, 0.05, 0.05), bg=C.DUO, bold=True)
    cv.pill(W / 2, 1640, "Design with Rakhi · @rakhi.ux", size=30, fam=MONO, col=(0.85, 0.85, 0.88))
    cv.png(out)
    print("cover", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../output/reels/day34_commitment_COVER.png")

"""Day 37 reel cover (1080x1920): Visibility of System Status · WhatsApp's ticks.

Dot-matrix law title + hook + a chat bubble showing the three tick states. Key content stays inside the centre
1080x1440 (Instagram 3:4 grid crop). usage: python3 cover_day37.py OUT.png
"""
import sys
from dots import *
from cover import dot_matrix, bg_grid, W, H
import day37_system_status as S


def main(out):
    cv = Canvas(W, H); cv.c.set_source_rgb(0, 0, 0); cv.c.paint()
    bg_grid(cv)
    cv.pill(W / 2, 300, "DAY 37 / 45 · UX LAWS", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
    dot_matrix(cv, "SYSTEM", W / 2, 440, 140, pitch=10, r=3.7, col=S.WA)
    dot_matrix(cv, "STATUS", W / 2, 590, 140, pitch=10, r=3.7, col=S.WA)
    cv.font(SANS, 48, True)
    for i, ln in enumerate(["Do neeli lines ka", "poora raaz"]):
        cv.text(W / 2 - cv.text_w(ln) / 2, 750 + i * 64, ln, (1, 1, 1))
    px, py, pw, ph = W / 2, 1240, 460, 600
    x0, y0 = px - pw / 2, py - ph / 2
    cv.fill_rrect(x0, y0, pw, ph, 46, (0.06, 0.06, 0.07))
    cv.drrect(x0, y0, pw, ph, 46, spacing=8, r=2.2, col=(0.85, 0.85, 0.88))
    cv.fill_rrect(x0 + 14, y0 + 30, pw - 28, 76, 14, (0.07, 0.20, 0.17))
    cv.c.new_path(); cv.c.set_source_rgba(0.35, 0.55, 0.85, 1); cv.c.arc(x0 + 60, y0 + 68, 22, 0, 6.2832); cv.c.fill()
    cv.font(SANS, 26, True); cv.text(x0 + 96, y0 + 78, "Rahul", (1, 1, 1))
    for j, (txt, st, lab) in enumerate([("Kal movie?", 1, "bhej diya"), ("Kal movie?", 2, "pahunch gaya"), ("Kal movie?", 3, "padh liya")]):
        y = y0 + 150 + j * 130
        bw = 240; bx = x0 + pw - 30 - bw
        cv.fill_rrect(bx, y, bw, 64, 16, S.BUB)
        cv.font(SANS, 24, True); cv.text(bx + 20, y + 41, txt, (1, 1, 1))
        S.ticks(cv, bx + bw - 40, y + 44, st, 1.2)
        cv.font(SANS, 20, True); cv.text(x0 + 30, y + 40, lab, S.WAB if st == 3 else (0.6, 0.6, 0.65))
    cv.pill(px, y0 + 540, "…aur reply nahi aaya", size=24, fam=MONO, col=(0.9, 0.9, 0.92))
    cv.pill(W / 2, 1640, "Design with Rakhi · @rakhi.ux", size=30, fam=MONO, col=(0.85, 0.85, 0.88))
    cv.png(out)
    print("cover", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../output/reels/day37_system_status_COVER.png")

"""Day 02/45 · Hick's Law, explained with Swiggy's filter chips.

No captions. Colour accents, frequent camera zoom in/out, dot animations (swarm, fall-away, dotted curve),
synthesized SFX, whole-frame dot break/form transitions. DAY badge sits lower (below Instagram's top bar).
Voice: hf_beta, speed 1.05, no extra processing (same as Day 01).
"""
import sys, math
from engine import *
from fx import Stage, dot_text, flash, ring

W, H = 1080, 1920
DAY, NEXT = 2, "Fitts's Law"
ORANGE = (0.988, 0.502, 0.098)
RED = (1.0, 0.36, 0.36)
GREEN = (0.35, 0.85, 0.55)
BLUE = (0.30, 0.62, 1.0)
YELLOW = (1.0, 0.80, 0.25)
IGBLUE = (0.0, 0.584, 0.965)
COLS = [ORANGE, RED, GREEN, BLUE, YELLOW, (0.75, 0.55, 1.0)]
ANCHOR = (W / 2, 1060)
FULL = [(0, W / 2, 1060, 1.0)]
stage = Stage(W, H, ANCHOR)
BADGE_Y = 300                       # slid down from the very top


def K(*keys): return [(t, p[0], p[1], z) for t, p, z in keys]


# ------------------------------------------------------------------ HUD (drawn on top of every scene, crisp)
def hud(cv):
    cv.c.set_source_rgba(*BG, 0.82); cv.c.rectangle(0, BADGE_Y - 40, W, 165); cv.c.fill()
    white_pill(cv, W / 2, BADGE_Y, f"DAY {DAY:02d}/45 · UX CHALLENGE", 30)
    x0, x1 = 110, W - 110
    for i in range(45):
        x = x0 + (x1 - x0) * i / 44; on = i < DAY
        cv._dot(x, BADGE_Y + 58, 5.5 if on else 3.2, ORANGE if on else (0.36, 0.36, 0.4), 1)
        if on and i == DAY - 1: cv.glow(x, BADGE_Y + 58, 22, 0.8)
    cv.font(MONO, 24, True); s = "Design with Rakhi · @rakhi.ux"
    cv.c.set_source_rgba(1, 1, 1, 0.5); cv.c.move_to(W / 2 - cv.text_w(s) / 2, BADGE_Y + 104); cv.c.show_text(s)


def mono(c, s, y, col=DOT, size=40, chars=None, x=None):
    c.font(MONO, size); s2 = s if chars is None else s[:max(0, chars)]
    c.text((x if x is not None else W / 2 - c.text_w(s) / 2), y, s2, col)


def cswarm(c, t, x, y, w, h, n=300, speed=1.0, seed=3, r=3.2, chaos=1.0, a=1.0):
    """Coloured jittering option-dots."""
    import random as R
    g = R.Random(seed)
    for i in range(n):
        px, py = g.random(), g.random(); ph = g.uniform(0, 6.28); col = COLS[i % len(COLS)]
        jx = math.sin(t * 3 * speed + ph) * 14 * chaos; jy = math.cos(t * 2.3 * speed + ph * 1.7) * 14 * chaos
        c._dot(x + px * w + jx, y + py * h + jy, r, col, a * (0.55 + 0.45 * abs(math.sin(t * 2 + ph))))


def phone(c, cx, cy, w, h, a=1.0):
    x, y = cx - w / 2, cy - h / 2
    c.drrect(x, y, w, h, w * 0.15, spacing=6.5, r=2.0, a=a)
    c.drrect(x + 10, y + 10, w - 20, h - 20, w * 0.12, spacing=7.5, r=1.2, col=DIM, a=a)
    c.drrect(cx - w * 0.13, y + 22, w * 0.26, 16, 8, spacing=5, r=1.4, a=a)
    return x, y


def resto_row(c, x, y, w, i, a=1.0):
    col = COLS[i % len(COLS)]
    c.drrect(x, y, 74, 74, 14, spacing=5.5, r=1.6, col=col, a=a)
    c._dot(x + 37, y + 37, 10, col, 0.8 * a)
    c.dbar(x + 92, y + 14, w * (0.45 + 0.25 * ((i * 37) % 10) / 10), rows=3, gap=6, a=a)
    c.dbar(x + 92, y + 46, w * 0.3, rows=2, gap=6, col=DIM, a=a)
    rx = x + w - 10
    c.fill_rrect(rx - 66, y + 22, 66, 32, 10, GREEN if i % 3 else ORANGE, 0.9 * a)
    c.font(SANS, 18, True); c.text(rx - 56, y + 44, f"{3.6 + (i % 13) / 10:.1f}★", (0.05, 0.05, 0.05), a)


def chip(c, x, y, label, on, size=24, k=1.0):
    c.font(SANS, size, True); w = c.text_w(label) + 40; h = size * 1.9
    if on: c.fill_rrect(x, y, w, h, h / 2, ORANGE, k)
    else: c.fill_rrect(x, y, w, h, h / 2, (0.14, 0.14, 0.16), k)
    c.rrect_path(x, y, w, h, h / 2); c.c.set_source_rgba(*(ORANGE if on else (0.4, 0.4, 0.45)), k); c.c.set_line_width(2); c.c.stroke()
    c.text(x + 20, y + h * 0.66, label, (0.05, 0.05, 0.05) if on else DOT, k)
    return w


def person(c, cx, cy, name="You", s=1.0):
    c.person(cx, cy, s); c.pill(cx, cy + 96 * s, name, size=28)


def count_pill(c, cx, cy, n, col):
    white = col == "white"
    c.pill(cx, cy, f"{n} restaurants", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=col if not white else (0.95, 0.95, 0.96), bold=True)


# ------------------------------------------------------------------ scenes
def s0(cv, t, d, st):                                     # series intro
    def world(c):
        cswarm(c, t, 80, 1250, 920, 420, n=160, chaos=0.6, a=0.7)
        dot_text(c, "45 DAYS", 150, W / 2, 800, ease(1 - t / 0.9))
        if t > 0.7: mono(c, "45 UX LAWS · CHALLENGE", 930, (0.88, 0.88, 0.9), 44, chars=int((t - 0.7) * 26))
        if t > 1.5:
            k = min(1, (t - 1.5) / 0.25); s = 1 + 0.25 * math.sin(math.pi * k)
            c.pill(W / 2, 1050, f"DAY {DAY:02d}", size=int(46 * s), fam=MONO, col=(0.05, 0.05, 0.05), bg=ORANGE, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.25), (1.6, ANCHOR, 1.0)), form=0.0, seed=1); hud(cv)


def s1(cv, t, d, st):                                     # question hook
    def world(c):
        mono(c, "UX designer ho?", 720, DOT, 62, chars=int(t * 14))
        if t > 1.3:
            dot_text(c, "HICK'S LAW", 128, W / 2, 900, ease(1 - (t - 1.3) / 0.8), col=ORANGE)
            c.glow(W / 2, 900, 380, 0.08)
        if t > 2.5: mono(c, "kya hai?", 1060, DOT, 62, chars=int((t - 2.5) * 14))
        for i in range(12):                               # orbiting coloured dots
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 900 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.35), (1.3, (W / 2, 900), 1.35), (2.2, (W / 2, 900), 1.0)), seed=2)
    hud(cv); flash(cv, t, 1.3)


ROWS = 300
def app_screen(c, cx, cy, w, h, t, scroll, n_show, chips_on=(), tap=None, fall=None):
    x, y = phone(c, cx, cy, w, h)
    sx, sy, sw = x + 26, y + 60, w - 52
    c.font(SANS, 30, True); c.text(sx, sy + 26, "swiggy", ORANGE)                 # app name as plain text
    c.drrect(sx, sy + 48, sw, 50, 25, spacing=6, r=1.4, col=DIM)
    c.font(SANS, 20); c.text(sx + 24, sy + 80, "Search restaurants...", DIM)
    labels = ["Pure Veg", "Rating 4.0+", "Under 30 min"]
    cxp = sx; chip_rects = []
    for i, lab in enumerate(labels):
        wch = chip(c, cxp, sy + 116, lab, i in chips_on, size=20)
        chip_rects.append((cxp + wch / 2, sy + 116 + 19)); cxp += wch + 12
    c.c.save(); c.rrect_path(sx - 6, sy + 180, sw + 12, h - 260, 12); c.c.clip()
    top = sy + 196 - scroll
    for i in range(min(n_show, 40)):
        yy = top + i * 100
        if yy < sy + 120 or yy > y + h: continue
        resto_row(c, sx, yy, sw, i)
    if fall is not None:                                   # removed rows fall away as coloured dust
        for j in range(60):
            k = fall; jx = (j * 53) % sw; jy = (j * 97) % 500
            c._dot(sx + jx + math.sin(j) * 30 * k, sy + 220 + jy + 900 * k * k * (0.5 + (j % 5) / 5), 4, COLS[j % 6], max(0, 1 - k))
    c.c.restore()
    return chip_rects


def s2(cv, t, d, st):                                     # story: 300+ restaurants
    sc = max(0, t - 1.8) * 420
    def world(c):
        mono(c, "10:04 PM · bhookh lagi hai", 520, (0.85, 0.85, 0.88), 38)
        app_screen(c, W / 2, 1080, 470, 900, t, sc, 40)
        if t > 0.6:
            pulse = 1 + 0.06 * math.sin(t * 8)
            c.pill(W / 2 + 330, 760, "300+", size=int(44 * pulse), fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
            c.pill(W / 2 + 330, 830, "options", size=26, fam=MONO, col=RED)
    stage.compose(cv, t, d, world, K((0, (W / 2 + 200, 800), 2.0), (1.4, (W / 2 + 200, 800), 2.0), (2.4, ANCHOR, 1.0),
                                     (d - 1.6, ANCHOR, 1.0), (d - 0.6, (W / 2, 1150), 1.3)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # overload: swarm + clock
    mins = min(15, int(t / max(1, d - 1.0) * 16))
    def world(c):
        cswarm(c, t, 140, 540, 800, 560, n=300, speed=1.6, chaos=1.4)
        c.drrect(120, 520, 840, 600, 30, spacing=10, r=1.4, col=DIM)
        c.pill(W / 2, 1150, "300 options", size=30, fam=MONO, col=RED)
        person(c, W / 2, 1330)
        c.glow(W / 2, 1300, 120 + 4 * mins, 0.15 + 0.02 * mins)
        for i in range(min(5, mins // 3 + 1)):
            ang = -2.5 + i * 0.6
            c.pill(W / 2 + math.cos(ang) * 200, 1330 + math.sin(ang) * 130, "?", size=34, fam=MONO, col=RED)
        col = RED if mins >= 10 else (YELLOW if mins >= 5 else DOT)
        c.pill(W / 2, 1530, f"scrolling: {mins:02d}:00 min", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=col, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 830), 1.15), (1.5, ANCHOR, 1.0), (d - 1.8, ANCHOR, 1.0), (d - 0.6, (W / 2, 1400), 1.45)),
                  punch=0.04 * max(0, 1 - abs(t - (d - 1.6)) / 0.12), seed=4)
    hud(cv); flash(cv, t, d - 1.6)


def s4(cv, t, d, st):                                     # law card + dotted log curve
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "HICK'S LAW", 118, W / 2, 640, ease(1 - t / 0.8), col=ORANGE)
        l1 = "zyada options = zyada decision time"; n = int(max(0, t - 0.9) * 26)
        mono(c, l1, 760, DOT, 36, chars=n)
        gx, gy, gw, gh = 190, 860, 720, 470
        c.dline(gx, gy + gh, gx + gw, gy + gh, spacing=9, r=1.8, col=DIM)
        c.dline(gx, gy, gx, gy + gh, spacing=9, r=1.8, col=DIM)
        c.font(MONO, 24); c.text(gx + gw - 170, gy + gh + 44, "options →", DIM); c.text(gx - 30, gy - 20, "time ↑", DIM)
        k = ease((t - 2.0) / 3.0)
        pts = []
        for i in range(61):
            u = i / 60; nopt = 1 + u * 299
            v = math.log2(nopt + 1) / math.log2(301)
            pts.append((gx + u * gw, gy + gh - v * gh * 0.92))
        m = int(k * 60)
        for i in range(m + 1):
            x, y = pts[i]; col = GREEN if i < 10 else (YELLOW if i < 30 else RED)
            c._dot(x, y, 6, col, 1);
        if m > 0:
            x, y = pts[m]; c.glow(x, y, 50, 0.9)
        if k > 0.08: c.pill(pts[3][0] + 120, pts[3][1] + 70, "3 options: fast", size=26, fam=MONO, col=GREEN)
        if k > 0.98: c.pill(pts[60][0] - 110, pts[60][1] - 60, "300: stuck", size=26, fam=MONO, col=RED)
        if t > 5.4: c.pill(W / 2, 1450, "T = a + b · log2(n + 1)", size=32, fam=MONO)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.6, (W / 2, 1000), 1.0), (5.0, (W / 2, 1000), 1.0),
                                     (5.6, (700, 960), 1.3), (d - 1.2, (700, 960), 1.3), (d - 0.6, (W / 2, 1000), 1.0)), seed=5)
    hud(cv)


TAPS = [1.4, 2.9, 4.4]
COUNTS = [300, 120, 45, 12]
def s5(cv, t, d, st):                                     # Swiggy filter chips
    n_on = sum(1 for tp in TAPS if t >= tp)
    def world(c):
        fall = None
        for tp in TAPS:
            if 0 <= t - tp < 0.9: fall = (t - tp) / 0.9
        rects = app_screen(c, W / 2, 1080, 470, 900, t, 0, max(4, 40 - 12 * n_on), chips_on=tuple(range(n_on)), fall=fall)
        st["rects"] = rects
        for i, tp in enumerate(TAPS):
            ring(c, rects[i][0], rects[i][1], t, tp, ORANGE)
            if tp - 0.5 < t < tp + 0.25: c._dot(rects[i][0] + 10, rects[i][1] + 12, 15, (1, 1, 1), 0.85)
        cnt = COUNTS[n_on]; col = RED if n_on == 0 else (YELLOW if n_on < 3 else GREEN)
        c.pill(W / 2 + 330, 620, f"{cnt}", size=46, fam=MONO, col=(0.05, 0.05, 0.05), bg=col, bold=True)
        c.pill(W / 2 + 330, 690, "options", size=26, fam=MONO, col=col)
    r = st.get("rects") or [(W / 2 - 150, 795), (W / 2, 795), (W / 2 + 150, 795)]
    keys = [(0, ANCHOR, 1.0), (0.8, r[0], 1.9)]
    for i, tp in enumerate(TAPS):
        keys += [(tp + 0.35, r[i], 1.9), (tp + 0.9, r[min(i + 1, 2)], 1.9)]
    keys += [(TAPS[-1] + 1.1, r[2], 1.9), (TAPS[-1] + 1.9, ANCHOR, 1.0)]
    stage.compose(cv, t, d, world, K(*keys), punch=0.05 * sum(max(0, 1 - abs(t - tp) / 0.1) for tp in TAPS), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # result: 300 -> 12, minutes -> seconds
    def world(c):
        dot_text(c, "300", 170, 300, 820, ease(1 - t / 0.7), col=RED)
        if t > 0.8:
            k = ease((t - 0.8) / 0.5)
            c.dots_path([(470, 820), (470 + 140 * k, 820)], spacing=10, r=3.5, col=DOT)
            if k > 0.95:
                c.dots_path([(590, 790), (615, 820), (590, 850)], spacing=8, r=3.5)
        if t > 1.3: dot_text(c, "12", 170, 800, 820, ease(1 - (t - 1.3) / 0.7), col=GREEN)
        if t > 2.2:
            c.pill(320, 1060, "15 min", size=40, fam=MONO, col=RED, bold=True)
            c.line(240, 1060, 400, 1060, RED, 4)
        if t > 2.8:
            c.pill(780, 1060, "30 sec", size=40, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
        if t > 3.4:
            for i in range(26):
                ang = i / 26 * 6.283; dd = 60 + 220 * ease((t - 3.4) / 1.2)
                c._dot(780 + math.cos(ang) * dd, 1060 + math.sin(ang) * dd * 0.6, 5, COLS[i % 6], max(0, 1 - (t - 3.4) / 1.2))
        if t > 3.0: white_pill(c, W / 2, 1300, "kam choices = fast decision", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 820), 1.3), (1.8, (W / 2, 900), 1.0), (2.6, (780, 1060), 1.5),
                                     (3.8, (780, 1060), 1.5), (4.6, (W / 2, 1000), 1.0)), seed=7)
    hud(cv); flash(cv, t, 2.8)


def s7(cv, t, d, st):                                     # designer tip: group, don't dump
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.6), ("DO", W * 0.73, t >= 2.6)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx = W * 0.27                                       # 16 options at once
        for i in range(16):
            r_, cc = i // 4, i % 4
            jx = math.sin(t * 4 + i) * 4
            c.fill_rrect(lx - 190 + cc * 96 + jx, 700 + r_ * 96, 80, 80, 14, COLS[i % 6], 0.85)
        c.pill(lx, 1140, "16 options ek saath", size=28, fam=MONO, col=RED)
        rx = W * 0.73                                       # 3 groups -> expand
        groups = ["Veg", "Fast", "Top rated"]
        for i, g in enumerate(groups):
            gy = 720 + i * 150
            on = t > 3.0 + i * 0.6
            c.fill_rrect(rx - 170, gy, 340, 96, 22, GREEN if on else (0.16, 0.16, 0.18))
            c.font(SANS, 34, True); c.text(rx - c.text_w(g) / 2, gy + 60, g, (0.05, 0.05, 0.05) if on else DOT)
        c.pill(rx, 1200, "3 groups → phir choose", size=28, fam=MONO, col=GREEN)
        if t > 5.2: white_pill(c, W / 2, 1380, "options hatao mat, GROUP karo", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.3, (W * 0.27, 900), 1.45), (2.9, (W * 0.73, 900), 1.45),
                                     (4.9, (W * 0.73, 900), 1.45), (5.5, ANCHOR, 1.0)), seed=8)
    hud(cv)


def s8(cv, t, d, st):                                     # follow card (one CTA)
    tap = st.setdefault("tap", min(d - 1.4, 2.6))
    def world(c):
        for y in range(18, H, 36):
            for x in range(18, W, 36): c._dot(x, y, 1.2, (0.2, 0.2, 0.23), 1.0)
        k = ease(t / 0.5); cx, ay = W / 2, 760
        for i, r in enumerate((150, 128, 106)):
            c.dellipse(cx, ay, r * k, r * k, spacing=8 - i, r=2.4 - 0.4 * i, col=ORANGE if i == 0 else DOT)
        c.font(SANS, 130, True); c.text(cx - c.text_w("R") / 2, ay + 46, "R", (1, 1, 1), k)
        c.font(SANS, 76, True); c.text(cx - c.text_w("Design with Rakhi") / 2, 1010, "Design with Rakhi", (1, 1, 1), k)
        c.font(MONO, 40); c.text(cx - c.text_w("@rakhi.ux") / 2, 1080, "@rakhi.ux", (0.75, 0.75, 0.78), k)
        tapped = t >= tap
        bw, bh = 420, 104; bx, by = cx - bw / 2, 1240 - bh / 2
        c.fill_rrect(bx, by, bw, bh, 22, (0.17, 0.17, 0.19) if tapped else IGBLUE, k)
        lab = "Following ✓" if tapped else "Follow"; c.font(SANS, 46, True); c.text(cx - c.text_w(lab) / 2, 1257, lab, (1, 1, 1), k)
        if tapped and t - tap < 1.2:
            lt = t - tap
            for i in range(30):
                ang = i / 30 * 6.283; dd = 80 + 260 * ease(lt / 1.2)
                c._dot(cx + math.cos(ang) * dd * 1.3, 1240 + math.sin(ang) * dd * 0.7, 4.5, COLS[i % 6], max(0, 1 - lt / 1.2))
        if 0.6 < t < tap + 0.4:
            u = ease((t - 0.6) / max(0.1, tap - 0.65))
            c._dot(lerp(cx + 330, cx + 40, u), lerp(1470, 1255, u), 16, (1, 1, 1), 0.9)
        if t > tap + 0.4: white_pill(c, cx, 1420, f"kal · Day {DAY + 1:02d}: {NEXT}", 34)
    stage.compose(cv, t, d, world, FULL, brk=0.0, seed=9); hud(cv)


SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे टू।", "", s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, हिक्स लॉ क्या है?", "", s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("रात के दस बजे, भूख लगी है। फूड ऐप खोला, और सामने तीन सौ से ज़्यादा रेस्टोरेंट्स।", "", s2, min_dur=7.0, whoosh=True,
          sfx=[(0.6, "pop_lo")] + [(1.9 + i * 0.16, "tick") for i in range(22)]),
    Scene("स्क्रॉल करते रहो, करते रहो। पंद्रह मिनट हो गए, और अभी तक कुछ ऑर्डर ही नहीं किया।", "", s3, min_dur=7.0, whoosh=True,
          sfx=[(0.3 + i * 0.9, "tick") for i in range(6)] + [(5.6, "buzz")]),
    Scene("यही है हिक्स लॉ। जितने ज़्यादा ऑप्शन, फैसला लेने में उतना ज़्यादा टाइम। तीन ऑप्शन में फैसला फटाफट, तीन सौ में दिमाग अटक जाता है।",
          "", s4, min_dur=10.0, whoosh=True, sfx=[(0.2, "ding"), (2.3, "pop_hi"), (5.0, "buzz"), (5.5, "pop")]),
    Scene("इसीलिए स्विगी ऊपर फिल्टर चिप्स देता है। प्योर वेज, रेटिंग फोर प्लस, और थर्टी मिनट के अंदर डिलीवरी।", "", s5, min_dur=7.6,
          whoosh=True, clicks=TAPS, sfx=[(tp + 0.02, "pop") for tp in TAPS]),
    Scene("तीन सौ से सिर्फ बारह ऑप्शन। और अब फैसला, सेकंड्स में।", "", s6, min_dur=5.6, whoosh=True,
          sfx=[(0.1, "pop_lo"), (1.3, "pop_hi"), (2.2, "buzz"), (2.8, "chime")]),
    Scene("डिज़ाइनर टिप। ऑप्शन हटाओ मत, उन्हें ग्रुप करो। फिल्टर, कैटेगरी, और स्मार्ट डिफॉल्ट्स दो।", "", s7, min_dur=7.0, whoosh=True,
          sfx=[(3.0, "pop"), (3.6, "pop"), (4.2, "pop_hi"), (5.2, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=None, voice="hf_beta", lang="hi",
                                   natural=False, voice_fx=False), 1), "s")

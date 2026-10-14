"""Day 01/45 · Labor Illusion (Zomato) - rebuilt in the Day 02 pattern.

Same story and voice as the original Day 01 (hf_beta, speed 1.05, no processing). Colour accents, frequent zoom
in/out, dot animations, SFX, lowered DAY badge, no captions. Series intro + follow outro reused from Day 02.
"""
import sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 1, "Hick's Law"
W, H = 1080, 1920
ZRED = (0.886, 0.216, 0.267)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
FULL = D.FULL
stage = Stage(W, H, ANCHOR)
K, hud, mono, cswarm, phone = D.K, D.hud, D.mono, D.cswarm, D.phone


def person(c, cx, cy, name="Rohan", s=1.0, col=None):
    c.person(cx, cy, s, **({"col": col} if col else {})); c.pill(cx, cy + 96 * s, name, size=28)


def spinner(c, cx, cy, t, r=26, col=DOT):
    for i in range(8):
        a = (t * 6 + i) % 8 / 8; ang = i / 8 * 6.283
        c._dot(cx + math.cos(ang) * r, cy + math.sin(ang) * r, 4, col, 0.15 + 0.85 * a)


def route_pts(x0, y0, w, h):
    return [(x0 + 20, y0 + 20), (x0 + 20, y0 + h * 0.45), (x0 + w * 0.55, y0 + h * 0.45),
            (x0 + w * 0.55, y0 + h - 30), (x0 + w - 20, y0 + h - 30)]


def along(pts, k):
    segs = list(zip(pts, pts[1:])); L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; d = k * sum(L)
    for (a, b), l in zip(segs, L):
        if d <= l: return a[0] + (b[0] - a[0]) * d / l, a[1] + (b[1] - a[1]) * d / l
        d -= l
    return pts[-1]


def mini_map(c, cx, cy, w, h, k, col=GREEN):
    x0, y0 = cx - w / 2, cy - h / 2
    for gx in range(int(x0) + 14, int(x0 + w), 34): c.dline(gx, y0, gx, y0 + h, spacing=8, r=1.0, col=(0.26, 0.26, 0.3))
    for gy in range(int(y0) + 14, int(y0 + h), 34): c.dline(x0, gy, x0 + w, gy, spacing=8, r=1.0, col=(0.26, 0.26, 0.3))
    pts = route_pts(x0, y0, w, h)
    c.dots_path(pts, spacing=7, r=2.2, col=(0.5, 0.5, 0.55))
    # travelled part in colour
    n = 40
    for i in range(int(k * n) + 1):
        x, y = along(pts, i / n); c._dot(x, y, 3.2, col, 1)
    rx, ry = along(pts, k)
    c.glow(rx, ry, 36, 0.9); c._dot(rx, ry, 7, (1, 1, 1), 1)
    c._dot(pts[-1][0], pts[-1][1], 8, ZRED, 1)
    return rx, ry


def steps(c, x, y, t, t0, gap=46, names=("Order placed", "Preparing", "Rider assigned", "On the way"), size=22, every=0.9):
    lit = int(max(0, (t - t0) / every)) + 1
    for i, n in enumerate(names):
        on = i < lit; yy = y + i * gap
        if i < len(names) - 1: c.line(x, yy + 8, x, yy + gap - 8, GREEN if i < lit - 1 else (0.3, 0.3, 0.33), 2.5)
        c.c.set_source_rgba(*(GREEN if on else (0.3, 0.3, 0.33)), 1); c.c.arc(x, yy, 8, 0, 6.3); c.c.fill()
        if on and i == lit - 1: c.glow(x, yy, 30, 0.7)
        c.font(SANS, size, True); c.text(x + 22, yy + 8, n, DOT if on else (0.55, 0.55, 0.58))
    return lit


def app_header(c, x, y, w):
    c.font(SANS, 34, True); c.text(x, y + 30, "zomato", ZRED)          # app name as plain text
    c.drrect(x, y + 50, w, 48, 24, spacing=6, r=1.4, col=DIM)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # question hook
    def world(c):
        mono(c, "UX designer ho?", 720, DOT, 62, chars=int(t * 14))
        if t > 1.3:
            dot_text(c, "LABOR ILLUSION", 104, W / 2, 900, ease(1 - (t - 1.3) / 0.8), col=ZRED)
            c.glow(W / 2, 900, 420, 0.08)
        if t > 2.5: mono(c, "kya hai?", 1060, DOT, 62, chars=int((t - 2.5) * 14))
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 480, 900 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.35), (1.3, (W / 2, 900), 1.35), (2.2, (W / 2, 900), 1.0)), seed=2)
    hud(cv); flash(cv, t, 1.3)


TAP2 = 3.4
def s2(cv, t, d, st):                                     # story: Friday 9:47 PM, Rohan orders biryani
    def world(c):
        mono(c, "Friday · 9:47 PM", 520, (0.85, 0.85, 0.88), 40, chars=int(t * 18))
        x, y = phone(c, W / 2, 1020, 440, 760)
        sx, sw = x + 26, 440 - 52
        app_header(c, sx, y + 60, sw)
        c.drrect(sx, y + 190, sw, 230, 22, spacing=6, r=1.6, col=YELLOW)                # biryani card
        for i in range(14):
            ang = i / 14 * 6.283
            c._dot(sx + 100 + math.cos(ang) * 46, y + 300 + math.sin(ang) * 30, 5, YELLOW if i % 2 else ORANGE, 1)
        c.font(SANS, 30, True); c.text(sx + 180, y + 280, "Biryani", DOT)
        c.font(MONO, 24); c.text(sx + 180, y + 320, "eta 30 min", DIM)
        ordered = t >= TAP2
        bx, by, bw, bh = sx, y + 560, sw, 84
        c.fill_rrect(bx, by, bw, bh, 20, (0.17, 0.17, 0.19) if ordered else ZRED)
        lab = "Order placed ✓" if ordered else "Place order"
        c.font(SANS, 32, True); c.text(bx + bw / 2 - c.text_w(lab) / 2, by + 54, lab, (1, 1, 1))
        if TAP2 - 0.5 < t < TAP2 + 0.25: c._dot(bx + bw / 2 + 30, by + 50, 16, (1, 1, 1), 0.85)
        ring(c, bx + bw / 2, by + bh / 2, t, TAP2, ZRED)
        if ordered:
            for i in range(24):
                ang = i / 24 * 6.283; dd = 40 + 200 * ease((t - TAP2) / 1.0)
                c._dot(bx + bw / 2 + math.cos(ang) * dd, by + bh / 2 + math.sin(ang) * dd * 0.6, 4.5, COLS[i % 6], max(0, 1 - (t - TAP2)))
        person(c, W / 2, 1530)
        if t > 1.6: c.pill(W / 2 + 330, 760, "biryani", size=30, fam=MONO, col=YELLOW)
        if t > 2.4: c.pill(W / 2 + 330, 830, "eta: 30 min", size=30, fam=MONO)
    stage.compose(cv, t, d, world, K((0, (W / 2, 560), 1.4), (1.2, ANCHOR, 1.0), (2.6, ANCHOR, 1.0), (3.1, (W / 2, 1030 + 160), 1.7),
                                     (TAP2 + 0.9, (W / 2, 1030 + 160), 1.7), (TAP2 + 1.6, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - TAP2) / 0.1), seed=3)
    hud(cv)


def split_labels(c, active):
    for lab, x, col, on in [("App A", W * 0.27, RED, active == 0), ("App B", W * 0.73, GREEN, active == 1)]:
        c.font(SANS, 76, True); c.text(x - c.text_w(lab) / 2, 560, lab, col if (on or active is None) else DIM)
    for yy in range(600, 1500, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)


def app_a(c, cx, cy, t, w=240, h=440):
    phone(c, cx, cy, w, h)
    c.font(SANS, 28, True); c.text(cx - c.text_w("Order placed") / 2, cy - 40, "Order placed", DOT)
    spinner(c, cx, cy + 40, t)


def app_b(c, cx, cy, t, k, w=240, h=440):
    phone(c, cx, cy, w, h)
    mini_map(c, cx, cy - 40, 190, 260, k)
    c.font(SANS, 24, True); c.text(cx - c.text_w("2.1 km away") / 2, cy + 160, "2.1 km away", GREEN)


def s3(cv, t, d, st):                                     # App A | App B
    def world(c):
        split_labels(c, None if t < 1.4 else (0 if t < d * 0.55 else 1))
        app_a(c, W * 0.27, 960, t); app_b(c, W * 0.73, 960, t, min(1, t / (d + 3)))
        for xx in (W * 0.27, W * 0.73): c.pill(xx, 1270, "wait: 30 min", size=32, fam=MONO)
        if t > d - 2.2: white_pill(c, W / 2, 1420, "same wait. alag feeling?", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.2, ANCHOR, 1.0), (2.0, (W * 0.27, 900), 1.4), (d * 0.5, (W * 0.27, 900), 1.4),
                                     (d * 0.55 + 0.6, (W * 0.73, 900), 1.4), (d - 2.4, (W * 0.73, 900), 1.4), (d - 1.6, ANCHOR, 1.0)), seed=4)
    hud(cv)


OPENS = [0.9, 1.6, 2.2, 2.8, 3.3, 3.7, 4.1]
def s4(cv, t, d, st):                                     # App A anxiety
    n = sum(1 for o in OPENS if t >= o)
    def world(c):
        split_labels(c, 0)
        lx, cy = W * 0.27, 900
        app_a(c, lx, cy, t)
        for o in OPENS: ring(c, lx, cy, t, o, RED)
        c.line(lx, cy + 230, lx, cy + 330)
        person(c, lx, cy + 400)
        if n: c.glow(lx, cy + 370, 70 + 8 * n, 0.12 + 0.05 * n)
        for i in range(min(n, 6)):
            ang = -2.6 + i * 0.5
            c.pill(lx + math.cos(ang) * 175, cy + 390 + math.sin(ang) * 130, "?", size=36, fam=MONO, col=RED)
        col = RED if n > 3 else YELLOW
        c.pill(lx + 40, cy - 290, f"app khola: {n} baar", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=col, bold=True)
        if t > 4.6:
            c.pill(lx + 100, cy + 590, "30 min = 1 ghanta jaisa", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (W * 0.27 + 110, 1050), 1.5), (4.2, (W * 0.27 + 110, 1050), 1.5),
                                     (4.8, (W * 0.27 + 110, 1250), 1.75), (d, (W * 0.27 + 110, 1250), 1.75)),
                  punch=0.05 * sum(max(0, 1 - abs(t - o) / 0.1) for o in OPENS), seed=5)
    hud(cv); flash(cv, t, 4.6)


def s5(cv, t, d, st):                                     # App B progress, calm
    def world(c):
        split_labels(c, 1)
        rx, cy = W * 0.73, 900
        phone(c, rx, cy, 260, 460)
        mini_map(c, rx, cy - 90, 210, 180, min(1, 0.25 + t / (d + 1)))
        steps(c, rx - 90, cy + 40, t, 0.6, gap=40, size=19)
        c.line(rx, cy + 240, rx, cy + 330)
        person(c, rx, cy + 400, col=GREEN)
        c.glow(rx, cy + 370, 90, 0.10)
        if t > 2.0: c.pill(rx - 230, cy + 390, "calm", size=36, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
        if t > 4.4: c.pill(rx - 100, cy + 590, "wait chhota lagta hai", size=34, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (W * 0.73 - 110, 1000), 1.55), (3.6, (W * 0.73 - 110, 1000), 1.55),
                                     (4.4, (W * 0.73 - 110, 1250), 1.7), (d, (W * 0.73 - 110, 1250), 1.7)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # the law + qualitative bars
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "LABOR ILLUSION", 100, W / 2, 640, ease(1 - t / 0.8), col=ZRED)
        l1, l2 = "kaam hota dikhe =", "wait chhota + value zyada"
        n = int(max(0, t - 0.9) * 24)
        mono(c, l1, 760, DOT, 40, chars=n); mono(c, l2, 815, GREEN, 40, chars=max(0, n - len(l1)))
        # qualitative comparison bars (no numbers): perceived wait and perceived value
        k = ease((t - 2.4) / 1.6)
        for gi, (title, a_h, b_h) in enumerate([("wait feels", 1.0, 0.45), ("value feels", 0.45, 1.0)]):
            gx = 230 + gi * 420; base = 1330
            c.font(MONO, 28); c.text(gx + 120 - c.text_w(title) / 2, 1430, title, DIM)
            for bi, (hh, col, lab) in enumerate([(a_h, RED, "A"), (b_h, GREEN, "B")]):
                bx = gx + bi * 140; top = base - 300 * hh * k
                for yy in range(int(base), int(top), -14):
                    for xx in range(int(bx), int(bx + 100), 14): c._dot(xx + 7, yy - 7, 4.2, col, 1)
                c.font(SANS, 30, True); c.text(bx + 38, base + 40, lab, col)
        if t > 4.6: c.pill(W / 2, 1480, "Buell & Norton · Harvard Business School · 2011", size=24, fam=MONO)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.3), (1.8, (W / 2, 1000), 1.0), (4.2, (W / 2, 1000), 1.0),
                                     (5.0, (W / 2, 1150), 1.2), (d - 1.0, (W / 2, 1150), 1.2), (d - 0.4, (W / 2, 1000), 1.0)), seed=7)
    hud(cv)


L7 = ["Order received", "Food being prepared", "Rider on the way", "Arriving in 9 min"]
def s7(cv, t, d, st):                                     # Zomato: every step + live rider
    def world(c):
        mono(c, "live app · zomato", 520, ZRED, 42)
        cx, cy = W / 2, 1020
        x, y = phone(c, cx, cy, 440, 780)
        app_header(c, x + 26, y + 50, 388)
        rx, ry = mini_map(c, cx, cy - 120, 360, 300, min(1, 0.3 + t / (d + 2)))
        st["rider"] = (rx, ry)
        lit = steps(c, cx - 160, cy + 110, t, 0.4, gap=56, names=tuple(L7), size=26, every=0.8)
        for i in range(min(lit, 4)):
            c.pill(cx + 330, cy + 110 + i * 56, ["update", "update", "live", "eta"][i], size=26, fam=MONO,
                   col=(0.05, 0.05, 0.05), bg=GREEN if i < 3 else ZRED, bold=True)
    rider = st.get("rider", (W / 2, 900))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, rider, 1.9), (2.6, rider, 1.9), (3.4, (W / 2, 1200), 1.25), (d, (W / 2, 1200), 1.25)), seed=8)
    hud(cv)


def s8(cv, t, d, st):                                     # DON'T | DO
    def world(c):
        for lab, x, col, on in [("DON'T", W * 0.27, RED, t < 2.4), ("DO", W * 0.73, GREEN, t >= 2.4)]:
            c.font(SANS, 76, True); c.text(x - c.text_w(lab) / 2, 560, lab, col if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        phone(c, lx, 960, 240, 440); spinner(c, lx, 960, t, col=RED)
        c.pill(lx, 1260, "khaali spinner", size=32, fam=MONO, col=RED)
        phone(c, rx, 960, 240, 440); steps(c, rx - 85, 860, t, 2.6, gap=50, size=19, every=0.5)
        c.pill(rx, 1260, "progress dikhao", size=32, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.4), (2.2, (W * 0.27, 900), 1.4), (2.8, (W * 0.73, 900), 1.4),
                                     (d - 1.0, (W * 0.73, 900), 1.4), (d - 0.4, ANCHOR, 1.0)), seed=9)
    hud(cv)


SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे वन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, लेबर इल्यूज़न क्या है?", "", s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("चलो समझते हैं, हमारे लाइव ऐप ज़ोमैटो से। फ्राइडे रात, नौ बजकर सैंतालीस मिनट। रोहन ने बिरयानी ऑर्डर की। डिलीवरी, तीस मिनट।",
          "", s2, min_dur=8.0, whoosh=True, clicks=[TAP2], sfx=[(1.6, "pop_lo"), (2.4, "pop"), (TAP2 + 0.02, "chime")]),
    Scene("अब दो ऐप्स सोचो। दोनों में इंतज़ार तीस मिनट। ऐप ए में सिर्फ लिखा है, ऑर्डर प्लेस्ड। ऐप बी में राइडर मैप पर चलता दिखता है।",
          "", s3, min_dur=8.0, whoosh=True, sfx=[(1.4, "pop"), (2.0, "pop_lo"), (4.6, "pop_hi")]),
    Scene("ऐप ए में रोहन बार बार ऐप खोलता है। कुछ बदलता ही नहीं। तीस मिनट, एक घंटे जैसे लगते हैं।", "", s4, min_dur=6.4,
          whoosh=True, clicks=OPENS, sfx=[(4.6, "buzz")]),
    Scene("ऐप बी में वही तीस मिनट, पर हर स्टेप दिखता है। खाना बन रहा है, राइडर निकल गया। रोहन शांत है।", "", s5, min_dur=6.4,
          whoosh=True, sfx=[(0.6 + i * 0.9, "pop") for i in range(4)] + [(4.4, "chime")]),
    Scene("यही है लेबर इल्यूज़न। हार्वर्ड बिज़नेस स्कूल की रिसर्च कहती है, जब यूज़र को काम होता दिखता है, तो इंतज़ार कम खलता है, और वो सर्विस को ज़्यादा वैल्यू देता है।",
          "", s6, min_dur=10.5, whoosh=True, sfx=[(0.2, "ding"), (2.4, "riser"), (3.3, "pop_hi"), (4.6, "pop")]),
    Scene("इसीलिए ज़ोमैटो में हर स्टेप का अपडेट आता है, और राइडर लाइव दिखता है।", "", s7, min_dur=5.6, whoosh=True,
          sfx=[(0.4 + i * 0.8, "pop") for i in range(4)]),
    Scene("तो अगली बार डिज़ाइन में खाली स्पिनर मत दिखाओ, प्रोग्रेस दिखाओ।", "", s8, min_dur=5.2, whoosh=True,
          sfx=[(0.3, "buzz"), (2.4, "pop"), (2.9, "pop"), (3.4, "pop_hi"), (3.9, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=None, voice="hf_beta", lang="hi",
                                   natural=False, voice_fx=False), 1), "s")

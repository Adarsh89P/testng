"""Day 03/45 · Fitts's Law, explained with Zomato's sticky full-width "View Cart" bar.

Day 02 pattern: same voice (hf_beta, 1.05, unprocessed), colour accents, zoom in/out, dot animations, SFX,
lowered DAY badge, no captions, series intro + single follow outro.
"""
import sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 3, "Jakob's Law"
W, H = 1080, 1920
ZRED = (0.886, 0.216, 0.267)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR, FULL = D.ANCHOR, D.FULL
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone

PX, PY, PW, PH = W / 2, 1040, 470, 860          # main phone geometry
X0, Y0 = PX - PW / 2, PY - PH / 2


def menu_rows(c, top, n=7, added=(), a=1.0, x=None, w=None):
    x = x if x is not None else X0 + 26; w = w if w is not None else PW - 52
    for i in range(n):
        y = top + i * 104
        col = COLS[i % 6]
        c.drrect(x, y, 70, 70, 14, spacing=5.5, r=1.6, col=col, a=a); c._dot(x + 35, y + 35, 9, col, 0.8 * a)
        c.dbar(x + 88, y + 14, w * 0.42, rows=3, gap=6, a=a); c.dbar(x + 88, y + 46, w * 0.22, rows=2, gap=6, col=DIM, a=a)
        bx = x + w - 110
        if i in added:
            c.fill_rrect(bx, y + 16, 104, 42, 10, GREEN, a); c.font(SANS, 20, True); c.text(bx + 22, y + 44, "– 1 +", (0.05, 0.05, 0.05), a)
        else:
            c.drrect(bx, y + 16, 104, 42, 10, spacing=5, r=1.5, col=GREEN, a=a); c.font(SANS, 20, True); c.text(bx + 30, y + 44, "ADD", GREEN, a)
    return [(x + w - 58, top + i * 104 + 37) for i in range(n)]


def thumb(c, x, y, a=1.0, col=(1, 1, 1)):
    c.glow(x, y, 46, 0.35 * a); c._dot(x, y, 20, col, 0.9 * a)
    c.dellipse(x, y, 30, 30, spacing=6, r=1.6, col=col, a=0.8 * a)


def miss(c, x, y, t, at):
    lt = t - at
    if 0 <= lt < 0.7:
        k = lt / 0.7; c.c.set_source_rgba(*RED, 1 - k); c.c.set_line_width(5)
        s = 22 + 10 * k
        c.c.move_to(x - s, y - s); c.c.line_to(x + s, y + s); c.c.move_to(x + s, y - s); c.c.line_to(x - s, y + s); c.c.stroke()


def cart_bar(c, k, items=2, total=498):
    if k <= 0: return None
    h = 96; y = Y0 + PH - 24 - (h + 10) * ease(k)
    x, w = X0 + 22, PW - 44
    c.fill_rrect(x, y, w, h, 18, ZRED)
    c.font(SANS, 24, True); c.text(x + 26, y + 40, f"{items} items added", (1, 1, 1))
    c.font(SANS, 20); c.text(x + 26, y + 70, f"₹{total}", (1, 1, 1))
    c.font(SANS, 26, True); c.text(x + w - 170, y + 58, "View Cart ›", (1, 1, 1))
    return (x, y, w, h)


def app_top(c):
    c.font(SANS, 34, True); c.text(X0 + 28, Y0 + 92, "zomato", ZRED)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # question hook
    def world(c):
        mono(c, "UX designer ho?", 720, DOT, 62, chars=int(t * 14))
        if t > 1.3:
            dot_text(c, "FITTS'S LAW", 120, W / 2, 900, ease(1 - (t - 1.3) / 0.8), col=BLUE)
            c.glow(W / 2, 900, 400, 0.08)
        if t > 2.5: mono(c, "kya hai?", 1060, DOT, 62, chars=int((t - 2.5) * 14))
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 900 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.35), (1.3, (W / 2, 900), 1.35), (2.2, (W / 2, 900), 1.0)), seed=2)
    hud(cv); flash(cv, t, 1.3)


ADDS = [1.6, 2.6]
def s2(cv, t, d, st):                                     # story: one hand, adding food
    def world(c):
        mono(c, "ek haath mein phone, doosre mein chai", 520, (0.85, 0.85, 0.88), 34)
        phone(c, PX, PY, PW, PH); app_top(c)
        added = tuple(i for i, a in zip((1, 3), ADDS) if t >= a)
        btn = menu_rows(c, Y0 + 140, added=added)
        for i, a in zip((1, 3), ADDS):
            ring(c, *btn[i], t, a, GREEN)
            if a - 0.6 < t < a + 0.2: thumb(c, btn[i][0] + 6, btn[i][1] + 8)
        # chai cup in the other hand (dotted)
        cx, cy = PX + 380, 1380
        c.drrect(cx - 50, cy - 60, 100, 120, 18, spacing=6, r=2, col=YELLOW)
        c.dellipse(cx + 62, cy, 22, 30, -90, 90, spacing=6, r=2, col=YELLOW)
        for i in range(3):
            c.dots_path([(cx - 20 + i * 20, cy - 80), (cx - 10 + i * 20, cy - 110 - 10 * math.sin(t * 3 + i)), (cx - 20 + i * 20, cy - 140)], spacing=7, r=2, col=(0.8, 0.8, 0.8))
    keys = [(0, ANCHOR, 1.0)]
    for a in ADDS: keys += [(a - 0.5, (PX + 120, Y0 + 300 + (ADDS.index(a)) * 208), 1.7), (a + 0.4, (PX + 120, Y0 + 300 + (ADDS.index(a)) * 208), 1.7)]
    keys += [(ADDS[-1] + 1.1, ANCHOR, 1.0)]
    stage.compose(cv, t, d, world, K(*keys), punch=0.05 * sum(max(0, 1 - abs(t - a) / 0.1) for a in ADDS), seed=3)
    hud(cv)


MISS = [2.8, 3.8]
def s3(cv, t, d, st):                                     # App A: tiny View Cart in the top corner
    def world(c):
        c.font(SANS, 76, True); c.text(W / 2 - c.text_w("App A") / 2, 540, "App A", RED)
        phone(c, PX, PY, PW, PH); app_top(c)
        menu_rows(c, Y0 + 140, added=(1, 3), a=0.5)
        tx, ty = X0 + PW - 70, Y0 + 82                    # tiny target
        c.font(SANS, 16, True); c.text(tx - 34, ty + 6, "cart ›", ZRED)
        ring(c, tx, ty, t, 1.0, RED)
        # thumb stretching from bottom-right towards the corner
        sx, sy = X0 + PW - 80, Y0 + PH - 120
        u = min(1, max(0, (t - 1.8) / 1.0)); u2 = min(1, max(0, (t - 3.2) / 0.6))
        reach = [(sx, sy), (sx - 40, sy - 300), (tx + 30, ty + 80)]
        c.dots_path(reach, spacing=12, r=2.6, col=RED, a=0.8, reveal=u)
        if t > 1.8:
            px = lerp(sx, tx + 26, ease(u)); py = lerp(sy, ty + 40, ease(u))
            if t > 3.2: px, py = lerp(tx + 26, tx - 24, ease(u2)), lerp(ty + 40, ty + 34, ease(u2))
            thumb(c, px, py, col=(1, 0.85, 0.85))
        for m in MISS: miss(c, tx + (24 if m == MISS[0] else -26), ty + 34, t, m)
        if t > 1.2:
            c.pill(PX + 330, Y0 + 70, "W: tiny", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
        if t > 2.0:
            c.pill(PX + 330, Y0 + 140, "D: far", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
        if t > 4.4: white_pill(c, W / 2, 1560, "angootha pahunchta hi nahi", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (X0 + PW - 90, Y0 + 160), 2.1), (1.7, (X0 + PW - 90, Y0 + 160), 2.1),
                                     (2.4, (PX + 60, PY - 60), 1.15), (3.4, (X0 + PW - 90, Y0 + 160), 1.9), (4.3, (X0 + PW - 90, Y0 + 160), 1.9),
                                     (5.0, ANCHOR, 1.0)),
                  punch=0.06 * sum(max(0, 1 - abs(t - m) / 0.1) for m in MISS), seed=4)
    hud(cv)
    for m in MISS: flash(cv, t, m, 0.12)


def zone_dots(c, k):
    """Thumb-reach heat zones (right-handed) filled with coloured dots."""
    cx, cy = X0 + PW + 30, Y0 + PH + 40
    for yy in range(int(Y0 + 120), int(Y0 + PH - 20), 22):
        for xx in range(int(X0 + 30), int(X0 + PW - 20), 22):
            dist = math.hypot(xx - cx, yy - cy)
            col = GREEN if dist < 430 else (YELLOW if dist < 640 else RED)
            rev = 1 - (dist - 150) / 800
            if k >= max(0, 1 - rev): c._dot(xx, yy, 4.2, col, 0.85)


def s4(cv, t, d, st):                                     # thumb zone
    def world(c):
        phone(c, PX, PY, PW, PH)
        zone_dots(c, ease((t - 0.4) / 2.0))
        if t > 2.2:
            c.pill(PX - 330, Y0 + 230, "hard", size=32, fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
            c.pill(PX - 330, PY, "ok", size=32, fam=MONO, col=(0.05, 0.05, 0.05), bg=YELLOW, bold=True)
            c.pill(PX + 330, Y0 + PH - 160, "easy", size=32, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
        if t > 3.0: white_pill(c, W / 2, 1560, "THUMB ZONE", 40)
        thumb(c, X0 + PW - 60 + 10 * math.sin(t * 2), Y0 + PH - 110 + 8 * math.cos(t * 2))
    stage.compose(cv, t, d, world, K((0, (PX, PY + 200), 1.4), (2.4, (PX, PY), 1.0), (d - 1.6, (PX, PY), 1.0), (d - 0.6, (PX + 120, PY + 300), 1.45)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # the law: size + distance
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "FITTS'S LAW", 116, W / 2, 640, ease(1 - t / 0.8), col=BLUE)
        l1, l2 = "bada + paas wala target =", "fast + easy tap"
        n = int(max(0, t - 0.9) * 24)
        mono(c, l1, 760, DOT, 40, chars=n); mono(c, l2, 815, GREEN, 40, chars=max(0, n - len(l1)))
        sx, sy = 210, 1250                                 # start point
        c._dot(sx, sy, 10, (1, 1, 1), 1); c.font(MONO, 24); c.text(sx - 40, sy + 50, "start", DIM)
        # far + small (red) vs near + big (green)
        fx_, fy_ = 900, 930; c.fill_rrect(fx_ - 22, fy_ - 22, 44, 44, 10, RED); c.font(MONO, 22); c.text(fx_ - 90, fy_ - 40, "far + small", RED)
        nx, ny = 560, 1250; c.fill_rrect(nx - 90, ny - 70, 180, 140, 20, GREEN); c.text(nx - 66, ny + 110, "near + big", GREEN)
        k1 = ease((t - 2.4) / 2.2); k2 = ease((t - 2.4) / 0.8)
        c.dots_path([(sx, sy), (fx_, fy_)], spacing=12, r=3, col=RED, reveal=k1)
        c.dots_path([(sx, sy), (nx - 90, ny)], spacing=12, r=3, col=GREEN, reveal=k2)
        if k2 >= 1: c.pill(nx, ny - 120, "fast", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
        if k1 >= 1: c.pill(fx_, fy_ + 80, "slow", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
        if t > 5.2: c.pill(W / 2, 1460, "T = a + b · log2(D/W + 1)", size=32, fam=MONO)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1060), 1.0), (4.4, (W / 2, 1060), 1.0),
                                     (5.0, (W / 2, 1300), 1.25), (d - 1.0, (W / 2, 1300), 1.25), (d - 0.4, (W / 2, 1060), 1.0)), seed=6)
    hud(cv)


TAP6 = 4.6
def s6(cv, t, d, st):                                     # Zomato: full-width sticky bottom bar
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("zomato") / 2, 540, "zomato", ZRED)
        phone(c, PX, PY, PW, PH); app_top(c)
        sc = max(0, t - 2.4) * 160
        c.c.save(); c.rrect_path(X0 + 14, Y0 + 120, PW - 28, PH - 140, 30); c.c.clip()
        menu_rows(c, Y0 + 140 - sc, n=12, added=(1, 3))
        c.c.restore()
        bar = cart_bar(c, ease((t - 0.8) / 0.6))
        if bar:
            x, y, w, h = bar
            if t > 1.6: c.pill(PX + 330, y - 30, "W: full width", size=28, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
            if t > 2.2: c.pill(PX + 330, y + 40, "D: thumb ke paas", size=28, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
            if t > 3.0: c.pill(PX - 330, y + 10, "stays", size=28, fam=MONO, col=GREEN)
            if TAP6 - 0.6 < t < TAP6 + 0.25: thumb(c, x + w - 120, y + 50)
            ring(c, x + w - 120, y + 50, t, TAP6, GREEN)
            if t >= TAP6:
                for i in range(26):
                    ang = i / 26 * 6.283; dd = 40 + 220 * ease((t - TAP6) / 1.0)
                    c._dot(x + w - 120 + math.cos(ang) * dd, y + 50 + math.sin(ang) * dd * 0.6, 4.5, COLS[i % 6], max(0, 1 - (t - TAP6)))
    bar_c = (PX, Y0 + PH - 80)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.9, bar_c, 1.7), (2.2, bar_c, 1.7), (2.9, ANCHOR, 1.0), (TAP6 - 0.6, ANCHOR, 1.0),
                                     (TAP6 - 0.1, (PX + 100, Y0 + PH - 80), 1.9), (TAP6 + 0.9, (PX + 100, Y0 + PH - 80), 1.9), (TAP6 + 1.5, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - TAP6) / 0.1), seed=7)
    hud(cv)


def s7(cv, t, d, st):                                     # DON'T | DO with 48dp
    def world(c):
        for lab, x, col, on in [("DON'T", W * 0.27, RED, t < 2.6), ("DO", W * 0.73, GREEN, t >= 2.6)]:
            c.font(SANS, 76, True); c.text(x - c.text_w(lab) / 2, 560, lab, col if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx, cy = W * 0.27, W * 0.73, 980
        phone(c, lx, cy, 240, 440); phone(c, rx, cy, 240, 440)
        c.fill_rrect(lx + 62, cy - 186, 26, 26, 6, RED)                       # tiny corner target
        c.pill(lx, cy + 280, "chhota + door", size=30, fam=MONO, col=RED)
        bx, by, bw, bh = rx - 96, cy + 120, 192, 66                            # big bottom CTA
        c.fill_rrect(bx, by, bw, bh, 16, GREEN)
        c.font(SANS, 24, True); c.text(rx - c.text_w("Checkout") / 2, by + 42, "Checkout", (0.05, 0.05, 0.05))
        if t > 3.2:                                                            # 48dp measure
            c.line(bx + bw + 16, by, bx + bw + 16, by + bh, YELLOW, 3)
            c.pill(bx + bw + 76, by + bh / 2, "≥ 48dp", size=26, fam=MONO, col=(0.05, 0.05, 0.05), bg=YELLOW, bold=True)
        c.pill(rx, cy + 280, "bada + paas", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
        if t > 4.4: white_pill(c, W / 2, 1450, "zaroori button = thumb zone mein", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.4), (2.3, (W * 0.27, 900), 1.4), (2.9, (W * 0.73, 1000), 1.5),
                                     (3.8, (W * 0.73, 1000), 1.5), (4.4, ANCHOR, 1.0)), seed=8)
    hud(cv)


SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे थ्री।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, फिट्स लॉ क्या है?", "", s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("रोहन ज़ोमैटो पर खाना ऐड कर रहा है। एक हाथ में फोन, और दूसरे में चाय।", "", s2, min_dur=5.6, whoosh=True,
          clicks=ADDS, sfx=[(a + 0.02, "pop") for a in ADDS]),
    Scene("अब सोचो, अगर व्यू कार्ट का बटन ऊपर कोने में, छोटा सा होता। अंगूठा पहुँचता ही नहीं, और गलत जगह टैप हो जाता।", "", s3, min_dur=6.4,
          whoosh=True, clicks=MISS, sfx=[(1.0, "pop_lo"), (1.8, "riser")] + [(m + 0.02, "buzz") for m in MISS]),
    Scene("हमारा अंगूठा स्क्रीन के नीचे वाले हिस्से में सबसे आसानी से पहुँचता है। इसे थंब ज़ोन कहते हैं।", "", s4, min_dur=6.0, whoosh=True,
          sfx=[(0.4, "riser"), (2.2, "pop"), (2.4, "pop"), (2.6, "pop_hi"), (3.0, "ding")]),
    Scene("यही है फिट्स लॉ। बटन जितना बड़ा, और जितना पास, उसे टैप करना उतना आसान और तेज़।", "", s5, min_dur=8.0, whoosh=True,
          sfx=[(0.2, "ding"), (2.4, "pop"), (3.2, "pop_hi"), (4.6, "buzz"), (5.2, "pop")]),
    Scene("इसीलिए ज़ोमैटो में व्यू कार्ट बार नीचे होता है, पूरी चौड़ाई में, और स्क्रॉल करने पर भी वहीं रहता है।", "", s6, min_dur=7.4, whoosh=True,
          clicks=[TAP6], sfx=[(0.8, "pop_lo"), (1.6, "pop"), (2.2, "pop"), (TAP6 + 0.02, "chime")] + [(2.5 + i * 0.25, "tick") for i in range(6)]),
    Scene("डिज़ाइनर टिप। ज़रूरी बटन बड़े रखो, और अंगूठे की पहुँच में। टैप टारगेट कम से कम अड़तालीस डी पी।", "", s7, min_dur=6.6, whoosh=True,
          sfx=[(0.3, "buzz"), (2.6, "pop"), (3.2, "pop_hi"), (4.4, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=None, voice="hf_beta", lang="hi",
                                   natural=False, voice_fx=False), 1), "s")

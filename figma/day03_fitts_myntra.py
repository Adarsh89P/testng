"""Day 03/45 · Fitts's Law, explained with Myntra's sticky bottom "ADD TO BAG" button.

Reuses the app-agnostic scenes of day03_fitts_law (hook, thumb zone, law card, designer tip) and replaces the
story / bad example / solution with a Myntra product page. Same voice and Day 02 pattern.
"""
import sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D
import day03_fitts_law as F

D.DAY, D.NEXT = 3, "Jakob's Law"
W, H = 1080, 1920
MPINK = (1.0, 0.247, 0.424)                        # Myntra pink
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
PX, PY, PW, PH, X0, Y0 = F.PX, F.PY, F.PW, F.PH, F.X0, F.Y0
thumb, miss = F.thumb, F.miss


def app_top(c):
    c.font(SANS, 34, True); c.text(X0 + 28, Y0 + 92, "myntra", MPINK)


def product_page(c, scroll=0.0, size_on=None, a=1.0):
    """Dotted Myntra-style product page: sneaker image, price, sizes, details."""
    x, w = X0 + 26, PW - 52
    top = Y0 + 120 - scroll
    c.drrect(x, top, w, 330, 20, spacing=6, r=1.6, col=(0.45, 0.45, 0.5), a=a)               # image box
    sx, sy = x + w / 2, top + 190                                                            # dotted sneaker
    c.dots_path([(sx - 140, sy + 40), (sx + 150, sy + 40)], spacing=8, r=2.6, col=DOT, a=a)  # sole
    c.dots_path([(sx - 140, sy + 40), (sx - 130, sy - 10), (sx - 40, sy - 30), (sx + 10, sy - 80), (sx + 70, sy - 70),
                 (sx + 150, sy + 10), (sx + 150, sy + 40)], spacing=7, r=2.4, col=MPINK, a=a)
    for i in range(4): c._dot(sx - 10 + i * 22, sy - 40 + i * 6, 3.5, DOT, a)                 # laces
    y = top + 360
    c.font(SANS, 26, True); c.text(x, y + 28, "Running Sneakers", DOT, a)
    c.font(SANS, 30, True); c.text(x, y + 76, "₹2,999", DOT, a)
    c.font(SANS, 22); c.text(x + 120, y + 74, "₹4,999", DIM, a); c.line(x + 118, y + 66, x + 196, y + 66, DIM, 2, a)
    c.font(SANS, 22, True); c.text(x + 212, y + 74, "40% OFF", ORANGE, a)
    c.font(SANS, 20, True); c.text(x, y + 126, "SELECT SIZE", DIM, a)
    chips = []
    for i, s in enumerate(["6", "7", "8", "9", "10"]):
        cx = x + 34 + i * 72; cy = y + 170
        on = s == size_on
        if on: c.c.set_source_rgba(*MPINK, a); c.c.arc(cx, cy, 28, 0, 6.3); c.c.fill()
        c.dellipse(cx, cy, 28, 28, spacing=6, r=1.5, col=MPINK if on else (0.6, 0.6, 0.65), a=a)
        c.font(SANS, 22, True); c.text(cx - c.text_w(s) / 2, cy + 8, s, (1, 1, 1) if on else DOT, a)
        chips.append((cx, cy))
    for i in range(6): c.dbar(x, y + 230 + i * 34, w * (0.9 - 0.08 * (i % 3)), rows=2, gap=6, col=DIM, a=a)
    return chips


def bag_bar(c, k):
    if k <= 0: return None
    h = 96; y = Y0 + PH - 24 - (h + 10) * ease(k)
    x, w = X0 + 22, PW - 44
    c.fill_rrect(x - 4, y - 14, w + 8, h + 28, 10, (0.06, 0.06, 0.07))
    ww = w * 0.38
    c.rrect_path(x, y, ww, h, 12); c.c.set_source_rgba(0.7, 0.7, 0.75, 1); c.c.set_line_width(2); c.c.stroke()
    c.font(SANS, 22, True); c.text(x + ww / 2 - c.text_w("WISHLIST") / 2, y + 58, "WISHLIST", DOT)
    bx, bw = x + ww + 14, w - ww - 14
    c.fill_rrect(bx, y, bw, h, 12, MPINK)
    c.font(SANS, 24, True); c.text(bx + bw / 2 - c.text_w("ADD TO BAG") / 2, y + 58, "ADD TO BAG", (1, 1, 1))
    return (bx, y, bw, h)


# ------------------------------------------------------------------ Myntra scenes
TAPSIZE = 3.0
def s2(cv, t, d, st):                                     # story: metro, one hand on the handle
    def world(c):
        mono(c, "metro · ek haath handle pe", 520, (0.85, 0.85, 0.88), 36)
        hx, hy = PX + 350, 640                            # dotted metro handle + strap
        c.dline(hx, 560, hx, hy - 40, spacing=7, r=2, col=(0.6, 0.6, 0.65))
        c.dellipse(hx, hy, 46, 46, spacing=6, r=2.2, col=YELLOW)
        c._dot(hx, hy + 60, 14, (1, 1, 1), 0.4)
        phone(c, PX, PY, PW, PH); app_top(c)
        chips = product_page(c, size_on="8" if t >= TAPSIZE else None)
        st["chip8"] = chips[2]
        ring(c, *chips[2], t, TAPSIZE, MPINK)
        if TAPSIZE - 0.6 < t < TAPSIZE + 0.25: thumb(c, chips[2][0] + 8, chips[2][1] + 10)
        if t > 1.2: c.pill(PX - 330, 900, "sneakers", size=30, fam=MONO, col=MPINK)
    ch = st.get("chip8", (PX, 1300))
    stage.compose(cv, t, d, world, K((0, (PX + 120, 720), 1.35), (1.4, ANCHOR, 1.0), (TAPSIZE - 0.6, ch, 1.9),
                                     (TAPSIZE + 0.7, ch, 1.9), (TAPSIZE + 1.3, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - TAPSIZE) / 0.1), seed=3)
    hud(cv)


MISS = F.MISS
def s3(cv, t, d, st):                                     # App A: tiny "bag" in the top corner
    def world(c):
        c.font(SANS, 76, True); c.text(W / 2 - c.text_w("App A") / 2, 540, "App A", RED)
        phone(c, PX, PY, PW, PH); app_top(c)
        product_page(c, size_on="8", a=0.5)
        tx, ty = X0 + PW - 70, Y0 + 82
        c.font(SANS, 16, True); c.text(tx - 40, ty + 6, "+ bag", MPINK)
        ring(c, tx, ty, t, 1.0, RED)
        sx, sy = X0 + PW - 80, Y0 + PH - 120
        u = min(1, max(0, (t - 1.8) / 1.0)); u2 = min(1, max(0, (t - 3.2) / 0.6))
        c.dots_path([(sx, sy), (sx - 40, sy - 300), (tx + 30, ty + 80)], spacing=12, r=2.6, col=RED, a=0.8, reveal=u)
        if t > 1.8:
            px = lerp(sx, tx + 26, ease(u)); py = lerp(sy, ty + 40, ease(u))
            if t > 3.2: px, py = lerp(tx + 26, tx - 24, ease(u2)), lerp(ty + 40, ty + 34, ease(u2))
            thumb(c, px, py, col=(1, 0.85, 0.85))
        for m in MISS: miss(c, tx + (24 if m == MISS[0] else -26), ty + 34, t, m)
        if t > 1.2: c.pill(PX + 330, Y0 + 70, "W: tiny", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
        if t > 2.0: c.pill(PX + 330, Y0 + 140, "D: far", size=30, fam=MONO, col=(0.05, 0.05, 0.05), bg=RED, bold=True)
        if t > 4.4: white_pill(c, W / 2, 1560, "angootha pahunchta hi nahi", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (X0 + PW - 90, Y0 + 160), 2.1), (1.7, (X0 + PW - 90, Y0 + 160), 2.1),
                                     (2.4, (PX + 60, PY - 60), 1.15), (3.4, (X0 + PW - 90, Y0 + 160), 1.9), (4.3, (X0 + PW - 90, Y0 + 160), 1.9),
                                     (5.0, ANCHOR, 1.0)),
                  punch=0.06 * sum(max(0, 1 - abs(t - m) / 0.1) for m in MISS), seed=4)
    hud(cv)
    for m in MISS: flash(cv, t, m, 0.12)


TAP6 = 4.6
def s6(cv, t, d, st):                                     # Myntra: sticky bottom ADD TO BAG
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("myntra") / 2, 540, "myntra", MPINK)
        phone(c, PX, PY, PW, PH); app_top(c)
        sc = max(0, t - 2.4) * 140
        c.c.save(); c.rrect_path(X0 + 14, Y0 + 110, PW - 28, PH - 130, 30); c.c.clip()
        product_page(c, scroll=sc, size_on="8")
        c.c.restore()
        bar = bag_bar(c, ease((t - 0.8) / 0.6))
        if bar:
            x, y, w, h = bar
            if t > 1.6: c.pill(PX + 330, y - 30, "W: bada", size=28, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
            if t > 2.2: c.pill(PX + 330, y + 40, "D: thumb ke paas", size=28, fam=MONO, col=(0.05, 0.05, 0.05), bg=GREEN, bold=True)
            if t > 3.0: c.pill(PX - 330, y + 10, "stays", size=28, fam=MONO, col=GREEN)
            tx, ty = x + w / 2, y + h / 2
            if TAP6 - 0.6 < t < TAP6 + 0.25: thumb(c, tx + 10, ty + 6)
            ring(c, tx, ty, t, TAP6, GREEN)
            if t >= TAP6:
                for i in range(26):
                    ang = i / 26 * 6.283; dd = 40 + 220 * ease((t - TAP6) / 1.0)
                    c._dot(tx + math.cos(ang) * dd, ty + math.sin(ang) * dd * 0.6, 4.5, COLS[i % 6], max(0, 1 - (t - TAP6)))
                c.pill(tx, y - 70, "added to bag ✓", size=28, fam=SANS, col=(0.05, 0.05, 0.05), bg=MPINK, bold=True)
    bar_c = (PX + 60, Y0 + PH - 80)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.9, bar_c, 1.7), (2.2, bar_c, 1.7), (2.9, ANCHOR, 1.0), (TAP6 - 0.6, ANCHOR, 1.0),
                                     (TAP6 - 0.1, bar_c, 1.9), (TAP6 + 0.9, bar_c, 1.9), (TAP6 + 1.5, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - TAP6) / 0.1), seed=7)
    hud(cv)


SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे थ्री।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, फिट्स लॉ क्या है?", "", F.s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("प्रिया मेट्रो में खड़ी है। एक हाथ से हैंडल पकड़ा है, और दूसरे हाथ में फोन। मिंत्रा पर स्नीकर्स पसंद आ गए।", "", s2, min_dur=6.4,
          whoosh=True, clicks=[TAPSIZE], sfx=[(1.2, "pop_lo"), (TAPSIZE + 0.02, "pop_hi")]),
    Scene("अब सोचो, अगर ऐड टू बैग का बटन ऊपर कोने में, छोटा सा होता। अंगूठा पहुँचता ही नहीं, और गलत जगह टैप हो जाता।", "", s3, min_dur=6.4,
          whoosh=True, clicks=MISS, sfx=[(1.0, "pop_lo"), (1.8, "riser")] + [(m + 0.02, "buzz") for m in MISS]),
    Scene("हमारा अंगूठा स्क्रीन के नीचे वाले हिस्से में सबसे आसानी से पहुँचता है। इसे थंब ज़ोन कहते हैं।", "", F.s4, min_dur=6.0, whoosh=True,
          sfx=[(0.4, "riser"), (2.2, "pop"), (2.4, "pop"), (2.6, "pop_hi"), (3.0, "ding")]),
    Scene("यही है फिट्स लॉ। बटन जितना बड़ा, और जितना पास, उसे टैप करना उतना आसान और तेज़।", "", F.s5, min_dur=8.0, whoosh=True,
          sfx=[(0.2, "ding"), (2.4, "pop"), (3.2, "pop_hi"), (4.6, "buzz"), (5.2, "pop")]),
    Scene("इसीलिए मिंत्रा में ऐड टू बैग बटन नीचे होता है, बड़ा और चौड़ा, और स्क्रॉल करने पर भी वहीं रहता है।", "", s6, min_dur=7.4, whoosh=True,
          clicks=[TAP6], sfx=[(0.8, "pop_lo"), (1.6, "pop"), (2.2, "pop"), (TAP6 + 0.02, "chime")] + [(2.5 + i * 0.25, "tick") for i in range(6)]),
    Scene("डिज़ाइनर टिप। ज़रूरी बटन बड़े रखो, और अंगूठे की पहुँच में। टैप टारगेट कम से कम अड़तालीस डी पी।", "", F.s7, min_dur=6.6, whoosh=True,
          sfx=[(0.3, "buzz"), (2.6, "pop"), (3.2, "pop_hi"), (4.4, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=None, voice="hf_beta", lang="hi",
                                   natural=False, voice_fx=False), 1), "s")

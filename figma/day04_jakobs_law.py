"""Day 04/45 · Jakob's Law, explained with Instagram Reels vs YouTube Shorts.

Users spend most of their time in OTHER apps, so they expect yours to work the same way: swipe up for the next
video, double-tap to like, actions on the right. Same Day 02 pattern and the Hinglish hf_beta voice (Days 1-3).
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 4, "Miller's Law"
W, H = 1080, 1920
IGPINK = (0.93, 0.25, 0.53)
YTRED = (1.0, 0.18, 0.18)
PURPLE = (0.72, 0.52, 1.0)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)


def heart(c, x, y, s, col, a=1.0, fill=False):
    pts = []
    for i in range(41):
        u = i / 40 * 6.283
        hx = 16 * math.sin(u) ** 3
        hy = -(13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u))
        pts.append((x + hx * s, y + hy * s))
    if fill:
        c.c.move_to(*pts[0])
        for p in pts[1:]: c.c.line_to(*p)
        c.c.close_path(); c.c.set_source_rgba(*col, a); c.c.fill()
    else:
        c.dots_path(pts, spacing=max(4, 6 * s / 2), r=1.9, col=col, a=a, closed=True)


def bubble(c, x, y, s, col, a=1.0):
    c.dellipse(x, y, 15 * s, 13 * s, spacing=5, r=1.8, col=col, a=a)
    c.dots_path([(x - 8 * s, y + 10 * s), (x - 14 * s, y + 20 * s), (x - 2 * s, y + 13 * s)], spacing=4, r=1.6, col=col, a=a)


def share(c, x, y, s, col, a=1.0):
    c.dots_path([(x - 14 * s, y + 12 * s), (x + 14 * s, y - 12 * s), (x + 2 * s, y + 16 * s), (x - 2 * s, y + 2 * s),
                 (x - 14 * s, y + 12 * s)], spacing=5, r=1.8, col=col, a=a)


def clip(c, x, y, w, h, seed, a=1.0):
    """One dotted 'video': a coloured blob scene + caption bars."""
    col = COLS[seed % 6]
    cx, cy = x + w / 2, y + h * 0.42
    for i, r in enumerate((110, 80, 50)):
        c.dellipse(cx + 20 * math.sin(seed + i), cy, r, r * 0.9, spacing=8 - i, r=2.2, col=col if i != 1 else DOT, a=a)
    c._dot(cx, cy, 18, col, 0.8 * a)
    c.dellipse(x + 46, y + h - 120, 20, 20, spacing=5, r=1.6, col=DOT, a=a)
    c.dbar(x + 78, y + h - 128, w * 0.35, rows=2, gap=6, a=a)
    c.dbar(x + 30, y + h - 82, w * 0.6, rows=2, gap=6, col=DIM, a=a)


def shorts_screen(c, cx, cy, w, h, brand, col, swipe=0.0, idx=0, liked=False, like_at=None, t=0.0,
                  layout="std", a=1.0):
    """Reels / Shorts style screen. swipe 0..1 moves to the next clip. layout 'odd' = the confusing App C."""
    x, y = phone(c, cx, cy, w, h, a=a)
    ix, iy, iw, ih = x + 16, y + 16, w - 32, h - 32
    c.c.save(); c.rrect_path(ix, iy, iw, ih, w * 0.11); c.c.clip()
    off = ease(swipe) * ih
    clip(c, ix, iy - off, iw, ih, idx, a)
    if swipe > 0: clip(c, ix, iy + ih - off, iw, ih, idx + 1, a)
    c.c.restore()
    c.font(SANS, 28, True); c.text(x + 34, y + 74, brand, col, a)
    if layout == "std":                                   # actions on the right, like everyone else
        rx = x + w - 52
        heart(c, rx, y + h * 0.55, 1.5, col if liked else DOT, a, fill=liked)
        bubble(c, rx, y + h * 0.66, 1.3, DOT, a)
        share(c, rx, y + h * 0.76, 1.2, DOT, a)
        if like_at is not None and 0 <= t - like_at < 0.9:  # big double-tap heart
            k = (t - like_at) / 0.9
            heart(c, cx, cy - 40, 4.5 * (0.6 + 0.6 * ease(min(1, k * 3))), col, a * (1 - k) ** 0.5, fill=True)
        return (rx, y + h * 0.55)
    # odd layout: like hidden in a top-left menu, "next" is a tiny arrow at the top
    c.font(SANS, 30, True); c.text(x + 40, y + 130, "•••", DOT, a)
    c.drrect(x + w - 120, y + 100, 70, 44, 12, spacing=5, r=1.5, col=DIM, a=a)
    c.font(SANS, 18, True); c.text(x + w - 104, y + 129, "next", DIM, a)
    return (x + w - 85, y + 122)


def swipe_hand(c, x, y0, y1, t, t0, dur=0.7):
    if t0 - 0.3 < t < t0 + dur + 0.2:
        u = ease(min(1, max(0, (t - t0) / dur)))
        y = lerp(y0, y1, u)
        c.dots_path([(x, y0), (x, y)], spacing=12, r=3, col=(1, 1, 1), a=0.5)
        c._dot(x, y, 16, (1, 1, 1), 0.9)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # question hook
    def world(c):
        mono(c, "UX designer ho?", 720, DOT, 62, chars=int(t * 14))
        if t > 1.3:
            dot_text(c, "JAKOB'S LAW", 120, W / 2, 900, ease(1 - (t - 1.3) / 0.8), col=PURPLE)
            c.glow(W / 2, 900, 400, 0.08)
        if t > 2.5: mono(c, "kya hai?", 1060, DOT, 62, chars=int((t - 2.5) * 14))
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 900 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.35), (1.3, (W / 2, 900), 1.35), (2.2, (W / 2, 900), 1.0)), seed=2)
    hud(cv); flash(cv, t, 1.3)


LX, RX, SY, SW, SH = 290, 790, 1080, 400, 760
SW1, SW2 = 1.6, 4.4                                       # swipe-up on Reels, then on Shorts
def s2(cv, t, d, st):                                     # story: Reels -> Shorts, the thumb already knows
    def world(c):
        mono(c, "raat 11 baje · scroll time", 560, (0.85, 0.85, 0.88), 36)
        shorts_screen(c, LX, SY, SW, SH, "Reels", IGPINK, swipe=(t - SW1) / 0.7 if t > SW1 else 0, idx=0, t=t)
        swipe_hand(c, LX + 60, SY + 220, SY - 160, t, SW1)
        a2 = min(1, max(0, (t - 2.6) / 0.5))
        if a2 > 0:
            shorts_screen(c, RX, SY, SW, SH, "Shorts", YTRED, swipe=(t - SW2) / 0.7 if t > SW2 else 0, idx=2, t=t, a=a2)
            swipe_hand(c, RX + 60, SY + 220, SY - 160, t, SW2)
        if t > 3.0:
            c.dots_path([(LX + 220, SY - 420), (W / 2, SY - 470), (RX - 220, SY - 420)], spacing=12, r=3, col=PURPLE,
                        reveal=min(1, (t - 3.0) / 0.6))
        if t > SW2 + 0.8: white_pill(c, W / 2, 1560, "kisi ne sikhaya nahi!", 38)
    stage.compose(cv, t, d, world, K((0, (LX, SY + 60), 1.3), (2.3, (LX, SY + 60), 1.3), (3.0, ANCHOR, 1.0), (3.7, (RX, SY + 60), 1.3),
                                     (SW2 + 1.0, (RX, SY + 60), 1.3), (SW2 + 1.7, ANCHOR, 1.0)),
                  punch=0.04 * max(0, 1 - abs(t - SW2) / 0.12), seed=3)
    hud(cv)


TRY = [1.6, 2.6, 3.4]
def s3(cv, t, d, st):                                     # App C: invents its own gestures
    def world(c):
        c.font(SANS, 76, True); c.text(W / 2 - c.text_w("App C") / 2, 540, "App C", RED)
        nx = shorts_screen(c, W / 2, 1080, 460, 860, "AppC", RED, idx=4, layout="odd", t=t)
        st["next"] = nx
        swipe_hand(c, W / 2 + 60, 1300, 900, t, TRY[0], 0.5)
        for tp in TRY[1:]:
            if tp - 0.3 < t < tp + 0.3: c._dot(W / 2 - 40 + (tp - 2) * 120, 1040, 16, (1, 1, 1), 0.9)
        for i, tp in enumerate(TRY):
            if t > tp + 0.2:
                c.pill(W / 2 + 360, 760 + i * 90, ["swipe? ×", "double tap? ×", "like kahan?"][i], size=28, fam=MONO,
                       col=DARK, bg=RED, bold=True)
        if t > 4.2:
            for i in range(5):
                ang = -2.6 + i * 0.5
                c.pill(W / 2 + math.cos(ang) * 300, 1080 + math.sin(ang) * 380, "?", size=40, fam=MONO, col=RED)
        if t > 4.8: white_pill(c, W / 2, 1600, "user confuse → app delete", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.2, (W / 2, 1100), 1.35), (3.8, (W / 2, 1100), 1.35), (4.6, ANCHOR, 0.95)),
                  punch=0.05 * sum(max(0, 1 - abs(t - tp - 0.2) / 0.1) for tp in TRY), seed=4)
    hud(cv)
    for tp in TRY: flash(cv, t, tp + 0.2, 0.12)


def s4(cv, t, d, st):                                     # law: users spend most time in OTHER apps
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "JAKOB'S LAW", 112, W / 2, 640, ease(1 - t / 0.8), col=PURPLE)
        l1 = "users chahte hain aapka app"; l2 = "baaki apps jaisa kaam kare"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 760, DOT, 36, chars=n); mono(c, l2, 812, PURPLE, 36, chars=n - len(l1))
        cx, cy = W / 2, 1170                               # you in the middle, other apps orbit
        c.person(cx, cy - 20, 0.9)
        apps = [("Instagram", IGPINK), ("YouTube", YTRED), ("WhatsApp", GREEN), ("Amazon", ORANGE), ("Flipkart", BLUE),
                ("Swiggy", YELLOW)]
        k = ease((t - 2.2) / 1.2)
        for i, (nm, col) in enumerate(apps):
            ang = -1.57 + i / 6 * 6.283 + t * 0.15
            x, y = cx + math.cos(ang) * 340 * k, cy + math.sin(ang) * 230 * k
            if k > 0.05:
                c.dots_path([(cx, cy), (x, y)], spacing=14, r=1.6, col=col, a=0.6 * k)
                c.pill(x, y, nm, size=26, fam=SANS, col=DARK, bg=col, bold=True, a=k)
        if t > 3.6:
            c.pill(cx, cy + 330, "99% time → doosre apps", size=32, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t > 5.4:
            c.pill(cx, cy + 410, "1% time → aapka app", size=30, fam=MONO, col=PURPLE)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1000), 1.0), (3.4, (W / 2, 1000), 1.0),
                                     (4.0, (W / 2, 1400), 1.35), (6.2, (W / 2, 1400), 1.35), (6.9, (W / 2, 1000), 1.0)), seed=5)
    hud(cv); flash(cv, t, 3.6)


SWP, DTAP = 1.2, 3.4
CHECK = ["swipe up = next", "double tap = like", "actions right side"]
def s5(cv, t, d, st):                                     # YouTube Shorts copies the familiar pattern
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("YouTube Shorts") / 2, 540, "YouTube Shorts", YTRED)
        hx = shorts_screen(c, W / 2, 1080, 460, 860, "Shorts", YTRED, swipe=(t - SWP) / 0.7 if t > SWP else 0, idx=1,
                           liked=t >= DTAP, like_at=DTAP, t=t)
        st["heart"] = hx
        swipe_hand(c, W / 2 + 40, 1300, 880, t, SWP)
        if DTAP - 0.35 < t < DTAP + 0.2: c._dot(W / 2, 1040, 16, (1, 1, 1), 0.9)
        ring(c, W / 2, 1040, t, DTAP, YTRED)
        ring(c, *hx, t, 4.8, GREEN)
        for i, lab in enumerate(CHECK):
            on_t = [SWP + 0.8, DTAP + 0.3, 4.8][i]
            if t > on_t:
                c.pill(W / 2 + 330 * (1 if i % 2 == 0 else -1), 700 + i * 120, lab + " ✓", size=26, fam=SANS, col=DARK,
                       bg=GREEN, bold=True)
        if t > 5.6: white_pill(c, W / 2, 1590, "same as Reels = zero learning", 36)
    hp = st.get("heart", (W / 2 + 180, 1100))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (W / 2, 1080), 1.25), (2.4, (W / 2, 1080), 1.25),
                                     (3.0, (W / 2, 1040), 1.6), (4.2, (W / 2, 1040), 1.6), (4.6, hp, 1.9), (5.3, hp, 1.9),
                                     (5.9, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - DTAP) / 0.1), seed=6)
    hud(cv); flash(cv, t, DTAP, 0.12)


def mini_shop(c, cx, cy, cart_pos, ok, a=1.0):
    w, h = 300, 560
    x, y = phone(c, cx, cy, w, h, a=a)
    col = GREEN if ok else RED
    c.dbar(x + 40, y + 70, 120, rows=2, gap=6, a=a)
    c.drrect(x + 30, y + 110, w - 60, 40, 20, spacing=6, r=1.3, col=DIM, a=a)             # search bar
    for i in range(3): c.drrect(x + 30, y + 180 + i * 110, w - 60, 90, 14, spacing=6, r=1.3, col=DIM, a=a)
    px, py = (x + w - 50, y + 80) if cart_pos == "top" else (x + 60, y + h - 70)
    c.fill_rrect(px - 26, py - 22, 52, 44, 10, col, a)
    c.font(SANS, 18, True); c.text(px - 15, py + 7, "cart", DARK, a)
    return px, py


def s6(cv, t, d, st):                                     # designer tip: DON'T reinvent | DO follow conventions
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        p1 = mini_shop(c, W * 0.27, 1000, "bottom", False)
        if t > 1.0: c.pill(W * 0.27, 1340, "cart neeche-left?", size=26, fam=MONO, col=RED)
        p2 = mini_shop(c, W * 0.73, 1000, "top", True)
        ring(c, *p2, t, 3.4, GREEN)
        if t > 3.4: c.pill(W * 0.73, 1340, "cart upar-right ✓", size=26, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1460, "familiar pattern follow karo", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 960), 1.45), (2.4, (W * 0.27, 960), 1.45), (3.0, (W * 0.73, 960), 1.45),
                                     (4.6, (W * 0.73, 960), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे फोर।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, जेकब्स लॉ क्या है?", "", s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("रात को इंस्टाग्राम रील्स देख रहे थे, फिर यूट्यूब शॉर्ट्स खोला। किसी ने सिखाया नहीं, फिर भी अंगूठा अपने आप ऊपर स्वाइप करता है।",
          "", s2, min_dur=7.2, whoosh=True, sfx=[(SW1, "pop_lo"), (2.7, "pop_lo"), (SW2, "pop_lo"), (SW2 + 0.8, "ding")]),
    Scene("अब सोचो, एक नया ऐप जहाँ स्वाइप काम नहीं करता, और लाइक बटन मेन्यू में छुपा है। यूज़र कंफ्यूज़, और ऐप डिलीट।", "", s3,
          min_dur=6.6, whoosh=True, clicks=TRY[1:], sfx=[(tp + 0.2, "buzz") for tp in TRY] + [(4.8, "drop")]),
    Scene("यही है जेकब्स लॉ। यूज़र्स अपना ज़्यादातर टाइम दूसरे ऐप्स पर बिताते हैं। इसलिए वो चाहते हैं कि आपका ऐप भी वैसे ही काम करे।",
          "", s4, min_dur=8.0, whoosh=True, sfx=[(0.2, "ding"), (2.3, "riser"), (3.6, "pop_hi"), (5.4, "pop")]),
    Scene("इसीलिए यूट्यूब शॉर्ट्स बिल्कुल रील्स जैसा है। ऊपर स्वाइप, डबल टैप पे लाइक, और साइड में बटन्स। कुछ नया सीखना ही नहीं पड़ता।",
          "", s5, min_dur=7.4, whoosh=True, clicks=[DTAP, 4.8],
          sfx=[(SWP, "pop_lo"), (SWP + 0.8, "pop"), (DTAP + 0.02, "pop_hi"), (DTAP + 0.3, "pop"), (4.82, "chime")]),
    Scene("डिज़ाइनर टिप। हर चीज़ नई मत बनाओ। कार्ट ऊपर राइट, सर्च ऊपर, और जाने पहचाने पैटर्न्स फॉलो करो।", "", s6, min_dur=6.6,
          whoosh=True, sfx=[(0.3, "buzz"), (3.4, "chime"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 04 voice-over (Tisha K master, supplied by Rakhi) has no long pauses, so it is split at measured cut times.
VO_CUTS = [8.28, 12.40, 20.71, 28.51, 35.89, 44.87, 52.73]

if __name__ == "__main__":
    import daily
    daily.run(4, "Jakob's Law", SCENES, "day04_jakobs_law", cuts=VO_CUTS)

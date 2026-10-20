"""Day 07/45 · Goal-Gradient Effect, explained with Blinkit's "add ₹30 more for FREE delivery" cart bar.

The closer a goal looks, the faster we work to finish it, so a nearly-full progress bar makes us add one more item.
Day 02 pattern. Voice: Rakhi's Day 07 ElevenLabs Tisha K file (uploaded as day62.mp3) at assets/voice/day07/full.mp3,
script in docs/scripts/day07.md; see docs/voice_workflow.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 7, "Peak-End Rule"
W, H = 1080, 1920
BYELLOW = (0.98, 0.80, 0.15)                      # Blinkit yellow
BGREEN = (0.20, 0.78, 0.38)                       # Blinkit green (brightened)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
GOAL = 200


def item_row(c, y, name, price, col, a=1.0):
    c.drrect(X0 + 30, y, 70, 70, 14, spacing=5, r=1.5, col=col, a=a)
    c._dot(X0 + 65, y + 35, 12, col, 0.8 * a)
    c.font(SANS, 24, True); c.text(X0 + 120, y + 30, name, DOT, a)
    c.font(SANS, 20); c.text(X0 + 120, y + 58, "1 unit", DIM, a)
    c.font(SANS, 24, True); s = f"₹{price}"; c.text(X0 + PW - 40 - c.text_w(s), y + 44, s, DOT, a)


def free_bar(c, total, t, y=None, a=1.0):
    """Blinkit-style free-delivery strip. Returns its centre."""
    y = y if y is not None else Y0 + 470
    x, w = X0 + 26, PW - 52
    done = total >= GOAL
    c.fill_rrect(x, y, w, 120, 16, (0.10, 0.16, 0.11) if done else (0.17, 0.15, 0.08), a)
    c.font(SANS, 22, True)
    msg = "FREE delivery unlocked ✓" if done else f"Add ₹{GOAL - total} more for FREE delivery"
    c.text(x + 20, y + 40, msg, BGREEN if done else BYELLOW, a)
    k = min(1, total / GOAL)
    c.fill_rrect(x + 20, y + 66, w - 40, 18, 9, (0.25, 0.25, 0.28), a)
    c.fill_rrect(x + 20, y + 66, max(18, (w - 40) * k), 18, 9, BGREEN if done else BYELLOW, a)
    c.font(MONO, 18, True); s = f"₹{total} / ₹{GOAL}"; c.text(x + w - 20 - c.text_w(s), y + 104, s, DIM, a)
    return (PX, y + 55)


def cart(c, items, t, a=1.0):
    phone(c, PX, PY, PW, PH, a=a)
    c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 90, "blinkit", BYELLOW, a)
    c.font(SANS, 22, True); c.text(X0 + PW - 140, Y0 + 90, "My Cart", DOT, a)
    for i, (n, p, col) in enumerate(items): item_row(c, Y0 + 130 + i * 90, n, p, col, a)
    total = sum(p for _, p, _ in items)
    pos = free_bar(c, total, t, y=Y0 + 150 + len(items) * 90, a=a)
    return total, pos


# ------------------------------------------------------------------ scenes
def runner(c, x, y, s, col, t):
    c.dellipse(x, y - 60 * s, 14 * s, 14 * s, spacing=4, r=1.8, col=col)
    leg = math.sin(t * 14) * 18 * s
    c.dots_path([(x, y - 46 * s), (x, y - 5 * s)], spacing=5, r=2, col=col)
    c.dots_path([(x, y - 5 * s), (x + leg, y + 30 * s)], spacing=5, r=2, col=col)
    c.dots_path([(x, y - 5 * s), (x - leg, y + 30 * s)], spacing=5, r=2, col=col)
    c.dots_path([(x - leg * 0.8, y - 40 * s), (x, y - 32 * s), (x + leg * 0.8, y - 22 * s)], spacing=5, r=2, col=col)


def s1(cv, t, d, st):                                     # hook: manzil paas = speed zyada
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "GOAL-GRADIENT", 100, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=BGREEN)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "EFFECT kya hai?", 980, DOT, 52, chars=int((t - 2.0) * 14))
        if t > 3.0:                                          # a runner speeds up as the finish line nears
            x0, x1, y = 170, 900, 1240
            c.dline(x0, y + 34, x1, y + 34, spacing=10, r=1.6, col=DIM)
            for i in range(6): c.fill_rrect(x1 + 6, y - 60 + i * 16, 12, 16, 2, (1, 1, 1) if i % 2 == 0 else DARK)
            u = min(1, (t - 3.0) / 2.2); p = u ** 2.2                # accelerating
            rx = lerp(x0, x1 - 20, p)
            for k in range(1, 5): c._dot(rx - k * 22 * (0.3 + p), y - 10, 4, BGREEN, 0.5 - k * 0.1)
            runner(c, rx, y, 1.3, BGREEN, t * (1 + 2 * p))
            c.pill(W / 2, 1360, "manzil paas = speed zyada", size=30, fam=MONO, col=BGREEN)
        if t > 5.4: c.pill(W / 2, 1470, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=BYELLOW, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 950), 1.0),
                                     (3.0, (W / 2, 1150), 1.0), (5.2, (W / 2, 1150), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


BASE = [("Milk", 70, (0.85, 0.9, 1.0)), ("Bread", 100, ORANGE)]
def s2(cv, t, d, st):                                     # cart: milk + bread, ₹30 away from free delivery
    def world(c):
        items = BASE[:1 + (t > 1.0)]
        total, pos = cart(c, items, t)
        st["bar"] = pos
        if t > 2.2:
            p = 1 + 0.06 * math.sin(t * 8)
            c.pill(PX + 330, pos[1], "sirf ₹30 aur!", size=int(32 * p), fam=MONO, col=DARK, bg=BYELLOW, bold=True)
            bx, by = pos
            c.rrect_path(X0 + 46 + (PW - 92) * 0.85, by + 7, (PW - 92) * 0.15, 26, 13)
            c.c.set_source_rgba(*BYELLOW, 0.4 + 0.4 * abs(math.sin(t * 4))); c.c.set_line_width(3); c.c.stroke()
    b = st.get("bar", (PX, Y0 + 385))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.6, ANCHOR, 1.0), (2.2, b, 1.7), (d - 0.4, b, 1.7)), seed=3)
    hud(cv)


TAP = 1.0
def s3(cv, t, d, st):                                     # + chips -> bar full, free delivery unlocked
    def world(c):
        items = BASE + ([("Chips", 30, YELLOW)] if t >= TAP + 0.2 else [])
        total, pos = cart(c, items, t)
        st["bar"] = pos
        bx, by = PX + 330, Y0 + 260
        if t < TAP + 0.3:                                    # "+ chips" suggestion button
            c.fill_rrect(bx - 90, by - 34, 180, 68, 34, BGREEN)
            c.font(SANS, 26, True); c.text(bx - 60, by + 10, "+ Chips", DARK)
            ring(c, bx, by, t, TAP, BGREEN)
            if TAP - 0.4 < t < TAP + 0.2: c._dot(bx + 8, by + 10, 16, (1, 1, 1), 0.9)
        if t > TAP + 0.4:
            px, py = pos
            for i in range(30):
                ang = i / 30 * 6.283; dd = 40 + 260 * ease((t - TAP - 0.4) / 1.2)
                c._dot(px + math.cos(ang) * dd, py + math.sin(ang) * dd * 0.6, 5, COLS[i % 6], max(0, 1 - (t - TAP - 0.4) / 1.2))
        if t > TAP + 1.4: white_pill(c, W / 2, 1640, "bar full · delivery FREE", 36)
    b = st.get("bar", (PX, Y0 + 475))
    stage.compose(cv, t, d, world, K((0, (PX + 200, Y0 + 300), 1.3), (TAP + 0.3, (PX + 200, Y0 + 300), 1.3),
                                     (TAP + 0.6, b, 1.6), (TAP + 2.0, b, 1.6), (TAP + 2.6, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - TAP - 0.4) / 0.12), seed=4)
    hud(cv); flash(cv, t, TAP + 0.4, 0.12)


def s4(cv, t, d, st):                                     # law card: effort curve rises steeply near the goal
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "GOAL-GRADIENT", 96, W / 2, 630, ease(1 - t / 0.8), col=BGREEN)
        l1 = "goal jitna kareeb,"; l2 = "utni tezi se poora karte hain"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 36, chars=n); mono(c, l2, 800, BGREEN, 36, chars=n - len(l1))
        gx, gy, gw, gh = 190, 880, 720, 440
        c.dline(gx, gy + gh, gx + gw, gy + gh, spacing=9, r=1.8, col=DIM); c.dline(gx, gy, gx, gy + gh, spacing=9, r=1.8, col=DIM)
        c.font(MONO, 24); c.text(gx + gw - 210, gy + gh + 44, "goal ke paas →", DIM); c.text(gx - 30, gy - 20, "speed ↑", DIM)
        k = ease((t - 2.0) / 2.6); m = int(k * 60)
        pts = [(gx + i / 60 * gw, gy + gh - (i / 60) ** 3 * gh * 0.92) for i in range(61)]
        for i in range(m + 1):
            x, y = pts[i]; c._dot(x, y, 6, DIM if i < 25 else (YELLOW if i < 45 else BGREEN), 1)
        if m > 0: c.glow(*pts[m], 50, 0.9)
        if k > 0.98:
            c.fill_rrect(gx + gw - 10, gy - 10, 16, 60, 3, (1, 1, 1))
            c.pill(gx + gw - 140, gy + 40, "GOAL!", size=30, fam=MONO, col=DARK, bg=BGREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1000), 1.0), (4.4, (W / 2, 1000), 1.0),
                                     (5.0, (780, 960), 1.3), (d - 0.6, (780, 960), 1.3)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # Blinkit: the bar itself, "₹170 / ₹200 · ₹30 baaki"
    def world(c):
        c.font(SANS, 64, True); c.text(W / 2 - c.text_w("blinkit") / 2, 540, "blinkit", BYELLOW)
        total, pos = cart(c, BASE, t)
        st["bar"] = pos
        if t > 1.0: c.pill(PX + 330, pos[1] - 40, "kitna hua", size=26, fam=MONO, col=DARK, bg=BYELLOW, bold=True)
        if t > 1.8: c.pill(PX + 330, pos[1] + 40, "kitna baaki", size=26, fam=MONO, col=DARK, bg=BGREEN, bold=True)
        if t > 3.4: white_pill(c, W / 2, 1640, "progress dikhta hai = log poora karte hain", 32)
    b = st.get("bar", (PX, Y0 + 385))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, b, 1.8), (3.0, b, 1.8), (3.6, ANCHOR, 1.0)), seed=6)
    hud(cv)


def stamp_card(c, cx, cy, n, filled, col, a=1.0, given=0):
    c.fill_rrect(cx - 190, cy - 120, 380, 240, 22, (0.11, 0.11, 0.13), a)
    c.rrect_path(cx - 190, cy - 120, 380, 240, 22); c.c.set_source_rgba(*col, a); c.c.set_line_width(2); c.c.stroke()
    per = 5 if n == 10 else 6
    for i in range(n):
        x = cx - 150 + (i % per) * (300 / (per - 1)); y = cy - 50 + (i // per) * 80
        on = i < filled
        if on: c.c.set_source_rgba(*(BYELLOW if i < given else col), a); c.c.arc(x, y, 20, 0, 6.3); c.c.fill()
        c.dellipse(x, y, 22, 22, spacing=5, r=1.4, col=col if on else DIM, a=a)


def s6(cv, t, d, st):                                     # designer tip: DON'T empty 0/10 | DO 2/12 with a head start
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        stamp_card(c, W * 0.27, 900, 10, 0, RED if t < 2.8 else DIM)
        c.pill(W * 0.27, 1080, "0 / 10 · shuru kahan se?", size=26, fam=MONO, col=RED)
        g = 2 if t > 3.2 else 0
        stamp_card(c, W * 0.73, 900, 12, g, GREEN, given=2)
        if t > 3.2: c.pill(W * 0.73, 1080, "2 / 12 · head start!", size=26, fam=MONO, col=DARK, bg=BYELLOW, bold=True)
        if t > 4.8: white_pill(c, W / 2, 1260, "pehla step already done", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration (Hinglish): the approved Day 07 script (docs/scripts/day07.md). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे सेवन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, गोल ग्रेडिएंट इफ़ेक्ट क्या है? मंज़िल जितनी पास, स्पीड उतनी ज़्यादा। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.2, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (3.0, "riser"), (5.2, "ding"), (5.4, "pop_hi")]),
    Scene("ब्लिंकिट पे दूध और ब्रेड लिया। कार्ट में दिखा, सिर्फ थर्टी रुपीज़ और, और डिलीवरी फ्री।", "", s2,
          min_dur=5.4, whoosh=True, sfx=[(0.2, "pop"), (1.0, "pop"), (2.2, "pop_hi")]),
    Scene("और हम तुरंत चिप्स उठा लेते हैं। बार फुल, फ्री डिलीवरी अनलॉक।", "", s3,
          min_dur=4.8, whoosh=True, clicks=[TAP], sfx=[(TAP + 0.02, "pop"), (TAP + 0.4, "chime"), (TAP + 1.4, "ding")]),
    Scene("यही है गोल ग्रेडिएंट इफ़ेक्ट। गोल जितना करीब दिखता है, हम उतनी तेज़ी से उसे पूरा करते हैं।", "", s4,
          min_dur=7.0, whoosh=True, sfx=[(0.2, "ding"), (2.0, "riser"), (4.6, "pop_hi")]),
    Scene("इसीलिए ब्लिंकिट कार्ट में प्रोग्रेस बार दिखाता है, कि फ्री डिलीवरी के लिए कितना बाकी है।", "", s5,
          min_dur=5.6, whoosh=True, sfx=[(1.0, "pop"), (1.8, "pop"), (3.4, "ding")]),
    Scene("डिज़ाइनर टिप। गोल का प्रोग्रेस दिखाओ, और शुरू में थोड़ा हेड स्टार्ट दो, जैसे पहला स्टेप ऑलरेडी डन।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.2, "pop"), (3.4, "pop_hi"), (4.8, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# full.mp3 = day62.mp3 (Day 07 take 2) has only 2 long pauses: line cuts mapped by alignment from take 1
# (take1_day6.mp3, uploaded as day6.mp3, same script with clean pauses), each snapped to the quietest point (all silent).
VO_CUTS = [4.08, 13.24, 20.04, 25.12, 32.0, 37.94, 46.28]

if __name__ == "__main__":
    import daily
    daily.run(7, "Goal-Gradient Effect", SCENES, "day07_goal_gradient", cuts=VO_CUTS)

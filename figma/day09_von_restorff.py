"""Day 09/45 · Von Restorff Effect, explained with Netflix's plan picker and its highlighted "Most Popular" plan.

Among similar items, the one that stands out is noticed first and remembered, so one highlighted plan guides the choice.
Day 02 pattern. Voice: Rakhi's Day 09 ElevenLabs Tisha K file at assets/voice/day09/full.mp3 (content-verified);
script in docs/scripts/day09.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 9, "Serial Position Effect"
W, H = 1080, 1920
NRED = (1.0, 0.22, 0.24)                          # Netflix red (brightened)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
PLANS = [("Mobile", "₹149"), ("Basic", "₹199"), ("Standard", "₹499"), ("Premium", "₹649")]
HI = 2                                             # the highlighted plan


def plan_card(c, x, y, w, h, name, price, hi_k=0.0, lift=0.0, a=1.0, every=False):
    y -= lift
    col = NRED if (hi_k > 0 or every) else GREY
    if hi_k > 0 or every:
        c.fill_rrect(x, y, w, h, 18, tuple(0.13 + (cc - 0.13) * 0.35 * (hi_k if not every else 1) for cc in NRED), a)
    else:
        c.fill_rrect(x, y, w, h, 18, (0.12, 0.12, 0.14), a)
    c.rrect_path(x, y, w, h, 18); c.c.set_source_rgba(*col, a); c.c.set_line_width(3 if hi_k > 0 or every else 1.5); c.c.stroke()
    c.font(SANS, 26, True); c.text(x + 22, y + 44, name, DOT, a)
    c.font(SANS, 30, True); c.text(x + w - 22 - c.text_w(price), y + 46, price, (1, 1, 1) if hi_k > 0 or every else DOT, a)
    for i in range(2): c.dbar(x + 22, y + 70 + i * 26, w * (0.55 - 0.12 * i), rows=1, gap=5, col=DIM, a=a)
    if hi_k > 0.3 or every:
        bw = 190
        c.fill_rrect(x + w / 2 - bw / 2, y - 22, bw, 40, 20, NRED, a)
        c.font(SANS, 18, True); s = "MOST POPULAR"; c.text(x + w / 2 - c.text_w(s) / 2, y + 5, s, (1, 1, 1), a)
    return (x + w / 2, y + h / 2)


def plans_screen(c, t, hi_k=0.0, every=False, a=1.0):
    phone(c, PX, PY, PW, PH, a=a)
    c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 90, "N", NRED, a)
    c.font(SANS, 26, True); c.text(X0 + 30, Y0 + 150, "Choose your plan", DOT, a)
    pos = []
    for i, (n, p) in enumerate(PLANS):
        hk = hi_k if i == HI else 0.0
        pos.append(plan_card(c, X0 + 30, Y0 + 210 + i * 160, PW - 60, 128, n, p, hk, lift=14 * hk, a=a, every=every))
    return pos


def brain(c, cx, cy, s=1.0, col=DOT, a=1.0):
    c.dellipse(cx - 40 * s, cy, 90 * s, 80 * s, spacing=7, r=2, col=col, a=a)
    c.dellipse(cx + 40 * s, cy, 90 * s, 80 * s, spacing=7, r=2, col=col, a=a)
    c.dots_path([(cx, cy - 75 * s), (cx, cy + 70 * s)], spacing=8, r=1.6, col=col, a=a * 0.7)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: jo alag, wahi yaad
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "VON RESTORFF", 104, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=NRED)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "EFFECT kya hai?", 980, DOT, 52, chars=int((t - 2.0) * 14))
        if t > 3.0:                                          # grid of grey dots, one red one pulses
            for r in range(4):
                for q in range(9):
                    x, y = 220 + q * 80, 1100 + r * 70
                    odd = (r, q) == (2, 6)
                    if odd:
                        p = 1 + 0.25 * abs(math.sin(t * 4)); c._dot(x, y, 16 * p, NRED, 1); c.glow(x, y, 50, 0.6)
                    else: c._dot(x, y, 12, GREY, 0.9)
            c.pill(W / 2, 1420, "jo alag, wahi yaad", size=30, fam=MONO, col=NRED)
        if t > 5.4: c.pill(W / 2, 1520, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=NRED, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1150), 1.0), (4.0, (700, 1240), 1.35), (5.2, (W / 2, 1200), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


def s2(cv, t, d, st):                                     # 4 plans, all identical grey cards
    def world(c):
        pos = plans_screen(c, t)
        st["pos"] = pos
        if t > 1.4:
            for i, p in enumerate(pos):
                if t > 1.4 + i * 0.25: c.pill(PX + 330, p[1], "same", size=24, fam=MONO, col=DIM)
        if t > 2.8:
            for i in range(5):                               # eye wanders, confused
                ang = -2.6 + i * 0.5
                c.pill(PX + math.cos(ang) * 320, Y0 + 520 + math.sin(ang) * 420, "?", size=34, fam=MONO, col=GREY)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.2, (PX, Y0 + 450), 1.15), (d - 0.4, (PX, Y0 + 450), 1.15)), seed=3)
    hud(cv)


POP = 0.6
def s3(cv, t, d, st):                                     # one card turns red + MOST POPULAR; the eye jumps there
    def world(c):
        k = ease(min(1, max(0, (t - POP) / 0.6)))
        pos = plans_screen(c, t, hi_k=k)
        st["hi"] = pos[HI]
        if t > POP + 0.8:                                    # eye-focus ring flies from the top to the highlighted card
            u = ease(min(1, (t - POP - 0.8) / 0.6))
            ex, ey = lerp(PX, pos[HI][0], u), lerp(Y0 + 120, pos[HI][1], u)
            c.dellipse(ex, ey, 70, 46, spacing=6, r=2.4, col=YELLOW)
            c._dot(ex, ey, 10, YELLOW, 1)
        if t > POP + 1.6: c.pill(PX + 330, pos[HI][1], "nazar yahin!", size=30, fam=MONO, col=DARK, bg=YELLOW, bold=True)
    hp = st.get("hi", (PX, Y0 + 594))
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + 450), 1.15), (POP + 0.6, (PX, Y0 + 450), 1.15), (POP + 1.4, hp, 1.6),
                                     (d - 0.4, hp, 1.6)), punch=0.05 * max(0, 1 - abs(t - POP - 0.6) / 0.12), seed=4)
    hud(cv); flash(cv, t, POP + 0.6, 0.12)


def s4(cv, t, d, st):                                     # law card: one different circle stays in memory
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "VON RESTORFF", 100, W / 2, 630, ease(1 - t / 0.8), col=NRED)
        l1 = "bheed mein jo alag dikhe,"; l2 = "wahi notice + yaad hota hai"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 36, chars=n); mono(c, l2, 800, NRED, 36, chars=n - len(l1))
        fade = ease(min(1, max(0, (t - 3.6) / 1.4)))
        for i in range(7):
            x = 180 + i * 120; odd = i == 4
            if odd:
                c.c.set_source_rgba(*NRED, 1); c.c.arc(x, 1060, 46, 0, 6.3); c.c.fill(); c.glow(x, 1060, 80, 0.7)
            else:
                c.dellipse(x, 1060, 44, 44, spacing=6, r=2, col=GREY, a=1 - 0.8 * fade)
        brain(c, W / 2, 1300, 0.9, col=DOT)
        if t > 3.8: c._dot(W / 2 + 20, 1300, 18, NRED, 1); c.pill(W / 2, 1450, "baaki bhool gaye", size=28, fam=MONO, col=DIM)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1050), 1.0), (d - 0.4, (W / 2, 1100), 1.05)), seed=5)
    hud(cv)


TAP = 2.2
def s5(cv, t, d, st):                                     # Netflix highlights one plan -> easy decision
    def world(c):
        c.font(SANS, 64, True); c.text(W / 2 - c.text_w("NETFLIX") / 2, 540, "NETFLIX", NRED)
        pos = plans_screen(c, t, hi_k=1.0)
        st["hi"] = pos[HI]
        ring(c, *pos[HI], t, TAP, NRED)
        if TAP - 0.4 < t < TAP + 0.2: c._dot(pos[HI][0] + 10, pos[HI][1] + 12, 16, (1, 1, 1), 0.9)
        if t > TAP + 0.2: c.pill(PX + 330, pos[HI][1], "selected ✓", size=28, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > TAP + 1.2: white_pill(c, W / 2, 1640, "decision aasaan", 36)
    hp = st.get("hi", (PX, Y0 + 594))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.0, hp, 1.5), (TAP + 1.0, hp, 1.5), (TAP + 1.6, ANCHOR, 1.0)),
                  punch=0.04 * max(0, 1 - abs(t - TAP) / 0.1), seed=6)
    hud(cv)


def mini_plans(c, cx, top, every):
    for i in range(4):
        x, y, w, h = cx - 160, top + i * 110, 320, 86
        on = every or i == HI
        c.fill_rrect(x, y, w, h, 14, (0.28, 0.08, 0.09) if on else (0.12, 0.12, 0.14))
        c.rrect_path(x, y, w, h, 14); c.c.set_source_rgba(*(NRED if on else GREY), 1); c.c.set_line_width(2.5 if on else 1.2); c.c.stroke()
        c.dbar(x + 18, y + 30, 160, rows=2, gap=6, col=DOT if on else DIM)
        if on: c.fill_rrect(x + w - 112, y - 12, 100, 26, 13, NRED); c.font(SANS, 13, True); c.text(x + w - 104, y + 6, "POPULAR", (1, 1, 1))


def s6(cv, t, d, st):                                     # designer tip: DON'T highlight everything | DO highlight one
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        mini_plans(c, W * 0.27, 680, every=True)
        c.pill(W * 0.27, 1160, "sab highlight = kuch nahi", size=24, fam=MONO, col=RED)
        mini_plans(c, W * 0.73, 680, every=False)
        c.pill(W * 0.73, 1160, "sirf ek highlight ✓", size=26, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "sirf ek cheez ko highlight karo", 34)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration (Hinglish): the approved Day 09 script (docs/scripts/day09.md). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे नाइन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, वॉन रेस्टॉर्फ इफ़ेक्ट क्या है? जो चीज़ सबसे अलग दिखती है, वही याद रहती है। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.4, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (3.0, "pop_hi"), (5.4, "pop_hi")]),
    Scene("नेटफ्लिक्स का प्लान चुनना है। चार प्लान्स, सब एक जैसे कार्ड्स।", "", s2,
          min_dur=4.6, whoosh=True, sfx=[(1.4 + i * 0.25, "tick") for i in range(4)] + [(2.8, "buzz")]),
    Scene("पर एक कार्ड अलग है, रंग भरा, और ऊपर लिखा, मोस्ट पॉपुलर। नज़र सीधा वहीं जाती है।", "", s3,
          min_dur=5.6, whoosh=True, sfx=[(POP + 0.6, "chime"), (POP + 0.8, "riser"), (POP + 1.6, "pop_hi")]),
    Scene("यही है वॉन रेस्टॉर्फ इफ़ेक्ट। भीड़ में जो अलग दिखे, दिमाग उसे सबसे पहले नोटिस करता है, और याद रखता है।", "", s4,
          min_dur=6.6, whoosh=True, sfx=[(0.2, "ding"), (3.6, "pop_lo"), (3.8, "pop_hi")]),
    Scene("इसीलिए नेटफ्लिक्स एक प्लान को हाइलाइट करता है, ताकि आपका डिसीज़न आसान हो जाए।", "", s5,
          min_dur=5.6, whoosh=True, clicks=[TAP], sfx=[(TAP + 0.02, "pop_hi"), (TAP + 0.2, "chime")]),
    Scene("डिज़ाइनर टिप। सिर्फ एक चीज़ को हाइलाइट करो। अगर सब कुछ हाइलाइट होगा, तो कुछ भी अलग नहीं दिखेगा।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# day9.mp3 has only 2 long pauses: line cuts found by aligning it to a TTS reading of the script, each snapped to the
# quietest point within 0.8 s (all silent); line check 8/8.
VO_CUTS = [4.3, 14.18, 18.98, 26.04, 33.54, 39.08, 45.98]

if __name__ == "__main__":
    import daily
    daily.run(9, "Von Restorff Effect", SCENES, "day09_von_restorff", cuts=VO_CUTS)

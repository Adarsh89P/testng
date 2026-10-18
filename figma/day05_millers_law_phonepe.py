"""Day 05/45 · Miller's Law (chunking), explained with PhonePe's OTP boxes and 4-4-4-4 card number input.

We hold roughly 7±2 items in working memory, so long information is easier when it is broken into chunks:
98765 43210 instead of 9876543210. Day 02 pattern. Voice: a NEW Day 05 voice-over (offline --generate in the reference voice, or Rakhi's own
recording) at assets/voice/day05/full.*; see docs/voice_workflow.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 5, "Zeigarnik Effect"
W, H = 1080, 1920
PPURPLE = (0.55, 0.36, 0.95)                     # PhonePe purple (brightened for the black background)
TEAL = (0.25, 0.85, 0.85)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
NUM = "9876543210"


def digits(c, s, cx, y, size, col=DOT, gap_after=(), spacing=1.0, jitter=0.0, t=0.0, a=1.0, cols=None):
    """Draw a digit string centred at cx; extra space after the indices in gap_after (chunking)."""
    c.font(MONO, size, True); cw = c.text_w("0") * spacing; gw = cw * 0.9
    tot = cw * len(s) + gw * len(gap_after); x = cx - tot / 2
    pos = []
    for i, ch in enumerate(s):
        jx = math.sin(t * 5 + i * 1.7) * jitter; jy = math.cos(t * 4 + i * 2.3) * jitter
        col_i = cols[i] if cols else col
        c.text(x + jx, y + jy, ch, col_i, a); pos.append((x + cw / 2, y - size * 0.35))
        x += cw + (gw if i in gap_after else 0)
    return pos


def brain(c, cx, cy, s=1.0, col=DOT, a=1.0):
    c.dellipse(cx - 40 * s, cy, 90 * s, 80 * s, spacing=7, r=2, col=col, a=a)
    c.dellipse(cx + 40 * s, cy, 90 * s, 80 * s, spacing=7, r=2, col=col, a=a)
    c.dots_path([(cx, cy - 75 * s), (cx, cy + 70 * s)], spacing=8, r=1.6, col=col, a=a * 0.7)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # question hook
    def world(c):
        mono(c, "UX designer ho?", 720, DOT, 62, chars=int(t * 14))
        if t > 1.3:
            dot_text(c, "MILLER'S LAW", 112, W / 2, 900, ease(1 - (t - 1.3) / 0.8), col=TEAL)
            c.glow(W / 2, 900, 400, 0.08)
        if t > 2.5: mono(c, "kya hai?", 1060, DOT, 62, chars=int((t - 2.5) * 14))
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 900 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.35), (1.3, (W / 2, 900), 1.35), (2.2, (W / 2, 900), 1.0)), seed=2)
    hud(cv); flash(cv, t, 1.3)


def s2(cv, t, d, st):                                     # story: one long number, brain overloaded
    n = min(len(NUM), int(max(0, t - 0.6) * 9))
    def world(c):
        mono(c, "dost ne number bola...", 690, (0.85, 0.85, 0.88), 40)
        c.person(W / 2 - 300, 860, 0.8)
        c.pill(W / 2 - 300, 960, "dost", size=26)
        if t > 0.4:
            c.dots_path([(W / 2 - 220, 800), (W / 2 + 160, 780)], spacing=12, r=2.4, col=DIM, reveal=min(1, (t - 0.4) / 0.6))
        digits(c, NUM[:n], W / 2, 1140, 96, col=DOT if t < 3.2 else RED, jitter=0 if t < 3.2 else 10 * min(1, t - 3.2), t=t)
        brain(c, W / 2 + 280, 820, 0.8, col=RED if t > 3.2 else DOT)
        if t > 3.2:
            for i in range(14):                               # digits leak out of memory
                k = ((t - 3.2) * 0.6 + i / 14) % 1
                c.font(MONO, 34, True)
                c.text(W / 2 + 280 + math.sin(i * 2.1) * 120 * k, 900 + 600 * k * k, NUM[i % 10], RED, max(0, 1 - k))
        if t > 4.2: white_pill(c, W / 2, 1420, "10 digits ek saath = bhool gaye", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.2), (1.0, (W / 2, 1100), 1.25), (3.0, (W / 2, 1100), 1.25),
                                     (3.4, (W / 2 + 200, 950), 1.5), (4.6, (W / 2 + 200, 950), 1.5), (5.3, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - 3.2) / 0.12), seed=3)
    hud(cv); flash(cv, t, 3.2, 0.12)


SPLIT = 1.4
def s3(cv, t, d, st):                                     # chunked: 98765 43210
    def world(c):
        k = ease((t - SPLIT) / 0.6)
        c.font(MONO, 110, True); cw = c.text_w("0")
        cols = [GREEN] * 5 + [BLUE] * 5 if t > SPLIT else None
        digits(c, NUM, W / 2, 1000, 110, col=DOT, gap_after=(4,) if k > 0 else (), spacing=1.0, cols=cols)
        if k > 0:
            x0 = W / 2 - (cw * 10 + cw * 0.9) / 2
            for j, (a, b, col) in enumerate([(0, 5, GREEN), (5, 10, BLUE)]):
                xa = x0 + a * cw + (cw * 0.9 if j else 0) - 10; xb = xa + 5 * cw + 20
                c.drrect(xa, 880, (xb - xa), 160, 26, spacing=7, r=2, col=col, a=k)
                c.pill((xa + xb) / 2, 1100, f"chunk {j + 1}", size=26, fam=MONO, col=col, a=k)
        if t > 2.6:
            brain(c, W / 2, 1320, 0.8, col=GREEN)
            for i in range(2): c._dot(W / 2 - 40 + i * 80, 1320, 16, [GREEN, BLUE][i], 1)
        if t > 3.4: white_pill(c, W / 2, 1520, "2 chunks = aasaani se yaad", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 980), 1.4), (2.2, (W / 2, 980), 1.4), (3.0, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - SPLIT) / 0.1), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law: 7 ± 2 memory slots
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "MILLER'S LAW", 106, W / 2, 640, ease(1 - t / 0.8), col=TEAL)
        l1 = "dimaag ek baar mein ~7 cheezein"; l2 = "hi yaad rakh paata hai"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 760, DOT, 36, chars=n); mono(c, l2, 812, TEAL, 36, chars=n - len(l1))
        brain(c, W / 2, 1060, 1.4)
        nin = min(12, int(max(0, t - 2.2) * 4))
        for i in range(nin):                               # items fly in; beyond 7 they fall out
            if i < 7:
                ang = -2.6 + i * 0.36
                x, y = W / 2 + math.cos(ang) * 120, 1060 + math.sin(ang) * 90 + 70
                c._dot(x, y, 16, COLS[i % 6], 1)
            else:
                k = min(1, (t - 2.2 - i / 4) * 0.8)
                c._dot(W / 2 + 260 + (i - 7) * 40, 1000 + 500 * k * k, 14, RED, max(0, 1 - k))
        if t > 3.0: c.pill(W / 2, 1260, f"{min(nin, 7)} / 7 slots", size=32, fam=MONO, col=DARK, bg=GREEN if nin <= 7 else YELLOW, bold=True)
        if t > 5.4: c.pill(W / 2, 1360, "7 ± 2", size=56, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t > 6.4: c.pill(W / 2, 1460, "isliye info ko chunks mein todo", size=30, fam=MONO, col=TEAL)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1000), 1.0), (5.0, (W / 2, 1000), 1.0),
                                     (5.6, (W / 2, 1300), 1.4), (d - 0.9, (W / 2, 1300), 1.4), (d - 0.3, (W / 2, 1000), 1.0)), seed=5)
    hud(cv)


PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
OTP = "482913"
CARD = "4111222233334444"
def s5(cv, t, d, st):                                     # PhonePe: 6 OTP boxes, then 4-4-4-4 card number
    otp_n = min(6, int(max(0, t - 1.0) * 5))
    card_n = min(16, int(max(0, t - 4.0) * 9))
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("PhonePe") / 2, 540, "PhonePe", PPURPLE)
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 90, "PhonePe", PPURPLE)
        c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 170, "Enter OTP", DOT)
        bw, gap = 58, 12; bx0 = PX - (6 * bw + 5 * gap) / 2
        for i in range(6):                                 # one digit per box
            x = bx0 + i * (bw + gap); on = i < otp_n
            c.drrect(x, Y0 + 200, bw, 74, 12, spacing=5, r=1.6, col=PPURPLE if on or i == otp_n else DIM)
            if on: c.font(MONO, 38, True); c.text(x + bw / 2 - c.text_w(OTP[i]) / 2, Y0 + 252, OTP[i], DOT)
        st["otp"] = (PX, Y0 + 237)
        c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 390, "Card number", DOT)
        c.drrect(X0 + 26, Y0 + 420, PW - 52, 84, 14, spacing=6, r=1.6, col=PPURPLE if t > 4.0 else DIM)
        s = CARD[:card_n]
        grouped = " ".join(s[i:i + 4] for i in range(0, len(s), 4))
        c.font(MONO, 34, True); c.text(X0 + 50, Y0 + 474, grouped, DOT)
        st["card"] = (PX, Y0 + 462)
        for i in range(4): c.dbar(X0 + 30, Y0 + 570 + i * 50, (PW - 60) * (0.8 - 0.1 * (i % 2)), rows=2, gap=6, col=DIM)
        if t > 2.4: c.pill(PX + 340, Y0 + 237, "6 boxes", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > 6.0: c.pill(PX + 340, Y0 + 462, "4-4-4-4", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > 6.8: white_pill(c, W / 2, 1620, "lambi info, chhote chunks", 36)
    o, cd = st.get("otp", (PX, 780)), st.get("card", (PX, 1080))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, o, 1.6), (3.0, o, 1.6), (3.8, cd, 1.6), (6.4, cd, 1.6),
                                     (7.0, ANCHOR, 1.0)),
                  punch=0.04 * max(0, 1 - abs(t - 2.2) / 0.1), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T one long form | DO grouped steps
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx = W * 0.27                                       # 14 fields in one go
        for i in range(14):
            c.drrect(lx - 170, 640 + i * 50, 340, 36, 8, spacing=5, r=1.3, col=RED if t < 2.8 else DIM)
        c.pill(lx, 1380, "14 fields ek page", size=28, fam=MONO, col=RED)
        rx = W * 0.73
        groups = ["1 · Personal", "2 · Address", "3 · Payment"]
        for i, g in enumerate(groups):
            gy = 680 + i * 220; on = t > 3.0 + i * 0.6
            c.fill_rrect(rx - 180, gy, 360, 170, 22, (0.12, 0.12, 0.14))
            c.rrect_path(rx - 180, gy, 360, 170, 22); c.c.set_source_rgba(*(GREEN if on else DIM), 1); c.c.set_line_width(2); c.c.stroke()
            c.font(SANS, 30, True); c.text(rx - 150, gy + 50, g, GREEN if on else DOT)
            for j in range(3): c.dbar(rx - 150, gy + 80 + j * 28, 280, rows=2, gap=6, col=DIM)
        c.pill(rx, 1380, "3 steps · chhote groups", size=28, fam=MONO, col=GREEN)
        if t > 5.0: white_pill(c, W / 2, 1480, "group karo, step by step", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 980), 1.4), (2.4, (W * 0.27, 980), 1.4), (3.0, (W * 0.73, 980), 1.4),
                                     (4.8, (W * 0.73, 980), 1.4), (5.4, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration (Hinglish): the approved Day 05 script. Generated / recorded voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे फाइव।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, मिलर्स लॉ क्या है?", "", s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("दोस्त ने फोन नंबर बोला, नाइन एट सेवन सिक्स फाइव फोर थ्री टू वन ज़ीरो। एक साथ दस डिजिट्स, और दो सेकंड में भूल गए।", "", s2,
          min_dur=6.6, whoosh=True, sfx=[(0.6 + i * 0.11, "tick") for i in range(10)] + [(3.2, "buzz")]),
    Scene("अब वही नंबर ऐसे सुनो, नाइन एट सेवन सिक्स फाइव, फोर थ्री टू वन ज़ीरो। दो छोटे टुकड़े, और याद हो गया।", "", s3,
          min_dur=5.6, whoosh=True, sfx=[(SPLIT, "pop_hi"), (2.6, "pop"), (3.4, "ding")]),
    Scene("यही है मिलर्स लॉ। हमारा दिमाग एक बार में लगभग सात चीज़ें ही याद रख पाता है। इसलिए लंबी जानकारी को छोटे चंक्स में तोड़ो।",
          "", s4, min_dur=8.0, whoosh=True, sfx=[(0.2, "ding"), (2.2, "riser")] + [(2.2 + i * 0.25, "pop") for i in range(7)]
          + [(4.0, "buzz"), (5.4, "pop_hi")]),
    Scene("इसीलिए फोनपे में ओटीपी छह अलग बॉक्सेस में आता है, और कार्ड नंबर चार चार के ग्रुप्स में दिखता है।", "", s5,
          min_dur=7.6, whoosh=True, clicks=[1.0 + i * 0.2 for i in range(6)],
          sfx=[(2.4, "chime"), (6.0, "chime")] + [(4.0 + i * 0.11, "tick") for i in range(16)]),
    Scene("डिज़ाइनर टिप। लंबे फॉर्म को स्टेप्स में बाँटो, और जानकारी को छोटे ग्रुप्स में दिखाओ।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop"), (3.6, "pop"), (4.2, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    import daily
    daily.run(5, "Miller's Law", SCENES, "day05_millers_law_phonepe")

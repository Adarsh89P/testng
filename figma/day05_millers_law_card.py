"""Day 05/45 · Miller's Law, version B: credit-card number and OTP input.

16 digits in one line are hard to read and check; 4-4-4-4 groups (and 6 separate OTP boxes) fit working memory.
Reuses hook / law card / PhonePe checkout / designer tip from day05_millers_law_phonepe.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D
import day05_millers_law_phonepe as P

D.DAY, D.NEXT = 5, "Zeigarnik Effect"
W, H = 1080, 1920
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono = D.K, D.hud, D.mono
DARK = (0.05, 0.05, 0.05)
CARD = "4111222233334444"
TYPO = "4111222223334444"                          # one wrong digit at index 8
GOLD = (0.95, 0.78, 0.35)


def card_face(c, cx, cy, w=760, h=460, a=1.0):
    x, y = cx - w / 2, cy - h / 2
    c.drrect(x, y, w, h, 34, spacing=7, r=2.0, col=GOLD, a=a)
    c.drrect(x + 60, y + 90, 110, 80, 14, spacing=5, r=1.6, col=GOLD, a=a)          # chip
    for i in range(3): c.dline(x + 70, y + 110 + i * 20, x + 160, y + 110 + i * 20, spacing=6, r=1.2, col=GOLD, a=a)
    c.font(SANS, 30, True); c.text(x + w - 170, y + 70, "BANK", GOLD, a)
    c.dbar(x + 60, y + h - 70, 240, rows=2, gap=6, col=DIM, a=a)
    return x, y


def s2(cv, t, d, st):                                     # story: 16 digits in one line, one typo hidden
    n = min(16, int(max(0, t - 0.6) * 12))
    def world(c):
        mono(c, "checkout · card number", 560, (0.85, 0.85, 0.88), 38)
        card_face(c, W / 2, 900)
        cols = None
        if t > 3.0: cols = [RED if i == 8 else DOT for i in range(16)]
        P.digits(c, TYPO[:n], W / 2, 960, 58, col=DOT, cols=cols[:n] if cols else None)
        if t > 2.2:
            for i in range(4):
                ang = -2.4 + i * 0.5
                c.pill(W / 2 + math.cos(ang) * 420, 900 + math.sin(ang) * 330, "?", size=40, fam=MONO, col=RED)
        if t > 3.0: c.pill(W / 2, 1220, "galti kahan hai?", size=34, fam=MONO, col=DARK, bg=RED, bold=True)
        if t > 4.2: white_pill(c, W / 2, 1400, "16 digits ek line = confusion", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.2), (1.8, (W / 2, 960), 1.25), (2.6, (W / 2, 960), 1.25),
                                     (3.2, (W / 2 + 40, 960), 1.7), (4.2, (W / 2 + 40, 960), 1.7), (4.8, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - 3.0) / 0.12), seed=3)
    hud(cv); flash(cv, t, 3.0, 0.12)


SPLIT = 1.2
def s3(cv, t, d, st):                                     # same number in 4-4-4-4: the typo jumps out
    def world(c):
        card_face(c, W / 2, 900)
        k = ease((t - SPLIT) / 0.6)
        gcols = [GREEN] * 4 + [BLUE] * 4 + [RED if t > 2.6 else YELLOW] * 4 + [ORANGE] * 4
        cols = gcols if k > 0 else None
        P.digits(c, TYPO, W / 2, 960, 58, gap_after=(3, 7, 11) if k > 0 else (), cols=cols)
        if t > 2.6:
            c.font(MONO, 58, True); cw = c.text_w("0"); tot = cw * 16 + cw * 0.9 * 3
            gx = W / 2 - tot / 2 + 8 * cw + 2 * cw * 0.9
            c.drrect(gx - 10, 900, 4 * cw + 20, 80, 14, spacing=6, r=2, col=RED)
            c.pill(gx + 2 * cw, 1060, "2333? → 3333", size=30, fam=MONO, col=DARK, bg=RED, bold=True)
        if t > 3.6: white_pill(c, W / 2, 1300, "4-4-4-4 = galti turant dikhi", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.0, (W / 2, 960), 1.25), (2.4, (W / 2, 960), 1.25),
                                     (2.9, (W / 2 + 60, 980), 1.6), (3.8, (W / 2 + 60, 980), 1.6), (4.4, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - SPLIT) / 0.1), seed=4)
    hud(cv); flash(cv, t, 2.6, 0.12)


SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे फाइव।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, मिलर्स लॉ क्या है?", "", P.s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("पेमेंट करते वक्त कार्ड नंबर एक लंबी लाइन में दिखे, सोलह डिजिट्स एक साथ। एक डिजिट गलत, और ढूँढना मुश्किल।", "", s2,
          min_dur=6.0, whoosh=True, sfx=[(0.6 + i * 0.08, "tick") for i in range(16)] + [(3.0, "buzz")]),
    Scene("अब वही नंबर चार चार के ग्रुप्स में। फोर वन वन वन, टू टू टू टू। और गलती तुरंत दिख जाती है।", "", s3,
          min_dur=5.4, whoosh=True, sfx=[(SPLIT, "pop_hi"), (2.6, "buzz"), (3.6, "ding")]),
    Scene("यही है मिलर्स लॉ। हमारा दिमाग एक बार में लगभग सात चीज़ें ही याद रख पाता है। इसलिए लंबी जानकारी को छोटे चंक्स में तोड़ो।",
          "", P.s4, min_dur=8.0, whoosh=True, sfx=[(0.2, "ding"), (2.2, "riser")] + [(2.2 + i * 0.25, "pop") for i in range(7)]
          + [(4.0, "buzz"), (5.4, "pop_hi")]),
    Scene("इसीलिए फोनपे में ओटीपी छह अलग बॉक्सेस में आता है, और कार्ड नंबर चार चार के ग्रुप्स में दिखता है।", "", P.s5,
          min_dur=7.6, whoosh=True, clicks=[1.0 + i * 0.2 for i in range(6)],
          sfx=[(2.4, "chime"), (6.0, "chime")] + [(4.0 + i * 0.11, "tick") for i in range(16)]),
    Scene("डिज़ाइनर टिप। लंबे नंबर और लंबे फॉर्म को छोटे ग्रुप्स में तोड़ो, और हर डिजिट के लिए साफ जगह दो।", "", P.s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop"), (3.6, "pop"), (4.2, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    import daily
    daily.run(5, "Miller's Law", SCENES, "day05_millers_law_card")

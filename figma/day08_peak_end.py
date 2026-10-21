"""Day 08/45 · Peak-End Rule, explained with Google Pay's payment-success moment (tick animation + sound).

People judge an experience mostly by its most intense moment and its end, not the average, so the success screen
matters more than the wait. Day 02 pattern. Voice: Rakhi's Day 08 ElevenLabs Tisha K file (uploaded as day7.mp3,
content verified as Day 08) at assets/voice/day08/full.mp3; script in docs/scripts/day08.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 8, "Von Restorff Effect"
W, H = 1080, 1920
GBLUE = (0.30, 0.55, 1.0)                         # Google blue
GGREEN = (0.20, 0.80, 0.45)                       # success green
PINK = (1.0, 0.45, 0.65)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def mood_curve(c, gx, gy, gw, gh, k, t, dim_mid=False, glow=True):
    """An experience as a line over time: dip (wait), a high peak, a good end. Returns peak and end points."""
    def f(u):  # mood 0..1
        return 0.45 + 0.12 * math.sin(u * 9) - 0.25 * math.exp(-((u - 0.35) / 0.1) ** 2) + 0.45 * math.exp(-((u - 0.62) / 0.05) ** 2) + 0.25 * u ** 6
    pts = [(gx + i / 80 * gw, gy + gh - f(i / 80) * gh) for i in range(81)]
    m = int(k * 80)
    for i in range(m + 1):
        x, y = pts[i]; mid = 8 < i < 74 and abs(i - 50) > 4
        c._dot(x, y, 5, DIM if (dim_mid and mid) else GBLUE, 0.5 if (dim_mid and mid) else 1)
    peak, end = pts[50], pts[80]
    if glow and m >= 50:
        c.glow(*peak, 60, 0.9); c.pill(peak[0], peak[1] - 50, "PEAK", size=28, fam=MONO, col=DARK, bg=PINK, bold=True)
    if glow and m >= 80:
        c.glow(*end, 60, 0.9); c.pill(end[0] - 20, end[1] - 50, "END", size=28, fam=MONO, col=DARK, bg=GGREEN, bold=True)
    return peak, end


def gpay_top(c, a=1.0):
    phone(c, PX, PY, PW, PH, a=a)
    c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 90, "G Pay", GBLUE, a)


def tick(c, cx, cy, r, k, col=GGREEN, a=1.0):
    c.c.set_source_rgba(*col, a * min(1, k * 2)); c.c.arc(cx, cy, r * min(1, 0.6 + k), 0, 6.3); c.c.fill()
    u = max(0, min(1, (k - 0.3) / 0.6))
    p1, p2, p3 = (cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.35), (cx + r * 0.5, cy - r * 0.35)
    pts = [p1, p2, p3]
    c.c.set_source_rgba(1, 1, 1, a); c.c.set_line_width(r * 0.16); c.c.set_line_cap(1); c.c.set_line_join(1)
    seg1 = min(1, u * 2); seg2 = max(0, u * 2 - 1)
    c.c.move_to(*p1); c.c.line_to(lerp(p1[0], p2[0], seg1), lerp(p1[1], p2[1], seg1))
    if seg2 > 0: c.c.line_to(lerp(p2[0], p3[0], seg2), lerp(p2[1], p3[1], seg2))
    c.c.stroke()


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: hum peak + end yaad rakhte hain
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "PEAK-END RULE", 104, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=PINK)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.2: mono(c, "kya hai?", 980, DOT, 58, chars=int((t - 2.2) * 14))
        if t > 3.0:
            mood_curve(c, 170, 1080, 740, 260, ease((t - 3.0) / 1.8), t, dim_mid=t > 4.6)
            if t > 4.8: c.pill(W / 2, 1420, "yaad rehta hai: peak + end", size=30, fam=MONO, col=PINK)
        if t > 5.6: c.pill(W / 2, 1520, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=GBLUE, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1150), 1.0), (5.4, (W / 2, 1200), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


def s2(cv, t, d, st):                                     # send ₹500, UPI PIN, wait
    def world(c):
        gpay_top(c)
        c.dellipse(PX, Y0 + 230, 60, 60, spacing=6, r=2, col=GBLUE); c.font(SANS, 44, True); c.text(PX - 14, Y0 + 246, "R", GBLUE)
        c.font(SANS, 26, True); c.text(PX - c.text_w("Rahul") / 2, Y0 + 330, "Rahul", DOT)
        c.font(SANS, 70, True); c.text(PX - c.text_w("₹500") / 2, Y0 + 440, "₹500", DOT)
        if t > 1.0:                                          # UPI PIN dots fill in
            c.font(SANS, 22, True); c.text(PX - c.text_w("ENTER UPI PIN") / 2, Y0 + 530, "ENTER UPI PIN", DIM)
            n = min(6, int((t - 1.0) * 6))
            for i in range(6):
                x = PX - 125 + i * 50
                if i < n: c._dot(x, Y0 + 580, 11, DOT, 1)
                else: c.dellipse(x, Y0 + 580, 11, 11, spacing=4, r=1.2, col=DIM)
        if t > 2.3:                                          # processing spinner = the boring middle
            for i in range(10):
                ang = t * 5 + i / 10 * 6.283
                c._dot(PX + math.cos(ang) * 50, Y0 + 720 + math.sin(ang) * 50, 6, GBLUE, (i + 1) / 10)
            c.font(SANS, 24, True); c.text(PX - c.text_w("Processing...") / 2, Y0 + 815, "Processing...", DIM)
            c.pill(PX + 330, Y0 + 720, "wait...", size=30, fam=MONO, col=DIM)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.9, (PX, Y0 + 520), 1.5), (2.2, (PX, Y0 + 520), 1.5), (2.8, (PX, Y0 + 700), 1.4),
                                     (d - 0.3, (PX, Y0 + 700), 1.4)), seed=3)
    hud(cv)


DONE = 0.4
def s3(cv, t, d, st):                                     # the peak: tick animation + sound, paid
    def world(c):
        gpay_top(c)
        k = ease(min(1, max(0, (t - DONE) / 0.9)))
        tick(c, PX, Y0 + 330, 120, k)
        if t > DONE + 0.6:
            for i in range(36):
                ang = i / 36 * 6.283; dd = 140 + 260 * ease((t - DONE - 0.6) / 1.4)
                c._dot(PX + math.cos(ang) * dd, Y0 + 330 + math.sin(ang) * dd * 0.8, 6, COLS[i % 6], max(0, 1 - (t - DONE - 0.6) / 1.4))
        if t > DONE + 1.0:
            c.font(SANS, 60, True); c.text(PX - c.text_w("₹500") / 2, Y0 + 560, "₹500", DOT)
            c.font(SANS, 26, True); s = "Paid to Rahul"; c.text(PX - c.text_w(s) / 2, Y0 + 610, s, GGREEN)
        if t > DONE + 1.6:
            c.pill(PX + 330, Y0 + 330, "ding!", size=32, fam=MONO, col=DARK, bg=GGREEN, bold=True)
        if t > DONE + 2.4: white_pill(c, W / 2, 1640, "payment ho gaya · mood accha", 36)
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + 330), 1.7), (DONE + 1.8, (PX, Y0 + 330), 1.7), (DONE + 2.4, ANCHOR, 1.0)),
                  punch=0.06 * max(0, 1 - abs(t - DONE - 0.6) / 0.12), seed=4)
    hud(cv); flash(cv, t, DONE + 0.6, 0.15)


def s4(cv, t, d, st):                                     # law card: whole experience, only peak & end remembered
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "PEAK-END RULE", 98, W / 2, 630, ease(1 - t / 0.8), col=PINK)
        l1 = "experience ko judge karte hain"; l2 = "sabse khaas pal + end se"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 34, chars=n); mono(c, l2, 800, PINK, 34, chars=n - len(l1))
        mood_curve(c, 170, 960, 740, 360, ease((t - 1.8) / 2.0), t, dim_mid=t > 4.0)
        c.font(MONO, 24); c.text(170, 1360, "start", DIM); c.text(840, 1360, "end", DIM)
        if t > 4.2: c.pill(W / 2, 1450, "beech ka wait = bhool gaye", size=30, fam=MONO, col=DIM)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1050), 1.0), (d - 0.4, (W / 2, 1100), 1.05)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # Google Pay makes the END special
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("Google Pay") / 2, 540, "Google Pay", GBLUE)
        gpay_top(c)
        tick(c, PX, Y0 + 330, 120, 1.0)
        c.font(SANS, 60, True); c.text(PX - c.text_w("₹500") / 2, Y0 + 560, "₹500", DOT)
        c.font(SANS, 26, True); s = "Paid to Rahul"; c.text(PX - c.text_w(s) / 2, Y0 + 610, s, GGREEN)
        for i in range(3): c.dbar(X0 + 60, Y0 + 680 + i * 40, PW - 120, rows=2, gap=6, col=DIM)
        ring(c, PX, Y0 + 330, t, 0.8, GGREEN)
        if t > 1.2: c.pill(PX - 330, Y0 + 330, "special END", size=28, fam=MONO, col=DARK, bg=GGREEN, bold=True)
        if t > 2.4: c.pill(PX + 330, Y0 + 720, "wait? bhool gaye", size=26, fam=MONO, col=DIM)
        if t > 3.6: white_pill(c, W / 2, 1640, "bas khushi yaad rehti hai", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX, Y0 + 400), 1.5), (2.8, (PX, Y0 + 400), 1.5), (3.4, ANCHOR, 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T plain end | DO memorable success screen
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 180, 680, 360, 420, 24, (0.13, 0.13, 0.15))
        c.font(SANS, 26, True); c.text(lx - c.text_w("Transaction") / 2, 860, "Transaction", DIM); c.text(lx - c.text_w("complete.") / 2, 900, "complete.", DIM)
        c.pill(lx, 1160, "boring end", size=28, fam=MONO, col=RED)
        c.fill_rrect(rx - 180, 680, 360, 420, 24, (0.10, 0.16, 0.12))
        k = ease(min(1, max(0, (t - 3.0) / 0.9)))
        tick(c, rx, 820, 70, k)
        if t > 3.8:
            c.font(SANS, 30, True); s = "₹500 sent!"; c.text(rx - c.text_w(s) / 2, 950, s, GGREEN)
            c.font(SANS, 22); s = "Rahul ko mil gaye"; c.text(rx - c.text_w(s) / 2, 990, s, DOT)
            for i in range(16):
                ang = i / 16 * 6.283; dd = 80 + 90 * ease((t - 3.8) / 1.0)
                c._dot(rx + math.cos(ang) * dd, 820 + math.sin(ang) * dd, 4, COLS[i % 6], max(0, 1 - (t - 3.8)))
        c.pill(rx, 1160, "yaadgaar end", size=28, fam=MONO, col=GREEN)
        if t > 5.0: white_pill(c, W / 2, 1300, "end ko yaadgaar banao", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration (Hinglish): the approved Day 08 script (docs/scripts/day08.md). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे एट।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, पीक एंड रूल क्या है? हम पूरा एक्सपीरियंस नहीं, बस उसका बेस्ट मोमेंट और एंड याद रखते हैं। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.6, whoosh=True, sfx=[(1.2, "drop"), (2.2, "pop"), (3.0, "riser"), (4.8, "ding"), (5.6, "pop_hi")]),
    Scene("गूगल पे से दोस्त को पैसे भेजे। यूपीआई पिन डाला, और थोड़ा वेट किया।", "", s2,
          min_dur=5.0, whoosh=True, sfx=[(1.0 + i * 0.17, "tick") for i in range(6)] + [(2.3 + i * 0.5, "tick") for i in range(5)]),
    Scene("और फिर, टिक का एनिमेशन, और एक प्यारी सी साउंड। पेमेंट हो गया, और मूड भी अच्छा।", "", s3,
          min_dur=5.4, whoosh=False, sfx=[(DONE + 0.5, "chime"), (DONE + 0.6, "pop_hi"), (DONE + 1.6, "ding")]),
    Scene("यही है पीक एंड रूल। लोग एक्सपीरियंस को उसके सबसे खास पल और उसके एंड से जज करते हैं।", "", s4,
          min_dur=6.6, whoosh=True, sfx=[(0.2, "ding"), (1.8, "riser"), (4.0, "pop"), (4.2, "pop_hi")]),
    Scene("इसीलिए गूगल पे पेमेंट के एंड को इतना स्पेशल बनाता है, कि वेट भूल जाते हैं, बस खुशी याद रहती है।", "", s5,
          min_dur=6.2, whoosh=True, sfx=[(0.8, "chime"), (1.2, "pop"), (3.6, "ding")]),
    Scene("डिज़ाइनर टिप। हर स्टेप परफेक्ट नहीं हो सकता, पर एंड को यादगार बनाओ। सक्सेस स्क्रीन पे ध्यान दो।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "chime"), (3.8, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# day7.mp3 (content = Day 08) has only 3 long pauses: line cuts found by aligning it to a TTS reading of the script,
# each snapped to the quietest point within 0.8 s (all silent); line check 8/8.
VO_CUTS = [4.58, 14.72, 19.96, 26.76, 33.42, 41.26, 48.94]

if __name__ == "__main__":
    import daily
    daily.run(8, "Peak-End Rule", SCENES, "day08_peak_end", cuts=VO_CUTS)

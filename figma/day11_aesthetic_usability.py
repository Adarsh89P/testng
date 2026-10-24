"""Day 11/45 · Aesthetic-Usability Effect, explained with CRED's credit-card bill payment.

People perceive a beautiful interface as easier to use (and trust it more), even when the task is the same.
Day 02 pattern. Voice: Rakhi's Day 11 ElevenLabs Tisha K file at assets/voice/day11/full.mp3 (content-verified);
script in docs/scripts/day11.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 11, "Doherty Threshold"
W, H = 1080, 1920
GOLD = (0.93, 0.80, 0.55)                          # CRED-style champagne accent
MINT = (0.45, 0.95, 0.80)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def messy_app(c, t, a=1.0, cx=PX, cy=PY, w=PW, h=PH, small=False):
    """Cluttered bill-pay screen: mismatched colours, crowded labels, tiny buttons."""
    x0, y0 = cx - w / 2, cy - h / 2
    phone(c, cx, cy, w, h, a=a)
    sc = w / PW
    c.fill_rrect(x0 + 20 * sc, y0 + 60 * sc, w - 40 * sc, 70 * sc, 4, (0.25, 0.30, 0.55), a)
    c.font(SANS, int(22 * sc), True); c.text(x0 + 34 * sc, y0 + 104 * sc, "PAY BILL NOW!!", YELLOW, a)
    labels = ["Card No.", "Amount", "Due", "Min amt", "Promo", "Remarks"]
    for i, lab in enumerate(labels):
        y = y0 + (160 + i * 64) * sc
        c.font(SANS, int(16 * sc)); c.text(x0 + 26 * sc + (i % 2) * 12 * sc, y + 4 * sc, lab, DIM, a)
        c.rrect_path(x0 + 120 * sc, y - 18 * sc, w - 150 * sc, 34 * sc, 2); c.c.set_source_rgba(*GREY, a); c.c.set_line_width(1); c.c.stroke()
    btn = [((0.9, 0.3, 0.3), "Pay"), ((0.3, 0.7, 0.3), "Save"), ((0.3, 0.5, 0.9), "Back"), ((0.8, 0.6, 0.2), "Help")]
    for i, (col, lab) in enumerate(btn):
        bx = x0 + (26 + i * 104) * sc; by = y0 + (570 + (i % 2) * 10) * sc
        c.fill_rrect(bx, by, 92 * sc, 40 * sc, 3, col, a)
        c.font(SANS, int(16 * sc), True); c.text(bx + 20 * sc, by + 26 * sc, lab, DARK, a)
    for i in range(5): c.dbar(x0 + 26 * sc, y0 + (650 + i * 26) * sc, (w - 60 * sc) * (0.9 - 0.1 * (i % 3)), rows=1, gap=4, col=GREY, a=a)
    return (cx, y0 + 590 * sc)


def cred_app(c, t, a=1.0, cx=PX, cy=PY, w=PW, h=PH, pay_k=0.0):
    """Clean dark CRED-style screen: one card, generous spacing, one clear Pay button with a soft glow."""
    x0, y0 = cx - w / 2, cy - h / 2
    sc = w / PW
    phone(c, cx, cy, w, h, a=a)
    c.font(SANS, int(30 * sc), True); c.text(x0 + 30 * sc, y0 + 92 * sc, "CRED", GOLD, a)
    kx, ky, kw, kh = x0 + 40 * sc, y0 + 150 * sc, w - 80 * sc, 230 * sc
    c.fill_rrect(kx, ky, kw, kh, 22, (0.12, 0.12, 0.14), a)
    c.rrect_path(kx, ky, kw, kh, 22); c.c.set_source_rgba(*GOLD, a * 0.7); c.c.set_line_width(1.5); c.c.stroke()
    sh = (t * 0.5) % 1.6 - 0.3                                          # soft sheen sweeping across the card
    if 0 < sh < 1:
        c.c.save(); c.rrect_path(kx, ky, kw, kh, 22); c.c.clip()
        g = c.c; sx = kx + kw * sh
        for i in range(8): g.set_source_rgba(1, 1, 1, 0.03); g.rectangle(sx - 20 + i * 5, ky, 6, kh); g.fill()
        c.c.restore()
    c.font(MONO, int(24 * sc), True); c.text(kx + 26 * sc, ky + 140 * sc, "•••• 4821", DOT, a)
    c.font(SANS, int(18 * sc)); c.text(kx + 26 * sc, ky + 190 * sc, "due in 3 days", DIM, a)
    c.font(SANS, int(18 * sc)); c.text(x0 + 40 * sc, y0 + 440 * sc, "total due", DIM, a)
    c.font(SANS, int(52 * sc), True); c.text(x0 + 40 * sc, y0 + 500 * sc, "₹12,480", DOT, a)
    bx, by, bw, bh = x0 + 40 * sc, y0 + 640 * sc, w - 80 * sc, 90 * sc
    glow = 0.5 + 0.5 * abs(math.sin(t * 2.4))
    c.glow(cx, by + bh / 2, 140 * sc, 0.25 * glow * a)
    c.fill_rrect(bx, by, bw, bh, bh / 2, GOLD if pay_k < 1 else MINT, a)
    lab = "pay ₹12,480" if pay_k < 1 else "paid ✓"
    c.font(SANS, int(28 * sc), True); c.text(cx - c.text_w(lab) / 2, by + bh * 0.64, lab, DARK, a)
    return (cx, by + bh / 2)


def meter(c, x, y, k, col, label, a=1.0):
    c.font(MONO, 22, True); c.text(x - 80, y - 14, label, DIM, a)
    c.fill_rrect(x - 80, y, 160, 18, 9, (0.2, 0.2, 0.23), a)
    if k > 0: c.fill_rrect(x - 80, y, max(18, 160 * k), 18, 9, col, a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: sundar = aasaan lagta hai
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "AESTHETIC-USABILITY", 76, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=GOLD)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "EFFECT kya hai?", 970, DOT, 52, chars=int((t - 2.0) * 14))
        if t > 3.0:                                          # a messy box turns into a clean glowing one
            k = ease(min(1, (t - 3.4) / 1.0))
            bx, by = W / 2, 1200
            for i in range(14):
                jx = math.sin(i * 2.7) * 120 * (1 - k); jy = math.cos(i * 1.9) * 70 * (1 - k)
                col = COLS[i % 6] if k < 0.5 else GOLD
                c.fill_rrect(bx - 150 + (i % 7) * 44 + jx, by - 40 + (i // 7) * 44 + jy, 34, 34, 4 + 10 * k, col, 0.4 + 0.6 * k)
            if k > 0.95: c.glow(bx, by, 160, 0.4)
            c.pill(W / 2, 1350, "sundar = aasaan lagta hai", size=30, fam=MONO, col=GOLD)
        if t > 5.4: c.pill(W / 2, 1460, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=GOLD, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1150), 1.0), (5.2, (W / 2, 1150), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


def s2(cv, t, d, st):                                     # App X: boring form, scattered buttons
    def world(c):
        c.font(SANS, 70, True); c.text(W / 2 - c.text_w("App X") / 2, 540, "App X", RED)
        b = messy_app(c, t)
        st["btn"] = b
        if t > 1.4: c.pill(PX + 340, Y0 + 300, "boring form", size=28, fam=MONO, col=DARK, bg=RED, bold=True)
        if t > 2.4: c.pill(PX + 340, b[1], "bikhre buttons", size=28, fam=MONO, col=DARK, bg=RED, bold=True)
        if t > 3.2:
            for i in range(4):
                ang = -2.4 + i * 0.6
                c.pill(PX + math.cos(ang) * 330, PY + math.sin(ang) * 460, "?", size=34, fam=MONO, col=RED)
    bb = st.get("btn", (PX, Y0 + 590))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.2, (PX, Y0 + 360), 1.4), (2.2, bb, 1.5), (d - 0.4, bb, 1.5)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # CRED: dark theme, smooth, clean -> feels easy
    def world(c):
        c.font(SANS, 70, True); c.text(W / 2 - c.text_w("CRED") / 2, 540, "CRED", GOLD)
        k = ease(min(1, t / 0.8))
        b = cred_app(c, t, a=k)
        st["btn"] = b
        if t > 1.0: c.pill(PX - 330, Y0 + 260, "dark theme", size=26, fam=MONO, col=DARK, bg=GOLD, bold=True)
        if t > 1.8: c.pill(PX + 330, Y0 + 260, "smooth animation", size=26, fam=MONO, col=DARK, bg=GOLD, bold=True)
        if t > 2.6: c.pill(PX - 330, b[1], "saaf design", size=26, fam=MONO, col=DARK, bg=GOLD, bold=True)
        if t > 3.6: white_pill(c, W / 2, 1640, "kaam wahi, par lagta aasaan", 36)
    bb = st.get("btn", (PX, Y0 + 685))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.0, (PX, Y0 + 300), 1.35), (2.4, bb, 1.4), (3.2, ANCHOR, 1.0)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law card: same task, "aasaan?" meter higher for the pretty one
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "AESTHETIC-USABILITY", 72, W / 2, 630, ease(1 - t / 0.8), col=GOLD)
        l1 = "sundar design dekh kar lagta hai,"; l2 = "use karna bhi aasaan hoga"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 32, chars=n); mono(c, l2, 798, GOLD, 32, chars=n - len(l1))
        messy_app(c, t, cx=W * 0.28, cy=1110, w=300, h=550)
        cred_app(c, t, cx=W * 0.72, cy=1110, w=300, h=550)
        k = ease(min(1, max(0, (t - 2.6) / 1.4)))
        meter(c, W * 0.28, 1430, 0.35 * k, RED, "aasaan?")
        meter(c, W * 0.72, 1430, 0.9 * k, GOLD, "aasaan?")
        if t > 4.2: c.pill(W * 0.72, 1500, "same kaam, zyada aasaan lagta", size=24, fam=MONO, col=GOLD)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1080), 1.0), (d - 0.4, (W / 2, 1100), 1.03)), seed=5)
    hud(cv)


PAY = 1.8
def s5(cv, t, d, st):                                     # CRED cares about design -> trust + delight
    def world(c):
        c.font(SANS, 70, True); c.text(W / 2 - c.text_w("CRED") / 2, 540, "CRED", GOLD)
        b = cred_app(c, t, pay_k=1.0 if t > PAY + 0.3 else 0.0)
        st["btn"] = b
        ring(c, *b, t, PAY, MINT)
        if PAY - 0.4 < t < PAY + 0.2: c._dot(b[0] + 10, b[1] + 12, 16, (1, 1, 1), 0.9)
        if t > PAY + 0.3:
            for i in range(30):
                ang = i / 30 * 6.283; dd = 60 + 240 * ease((t - PAY - 0.3) / 1.2)
                c._dot(b[0] + math.cos(ang) * dd, b[1] + math.sin(ang) * dd * 0.6, 5, COLS[i % 6], max(0, 1 - (t - PAY - 0.3) / 1.2))
        if t > PAY + 1.0: c.pill(PX + 330, Y0 + 260, "bharosa ↑", size=30, fam=MONO, col=DARK, bg=MINT, bold=True)
        if t > PAY + 1.6: c.pill(PX - 330, Y0 + 260, "maza ↑", size=30, fam=MONO, col=DARK, bg=GOLD, bold=True)
    bb = st.get("btn", (PX, Y0 + 685))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.0, bb, 1.5), (PAY + 0.9, bb, 1.5), (PAY + 1.5, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - PAY) / 0.1), seed=6)
    hud(cv); flash(cv, t, PAY + 0.3, 0.12)


def s6(cv, t, d, st):                                     # designer tip: DON'T pretty but confusing | DO usable first, then pretty
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 180, 680, 360, 420, 28, (0.14, 0.11, 0.18))           # pretty gradient-ish card, but no clear action
        for i in range(10): c._dot(lx - 120 + (i % 5) * 60, 760 + (i // 5) * 60, 12, COLS[i % 6], 0.8)
        c.font(SANS, 22); c.text(lx - 60, 1000, "pay kahan?", DIM)
        c._dot(lx + 150, 1080, 6, GREY, 0.5)                                      # the "button": a tiny hidden dot
        c.pill(lx, 1160, "sundar par confusing", size=26, fam=MONO, col=RED)
        c.fill_rrect(rx - 180, 680, 360, 420, 28, (0.12, 0.12, 0.14))
        c.font(SANS, 26, True); c.text(rx - 150, 760, "Total due", DIM); c.font(SANS, 44, True); c.text(rx - 150, 820, "₹12,480", DOT)
        c.fill_rrect(rx - 150, 960, 300, 76, 38, GOLD); c.font(SANS, 26, True); c.text(rx - 40, 1008, "Pay", DARK)
        c.pill(rx, 1160, "pehle usable, phir sundar ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "sundarta kaam ki jagah nahi leti", 34)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 11 script (docs/scripts/day11.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे इलेवन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, एस्थेटिक यूज़ेबिलिटी इफ़ेक्ट क्या है? जो चीज़ सुंदर दिखती है, वो इस्तेमाल में भी आसान लगती है। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.4, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (3.4, "riser"), (4.4, "chime"), (5.4, "pop_hi")]),
    Scene("दो ऐप्स, दोनों में क्रेडिट कार्ड का बिल भरना है। एक ऐप में बोरिंग फ़ॉर्म, और बिखरे हुए बटन्स।", "", s2,
          min_dur=5.4, whoosh=True, sfx=[(1.4, "buzz"), (2.4, "buzz"), (3.2, "pop_lo")]),
    Scene("और क्रेड में, डार्क थीम, स्मूद एनिमेशन, और साफ़ सुथरा डिज़ाइन। काम वही, पर लगता है बहुत आसान।", "", s3,
          min_dur=5.6, whoosh=True, sfx=[(0.2, "riser"), (1.0, "pop"), (1.8, "pop"), (2.6, "pop_hi"), (3.6, "ding")]),
    Scene("यही है एस्थेटिक यूज़ेबिलिटी इफ़ेक्ट। सुंदर डिज़ाइन देखकर हमें लगता है कि ऐप इस्तेमाल करना भी आसान होगा।", "", s4,
          min_dur=6.6, whoosh=True, sfx=[(0.2, "ding"), (2.6, "riser"), (4.2, "pop_hi")]),
    Scene("इसीलिए क्रेड डिज़ाइन पे इतना ध्यान देता है, ताकि भरोसा बढ़े और यूज़र्स को मज़ा आए।", "", s5,
          min_dur=5.6, whoosh=True, clicks=[PAY], sfx=[(PAY + 0.02, "pop_hi"), (PAY + 0.3, "chime"), (PAY + 1.0, "pop"), (PAY + 1.6, "pop")]),
    Scene("डिज़ाइनर टिप। सुंदरता ज़रूरी है, पर काम की जगह नहीं ले सकती। पहले यूज़ेबल बनाओ, फिर सुंदर।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 11 file has 7 pauses, but one sits inside line 7 ("Designer tip. ...") and lines 5/6 run together, so the
# auto split is off; line cuts found by aligning to a TTS reading of the script, snapped to silence; line check 8/8.
VO_CUTS = [6.02, 16.08, 24.48, 32.1, 39.64, 46.1, 54.4]

if __name__ == "__main__":
    import daily
    daily.run(11, "Aesthetic-Usability Effect", SCENES, "day11_aesthetic_usability", cuts=VO_CUTS)

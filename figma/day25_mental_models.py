"""Day 25/45 · Mental Models, explained with the cart icon in shopping apps.

A mental model is the picture of how something works that users bring with them. Nobody was taught the cart icon:
pushing a supermarket trolley taught it. So Amazon and Flipkart keep a cart in the corner (some apps a bag, same idea);
a safe or a box there would leave users searching. Day 02 pattern; the script opens as a guessing game and ends with a
"which icon still confuses you?" question. Voice: Rakhi's Day 25 ElevenLabs Tisha K file at
assets/voice/day25/full.mp3 (content-verified); script in docs/scripts/day25.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 25, "Banner Blindness"
W, H = 1080, 1920
MINT = (0.30, 0.85, 0.70)                         # mental-model accent
AMZ = (1.0, 0.60, 0.0)
FK = (0.16, 0.45, 0.94)
PINK = (0.95, 0.35, 0.55)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def cart(c, x, y, s=1.0, col=DOT, a=1.0, count=None):
    """Shopping trolley outline (dotted handle + basket + two wheels)."""
    pts = [(x - 34 * s, y - 26 * s), (x - 24 * s, y - 26 * s), (x - 14 * s, y + 10 * s), (x + 26 * s, y + 10 * s),
           (x + 32 * s, y - 14 * s), (x - 19 * s, y - 14 * s)]
    c.dots_path(pts, spacing=max(3, 5 * s), r=max(1.6, 2.6 * s), col=col, a=a)
    for wx in (x - 10 * s, x + 22 * s):
        c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(wx, y + 22 * s, 5 * s, 0, 6.2832); c.c.fill()
    if count:
        c.c.new_path(); c.c.set_source_rgba(*AMZ, a); c.c.arc(x + 26 * s, y - 32 * s, 13 * s, 0, 6.2832); c.c.fill()
        c.font(SANS, int(16 * s), True); c.text(x + 21 * s, y - 26 * s, str(count), DARK, a)
    c.c.new_path()


def bag(c, x, y, s=1.0, col=DOT, a=1.0):
    c.rrect_path(x - 24 * s, y - 14 * s, 48 * s, 40 * s, 6 * s); c.c.set_source_rgba(*col, a); c.c.set_line_width(3 * s); c.c.stroke()
    c.c.new_path(); c.c.arc(x, y - 14 * s, 12 * s, math.pi, 2 * math.pi); c.c.stroke(); c.c.new_path()


def safe(c, x, y, s=1.0, col=DOT, a=1.0):
    c.rrect_path(x - 26 * s, y - 24 * s, 52 * s, 48 * s, 6 * s); c.c.set_source_rgba(*col, a); c.c.set_line_width(3 * s); c.c.stroke()
    c.c.new_path(); c.c.arc(x, y, 10 * s, 0, 6.2832); c.c.stroke()
    c.c.new_path(); c.c.move_to(x, y); c.c.line_to(x + 8 * s, y - 6 * s); c.c.stroke(); c.c.new_path()


def box(c, x, y, s=1.0, col=DOT, a=1.0):
    c.rrect_path(x - 26 * s, y - 16 * s, 52 * s, 40 * s, 4 * s); c.c.set_source_rgba(*col, a); c.c.set_line_width(3 * s); c.c.stroke()
    c.c.new_path(); c.c.move_to(x - 26 * s, y - 16 * s); c.c.line_to(x - 16 * s, y - 28 * s); c.c.line_to(x + 36 * s, y - 28 * s)
    c.c.line_to(x + 26 * s, y - 16 * s); c.c.stroke(); c.c.new_path()


def shop_screen(c, title, col, icon="cart", a=1.0, count=3):
    phone(c, PX, PY, PW, PH)
    c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 70, 12, col, a)
    c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 96, title, (1, 1, 1), a)
    ix, iy = X0 + PW - 60, Y0 + 86
    {"cart": lambda: cart(c, ix, iy, 0.8, (1, 1, 1), a, count), "bag": lambda: bag(c, ix, iy, 0.8, (1, 1, 1), a),
     "safe": lambda: safe(c, ix, iy, 0.75, (1, 1, 1), a), "box": lambda: box(c, ix, iy, 0.75, (1, 1, 1), a)}[icon]()
    for i in range(2):
        for j in range(2):
            x = X0 + 30 + j * 215; y = Y0 + 150 + i * 330
            c.fill_rrect(x, y, 195, 300, 14, CARD, a)
            c.fill_rrect(x + 15, y + 15, 165, 160, 10, tuple(0.2 + cc * 0.35 for cc in COLS[(i * 2 + j) % 6]), a)
            c.dbar(x + 15, y + 200, 140, rows=2, gap=8, col=DOT)
            c.font(SANS, 22, True); c.text(x + 15, y + 270, "₹" + str(499 + (i * 2 + j) * 300), DOT, a)
    return ix, iy


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # guess: tiny trolley in the corner — you already know it
    def world(c):
        ix, iy = shop_screen(c, "Shop", (0.20, 0.22, 0.28))
        if t > 0.6: ring(c, ix, iy, t, 0.6, col=MINT)
        if t > 1.2:
            k = ease(min(1, (t - 1.2) / 0.6))
            c.c.new_path(); c.c.set_source_rgba(0.08, 0.08, 0.09, 0.95 * k); c.c.arc(PX, PY - 40, 170 * k, 0, 6.2832); c.c.fill()
            c.c.new_path(); c.c.set_source_rgba(*MINT, k); c.c.arc(PX, PY - 40, 170 * k, 0, 6.2832); c.c.set_line_width(4); c.c.stroke()
            cart(c, PX, PY - 40, 2.6 * k, DOT, k, 3)
        if t > 2.2: c.pill(PX, PY + 170, "bina padhe pata hai", size=28, fam=SANS, col=DARK, bg=MINT, bold=True)
        if t > 3.6: white_pill(c, W / 2, 1660, "aapka saamaan, jo khareedne waale ho", 32)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 120, Y0 + 200), 1.35), (1.2, (PX, PY), 1.05),
                                     (d - 0.4, (PX, PY + 40), 1.05)), seed=2)
    hud(cv)


def s2(cv, t, d, st):                                     # origin: the supermarket trolley taught it
    def world(c):
        c.pill(W / 2, 560, "kisi ne sikhaaya nahi", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        cart(c, W / 2 - 200, 1000, 6.0, DOT)
        for i in range(5):
            at = 0.6 + i * 0.45
            if t > at:
                k = ease(min(1, (t - at) / 0.4))
                c.fill_rrect(W / 2 - 300 + i * 46, 760 + 140 * k, 40, 50, 8, COLS[i % 6])
        c.font(SANS, 34, True); c.text(W / 2 - 300, 1260, "supermarket", DIM)
        if t > 3.0:
            k = ease(min(1, (t - 3.0) / 0.6))
            c.dots_path([(W / 2 + 40, 1000), (W / 2 + 40 + 180 * k, 1000)], spacing=9, r=3, col=MINT)
            c.fill_rrect(W / 2 + 230, 900, 200, 200, 30, (0.20, 0.22, 0.28), k)
            cart(c, W / 2 + 330, 1000, 1.8, (1, 1, 1), k, 3)
            c.font(SANS, 30, True); c.text(W / 2 + 270, 1260, "app", DIM, k)
        if t > 4.0: c.pill(W / 2, 1400, "dimaag mein baith gayi", size=30, fam=MONO, col=DARK, bg=MINT, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2 - 160, 960), 1.15), (2.8, (W / 2 - 160, 960), 1.15), (3.6, (W / 2, 1000), 1.0),
                                     (d - 0.4, (W / 2, 1040), 1.0)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # law named: the picture users bring with them
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "MENTAL", 120, W / 2, 620, ease(1 - t / 0.8), col=MINT)
        dot_text(c, "MODEL", 120, W / 2, 750, ease(1 - (t - 0.2) / 0.8), col=MINT)
        hx, hy = W / 2, 1100
        c.dellipse(hx, hy, 170, 190, spacing=8, r=2.6, col=DOT)
        c.dots_path([(hx - 60, hy + 186), (hx - 70, hy + 290), (hx + 80, hy + 290), (hx + 60, hy + 186)], spacing=8, r=2.6, col=DOT)
        if t > 1.6:
            k = ease(min(1, (t - 1.6) / 0.6))
            c.fill_rrect(hx - 120, hy - 90, 240, 150, 20, (0.10, 0.20, 0.18), k)
            cart(c, hx, hy - 15, 2.0 * k, MINT, k)
        if t > 2.8:
            for i, lab in enumerate(["cheezein kaise", "kaam karti hain"]):
                c.font(SANS, 28, True); c.text(hx + 220, hy - 40 + i * 40, lab, DOT)
        if t > 3.8: c.pill(W / 2, 1480, "user pehle se lekar aata hai", size=30, fam=MONO, col=DARK, bg=MINT, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1060), 1.0), (d - 0.4, (W / 2, 1100), 1.03)), seed=4)
    hud(cv); flash(cv, t, 0.2)


def mini_app(c, cx, y, title, col, icon, a=1.0):
    c.fill_rrect(cx - 150, y, 300, 420, 26, (0.09, 0.09, 0.10), a)
    c.rrect_path(cx - 150, y, 300, 420, 26); c.c.set_source_rgba(*GREY, a); c.c.set_line_width(2); c.c.stroke()
    c.fill_rrect(cx - 140, y + 14, 280, 64, 14, col, a)
    c.font(SANS, 24, True); c.text(cx - 124, y + 56, title, (1, 1, 1), a)
    (cart if icon == "cart" else bag)(c, cx + 100, y + 46, 0.7, (1, 1, 1), a)
    for k in range(3): c.fill_rrect(cx - 130, y + 100 + k * 100, 260, 84, 12, CARD, a)


def s4(cv, t, d, st):                                     # Amazon, Flipkart: cart in the corner; some show a bag — same idea
    def world(c):
        apps = [("amazon", AMZ, "cart", W / 2 - 330), ("Flipkart", FK, "cart", W / 2), ("Fashion", PINK, "bag", W / 2 + 330)]
        for i, (nm, col, ic, cx) in enumerate(apps):
            at = 0.3 + i * 0.6
            k = ease(min(1, max(0, (t - at) / 0.5)))
            if k > 0:
                mini_app(c, cx, 640, nm, col, ic, k)
                if t > at + 0.5: ring(c, cx + 100, 686, t, at + 0.5, col=MINT)
        if t > 2.4: c.pill(W / 2 + 330, 1110, "bag? idea wahi", size=24, fam=MONO, col=DARK, bg=PINK, bold=True)
        if t > 3.2:
            steps = ["saamaan daalo", "→", "aakhir mein pay"]
            c.pill(W / 2, 1250, "  ".join(steps), size=30, fam=SANS, col=DARK, bg=MINT, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 980), 1.02)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # broken model: a safe or a box in the corner → user searches
    def world(c):
        icon = "safe" if t < 2.4 else "box"
        ix, iy = shop_screen(c, "Shop", (0.20, 0.22, 0.28), icon=icon, count=None)
        ring(c, ix, iy, t, 0.4 if icon == "safe" else 2.4, col=RED)
        c.pill(ix - 20, iy + 80, "tijori?" if icon == "safe" else "dibba?", size=24, fam=SANS, col=DARK, bg=RED, bold=True)
        if t > 1.0:
            path_t = (t - 1.0) * 1.6
            cx = PX + math.sin(path_t * 1.7) * 150; cy = PY + math.cos(path_t * 1.1) * 260
            c._dot(cx, cy, 13, (1, 1, 1), 1)
            for j, (dx, dy) in enumerate([(-150, -150), (140, 60), (-60, 250)]):
                if t > 1.4 + j * 0.5: c.font(SANS, 56, True); c.text(PX + dx, PY + dy, "?", YELLOW)
        if t > 3.4: white_pill(c, W / 2, 1640, "dhoondhta hi reh gaya", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.4, (PX + 100, Y0 + 260), 1.25), (1.8, (PX, PY), 1.0),
                                     (d - 0.4, (PX, PY + 30), 1.02)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # tip: don't teach new things — match what users already know
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("designer ka kaam") / 2, 560, "designer ka kaam", MINT)
        lx, rx = W * 0.27, W * 0.73
        k1 = ease(min(1, max(0, (t - 0.4) / 0.5)))
        c.fill_rrect(lx - 200, 660, 400, 420, 24, CARD, k1)
        safe(c, lx, 830, 2.4, DIM, k1)
        c.font(SANS, 26, True); c.text(lx - c.text_w("nayi cheez sikhaana") / 2, 1020, "nayi cheez sikhaana", RED, k1)
        if t > 1.2: c.font(SANS, 70, True); c.text(lx - 22, 760, "✗", RED)
        k2 = ease(min(1, max(0, (t - 2.0) / 0.5)))
        c.fill_rrect(rx - 200, 660, 400, 420, 24, (0.08, 0.20, 0.17), k2)
        c.dellipse(rx - 70, 820, 60, 66, spacing=6, r=2, col=DOT, a=k2)
        cart(c, rx - 70, 815, 1.0, MINT, k2)
        c.font(SANS, 44, True); c.text(rx - 10, 836, "=", DOT, k2)
        cart(c, rx + 90, 815, 1.6, MINT, k2)
        c.font(SANS, 24, True); c.text(rx - c.text_w("jo pehle se jaanta hai") / 2, 1020, "jo pehle se jaanta hai", GREEN, k2)
        if t > 3.6: white_pill(c, W / 2, 1240, "design ko usi se milaao", 38)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 870), 1.3), (1.6, (W * 0.27, 870), 1.3), (2.4, (W * 0.73, 870), 1.3),
                                     (3.4, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 960), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 25 script (docs/scripts/day25.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी फ़ाइव। चलो, आज एक छोटा सा गेस करते हैं।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("स्क्रीन के कोने में, एक छोटी सी ट्रॉली। बिना कुछ पढ़े, आपको पता है ये क्या है। आपका सामान, जो आप ख़रीदने वाले हो।", "", s1,
          min_dur=6.0, whoosh=True, sfx=[(0.6, "pop_hi"), (1.2, "riser"), (2.2, "chime"), (3.6, "ding")]),
    Scene("ये आपको किसी ने सिखाया नहीं। सुपरमार्केट में ट्रॉली में सामान डालते-डालते, ये बात दिमाग़ में बैठ गई।", "", s2,
          min_dur=5.6, whoosh=True, sfx=[(0.6 + i * 0.45, "pop") for i in range(5)] + [(3.0, "riser"), (4.0, "chime")]),
    Scene("इसे कहते हैं, मेंटल मॉडल। चीज़ें कैसे काम करती हैं, उसकी वो तस्वीर, जो यूज़र पहले से अपने दिमाग़ में लेकर आता है।", "", s3,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "drop"), (1.6, "pop_hi"), (2.8, "pop"), (3.8, "ding")]),
    Scene("इसीलिए ऐमज़ॉन हो या फ़्लिपकार्ट, सबके कोने में कार्ट है। कोई बैग दिखाता है, पर आइडिया वही। सामान डालो, और आख़िर में पैसे दो।", "", s4,
          min_dur=6.4, whoosh=True, sfx=[(0.3 + i * 0.6, "pop") for i in range(3)] + [(2.4, "pop_hi"), (3.2, "chime")]),
    Scene("अब सोचो, कोई ऐप वहाँ एक तिजोरी, या डिब्बा रख दे। यूज़र रुकेगा, सोचेगा, और शायद, ढूँढता ही रह जाएगा।", "", s5,
          min_dur=5.6, whoosh=True, sfx=[(0.4, "buzz"), (1.4, "pop_lo"), (1.9, "pop_lo"), (2.4, "buzz"), (2.4, "pop_lo"), (3.4, "drop")]),
    Scene("तो डिज़ाइनर का काम, यूज़र को नई चीज़ सिखाना नहीं। बल्कि जो वो पहले से जानता है, डिज़ाइन को उसी से मिलाना है।", "", s6,
          min_dur=6.0, whoosh=True, sfx=[(0.4, "pop_lo"), (1.2, "buzz"), (2.0, "pop_hi"), (2.6, "chime"), (3.6, "ding")]),
    Scene("आपके फ़ोन में ऐसा कौन सा आइकन है, जो आज तक समझ नहीं आया? कमेंट करो। कल मिलते हैं, बैनर ब्लाइंडनेस के साथ।", "", D.s8,
          min_dur=5.0, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = "auto"

if __name__ == "__main__":
    import daily
    daily.run(25, "Mental Models", SCENES, "day25_mental_models", cuts=VO_CUTS)

"""Day 38/45 · Recognition over Recall, explained with Zomato's veg / non-veg dot and order history.

A green or red dot lets you pick food without reading a word. Quick test: what did you order last week? (hard to
recall) → open order history → "arre haan, yahi tha!" (recognising takes a second). Let users recognise, don't make
them remember: veg dot, recent searches, Order Again, labels under icons. The brain tires recalling, not recognising.
Tip: show past choices, keep options visible, give suggestions instead of an empty box. Day 02 pattern; hook pays off
yesterday's teaser. Voice: Rakhi's Day 38 ElevenLabs Tisha K file at assets/voice/day38/full.mp3 (content-verified);
script in docs/scripts/day38.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 38, "Error Prevention"
W, H = 1080, 1920
ZR = (0.89, 0.22, 0.27)                            # Zomato red
VEG = (0.10, 0.62, 0.30)
NON = (0.62, 0.24, 0.14)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def food_mark(c, x, y, veg=True, s=1.0, a=1.0):
    """FSSAI-style mark: square outline + green dot (veg) or brown triangle (non-veg)."""
    col = VEG if veg else NON
    h = 15 * s
    c.c.new_path(); c.c.set_source_rgba(1, 1, 1, a); c.c.rectangle(x - h, y - h, 2 * h, 2 * h); c.c.fill()
    c.c.set_source_rgba(*col, a); c.c.set_line_width(2.6 * s); c.c.rectangle(x - h + 2 * s, y - h + 2 * s, 2 * h - 4 * s, 2 * h - 4 * s); c.c.stroke()
    c.c.new_path()
    if veg:
        c.c.arc(x, y, 6.5 * s, 0, 6.2832); c.c.fill()
    else:
        c.c.move_to(x, y - 7 * s); c.c.line_to(x + 7.5 * s, y + 6 * s); c.c.line_to(x - 7.5 * s, y + 6 * s); c.c.close_path(); c.c.fill()
    c.c.new_path()


def app_head(c, title="Zomato"):
    phone(c, PX, PY, PW, PH)
    c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 76, 12, (0.20, 0.06, 0.08))
    c.font(SANS, 30, True); c.text(X0 + 40, Y0 + 100, title, ZR)


def blur_bar(c, x, y, w, a=1.0):
    c.fill_rrect(x, y, w, 16, 8, (0.30, 0.30, 0.33), a)


# ------------------------------------------------------------------ scenes
def s2(cv, t, d, st):                                     # test: what did you order last week? (recall is hard)
    def world(c):
        c.pill(W / 2, 520, "chhota sa test", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        c.font(SANS, 44, True)
        for i, ln in enumerate(["Pichhle hafte", "kya mangaaya tha?"]):
            c.text(W / 2 - c.text_w(ln) / 2, 640 + i * 60, ln, DOT)
        for j in range(3):
            k = ease(min(1, max(0, (t - 1.0 - j * 0.4) / 0.4)))
            if k <= 0: continue
            y = 820 + j * 130
            c.fill_rrect(W / 2 - 300, y, 600, 100, 18, CARD, k)
            c.font(MONO, 34, True); c.text(W / 2 - 270, y + 62, f"{j + 1}.", DIM, k)
            c.dots_path([(W / 2 - 200, y + 70), (W / 2 + 220, y + 70)], spacing=12, r=2.5, col=GREY, a=k)
            c.font(SANS, 52, True); c.text(W / 2 + 230, y + 70, "?", YELLOW, k * (0.6 + 0.4 * math.sin(t * 5 + j)))
        if t > 3.2: white_pill(c, W / 2, 1300, "sochna pad raha hai na?", 38)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.1), (d - 0.4, (W / 2, 900), 1.0)), seed=3)
    hud(cv)


HIST = [("Paneer Biryani", True, "₹249"), ("Butter Chicken", False, "₹329"), ("Masala Dosa", True, "₹149")]
def s3(cv, t, d, st):                                     # order history → "arre haan!" — recognising takes a second
    def world(c):
        app_head(c, "Order history")
        for j, (name, veg, price) in enumerate(HIST):
            k = ease(min(1, max(0, (t - 0.3 - j * 0.25) / 0.35)))
            if k <= 0: continue
            y = Y0 + 170 + j * 130
            c.fill_rrect(X0 + 24, y, PW - 48, 110, 16, CARD, k)
            food_mark(c, X0 + 64, y + 42, veg, 1.0, k)
            c.font(SANS, 28, True); c.text(X0 + 96, y + 52, name, DOT, k)
            c.font(SANS, 22, True); c.text(X0 + 96, y + 88, price + "  ·  delivered", DIM, k)
        if t > 1.6:
            c.pill(PX, Y0 + 610, "arre haan, yahi tha!", size=32, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 3.0:
            c.fill_rrect(X0 + 24, Y0 + 680, PW - 48, 150, 18, (0.08, 0.08, 0.09))
            c.font(SANS, 24, True); c.text(X0 + 50, Y0 + 730, "yaad karna", DIM)
            c.font(SANS, 24, True); c.text(X0 + 50, Y0 + 790, "pehchaanna", DOT)
            c.fill_rrect(X0 + 210, Y0 + 712, 200, 22, 11, RED); c.fill_rrect(X0 + 210, Y0 + 772, 24, 22, 11, GREEN)
            c.font(MONO, 22, True); c.text(X0 + 244, Y0 + 791, "1 sec", GREEN)
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + 420), 1.1), (2.8, (PX, Y0 + 520), 1.0), (d - 0.4, (PX, Y0 + 530), 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - 1.6) / 0.12), seed=4)
    hud(cv); flash(cv, t, 1.6, 0.08)


def s4(cv, t, d, st):                                     # law named: don't make users remember — show it so they recognise
    def world(c):
        c.pill(W / 2, 480, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "RECOGNITION", 104, W / 2, 600, ease(1 - t / 0.8), col=ZR)
        dot_text(c, "OVER RECALL", 104, W / 2, 720, ease(1 - (t - 0.2) / 0.8), col=ZR)
        if t > 2.0:
            k = ease(min(1, (t - 2.0) / 0.4))
            c.pill(W / 2 - 200, 900, "yaad mat karwao", size=32, fam=SANS, col=DARK, bg=(0.75, 0.75, 0.78), bold=True, a=k)
        if t > 3.0:
            k = ease(min(1, (t - 3.0) / 0.4))
            c.pill(W / 2 + 220, 900, "saamne dikhao", size=32, fam=SANS, col=DARK, bg=GREEN, bold=True, a=k)
        if t > 4.0: white_pill(c, W / 2, 1040, "user bas pehchaan le", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 660), 1.15), (1.8, (W / 2, 860), 1.0), (d - 0.4, (W / 2, 880), 1.02)), seed=5)
    hud(cv); flash(cv, t, 0.2)


def s5(cv, t, d, st):                                     # same law: veg dot, recent searches, Order Again, icon labels
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("har jagah yahi law") / 2, 560, "har jagah yahi law", ZR)
        cells = [(0.2, "Veg / non-veg dot"), (1.2, "Recent searches"), (2.2, "Order again"), (3.2, "Icon + naam")]
        for j, (at, title) in enumerate(cells):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            cx = W / 2 - 205 + (j % 2) * 410; cy = 640 + (j // 2) * 330
            c.fill_rrect(cx - 190, cy, 380, 300, 24, CARD, k)
            c.font(SANS, 26, True); c.text(cx - c.text_w(title) / 2, cy + 270, title, DOT, k)
            if j == 0:
                food_mark(c, cx - 60, cy + 120, True, 2.2, k); food_mark(c, cx + 60, cy + 120, False, 2.2, k)
            elif j == 1:
                for i, q in enumerate(["biryani", "pizza", "momos"]):
                    c.font(SANS, 24, True); c.text(cx - 150, cy + 60 + i * 56, "›  " + q, DIM, k)
            elif j == 2:
                c.fill_rrect(cx - 130, cy + 90, 260, 70, 35, ZR, k)
                c.font(SANS, 28, True); c.text(cx - c.text_w("Order again") / 2, cy + 135, "Order again", (1, 1, 1), k)
            else:
                for i, (lab, col) in enumerate([("Home", BLUE), ("Search", ORANGE), ("Cart", GREEN)]):
                    x = cx - 115 + i * 115
                    c.fill_rrect(x - 34, cy + 60, 68, 68, 18, col, k)
                    c.font(SANS, 20, True); c.text(x - c.text_w(lab) / 2, cy + 165, lab, DOT, k)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 970), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # recall tires the brain, recognition doesn't
    def world(c):
        lx, rx = W * 0.27, W * 0.73
        for x, lab, col in [(lx, "yaad karna", RED), (rx, "pehchaanna", GREEN)]:
            c.fill_rrect(x - 200, 620, 400, 460, 24, CARD)
            c.font(SANS, 34, True); c.text(x - c.text_w(lab) / 2, 690, lab, col)
        # energy bars: recall drains, recognition stays full
        drain = max(0.12, 1 - t / 2.5)
        for x, lvl, col in [(lx, drain, RED if drain < 0.4 else YELLOW), (rx, 1.0, GREEN)]:
            c.rrect_path(x - 60, 740, 120, 240, 16); c.c.set_source_rgba(*GREY, 1); c.c.set_line_width(3); c.c.stroke()
            hh = 228 * lvl
            c.fill_rrect(x - 54, 974 - hh, 108, hh, 12, col)
        c.font(MONO, 26, True); c.text(lx - c.text_w("thak gaya") / 2, 1040, "thak gaya", DIM)
        c.text(rx - c.text_w("fresh") / 2, 1040, "fresh", DIM)
        if t > 2.6: c.pill(rx, 1160, "dikh gaya → chun liya", size=26, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 3.8: c.pill(lx, 1160, "yaad karna pada → chhod diya", size=22, fam=SANS, col=DARK, bg=RED, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.0), (d - 0.4, (W / 2, 940), 1.02)), seed=7)
    hud(cv)


def s7(cv, t, d, st):                                     # tip: show past picks, keep options visible, suggest instead of an empty box
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("memory par bojh mat daalo") / 2, 560, "memory par bojh mat daalo", ZR)
        # empty box (bad)
        c.rrect_path(W / 2 - 360, 660, 720, 90, 45); c.c.set_source_rgba(*GREY, 1); c.c.set_line_width(2); c.c.stroke()
        c.font(SANS, 28, True); c.text(W / 2 - 320, 716, "Search karo…", DIM)
        if t < 3.4 and int(t * 2) % 2 == 0:
            c.fill_rrect(W / 2 - 145, 690, 4, 36, 2, DOT)
        items = [("pichhla order", 0.8), ("options saamne", 1.8), ("suggestions", 2.8)]
        for j, (lab, at) in enumerate(items):
            if t > at:
                k = ease(min(1, (t - at) / 0.4))
                c.pill(W / 2 - 240 + j * 240, 820, lab, size=26, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True, a=k)
        if t > 3.4:
            for i, (q, veg) in enumerate([("Paneer Biryani", True), ("Butter Chicken", False), ("Masala Dosa", True)]):
                k = ease(min(1, (t - 3.4 - i * 0.15) / 0.35))
                if k <= 0: continue
                y = 900 + i * 100
                c.fill_rrect(W / 2 - 360, y, 720, 84, 16, CARD, k)
                food_mark(c, W / 2 - 310, y + 42, veg, 1.0, k)
                c.font(SANS, 28, True); c.text(W / 2 - 270, y + 52, q, DOT, k)
                c.font(SANS, 22, True); c.text(W / 2 + 200, y + 52, "phir se ›", ZR, k)
    stage.compose(cv, t, d, world, K((0, (W / 2, 820), 1.05), (d - 0.4, (W / 2, 920), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 38 script (docs/scripts/day38.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("हरा डॉट, या लाल डॉट। एक शब्द पढ़े बिना, आप खाना चुन लेते हो। डे थर्टी एट में, आज इस छोटे से निशान का जादू।", "", D.s0, min_dur=4.6,
          sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("चलो एक छोटा सा टेस्ट। बिना फ़ोन देखे बताओ, पिछले हफ़्ते आपने ज़ोमैटो से क्या-क्या मंगाया था? सोचना पड़ रहा है ना?", "", s2,
          min_dur=5.4, whoosh=True, sfx=[(0.0, "pop_hi"), (1.0, "tick"), (1.4, "tick"), (1.8, "tick"), (3.2, "buzz")]),
    Scene("अब ऐप खोलो, ऑर्डर हिस्ट्री देखो। अरे हाँ, यही तो था! याद करना मुश्किल था, पर पहचानना, बस एक सेकंड का काम।", "", s3, min_dur=5.6,
          whoosh=True, sfx=[(0.3, "pop"), (0.55, "pop"), (0.8, "pop"), (1.6, "chime"), (3.0, "ding")]),
    Scene("इसे कहते हैं, रिकग्निशन ओवर रिकॉल। यूज़र से चीज़ें याद मत करवाओ, उसे सामने दिखा दो, ताकि वो बस पहचान ले।", "", s4, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "drop"), (2.0, "pop_lo"), (3.0, "pop_hi"), (4.0, "chime")]),
    Scene("हरा-लाल डॉट, रीसेंट सर्चेस, ऑर्डर अगेन बटन, और आइकॉन के नीचे लिखा नाम, सब यही लॉ है।", "", s5, min_dur=5.2, whoosh=True,
          sfx=[(0.2, "pop"), (1.2, "pop"), (2.2, "pop"), (3.2, "pop"), (4.0, "ding")]),
    Scene("क्योंकि दिमाग़ याद करने में थकता है, पहचानने में नहीं। जो दिख गया, वो चुन लिया। जो याद करना पड़ा, वो छोड़ दिया।", "", s6, min_dur=5.4,
          whoosh=True, sfx=[(0.3, "riser"), (2.6, "chime"), (3.8, "drop")]),
    Scene("तो डिज़ाइनर्स, यूज़र की मेमोरी पर बोझ मत डालो। पिछला चुना हुआ दिखाओ, ऑप्शन सामने रखो, और खाली बॉक्स की जगह, सुझाव दो।", "", s7,
          min_dur=6.0, whoosh=True, sfx=[(0.8, "pop_hi"), (1.8, "pop_hi"), (2.8, "pop_hi"), (3.4, "chime")]),
    Scene("आप ऑर्डर अगेन दबाते हो, या हर बार पूरा मेन्यू देखते हो? कमेंट में अगेन या मेन्यू लिखो। और कल, वो एक नाम, जो आपको ग़लत इंसान को पैसे भेजने से बचा लेता है।", "", D.s8,
          min_dur=5.6, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = [9.26, 18.24, 27.42, 36.25, 43.46, 51.76, 61.5]

if __name__ == "__main__":
    import daily
    daily.run(38, "Recognition over Recall", SCENES, "day38_recognition_over_recall", cuts=VO_CUTS)

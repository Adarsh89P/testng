"""Day 26/45 · Banner Blindness, explained with the promo carousels people skip.

Anything that looks like an ad gets ignored. Eye-tracking shows gaze going straight to the search bar and products,
skipping the big rotating banner, so nobody remembers what it said. The trap: an important message (delivery delay,
payment failed) styled like a flashy banner gets skipped too; good apps show it like content, plain and in the flow.
Day 02 pattern; the script opens with a memory test the viewer fails. Voice: Rakhi's Day 26 ElevenLabs Tisha K file at
assets/voice/day26/full.mp3 (content-verified); script in docs/scripts/day26.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 26, "Scarcity"
W, H = 1080, 1920
HOT = (1.0, 0.30, 0.45)                           # promo pink
HEAT = [(0.20, 0.40, 1.0), (0.20, 0.85, 0.40), (1.0, 0.85, 0.15), (1.0, 0.35, 0.15)]
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
PROMOS = [("MEGA SALE", "upto 70% OFF", (0.85, 0.20, 0.45)), ("FESTIVE DHAMAKA", "Extra 10% off", (0.95, 0.55, 0.10)),
          ("NEW LAUNCH", "Shop now ›", (0.45, 0.25, 0.85))]
BANNER = (X0 + 20, Y0 + 200, PW - 40, 200)        # banner rect inside the phone


def banner(c, t, a=1.0, text=None, col=None):
    x, y, w, h = BANNER
    if text:
        c.fill_rrect(x, y, w, h, 18, col, a)
        c.font(SANS, 34, True); c.text(x + 30, y + 90, text[0], (1, 1, 1), a)
        c.font(SANS, 24, True); c.text(x + 30, y + 140, text[1], (1, 1, 1), a)
        return
    i = int(t / 1.2) % 3
    nm, sub, cc = PROMOS[i]
    c.fill_rrect(x, y, w, h, 18, cc, a)
    for k in range(6): c._dot(x + w - 60 - (k * 37) % 120, y + 30 + (k * 53) % 140, 10 + k % 3 * 6, (1, 1, 1), 0.25 * a)
    c.font(SANS, 36, True); c.text(x + 30, y + 92, nm, (1, 1, 1), a)
    c.font(SANS, 24, True); c.text(x + 30, y + 142, sub, (1, 1, 1), a)
    for k in range(3):
        c.c.new_path(); c.c.set_source_rgba(1, 1, 1, (1 if k == i else 0.4) * a); c.c.arc(x + w / 2 - 20 + k * 20, y + h - 18, 5, 0, 6.2832); c.c.fill()


def shop(c, t, a=1.0, banner_fn=None):
    phone(c, PX, PY, PW, PH)
    c.font(SANS, 28, True); c.text(X0 + 26, Y0 + 92, "ShopKart", DOT, a)
    c.fill_rrect(X0 + 20, Y0 + 120, PW - 40, 60, 30, (0.20, 0.20, 0.22), a)
    c.dellipse(X0 + 56, Y0 + 150, 12, 12, spacing=4, r=1.6, col=DIM, a=a)
    c.font(SANS, 20, True); c.text(X0 + 80, Y0 + 158, "Search for products", DIM, a)
    (banner_fn or (lambda: banner(c, t, a)))()
    for i in range(2):
        for j in range(2):
            x = X0 + 20 + j * 225; y = Y0 + 430 + i * 215
            c.fill_rrect(x, y, 215, 200, 14, CARD, a)
            c.fill_rrect(x + 12, y + 12, 191, 110, 10, tuple(0.2 + cc * 0.35 for cc in COLS[(i * 2 + j + 2) % 6]), a)
            c.dbar(x + 12, y + 140, 150, rows=1, gap=6, col=DOT)
            c.font(SANS, 20, True); c.text(x + 12, y + 182, "₹" + str(399 + (i * 2 + j) * 250), DOT, a)


def heat(c, x, y, r, k, a=1.0):
    for j, col in enumerate(HEAT):
        rr = r * (1 - j * 0.22) * k
        c.c.new_path(); c.c.set_source_rgba(*col, 0.15 * a); c.c.arc(x, y, max(1, rr), 0, 6.2832); c.c.fill()


# ------------------------------------------------------------------ scenes
HIDE = 3.4
def s1(cv, t, d, st):                                     # memory test: what did the top banner say?
    def world(c):
        shop(c, t)
        if t > HIDE:
            k = ease(min(1, (t - HIDE) / 0.5))
            x, y, w, h = BANNER
            c.fill_rrect(x, y, w, h, 18, (0.10, 0.10, 0.11), k)
            c.font(SANS, 100, True); c.text(PX - 26, y + 140, "?", YELLOW, k)
            c.pill(PX, Y0 + PH + 70, "us par kya likha tha?", size=32, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > HIDE + 1.4: white_pill(c, W / 2, Y0 + PH + 150, "yaad nahi na?", 38)
        if t < HIDE: c.pill(PX + 285, Y0 + 300, "bada, rangeen", size=24, fam=MONO, col=DOT)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX + 60, Y0 + 330), 1.25), (HIDE, (PX + 60, Y0 + 330), 1.25),
                                     (d - 0.4, (PX, PY + 60), 0.95)), punch=0.05 * max(0, 1 - abs(t - HIDE) / 0.12), seed=2)
    hud(cv); flash(cv, t, HIDE, 0.08)


def s2(cv, t, d, st):                                     # eye-tracking: gaze to search + products, banner skipped
    SPOTS = [(X0 + 200, Y0 + 150, 120), (X0 + 120, Y0 + 500, 110), (X0 + 345, Y0 + 500, 100), (X0 + 120, Y0 + 720, 90),
             (X0 + 345, Y0 + 715, 80)]
    def world(c):
        shop(c, t)
        for i, (x, y, r) in enumerate(SPOTS):
            at = 0.8 + i * 0.45
            if t > at: heat(c, x, y, r, ease(min(1, (t - at) / 0.5)))
        n = sum(1 for i in range(len(SPOTS)) if t > 0.8 + i * 0.45)
        if n > 1: c.dots_path([(x, y) for x, y, _ in SPOTS[:n]], spacing=12, r=3, col=(1, 1, 1), a=0.9)
        c.pill(PX + 275, Y0 + 120, "eye-tracking", size=24, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t > 3.2:
            x, y, w, h = BANNER
            c.rrect_path(x - 6, y - 6, w + 12, h + 12, 22); c.c.set_source_rgba(*RED, 1); c.c.set_line_width(3); c.c.stroke()
            c.pill(PX + 275, y + 100, "banner: 0 nazar", size=24, fam=SANS, col=DARK, bg=RED, bold=True)
    stage.compose(cv, t, d, world, K((0, (PX, PY), 0.95), (0.8, (PX + 60, Y0 + 420), 1.15), (d - 0.4, (PX + 60, Y0 + 430), 1.12)),
                  seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # law named: ad-looking things get ignored automatically
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "BANNER", 124, W / 2, 620, ease(1 - t / 0.8), col=HOT)
        dot_text(c, "BLINDNESS", 106, W / 2, 750, ease(1 - (t - 0.2) / 0.8), col=HOT)
        fade = ease(min(1, max(0, (t - 2.6) / 1.0)))
        for i, (nm, sub, cc) in enumerate(PROMOS):
            k = ease(min(1, max(0, (t - 1.2 - i * 0.3) / 0.4)))
            col = tuple(cc[j] + (0.25 - cc[j]) * fade for j in range(3))
            x = W / 2 - 420 + i * 290
            c.fill_rrect(x, 900, 260, 150, 16, col, k)
            c.font(SANS, 22, True); c.text(x + 20, 960, nm, (1, 1, 1), k * (1 - 0.7 * fade))
        if t > 2.6:
            hx = W / 2
            c.dellipse(hx, 1220, 90, 50, spacing=6, r=2.4, col=DOT)
            c.c.new_path(); c.c.set_source_rgba(*DOT, 1); c.c.arc(hx, 1220, 22, 0, 6.2832); c.c.fill()
            c.dots_path([(hx - 110, 1290), (hx + 110, 1150)], spacing=6, r=3, col=RED)
        if t > 3.6: c.pill(W / 2, 1400, "ad jaisa dikha = andekha", size=30, fam=MONO, col=DARK, bg=HOT, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1060), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


SKIP = 2.4
def s4(cv, t, d, st):                                     # trap: important message styled like a banner → skipped too
    def world(c):
        shop(c, t, banner_fn=lambda: banner(c, t, text=("PAYMENT FAILED!", "Order hold par hai · retry karo"), col=(0.95, 0.30, 0.30)))
        if t > 1.2: c.pill(PX + 280, Y0 + 300, "zaroori message!", size=24, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > SKIP:
            k = ease(min(1, (t - SKIP) / 1.0))
            pts = [(X0 + 200, Y0 + 150), (X0 + 120 + 80 * k, Y0 + 150 + 350 * k)]
            c.dots_path(pts, spacing=12, r=3, col=(1, 1, 1), a=0.9)
            heat(c, X0 + 200, Y0 + 150, 100, 1.0); heat(c, X0 + 160, Y0 + 500, 100, k)
        if t > SKIP + 1.2:
            c.pill(PX + 300, Y0 + 380, "skip!", size=34, fam=SANS, col=DARK, bg=RED, bold=True)
        if t > SKIP + 2.0: white_pill(c, W / 2, 1660, "user ne dekha hi nahi", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 60, Y0 + 360), 1.2), (d - 0.4, (PX + 60, Y0 + 380), 1.15)),
                  punch=0.04 * max(0, 1 - abs(t - SKIP - 1.2) / 0.12), seed=5)
    hud(cv)


def plain_notice(c, y, k=1.0):
    c.fill_rrect(X0 + 20, y, PW - 40, 120, 14, (0.16, 0.16, 0.18), k)
    c.fill_rrect(X0 + 20, y, 8, 120, 4, YELLOW, k)
    c.c.new_path(); c.c.set_source_rgba(*YELLOW, k); c.c.arc(X0 + 70, y + 60, 18, 0, 6.2832); c.c.fill()
    c.font(SANS, 22, True); c.text(X0 + 64, y + 68, "!", DARK, k)
    c.font(SANS, 22, True); c.text(X0 + 106, y + 52, "Payment fail hua", DOT, k)
    c.font(SANS, 18, True); c.text(X0 + 106, y + 84, "Order hold par hai · Retry ›", DIM, k)


def s5(cv, t, d, st):                                     # good apps: important info looks like content — plain, in place
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 28, True); c.text(X0 + 26, Y0 + 92, "My Orders", DOT)
        k = ease(min(1, max(0, (t - 0.6) / 0.5)))
        plain_notice(c, Y0 + 130, k)
        for i in range(4):
            y = Y0 + 280 + i * 140
            c.fill_rrect(X0 + 20, y, PW - 40, 120, 14, CARD)
            c.fill_rrect(X0 + 36, y + 16, 88, 88, 10, tuple(0.2 + cc * 0.35 for cc in COLS[i % 6]))
            c.dbar(X0 + 140, y + 40, 200, rows=2, gap=10, col=DOT)
        if t > 1.2: heat(c, X0 + 200, Y0 + 190, 110, ease(min(1, (t - 1.2) / 0.6)))
        labels = [("saada", 2.0), ("saaf", 2.6), ("sahi jagah", 3.2)]
        for j, (lab, at) in enumerate(labels):
            if t > at: c.pill(PX + 285, Y0 + 150 + j * 70, lab + " ✓", size=24, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 4.0: white_pill(c, W / 2, 1660, "ad jaisa nahi, content jaisa", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 60, Y0 + 280), 1.25), (d - 0.4, (PX + 60, Y0 + 300), 1.2)),
                  seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # tip: don't make it flashy — put it where users already look
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.6), ("DO", W * 0.73, t >= 2.6)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 200, 660, 400, 200, 18, (0.95, 0.30, 0.30))
        for k in range(5): c._dot(lx + 120 - (k * 41) % 120, 690 + (k * 37) % 140, 10 + k % 3 * 5, (1, 1, 1), 0.3)
        c.font(SANS, 30, True); c.text(lx - 170, 750, "ZAROORI!!!", (1, 1, 1))
        c.font(SANS, 22, True); c.text(lx - 170, 800, "flashy banner", (1, 1, 1))
        c.pill(lx, 920, "flashy = skip ✗", size=24, fam=SANS, col=RED)
        c.fill_rrect(rx - 200, 660, 400, 56, 28, (0.20, 0.20, 0.22))
        c.font(SANS, 18, True); c.text(rx - 160, 696, "Search", DIM)
        c.fill_rrect(rx - 200, 730, 400, 110, 14, (0.16, 0.16, 0.18))
        c.fill_rrect(rx - 200, 730, 8, 110, 4, YELLOW)
        c.font(SANS, 22, True); c.text(rx - 170, 778, "Payment fail hua", DOT)
        c.font(SANS, 18, True); c.text(rx - 170, 810, "Retry ›", DIM)
        if t >= 2.6: heat(c, rx - 60, 760, 90, ease(min(1, (t - 2.6) / 0.6)))
        c.pill(rx, 920, "jahan nazar hai, wahan ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 4.4: white_pill(c, W / 2, 1120, "zaroori ko flashy mat banao", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 820), 1.45), (2.2, (W * 0.27, 820), 1.45), (2.8, (W * 0.73, 820), 1.45),
                                     (4.0, (W * 0.73, 820), 1.45), (4.6, (W / 2, 950), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 26 script (docs/scripts/day26.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी सिक्स। आज आपकी याददाश्त का, एक छोटा सा टेस्ट।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("पिछली बार जब आपने कोई शॉपिंग ऐप खोला, सबसे ऊपर एक बड़ा, रंगीन बैनर घूम रहा था। उस पर क्या लिखा था? याद नहीं ना?", "", s1,
          min_dur=6.0, whoosh=True, sfx=[(1.2, "pop"), (2.4, "pop"), (HIDE, "drop"), (HIDE + 1.4, "ding")]),
    Scene("क्योंकि आपकी आँखों ने, उसे देखा ही नहीं। आई-ट्रैकिंग स्टडीज़ में यही दिखता है, नज़र सीधे सर्च बार और प्रोडक्ट्स पर जाती है, बैनर को छोड़कर।",
          "", s2, min_dur=6.4, whoosh=True, sfx=[(0.8 + i * 0.45, "pop_lo") for i in range(5)] + [(3.2, "buzz")]),
    Scene("इसे कहते हैं, बैनर ब्लाइंडनेस। जो चीज़ भी ऐड जैसी दिखती है, दिमाग़ उसे अपने आप, अनदेखा कर देता है।", "", s3, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "drop")] + [(1.2 + i * 0.3, "pop") for i in range(3)] + [(2.6, "riser"), (3.6, "ding")]),
    Scene("और यहीं गड़बड़ होती है। अगर कोई ज़रूरी मैसेज, जैसे डिलीवरी में देरी, या पेमेंट फ़ेल, चमकीले बैनर में डाल दिया, तो यूज़र उसे भी स्किप कर देगा।",
          "", s4, min_dur=6.6, whoosh=True, sfx=[(1.2, "pop_hi"), (SKIP, "riser"), (SKIP + 1.2, "buzz"), (SKIP + 2.0, "pop_lo")]),
    Scene("इसीलिए अच्छे ऐप्स, ज़रूरी बातें ऐड की तरह नहीं, बल्कि कंटेंट की तरह दिखाते हैं। सादा, साफ़, और सही जगह पर।", "", s5,
          min_dur=5.8, whoosh=True, sfx=[(0.6, "pop"), (1.2, "chime"), (2.0, "pop_hi"), (2.6, "pop_hi"), (3.2, "pop_hi"), (4.0, "ding")]),
    Scene("तो अगली बार कुछ ज़रूरी दिखाना हो, उसे फ़्लैशी मत बनाओ। उसे वहाँ रखो, जहाँ यूज़र पहले से देख रहा है।", "", s6, min_dur=5.6,
          whoosh=True, sfx=[(0.3, "buzz"), (2.8, "pop_hi"), (3.2, "chime"), (4.4, "ding")]),
    Scene("सच बताओ, आज आपने कितने बैनर स्किप किए? कमेंट में लिखो। कल मिलते हैं, स्कार्सिटी के साथ।", "", D.s8, min_dur=5.0,
          whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 26 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each snapped to the quietest point within 0.8 s (all in the silence between sentences); line check 8/8.
VO_CUTS = [5.14, 14.72, 25.34, 33.44, 44.14, 53.52, 61.0]

if __name__ == "__main__":
    import daily
    daily.run(26, "Banner Blindness", SCENES, "day26_banner_blindness", cuts=VO_CUTS)

"""Day 28/45 · Social Proof, explained with Zomato ratings + review counts.

When unsure, we do what others are doing: the golgappa stall with the queue wins; on Zomato 4.2★ with 2,000+ ratings
beats 4.8★ with 12. Apps use Bestseller tags, "X bought", "X viewing now". Fake reviews and numbers get caught and
kill trust, so show real numbers, real people and useful reviews. Day 02 pattern; the script lets the viewer choose
first and names the law from that choice. Voice: Rakhi's Day 28 ElevenLabs Tisha K file at assets/voice/day28/full.mp3
(content-verified); script in docs/scripts/day28.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 28, "Anchoring"
W, H = 1080, 1920
ZOM = (0.89, 0.22, 0.30)                          # Zomato red
STAR = (0.24, 0.70, 0.35)                         # rating-badge green
AMY = (1.0, 0.85, 0.10)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def stall(c, x, y, a=1.0):
    c.fill_rrect(x - 110, y - 40, 220, 120, 12, (0.55, 0.38, 0.20), a)
    c.fill_rrect(x - 130, y - 110, 260, 50, 10, ZOM, a)
    c.font(SANS, 22, True); c.text(x - c.text_w("GOLGAPPE") / 2, y - 76, "GOLGAPPE", (1, 1, 1), a)
    for dx in (-90, 90): c.dots_path([(x + dx, y - 60), (x + dx, y - 40)], spacing=5, r=2, col=DOT, a=a)
    for wx in (x - 70, x + 70):
        c.c.new_path(); c.c.set_source_rgba(*DOT, a); c.c.arc(wx, y + 96, 16, 0, 6.2832); c.c.stroke()
    for k in range(5):
        c.c.new_path(); c.c.set_source_rgba(0.92, 0.80, 0.55, a); c.c.arc(x - 60 + k * 30, y + 10, 11, 0, 6.2832); c.c.fill()


def person(c, x, y, col, a=1.0, s=1.0):
    c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x, y - 22 * s, 11 * s, 0, 6.2832); c.c.fill()
    c.fill_rrect(x - 13 * s, y - 8 * s, 26 * s, 38 * s, 10 * s, col, a)


def badge(c, x, y, rating, a=1.0):
    c.fill_rrect(x, y - 26, 92, 36, 9, STAR, a)
    c.font(SANS, 22, True); c.text(x + 12, y, rating + " ★", (1, 1, 1), a)


def resto(c, x, y, w, name, rating, count, col, a=1.0, hi=0.0):
    c.fill_rrect(x, y, w, 300, 20, CARD, a)
    if hi > 0:
        c.rrect_path(x - 4, y - 4, w + 8, 308, 24); c.c.set_source_rgba(*AMY, hi * a); c.c.set_line_width(4); c.c.stroke()
    c.fill_rrect(x + 16, y + 16, w - 32, 150, 14, col, a)
    c.font(SANS, 26, True); c.text(x + 20, y + 210, name, DOT, a)
    badge(c, x + 20, y + 262, rating, a)
    c.font(SANS, 20, True); c.text(x + 126, y + 258, count, DIM if hi == 0 else AMY, a)


# ------------------------------------------------------------------ scenes
GO = 3.6
def s1(cv, t, d, st):                                     # two golgappa stalls — you pick the one with the queue
    def world(c):
        lx, rx = W * 0.27, W * 0.73
        stall(c, lx, 800); stall(c, rx, 800)
        n = min(8, int(max(0, t - 0.4) * 6))
        for i in range(n): person(c, lx - 40 + (i % 2) * 60, 960 + (i // 2) * 90, COLS[i % 6])
        c.pill(lx, 1380, "lambi line", size=26, fam=MONO, col=DARK, bg=AMY, bold=True)
        c.pill(rx, 1380, "bilkul khaali", size=26, fam=MONO, col=DOT)
        if t > 1.8: c.pill(W / 2, 600, "aap kiske paas jaaoge?", size=34, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t > GO:
            k = ease(min(1, (t - GO) / 0.9))
            x = W / 2 + (lx + 130 - W / 2) * k; y = 1500 - (1500 - 1250) * k
            person(c, x, y, (1, 1, 1), 1, 1.2)
            c.pill(x + 60, y - 30, "aap", size=22, fam=MONO, col=DARK, bg=(1, 1, 1), bold=True)
        if t > GO + 1.1: white_pill(c, W / 2, 1520, "line waale ke paas na?", 38)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 0.95), (d - 0.4, (W / 2, 1040), 0.95)), seed=2)
    hud(cv)


PICK = 3.4
def s2(cv, t, d, st):                                     # Zomato: 4.8★ with 12 vs 4.2★ with 2,000+ → most pick the second
    def world(c):
        c.font(SANS, 40, True); c.text(W / 2 - c.text_w("zomato") / 2, 560, "zomato", ZOM)
        lx, rx = W / 2 - 420, W / 2 + 20
        ka = ease(min(1, max(0, (t - 0.4) / 0.5))); kb = ease(min(1, max(0, (t - 1.4) / 0.5)))
        hl = ease(min(1, max(0, (t - 2.4) / 0.4)))
        resto(c, lx, 640, 400, "Spice Garden", "4.8", "12 ratings", (0.70, 0.40, 0.25), ka, hi=hl)
        resto(c, rx, 640, 400, "Biryani House", "4.2", "2,000+ ratings", (0.45, 0.30, 0.60), kb, hi=hl)
        if t > PICK:
            for i in range(20):
                kk = ease(min(1, max(0, (t - PICK - i * 0.05) / 0.6)))
                to_b = i % 6 != 0
                tx = (rx + 60 + (i % 8) * 40) if to_b else (lx + 60 + (i % 4) * 40)
                ty = 1040 + (i // 8) * 40
                c._dot(W / 2 + (tx - W / 2) * kk, 1500 + (ty - 1500) * kk, 14, COLS[i % 6], 1)
        if t > PICK + 1.4: c.pill(W / 2, 1260, "zyaadatar log: doosra", size=30, fam=SANS, col=DARK, bg=AMY, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.05), (2.2, (W / 2, 850), 1.05), (2.8, (W / 2, 900), 1.15),
                                     (PICK, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 980), 1.0)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # law named: unsure → do what others do
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "SOCIAL", 130, W / 2, 620, ease(1 - t / 0.8), col=ZOM)
        dot_text(c, "PROOF", 130, W / 2, 760, ease(1 - (t - 0.2) / 0.8), col=ZOM)
        k = min(1, max(0, (t - 1.4) / 2.4))
        for i in range(24):
            ox = W / 2 - 380 + (i % 8) * 108; oy = 980 + (i // 8) * 110
            lead = i < 6
            tx = W / 2 + 120 + (i % 6) * 55; ty = 1000 + (i // 6) * 75
            p = min(1, max(0, k * 1.6 - (0 if lead else 0.3 + (i % 8) * 0.05)))
            x = ox + (tx - ox) * p; y = oy + (ty - oy) * p
            person(c, x, y, ZOM if lead else COLS[i % 6], 1, 0.8)
        if t > 2.0: c.dots_path([(W / 2 - 420, 1350), (W / 2 + 420, 1350)], spacing=9, r=3, col=AMY, reveal=min(1, (t - 2.0) / 0.8))
        if t > 3.6: c.pill(W / 2, 1450, "jo baaki log kar rahe hain", size=30, fam=MONO, col=DARK, bg=AMY, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1050), 1.0), (d - 0.4, (W / 2, 1100), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


def s4(cv, t, d, st):                                     # forms: Bestseller tag, "X bought", "X viewing now"
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 26, True); c.text(X0 + 30, Y0 + 90, "Product", DOT)
        c.fill_rrect(X0 + 30, Y0 + 130, PW - 60, 300, 16, CARD)
        c.dellipse(PX, Y0 + 280, 90, 90, spacing=7, r=2.4, col=DOT)
        c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 480, "Wireless Earbuds", DOT)
        c.font(SANS, 36, True); c.text(X0 + 30, Y0 + 530, "₹1,499", DOT)
        items = [("Bestseller", 0.6, lambda y: (c.fill_rrect(X0 + 40, y - 26, 140, 38, 8, ORANGE), c.font(SANS, 20, True),
                                                   c.text(X0 + 54, y, "#1 Bestseller", DARK))),
                 ("bought", 1.6, lambda y: (c.font(SANS, 22, True), c.text(X0 + 30, y, "10K+ bought in past month", DOT))),
                 ("viewing", 2.6, lambda y: (c.font(SANS, 22, True), c.text(X0 + 30, y, "● 23 log abhi dekh rahe hain", ZOM)))]
        ys = [Y0 + 165, Y0 + 590, Y0 + 640]
        for (nm, at, fn), y in zip(items, ys):
            if t > at: fn(y)
        for j, (lab, at) in enumerate([("bestseller tag", 0.6), ("itne logon ne khareeda", 1.6), ("abhi itne log dekh rahe", 2.6)]):
            if t > at: c.pill(PX + 290, Y0 + 220 + j * 90, lab, size=22, fam=SANS, col=DARK, bg=AMY, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 90, Y0 + 420), 1.15), (d - 0.4, (PX + 90, Y0 + 440), 1.12)), seed=5)
    hud(cv)


STAMP = 2.8
def s5(cv, t, d, st):                                     # fake reviews get caught → nobody trusts ratings
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("par yaad rakho") / 2, 560, "par yaad rakho", ZOM)
        for i in range(5):
            k = ease(min(1, max(0, (t - 0.3 - i * 0.3) / 0.4)))
            y = 660 + i * 130
            c.fill_rrect(W / 2 - 380, y, 760, 110, 16, CARD, k)
            c.font(SANS, 24, True); c.text(W / 2 - 350, y + 46, "★★★★★  User" + str(1000 + i * 7), YELLOW, k)
            c.font(SANS, 24, True); c.text(W / 2 - 350, y + 86, "Best product!!! Must buy!!!", DOT, k)
        if t > STAMP:
            k = ease(min(1, (t - STAMP) / 0.3))
            c.c.save(); c.c.translate(W / 2, 960); c.c.rotate(-0.25)
            c.rrect_path(-200 * k, -70 * k, 400 * k, 140 * k, 16); c.c.set_source_rgba(*RED, k); c.c.set_line_width(8); c.c.stroke()
            c.font(SANS, int(80 * max(0.2, k)), True); c.text(-c.text_w("NAKLI") / 2, 28 * k, "NAKLI", RED, k)
            c.c.restore()
        if t > STAMP + 0.8:
            tk = 1 - 0.85 * ease(min(1, (t - STAMP - 0.8) / 1.0))
            c.font(MONO, 24, True); c.text(W / 2 - 300, 1340, "rating par bharosa", DIM)
            c.fill_rrect(W / 2 - 300, 1360, 600, 36, 18, (0.20, 0.20, 0.22))
            c.fill_rrect(W / 2 - 300, 1360, max(36, 600 * tk), 36, 18, GREEN if tk > 0.5 else RED)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 1050), 0.98)),
                  punch=0.06 * max(0, 1 - abs(t - STAMP) / 0.12), seed=6)
    hud(cv); flash(cv, t, STAMP, 0.1)


def s6(cv, t, d, st):                                     # tip: real numbers, real people, reviews that say something
    REVIEWS = [("Ravi K.", "2 din pehle", "Biryani mast thi, par raita thoda kam tha."),
               ("Sneha M.", "1 hafta pehle", "Delivery 25 min mein. Packing achhi thi.")]
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("dikhao, par sachcha") / 2, 560, "dikhao, par sachcha", STAR)
        c.fill_rrect(W / 2 - 400, 640, 800, 120, 18, CARD)
        badge(c, W / 2 - 370, 712, "4.2")
        c.font(SANS, 28, True); c.text(W / 2 - 250, 708, "2,134 ratings", DOT)
        for i, (nm, when, txt) in enumerate(REVIEWS):
            k = ease(min(1, max(0, (t - 0.8 - i * 0.6) / 0.4)))
            y = 790 + i * 190
            c.fill_rrect(W / 2 - 400, y, 800, 170, 18, CARD, k)
            c.c.new_path(); c.c.set_source_rgba(*COLS[i + 2], k); c.c.arc(W / 2 - 350, y + 50, 26, 0, 6.2832); c.c.fill()
            c.font(SANS, 26, True); c.text(W / 2 - 310, y + 48, nm, DOT, k)
            c.font(SANS, 20, True); c.text(W / 2 - 310, y + 76, when, DIM, k)
            c.font(SANS, 24, True); c.text(W / 2 - 370, y + 130, txt, DOT, k)
        for j, (lab, at) in enumerate([("asli number", 2.2), ("asli log", 2.7), ("kaam ke review", 3.2)]):
            if t > at: c.pill(W / 2 - 270 + j * 270, 1220, lab + " ✓", size=24, fam=SANS, col=DARK, bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 960), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 28 script (docs/scripts/day28.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी एट। चलो, आज आप ही फ़ैसला करो।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("सड़क पर दो गोलगप्पे वाले। एक के सामने लंबी लाइन, दूसरा बिल्कुल ख़ाली। आप किसके पास जाओगे? सच बताओ, लाइन वाले के पास ना?", "", s1,
          min_dur=6.0, whoosh=True, sfx=[(0.4 + i / 6, "pop_lo") for i in range(8)] + [(1.8, "pop"), (GO, "riser"), (GO + 1.1, "ding")]),
    Scene("अब ज़ोमैटो खोलो। एक रेस्टोरेंट, फ़ोर पॉइंट एट स्टार, पर सिर्फ़ बारह रेटिंग्स। दूसरा, फ़ोर पॉइंट टू स्टार, पर दो हज़ार से ज़्यादा रेटिंग्स। ज़्यादातर लोग, दूसरा चुनते हैं।",
          "", s2, min_dur=7.0, whoosh=True, sfx=[(0.4, "pop"), (1.4, "pop"), (2.4, "pop_hi")] + [(PICK + i * 0.1, "tick") for i in range(10)]
          + [(PICK + 1.4, "chime")]),
    Scene("इसे कहते हैं, सोशल प्रूफ़। जब हमें पक्का नहीं पता, तो हम वही करते हैं, जो बाक़ी लोग कर रहे हैं।", "", s3, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "drop"), (1.4, "riser"), (3.6, "ding")]),
    Scene("इसीलिए ऐप्स में दिखता है, बेस्टसेलर का टैग, इतने लोगों ने ख़रीदा, या अभी इतने लोग ये देख रहे हैं।", "", s4, min_dur=5.4,
          whoosh=True, sfx=[(0.6, "pop_hi"), (1.6, "pop_hi"), (2.6, "pop_hi")]),
    Scene("पर याद रखो, नक़ली रिव्यू और झूठे नंबर, एक दिन पकड़े जाते हैं। और फिर, कोई भी रेटिंग पर भरोसा नहीं करता।", "", s5, min_dur=5.8,
          whoosh=True, sfx=[(0.3 + i * 0.3, "pop") for i in range(5)] + [(STAMP, "buzz"), (STAMP + 0.8, "drop")]),
    Scene("तो सोशल प्रूफ़ दिखाओ, पर सच्चा। असली नंबर, असली लोग, और ऐसे रिव्यू, जो सच में कुछ बताएँ।", "", s6, min_dur=5.6,
          whoosh=True, sfx=[(0.8, "pop"), (1.4, "pop"), (2.2, "pop_hi"), (2.7, "pop_hi"), (3.2, "chime")]),
    Scene("आप स्टार्स देखकर ऑर्डर करते हो, या रिव्यू पढ़कर? कमेंट में बताओ। कल मिलते हैं, एंकरिंग के साथ।", "", D.s8, min_dur=5.0,
          whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 28 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [3.9, 14.0, 27.1, 34.12, 41.78, 50.24, 57.72]

if __name__ == "__main__":
    import daily
    daily.run(28, "Social Proof", SCENES, "day28_social_proof", cuts=VO_CUTS)

"""Day 29/45 · Anchoring, explained with Myntra's strike-through MRP.

The first number we see becomes the anchor we judge everything else by. A plain T-shirt at ₹999 feels a bit costly;
the same ₹999 under a struck-out ₹2,999 (67% off) feels like a deal. Menus do it with one very expensive dish.
Twist: an MRP inflated on purpose is cheating, and users remember. Day 02 pattern; the script opens as a price game.
Voice: Rakhi's Day 29 ElevenLabs Tisha K file at assets/voice/day29/full.mp3 (content-verified); script in
docs/scripts/day29.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 29, "Loss Aversion"
W, H = 1080, 1920
MYN = (0.95, 0.25, 0.42)                          # Myntra pink
OFF = (1.0, 0.55, 0.20)                           # discount orange
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def tshirt(c, x, y, s=1.0, col=(0.30, 0.55, 0.85), a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*col, a)
    pts = [(-60, -70), (-20, -80), (0, -66), (20, -80), (60, -70), (95, -30), (68, -8), (52, -24), (52, 80), (-52, 80),
           (-52, -24), (-68, -8), (-95, -30)]
    c.c.move_to(x + pts[0][0] * s, y + pts[0][1] * s)
    for px, py in pts[1:]: c.c.line_to(x + px * s, y + py * s)
    c.c.close_path(); c.c.fill(); c.c.new_path()


def meter(c, cx, cy, v, a=1.0):
    """Half-dial from 'sasti' (left) to 'mehngi' (right); v in 0..1."""
    c.dellipse(cx, cy, 220, 220, a0=180, a1=360, spacing=8, r=2.6, col=DOT, a=a)
    ang = math.pi + v * math.pi
    c.dots_path([(cx, cy), (cx + math.cos(ang) * 190, cy + math.sin(ang) * 190)], spacing=6, r=4, col=YELLOW, a=a)
    c.c.new_path(); c.c.set_source_rgba(*YELLOW, a); c.c.arc(cx, cy, 14, 0, 6.2832); c.c.fill()
    c.font(SANS, 26, True); c.text(cx - 270, cy + 40, "sasti / deal", GREEN, a)
    c.font(SANS, 26, True); c.text(cx + 150, cy + 40, "mehngi", RED, a)


def price_tag(c, x, y, mrp=True, k_mrp=1.0, a=1.0):
    if mrp:
        c.font(SANS, 34, True); w = c.text_w("₹2,999")
        c.text(x, y - 70, "₹2,999", DIM, a * k_mrp)
        c.c.set_source_rgba(*DIM, a * k_mrp); c.c.rectangle(x - 4, y - 84, w + 8, 4); c.c.fill()
        c.font(SANS, 30, True); c.text(x + w + 24, y - 70, "(67% OFF)", OFF, a * k_mrp)
    c.font(SANS, 72, True); c.text(x, y + 10, "₹999", DOT, a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # price game: plain T-shirt at ₹999 — cheap or costly?
    def world(c):
        c.pill(W / 2, 560, "price game", size=32, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        k = ease(min(1, max(0, (t - 0.3) / 0.5)))
        tshirt(c, W / 2, 780, 1.5, a=k)
        c.font(SANS, 80, True); c.text(W / 2 - c.text_w("₹999") / 2, 1010, "₹999", DOT, k)
        v = 0.5 + 0.25 * ease(min(1, max(0, (t - 2.0) / 1.0))) + 0.03 * math.sin(t * 6) * (t < 2.0)
        meter(c, W / 2, 1320, v)
        if t > 1.2: c.pill(W / 2, 1100, "sasti ya mehngi?", size=30, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > 3.2: white_pill(c, W / 2, 1450, "thodi mehngi na?", 38)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 1060), 0.98)), seed=2)
    hud(cv)


FLIP = 2.4
def s2(cv, t, d, st):                                     # same T-shirt on Myntra: struck ₹2,999 above ₹999 → deal!
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 30, True); c.text(X0 + 26, Y0 + 92, "Myntra", MYN)
        c.fill_rrect(X0 + 30, Y0 + 130, PW - 60, 380, 16, (0.92, 0.92, 0.94))
        tshirt(c, PX, Y0 + 320, 1.5)
        c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 560, "Men Solid Cotton T-shirt", DOT)
        price_tag(c, X0 + 30, Y0 + 720, mrp=True, k_mrp=ease(min(1, max(0, (t - 0.8) / 0.5))))
        if t > FLIP:
            v = 0.75 - 0.6 * ease(min(1, (t - FLIP) / 0.8))
            c.c.save(); c.c.translate(PX + 310, PY + 160); c.c.scale(0.55, 0.55)
            meter(c, 0, 0, v); c.c.restore()
        if t > FLIP + 1.2: white_pill(c, W / 2, 1660, "ab? ekdum deal!", 40)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 60, Y0 + 600), 1.15), (d - 0.4, (PX + 80, Y0 + 620), 1.1)),
                  punch=0.05 * max(0, 1 - abs(t - FLIP) / 0.12), seed=3)
    hud(cv); flash(cv, t, FLIP, 0.08)


def anchor_icon(c, x, y, s=1.0, col=DOT, a=1.0):
    c.dellipse(x, y - 70 * s, 16 * s, 16 * s, spacing=5, r=2.4 * s, col=col, a=a)
    c.dots_path([(x, y - 54 * s), (x, y + 60 * s)], spacing=6, r=3 * s, col=col, a=a)
    c.dots_path([(x - 34 * s, y - 30 * s), (x + 34 * s, y - 30 * s)], spacing=6, r=3 * s, col=col, a=a)
    c.dellipse(x, y + 10 * s, 60 * s, 52 * s, a0=20, a1=160, spacing=6, r=3 * s, col=col, a=a)


def s3(cv, t, d, st):                                     # law named: the first number becomes the mind's anchor
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "ANCHORING", 124, W / 2, 640, ease(1 - t / 0.8), col=MYN)
        c.glow(W / 2, 640, 420, 0.07)
        drop = ease(min(1, max(0, (t - 1.2) / 0.8)))
        ax, ay = W / 2 - 280, 820 + 300 * drop
        c.dots_path([(W / 2 - 280, 780), (ax, ay - 70)], spacing=8, r=2.4, col=DIM)
        anchor_icon(c, ax, ay, 1.4, YELLOW)
        if drop >= 1:
            c.font(SANS, 46, True); c.text(W / 2 - 180, 1100, "₹2,999", DOT)
            c.font(SANS, 24, True); c.text(W / 2 - 180, 1140, "pehla number", YELLOW)
        if t > 2.6:
            for j, p in enumerate(["₹1,499", "₹999"]):
                c.font(SANS, 40, True); c.text(W / 2 + 120, 1040 + j * 90, p, GREEN)
            c.dots_path([(W / 2 + 60, 1085), (W / 2 + 110, 1030)], spacing=6, r=2.4, col=DIM)
            c.dots_path([(W / 2 + 60, 1085), (W / 2 + 110, 1120)], spacing=6, r=2.4, col=DIM)
            c.pill(W / 2 + 230, 1210, "usi se taulte hain", size=24, fam=MONO, col=DOT)
        if t > 3.8: c.pill(W / 2, 1360, "pehla number = dimaag ka langar", size=30, fam=MONO, col=DARK, bg=YELLOW, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.2), (1.2, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1060), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


def s4(cv, t, d, st):                                     # restaurant menu: one very expensive dish makes the rest look cheap
    DISHES = [("Royal Lobster Thali", "₹2,499", True), ("Paneer Butter Masala", "₹349", False), ("Dal Makhani", "₹299", False),
              ("Chicken Biryani", "₹399", False), ("Butter Naan", "₹69", False)]
    def world(c):
        c.fill_rrect(W / 2 - 400, 560, 800, 860, 26, (0.12, 0.10, 0.08))
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("MENU") / 2, 650, "MENU", (0.95, 0.85, 0.60))
        for i, (nm, pr, big) in enumerate(DISHES):
            k = ease(min(1, max(0, (t - 0.3 - i * 0.3) / 0.4)))
            y = 760 + i * 120
            c.font(SANS, 30, True); c.text(W / 2 - 350, y, nm, (1.0, 0.80, 0.30) if big else DOT, k)
            c.font(SANS, 30, True); c.text(W / 2 + 350 - c.text_w(pr), y, pr, (1.0, 0.80, 0.30) if big else DOT, k)
            if big and t > 2.0:
                c.rrect_path(W / 2 - 370, y - 46, 740, 70, 14); c.c.set_source_rgba(1.0, 0.80, 0.30, 1); c.c.set_line_width(3); c.c.stroke()
                c.pill(W / 2 + 250, y - 70, "kam hi koi order karta", size=20, fam=MONO, col=DARK, bg=(1.0, 0.80, 0.30), bold=True)
            if not big and t > 3.0 + i * 0.25:
                c.pill(W / 2 + 140, y - 10, "sasti lagi ✓", size=20, fam=SANS, col=DARK, bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (2.0, (W / 2, 820), 1.2), (2.8, (W / 2, 990), 1.0),
                                     (d - 0.4, (W / 2, 1010), 1.0)), seed=5)
    hud(cv)


EDIT = 1.2
def s5(cv, t, d, st):                                     # trap: MRP inflated on purpose = cheating, and users remember
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("par dhyaan rahe") / 2, 560, "par dhyaan rahe", MYN)
        c.fill_rrect(W / 2 - 300, 660, 600, 360, 24, CARD)
        c.font(SANS, 30, True); c.text(W / 2 - 250, 740, "MRP", DIM)
        k = ease(min(1, max(0, (t - EDIT) / 0.8)))
        old, new = "₹999", "₹2,999"
        c.font(SANS, 70, True)
        if k < 0.5: c.text(W / 2 - 250, 850, old, DOT, 1 - k * 2)
        else: c.text(W / 2 - 250, 850, new, RED, (k - 0.5) * 2)
        if EDIT - 0.2 < t < EDIT + 1.0:
            px_ = W / 2 + 120 - 200 * k
            c.dots_path([(px_, 860), (px_ + 70, 760)], spacing=6, r=4, col=YELLOW)
        c.font(SANS, 26, True); c.text(W / 2 - 250, 960, "→ phir '67% OFF'", DIM)
        if t > 2.4:
            ks = ease(min(1, (t - 2.4) / 0.3))
            c.c.save(); c.c.translate(W / 2, 1180); c.c.rotate(-0.2)
            c.rrect_path(-210 * ks, -70 * ks, 420 * ks, 140 * ks, 16); c.c.set_source_rgba(*RED, ks); c.c.set_line_width(8); c.c.stroke()
            c.font(SANS, int(76 * max(0.2, ks)), True); c.text(-c.text_w("DHOKHA") / 2, 26 * ks, "DHOKHA", RED, ks)
            c.c.restore()
        if t > 3.6: white_pill(c, W / 2, 1400, "user ye yaad rakhta hai", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 1040), 1.0)),
                  punch=0.06 * max(0, 1 - abs(t - 2.4) / 0.12), seed=6)
    hud(cv); flash(cv, t, 2.4, 0.1)


def s6(cv, t, d, st):                                     # tip: which number will they see first? make it honest
    def world(c):
        c.font(SANS, 44, True); c.text(W / 2 - c.text_w("pehla number kaun sa?") / 2, 560, "pehla number kaun sa?", YELLOW)
        hx, hy = W / 2, 760
        c.dellipse(hx, hy, 110, 60, spacing=6, r=2.6, col=DOT)
        c.c.new_path(); c.c.set_source_rgba(*DOT, 1); c.c.arc(hx, hy, 28, 0, 6.2832); c.c.fill()
        k = ease(min(1, max(0, (t - 0.8) / 0.8)))
        c.dots_path([(hx, hy + 70), (hx, hy + 70 + 160 * k)], spacing=8, r=3, col=YELLOW)
        if k >= 1:
            c.fill_rrect(W / 2 - 300, 1000, 600, 220, 24, CARD)
            c.font(SANS, 34, True); w = c.text_w("₹1,499")
            c.text(W / 2 - 250, 1070, "₹1,499", DIM); c.c.set_source_rgba(*DIM, 1); c.c.rectangle(W / 2 - 254, 1058, w + 8, 4); c.c.fill()
            c.font(SANS, 30, True); c.text(W / 2 - 250 + w + 20, 1070, "(asli MRP)", GREEN)
            c.font(SANS, 64, True); c.text(W / 2 - 250, 1170, "₹999", DOT)
        if t > 2.4: c.pill(W / 2, 1300, "hamesha sachcha number ✓", size=30, fam=SANS, col=DARK, bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 800), 1.1), (d - 0.4, (W / 2, 1000), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 29 script (docs/scripts/day29.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी नाइन। आज एक छोटा सा प्राइस गेम खेलते हैं।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("एक सादी सी टी-शर्ट, नौ सौ निन्यानवे रुपये। सस्ती लगी, या महँगी? थोड़ी महँगी ना?", "", s1, min_dur=5.0, whoosh=True,
          sfx=[(0.3, "pop"), (1.2, "pop_hi"), (2.0, "riser"), (3.2, "ding")]),
    Scene("अब वही टी-शर्ट, मिंत्रा पर। ऊपर कटा हुआ, दो हज़ार नौ सौ निन्यानवे, और नीचे, नौ सौ निन्यानवे। सिक्सटी सेवन परसेंट ऑफ़। अब? एकदम डील लगी ना?",
          "", s2, min_dur=6.6, whoosh=True, sfx=[(0.8, "pop"), (FLIP, "riser"), (FLIP + 0.8, "chime"), (FLIP + 1.2, "ding")]),
    Scene("इसे कहते हैं, एंकरिंग। जो नंबर हम सबसे पहले देखते हैं, बाक़ी सब उसी से तौलते हैं। वो पहला नंबर, दिमाग़ का लंगर बन जाता है।", "", s3,
          min_dur=6.4, whoosh=True, sfx=[(0.2, "drop"), (1.2, "riser"), (2.0, "drop"), (2.6, "pop"), (3.8, "ding")]),
    Scene("रेस्टोरेंट के मेन्यू में भी, अक्सर एक बहुत महँगी डिश होती है। उसे कोई कम ही ऑर्डर करता है, पर उसके बग़ल में, बाक़ी डिशेज़ सस्ती लगने लगती हैं।",
          "", s4, min_dur=6.8, whoosh=True, sfx=[(0.3 + i * 0.3, "pop_lo") for i in range(5)] + [(2.0, "pop_hi")]
          + [(3.25 + i * 0.25, "pop") for i in range(4)]),
    Scene("पर ध्यान रहे। अगर एम आर पी जानबूझकर बढ़ाकर लिखी हो, तो ये ट्रिक नहीं, धोखा है। और यूज़र ये बात याद रखता है।", "", s5, min_dur=5.6,
          whoosh=True, sfx=[(EDIT, "riser"), (2.4, "buzz"), (3.6, "pop_lo")]),
    Scene("तो जब भी प्राइस दिखाओ, सोचो, यूज़र सबसे पहले कौन सा नंबर देखेगा। और वो नंबर, हमेशा सच्चा होना चाहिए।", "", s6, min_dur=5.4,
          whoosh=True, sfx=[(0.8, "riser"), (1.6, "pop"), (2.4, "chime")]),
    Scene("आपकी सबसे बड़ी सेल वाली ख़रीदारी कौन सी थी? कमेंट में बताओ। कल मिलते हैं, लॉस अवर्ज़न के साथ।", "", D.s8, min_dur=5.0,
          whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 29 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [4.0, 11.4, 24.18, 34.5, 44.25, 53.8, 62.56]

if __name__ == "__main__":
    import daily
    daily.run(29, "Anchoring", SCENES, "day29_anchoring", cuts=VO_CUTS)

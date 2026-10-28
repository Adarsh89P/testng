"""Day 15/45 · Law of Proximity, explained with an Amazon product page.

Things placed close together are read as one group. A scattered product page (price at the top, offer somewhere
below, delivery in a far corner) makes the eye wander; Amazon keeps price, discount and bank offer together, so the
whole deal reads at a glance. Day 02 pattern. Voice: Rakhi's Day 15 ElevenLabs Tisha K file at
assets/voice/day15/full.mp3 (content-verified); script in docs/scripts/day15.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 15, "Law of Common Region"
W, H = 1080, 1920
AMBER = (1.0, 0.62, 0.10)                         # Amazon-ish amber accent
PINK = (0.95, 0.35, 0.55)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.12, 0.12, 0.14)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def lerp(a, b, k): return a + (b - a) * k


def product(c, y, a=1.0):
    """Dotted headphones product shot + title inside the phone."""
    c.fill_rrect(X0 + 30, y, PW - 60, 230, 16, CARD, a)
    c.dellipse(PX, y + 130, 80, 80, a0=180, a1=360, spacing=6, r=2.6, col=DOT, a=a)
    c.fill_rrect(PX - 100, y + 120, 40, 70, 12, AMBER, a); c.fill_rrect(PX + 60, y + 120, 40, 70, 12, AMBER, a)
    c.font(SANS, 22, True); c.text(X0 + 30, y + 270, "Wireless Headphones", DOT, a)


def price(c, x, y, a=1.0):
    c.font(SANS, 30, True); c.text(x, y, "-40%", RED, a)
    c.font(SANS, 44, True); c.text(x + 90, y + 4, "₹1,199", DOT, a)
    c.font(SANS, 18, True); c.text(x, y + 36, "M.R.P. ₹1,999", DIM, a)


def offer(c, x, y, a=1.0, w=PW - 60):
    c.rrect_path(x, y, w, 64, 12); c.c.set_source_rgba(*GREEN, a); c.c.set_line_width(1.6); c.c.stroke()
    c.font(SANS, 19, True); c.text(x + 16, y + 26, "Bank offer", GREEN, a)
    c.font(SANS, 17, True); c.text(x + 16, y + 50, "10% off · HDFC card", DOT, a)


def delivery(c, x, y, a=1.0):
    c.font(SANS, 19, True); c.text(x, y, "FREE delivery", BLUE, a)
    c.font(SANS, 17, True); c.text(x, y + 24, "Kal, 29 Oct", DOT, a)


def cluster_dots(c, t0, t, cx, cy, n=14, spread=380, gap=170, col_split=True):
    """Scattered dots that drift into two tight groups (proximity = grouping)."""
    k = ease(min(1, max(0, (t - t0) / 1.2)))
    for i in range(n):
        sx = cx + ((i * 97) % 100 - 50) / 50 * spread
        sy = cy + ((i * 61) % 100 - 50) / 50 * spread * 0.45
        g = 0 if i < n // 2 else 1
        j = i % (n // 2)
        tx = cx + (-gap if g == 0 else gap) + (j % 3 - 1) * 38
        ty = cy + (j // 3 - 1) * 38
        col = (BLUE if g == 0 else PINK) if (k > 0.6 and col_split) else DOT
        c._dot(lerp(sx, tx, k), lerp(sy, ty, k), 12, col, 1)
    return k


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: paas-paas = ek group
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "LAW OF PROXIMITY", 92, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=AMBER)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "kya hai?", 980, DOT, 56, chars=int((t - 2.0) * 14))
        if t > 2.8:
            k = cluster_dots(c, 3.4, t, W / 2, 1260)
            if k >= 1:
                for gx, col in [(W / 2 - 170, BLUE), (W / 2 + 170, PINK)]:
                    c.dellipse(gx, 1260, 100, 100, spacing=7, r=1.8, col=col)
                c.pill(W / 2, 1430, "paas-paas = ek group", size=30, fam=MONO, col=DARK, bg=AMBER, bold=True)
        if t > 5.6: c.pill(W / 2, 1560, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=AMBER, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (2.9, (W / 2, 1200), 1.0), (5.4, (W / 2, 1230), 1.02)), seed=2)
    hud(cv); flash(cv, t, 1.2)


def s2(cv, t, d, st):                                     # scattered page: eye zig-zags between price, offer, delivery
    PT, OF, DL = (X0 + 40, Y0 + 140), (X0 + 30, Y0 + 740), (X0 + PW - 180, Y0 + 590)
    def world(c):
        phone(c, PX, PY, PW, PH)
        price(c, *PT)
        product(c, Y0 + 210)
        delivery(c, *DL)
        offer(c, *OF)
        stops = [(PT[0] + 120, PT[1] - 10), (DL[0] + 70, DL[1] - 5), (OF[0] + 120, OF[1] + 30), (PT[0] + 60, PT[1] + 30)]
        k = max(0, (t - 1.0) / 2.6)
        n = min(len(stops) - 1, int(k * (len(stops) - 1)) + 1) if k > 0 else 0
        for i in range(n):
            kk = min(1, k * (len(stops) - 1) - i)
            c.dots_path([stops[i], stops[i + 1]], spacing=10, r=3, col=AMBER, a=0.9, reveal=kk)
        if k > 0:
            j = min(len(stops) - 1, int(k * (len(stops) - 1)))
            ex, ey = stops[j]
            c.c.set_source_rgba(1, 1, 1, 0.9); c.c.arc(ex, ey, 16, 0, 6.3); c.c.set_line_width(3); c.c.stroke()
            c._dot(ex, ey, 6, DOT, 1)
        if t > 1.4: c.pill(PT[0] + 140, PT[1] - 60, "price: upar", size=22, fam=MONO, col=DARK, bg=AMBER, bold=True)
        if t > 2.2: c.pill(DL[0] + 70, DL[1] - 60, "delivery: kone mein", size=22, fam=MONO, col=DARK, bg=AMBER, bold=True)
        if t > 3.0: c.pill(OF[0] + 160, OF[1] + 110, "offer: neeche kahin", size=22, fam=MONO, col=DARK, bg=AMBER, bold=True)
        if t > 4.2: white_pill(c, W / 2, 1640, "aankhein idhar-udhar bhatakti hain", 34)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX, Y0 + 430), 1.2), (d - 0.4, (PX, Y0 + 460), 1.15)),
                  seed=3)
    hud(cv)


SNAP = 1.4
def s3(cv, t, d, st):                                     # Amazon: price + discount + bank offer + delivery together
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 56, 10, (0.08, 0.11, 0.16)); c.font(SANS, 24, True)
        c.text(X0 + 30, Y0 + 88, "amazon.in", DOT)
        product(c, Y0 + 130)
        k = ease(min(1, max(0, (t - 0.4) / (SNAP - 0.4))))
        gy = Y0 + 440
        price(c, X0 + 40, lerp(gy + 230, gy + 40, k))
        offer(c, X0 + 30, lerp(Y0 + 60, gy + 100, k), a=k)
        delivery(c, lerp(X0 + PW - 180, X0 + 40, k), lerp(Y0 + 600, gy + 200, k))
        if t > SNAP:
            kk = ease(min(1, (t - SNAP) / 0.4))
            c.drrect(X0 + 18, gy - 10, PW - 36, 250, 16, spacing=7, r=2, col=AMBER, a=kk)
            c.c.set_source_rgba(1, 1, 1, 0.9 * kk); c.c.arc(X0 + 170, gy + 120, 16, 0, 6.3); c.c.set_line_width(3); c.c.stroke()
        c.fill_rrect(X0 + 30, Y0 + PH - 160, PW - 60, 60, 30, YELLOW); c.font(SANS, 24, True)
        c.text(PX - c.text_w("Add to Cart") / 2, Y0 + PH - 121, "Add to Cart", DARK)
        c.fill_rrect(X0 + 30, Y0 + PH - 90, PW - 60, 60, 30, AMBER)
        c.text(PX - c.text_w("Buy Now") / 2, Y0 + PH - 51, "Buy Now", DARK)
        for i, lab in enumerate(["price", "discount", "bank offer"]):
            if t > SNAP + 0.5 + i * 0.35: c.pill(PX + 330, gy + 40 + i * 80, lab + " ✓", size=24, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > SNAP + 2.4: white_pill(c, W / 2, 1640, "ek nazar mein poori deal", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (SNAP, ANCHOR, 1.0), (SNAP + 0.5, (PX + 110, Y0 + 570), 1.3),
                                     (SNAP + 2.2, (PX + 110, Y0 + 570), 1.3), (SNAP + 2.8, ANCHOR, 1.0), (d - 0.4, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - SNAP) / 0.12), seed=4)
    hud(cv); flash(cv, t, SNAP, 0.1)


def grid(c, cx, cy, gap_k, a=1.0):
    """6x3 dot grid; gap_k opens a gutter between the left and right 3 columns."""
    for r in range(3):
        for col in range(6):
            x = cx + (col - 2.5) * 70 + (gap_k * 90 if col >= 3 else -gap_k * 90)
            y = cy + (r - 1) * 70
            cc = (BLUE if col < 3 else PINK) if gap_k > 0.5 else DOT
            c._dot(x, y, 16, cc, a)


def s4(cv, t, d, st):                                     # law card: judi cheezein paas, alag cheezon mein jagah
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "LAW OF PROXIMITY", 88, W / 2, 630, ease(1 - t / 0.8), col=AMBER)
        l1 = "judi cheezein: paas rakho,"; l2 = "alag cheezein: jagah chhodo"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 34, chars=n); mono(c, l2, 800, AMBER, 34, chars=n - len(l1))
        gk = ease(min(1, max(0, (t - 3.0) / 1.0)))
        grid(c, W / 2, 1120, gk)
        if t > 2.6 and gk < 0.5: c.pill(W / 2, 1320, "1 group?", size=28, fam=MONO, col=DOT)
        if gk >= 1:
            c.pill(W / 2 - 230, 1320, "group 1", size=28, fam=MONO, col=DARK, bg=BLUE, bold=True)
            c.pill(W / 2 + 230, 1320, "group 2", size=28, fam=MONO, col=DARK, bg=PINK, bold=True)
            c.pill(W / 2, 1420, "sirf beech ki jagah ne", size=26, fam=MONO, col=AMBER)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1040), 1.0), (d - 0.4, (W / 2, 1070), 1.03)), seed=5)
    hud(cv); flash(cv, t, 3.0, 0.08)


FADE = 1.6
def s5(cv, t, d, st):                                     # no borders needed: boxes fade, groups stay
    def world(c):
        c.font(SANS, 52, True); c.text(W / 2 - c.text_w("border? zaroorat nahi") / 2, 560, "border? zaroorat nahi", AMBER)
        bk = 1 - ease(min(1, max(0, (t - FADE) / 1.0)))
        groups = [("Price", ["₹1,199", "-40%", "M.R.P. ₹1,999"]), ("Offers", ["Bank offer", "Cashback", "No-cost EMI"]),
                  ("Delivery", ["FREE", "Kal, 29 Oct", "7-day return"])]
        for gi, (title, items) in enumerate(groups):
            y = 700 + gi * 230
            if bk > 0:
                c.rrect_path(W / 2 - 300, y - 30, 600, 190, 16); c.c.set_source_rgba(*GREY, bk); c.c.set_line_width(2); c.c.stroke()
                c.c.set_source_rgba(*GREY, bk); c.c.rectangle(W / 2 - 280, y + 30, 560, 2); c.c.fill()
            c.font(SANS, 26, True); c.text(W / 2 - 270, y + 14, title, AMBER if bk < 0.5 else DOT)
            for i, it in enumerate(items):
                c.font(SANS, 22, True); c.text(W / 2 - 270 + i * 190, y + 90, it, DOT)
        if t > FADE + 1.2: c.pill(W / 2, 1440, "sirf space se group ban gaye", size=30, fam=MONO, col=DARK, bg=AMBER, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (d - 0.4, (W / 2, 1000), 1.0)), seed=6)
    hud(cv)


def form_pair(c, x, y, lab, val, gap_above, gap_below, col=GREY):
    c.font(SANS, 20, True); c.text(x, y, lab, DIM)
    c.rrect_path(x, y + gap_below, 340, 56, 12); c.c.set_source_rgba(*col, 1); c.c.set_line_width(1.6); c.c.stroke()
    c.font(SANS, 20, True); c.text(x + 16, y + gap_below + 36, val, DOT)


def s6(cv, t, d, st):                                     # designer tip: DON'T equal spacing | DO label close to its field
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27 - 170, W * 0.73 - 170
        for i, (lab, val) in enumerate([("Name", "Rahul"), ("Phone", "98765 43210"), ("Pincode", "560001")]):
            form_pair(c, lx, 700 + i * 140, lab, val, 0, 50, RED if t < 2.8 else GREY)
            form_pair(c, rx, 700 + i * 140, lab, val, 0, 14, GREEN if t >= 2.8 else GREY)
        c.pill(W * 0.27, 1160, "label kis field ka? ✗", size=24, fam=SANS, col=RED)
        c.pill(W * 0.73, 1160, "label field ke saath ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "spacing batati hai: kya kiske saath hai", 32)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 15 script (docs/scripts/day15.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे फ़िफ़्टीन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, लॉ ऑफ़ प्रॉक्सिमिटी क्या है? जो चीज़ें पास-पास होती हैं, दिमाग़ उन्हें एक ग्रुप मान लेता है। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.4, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (2.8, "pop_lo"), (3.4, "riser"), (4.6, "chime"),
                                                 (5.6, "pop_hi")]),
    Scene("सोचो, किसी प्रोडक्ट पेज पे, प्राइस ऊपर, ऑफ़र नीचे कहीं, और डिलीवरी बिल्कुल अलग कोने में। आँखें इधर-उधर भटकती रहती हैं।",
          "", s2, min_dur=6.2, whoosh=True, sfx=[(1.4, "pop"), (2.2, "pop"), (3.0, "pop"), (4.2, "buzz")]),
    Scene("अब ऐमज़ॉन पे देखो, प्राइस, डिस्काउंट और बैंक ऑफ़र, सब एक साथ, पास-पास। एक नज़र में पूरी डील समझ आ जाती है।", "", s3,
          min_dur=6.0, whoosh=True, sfx=[(0.4, "riser"), (SNAP, "chime")] + [(SNAP + 0.5 + i * 0.35, "pop_hi") for i in range(3)]
          + [(SNAP + 2.4, "ding")]),
    Scene("यही है लॉ ऑफ़ प्रॉक्सिमिटी। जो चीज़ें आपस में जुड़ी हैं, उन्हें पास रखो, और जो अलग हैं, उनके बीच जगह छोड़ो।", "", s4,
          min_dur=6.4, whoosh=True, sfx=[(0.2, "ding"), (2.6, "pop_lo"), (3.0, "riser"), (4.0, "pop_hi"), (4.3, "pop_hi")]),
    Scene("इसीलिए अच्छे डिज़ाइन में, बॉर्डर या लाइन की ज़रूरत ही नहीं पड़ती, सिर्फ़ स्पेस से ही ग्रुप बन जाते हैं।", "", s5,
          min_dur=6.0, whoosh=True, sfx=[(FADE, "riser"), (FADE + 1.2, "ding")]),
    Scene("डिज़ाइनर टिप, स्पेसिंग को ख़ाली जगह मत समझो, यही बताती है कि क्या किसके साथ है।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 15 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [5.14, 15.64, 25.56, 34.84, 43.42, 50.2, 56.84]

if __name__ == "__main__":
    import daily
    daily.run(15, "Law of Proximity", SCENES, "day15_law_of_proximity", cuts=VO_CUTS)

"""Reel 4b: Zomato ke 3 UX secrets - punchier cut with zoom-ins, dot break/form transitions and LAW cards."""
import sys, math
from engine import *
from fx import Stage, law_card, dot_text, flash, ring
import reel4_zomato_ux as z
from reel4_zomato_ux import (phone, menu, cart_bar, veg_mark, tap, side_pill, ux_box, head, map_screen, route_point,
                             menu_veg, SX0, SY0, SW, SH, PX, PY, PW, PH, MENU, GREEN, RED, nchars, span)

W, H = 1080, 1920
ANCHOR = (PX + PW / 2, PY + PH / 2)
FULL = (0, *ANCHOR, 1.0)
stage = Stage(W, H, ANCHOR)

ADD1 = (SX0 + SW - 78, SY0 + 120 + 128 + 44)        # ADD button of row 1 (scroll 0)
CART = (SX0 + SW / 2, SY0 + SH - 64)
VEG0 = (SX0 + 41, SY0 + 120 + 25)
TOGGLE = (SX0 + SW - 78, SY0 + 56)


def K(*keys):
    """Camera keys helper: (t, (x, y), zoom) -> (t, x, y, zoom)."""
    return [(t, p[0], p[1], zz) for t, p, zz in keys]


# ------------------------------------------------------------------ 0. hook
def s0(cv, t, d, st):
    def world(c):
        phone(c); z.clip_screen(c); menu(c, scroll=20 * t, added=(0,)); cart_bar(c, 1); c.c.restore()
        if t > 3.2: side_pill(c, 760, "sundar UI", x=170, col=DIM)
    stage.compose(cv, t, d, world, K((0, CART, 2.6), (1.4, CART, 2.6), (2.6, ANCHOR, 1.0)), form=0.6, seed=1)
    head(cv, "ZOMATO · UX BREAKDOWN")
    cv.fill_rrect(60, 330, W - 120, 140, 24, BG, 0.92)
    dot_text(cv, "ye yahan KYUN hai?", 64, W / 2, 400, ease(1 - (t - 0.4) / 0.8) if t > 0.4 else 1.0)
    if t > 3.6: white_pill(cv, W / 2, 1650, "45 LPA designer: har pixel ka reason", 26)
    flash(cv, t, 0.0)


# ------------------------------------------------------------------ 1. sticky cart appears (zoom ADD -> cart)
L1 = ["ux #1: sticky 'View Cart' bar", "always visible while scrolling"]
def s1(cv, t, d, st):
    added = (1,) if t >= 1.5 else ()
    sc = max(0, t - 3.4) * 140
    def world(c):
        phone(c); z.clip_screen(c); menu(c, scroll=sc, added=added); cart_bar(c, ease((t - 2.0) / 0.5)); c.c.restore()
        ring(c, *ADD1, t, 1.5, GREEN)
        if t < 2.0: tap(c, ADD1[0], ADD1[1], t, 1.5)
        if t > 3.6: side_pill(c, SY0 + SH - 60, "stays here", col=GOOD)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.0, ADD1, 2.4), (1.9, ADD1, 2.4), (2.6, CART, 2.0),
                                     (3.4, CART, 2.0), (4.2, ANCHOR, 1.0)),
                  punch=0.06 * max(0, 1 - abs(t - 1.55) / 0.15), seed=2)
    head(cv, "UX #1 · Sticky cart"); ux_box(cv, t, L1)


# ------------------------------------------------------------------ 2. Fitts's law
def s2(cv, t, d, st):
    def world(c):
        phone(c); z.clip_screen(c); menu(c, scroll=380, added=(1,), a=0.5); y = cart_bar(c, 1)
        k = ease((t - (d - 2.4)) / 0.8)
        cx, cy = SX0 + SW + 40, SY0 + SH + 60
        for r, col in [(560, BAD), (420, (1.0, 0.8, 0.3)), (300, GOOD)]:
            if k > 0: c.dellipse(cx, cy, r * k, r * k, 180, 270, spacing=9, r=2.4, col=col, a=0.95)
        c.c.restore()
        if k > 0.6:
            side_pill(c, SY0 + 120, "hard to reach", col=BAD, x=170)
            side_pill(c, SY0 + SH - 60, "thumb zone", col=GOOD)
        ring(c, *CART, t, d - 1.3, GOOD)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (d - 2.4, ANCHOR, 1.0), (d - 1.4, (ANCHOR[0], CART[1] - 200), 1.5)), seed=3)
    head(cv, "UX #1 · Sticky cart")
    law_card(cv, t, 0.5, d - 2.5, 1, "FITTS'S LAW", "bada + paas wala target = fast tap",
             "-> isliye cart bar neeche + full width")


# ------------------------------------------------------------------ 3. visibility of status (zoom into bar text)
def s3(cv, t, d, st):
    items = 1 + (t > 1.2) + (t > 2.0)
    def world(c):
        phone(c); z.clip_screen(c)
        menu(c, scroll=380, added=tuple(range(1, 1 + items)), a=0.6)
        y = cart_bar(c, 1, items, 249 + (items - 1) * 180); c.c.restore()
        ring(c, SX0 + 110, y + 34, t, 1.2); ring(c, SX0 + 110, y + 34, t, 2.0)
    stage.compose(cv, t, d, world, K((0, CART, 1.2), (0.8, (SX0 + 130, CART[1]), 2.8), (2.8, (SX0 + 130, CART[1]), 2.8),
                                     (3.4, ANCHOR, 1.0)),
                  punch=0.05 * (max(0, 1 - abs(t - 1.25) / 0.12) + max(0, 1 - abs(t - 2.05) / 0.12)), seed=4)
    head(cv, "UX #1 · Sticky cart")
    law_card(cv, t, 3.3, d - 0.6, 2, "VISIBILITY OF STATUS", "user ko hamesha pata ho kya ho raha hai",
             "Nielsen heuristic #1")


# ------------------------------------------------------------------ 4. veg symbol (text -> symbol, zoom 3x)
L4 = ["ux #2: veg / non-veg symbol"]
def s4(cv, t, d, st):
    text_mode = t < 2.0
    def world(c):
        phone(c); z.clip_screen(c); menu(c, scroll=0, symbols=not text_mode, text_labels=text_mode); c.c.restore()
        if text_mode:
            side_pill(c, 820, "padhna padta hai", col=BAD); side_pill(c, 900, "slow", col=BAD)
        else:
            ring(c, VEG0[0] + 13, VEG0[1], t, 2.1, GREEN)
            side_pill(c, 820, "1 glance", col=GOOD)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.4, (SX0 + 120, SY0 + 160), 1.8), (2.0, (SX0 + 120, SY0 + 160), 1.8),
                                     (2.5, VEG0, 3.4), (3.6, VEG0, 3.4), (4.2, ANCHOR, 1.0)),
                  punch=0.07 * max(0, 1 - abs(t - 2.05) / 0.15), seed=5)
    head(cv, "UX #2 · Veg symbol"); ux_box(cv, t, L4)
    flash(cv, t, 2.0)
    law_card(cv, t, 4.2, d - 0.6, 3, "RECOGNITION > RECALL", "padhna nahi, pehchanna",
             "-> packet wala symbol, sab pehle se jaante hain")


# ------------------------------------------------------------------ 5. pure veg toggle (zoom on toggle)
L5 = ["filter: 'Pure Veg' toggle"]
def s5(cv, t, d, st):
    on = t > 1.4
    def world(c):
        phone(c); z.clip_screen(c)
        if on: menu_veg(c, [i for i, (v, _) in enumerate(MENU) if v])
        else: menu(c, scroll=0)
        c.c.restore()
        tx, ty = TOGGLE[0] - 42, TOGGLE[1] - 22
        c.fill_rrect(tx, ty, 84, 44, 22, GREEN if on else PILL)
        c.c.set_source_rgb(1, 1, 1); c.c.arc(tx + (62 if on else 22), ty + 22, 17, 0, 6.3); c.c.fill()
        if t < 1.8: tap(c, *TOGGLE, t, 1.3)
        ring(c, *TOGGLE, t, 1.4, GREEN)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.9, TOGGLE, 2.6), (2.0, TOGGLE, 2.6), (2.7, ANCHOR, 1.0)),
                  punch=0.06 * max(0, 1 - abs(t - 1.4) / 0.15), seed=6)
    head(cv, "UX #2 · Veg symbol"); ux_box(cv, t, L5)
    law_card(cv, t, 2.8, d - 0.6, 4, "CONSISTENCY", "same symbol + same color, har jagah",
             "Nielsen heuristic #4")


# ------------------------------------------------------------------ 6. live tracking (camera follows rider)
L6 = ["ux #3: live rider tracking + ETA"]
def s6(cv, t, d, st):
    k = min(1, t / max(1, d - 0.6))
    rk = 0.12 + 0.6 * k
    rx, ry = route_point(rk)
    def world(c):
        phone(c); map_screen(c, rk, 14 - int(5 * k), 2)
    zoom = 1.0 + 1.2 * ease(t / 1.2) - 1.2 * ease((t - 3.4) / 0.8)
    stage.compose(cv, t, d, world, [(0, lerp(ANCHOR[0], rx, min(1, zoom - 1)), lerp(ANCHOR[1], ry, min(1, zoom - 1)), zoom)], seed=7)
    head(cv, "UX #3 · Live tracking"); ux_box(cv, t, L6)
    law_card(cv, t, 4.2, d - 0.6, 5, "LABOR ILLUSION", "kaam hota dikhe = wait chhota lage",
             "Buell & Norton, Harvard research")


# ------------------------------------------------------------------ 7. without vs with
def s7(cv, t, d, st):
    sw = 2.6
    def world(c):
        phone(c)
        if t < sw:
            z.clip_screen(c)
            c.font(SANS, 30, True); c.text(SX0 + 80, SY0 + 420, "Order placed ✓", DOT)
            c.font(SANS, 20); c.text(SX0 + 110, SY0 + 470, "We'll update you soon", DIM)
            c.c.restore()
            for i in range(3):
                c.pill(PX + PW + 130, 760 + i * 90, "?", size=30, fam=MONO, col=BAD, a=min(1, max(0, (t - i * 0.5) / 0.3)))
        else:
            map_screen(c, 0.75 + min(0.2, (t - sw) / 12), 9, 2)
            side_pill(c, SY0 + 300, "trust", col=GOOD); side_pill(c, SY0 + 380, "calm", col=GOOD)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (sw - 0.3, ANCHOR, 1.0), (sw + 0.5, (ANCHOR[0], SY0 + 720), 2.0),
                                     (d - 1.0, (ANCHOR[0], SY0 + 720), 2.0), (d - 0.4, ANCHOR, 1.2)), seed=8)
    head(cv, "UX #3 · Live tracking")
    cv.pill(W / 2, 330, "WITHOUT tracking" if t < sw else "WITH tracking", size=30, fam=MONO,
            col=BAD if t < sw else GOOD, bold=True)
    flash(cv, t, sw)


# ------------------------------------------------------------------ 8. recap
LAWS = [("Sticky cart", "FITTS'S LAW"), ("Veg symbol", "RECOGNITION > RECALL"), ("Live tracking", "LABOR ILLUSION")]
def s8(cv, t, d, st):
    def world(c):
        swarm(c, t, 60, 600, 960, 1000, n=260, a=0.5)
    stage.compose(cv, t, d, world, [FULL], brk=0, seed=9)
    head(cv, "45 LPA mindset")
    for i, (ux, law) in enumerate(LAWS):
        t0 = 0.6 + i * 1.3
        if t < t0: continue
        y = 720 + i * 230
        cv.pill(W / 2, y - 60, ux, size=24, fam=MONO, a=min(1, (t - t0) / 0.3))
        dot_text(cv, law, 62, W / 2, y, ease(1 - (t - t0) / 0.6))
    if t > 4.8: white_pill(cv, W / 2, 1520, "next app? comment karo", 28)


SCENES = [
    Scene("ज़ोमैटो पर रोज़ ऑर्डर करते हो, पर कभी सोचा है, ये चीज़ें वहाँ क्यों हैं? पैंतालीस एल पी ए डिज़ाइनर को हर पिक्सेल का रीज़न पता होता है।",
          "Zomato ki ye cheezein wahan KYUN hain?", s0, whoosh=True, min_dur=6.0),
    Scene("पहला, व्यू कार्ट बार। ऐड दबाते ही ये नीचे आ जाता है, और आप कितना भी स्क्रॉल करो, ये वहीं रहता है।",
          "#1: ADD dabao, View Cart bar aata hai, aur WAHIN rehta hai.", s1, type_spans=span(L1), clicks=[1.5], min_dur=6.0, whoosh=True),
    Scene("क्यों? ये है फिट्स लॉ। जो बटन बड़ा हो, और अंगूठे के पास हो, वो सबसे जल्दी टैप होता है। इसलिए कार्ट बार नीचे है, और पूरी चौड़ाई में।",
          "FITTS'S LAW: bada + paas wala button = fast tap.", s2, min_dur=8.5),
    Scene("और इसमें आइटम काउंट और टोटल हमेशा दिखता है। ये नील्सन का पहला रूल है, विज़िबिलिटी ऑफ सिस्टम स्टेटस।",
          "Count + total hamesha visible: VISIBILITY OF STATUS.", s3, clicks=[1.2, 2.0], min_dur=6.6),
    Scene("दूसरा, वेज और नॉन वेज का निशान। टेक्स्ट पढ़ना पड़ता, पर ये सिंबल हर इंडियन पैकेट्स पर पहले से पहचानता है। इसे कहते हैं रिकग्निशन ओवर रिकॉल।",
          "#2: Veg symbol. Padhna nahi, PEHCHANNA: Recognition over Recall.", s4, type_spans=span(L4), min_dur=8.0, whoosh=True),
    Scene("और प्योर वेज टॉगल में भी वही सिंबल और वही कलर। हर जगह एक जैसा, ये है कंसिस्टेंसी।",
          "Pure Veg toggle: same symbol, same color = CONSISTENCY.", s5, type_spans=span(L5), clicks=[1.3], min_dur=6.0),
    Scene("तीसरा, लाइव ट्रैकिंग। राइडर को मैप पर चलता देखकर इंतज़ार छोटा लगता है। हार्वर्ड की रिसर्च इसे लेबर इल्यूज़न कहती है।",
          "#3: Live tracking. Kaam hota dikhe to wait chhota: LABOR ILLUSION.", s6, type_spans=span(L6), min_dur=8.0, whoosh=True),
    Scene("सोचो, अगर सिर्फ ऑर्डर प्लेस्ड लिखा होता, तो आप बार बार ऐप खोलकर चेक करते। ट्रैकिंग से बेचैनी कम होती है।",
          "Sirf 'Order placed' = anxiety. Tracking = TRUST.", s7, min_dur=6.0),
    Scene("तो याद रखो, अच्छा डिज़ाइन सिर्फ सुंदर नहीं होता, हर चीज़ के पीछे एक लॉ होता है। अगला ऐप कौन सा? कमेंट करो, और फॉलो करो।",
          "Har pixel ke peeche ek LAW. Next app? Comment karo!", s8, min_dur=6.5, whoosh=True),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=1800), 1), "s")

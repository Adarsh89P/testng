"""Reel 4: Zomato ke 3 UX secrets - why is this UX here? (dotted style, Hinglish VO baked in).

Generic dotted food-app screens (no brand assets); the app is only named in title/voice for commentary.
"""
import sys, math
from engine import *

W, H = 1080, 1920
CPS = 24
PX, PY, PW, PH = 300, 590, 480, 980          # phone body
SX0, SY0, SW, SH = PX + 22, PY + 70, PW - 44, PH - 110   # screen area
GREEN = (0.25, 0.75, 0.40)
RED = (0.92, 0.27, 0.30)
CART = (0.86, 0.22, 0.28)


def nchars(lines): return sum(len(l) + 1 for l in lines)
def span(lines, start=0.0): return [(start, start + nchars(lines) / CPS)]


def phone(cv, a=1.0):
    cv.drrect(PX, PY, PW, PH, 60, spacing=6.5, r=1.9, a=a)
    cv.drrect(PX + 12, PY + 12, PW - 24, PH - 24, 50, spacing=7.5, r=1.4, col=DIM, a=a)
    cv.drrect(PX + PW / 2 - 50, PY + 30, 100, 22, 11, spacing=5, r=1.5, a=a)


def ux_box(cv, t, lines, start=0.0):
    chars = int(max(0, t - start) * CPS)
    cv.code_box(30, 270, W - 60, 250, lines, chars,
                cursor_on=chars < nchars(lines) or int(t * 2) % 2 == 0)


def head(cv, s):
    cv.pill(W / 2, 205, s, size=30, bold=True)


def clip_screen(cv):
    cv.c.save(); cv.rrect_path(SX0, SY0, SW, SH, 26); cv.c.clip()


def veg_mark(cv, x, y, veg=True, s=1.0, a=1.0):
    col = GREEN if veg else RED
    cv.c.set_source_rgba(*col, a); cv.c.set_line_width(2.4 * s); cv.c.rectangle(x, y, 26 * s, 26 * s); cv.c.stroke()
    if veg:
        cv.c.arc(x + 13 * s, y + 13 * s, 6.5 * s, 0, 6.3)
    else:
        cv.c.move_to(x + 13 * s, y + 5 * s); cv.c.line_to(x + 21 * s, y + 20 * s); cv.c.line_to(x + 5 * s, y + 20 * s); cv.c.close_path()
    cv.c.fill()


MENU = [(True, 0.62), (False, 0.50), (True, 0.70), (True, 0.45), (False, 0.66), (True, 0.55), (False, 0.48),
        (True, 0.60), (True, 0.52), (False, 0.58), (True, 0.64), (True, 0.47)]


def menu(cv, scroll=0.0, added=(), symbols=True, text_labels=False, hi=None, a=1.0):
    """Dotted menu list inside the screen; returns y of each row."""
    top = SY0 + 120 - scroll
    cv.dbar(SX0 + 30, SY0 + 40, SW * 0.55, rows=3, gap=6.5, a=a)            # restaurant name
    cv.dbar(SX0 + 30, SY0 + 76, SW * 0.35, rows=2, gap=6.5, col=DIM, a=a)
    rows = []
    for i, (veg, wfrac) in enumerate(MENU):
        y = top + i * 128
        rows.append(y)
        if y < SY0 - 130 or y > SY0 + SH + 10: continue
        ra = a * (0.25 if hi is not None and i != hi else 1.0)
        if symbols: veg_mark(cv, SX0 + 28, y + 12, veg, a=ra)
        if text_labels:
            cv.font(SANS, 17, True); cv.text(SX0 + 28, y + 30, "Vegetarian" if veg else "Non-vegetarian", DIM, ra)
            cv.dbar(SX0 + 28, y + 48, SW * wfrac * 0.8, rows=3, gap=6.5, a=ra)
        else:
            cv.dbar(SX0 + 70, y + 16, SW * wfrac * 0.7, rows=3, gap=6.5, a=ra)
        cv.dbar(SX0 + 70 if not text_labels else SX0 + 28, y + 64, 60, rows=2, gap=6.5, col=DIM, a=ra)
        bx, by = SX0 + SW - 130, y + 20
        if i in added:
            cv.fill_rrect(bx, by, 104, 48, 10, GREEN, ra)
            cv.font(SANS, 20, True); cv.text(bx + 18, by + 32, "–  1  +", (1, 1, 1), ra)
        else:
            cv.drrect(bx, by, 104, 48, 10, spacing=5.5, r=1.5, col=GREEN, a=ra)
            cv.font(SANS, 20, True); cv.text(bx + 30, by + 32, "ADD", GREEN, ra)
        cv.line(SX0 + 20, y + 118, SX0 + SW - 20, y + 118, (0.18, 0.18, 0.2), 1, ra)
    return rows


def cart_bar(cv, k=1.0, items=1, total=249, a=1.0):
    if k <= 0: return
    h = 92; y = SY0 + SH - (h + 18) * ease(k)
    cv.fill_rrect(SX0 + 14, y, SW - 28, h, 16, CART, a)
    cv.font(SANS, 21, True); cv.text(SX0 + 36, y + 38, f"{items} item{'s' if items > 1 else ''} added", (1, 1, 1), a)
    cv.font(SANS, 18); cv.text(SX0 + 36, y + 66, f"₹{total}", (1, 1, 1), a * 0.85)
    cv.font(SANS, 22, True); cv.text(SX0 + SW - 170, y + 55, "View Cart ›", (1, 1, 1), a)
    return y


def tap(cv, x, y, t, at):
    if 0 <= t - at < 0.4:
        k = (t - at) / 0.4
        cv.c.set_source_rgba(1, 1, 1, 0.5 * (1 - k)); cv.c.arc(x, y, 14 + 34 * k, 0, 6.3); cv.c.fill()
    cv._dot(x, y, 9, (1, 1, 1), 0.85)


def side_pill(cv, y, s, col=DOT, a=1.0, x=None):
    cv.pill(x or (PX + PW + 135), y, s, size=22, fam=MONO, col=col, a=a)


# ------------------------------------------------------------------ 0. hook
L0 = ["// zomato ux breakdown", "why is this UX here?"]
def s0(cv, t, d, st):
    head(cv, "15 LPA vs 45 LPA")
    ux_box(cv, t, L0)
    phone(cv, a=ease(t / 0.8))
    clip_screen(cv); menu(cv, scroll=20 * t, added=(0,)); cart_bar(cv, 1); cv.c.restore()
    side_pill(cv, 760, "15 LPA: sundar UI", a=min(1, t / 1.0), x=170)
    if t > 2.2: white_pill(cv, W / 2, 1640, "45 LPA: har pixel ka reason", 24)

# ------------------------------------------------------------------ 1a. sticky cart appears
L1 = ["ux: sticky 'View Cart' bar", "always visible while scrolling"]
def s1(cv, t, d, st):
    head(cv, "UX #1 · Sticky cart")
    ux_box(cv, t, L1)
    phone(cv)
    added = (1,) if t >= 1.4 else ()
    sc = max(0, t - 2.4) * 120
    clip_screen(cv)
    rows = menu(cv, scroll=sc, added=added)
    cart_bar(cv, ease((t - 1.5) / 0.5))
    cv.c.restore()
    bx, by = SX0 + SW - 78, rows[1] + 44
    if t < 2.2: tap(cv, bx, by, t, 1.3)
    if t > 2.4:
        side_pill(cv, SY0 + SH - 60, "stays here", col=GOOD)
        # scroll indicator
        cv.c.set_source_rgba(1, 1, 1, 0.5); cv.rrect_path(PX + PW - 30, SY0 + 140 + (sc % 400), 6, 90, 3); cv.c.fill()

# ------------------------------------------------------------------ 1b. thumb zone
L2 = ["law: Fitts's Law", "big + near target = fast tap", "zone: bottom = thumb zone"]
def s2(cv, t, d, st):
    head(cv, "UX #1 · Sticky cart")
    ux_box(cv, t, L2)
    phone(cv)
    clip_screen(cv); menu(cv, scroll=380, added=(1,), a=0.5); y = cart_bar(cv, 1)
    k = ease((t - 1.0) / 1.0)
    if k > 0:  # thumb reach arcs from bottom-right
        cx, cy = SX0 + SW + 40, SY0 + SH + 60
        for r, col, lab in [(560, BAD, None), (420, (1.0, 0.8, 0.3), None), (300, GOOD, None)]:
            cv.dellipse(cx, cy, r * k, r * k, 180, 270, spacing=9, r=2.2, col=col, a=0.9)
    cv.c.restore()
    if k > 0.5:
        side_pill(cv, SY0 + 120, "hard to reach", col=BAD, x=170)
        side_pill(cv, SY0 + 470, "ok", col=(1.0, 0.8, 0.3), x=190)
        side_pill(cv, SY0 + SH - 60, "thumb zone", col=GOOD)
    if t > 2.6:
        tap(cv, SX0 + SW - 110, y + 46, t, 2.8)

L3 = ["status: '1 item added · Rs 249'", "user always knows cart state", "checkout: always 1 tap away"]
def s3(cv, t, d, st):
    head(cv, "UX #1 · Sticky cart")
    ux_box(cv, t, L3)
    phone(cv)
    items = 1 + (t > 1.6) + (t > 2.6)
    clip_screen(cv)
    menu(cv, scroll=380, added=tuple(range(1, 1 + items)) if items > 1 else (1,), a=0.6)
    y = cart_bar(cv, 1, items, 249 + (items - 1) * 180)
    cv.c.restore()
    cv.glow(SX0 + 110, y + 34, 90, 0.5 + 0.3 * math.sin(t * 5))
    side_pill(cv, y + 46, "visibility of status", col=GOOD)

# ------------------------------------------------------------------ 2. veg symbol
L4 = ["ux: veg / non-veg symbol", "law: Recognition over Recall", "scan in 1 glance, no reading"]
def s4(cv, t, d, st):
    head(cv, "UX #2 · Veg symbol")
    ux_box(cv, t, L4)
    phone(cv)
    text_mode = t < 2.2
    clip_screen(cv); menu(cv, scroll=0, symbols=not text_mode, text_labels=text_mode); cv.c.restore()
    if text_mode:
        side_pill(cv, 820, "padhna padta hai", col=BAD)
        side_pill(cv, 900, "slow", col=BAD)
    else:
        side_pill(cv, 820, "1 glance", col=GOOD)
        side_pill(cv, 900, "already familiar", col=GOOD)
        veg_mark(cv, 90, 1000, True, 2.4); veg_mark(cv, 90, 1100, False, 2.4)
        cv.font(MONO, 22); cv.text(60, 1200, "packet wala", DIM); cv.text(80, 1230, "symbol", DIM)

L5 = ["filter: 'Pure Veg' toggle", "same symbol everywhere =", "  consistency"]
def s5(cv, t, d, st):
    head(cv, "UX #2 · Veg symbol")
    ux_box(cv, t, L5)
    phone(cv)
    on = t > 1.4
    clip_screen(cv)
    if on:
        keep = [i for i, (v, _) in enumerate(MENU) if v]
        menu_veg(cv, keep)
    else:
        menu(cv, scroll=0)
    cv.c.restore()
    # toggle on top-right of screen
    tx, ty = SX0 + SW - 120, SY0 + 34
    cv.fill_rrect(tx, ty, 84, 44, 22, GREEN if on else PILL)
    cv.c.set_source_rgb(1, 1, 1); cv.c.arc(tx + (62 if on else 22), ty + 22, 17, 0, 6.3); cv.c.fill()
    if t < 1.6: tap(cv, tx + 42, ty + 22, t, 1.3)
    side_pill(cv, ty + 22, "Pure Veg", col=GREEN if on else DIM)


def menu_veg(cv, keep):
    global MENU
    old = MENU
    MENU = [old[i] for i in keep]
    menu(cv, scroll=0)
    MENU = old

# ------------------------------------------------------------------ 3. live tracking
ROUTE = [(SX0 + 70, SY0 + 160), (SX0 + 70, SY0 + 320), (SX0 + 260, SY0 + 320), (SX0 + 260, SY0 + 470),
         (SX0 + SW - 80, SY0 + 470), (SX0 + SW - 80, SY0 + 560)]


def route_point(k):
    segs = list(zip(ROUTE, ROUTE[1:])); L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    d = k * sum(L)
    for (a, b), l in zip(segs, L):
        if d <= l: return (a[0] + (b[0] - a[0]) * d / l, a[1] + (b[1] - a[1]) * d / l)
        d -= l
    return ROUTE[-1]


def map_screen(cv, k, eta, step):
    clip_screen(cv)
    for gx in range(int(SX0) + 30, int(SX0 + SW), 95): cv.dline(gx, SY0 + 100, gx, SY0 + 640, spacing=11, r=1.2, col=(0.3, 0.3, 0.33))
    for gy in range(int(SY0) + 120, int(SY0 + 640), 95): cv.dline(SX0, gy, SX0 + SW, gy, spacing=11, r=1.2, col=(0.3, 0.3, 0.33))
    cv.dots_path(ROUTE, spacing=8, r=2.2)
    # restaurant + home pins
    cv.fill_rrect(ROUTE[0][0] - 16, ROUTE[0][1] - 40, 32, 32, 8, PILL); cv.font(SANS, 18, True); cv.text(ROUTE[0][0] - 7, ROUTE[0][1] - 17, "R", DOT)
    hx, hy = ROUTE[-1]; cv.fill_rrect(hx - 16, hy + 6, 32, 32, 8, GREEN); cv.text(hx - 7, hy + 29, "H", (1, 1, 1))
    rx, ry = route_point(k)
    cv.glow(rx, ry, 50, 0.9); cv._dot(rx, ry, 8, (1, 1, 1), 1)
    # bottom sheet with ETA + steps
    cv.fill_rrect(SX0, SY0 + 640, SW, SH - 640, 22, (0.09, 0.09, 0.1))
    cv.font(SANS, 30, True); cv.text(SX0 + 28, SY0 + 705, f"Arriving in {eta} min", DOT)
    names = ["Placed", "Preparing", "On the way"]
    for i, n in enumerate(names):
        x = SX0 + 40 + i * 140
        on = i <= step
        cv.c.set_source_rgba(*(GOOD if on else DIM), 1); cv.c.arc(x, SY0 + 765, 8, 0, 6.3); cv.c.fill()
        if i < 2: cv.line(x + 10, SY0 + 765, x + 130, SY0 + 765, GOOD if i < step else DIM, 2)
        cv.font(SANS, 16, True); cv.text(x - 20, SY0 + 800, n, DOT if on else DIM)
    cv.c.restore()


L6 = ["ux: live rider tracking + ETA", "law: Labor Illusion", "  (Buell & Norton, Harvard)"]
def s6(cv, t, d, st):
    head(cv, "UX #3 · Live tracking")
    ux_box(cv, t, L6)
    phone(cv)
    k = min(1, t / 9.0)
    map_screen(cv, 0.15 + 0.55 * k, 14 - int(4 * k), 2)
    side_pill(cv, SY0 + 300, "progress dikhta hai", col=GOOD)
    side_pill(cv, SY0 + 380, "wait chhota lagta hai", col=GOOD)

L7 = ["without tracking: 'Order placed'", "  ...anxiety, app khol-khol ke check", "with tracking: trust + calm"]
def s7(cv, t, d, st):
    head(cv, "UX #3 · Live tracking")
    ux_box(cv, t, L7)
    phone(cv)
    if t < 2.4:
        clip_screen(cv)
        cv.font(SANS, 30, True); cv.text(SX0 + 80, SY0 + 420, "Order placed ✓", DOT)
        cv.font(SANS, 20); cv.text(SX0 + 110, SY0 + 470, "We'll update you soon", DIM)
        cv.c.restore()
        for i in range(3):
            cv.pill(PX + PW + 130, 760 + i * 90, "?", size=30, fam=MONO, col=BAD, a=min(1, max(0, (t - i * 0.5) / 0.3)))
    else:
        k = 0.7 + min(0.3, (t - 2.4) / 10)
        map_screen(cv, k, 9, 2)
        side_pill(cv, SY0 + 300, "trust", col=GOOD); side_pill(cv, SY0 + 380, "calm", col=GOOD)

# ------------------------------------------------------------------ 4. recap + CTA
L8 = ["1. sticky cart   -> Fitts's Law", "2. veg symbol   -> Recognition", "3. live tracking -> Labor Illusion"]
def s8(cv, t, d, st):
    head(cv, "45 LPA mindset")
    ux_box(cv, t, L8)
    phone(cv, a=0.5)
    swarm(cv, t, PX + 30, PY + 100, PW - 60, PH - 200, n=180, a=0.5)
    if t > 2.5: white_pill(cv, W / 2, 1640, "next app? comment karo", 26)


SCENES = [
    Scene("ज़ोमैटो पर रोज़ ऑर्डर करते हो, पर कभी सोचा है, ये चीज़ें वहाँ क्यों हैं? पंद्रह एल पी ए डिज़ाइनर को सुंदर यू आई दिखता है, पैंतालीस एल पी ए को हर पिक्सेल का रीज़न।",
          "Zomato ki ye cheezein wahan KYUN hain?", s0, type_spans=span(L0), whoosh=True, min_dur=6.5),
    Scene("पहला, नीचे वाला व्यू कार्ट बार। आइटम ऐड करते ही ये आ जाता है, और आप कितना भी स्क्रॉल करो, ये वहीं रहता है।",
          "#1: View Cart bar. Kitna bhi scroll karo, wahin rehta hai.", s1, type_spans=span(L1), clicks=[1.3], min_dur=5.5),
    Scene("क्यों? क्योंकि नीचे का हिस्सा थंब ज़ोन है, जहाँ अंगूठा आराम से पहुँचता है। फिट्स लॉ कहता है, बड़ा और पास वाला बटन सबसे जल्दी टैप होता है।",
          "Thumb zone + FITTS'S LAW: bada aur paas wala button = fast tap.", s2, type_spans=span(L2), clicks=[2.8], min_dur=6.0),
    Scene("और इसमें आइटम काउंट और टोटल हमेशा दिखता है। यूज़र को हर वक्त पता रहता है कि कार्ट में क्या है, और चेकआउट बस एक टैप दूर है।",
          "Count + total hamesha dikhta hai = VISIBILITY of status.", s3, type_spans=span(L3), clicks=[1.6, 2.6]),
    Scene("दूसरा, वेज और नॉन वेज का छोटा सा निशान। ये वही सिंबल है जो हर इंडियन पैकेट्स पर पहले से देखता है। पढ़ने की ज़रूरत नहीं, एक नज़र में स्कैन। इसे कहते हैं रिकग्निशन ओवर रिकॉल।",
          "#2: Veg symbol. Padhna nahi, PEHCHANNA hai. Recognition over Recall.", s4, type_spans=span(L4), min_dur=6.5),
    Scene("और प्योर वेज टॉगल में भी वही सिंबल और वही कलर। हर जगह एक जैसा, यही है कंसिस्टेंसी।",
          "Pure Veg toggle: same symbol, same color = CONSISTENCY.", s5, type_spans=span(L5), clicks=[1.3]),
    Scene("तीसरा, लाइव ट्रैकिंग। राइडर को मैप पर चलता देखकर इंतज़ार छोटा लगता है। हार्वर्ड की रिसर्च इसे लेबर इल्यूज़न कहती है, जब काम होता दिखता है, तो हम ज़्यादा भरोसा करते हैं।",
          "#3: Live tracking. Kaam hota dikhe to wait chhota lagta hai: LABOR ILLUSION.", s6, type_spans=span(L6), min_dur=8.0),
    Scene("सोचो, अगर सिर्फ ऑर्डर प्लेस्ड लिखा होता, तो आप बार बार ऐप खोलकर चेक करते। ट्रैकिंग से बेचैनी कम होती है, और ऐप पर भरोसा बढ़ता है।",
          "Sirf 'Order placed' = anxiety. Tracking = TRUST.", s7, type_spans=span(L7), min_dur=6.0),
    Scene("तो याद रखो, अच्छा डिज़ाइन सिर्फ सुंदर नहीं होता, हर चीज़ का एक रीज़न होता है। अगला ऐप कौन सा? कमेंट में बताओ, और फॉलो करो।",
          "Har pixel ka REASON. Next app? Comment karo!", s8, type_spans=span(L8), whoosh=True),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=1800), 1), "s")

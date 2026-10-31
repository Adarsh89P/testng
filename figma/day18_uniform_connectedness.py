"""Day 18/45 · Uniform Connectedness, explained with Flipkart's order-tracking stepper.

Elements joined by a line read as one flow, even when they are far apart. Flipkart's order page joins Ordered,
Packed, Shipped and Delivered with one line, so four words read as one journey, and how far the line is filled shows
where the parcel is. Day 02 pattern; the script opens on the "where is my parcel?" moment and names the law later.
Voice: Rakhi's Day 18 ElevenLabs Tisha K file at assets/voice/day18/full.mp3 (content-verified); script in
docs/scripts/day18.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 18, "Law of Prägnanz"
W, H = 1080, 1920
FK = (0.16, 0.45, 0.94)                           # Flipkart blue
FKY = (1.0, 0.85, 0.15)                           # Flipkart yellow
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
STEPS = [("Ordered", "Mon, 27 Oct"), ("Packed", "Tue, 28 Oct"), ("Shipped", "Wed, 29 Oct"), ("Delivered", "Expected Fri")]
SY = [Y0 + 330 + i * 120 for i in range(4)]       # stepper rows inside the phone
LX = X0 + 70                                       # stepper line x


def parcel(c, x, y, s=1.0, a=1.0):
    c.fill_rrect(x - 60 * s, y - 45 * s, 120 * s, 90 * s, 8 * s, (0.72, 0.52, 0.30), a)
    c.c.set_source_rgba(0.55, 0.38, 0.20, a); c.c.rectangle(x - 10 * s, y - 45 * s, 20 * s, 90 * s); c.c.fill()


def truck(c, x, y, a=1.0):
    c.fill_rrect(x - 34, y - 20, 44, 32, 5, FKY, a); c.fill_rrect(x + 10, y - 10, 24, 22, 5, FKY, a)
    for wx in (x - 20, x + 22):
        c.c.new_path(); c.c.set_source_rgba(*DOT, a); c.c.arc(wx, y + 14, 7, 0, 6.2832); c.c.fill()


def stepper(c, line_k=1.0, fill_to=None, a=1.0, labels=True):
    """Vertical order stepper. line_k: how much of the connector is drawn; fill_to: filled progress (rows)."""
    if line_k > 0:
        c.dots_path([(LX, SY[0]), (LX, SY[-1])], spacing=7, r=2.4, col=GREY, a=a, reveal=line_k)
    if fill_to is not None and fill_to > 0:
        yy = SY[0] + (SY[-1] - SY[0]) * min(1, fill_to / 3)
        c.c.new_path(); c.c.set_source_rgba(*GREEN, a); c.c.rectangle(LX - 3, SY[0], 6, yy - SY[0]); c.c.fill()
    for i, (lab, date) in enumerate(STEPS):
        done = fill_to is not None and i <= fill_to + 1e-6
        c.c.new_path(); c.c.set_source_rgba(*(GREEN if done else (0.25, 0.25, 0.28)), a); c.c.arc(LX, SY[i], 14, 0, 6.2832); c.c.fill()
        if done: c.font(SANS, 16, True); c.text(LX - 6, SY[i] + 6, "✓", DARK, a)
        if labels:
            c.font(SANS, 26, True); c.text(LX + 40, SY[i] + 4, lab, DOT if done or fill_to is None else DIM, a)
            c.font(SANS, 17, True); c.text(LX + 40, SY[i] + 32, date, DIM, a)


def fk_page(c):
    phone(c, PX, PY, PW, PH)
    c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 64, 10, FK); c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 94, "Flipkart", (1, 1, 1))
    c.font(SANS, 18, True); c.text(X0 + PW - 140, Y0 + 92, "My Orders", (1, 1, 1))
    c.fill_rrect(X0 + 20, Y0 + 140, PW - 40, 120, 14, CARD)
    parcel(c, X0 + 80, Y0 + 200, 0.6)
    c.font(SANS, 22, True); c.text(X0 + 140, Y0 + 190, "Wireless Earbuds", DOT)
    c.font(SANS, 18, True); c.text(X0 + 140, Y0 + 222, "Order #OD4271  ·  ₹1,499", DIM)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: "mera parcel aakhir hai kahan?"
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 26, True); c.text(X0 + 30, Y0 + 90, "My Orders", DOT)
        parcel(c, PX, Y0 + 330, 1.4)
        for i in range(3):                                # repeated app opens: refresh taps
            at = 0.8 + i * 1.0
            if t > at:
                kk = max(0, 1 - (t - at) / 0.8)
                c.dellipse(PX, Y0 + 330, 120 + 80 * (1 - kk), 120 + 80 * (1 - kk), spacing=8, r=2, col=FK, a=kk)
        # clock hand spinning = hours passing
        cx, cy = PX, Y0 + 600
        c.dellipse(cx, cy, 70, 70, spacing=7, r=2.2, col=DOT)
        ang = t * 2.4
        c.dots_path([(cx, cy), (cx + 50 * math.sin(ang), cy - 50 * math.cos(ang))], spacing=6, r=3, col=FKY)
        c.dots_path([(cx, cy), (cx + 32 * math.sin(ang / 12), cy - 32 * math.cos(ang / 12))], spacing=6, r=3, col=DOT)
        if t > 1.0: c.pill(PX + 330, Y0 + 280, "har ghante check", size=24, fam=MONO, col=DARK, bg=FKY, bold=True)
        for i, (dx, dy) in enumerate([(-150, 200), (150, 230), (0, 150)]):
            if t > 2.2 + i * 0.3: c.font(SANS, 70, True); c.text(PX + dx - 18, Y0 + dy, "?", FKY)
        if t > 3.4: white_pill(c, W / 2, 1640, "mera parcel aakhir hai kahan? 📦", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX, Y0 + 420), 1.25), (d - 0.4, (PX, Y0 + 460), 1.15)), seed=2)
    hud(cv)


LINE = 2.6
def s2(cv, t, d, st):                                     # Flipkart order page: 4 steps, then one line joins them
    def world(c):
        fk_page(c)
        k = ease(min(1, max(0, (t - LINE) / 1.0)))
        for i in range(4):
            kk = ease(min(1, max(0, (t - 0.5 - i * 0.35) / 0.35)))
        n = sum(1 for i in range(4) if t > 0.5 + i * 0.35)
        if n:
            for i, (lab, date) in enumerate(STEPS[:n]):
                c.c.new_path(); c.c.set_source_rgba(0.25, 0.25, 0.28, 1); c.c.arc(LX, SY[i], 14, 0, 6.2832); c.c.fill()
                c.font(SANS, 26, True); c.text(LX + 40, SY[i] + 4, lab, DOT)
                c.font(SANS, 17, True); c.text(LX + 40, SY[i] + 32, date, DIM)
        if k > 0: c.dots_path([(LX, SY[0] + 16), (LX, SY[-1] - 16)], spacing=7, r=2.6, col=FK, reveal=k)
        if t > 1.9: c.pill(PX + 320, SY[1], "4 steps", size=26, fam=MONO, col=DARK, bg=FKY, bold=True)
        if t > LINE + 1.0: c.pill(PX + 320, SY[2] + 20, "+ 1 seedhi line", size=26, fam=MONO, col=(1, 1, 1), bg=FK, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.4, (PX + 60, Y0 + 500), 1.3), (d - 0.4, (PX + 60, Y0 + 520), 1.28)),
                  punch=0.04 * max(0, 1 - abs(t - LINE - 1.0) / 0.12), seed=3)
    hud(cv); flash(cv, t, LINE + 1.0, 0.08)


FILL = 2.4
def s3(cv, t, d, st):                                     # one journey: the line fills up to where the parcel is
    def world(c):
        fk_page(c)
        prog = 2 * ease(min(1, max(0, (t - FILL) / 1.4)))
        stepper(c, 1.0, fill_to=prog)
        ty = SY[0] + (SY[-1] - SY[0]) * prog / 3
        if t > FILL: truck(c, LX + PW - 120, ty)
        if t < FILL:
            k = ease(min(1, t / 0.6))
            c.pill(PX, Y0 + 830, "4 alag shabd? nahi…", size=26, fam=MONO, col=DOT, a=k)
        else:
            c.pill(PX, Y0 + 830, "ek safar →", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > FILL + 1.6: white_pill(c, W / 2, 1640, "line jahan tak bhari, parcel wahin tak", 34)
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + 520), 1.25), (FILL, (PX, Y0 + 520), 1.25), (d - 0.4, (PX, Y0 + 560), 1.15)),
                  seed=4)
    hud(cv); flash(cv, t, FILL + 1.4, 0.06)


THREAD = 3.0
def s4(cv, t, d, st):                                     # law named: a line makes far things one story
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "UNIFORM", 96, W / 2, 610, ease(1 - t / 0.8), col=FK)
        dot_text(c, "CONNECTEDNESS", 80, W / 2, 710, ease(1 - (t - 0.2) / 0.8), col=FK)
        l1 = "line se jude = ek kahani,"; l2 = "chahe door-door hon"
        n = int(max(0, t - 1.0) * 28)
        mono(c, l1, 820, DOT, 34, chars=n); mono(c, l2, 870, FKY, 34, chars=n - len(l1))
        k = ease(min(1, max(0, (t - THREAD) / 0.9)))
        pts = [(W / 2 - 320, 1080), (W / 2 - 220, 1080), (W / 2 + 220, 1300), (W / 2 + 320, 1300)]
        a, b = (W / 2 - 220, 1080), (W / 2 + 220, 1300)
        if k > 0: c.dots_path([a, (W / 2, 1080), (W / 2, 1300), b], spacing=8, r=3, col=FKY, reveal=k)
        for i, p in enumerate(pts):
            linked = p in (a, b) and k >= 1
            c._dot(p[0], p[1], 24, FKY if linked else DOT, 1)
        if k >= 1:
            c.pill(W / 2, 1420, "door hain, phir bhi saath", size=28, fam=MONO, col=DARK, bg=FKY, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.25), (2.2, (W / 2, 1060), 1.0), (d - 0.4, (W / 2, 1080), 1.03)), seed=5)
    hud(cv); flash(cv, t, THREAD + 0.9, 0.06)


def s5(cv, t, d, st):                                     # everyday: metro map, chat reply thread, form steps
    def world(c):
        c.font(SANS, 50, True); c.text(W / 2 - c.text_w("har jagah yahi trick") / 2, 540, "har jagah yahi trick", FKY)
        panels = [("Metro map", 0.4), ("Chat thread", 1.6), ("Form steps", 2.8)]
        for j, (title, at) in enumerate(panels):
            k = ease(min(1, max(0, (t - at) / 0.5)))
            if k <= 0: continue
            y = 640 + j * 280
            c.fill_rrect(W / 2 - 420, y, 840, 250, 22, CARD, k)
            c.font(SANS, 26, True); c.text(W / 2 - 390, y + 46, title, DOT, k)
            r = min(1, max(0, (t - at - 0.3) / 0.8))
            if j == 0:
                for col, yy, xs in [(PINK_, y + 120, [-300, -150, 0, 150, 300]), (FK, y + 190, [-300, -100, 100, 300])]:
                    c.dots_path([(W / 2 + xs[0], yy), (W / 2 + xs[-1], yy)], spacing=6, r=3.4, col=col, a=k, reveal=r)
                    for x in xs:
                        c.c.new_path(); c.c.set_source_rgba(*DOT, k); c.c.arc(W / 2 + x, yy, 11, 0, 6.2832); c.c.fill()
            elif j == 1:
                c.fill_rrect(W / 2 - 360, y + 80, 380, 54, 18, (0.22, 0.22, 0.26), k)
                c.font(SANS, 20, True); c.text(W / 2 - 340, y + 114, "Kal movie chalein?", DOT, k)
                c.fill_rrect(W / 2 - 240, y + 170, 420, 54, 18, (0.10, 0.36, 0.30), k)
                c.font(SANS, 20, True); c.text(W / 2 - 220, y + 204, "↪ Haan! 7 baje?", DOT, k)
                c.dots_path([(W / 2 - 340, y + 136), (W / 2 - 340, y + 197), (W / 2 - 250, y + 197)], spacing=6, r=2.6,
                            col=GREEN, a=k, reveal=r)
            else:
                xs = [-300, -100, 100, 300]
                c.dots_path([(W / 2 + xs[0], y + 150), (W / 2 + xs[-1], y + 150)], spacing=7, r=3, col=FK, a=k, reveal=r)
                for i, x in enumerate(xs):
                    c.c.new_path(); c.c.set_source_rgba(*(FK if r * 3 >= i else (0.25, 0.25, 0.28)), k)
                    c.c.arc(W / 2 + x, y + 150, 24, 0, 6.2832); c.c.fill()
                    c.font(SANS, 22, True); c.text(W / 2 + x - 7, y + 158, str(i + 1), (1, 1, 1), k)
        if t > 4.0: c.pill(W / 2, 1520, "line = ek flow", size=30, fam=MONO, col=DARK, bg=FKY, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.1), (d - 0.4, (W / 2, 1040), 1.0)), seed=6)
    hud(cv)


PINK_ = (0.95, 0.35, 0.55)


def mini_steps(c, cx, y0, joined, col):
    for i, lab in enumerate(["Cart", "Address", "Payment", "Done"]):
        y = y0 + i * 120
        c.c.new_path(); c.c.set_source_rgba(*col, 1); c.c.arc(cx - 110, y, 16, 0, 6.2832); c.c.fill()
        c.font(SANS, 24, True); c.text(cx - 80, y + 9, lab, DOT)
    if joined: c.dots_path([(cx - 110, y0 + 18), (cx - 110, y0 + 3 * 120 - 18)], spacing=7, r=2.8, col=col)


def s6(cv, t, d, st):                                     # designer tip: DON'T loose steps | DO join them with a line
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        mini_steps(c, W * 0.27, 720, False, RED if t < 2.8 else GREY)
        mini_steps(c, W * 0.73, 720, True, GREEN if t >= 2.8 else GREY)
        c.pill(W * 0.27, 1180, "bikhre steps ✗", size=24, fam=SANS, col=RED)
        c.pill(W * 0.73, 1180, "ek line, ek flow ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "steps ko line se jodna mat bhoolna", 34)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 18 script (docs/scripts/day18.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़, और आज है डे एटीन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("आपने ऑनलाइन कुछ ऑर्डर किया, और अब हर घंटे ऐप खोलकर देख रहे हो, मेरा पार्सल आख़िर है कहाँ?", "", s1, min_dur=5.2,
          whoosh=True, sfx=[(0.8, "pop"), (1.8, "pop"), (2.8, "pop"), (2.2, "pop_lo"), (2.5, "pop_lo"), (3.4, "ding")]),
    Scene("फ़्लिपकार्ट का ऑर्डर पेज खोलो। ऑर्डर्ड, पैक्ड, शिप्ड, डिलीवर्ड। चार स्टेप्स, और उन्हें जोड़ती हुई, एक सीधी लाइन।", "", s2,
          min_dur=5.8, whoosh=True, sfx=[(0.5 + i * 0.35, "pop") for i in range(4)] + [(1.9, "pop_hi"), (LINE, "riser"),
                                                                                     (LINE + 1.0, "chime")]),
    Scene("उस एक लाइन की वजह से, ये चार अलग-अलग शब्द नहीं लगते, एक सफ़र लगता है। लाइन जहाँ तक भरी है, आपका पार्सल वहीं तक पहुँचा है।",
          "", s3, min_dur=6.6, whoosh=True, sfx=[(0.3, "pop_lo"), (FILL, "riser"), (FILL + 1.4, "chime"), (FILL + 1.6, "ding")]),
    Scene("इसे कहते हैं, यूनिफ़ॉर्म कनेक्टेडनेस। जो चीज़ें किसी लाइन या धागे से जुड़ी हों, दिमाग़ उन्हें एक ही कहानी मानता है, चाहे वो दूर-दूर क्यों न हों।",
          "", s4, min_dur=6.8, whoosh=True, sfx=[(0.2, "drop"), (THREAD, "riser"), (THREAD + 0.9, "chime")]),
    Scene("मेट्रो का मैप हो, चैट के रिप्लाई थ्रेड हों, या किसी फ़ॉर्म के स्टेप्स, हर जगह यही छोटी सी ट्रिक काम कर रही है।", "", s5,
          min_dur=6.0, whoosh=True, sfx=[(0.4, "pop"), (1.6, "pop"), (2.8, "pop"), (4.0, "ding")]),
    Scene("तो अगली बार कोई स्टेप-बाय-स्टेप फ़्लो डिज़ाइन करो, तो स्टेप्स को एक लाइन से जोड़ना मत भूलना।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("कल डे नाइनटीन पे मिलते हैं, तब तक डिज़ाइन विद राखी को फ़ॉलो कर लो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 18 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each snapped to the quietest point within 0.8 s (all in the silence between sentences); line check 8/8.
VO_CUTS = [5.78, 12.62, 21.6, 31.18, 41.18, 49.24, 55.54]

if __name__ == "__main__":
    import daily
    daily.run(18, "Uniform Connectedness", SCENES, "day18_uniform_connectedness", cuts=VO_CUTS)

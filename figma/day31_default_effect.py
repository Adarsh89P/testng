"""Day 31/45 · Default Effect, explained with the last-used UPI pre-selected at checkout.

Most people keep whatever is pre-selected: few ever change their phone's default ringtone; in the organ-donation
study (Johnson & Goldstein, 2003) opt-out countries have far more donors than opt-in ones. Checkout pre-selects the
UPI you used last time, so paying is one tap. Dark side: pre-ticked insurance or donations nobody asked for. Day 02
pattern; the script opens with an honest-answer question. Voice: Rakhi's Day 31 ElevenLabs Tisha K file at
assets/voice/day31/full.mp3 (content-verified); script in docs/scripts/day31.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 31, "Endowment Effect"
W, H = 1080, 1920
VIO = (0.55, 0.40, 1.0)                           # default-effect accent
PAY = (0.36, 0.20, 0.70)                          # checkout purple
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def radio(c, x, y, on, a=1.0, col=VIO):
    c.c.new_path(); c.c.set_source_rgba(*(col if on else GREY), a); c.c.arc(x, y, 14, 0, 6.2832); c.c.set_line_width(3); c.c.stroke()
    if on: c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x, y, 7, 0, 6.2832); c.c.fill()
    c.c.new_path()


def checkbox(c, x, y, on, a=1.0, col=VIO):
    c.rrect_path(x - 14, y - 14, 28, 28, 6)
    if on: c.c.set_source_rgba(*col, a); c.c.fill(); c.font(SANS, 20, True); c.text(x - 8, y + 8, "✓", (1, 1, 1), a)
    else: c.c.set_source_rgba(*GREY, a); c.c.set_line_width(2); c.c.stroke()
    c.c.new_path()


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # ringtone: ever changed it? most keep what's set
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 28, True); c.text(X0 + 26, Y0 + 92, "Settings  ›  Sound", DOT)
        rows = ["Default ringtone", "Classic Bell", "Marimba", "Sunrise", "Pulse"]
        for i, r in enumerate(rows):
            y = Y0 + 150 + i * 90
            c.fill_rrect(X0 + 20, y, PW - 40, 76, 14, CARD)
            radio(c, X0 + 56, y + 38, i == 0)
            c.font(SANS, 24, True); c.text(X0 + 90, y + 46, r, DOT if i == 0 else DIM)
        if t > 1.0: c.pill(PX + 290, Y0 + 190, "kabhi badli?", size=28, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > 2.6:
            k = ease(min(1, (t - 2.6) / 0.8))
            c.fill_rrect(X0 + 30, Y0 + 640, (PW - 60) * 0.85 * k, 50, 12, VIO)
            c.fill_rrect(X0 + 30, Y0 + 710, (PW - 60) * 0.15 * k, 50, 12, GREY)
            c.font(SANS, 20, True); c.text(X0 + 40, Y0 + 674, "jo set hai, wahi", DARK if k > 0.5 else DOT)
            c.font(SANS, 20, True); c.text(X0 + 40 + (PW - 60) * 0.15 * k + 12, Y0 + 744, "badla", DIM)
        if t > 4.0: white_pill(c, W / 2, 1660, "zyaadatar log: jo pehle se set", 34)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 70, Y0 + 380), 1.15), (d - 0.4, (PX + 60, Y0 + 420), 1.1)), seed=2)
    hud(cv)


def s2(cv, t, d, st):                                     # organ donation: opt-in → few donors; opt-out → almost all
    def panel(c, cx, title, sub, frac, col, at, label):
        k = ease(min(1, max(0, (t - at) / 0.5)))
        c.fill_rrect(cx - 200, 680, 400, 640, 26, CARD, k)
        c.font(SANS, 30, True); c.text(cx - c.text_w(title) / 2, 750, title, DOT, k)
        c.font(SANS, 22, True); c.text(cx - c.text_w(sub) / 2, 790, sub, DIM, k)
        checkbox(c, cx, 870, title == "Opt-out", k)
        g = ease(min(1, max(0, (t - at - 0.6) / 1.0)))
        c.fill_rrect(cx - 60, 1260 - 320 * frac * g, 120, 320 * frac * g, 12, col, k)
        if g >= 1: c.pill(cx, 1300, label, size=24, fam=SANS, col=DARK, bg=col, bold=True)
    def world(c):
        c.pill(W / 2, 580, "ek mashhoor study", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        panel(c, W * 0.27, "Opt-in", "khud 'haan' karo", 0.15, GREY, 0.4, "bahut kam donor")
        panel(c, W * 0.73, "Opt-out", "'haan' pehle se", 0.92, VIO, 1.6, "lagbhag sab")
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 980), 1.15), (1.4, (W * 0.27, 980), 1.15), (2.2, (W / 2, 1000), 1.0),
                                     (d - 0.4, (W / 2, 1020), 1.0)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # law named: people keep the pre-selected option — changing takes effort
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "DEFAULT", 130, W / 2, 630, ease(1 - t / 0.8), col=VIO)
        dot_text(c, "EFFECT", 130, W / 2, 770, ease(1 - (t - 0.2) / 0.8), col=VIO)
        for i, lab in enumerate(["Option A", "Option B", "Option C"]):
            y = 960 + i * 110
            c.fill_rrect(W / 2 - 300, y, 600, 90, 18, (0.20, 0.14, 0.34) if i == 0 else CARD)
            radio(c, W / 2 - 250, y + 45, i == 0)
            c.font(SANS, 30, True); c.text(W / 2 - 210, y + 56, lab + ("  (pehle se)" if i == 0 else ""), DOT if i == 0 else DIM)
        if t > 2.2:
            n = int(min(12, (t - 2.2) * 8))
            for j in range(n): c._dot(W / 2 + 330 + (j % 3) * 30, 990 + (j // 3) * 22, 9, VIO, 1)
            c.pill(W / 2 + 360, 1310, "zyaadatar: wahi rakh lete", size=22, fam=MONO, col=DOT)
        if t > 3.6: c.pill(W / 2, 1420, "badalne mein mehnat lagti hai", size=30, fam=MONO, col=DARK, bg=VIO, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1080), 1.0), (d - 0.4, (W / 2, 1110), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


TAP = 2.8
def s4(cv, t, d, st):                                     # checkout: last-used UPI pre-selected → just tap Pay
    OPTS = [("UPI · rahul@okbank", "pichhli baar use kiya", True), ("Credit / Debit card", "", False),
            ("Net banking", "", False), ("Cash on delivery", "", False)]
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 64, 12, PAY)
        c.font(SANS, 26, True); c.text(X0 + 30, Y0 + 94, "Payment", (1, 1, 1))
        for i, (nm, sub, on) in enumerate(OPTS):
            y = Y0 + 140 + i * 110
            c.fill_rrect(X0 + 20, y, PW - 40, 96, 14, (0.20, 0.14, 0.34) if on else CARD)
            radio(c, X0 + 56, y + 48, on)
            c.font(SANS, 24, True); c.text(X0 + 90, y + 44, nm, DOT if on else DIM)
            if sub: c.font(SANS, 18, True); c.text(X0 + 90, y + 74, sub, VIO)
        if t > 0.8: ring(c, X0 + 56, Y0 + 188, t, 0.8, col=VIO)
        if t > 1.0: c.pill(PX + 270, Y0 + 180, "pehle se selected", size=22, fam=SANS, col=DARK, bg=VIO, bold=True)
        pressed = TAP < t < TAP + 0.25
        c.fill_rrect(X0 + 30, Y0 + PH - 150 + (4 if pressed else 0), PW - 60, 80, 40, GREEN)
        c.font(SANS, 28, True); c.text(PX - c.text_w("Pay ₹1,499") / 2, Y0 + PH - 98, "Pay ₹1,499", DARK)
        if TAP - 0.8 < t < TAP + 0.2:
            k = ease(min(1, (t - TAP + 0.8) / 0.8))
            c._dot(PX + 160 - 160 * k, Y0 + PH + 60 - 170 * k, 13, (1, 1, 1), 1)
        if t > TAP + 0.4:
            k = ease(min(1, (t - TAP - 0.4) / 0.4))
            c.c.new_path(); c.c.set_source_rgba(*GREEN, k); c.c.arc(PX, Y0 + 640, 60 * k, 0, 6.2832); c.c.fill()
            c.dots_path([(PX - 24, Y0 + 640), (PX - 6, Y0 + 660), (PX + 28, Y0 + 622)], spacing=5, r=3.4, col=(1, 1, 1), a=k)
        if t > TAP + 1.0: white_pill(c, W / 2, 1660, "kuch badalna nahi, bas tap", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 60, Y0 + 380), 1.15), (d - 0.4, (PX + 40, Y0 + 440), 1.1)),
                  punch=0.05 * max(0, 1 - abs(t - TAP) / 0.12), seed=5)
    hud(cv); flash(cv, t, TAP, 0.08)


STAMP = 2.8
def s5(cv, t, d, st):                                     # dark side: pre-ticked insurance / donation nobody asked for
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("galat istemaal") / 2, 560, "galat istemaal", RED)
        c.fill_rrect(W / 2 - 380, 660, 760, 520, 24, CARD)
        c.font(SANS, 28, True); c.text(W / 2 - 340, 720, "Order summary", DOT)
        rows = [("Ticket", "₹2,450", None), ("Travel insurance", "₹199", True), ("Donate to charity", "₹10", True),
                ("Seat selection", "₹349", True)]
        for i, (nm, pr, tick) in enumerate(rows):
            y = 790 + i * 90
            k = ease(min(1, max(0, (t - 0.4 - i * 0.35) / 0.4)))
            if tick is not None: checkbox(c, W / 2 - 320, y + 26, True, k, RED)
            c.font(SANS, 28, True); c.text(W / 2 - 280 if tick is not None else W / 2 - 340, y + 36, nm, DOT, k)
            c.font(SANS, 28, True); c.text(W / 2 + 330 - c.text_w(pr), y + 36, pr, RED if tick else DOT, k)
        if t > 2.0: c.pill(W / 2 + 200, 640, "maanga hi nahi!", size=26, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > STAMP:
            ks = ease(min(1, (t - STAMP) / 0.3))
            c.c.save(); c.c.translate(W / 2, 1300); c.c.rotate(-0.18)
            c.rrect_path(-260 * ks, -70 * ks, 520 * ks, 140 * ks, 16); c.c.set_source_rgba(*RED, ks); c.c.set_line_width(8); c.c.stroke()
            c.font(SANS, int(70 * max(0.2, ks)), True); c.text(-c.text_w("CHAALAAKI") / 2, 26 * ks, "CHAALAAKI", RED, ks)
            c.c.restore()
    stage.compose(cv, t, d, world, K((0, (W / 2, 920), 1.05), (d - 0.4, (W / 2, 1020), 1.0)),
                  punch=0.06 * max(0, 1 - abs(t - STAMP) / 0.12), seed=6)
    hud(cv); flash(cv, t, STAMP, 0.1)


def s6(cv, t, d, st):                                     # tip: default = what most users really want; changing stays easy
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("sahi default kaisa?") / 2, 560, "sahi default kaisa?", VIO)
        items = [("jo zyaadatar users chahte hain", 0.5), ("badalna hamesha aasaan", 1.6), ("koi chupa hua charge nahi", 2.6)]
        for j, (lab, at) in enumerate(items):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            y = 660 + j * 170
            c.fill_rrect(W / 2 - 400, y, 800, 140, 22, CARD, k)
            c.c.new_path(); c.c.set_source_rgba(*GREEN, k); c.c.arc(W / 2 - 330, y + 70, 30, 0, 6.2832); c.c.fill()
            c.font(SANS, 30, True); c.text(W / 2 - 344, y + 82, "✓", DARK, k)
            c.font(SANS, 32, True); c.text(W / 2 - 270, y + 82, lab, DOT, k)
        if t > 1.6:
            c.font(SANS, 26, True); c.text(W / 2 + 230, 920, "Change ›", VIO)
        if t > 3.6: white_pill(c, W / 2, 1240, "default = madad, chaalaaki nahi", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 960), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 31 script (docs/scripts/day31.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे थर्टी वन। एक सवाल, और ईमानदारी से जवाब देना।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("नया फ़ोन लिया था, तो उसकी रिंगटोन, आपने कभी बदली? ज़्यादातर लोग, जो पहले से सेट है, वही चलने देते हैं।", "", s1, min_dur=5.6,
          whoosh=True, sfx=[(1.0, "pop_hi"), (2.6, "riser"), (4.0, "ding")]),
    Scene("एक मशहूर स्टडी में देखा गया, जिन देशों में ऑर्गन डोनेशन के लिए ख़ुद हाँ करना पड़ता है, वहाँ बहुत कम लोग डोनर बनते हैं। और जहाँ हाँ पहले से चुना होता है, वहाँ लगभग सब।",
          "", s2, min_dur=7.0, whoosh=True, sfx=[(0.4, "pop"), (1.0, "riser"), (1.6, "pop"), (2.2, "riser"), (3.2, "chime")]),
    Scene("इसे कहते हैं, डिफ़ॉल्ट इफ़ेक्ट। जो ऑप्शन पहले से चुना होता है, ज़्यादातर लोग वही रख लेते हैं। बदलने में, मेहनत जो लगती है।", "", s3,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "drop")] + [(2.2 + i * 0.12, "tick") for i in range(12)] + [(3.6, "ding")]),
    Scene("इसीलिए चेकआउट पर, आपका पिछली बार वाला यूपीआई, पहले से सेलेक्टेड आता है। कुछ बदलना नहीं, बस पे पर टैप।", "", s4, min_dur=5.6,
          whoosh=True, sfx=[(0.8, "pop_hi"), (TAP, "pop"), (TAP + 0.4, "chime"), (TAP + 1.0, "ding")]),
    Scene("पर इसका ग़लत इस्तेमाल भी होता है। पहले से टिक किया हुआ इंश्योरेंस, या डोनेशन, जिसे यूज़र ने माँगा ही नहीं। ये डिफ़ॉल्ट नहीं, चालाकी है।", "", s5,
          min_dur=6.4, whoosh=True, sfx=[(0.4 + i * 0.35, "pop_lo") for i in range(4)] + [(2.0, "buzz"), (STAMP, "drop")]),
    Scene("तो डिफ़ॉल्ट वही रखो, जो ज़्यादातर यूज़र्स सच में चाहते हैं। और बदलने का रास्ता, हमेशा आसान रखो।", "", s6, min_dur=5.4,
          whoosh=True, sfx=[(0.5, "pop_hi"), (1.6, "pop_hi"), (2.6, "pop_hi"), (3.6, "ding")]),
    Scene("आपके फ़ोन में ऐसी कौन सी सेटिंग है, जो आज तक नहीं बदली? कमेंट में बताओ। कल मिलते हैं, एंडाउमेंट इफ़ेक्ट के साथ।", "", D.s8,
          min_dur=5.0, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 31 file (model v4) has no pauses (break tags ignored): line cuts found with tools/align_cuts.py, each in the
# silence between sentences; line check 8/8.
VO_CUTS = [4.56, 13.58, 26.16, 35.32, 43.22, 53.49, 61.47]

if __name__ == "__main__":
    import daily
    daily.run(31, "Default Effect", SCENES, "day31_default_effect", cuts=VO_CUTS)

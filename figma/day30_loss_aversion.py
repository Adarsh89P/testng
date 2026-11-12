"""Day 30/45 · Loss Aversion, explained with Snapchat streaks.

Losing something hurts roughly twice as much as gaining the same thing feels good: finding ₹500 vs losing ₹500. At
11:59 pm people send a blank snap just to save a 200-day streak's little fire. Duolingo streaks, "your cart will be
cleared" and "free trial ends tomorrow" use the same law. Caution: daily fear builds tension, not habit; show loss
gently (streak freeze). Day 02 pattern; Day 30 milestone opening. Voice: Rakhi's Day 30 ElevenLabs Tisha K file at
assets/voice/day30/full.mp3 (content-verified); script in docs/scripts/day30.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 30, "Default Effect"
W, H = 1080, 1920
SNAP = (1.0, 0.95, 0.10)                          # Snapchat yellow
FIRE = (1.0, 0.45, 0.10)
ICE = (0.55, 0.85, 1.0)
DUO = (0.35, 0.80, 0.20)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def flame(c, x, y, s=1.0, a=1.0, col=FIRE, t=0.0):
    w = 1 + 0.06 * math.sin(t * 9)
    c.c.new_path(); c.c.set_source_rgba(*col, a)
    c.c.move_to(x, y - 30 * s * w)
    c.c.curve_to(x + 22 * s, y - 8 * s, x + 20 * s, y + 18 * s, x, y + 22 * s)
    c.c.curve_to(x - 20 * s, y + 18 * s, x - 22 * s, y - 2 * s, x - 6 * s, y - 14 * s)
    c.c.curve_to(x - 4 * s, y - 2 * s, x + 2 * s, y - 6 * s, x, y - 30 * s * w)
    c.c.close_path(); c.c.fill()
    c.c.new_path(); c.c.set_source_rgba(1.0, 0.85, 0.20, a)
    c.c.arc(x, y + 8 * s, 8 * s, 0, 6.2832); c.c.fill(); c.c.new_path()


def note(c, x, y, s=1.0, a=1.0, ang=0.0):
    c.c.save(); c.c.translate(x, y); c.c.rotate(ang)
    c.fill_rrect(-90 * s, -45 * s, 180 * s, 90 * s, 8 * s, (0.55, 0.45, 0.70), a)
    c.dellipse(0, 0, 26 * s, 26 * s, spacing=5, r=1.8, col=(1, 1, 1), a=a)
    c.font(SANS, int(28 * s), True); c.text(-80 * s, -14 * s, "₹500", (1, 1, 1), a)
    c.c.restore()


def snowflake(c, x, y, s=1.0, a=1.0):
    for k in range(3):
        ang = k * math.pi / 3
        c.dots_path([(x - math.cos(ang) * 40 * s, y - math.sin(ang) * 40 * s), (x + math.cos(ang) * 40 * s, y + math.sin(ang) * 40 * s)],
                    spacing=6, r=3 * s, col=ICE, a=a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # find ₹500 vs lose ₹500 — which one stays longer?
    def world(c):
        lx, rx = W * 0.27, W * 0.73
        k1 = ease(min(1, max(0, (t - 0.4) / 0.6)))
        note(c, lx, 780 - 60 * (1 - k1), 1.2, k1)
        c.font(SANS, 30, True); c.text(lx - c.text_w("mil gaye") / 2, 900, "mil gaye", GREEN, k1)
        if t > 1.4:
            c.fill_rrect(lx - 30, 1100 - 120, 60, 120, 10, GREEN); c.font(SANS, 26, True); c.text(lx - 22, 1140, "+1", GREEN)
        if t > 2.2:
            k2 = ease(min(1, (t - 2.2) / 0.9))
            note(c, rx, 760 + 220 * k2, 1.2, 1 - 0.4 * k2, ang=k2 * 0.8)
            c.font(SANS, 30, True); c.text(rx - c.text_w("gir gaye") / 2, 720, "gir gaye", RED)
        if t > 3.2:
            kk = ease(min(1, (t - 3.2) / 0.6))
            c.fill_rrect(rx - 30, 980, 60, 240 * kk, 10, RED); c.font(SANS, 26, True); c.text(rx - 22, 1260, "−2", RED)
        if t > 4.0: c.pill(W / 2, 1400, "kaun sa zyaada der yaad rahega?", size=30, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        c.pill(W / 2, 580, "Day 30 · 45 mein se 30", size=28, fam=MONO, col=DARK, bg=SNAP, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 1000), 1.02)), seed=2)
    hud(cv)


SEND = 3.4
def s2(cv, t, d, st):                                     # Snapchat 200-day streak, 11:59 pm, blank snap to save the fire
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 70, 12, SNAP)
        c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 98, "Chat", DARK)
        mm = 59 if t < SEND + 0.6 else 0
        hh = 11 if t < SEND + 0.6 else 12
        c.font(MONO, 24, True); c.text(X0 + PW - 150, Y0 + 98, f"{hh}:{mm:02d} PM" if hh == 11 else "12:00 AM", DARK)
        for i, (nm, n) in enumerate([("priya", 200), ("rahul", 34), ("ananya", 12), ("kabir", 3)]):
            y = Y0 + 150 + i * 110
            c.fill_rrect(X0 + 20, y, PW - 40, 96, 14, CARD)
            c.c.new_path(); c.c.set_source_rgba(*COLS[i], 1); c.c.arc(X0 + 70, y + 48, 28, 0, 6.2832); c.c.fill()
            c.font(SANS, 24, True); c.text(X0 + 116, y + 44, nm, DOT)
            cnt = n + (1 if (i == 0 and t > SEND + 0.6) else 0)
            c.font(SANS, 22, True); c.text(X0 + 116, y + 76, str(cnt), FIRE if i == 0 else DIM)
            flame(c, X0 + 116 + c.text_w(str(cnt)) + 22, y + 66, 0.55, 1, FIRE if i == 0 else GREY, t)
        if 1.0 < t < SEND + 0.6:
            pulse = 0.6 + 0.4 * math.sin(t * 10)
            c.pill(PX + 280, Y0 + 98, "11:59!", size=30, fam=SANS, col=DARK, bg=RED, bold=True, a=pulse)
        if 2.0 < t < SEND + 0.4:
            k = ease(min(1, (t - 2.0) / 0.4))
            c.fill_rrect(X0 + 40, Y0 + 600, PW - 80, 240, 18, (0, 0, 0), k)
            c.rrect_path(X0 + 40, Y0 + 600, PW - 80, 240, 18); c.c.set_source_rgba(*GREY, k); c.c.set_line_width(2); c.c.stroke()
            c.font(SANS, 22, True); c.text(PX - c.text_w("blank snap") / 2, Y0 + 730, "blank snap", DIM, k)
        if t > SEND:
            ring(c, X0 + 160, Y0 + 216, t, SEND, col=FIRE)
        if t > SEND + 0.8: white_pill(c, W / 2, 1660, "bas us chhoti si aag ko bachaane", 34)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 60, Y0 + 340), 1.2), (d - 0.4, (PX + 40, Y0 + 380), 1.15)),
                  punch=0.05 * max(0, 1 - abs(t - SEND) / 0.12), seed=3)
    hud(cv); flash(cv, t, SEND, 0.08)


def s3(cv, t, d, st):                                     # law named: losing hurts ~2× gaining
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "LOSS", 140, W / 2, 630, ease(1 - t / 0.8), col=FIRE)
        dot_text(c, "AVERSION", 116, W / 2, 770, ease(1 - (t - 0.2) / 0.8), col=FIRE)
        base = 1300
        k1 = ease(min(1, max(0, (t - 1.6) / 0.6))); k2 = ease(min(1, max(0, (t - 2.4) / 0.9)))
        c.fill_rrect(W / 2 - 220, base - 160 * k1, 160, 160 * k1, 14, GREEN)
        c.fill_rrect(W / 2 + 60, base - 320 * k2, 160, 320 * k2, 14, RED)
        c.font(SANS, 30, True); c.text(W / 2 - 220, base + 44, "paane ki khushi", GREEN)
        c.font(SANS, 30, True); c.text(W / 2 + 60, base + 44, "khone ka dard", RED)
        if k2 >= 1: c.pill(W / 2 + 140, base - 370, "~2×", size=40, fam=SANS, col=DARK, bg=YELLOW, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.2), (1.4, (W / 2, 1060), 1.0), (d - 0.4, (W / 2, 1100), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


def s4(cv, t, d, st):                                     # same law everywhere: Duolingo streak, cart cleared, trial ending
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("yahi law, har jagah") / 2, 560, "yahi law, har jagah", SNAP)
        cards = [(0.4, DUO, "Duolingo", "45 din ki streak"), (1.4, ORANGE, "Cart", "Aapka cart khaali ho jaayega!"),
                 (2.4, RED, "Free trial", "Kal khatam ho raha hai")]
        for j, (at, col, title, sub) in enumerate(cards):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            y = 660 + j * 230
            c.fill_rrect(W / 2 - 400, y, 800, 200, 24, CARD, k)
            c.fill_rrect(W / 2 - 400, y, 12, 200, 6, col, k)
            if j == 0: flame(c, W / 2 - 320, y + 100, 1.3, k, FIRE, t)
            elif j == 1:
                c.dots_path([(W / 2 - 360, y + 70), (W / 2 - 340, y + 70), (W / 2 - 325, y + 120), (W / 2 - 280, y + 120), (W / 2 - 270, y + 85),
                             (W / 2 - 335, y + 85)], spacing=5, r=2.6, col=ORANGE, a=k)
            else:
                c.dellipse(W / 2 - 320, y + 100, 40, 40, spacing=5, r=2.4, col=RED, a=k)
                c.dots_path([(W / 2 - 320, y + 100), (W / 2 - 320, y + 74), (W / 2 - 300, y + 108)], spacing=5, r=2.4, col=RED, a=k)
            c.font(SANS, 34, True); c.text(W / 2 - 240, y + 86, title, col, k)
            c.font(SANS, 28, True); c.text(W / 2 - 240, y + 140, sub, DOT, k)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 990), 1.0)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # caution: daily fear → tension, not habit
    MSGS = ["Streak tootne waali hai!", "Sirf 2 ghante bache!", "Aap sab kho doge!", "Jaldi karo!!!", "Last chance!"]
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("par dhyaan rahe") / 2, 560, "par dhyaan rahe", RED)
        for i, m in enumerate(MSGS):
            at = 0.3 + i * 0.4
            if t < at: continue
            k = ease(min(1, (t - at) / 0.3))
            y = 660 + i * 120 + (1 - k) * 40
            c.fill_rrect(W / 2 - 380 + (i % 2) * 30, y, 760, 100, 20, (0.20, 0.10, 0.10), k)
            flame(c, W / 2 - 330 + (i % 2) * 30, y + 52, 0.7, k, RED, t)
            c.font(SANS, 28, True); c.text(W / 2 - 280 + (i % 2) * 30, y + 62, m, DOT, k)
        if t > 2.6:
            lvl = min(1, (t - 2.6) / 1.2)
            c.font(MONO, 24, True); c.text(W / 2 - 300, 1310, "tension", DIM)
            c.fill_rrect(W / 2 - 300, 1330, 600, 36, 18, (0.20, 0.20, 0.22))
            c.fill_rrect(W / 2 - 300, 1330, max(36, 600 * lvl), 36, 18, RED)
        if t > 3.8: c.pill(W / 2, 1440, "aadat nahi, bas tension", size=30, fam=SANS, col=DARK, bg=RED, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 1050), 0.98)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # tip: show loss gently — streak freeze, one day off
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("thoda pyaar se") / 2, 560, "thoda pyaar se", ICE)
        c.fill_rrect(W / 2 - 360, 660, 720, 420, 28, (0.08, 0.14, 0.20))
        k = ease(min(1, max(0, (t - 0.6) / 0.6)))
        snowflake(c, W / 2, 800, 1.6 * k, k)
        flame(c, W / 2 + 170, 820, 1.2, k, ICE, t)
        c.font(SANS, 40, True); c.text(W / 2 - c.text_w("Streak Freeze") / 2, 960, "Streak Freeze", ICE, k)
        c.font(SANS, 28, True); c.text(W / 2 - c.text_w("1 din ki chhutti, streak safe") / 2, 1020, "1 din ki chhutti, streak safe", DOT, k)
        if t > 2.0:
            for j, lab in enumerate(["yaad dilao", "darao mat"]):
                c.pill(W / 2 - 160 + j * 320, 1170, lab + " ✓", size=26, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 3.2: white_pill(c, W / 2, 1300, "user bana rahe, par darkar nahi", 34)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 980), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 30 script (docs/scripts/day30.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे थर्टी! पैंतालीस में से तीस, और आज का लॉ, आपका दिल ज़रूर छुएगा।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("सोचो, सड़क पर पाँच सौ रुपये मिल गए। अच्छा लगा ना? अब सोचो, जेब से पाँच सौ रुपये गिर गए। कौन सी बात, ज़्यादा देर याद रहेगी?", "", s1,
          min_dur=6.0, whoosh=True, sfx=[(0.4, "chime"), (1.4, "pop_hi"), (2.2, "drop"), (3.2, "buzz"), (4.0, "pop")]),
    Scene("स्नैपचैट पर, दो सौ दिन की स्ट्रीक। रात के ग्यारह बजकर उनसठ मिनट, और लोग बस एक ब्लैंक स्नैप भेज रहे हैं, सिर्फ़ उस छोटी सी आग को बचाने के लिए।",
          "", s2, min_dur=6.6, whoosh=True, sfx=[(1.0, "tick"), (1.5, "tick"), (2.0, "pop"), (SEND, "pop_hi"), (SEND + 0.6, "chime"),
                                                 (SEND + 0.8, "ding")]),
    Scene("इसे कहते हैं, लॉस अवर्ज़न। कुछ खोने का दर्द, उतनी ही चीज़ पाने की ख़ुशी से, लगभग दोगुना लगता है।", "", s3, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "drop"), (1.6, "pop"), (2.4, "riser"), (3.3, "ding")]),
    Scene("ड्यूलिंगो की स्ट्रीक, आपका कार्ट ख़ाली हो जाएगा, या फ़्री ट्रायल कल ख़त्म हो रहा है। ये सब, यही लॉ इस्तेमाल करते हैं।", "", s4,
          min_dur=5.6, whoosh=True, sfx=[(0.4, "pop_hi"), (1.4, "pop_hi"), (2.4, "pop_hi")]),
    Scene("पर ध्यान रहे। अगर ऐप यूज़र को रोज़ डराने लगे, तो आदत नहीं बनती, बस टेंशन बनती है।", "", s5, min_dur=5.0, whoosh=True,
          sfx=[(0.3 + i * 0.4, "buzz" if i % 2 else "pop_lo") for i in range(5)] + [(3.8, "drop")]),
    Scene("तो खोने का डर, थोड़ा प्यार से दिखाओ। जैसे स्ट्रीक फ़्रीज़, एक दिन की छुट्टी। यूज़र बना रहे, पर डरकर नहीं।", "", s6, min_dur=5.6,
          whoosh=True, sfx=[(0.6, "chime"), (2.0, "pop_hi"), (3.2, "ding")]),
    Scene("आपकी सबसे लंबी स्ट्रीक कितने दिन की है? कमेंट में बताओ। कल मिलते हैं, डिफ़ॉल्ट इफ़ेक्ट के साथ।", "", D.s8, min_dur=5.0,
          whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 30 file (model v4) has no pauses (break tags ignored): line cuts found with tools/align_cuts.py, each in the
# silence between sentences; line check 8/8.
VO_CUTS = [6.4, 16.36, 27.18, 35.1, 43.45, 50.28, 58.96]

if __name__ == "__main__":
    import daily
    daily.run(30, "Loss Aversion", SCENES, "day30_loss_aversion", cuts=VO_CUTS)

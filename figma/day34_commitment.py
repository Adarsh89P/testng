"""Day 34/45 · Commitment & Consistency, explained with Duolingo's onboarding.

A small "yes" makes the next "yes" easier: Duolingo asks why you're learning (Travel), how long a day (just 5 minutes),
then gives one tiny lesson and a "Shaabaash!" — and you do one more. In the foot-in-the-door study (Freedman & Fraser,
1966) people who first agreed to a small sticker were far more likely to accept a big sign later. Ask for one small
easy step; moving on must stay the user's choice, not a trap. Day 02 pattern; open-loop hook before the day number.
Voice: Rakhi's Day 34 ElevenLabs Tisha K file at assets/voice/day34/full.mp3 (content-verified); script in
docs/scripts/day34.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 34, "Variable Reward"
W, H = 1080, 1920
DUO = (0.35, 0.80, 0.20)                          # Duolingo green
DUOD = (0.20, 0.55, 0.10)
GOLD = (1.0, 0.78, 0.25)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def owl(c, x, y, s=1.0, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*DUO, a); c.c.arc(x, y, 60 * s, 0, 6.2832); c.c.fill()
    for dx in (-22, 22):
        c.c.new_path(); c.c.set_source_rgba(1, 1, 1, a); c.c.arc(x + dx * s, y - 10 * s, 18 * s, 0, 6.2832); c.c.fill()
        c.c.new_path(); c.c.set_source_rgba(0.1, 0.1, 0.1, a); c.c.arc(x + dx * s + 3 * s, y - 8 * s, 8 * s, 0, 6.2832); c.c.fill()
    c.c.new_path(); c.c.set_source_rgba(1.0, 0.70, 0.10, a)
    c.c.move_to(x - 10 * s, y + 12 * s); c.c.line_to(x + 10 * s, y + 12 * s); c.c.line_to(x, y + 26 * s); c.c.close_path(); c.c.fill()
    c.c.new_path()


def option(c, x, y, w, lab, chosen, a=1.0):
    c.fill_rrect(x, y, w, 72, 16, (0.10, 0.25, 0.08) if chosen else CARD, a)
    c.rrect_path(x, y, w, 72, 16); c.c.set_source_rgba(*(DUO if chosen else GREY), a); c.c.set_line_width(3 if chosen else 1.5); c.c.stroke()
    c.font(SANS, 24, True); c.text(x + 24, y + 46, lab, DOT, a)


# ------------------------------------------------------------------ scenes
T1, T2 = 1.6, 3.8
def s1(cv, t, d, st):                                     # onboarding: why learn? → Travel; how long a day? → just 5 min
    def world(c):
        phone(c, PX, PY, PW, PH)
        owl(c, X0 + 70, Y0 + 110, 0.6)
        q2 = t > T1 + 0.6
        c.font(SANS, 26, True)
        c.text(X0 + 120, Y0 + 104, "Roz kitna time?" if q2 else "Aap kyun seekh rahe ho?", DOT)
        opts = ["5 min · casual", "10 min · regular", "15 min · serious", "20 min · intense"] if q2 else ["Travel", "Career", "School", "Fun"]
        for i, o in enumerate(opts):
            chosen = (not q2 and i == 0 and t > T1) or (q2 and i == 0 and t > T2)
            option(c, X0 + 30, Y0 + 180 + i * 92, PW - 60, o, chosen)
        tap = T1 if not q2 else T2
        if tap - 0.6 < t < tap + 0.2:
            k = ease(min(1, (t - tap + 0.6) / 0.6))
            c._dot(PX + 150 - 150 * k, Y0 + 600 - 384 * k, 13, (1, 1, 1), 1)
        if t > T1: c.pill(PX + 290, Y0 + 216, "chhoti haan #1", size=22, fam=SANS, col=DARK, bg=DUO, bold=True)
        if t > T2: c.pill(PX + 290, Y0 + 300, "chhoti haan #2", size=22, fam=SANS, col=DARK, bg=DUO, bold=True)
        if t > T2 + 0.8: white_pill(c, W / 2, 1660, "bas paanch minute", 40)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 70, Y0 + 330), 1.15), (d - 0.4, (PX + 60, Y0 + 360), 1.12)),
                  punch=0.04 * max(0, 1 - min(abs(t - T1), abs(t - T2)) / 0.12), seed=2)
    hud(cv)


DONE = 1.6
def s2(cv, t, d, st):                                     # first tiny lesson → "Shaabaash!" → "chalo, ek aur"
    def world(c):
        phone(c, PX, PY, PW, PH)
        prog = min(1, t / DONE)
        c.fill_rrect(X0 + 30, Y0 + 70, PW - 60, 24, 12, (0.25, 0.25, 0.28))
        c.fill_rrect(X0 + 30, Y0 + 70, (PW - 60) * prog, 24, 12, DUO)
        if t < DONE:
            c.font(SANS, 26, True); c.text(X0 + 40, Y0 + 160, "Translate: Hello", DOT)
            for i, w in enumerate(["Hola", "Adiós", "Gracias"]):
                option(c, X0 + 40, Y0 + 210 + i * 92, PW - 80, w, i == 0 and t > 0.8)
        else:
            k = ease(min(1, (t - DONE) / 0.5))
            owl(c, PX, Y0 + 300, 1.4 * k, k)
            c.font(SANS, 52, True); c.text(PX - c.text_w("Shaabaash!") / 2, Y0 + 470, "Shaabaash!", DUO, k)
            c.font(SANS, 24, True); c.text(PX - c.text_w("Lesson 1 complete · +10 XP") / 2, Y0 + 520, "Lesson 1 complete · +10 XP", GOLD, k)
            c.fill_rrect(X0 + 40, Y0 + PH - 150, PW - 80, 80, 40, DUO, k)
            c.font(SANS, 26, True); c.text(PX - c.text_w("Ek aur lesson") / 2, Y0 + PH - 100, "Ek aur lesson", DARK, k)
        if t > DONE + 1.2:
            c.fill_rrect(W / 2 - 330, 560, 660, 110, 40, (0.95, 0.95, 0.96))
            c.font(SANS, 32, True); c.text(W / 2 - c.text_w("chalo, ek aur kar lete hain") / 2, 628, "chalo, ek aur kar lete hain", DARK)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (DONE, ANCHOR, 1.0), (d - 0.4, (PX, PY - 40), 1.05)), seed=3)
    hud(cv); flash(cv, t, DONE, 0.1)


def house(c, x, y, s=1.0, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*DOT, a); c.c.set_line_width(4 * s)
    c.c.move_to(x - 120 * s, y); c.c.line_to(x, y - 100 * s); c.c.line_to(x + 120 * s, y); c.c.stroke()
    c.rrect_path(x - 100 * s, y, 200 * s, 160 * s, 6 * s); c.c.stroke()
    c.rrect_path(x - 70 * s, y + 40 * s, 60 * s, 50 * s, 4 * s); c.c.stroke()
    c.rrect_path(x + 20 * s, y + 60 * s, 50 * s, 100 * s, 4 * s); c.c.stroke(); c.c.new_path()


def s3(cv, t, d, st):                                     # foot-in-the-door: a small sticker first → later yes to a big board
    def world(c):
        c.pill(W / 2, 560, "ek puraani study", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        house(c, W / 2, 900, 1.6)
        k1 = ease(min(1, max(0, (t - 0.8) / 0.4)))
        c.fill_rrect(W / 2 - 100, 980, 60, 44, 6, GOLD, k1)
        if k1 > 0: c.pill(W / 2 - 300, 1000, "pehle: chhota sticker", size=24, fam=SANS, col=DARK, bg=GOLD, bold=True, a=k1)
        k2 = ease(min(1, max(0, (t - 2.4) / 0.6)))
        if k2 > 0:
            c.dots_path([(W / 2 + 250, 1160), (W / 2 + 250, 960)], spacing=7, r=3, col=DOT, a=k2)
            c.fill_rrect(W / 2 + 140, 820, 220, 150, 12, DUO, k2)
            c.font(SANS, 30, True); c.text(W / 2 + 170, 905, "BADA BOARD", DARK, k2)
        if t > 3.4:
            for j, (lab, h, col) in enumerate([("bina sticker", 90, GREY), ("sticker ke baad", 260, DUO)]):
                x = W / 2 - 200 + j * 260
                c.fill_rrect(x, 1480 - h, 120, h, 12, col)
                c.font(SANS, 22, True); c.text(x + 60 - c.text_w(lab) / 2, 1520, lab, DOT)
            c.pill(W / 2 + 270, 1240, "kahin zyaada haan", size=24, fam=SANS, col=DARK, bg=DUO, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (3.2, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1150), 0.95)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law named: after a small yes, we stay consistent with it
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "COMMITMENT", 110, W / 2, 630, ease(1 - t / 0.8), col=DUO)
        dot_text(c, "& CONSISTENCY", 92, W / 2, 760, ease(1 - (t - 0.2) / 0.8), col=DUO)
        c.glow(W / 2, 700, 420, 0.07)
        if t > 1.8:
            k = ease(min(1, (t - 1.8) / 0.4))
            c.fill_rrect(W / 2 - 320, 920, 260, 110, 22, DUO, k)
            c.font(SANS, 40, True); c.text(W / 2 - 190 - c.text_w("haan") / 2, 990, "haan", DARK, k)
            c.dots_path([(W / 2 - 40, 975), (W / 2 + 40, 975)], spacing=8, r=3, col=DOT, a=k)
        if t > 2.8:
            k = ease(min(1, (t - 2.8) / 0.4))
            c.fill_rrect(W / 2 + 60, 920, 260, 110, 22, DUOD, k)
            c.font(SANS, 32, True); c.text(W / 2 + 190 - c.text_w("usi pe tikna") / 2, 990, "usi pe tikna", DOT, k)
        if t > 3.8: c.pill(W / 2, 1140, "hum consistent rehna chahte hain", size=28, fam=MONO, col=DARK, bg=DUO, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.15), (1.6, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 980), 1.02)), seed=5)
    hud(cv); flash(cv, t, 0.2)


def s5(cv, t, d, st):                                     # nobody makes a big promise — a small yes opens the next yes
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("chhoti haan → agli haan") / 2, 560, "chhoti haan → agli haan", DUO)
        labs = ["5 min", "1 lesson", "2 lessons", "daily goal", "streak"]
        for i, lab in enumerate(labs):
            at = 0.4 + i * 0.5
            k = ease(min(1, max(0, (t - at) / 0.4)))
            x = W / 2 - 420 + i * 175; y = 1360 - i * 140
            c.fill_rrect(x, y, 165, 1400 - y + 40, 14, tuple(cc * (0.5 + 0.1 * i) for cc in DUO), k)
            c.font(SANS, 24, True); c.text(x + 82 - c.text_w(lab) / 2, y + 44, lab, DARK if i > 1 else DOT, k)
        n = sum(1 for i in range(5) if t > 0.4 + i * 0.5 + 0.4)
        if n: owl(c, W / 2 - 420 + (n - 1) * 175 + 82, 1360 - (n - 1) * 140 - 70, 0.6)
        if t > 3.4: white_pill(c, W / 2, 1520, "bada waada koi nahi karta", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 1050), 0.98), (d - 0.4, (W / 2, 1050), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # tip: one small easy step — moving on is their choice, not a trap
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.6), ("DO", W * 0.73, t >= 2.6)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        for i, f in enumerate(["Name", "Email", "Phone", "Address", "Card", "Goals", "Photo"]):
            c.rrect_path(lx - 170, 660 + i * 70, 340, 52, 10); c.c.set_source_rgba(*(RED if t < 2.6 else GREY), 1); c.c.set_line_width(1.6); c.c.stroke()
            c.font(SANS, 20, True); c.text(lx - 150, 694 + i * 70, f, DIM)
        c.pill(lx, 1200, "pehle din hi sab ✗", size=24, fam=SANS, col=RED)
        option(c, rx - 170, 700, 340, "5 min · casual", True)
        c.fill_rrect(rx - 170, 820, 340, 70, 35, DUO)
        c.font(SANS, 24, True); c.text(rx - c.text_w("Start") / 2, 864, "Start", DARK)
        c.font(SANS, 20, True); c.text(rx - c.text_w("Skip · baad mein") / 2, 940, "Skip · baad mein", DIM)
        c.pill(rx, 1200, "1 aasaan step ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 4.0: white_pill(c, W / 2, 1320, "aage badhna marzi ho, jaal nahi", 34)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.2, (W * 0.27, 900), 1.45), (2.8, (W * 0.73, 900), 1.45),
                                     (3.8, (W * 0.73, 900), 1.45), (4.4, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 34 script (docs/scripts/day34.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("सिर्फ़ पाँच मिनट का वादा, और आप रोज़ एक नई भाषा सीखने लगे? डे थर्टी फ़ोर में, आज इस जादू का राज़।", "", D.s0, min_dur=4.8,
          sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("ड्यूलिंगो खोला। पहला सवाल, आप भाषा क्यों सीखना चाहते हो? आपने टैप किया, ट्रैवल। फिर पूछा, रोज़ कितना टाइम? आपने चुना, बस पाँच मिनट।", "", s1,
          min_dur=6.4, whoosh=True, sfx=[(0.3, "pop"), (T1, "pop_hi"), (T1 + 0.6, "pop"), (T2, "pop_hi"), (T2 + 0.8, "ding")]),
    Scene("और फिर, पहला छोटा सा लेसन। ख़त्म होते ही, शाबाश! और आप सोचते हो, चलो, एक और कर लेते हैं।", "", s2, min_dur=5.0, whoosh=True,
          sfx=[(0.8, "pop_hi"), (DONE, "chime"), (DONE + 1.2, "pop")]),
    Scene("एक पुरानी स्टडी में, लोगों से पहले बस एक छोटा सा स्टिकर लगाने को कहा गया। और बाद में, उन्हीं में से कहीं ज़्यादा लोग, घर के बाहर बड़ा बोर्ड लगाने को भी मान गए।",
          "", s3, min_dur=6.6, whoosh=True, sfx=[(0.8, "pop"), (2.4, "riser"), (3.4, "chime")]),
    Scene("इसे कहते हैं, कमिटमेंट एंड कंसिस्टेंसी। एक बार छोटी सी हाँ कह दी, तो हम उसी के साथ, कंसिस्टेंट रहना चाहते हैं।", "", s4, min_dur=6.0,
          whoosh=True, sfx=[(0.2, "drop"), (1.8, "pop_hi"), (2.8, "pop_hi"), (3.8, "ding")]),
    Scene("बड़ा वादा कोई नहीं करता। पर छोटी हाँ, अगली हाँ का रास्ता खोल देती है।", "", s5, min_dur=4.8, whoosh=True,
          sfx=[(0.4 + i * 0.5, "pop_hi") for i in range(5)] + [(3.4, "ding")]),
    Scene("तो यूज़र से पहले दिन ही सब मत माँगो। एक छोटा सा, आसान स्टेप दो। पर ध्यान रहे, आगे बढ़ना उसकी मर्ज़ी हो, कोई जाल नहीं।", "", s6, min_dur=6.0,
          whoosh=True, sfx=[(0.3, "buzz"), (2.8, "pop_hi"), (4.0, "ding")]),
    Scene("आपने आख़िरी बार, किस ऐप को पाँच मिनट दिए, और घंटा बीत गया? कमेंट करो। कल मिलते हैं, वेरिएबल रिवॉर्ड के साथ।", "", D.s8, min_dur=5.0,
          whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 34 file (model v4) has no pauses (break tags ignored): line cuts found with tools/align_cuts.py, each in the
# silence between sentences; line check 8/8.
VO_CUTS = [7.81, 19.26, 27.34, 38.37, 47.02, 52.37, 61.96]

if __name__ == "__main__":
    import daily
    daily.run(34, "Commitment & Consistency", SCENES, "day34_commitment", cuts=VO_CUTS)

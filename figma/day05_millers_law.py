"""Day 05/45 · Miller's Law: Duolingo lessons (the chosen Day 05 version; Netflix / card / PhonePe are alternates).

A whole language in one lesson (500 words) overloads working memory; Duolingo breaks a course into units of ~5 short
lessons, each with only a few new words. Reuses hook / law card / designer tip from day05_millers_law_phonepe.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D
import day05_millers_law_phonepe as P

D.DAY, D.NEXT = 5, "Zeigarnik Effect"
W, H = 1080, 1920
DGREEN = (0.47, 0.82, 0.12)                       # Duolingo green
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
WORDS = ["apple", "water", "book", "house", "friend", "school", "happy", "walk", "eat", "city", "rain", "music", "car",
         "money", "time", "door", "chair", "green", "bread", "dog", "night", "smile", "phone", "street"]
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def s1(cv, t, d, st):                                     # hook: "kya aapko pata hai?" -> padhte hain, bhool jaate hain -> live app
    def world(c):
        mono(c, "kya aapko pata hai?", 700, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "MILLER'S LAW", 112, W / 2, 880, ease(1 - (t - 1.2) / 0.8), col=P.TEAL)
            c.glow(W / 2, 880, 400, 0.08)
        if t > 2.2: mono(c, "kya hai?", 1020, DOT, 58, chars=int((t - 2.2) * 14))
        if t > 3.2:                                          # read it ... forget it: an open book whose dots fall away
            bx, by = W / 2, 1230
            c.dots_path([(bx - 160, by - 50), (bx, by - 20), (bx + 160, by - 50), (bx + 160, by + 60), (bx, by + 90),
                         (bx - 160, by + 60), (bx - 160, by - 50)], spacing=8, r=2.2, col=DOT)
            c.dots_path([(bx, by - 20), (bx, by + 90)], spacing=8, r=2.0, col=DIM)
            for i in range(24):
                k = max(0, min(1, (t - 3.8 - (i % 8) * 0.06) / 1.2))
                c._dot(bx - 130 + (i % 12) * 23, by - 10 + (i // 12) * 40 + 420 * k * k, 4, COLS[i % 6], 1 - k)
            c.pill(W / 2, 1380, "padhte hain... bhool jaate hain", size=30, fam=MONO, col=RED if t > 4.2 else DOT)
        if t > 5.4:
            c.pill(W / 2, 1490, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=DGREEN, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 880 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 880), 1.35), (1.2, (W / 2, 880), 1.35), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1100), 1.0), (5.2, (W / 2, 1150), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


def s2(cv, t, d, st):                                     # story: 500 words in ONE lesson
    n = int(max(0, t - 0.8) * 40)
    def world(c):
        mono(c, "Lesson 1 · 500 new words", 630, RED if t > 3.0 else (0.85, 0.85, 0.88), 40)
        c.person(W / 2, 1330, 0.9)
        P.brain(c, W / 2, 1120, 0.6, col=RED if t > 3.0 else DOT)
        for i in range(min(n, 90)):                         # words pour down onto the learner
            k = ((t - 0.8 - i / 40) * 0.5) % 1
            x = 120 + (i * 137) % 840; y = 700 + 640 * k
            c.font(MONO, 26, True); c.text(x, y, WORDS[i % len(WORDS)], COLS[i % 6], max(0, 1 - k) * 0.9)
        c.pill(W / 2 + 330, 760, f"{min(500, n * 3)} / 500", size=34, fam=MONO, col=DARK, bg=RED if n > 4 else YELLOW, bold=True)
        if t > 3.0:
            for i in range(5):
                ang = -2.6 + i * 0.5
                c.pill(W / 2 + math.cos(ang) * 230, 1150 + math.sin(ang) * 170, "?", size=36, fam=MONO, col=RED)
        if t > 4.2: white_pill(c, W / 2, 1560, "10 words ke baad dimaag full", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 800), 1.2), (1.6, ANCHOR, 1.0), (2.8, ANCHOR, 1.0),
                                     (3.4, (W / 2, 1200), 1.45), (4.6, (W / 2, 1200), 1.45), (5.2, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - 3.0) / 0.12), seed=3)
    hud(cv); flash(cv, t, 3.0, 0.12)


def path_nodes(cx, top, n=5, gap=150, amp=110):
    return [(cx + math.sin(i * 1.1) * amp, top + i * gap) for i in range(n)]


SPLIT = 1.0
def s3(cv, t, d, st):                                     # course -> units -> 5 small lessons, ~7 words each
    def world(c):
        k = ease((t - SPLIT) / 0.8)
        c.pill(W / 2, 600, "Course", size=40, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        for u, (ux, col) in enumerate([(W * 0.22, DGREEN), (W * 0.5, BLUE), (W * 0.78, ORANGE)]):
            uy = 720
            c.dots_path([(W / 2, 630), (ux, uy - 30)], spacing=10, r=2, col=col, reveal=k)
            c.pill(ux, uy, f"Unit {u + 1}", size=32, fam=SANS, col=DARK, bg=col, bold=True, a=k)
            for i, (x, y) in enumerate(path_nodes(ux, 830, amp=50, gap=120)):
                kk = ease((t - SPLIT - 0.6 - i * 0.18) / 0.4)
                if kk <= 0: continue
                done = u == 0 and t > 3.0 + i * 0.25
                if done: c.c.set_source_rgba(*col, 1); c.c.arc(x, y, 38 * kk, 0, 6.3); c.c.fill()
                c.dellipse(x, y, 40 * kk, 40 * kk, spacing=6, r=2, col=col)
                c.font(SANS, 24, True); c.text(x - 8, y + 9, str(i + 1), DARK if done else DOT, kk)
        if t > 2.4: c.pill(W * 0.22 + 170, 830, "~7 words", size=26, fam=MONO, col=DGREEN)
        if t > 4.0: white_pill(c, W / 2, 1520, "chhote lessons = yaad rehta hai", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.6, ANCHOR, 1.0), (2.6, ANCHOR, 1.0),
                                     (3.0, (W * 0.3, 1000), 1.4), (4.2, (W * 0.3, 1000), 1.4), (4.8, ANCHOR, 1.0)),
                  seed=4)
    hud(cv)


TAP = 2.4
def s5(cv, t, d, st):                                     # Duolingo app: unit banner, winding lesson path, tiny lesson
    def world(c):
        c.font(SANS, 64, True); c.text(W / 2 - c.text_w("duolingo") / 2, 540, "duolingo", DGREEN)
        phone(c, PX, PY, PW, PH)
        c.fill_rrect(X0 + 26, Y0 + 70, PW - 52, 110, 18, DGREEN)
        c.font(SANS, 24, True); c.text(X0 + 50, Y0 + 115, "UNIT 1 · SECTION 1", DARK); c.font(SANS, 22); c.text(X0 + 50, Y0 + 152, "Order food, describe people", DARK)
        nodes = path_nodes(PX, Y0 + 280, n=5, gap=125, amp=90)
        for i, (x, y) in enumerate(nodes):
            done = i < 2 or (i == 2 and t > TAP + 2.2)
            if done: c.c.set_source_rgba(*DGREEN, 1); c.c.arc(x, y, 42, 0, 6.3); c.c.fill()
            c.dellipse(x, y, 44, 44, spacing=6, r=2.2, col=DGREEN if (done or i == 2) else DIM)
            c.font(SANS, 26, True); c.text(x - 9, y + 10, "✓" if done else str(i + 1), DARK if done else DOT)
        st["node"] = nodes[2]
        ring(c, *nodes[2], t, TAP, DGREEN)
        if TAP - 0.4 < t < TAP + 0.2: c._dot(nodes[2][0] + 8, nodes[2][1] + 10, 16, (1, 1, 1), 0.9)
        if TAP + 0.3 < t < TAP + 2.2:                       # lesson card: only a few new words
            k = ease((t - TAP - 0.3) / 0.4)
            c.fill_rrect(X0 + 40, Y0 + 300, PW - 80, 360 * k, 22, (0.12, 0.12, 0.14))
            if k > 0.9:
                c.font(SANS, 26, True); c.text(X0 + 70, Y0 + 350, "Lesson 3 · 6 new words", DGREEN)
                for j, wd in enumerate(["water", "bread", "eat", "please", "thanks", "rice"]):
                    c.pill(X0 + 130 + (j % 2) * 210, Y0 + 420 + (j // 2) * 70, wd, size=26, fam=MONO, col=DOT)
        if t > 1.2: c.pill(PX + 340, Y0 + 125, "1 unit", size=26, fam=MONO, col=DARK, bg=DGREEN, bold=True)
        if t > 1.6: c.pill(PX + 340, Y0 + 400, "5 lessons", size=26, fam=MONO, col=DARK, bg=DGREEN, bold=True)
        if t > TAP + 2.4: c.pill(PX - 330, nodes[2][1], "+10 XP", size=30, fam=MONO, col=DARK, bg=YELLOW, bold=True)
        if t > 5.6: white_pill(c, W / 2, 1620, "thoda thoda, roz", 36)
    n2 = st.get("node", (PX, Y0 + 530))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.8, ANCHOR, 1.0), (2.3, (PX, Y0 + 480), 1.5), (4.4, (PX, Y0 + 480), 1.5),
                                     (5.0, ANCHOR, 1.0)),
                  punch=0.04 * max(0, 1 - abs(t - TAP) / 0.1), seed=6)
    hud(cv)


SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे फाइव।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, मिलर्स लॉ क्या है? हम पढ़ते तो हैं, लेकिन भूल जाते हैं। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।", "", s1,
          min_dur=7.2, whoosh=True, sfx=[(1.2, "drop"), (2.2, "pop"), (3.8, "riser"), (4.2, "buzz"), (5.4, "pop_hi")]),
    Scene("एक लेसन में पाँच सौ नए वर्ड्स? दस के बाद ही दिमाग फुल।", "", s2,
          min_dur=6.0, whoosh=True, sfx=[(0.8 + i * 0.2, "tick") for i in range(10)] + [(3.0, "buzz")]),
    Scene("अब वही कोर्स छोटे यूनिट्स में, और हर लेसन में बस कुछ वर्ड्स।", "", s3,
          min_dur=5.8, whoosh=True, sfx=[(SPLIT, "riser"), (1.8, "pop"), (2.1, "pop"), (2.4, "pop_hi"), (3.0, "ding")]),
    Scene("यही है मिलर्स लॉ। दिमाग एक बार में लगभग सात चीज़ें ही याद रखता है।",
          "", P.s4, min_dur=8.0, whoosh=True, sfx=[(0.2, "ding"), (2.2, "riser")] + [(2.2 + i * 0.25, "pop") for i in range(7)]
          + [(4.0, "buzz"), (5.4, "pop_hi")]),
    Scene("इसीलिए ड्यूओलिंगो छोटे लेसन्स देता है। रोज़ थोड़ा थोड़ा।", "", s5,
          min_dur=7.4, whoosh=True, clicks=[TAP], sfx=[(1.2, "pop"), (1.6, "pop"), (TAP + 0.02, "pop_hi"), (TAP + 2.4, "chime")]),
    Scene("डिज़ाइनर टिप। बड़े काम को छोटे स्टेप्स में तोड़ो।", "", P.s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop"), (3.6, "pop"), (4.2, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    import daily
    daily.run(5, "Miller's Law", SCENES, "day05_millers_law")

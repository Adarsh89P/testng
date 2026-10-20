"""Day 06/45 · Zeigarnik Effect, explained with LinkedIn's profile-strength meter.

Unfinished tasks stay on our mind more than finished ones, so a visible "70% complete" bar pulls us to finish.
Day 02 pattern. Voice: a NEW Day 06 voice-over (Rakhi's ElevenLabs Tisha K file or recording) at
assets/voice/day06/full.*, script in docs/scripts/day06.md; see docs/voice_workflow.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 6, "Goal-Gradient Effect"
W, H = 1080, 1920
LBLUE = (0.25, 0.58, 0.98)                        # LinkedIn blue (brightened for the black background)
AMBER = (1.0, 0.72, 0.25)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def checkbox(c, x, y, done, col=GREEN, a=1.0, s=1.0):
    c.drrect(x - 18 * s, y - 18 * s, 36 * s, 36 * s, 8, spacing=5, r=1.6, col=col if done else DIM, a=a)
    if done: c.dots_path([(x - 10 * s, y), (x - 2 * s, y + 9 * s), (x + 12 * s, y - 10 * s)], spacing=4, r=2.4, col=col, a=a)


def bar(c, x, y, w, k, col=LBLUE, h=22, a=1.0, glow_gap=False, t=0.0):
    c.fill_rrect(x, y, w, h, h / 2, (0.16, 0.16, 0.19), a)
    if k > 0: c.fill_rrect(x, y, max(h, w * k), h, h / 2, col, a)
    if glow_gap and k < 1:                               # the unfinished part keeps pulsing
        p = 0.35 + 0.35 * abs(math.sin(t * 3))
        c.rrect_path(x + w * k, y - 4, w * (1 - k), h + 8, (h + 8) / 2); c.c.set_source_rgba(*AMBER, p * a)
        c.c.set_line_width(3); c.c.stroke()


def avatar(c, x, y, filled, a=1.0):
    c.dellipse(x, y, 54, 54, spacing=6, r=2.0, col=LBLUE if filled else DIM, a=a)
    if filled:
        c.c.set_source_rgba(*LBLUE, 0.85 * a); c.c.arc(x, y, 50, 0, 6.3); c.c.fill()
        c.person(x, y + 6, 0.42)
    else:
        c.font(SANS, 40, True); c.text(x - 12, y + 14, "+", DIM, a)


def profile(c, k, photo=False, skills=0, t=0.0, a=1.0, glow=True):
    """Dotted LinkedIn-style profile card inside the phone. k = profile strength 0..1."""
    phone(c, PX, PY, PW, PH, a=a)
    c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 90, "in", LBLUE, a)
    c.drrect(X0 + 26, Y0 + 120, PW - 52, 120, 16, spacing=6, r=1.4, col=DIM, a=a)        # banner
    avatar(c, X0 + 100, Y0 + 240, photo, a)
    c.dbar(X0 + 30, Y0 + 320, 220, rows=3, gap=7, a=a); c.dbar(X0 + 30, Y0 + 356, 300, rows=2, gap=6, col=DIM, a=a)
    c.font(SANS, 22, True); c.text(X0 + 30, Y0 + 420, "Profile strength", DOT, a)
    c.font(MONO, 24, True); pct = f"{int(round(k * 100))}%"; c.text(X0 + PW - 30 - c.text_w(pct), Y0 + 420, pct, LBLUE if k < 1 else GREEN, a)
    bar(c, X0 + 30, Y0 + 438, PW - 60, k, col=LBLUE if k < 1 else GREEN, a=a, glow_gap=glow, t=t)
    c.font(SANS, 22, True); c.text(X0 + 30, Y0 + 510, "Skills", DOT, a)
    for i, sk in enumerate(["Figma", "UX", "Research"][:skills]):
        c.pill(X0 + 80 + i * 130, Y0 + 550, sk, size=22, fam=SANS, col=DARK, bg=LBLUE, bold=True, a=a)
    if skills == 0: c.dbar(X0 + 30, Y0 + 545, 200, rows=1, gap=6, col=DIM, a=a)
    for i in range(3): c.dbar(X0 + 30, Y0 + 610 + i * 40, (PW - 60) * (0.85 - 0.12 * i), rows=2, gap=6, col=DIM, a=a)
    return {"avatar": (X0 + 100, Y0 + 240), "bar": (PX, Y0 + 449), "skills": (X0 + 80, Y0 + 550)}


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: kya aapko pata hai? adhoora kaam dimaag se nahi jaata
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "ZEIGARNIK EFFECT", 92, W / 2, 860, ease(1 - (t - 1.2) / 0.8), col=AMBER)
            c.glow(W / 2, 860, 420, 0.08)
        if t > 2.2: mono(c, "kya hai?", 990, DOT, 58, chars=int((t - 2.2) * 14))
        if t > 3.0:                                          # a to-do list with one task that keeps blinking
            for i, (lab, done) in enumerate([("Email bhejna", True), ("Report", True), ("Course khatam", False)]):
                y = 1110 + i * 70
                blink = (not done) and (int(t * 3) % 2 == 0)
                checkbox(c, W / 2 - 170, y, done, col=GREEN if done else AMBER, a=1.0 if not blink else 0.35)
                c.font(SANS, 32, True); c.text(W / 2 - 130, y + 11, lab, DOT if done else AMBER)
            c.pill(W / 2, 1360, "adhoora kaam dimaag se nahi jaata", size=30, fam=MONO, col=AMBER)
        if t > 5.4: c.pill(W / 2, 1470, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=LBLUE, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 860 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 860), 1.3), (1.2, (W / 2, 860), 1.3), (2.1, (W / 2, 950), 1.0),
                                     (3.0, (W / 2, 1100), 1.0), (5.2, (W / 2, 1150), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


def s2(cv, t, d, st):                                     # LinkedIn: profile 70% complete, "bas thoda sa aur"
    def world(c):
        k = 0.7 * ease(min(1, max(0, (t - 0.6) / 1.4)))
        pos = profile(c, k, t=t)
        st["bar"] = pos["bar"]
        if t > 2.4:
            c.pill(PX + 330, Y0 + 449, "70% complete", size=30, fam=MONO, col=DARK, bg=AMBER, bold=True)
        if t > 3.4:                                          # thought bubble
            bx, by = PX - 300, Y0 + 300
            for i, r in enumerate((10, 16)): c._dot(bx + 60 + i * 30, by + 120 - i * 30, r, (1, 1, 1), 0.8)
            c.fill_rrect(bx - 150, by - 20, 300, 90, 40, (0.95, 0.95, 0.96))
            c.font(SANS, 28, True); c.text(bx - 120, by + 35, "bas thoda sa aur...", DARK)
    b = st.get("bar", (PX, Y0 + 449))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, b, 1.7), (2.8, b, 1.7), (3.4, (PX - 80, Y0 + 380), 1.15),
                                     (d - 0.5, (PX - 80, Y0 + 380), 1.15)), seed=3)
    hud(cv)


TAP1, TAP2 = 1.0, 2.4
def s3(cv, t, d, st):                                     # add photo, add skills -> 100%
    k = 0.7 + (0.15 if t >= TAP1 + 0.2 else 0) + (0.15 if t >= TAP2 + 0.2 else 0)
    def world(c):
        kk = min(k, 0.7 + 0.3 * ease(min(1, max(0, (t - TAP1) / (TAP2 + 0.6 - TAP1)))))
        pos = profile(c, kk, photo=t >= TAP1, skills=0 if t < TAP2 else min(3, int((t - TAP2) * 6) + 1), t=t, glow=kk < 1)
        st.update(pos)
        ring(c, *pos["avatar"], t, TAP1, LBLUE); ring(c, *pos["skills"], t, TAP2, LBLUE)
        if TAP1 - 0.4 < t < TAP1 + 0.2: c._dot(pos["avatar"][0] + 10, pos["avatar"][1] + 12, 16, (1, 1, 1), 0.9)
        if TAP2 - 0.4 < t < TAP2 + 0.2: c._dot(pos["skills"][0] + 10, pos["skills"][1] + 12, 16, (1, 1, 1), 0.9)
        if t > TAP1: c.pill(PX + 330, Y0 + 240, "+ photo", size=28, fam=MONO, col=DARK, bg=LBLUE, bold=True)
        if t > TAP2: c.pill(PX + 330, Y0 + 550, "+ skills", size=28, fam=MONO, col=DARK, bg=LBLUE, bold=True)
        done_t = TAP2 + 0.8
        if t > done_t:
            bx, by = pos["bar"]
            for i in range(30):
                ang = i / 30 * 6.283; dd = 40 + 260 * ease((t - done_t) / 1.2)
                c._dot(bx + math.cos(ang) * dd, by + math.sin(ang) * dd * 0.6, 5, COLS[i % 6], max(0, 1 - (t - done_t) / 1.2))
            c.pill(PX, Y0 + PH + 70, "100% · done ✓", size=36, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > done_t + 0.8: white_pill(c, W / 2, 1640, "ab jaake sukoon mila", 36)
    a, s = st.get("avatar", (X0 + 100, Y0 + 240)), st.get("skills", (X0 + 80, Y0 + 550))
    b = st.get("bar", (PX, Y0 + 449))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, a, 1.6), (1.6, a, 1.6), (2.1, s, 1.6), (3.0, s, 1.6),
                                     (3.4, b, 1.5), (4.2, b, 1.5), (4.8, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - TAP2 - 0.8) / 0.12), seed=4)
    hud(cv); flash(cv, t, TAP2 + 0.8, 0.12)


def s4(cv, t, d, st):                                     # law card: unfinished list pulses in memory, finished fades
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "ZEIGARNIK EFFECT", 84, W / 2, 630, ease(1 - t / 0.8), col=AMBER)
        l1 = "adhoore kaam, poore kaamon se"; l2 = "zyada yaad rehte hain"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 34, chars=n); mono(c, l2, 800, AMBER, 34, chars=n - len(l1))
        fade = ease(min(1, max(0, (t - 3.6) / 1.4)))
        for side, (x, title, done, col) in enumerate([(W * 0.28, "Adhoora", [True, True, False, False], AMBER),
                                                      (W * 0.72, "Poora", [True, True, True, True], GREEN)]):
            a = 1.0 if side == 0 else 1.0 - 0.75 * fade
            pulse = 1 + (0.05 * math.sin(t * 6) if side == 0 and t > 3.0 else 0)
            c.fill_rrect(x - 170 * pulse, 900, 340 * pulse, 420, 26, (0.11, 0.11, 0.13), a)
            c.rrect_path(x - 170 * pulse, 900, 340 * pulse, 420, 26); c.c.set_source_rgba(*col, a); c.c.set_line_width(3 if side == 0 else 2); c.c.stroke()
            c.font(SANS, 36, True); c.text(x - c.text_w(title) / 2, 960, title, col, a)
            for i, dn in enumerate(done):
                y = 1030 + i * 66
                checkbox(c, x - 110, y, dn, col=col if dn else AMBER, a=a)
                c.dbar(x - 70, y - 6, 170, rows=2, gap=6, col=DOT if not dn else DIM, a=a)
        if t > 3.0: c.pill(W * 0.28, 1370, "dimaag mein atka", size=28, fam=MONO, col=DARK, bg=AMBER, bold=True)
        if t > 4.4: c.pill(W * 0.72, 1370, "bhool gaye", size=28, fam=MONO, col=DIM)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1000), 1.0), (2.8, (W / 2, 1000), 1.0),
                                     (3.3, (W * 0.28, 1110), 1.3), (4.6, (W * 0.28, 1110), 1.3), (5.4, (W / 2, 1050), 1.0)), seed=5)
    hud(cv)


ADD = 4.2
def s5(cv, t, d, st):                                     # LinkedIn: profile-strength meter + "next step" card
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("LinkedIn") / 2, 540, "LinkedIn", LBLUE)
        pos = profile(c, 0.85, photo=True, skills=3, t=t)
        st["bar"] = pos["bar"]
        k = ease(min(1, max(0, (t - 1.6) / 0.5)))
        cy = Y0 + 600
        c.fill_rrect(X0 + 26, cy, PW - 52, 170 * k, 18, (0.13, 0.15, 0.2))
        if k > 0.9:
            c.rrect_path(X0 + 26, cy, PW - 52, 170, 18); c.c.set_source_rgba(*LBLUE, 1); c.c.set_line_width(2); c.c.stroke()
            c.font(SANS, 22, True); c.text(X0 + 50, cy + 44, "Next step", LBLUE)
            c.font(SANS, 26, True); c.text(X0 + 50, cy + 86, "Add a summary · 1 min", DOT)
            bx, by = X0 + 50, cy + 108
            c.fill_rrect(bx, by, 120, 44, 22, LBLUE); c.font(SANS, 22, True); c.text(bx + 38, by + 30, "Add", DARK)
            st["add"] = (bx + 60, by + 22)
            ring(c, bx + 60, by + 22, t, ADD, LBLUE)
            if ADD - 0.4 < t < ADD + 0.2: c._dot(bx + 70, by + 34, 16, (1, 1, 1), 0.9)
        if t > 0.8: c.pill(PX + 330, Y0 + 449, "progress dikhta hai", size=26, fam=MONO, col=DARK, bg=AMBER, bold=True)
        if t > 2.4: c.pill(PX + 330, cy + 86, "agla step saaf", size=26, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > 5.2: white_pill(c, W / 2, 1640, "adhoora dikhao, aage badhao", 36)
    b, ad = st.get("bar", (PX, Y0 + 449)), st.get("add", (X0 + 110, Y0 + 730))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, b, 1.6), (1.5, b, 1.6), (2.2, (PX, Y0 + 690), 1.5),
                                     (ADD - 0.4, ad, 1.8), (ADD + 0.8, ad, 1.8), (ADD + 1.4, ANCHOR, 1.0)),
                  punch=0.04 * max(0, 1 - abs(t - ADD) / 0.1), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T fake pressure | DO honest progress + next step
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx = W * 0.27
        secs = max(0, 120 - int(t * 23))
        shake = math.sin(t * 40) * 6 if t < 2.8 else 0
        c.fill_rrect(lx - 180 + shake, 680, 360, 110, 20, (0.25, 0.06, 0.06))
        c.font(MONO, 44, True); s = f"0{secs // 60}:{secs % 60:02d}"; c.text(lx - c.text_w(s) / 2 + shake, 752, s, RED)
        for i, wtxt in enumerate(["Complete NOW!!", "Profile weak!", "Last chance!"]):
            c.pill(lx + shake * (i % 2), 860 + i * 80, wtxt, size=28, fam=SANS, col=DARK, bg=RED, bold=True)
        c.pill(lx, 1140, "jhootha pressure", size=28, fam=MONO, col=RED)
        rx = W * 0.73
        c.fill_rrect(rx - 180, 680, 360, 260, 24, (0.11, 0.11, 0.13))
        c.font(SANS, 26, True); c.text(rx - 150, 730, "Profile 85%", DOT)
        bar(c, rx - 150, 750, 300, 0.85, col=LBLUE, glow_gap=True, t=t)
        c.font(SANS, 24, True); c.text(rx - 150, 830, "Next: summary", LBLUE); c.font(SANS, 22); c.text(rx - 150, 868, "~1 min", DIM)
        c.pill(rx, 1140, "sach + agla step", size=28, fam=MONO, col=GREEN)
        if t > 5.0: white_pill(c, W / 2, 1300, "progress dikhao, pressure nahi", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration (Hinglish): the approved Day 06 script (docs/scripts/day06.md). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे सिक्स।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, ज़ाइगार्निक इफ़ेक्ट क्या है? अधूरा काम दिमाग से जाता ही नहीं। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।", "", s1,
          min_dur=7.2, whoosh=True, sfx=[(1.2, "drop"), (2.2, "pop"), (3.0, "pop"), (3.4, "pop"), (3.8, "buzz"), (5.4, "pop_hi")]),
    Scene("लिंक्डइन खोलते ही दिखता है, प्रोफाइल सेवेंटी परसेंट कंप्लीट। और हम सोचते हैं, बस थोड़ा सा और।", "", s2,
          min_dur=5.6, whoosh=True, sfx=[(0.6, "riser"), (2.4, "pop_hi"), (3.4, "pop")]),
    Scene("फोटो डाली, स्किल्स डाले, और बार हंड्रेड परसेंट तक पहुँच गई। अब जाके सुकून मिला।", "", s3,
          min_dur=5.6, whoosh=True, clicks=[TAP1, TAP2], sfx=[(TAP1 + 0.02, "pop"), (TAP2 + 0.02, "pop"), (TAP2 + 0.8, "chime"), (TAP2 + 1.6, "ding")]),
    Scene("यही है ज़ाइगार्निक इफ़ेक्ट। अधूरे काम हमें पूरे कामों से ज़्यादा याद रहते हैं।", "", s4,
          min_dur=6.6, whoosh=True, sfx=[(0.2, "ding"), (3.0, "buzz"), (4.4, "pop_lo")]),
    Scene("इसीलिए लिंक्डइन प्रोग्रेस बार और अगला स्टेप दिखाता है, ताकि आप प्रोफाइल पूरी कर दो।", "", s5,
          min_dur=6.4, whoosh=True, clicks=[ADD], sfx=[(0.8, "pop"), (1.6, "riser"), (2.4, "pop_hi"), (ADD + 0.02, "chime")]),
    Scene("डिज़ाइनर टिप। प्रोग्रेस दिखाओ, और अगला छोटा स्टेप साफ बताओ। पर झूठा प्रेशर मत दो।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.2, "buzz"), (1.0, "buzz"), (3.0, "pop"), (3.6, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    import daily
    daily.run(6, "Zeigarnik Effect", SCENES, "day06_zeigarnik_effect")

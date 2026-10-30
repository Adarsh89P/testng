"""Day 17/45 · Law of Similarity, explained with Instagram story rings.

Things that look alike (colour, shape, size) are read as one group with one meaning. In the Instagram stories row a
colourful ring means a new story, a grey ring means seen and a green ring means Close Friends; users read this
without any text. Day 02 pattern. Voice: Rakhi's Day 17 ElevenLabs Tisha K file at assets/voice/day17/full.mp3
(content-verified); script in docs/scripts/day17.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 17, "Uniform Connectedness"
W, H = 1080, 1920
IGRAD = [(1.0, 0.80, 0.25), (0.99, 0.45, 0.20), (0.90, 0.20, 0.45), (0.60, 0.25, 0.80)]   # story-ring gradient
CF = (0.25, 0.80, 0.35)                           # Close Friends green
SEEN = (0.42, 0.42, 0.46)
PINK = IGRAD[2]
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
# (name, kind, avatar colour); kind: new | seen | cf
STORIES = [("Your story", "own", (0.55, 0.55, 0.60)), ("priya", "new", (0.85, 0.55, 0.35)),
           ("rahul", "seen", (0.35, 0.55, 0.85)), ("ananya", "cf", (0.80, 0.40, 0.55)),
           ("kabir", "new", (0.45, 0.75, 0.55)), ("meera", "seen", (0.75, 0.65, 0.30))]


def grad_col(k):
    k = max(0.0, min(0.999, k)) * (len(IGRAD) - 1); i = int(k); f = k - i
    return tuple(IGRAD[i][j] + (IGRAD[i + 1][j] - IGRAD[i][j]) * f for j in range(3))


def story_ring(c, x, y, r, kind, a=1.0, lw=6):
    """Instagram-style ring: gradient for new, grey for seen, green for Close Friends."""
    c.c.new_path()
    if kind == "new":
        n = 48
        for i in range(n):
            c.c.new_path(); c.c.set_source_rgba(*grad_col(i / n), a)
            c.c.arc(x, y, r, math.pi * 0.75 + i / n * 6.2832, math.pi * 0.75 + (i + 1.05) / n * 6.2832)
            c.c.set_line_width(lw); c.c.stroke()
    elif kind in ("seen", "cf"):
        c.c.set_source_rgba(*(SEEN if kind == "seen" else CF), a); c.c.arc(x, y, r, 0, 6.2832)
        c.c.set_line_width(lw * (0.5 if kind == "seen" else 1)); c.c.stroke()
    c.c.new_path()


def avatar(c, x, y, r, col, kind, name=None, a=1.0, lw=6):
    story_ring(c, x, y, r + 9, kind, a, lw)
    c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x, y, r, 0, 6.2832); c.c.fill()
    c.dellipse(x, y - r * 0.18, r * 0.30, r * 0.30, spacing=5, r=1.8, col=(1, 1, 1), a=a)
    c.dellipse(x, y + r * 0.62, r * 0.55, r * 0.40, a0=180, a1=360, spacing=5, r=1.8, col=(1, 1, 1), a=a)
    if kind == "own":
        c.c.new_path(); c.c.set_source_rgba(*BLUE, a); c.c.arc(x + r * 0.72, y + r * 0.72, r * 0.26, 0, 6.2832); c.c.fill()
        c.font(SANS, int(r * 0.42), True); c.text(x + r * 0.72 - r * 0.12, y + r * 0.86, "+", (1, 1, 1), a)
    if name:
        c.font(SANS, 18, True); c.text(x - c.text_w(name) / 2, y + r + 40, name, DOT, a)


def stories_row(c, y, a=1.0, upto=6, r=42):
    for i, (nm, kind, col) in enumerate(STORIES[:upto]):
        avatar(c, X0 + 62 + i * 108, y, r, col, kind, nm, a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: ek jaisa dikhe = ek group
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "LAW OF SIMILARITY", 86, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=PINK)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "kya hai?", 980, DOT, 56, chars=int((t - 2.0) * 14))
        if t > 2.8:
            k = ease(min(1, max(0, (t - 3.6) / 0.8)))
            for r in range(3):
                for col in range(6):
                    x = W / 2 - 300 + col * 120; y = 1150 + r * 100
                    if col % 2 == 0:
                        c._dot(x, y, 22, BLUE if k > 0.5 else DOT, 1)
                    else:
                        s = 22
                        c.fill_rrect(x - s, y - s, 2 * s, 2 * s, 4, PINK if k > 0.5 else DOT, 1)
            if k >= 1: c.pill(W / 2, 1460, "ek jaisa dikhe = ek group", size=30, fam=MONO, col=DARK, bg=PINK, bold=True)
        if t > 5.6: c.pill(W / 2, 1570, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=PINK, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (2.9, (W / 2, 1220), 1.0), (5.4, (W / 2, 1250), 1.02)), seed=2)
    hud(cv); flash(cv, t, 3.6, 0.08)


def feed(c, y0):
    """Simple dotted Instagram post below the stories row."""
    c.c.new_path(); c.c.set_source_rgba(*STORIES[1][2], 1); c.c.arc(X0 + 50, y0 + 30, 22, 0, 6.2832); c.c.fill()
    c.font(SANS, 20, True); c.text(X0 + 84, y0 + 37, "priya", DOT)
    c.fill_rrect(X0 + 10, y0 + 70, PW - 20, 330, 6, CARD)
    c.dellipse(PX, y0 + 230, 70, 70, spacing=7, r=2.2, col=DIM)


def s2(cv, t, d, st):                                     # Instagram: stories row, colourful vs grey rings
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 34, True); c.text(X0 + 26, Y0 + 96, "Instagram", DOT)
        k = ease(min(1, max(0, (t - 0.3) / 0.6)))
        stories_row(c, Y0 + 190, a=k)
        feed(c, Y0 + 300)
        if t > 2.0:
            for i, (nm, kind, col) in enumerate(STORIES):
                if kind == "new": ring(c, X0 + 62 + i * 108, Y0 + 190, t, 2.0, col=IGRAD[1])
            c.pill(PX, Y0 + 300 + 440, "rangeen ring", size=26, fam=SANS, col=DARK, bg=IGRAD[1], bold=True)
        if t > 3.4:
            for i, (nm, kind, col) in enumerate(STORIES):
                if kind == "seen": ring(c, X0 + 62 + i * 108, Y0 + 190, t, 3.4, col=SEEN)
            c.pill(PX, Y0 + 300 + 510, "grey ring", size=26, fam=SANS, col=DOT, bg=SEEN, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX, Y0 + 260), 1.45), (d - 0.4, (PX, Y0 + 320), 1.35)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # meaning read without text: new / seen / close friends
    LEG = [("new", "nayi story", IGRAD[1], 0.8), ("seen", "dekh li", SEEN, 2.0), ("cf", "close friends", CF, 3.4)]
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 34, True); c.text(X0 + 26, Y0 + 96, "Instagram", DOT)
        stories_row(c, Y0 + 190)
        feed(c, Y0 + 300)
        for j, (kind, lab, col, at) in enumerate(LEG):
            if t < at: continue
            kk = ease(min(1, (t - at) / 0.4))
            y = 1560 + j * 120
            avatar(c, W / 2 - 200, y, 38, STORIES[1][2], kind, a=kk, lw=6)
            c.font(SANS, 34, True); c.text(W / 2 - 120, y + 12, "= " + lab, col if kind != "seen" else DOT, kk)
            for i, (nm, kd, cl) in enumerate(STORIES):
                if kd == kind: ring(c, X0 + 62 + i * 108, Y0 + 190, t, at, col=col)
        if t > 4.6: white_pill(c, W / 2, 1460, "bina kuch padhe samajh aa gaya", 34)
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + 300), 1.2), (0.6, (W / 2, 1300), 0.82), (d - 0.4, (W / 2, 1320), 0.82)),
                  seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law card: same colour / shape / size = same job
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "LAW OF SIMILARITY", 80, W / 2, 630, ease(1 - t / 0.8), col=PINK)
        l1 = "rang, shape ya size ek jaisa,"; l2 = "toh kaam bhi ek jaisa"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 34, chars=n); mono(c, l2, 800, PINK, 34, chars=n - len(l1))
        rows = [("rang", 2.4), ("shape", 3.2), ("size", 4.0)]
        for j, (lab, at) in enumerate(rows):
            kk = ease(min(1, max(0, (t - at) / 0.5)))
            if kk <= 0: continue
            y = 960 + j * 150
            c.font(MONO, 30, True); c.text(W / 2 - 400, y + 10, lab, DOT, kk)
            for i in range(5):
                x = W / 2 - 180 + i * 110
                odd = i in (1, 3)
                if lab == "rang": c._dot(x, y, 26, PINK if odd else BLUE, kk)
                elif lab == "shape":
                    if odd: c.fill_rrect(x - 24, y - 24, 48, 48, 4, DOT, kk)
                    else: c._dot(x, y, 26, DOT, kk)
                else: c._dot(x, y, 34 if odd else 16, DOT, kk)
        if t > 4.8: c.pill(W / 2, 1450, "jo milte-julte, woh ek group", size=28, fam=MONO, col=DARK, bg=PINK, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.9, (W / 2, 1060), 1.0), (d - 0.4, (W / 2, 1080), 1.03)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # consistent links & buttons = instant recognition
    def world(c):
        c.font(SANS, 52, True); c.text(W / 2 - c.text_w("ek jaisa = turant pehchaan") / 2, 560, "ek jaisa = turant pehchaan", PINK)
        c.fill_rrect(W / 2 - 400, 660, 800, 680, 26, CARD)
        lines = ["Apna order ", "yahan", " track karo. Help ke liye ", "support", " se baat karo,", "ya ", "FAQ", " padho."]
        x, y = W / 2 - 360, 760
        k = ease(min(1, max(0, (t - 0.6) / 0.6)))
        for s in lines:
            link = s in ("yahan", "support", "FAQ")
            c.font(SANS, 30, True)
            w = c.text_w(s)
            if x + w > W / 2 + 370: x, y = W / 2 - 360, y + 54
            c.text(x, y, s, BLUE if link else DOT, k)
            if link and t > 1.6: c.c.set_source_rgba(*BLUE, k); c.c.rectangle(x, y + 8, w, 3); c.c.fill()
            x += w
        for i, lab in enumerate(["Pay", "Track", "Reorder"]):
            kk = ease(min(1, max(0, (t - 2.2 - i * 0.3) / 0.4)))
            c.fill_rrect(W / 2 - 360 + i * 250, 1060, 220, 80, 40, PINK, kk)
            c.font(SANS, 28, True); c.text(W / 2 - 250 + i * 250 - c.text_w(lab) / 2, 1110, lab, DARK, kk)
        if t > 1.6: c.pill(W / 2 + 230, 950, "saare link: blue", size=24, fam=MONO, col=DARK, bg=BLUE, bold=True)
        if t > 3.2: c.pill(W / 2, 1230, "saare button: ek jaise", size=24, fam=MONO, col=DARK, bg=PINK, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (d - 0.4, (W / 2, 1000), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T mix looks | DO same job = same look
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        mixed = [("Save", BLUE, 40), ("Next", GREEN, 8), ("Done", ORANGE, 24)]
        for i, (lab, col, rad) in enumerate(mixed):
            c.fill_rrect(lx - 150, 700 + i * 120, 300, 80, rad, col)
            c.font(SANS, 28, True); c.text(lx - c.text_w(lab) / 2, 750 + i * 120, lab, DARK)
        c.fill_rrect(lx - 150, 1060, 300, 80, 40, (0.30, 0.30, 0.34))
        c.font(SANS, 28, True); c.text(lx - c.text_w("Delete") / 2, 1110, "Delete", DIM)
        c.pill(lx, 1200, "har button alag ✗", size=24, fam=SANS, col=RED)
        for i, lab in enumerate(["Save", "Next", "Done"]):
            c.fill_rrect(rx - 150, 700 + i * 120, 300, 80, 40, PINK)
            c.font(SANS, 28, True); c.text(rx - c.text_w(lab) / 2, 750 + i * 120, lab, DARK)
        c.rrect_path(rx - 150, 1060, 300, 80, 40); c.c.set_source_rgba(*RED, 1); c.c.set_line_width(3); c.c.stroke()
        c.font(SANS, 28, True); c.text(rx - c.text_w("Delete") / 2, 1110, "Delete", RED)
        c.pill(rx, 1200, "alag kaam, alag look ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1320, "ek jaisa kaam, ek jaisa look", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 17 script (docs/scripts/day17.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे सेवनटीन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, लॉ ऑफ़ सिमिलैरिटी क्या है? जो चीज़ें एक जैसी दिखती हैं, दिमाग़ उन्हें एक ही ग्रुप का मान लेता है। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.4, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (2.8, "pop_lo"), (3.6, "riser"), (4.4, "chime"),
                                                 (5.6, "pop_hi")]),
    Scene("इंस्टाग्राम खोलो, सबसे ऊपर स्टोरीज़। कुछ प्रोफ़ाइल्स के चारों तरफ़ रंगीन रिंग है, और कुछ की रिंग ग्रे है।",
          "", s2, min_dur=5.6, whoosh=True, sfx=[(0.3, "pop"), (2.0, "pop_hi"), (3.4, "pop_lo")]),
    Scene("बिना कुछ पढ़े, आप समझ जाते हो, रंगीन रिंग मतलब नई स्टोरी, ग्रे मतलब देख ली। और हरी रिंग, क्लोज़ फ़्रेंड्स।", "", s3,
          min_dur=6.0, whoosh=True, sfx=[(0.8, "pop_hi"), (2.0, "pop"), (3.4, "chime"), (4.6, "ding")]),
    Scene("यही है लॉ ऑफ़ सिमिलैरिटी। जिनका रंग, शेप या साइज़ एक जैसा हो, वो एक ही काम की लगती हैं।", "", s4,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "ding"), (2.4, "pop"), (3.2, "pop"), (4.0, "pop"), (4.8, "pop_hi")]),
    Scene("इसीलिए ऐप में सारे लिंक एक रंग के होते हैं, और सारे बटन एक जैसे, ताकि यूज़र तुरंत पहचान ले।", "", s5,
          min_dur=6.0, whoosh=True, sfx=[(0.6, "pop"), (1.6, "pop_hi")] + [(2.2 + i * 0.3, "pop") for i in range(3)] + [(3.2, "ding")]),
    Scene("डिज़ाइनर टिप, एक जैसा काम, एक जैसा लुक। अलग काम है, तो उसे अलग दिखाओ।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 17 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each snapped to the quietest point within 0.8 s (all in the silence between sentences); line check 8/8.
VO_CUTS = [5.12, 16.04, 23.94, 32.52, 39.84, 47.26, 53.14]

if __name__ == "__main__":
    import daily
    daily.run(17, "Law of Similarity", SCENES, "day17_law_of_similarity", cuts=VO_CUTS)

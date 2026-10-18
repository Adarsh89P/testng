"""Day 05/45 · Miller's Law (chunking), explained with Netflix's home screen: rows of a few titles, grouped by category.

We hold roughly 7±2 items in working memory. One endless list of 200 movies overloads it; short labelled rows
("Top 10", "Continue Watching", "Comedy") are easy to scan and remember. Day 02 pattern.
Voice: a NEW Day 05 voice-over (offline --generate in the reference voice, or Rakhi's own recording) at
assets/voice/day05/full.*; see docs/voice_workflow.md. (The PhonePe version lives in day05_millers_law_phonepe.py.)
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D
import day05_millers_law_phonepe as P             # shared: hook (s1), law card (s4), designer tip (s6), brain()

D.DAY, D.NEXT = 5, "Zeigarnik Effect"
W, H = 1080, 1920
NRED = (1.0, 0.22, 0.24)                          # Netflix red (brightened for the black background)
TEAL = P.TEAL
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
brain = P.brain
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def poster(c, x, y, w, h, i, a=1.0, hi=False):
    col = COLS[i % 6]
    c.drrect(x, y, w, h, 10, spacing=5, r=1.5, col=col if not hi else (1, 1, 1), a=a)
    c._dot(x + w / 2, y + h * 0.42, min(w, h) * 0.16, col, 0.8 * a)
    c.dbar(x + 8, y + h - 18, w * 0.6, rows=1, gap=4, col=DIM, a=a)


def clip_screen(c):
    c.c.save(); c.rrect_path(X0 + 14, Y0 + 110, PW - 28, PH - 130, 30); c.c.clip()


# ------------------------------------------------------------------ scenes
def s2(cv, t, d, st):                                     # story: one endless list of 200 movies
    sc = max(0, t - 1.2) * 520
    def world(c):
        mono(c, "raat · kuch dekhna hai...", 575, (0.85, 0.85, 0.88), 40)
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 90, "App X · all movies", RED)
        clip_screen(c)
        gw, gh, gap = 96, 136, 14                          # 4-wide wall of identical posters, no labels
        for i in range(200):
            r_, cc = i // 4, i % 4
            y = Y0 + 130 + r_ * (gh + gap) - sc
            if Y0 + 60 < y < Y0 + PH: poster(c, X0 + 34 + cc * (gw + gap), y, gw, gh, i * 7)
        c.c.restore()
        n = min(200, int(4 + sc / (gh + gap) * 4))
        c.pill(PX + 340, Y0 + 160, f"{n} / 200", size=34, fam=MONO, col=DARK, bg=RED if n > 60 else YELLOW, bold=True)
        if t > 3.6:
            brain(c, PX - 340, Y0 + 300, 0.7, col=RED)
            for i in range(10):
                k = ((t - 3.6) * 0.6 + i / 10) % 1
                c._dot(PX - 340 + math.sin(i * 2.3) * 80 * k, Y0 + 360 + 500 * k * k, 9, COLS[i % 6], max(0, 1 - k))
        if t > 4.4: white_pill(c, W / 2, 1600, "upar kya tha? yaad hi nahi", 36)
    stage.compose(cv, t, d, world, K((0, (PX, 900), 1.15), (1.2, ANCHOR, 1.0), (3.2, ANCHOR, 1.0),
                                     (3.8, (PX - 160, Y0 + 300), 1.35), (5.0, (PX - 160, Y0 + 300), 1.35), (5.6, ANCHOR, 1.0)),
                  seed=3)
    hud(cv)


ROWS = [("Top 10", RED), ("Continue Watching", GREEN), ("Comedy", YELLOW), ("Thriller", BLUE)]
GROUP = 1.2
def s3(cv, t, d, st):                                     # same movies, chunked into labelled rows
    def world(c):
        k = ease((t - GROUP) / 0.8)
        for ri, (lab, col) in enumerate(ROWS):
            y = 640 + ri * 230
            for j in range(6):                              # a row shows only a handful at once
                x0 = 120 + (j % 4) * 220 + (j // 4) * 40; y0 = 700 + ((ri * 7 + j) % 5) * 150   # scattered start
                x1 = 80 + j * 155; y1 = y + 40
                poster(c, lerp(x0, x1, k), lerp(y0, y1, k), 130, 170 * (0.6 + 0.4 * k) if k < 1 else 170, ri * 7 + j)
            if k > 0.3:
                c.font(SANS, 34, True); c.text(80, y + 24, lab, col, min(1, (k - 0.3) / 0.4))
        if t > 3.2:
            c.pill(W / 2, 1600, "4 rows · har row mein ~6", size=32, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > 3.8: white_pill(c, W / 2, 1680, "chhote groups = aasaani se yaad", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (2.2, ANCHOR, 1.0), (2.8, (W / 2 - 150, 760), 1.35),
                                     (3.6, (W / 2 - 150, 760), 1.35), (4.2, (W / 2, 1100), 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - GROUP - 0.8) / 0.12), seed=4)
    hud(cv); flash(cv, t, GROUP + 0.8, 0.12)


SWIPE = 3.4
def s5(cv, t, d, st):                                     # Netflix home: labelled rows, ~6 titles each
    def world(c):
        c.font(SANS, 64, True); c.text(W / 2 - c.text_w("NETFLIX") / 2, 540, "NETFLIX", NRED)
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 34, True); c.text(X0 + 30, Y0 + 92, "N", NRED)
        clip_screen(c)
        c.drrect(X0 + 26, Y0 + 120, PW - 52, 220, 16, spacing=6, r=1.6, col=NRED)      # hero banner
        c._dot(PX, Y0 + 220, 34, NRED, 0.7)
        for ri, (lab, col) in enumerate(ROWS[:3]):
            y = Y0 + 370 + ri * 160
            k = ease((t - 0.8 - ri * 0.5) / 0.5)
            c.font(SANS, 22, True); c.text(X0 + 30, y + 20, lab, col, k)
            off = (ease((t - SWIPE) / 0.8) * 230) if ri == 0 else 0
            for j in range(6):
                poster(c, X0 + 30 + j * 92 - off, y + 34, 82, 112, ri * 6 + j, a=k, hi=(ri == 0 and j == 2))
            st[f"row{ri}"] = (PX, y + 80)
        c.c.restore()
        for ri in range(3):
            if t > 1.4 + ri * 0.5:
                c.pill(PX + 330, Y0 + 450 + ri * 160, "~6 titles", size=26, fam=MONO, col=DARK, bg=ROWS[ri][1], bold=True)
        if SWIPE - 0.3 < t < SWIPE + 0.9:
            u = ease(min(1, max(0, (t - SWIPE) / 0.8)))
            c._dot(lerp(X0 + PW - 60, X0 + 140, u), Y0 + 450, 16, (1, 1, 1), 0.9)
        if t > 5.4: white_pill(c, W / 2, 1620, "categories + chhoti rows", 36)
    r0 = st.get("row0", (PX, Y0 + 450))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (2.6, ANCHOR, 1.0), (3.1, r0, 1.6), (4.5, r0, 1.6), (5.1, ANCHOR, 1.0)),
                  seed=6)
    hud(cv)


# Narration (Hinglish): the approved Day 05 script. Generated / recorded voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे फाइव।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, मिलर्स लॉ क्या है?", "", P.s1, min_dur=4.8, whoosh=True, sfx=[(1.3, "drop"), (2.5, "pop")]),
    Scene("रात को कुछ देखना था। ऐप खोला, और एक ही लंबी लिस्ट में दो सौ मूवीज़। स्क्रॉल करते करते, ये भी याद नहीं रहा कि ऊपर क्या देखा था।",
          "", s2, min_dur=6.8, whoosh=True, sfx=[(1.2 + i * 0.18, "tick") for i in range(14)] + [(3.6, "buzz")]),
    Scene("अब वही मूवीज़ छोटे ग्रुप्स में। टॉप टेन, कॉमेडी, थ्रिलर। हर लाइन में बस कुछ ही मूवीज़, और दिमाग को सब आसान लगता है।", "", s3,
          min_dur=6.0, whoosh=True, sfx=[(GROUP, "riser"), (GROUP + 0.8, "pop_hi"), (3.2, "pop"), (3.8, "ding")]),
    Scene("यही है मिलर्स लॉ। हमारा दिमाग एक बार में लगभग सात चीज़ें ही याद रख पाता है। इसलिए लंबी जानकारी को छोटे चंक्स में तोड़ो।",
          "", P.s4, min_dur=8.0, whoosh=True, sfx=[(0.2, "ding"), (2.2, "riser")] + [(2.2 + i * 0.25, "pop") for i in range(7)]
          + [(4.0, "buzz"), (5.4, "pop_hi")]),
    Scene("इसीलिए नेटफ्लिक्स होम स्क्रीन को कैटेगरीज़ में बाँटता है, और हर रो में बस कुछ टाइटल्स दिखाता है। बाकी देखने के लिए, साइड में स्वाइप करो।",
          "", s5, min_dur=7.6, whoosh=True, clicks=[SWIPE],
          sfx=[(0.8, "pop"), (1.3, "pop"), (1.8, "pop_hi"), (SWIPE, "pop_lo"), (5.4, "chime")]),
    Scene("डिज़ाइनर टिप। लंबे फॉर्म को स्टेप्स में बाँटो, और जानकारी को छोटे ग्रुप्स में दिखाओ।", "", P.s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop"), (3.6, "pop"), (4.2, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    import daily
    daily.run(5, "Miller's Law", SCENES, "day05_millers_law")

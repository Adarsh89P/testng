"""Day 14/45 · Postel's Law, explained with a phone-number login field.

Be liberal in what you accept, conservative in what you send: a good login field accepts "+91 98765 43210",
"098765 43210" or "9876543210", cleans it up itself and stores one clean format; a bad one says "invalid number".
Day 02 pattern. Voice: Rakhi's Day 14 ElevenLabs Tisha K file at assets/voice/day14/full.mp3 (content-verified);
script in docs/scripts/day14.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 14, "Law of Proximity"
W, H = 1080, 1920
TEAL = (0.20, 0.78, 0.85)                         # Postel accent
APP = (0.99, 0.45, 0.18)                          # login app orange
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
VARIANTS = ["+91 98765 43210", "098765 43210", "98765-43210", "9876543210"]
CLEAN = "98765 43210"


def field(c, x, y, w, val, col=GREY, txt=DOT, a=1.0, lw=1.6):
    c.rrect_path(x, y, w, 70, 14); c.c.set_source_rgba(*col, a); c.c.set_line_width(lw); c.c.stroke()
    c.font(MONO, 26, True); c.text(x + 20, y + 46, val, txt, a)


def login(c, title_col=APP):
    phone(c, PX, PY, PW, PH)
    c.fill_rrect(PX - 40, Y0 + 70, 80, 80, 20, title_col); c.font(SANS, 44, True); c.text(PX - 14, Y0 + 126, "f", DARK)
    c.font(SANS, 30, True); c.text(PX - c.text_w("Login") / 2, Y0 + 210, "Login", DOT)
    c.font(SANS, 20, True); c.text(X0 + 30, Y0 + 280, "Phone number", DIM)


def funnel(c, cx, cy, a=1.0, col=TEAL):
    c.dots_path([(cx - 220, cy - 120), (cx - 50, cy + 40), (cx - 50, cy + 120)], spacing=7, r=2.4, col=col, a=a)
    c.dots_path([(cx + 220, cy - 120), (cx + 50, cy + 40), (cx + 50, cy + 120)], spacing=7, r=2.4, col=col, a=a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: user jaise bhi likhe, app samjhe
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "POSTEL'S LAW", 110, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=TEAL)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "kya hai?", 980, DOT, 56, chars=int((t - 2.0) * 14))
        if t > 3.0:
            for i, v in enumerate(VARIANTS):
                k = ease(min(1, max(0, (t - 3.0 - i * 0.35) / 0.4)))
                if k > 0: c.pill(W / 2 + (i - 1.5) * 230, 1120 + (i % 2) * 70, v, size=24, fam=MONO, col=DOT, a=k)
            funnel(c, W / 2, 1360, a=ease(min(1, (t - 3.6) / 0.6)) if t > 3.6 else 0)
            if t > 4.6: c.pill(W / 2, 1530, CLEAN + "  ✓", size=30, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 5.6: c.pill(W / 2, 1640, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=TEAL, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1200), 1.0), (5.4, (W / 2, 1250), 1.0)), seed=2)
    hud(cv); flash(cv, t, 1.2)


ERR = 3.8
def s2(cv, t, d, st):                                     # strict app: "+91 98765 43210" -> Invalid number
    def world(c):
        login(c)
        v = VARIANTS[0]; n = int(max(0, (t - 0.6) * 9))
        bad = t > ERR
        field(c, X0 + 30, Y0 + 300, PW - 60, v[:n], RED if bad else GREY, RED if bad else DOT, lw=2.6 if bad else 1.6)
        if 0.6 < t < ERR and int(t * 3) % 2: c.c.set_source_rgba(*DOT, 1); c.c.rectangle(X0 + 52 + c.text_w(v[:n]), Y0 + 320, 3, 34); c.c.fill()
        if bad:
            c.font(SANS, 20, True); c.text(X0 + 30, Y0 + 405, "⚠ Invalid number", RED)
            c.font(SANS, 17, True); c.text(X0 + 30, Y0 + 435, "Sirf 10 digits daalein, bina space ke", RED)
        if t > 1.2: c.pill(PX - 100, Y0 + 520, "+91 ke saath", size=24, fam=MONO, col=DARK, bg=APP, bold=True)
        if t > 2.2: c.pill(PX + 90, Y0 + 590, "beech mein space", size=24, fam=MONO, col=DARK, bg=APP, bold=True)
        c.fill_rrect(X0 + 30, Y0 + PH - 140, PW - 60, 80, 40, (0.25, 0.25, 0.28)); c.font(SANS, 26, True)
        c.text(PX - c.text_w("Continue") / 2, Y0 + PH - 90, "Continue", DIM)
        if t > ERR + 0.9: white_pill(c, W / 2, 1640, "gussa aata hai na? 😤", 36)
    fpt = (PX, Y0 + 380)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.5, (PX, Y0 + 340), 1.35), (ERR - 0.3, (PX, Y0 + 340), 1.35),
                                     (ERR, fpt, 1.7), (d - 0.5, fpt, 1.7)),
                  punch=0.06 * max(0, 1 - abs(t - ERR) / 0.1), seed=3)
    hud(cv); flash(cv, t, ERR, 0.12)


STEP = 1.25
def s3(cv, t, d, st):                                     # forgiving app: every format gets cleaned and accepted
    def world(c):
        login(c, title_col=TEAL)
        i = min(2, int(t / STEP)); lt = t - i * STEP
        v = VARIANTS[i]
        clean = lt > 0.75 or t > 3 * STEP
        if t > 3 * STEP: v = CLEAN
        field(c, X0 + 30, Y0 + 300, PW - 60, (CLEAN if clean else v[:int(lt * 26)]), GREEN if clean else GREY,
              DOT, lw=2.4 if clean else 1.6)
        if clean: c.font(SANS, 26, True); c.text(X0 + PW - 72, Y0 + 346, "✓", GREEN)
        for j, lab in enumerate(["+91 likho ✓", "0 lagao ✓", "space daalo ✓"]):
            if t > j * STEP + 0.75: c.pill(PX, Y0 + 470 + j * 80, lab, size=24, fam=SANS, col=DARK, bg=GREEN, bold=True)
        ok = t > 3 * STEP + 0.2
        c.fill_rrect(X0 + 30, Y0 + PH - 140, PW - 60, 80, 40, TEAL if ok else (0.25, 0.25, 0.28))
        c.font(SANS, 26, True); c.text(PX - c.text_w("Continue") / 2, Y0 + PH - 90, "Continue", DARK if ok else DIM)
        if t > 3 * STEP + 0.8: white_pill(c, W / 2, 1640, "app khud saaf kar leta hai", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.5, (PX, Y0 + 460), 1.25), (3 * STEP, (PX, Y0 + 460), 1.25),
                                     (3 * STEP + 0.6, ANCHOR, 1.0), (d - 0.4, ANCHOR, 1.0)),
                  punch=0.04 * max(0, 1 - abs(t - 3 * STEP - 0.2) / 0.12), seed=4)
    hud(cv); flash(cv, t, 3 * STEP + 0.2, 0.1)


def s4(cv, t, d, st):                                     # law card: lene mein lachile, dikhane mein saaf
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "POSTEL'S LAW", 104, W / 2, 630, ease(1 - t / 0.8), col=TEAL)
        l1 = "user se jo lo: lachile raho,"; l2 = "jo dikhao: ekdum saaf raho"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 34, chars=n); mono(c, l2, 800, TEAL, 34, chars=n - len(l1))
        for i, v in enumerate(VARIANTS):
            k = ease(min(1, max(0, (t - 2.4 - i * 0.25) / 0.4)))
            if k > 0: c.pill(W / 2 + (i - 1.5) * 230, 960 + (i % 2) * 60, v, size=22, fam=MONO, col=DOT, a=k)
        if t > 3.2: funnel(c, W / 2, 1180, a=ease(min(1, (t - 3.2) / 0.5)))
        if t > 3.8: c.pill(W / 2 - 300, 1110, "accept: lachila", size=26, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > 4.4:
            c.pill(W / 2, 1360, "+91 98765 43210", size=32, fam=MONO, col=DARK, bg=TEAL, bold=True)
            c.pill(W / 2 + 300, 1250, "output: saaf", size=26, fam=MONO, col=TEAL)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.9, (W / 2, 1040), 1.0), (d - 0.4, (W / 2, 1060), 1.03)), seed=5)
    hud(cv)


OPEN = 0.6
def s5(cv, t, d, st):                                     # behind the form: every format -> one stored format
    def world(c):
        c.font(SANS, 52, True); c.text(W / 2 - c.text_w("form ke peeche") / 2, 540, "form ke peeche", TEAL)
        sx, ex = W / 2 - 250, W / 2 + 270
        for i, v in enumerate(VARIANTS):
            k = ease(min(1, max(0, (t - OPEN - i * 0.45) / 0.5)))
            if k <= 0: continue
            y = 720 + i * 150
            c.fill_rrect(sx - 180, y - 40, 360, 72, 14, (0.12, 0.13, 0.15), k)
            c.font(MONO, 24, True); c.text(sx - c.text_w(v) / 2, y + 6, v, DOT, k)
            kk = ease(min(1, max(0, (t - OPEN - i * 0.45 - 0.4) / 0.5)))
            c.dots_path([(sx + 190, y - 4), (ex - 170, 945)], spacing=9, r=2.4, col=TEAL, a=kk, reveal=kk)
        if t > OPEN + 2.0:
            k = ease(min(1, (t - OPEN - 2.0) / 0.5))
            c.fill_rrect(ex - 160, 900, 320, 90, 18, TEAL, k)
            c.font(MONO, 28, True); c.text(ex - c.text_w("+919876543210") / 2, 957, "+919876543210", DARK, k)
            c.font(SANS, 20, True); c.text(ex - c.text_w("ek hi format") / 2, 1030, "ek hi format", TEAL, k)
        if t > OPEN + 2.8: c.pill(W / 2, 1420, "har format apnao · peeche saaf karo", size=28, fam=MONO, col=DARK, bg=TEAL, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.15), (OPEN + 1.8, (W / 2, 950), 1.1), (OPEN + 2.4, (W / 2 + 60, 950), 1.1),
                                     (d - 0.4, (W / 2, 1050), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T teach the format | DO adapt to the user
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        field(c, lx - 200, 700, 400, "+91 98765 43210", RED, RED, lw=2.4)
        c.font(SANS, 18, True); c.text(lx - 200, 805, "Format: XXXXXXXXXX only", RED)
        c.font(SANS, 18, True); c.text(lx - 200, 835, "No spaces, no +91, no 0", RED)
        c.pill(lx, 1160, "user ko format sikhao ✗", size=24, fam=SANS, col=RED)
        field(c, rx - 200, 700, 400, "+91 98765 43210", GREY)
        c.dots_path([(rx, 790), (rx, 870)], spacing=8, r=2.6, col=TEAL)
        field(c, rx - 200, 890, 400, CLEAN, GREEN, lw=2.4)
        c.font(SANS, 26, True); c.text(rx + 160, 936, "✓", GREEN)
        c.pill(rx, 1160, "format user ke hisaab se ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "format ko user ke hisaab se dhaalo", 34)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 14 script (docs/scripts/day14.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे फ़ोर्टीन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, पोस्टेल्स लॉ क्या है? यूज़र जैसे भी लिखे, ऐप को समझ जाना चाहिए। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.4, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop")] + [(3.0 + i * 0.35, "pop_lo") for i in range(4)]
          + [(4.6, "chime"), (5.6, "pop_hi")]),
    Scene("किसी ऐप में लॉगिन करते वक़्त, आपने नंबर लिखा, प्लस नाइन वन के साथ, बीच में स्पेस डालकर। और ऐप बोला, इनवैलिड नंबर। गुस्सा आता है ना?",
          "", s2, min_dur=6.6, whoosh=True, sfx=[(0.6 + i * 0.11, "tick") for i in range(15)] + [(ERR, "buzz"), (ERR + 0.9, "pop")]),
    Scene("अब अच्छे ऐप्स में, प्लस नाइन वन लिखो, ज़ीरो लगाओ, या स्पेस डालो, ऐप ख़ुद साफ़ कर लेता है, और नंबर एक्सेप्ट हो जाता है।", "", s3,
          min_dur=6.2, whoosh=True, sfx=[(j * STEP + 0.75, "pop_hi") for j in range(3)] + [(3 * STEP + 0.2, "chime")]),
    Scene("यही है पोस्टेल्स लॉ। यूज़र से जो लो, उसमें लचीले रहो, और जो दिखाओ, उसमें एकदम साफ़ रहो।", "", s4,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "ding")] + [(2.4 + i * 0.25, "pop_lo") for i in range(4)] + [(3.8, "pop_hi"), (4.4, "ding")]),
    Scene("इसीलिए अच्छे फ़ॉर्म, हर फ़ॉर्मेट को अपना लेते हैं, और पीछे ख़ुद सही फ़ॉर्मेट में बदल देते हैं।", "", s5,
          min_dur=6.0, whoosh=True, sfx=[(OPEN + i * 0.45, "pop") for i in range(4)] + [(OPEN + 2.0, "riser"), (OPEN + 2.8, "ding")]),
    Scene("डिज़ाइनर टिप, यूज़र को फ़ॉर्मेट मत सिखाओ, फ़ॉर्मेट को यूज़र के हिसाब से ढालो।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 14 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [4.94, 14.38, 24.52, 32.98, 40.94, 47.86, 53.7]

if __name__ == "__main__":
    import daily
    daily.run(14, "Postel's Law", SCENES, "day14_postels_law", cuts=VO_CUTS)

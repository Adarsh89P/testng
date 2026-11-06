"""Day 24/45 · Choice Overload, explained with Netflix's "Top 10" row.

Too many options tire the brain and people choose nothing. Friday night: 30 minutes of scrolling, nothing watched.
In the well-known jam study (Iyengar & Lepper, 2000) a table of 6 flavours sold many times more than one of 24.
Netflix puts a short curated Top 10 row on top: big numbers, clear order, one glance, one tap. Day 02 pattern; the
script opens on the scrolling story and names the law from the study. Voice: Rakhi's Day 24 ElevenLabs Tisha K file
at assets/voice/day24/full.mp3 (content-verified); script in docs/scripts/day24.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 24, "Mental Models"
W, H = 1080, 1920
NRED = (1.0, 0.22, 0.24)                          # Netflix red (brightened)
JAM = [(0.75, 0.15, 0.25), (0.95, 0.55, 0.15), (0.55, 0.20, 0.55), (0.90, 0.75, 0.20), (0.35, 0.60, 0.25), (0.85, 0.35, 0.45)]
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def poster(c, x, y, w, h, i, a=1.0):
    col = COLS[i % 6]
    c.fill_rrect(x, y, w, h, 8, tuple(0.15 + cc * 0.45 for cc in col), a)
    c.dbar(x + 8, y + h - 22, w - 16, rows=1, gap=4, col=DOT)


def jar(c, x, y, s, col, a=1.0):
    c.fill_rrect(x - 18 * s, y - 34 * s, 36 * s, 10 * s, 3 * s, (0.75, 0.75, 0.78), a)
    c.fill_rrect(x - 22 * s, y - 24 * s, 44 * s, 52 * s, 9 * s, col, a)
    c.fill_rrect(x - 14 * s, y - 8 * s, 28 * s, 16 * s, 3 * s, (0.95, 0.92, 0.85), a)


def nf_header(c, a=1.0):
    phone(c, PX, PY, PW, PH)
    c.font(SANS, 40, True); c.text(X0 + 26, Y0 + 98, "N", NRED, a)
    c.font(SANS, 20, True); c.text(X0 + 80, Y0 + 92, "Shows   Movies   Categories", DOT, a)


# ------------------------------------------------------------------ scenes
GIVE = 4.6
def s1(cv, t, d, st):                                     # Friday night: 30 minutes of scrolling, watched nothing
    def world(c):
        nf_header(c)
        off = (t * 260) % 230 if t < GIVE else (GIVE * 260) % 230
        for r in range(-1, 5):
            y = Y0 + 140 + r * 230 - off
            for j in range(4):
                top, bot = max(Y0 + 120, y), min(Y0 + PH - 30, y + 180)
                if bot - top > 24:
                    poster(c, X0 + 18 + j * 114, top, 104, bot - top, r * 4 + j + int(t * 1.1))
        mins = min(30, int(t / GIVE * 30))
        c.pill(PX + 300, Y0 + 200, f"0:{mins:02d}", size=30, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        c.pill(PX + 300, Y0 + 120, "Shukravaar raat", size=22, fam=MONO, col=DOT)
        if t > 2.4: c.pill(PX + 300, Y0 + 290, "trailer… trailer…", size=22, fam=MONO, col=DOT)
        if t > GIVE:
            k = ease(min(1, (t - GIVE) / 0.5))
            c.c.new_path(); c.c.set_source_rgba(0, 0, 0, 0.7 * k); c.c.rectangle(X0, Y0, PW, PH); c.c.fill()
            white_pill(c, PX, PY, "kuch bhi nahi dekha", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 100, Y0 + 420), 1.1), (GIVE, (PX + 100, Y0 + 420), 1.1),
                                     (d - 0.4, (PX, PY), 1.15)), punch=0.05 * max(0, 1 - abs(t - GIVE) / 0.12), seed=2)
    hud(cv); flash(cv, t, GIVE, 0.08)


def s2(cv, t, d, st):                                     # jam study: 24 flavours vs 6 — the 6 table sold far more
    def table(c, cx, n, cols_per_row, at, bags, label):
        k = ease(min(1, max(0, (t - at) / 0.5)))
        c.fill_rrect(cx - 220, 1040, 440, 30, 8, (0.45, 0.32, 0.20), k)
        c.font(SANS, 36, True); c.text(cx - c.text_w(label) / 2, 700, label, DOT, k)
        for i in range(n):
            kk = ease(min(1, max(0, (t - at - i * 0.04) / 0.3)))
            r, q = divmod(i, cols_per_row)
            rows = (n + cols_per_row - 1) // cols_per_row
            x = cx - (cols_per_row - 1) * 33 + q * 66; y = 1010 - (rows - 1 - r) * 70
            jar(c, x, y, 0.9, JAM[i % 6], kk)
        if t > 2.8:
            nb = min(bags, int((t - 2.8) * 6))
            for b in range(nb):
                bx = cx - 180 + (b % 6) * 70; by = 1160 + (b // 6) * 80
                c.fill_rrect(bx, by, 50, 56, 8, (0.92, 0.85, 0.70)); c.font(SANS, 18, True); c.text(bx + 14, by + 36, "₹", DARK)
    def world(c):
        c.pill(W / 2, 560, "ek mashhoor study", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        table(c, W * 0.27, 24, 6, 0.4, 1, "24 jam")
        table(c, W * 0.73, 6, 3, 1.4, 10, "6 jam")
        if t > 4.6: c.pill(W / 2, 1450, "6 waali table: kai guna zyaada khareeda", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.2), (1.2, (W * 0.27, 900), 1.2), (2.2, (W / 2, 980), 1.0),
                                     (d - 0.4, (W / 2, 1050), 1.0)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # law named: too many options → tired brain → we give up
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "CHOICE", 120, W / 2, 620, ease(1 - t / 0.8), col=NRED)
        dot_text(c, "OVERLOAD", 120, W / 2, 750, ease(1 - (t - 0.2) / 0.8), col=NRED)
        n = int(min(60, max(0, (t - 1.4) * 30)))
        for i in range(n):
            ang = i * 2.39; rr = 40 + (i * 9) % 320
            c._dot(W / 2 + math.cos(ang) * rr * 1.2, 1150 + math.sin(ang) * rr * 0.6, 12, COLS[i % 6], 0.85)
        if t > 2.4: c.pill(W / 2, 1150, "dimaag thak gaya", size=32, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > 3.8: c.pill(W / 2, 1440, "chunne ke bajaay: chhod dete hain", size=30, fam=MONO, col=DARK, bg=NRED, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.6, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1060), 1.02)),
                  seed=4)
    hud(cv); flash(cv, t, 0.2)


def top10_row(c, y, k=1.0, hi=None):
    c.font(SANS, 24, True); c.text(X0 + 26, y - 16, "Top 10 in India Today", DOT, k)
    for i in range(4):
        x = X0 + 20 + i * 118
        c.font(SANS, 120, True); c.text(x - 6, y + 160, str(i + 1), (0.30, 0.30, 0.34), k)
        poster(c, x + 44, y, 70, 160, i + 3, k)
        if hi == i:
            c.rrect_path(x + 40, y - 4, 78, 168, 10); c.c.set_source_rgba(1, 1, 1, k); c.c.set_line_width(3); c.c.stroke()


def s4(cv, t, d, st):                                     # Netflix: a small Top 10 row on top — out of thousands, just ten
    def world(c):
        nf_header(c)
        k = ease(min(1, max(0, (t - 0.6) / 0.6)))
        for r in range(3):
            for j in range(4):
                poster(c, X0 + 18 + j * 114, Y0 + 420 + r * 150, 104, 130, r * 4 + j, 0.35)
        c.fill_rrect(X0 + 10, Y0 + 130, PW - 20, 250, 14, (0.08, 0.08, 0.09), k)
        top10_row(c, Y0 + 180, k)
        if t > 1.6: c.pill(PX + 290, Y0 + 520, "hazaaron shows", size=24, fam=MONO, col=DIM)
        if t > 2.6: c.pill(PX + 320, Y0 + 200, "bas 10", size=30, fam=SANS, col=DARK, bg=NRED, bold=True)
        if t > 3.6: c.pill(PX + 290, Y0 + 290, "bade number, saaf order", size=22, fam=MONO, col=DOT)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX + 110, Y0 + 320), 1.25), (d - 0.4, (PX + 110, Y0 + 330), 1.22)),
                  seed=5)
    hud(cv)


TAP = 1.8
def s5(cv, t, d, st):                                     # one glance, one tap, show on
    def world(c):
        nf_header(c)
        top10_row(c, Y0 + 180, 1.0, hi=0 if t > 0.6 else None)
        if TAP - 0.6 < t < TAP + 0.2:
            k = ease(min(1, (t - TAP + 0.6) / 0.6))
            c._dot(X0 + 100 + 200 * (1 - k), Y0 + 270 + 200 * (1 - k), 12, (1, 1, 1), 1)
        if t > TAP:
            k = ease(min(1, (t - TAP) / 0.5))
            c.fill_rrect(X0 + 10, Y0 + 130, PW - 20, PH - 160, 14, (0.04, 0.04, 0.05), k)
            poster(c, X0 + 30, Y0 + 170, PW - 60, 300, 3, k)
            c.c.new_path(); c.c.set_source_rgba(1, 1, 1, k); c.c.move_to(PX - 26, Y0 + 290); c.c.line_to(PX + 34, Y0 + 320)
            c.c.line_to(PX - 26, Y0 + 350); c.c.close_path(); c.c.fill()
            prog = max(0, min(1, (t - TAP - 0.6) / 2.4))
            c.fill_rrect(X0 + 30, Y0 + 500, PW - 60, 8, 4, (0.3, 0.3, 0.32), k)
            c.fill_rrect(X0 + 30, Y0 + 500, (PW - 60) * prog, 8, 4, NRED, k)
        for j, (lab, at) in enumerate([("ek nazar", 0.6), ("ek tap", TAP), ("show chaalu", TAP + 0.8)]):
            if t > at: c.pill(PX + 300, Y0 + 220 + j * 80, lab + " ✓", size=24, fam=SANS, col=DARK, bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (PX + 110, Y0 + 330), 1.22), (d - 0.4, (PX + 80, Y0 + 360), 1.15)),
                  punch=0.05 * max(0, 1 - abs(t - TAP) / 0.12), seed=6)
    hud(cv); flash(cv, t, TAP, 0.08)


def s6(cv, t, d, st):                                     # tip: don't show everything; hand-pick a few, rest on demand
    def world(c):
        c.font(SANS, 50, True); c.text(W / 2 - c.text_w("sab ek saath mat dikhao") / 2, 560, "sab ek saath mat dikhao", NRED)
        k = ease(min(1, max(0, (t - 0.8) / 1.4)))
        for i in range(30):
            sx = W / 2 - 360 + (i % 10) * 80; sy = 700 + (i // 10) * 90
            pick = i in (3, 14, 27)
            tx = W / 2 - 240 + (0 if i == 3 else 1 if i == 14 else 2) * 240 if pick else sx
            ty = 1080 if pick else sy
            a = 1 if pick else 1 - 0.75 * k
            x = sx + (tx - sx) * k; y = sy + (ty - sy) * k
            c.fill_rrect(x - 32 if not pick else x - 90 * (0.35 + 0.65 * k), y - 40 if not pick else y - 120 * (0.35 + 0.65 * k),
                         64 if not pick else 180 * (0.35 + 0.65 * k), 80 if not pick else 240 * (0.35 + 0.65 * k), 10,
                         tuple(0.15 + cc * 0.45 for cc in COLS[i % 6]), a)
        if t > 2.4:
            c.pill(W / 2, 1300, "pehle: kuch achhe options", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
            c.fill_rrect(W / 2 - 140, 1360, 280, 64, 32, (0.22, 0.22, 0.25))
            c.font(SANS, 26, True); c.text(W / 2 - c.text_w("aur dekho ›") / 2, 1402, "aur dekho ›", DOT)
        if t > 3.4: c.pill(W / 2, 1480, "baaki: zaroorat padne par", size=24, fam=MONO, col=DIM)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 1050), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 24 script (docs/scripts/day24.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी फ़ोर, और आज की कहानी, शायद आपकी भी है।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("शुक्रवार की रात। नेटफ़्लिक्स खोला, सोचा कुछ अच्छा देखेंगे। आधा घंटा स्क्रॉल किया, ट्रेलर देखे, और आख़िर में, कुछ भी नहीं देखा।",
          "", s1, min_dur=6.4, whoosh=True, sfx=[(i * 0.4, "tick") for i in range(11)] + [(2.4, "pop_lo"), (GIVE, "drop")]),
    Scene("एक मशहूर स्टडी में, दुकान पर पहले चौबीस तरह के जैम रखे गए, फिर सिर्फ़ छह। और छह वाली टेबल पर, लोगों ने कई गुना ज़्यादा ख़रीदा।",
          "", s2, min_dur=6.6, whoosh=True, sfx=[(0.4, "riser"), (1.4, "riser")] + [(2.8 + i / 6, "pop") for i in range(10)]
          + [(4.6, "chime")]),
    Scene("इसे कहते हैं, चॉइस ओवरलोड। जब ऑप्शन बहुत ज़्यादा हों, तो दिमाग़ थक जाता है, और हम चुनने के बजाय, छोड़ देते हैं।", "", s3,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "drop")] + [(1.4 + i * 0.1, "tick") for i in range(10)] + [(2.4, "buzz"), (3.8, "pop_lo")]),
    Scene("इसीलिए नेटफ़्लिक्स ने ऊपर रखी, टॉप टेन की एक छोटी सी रो। हज़ारों शोज़ में से, बस दस। बड़े नंबर, साफ़ ऑर्डर।", "", s4,
          min_dur=5.6, whoosh=True, sfx=[(0.6, "riser"), (1.6, "pop_lo"), (2.6, "chime"), (3.6, "pop_hi")]),
    Scene("अब सोचना नहीं पड़ता, कि शुरू कहाँ से करें। एक नज़र, एक टैप, और शो चालू।", "", s5, min_dur=4.6, whoosh=True,
          sfx=[(0.6, "pop_hi"), (TAP, "pop"), (TAP + 0.3, "chime"), (TAP + 0.8, "ding")]),
    Scene("तो डिज़ाइन में सब कुछ एक साथ मत दिखाओ। पहले कुछ अच्छे ऑप्शन चुनकर दो, बाक़ी, ज़रूरत पड़ने पर।", "", s6, min_dur=5.4,
          whoosh=True, sfx=[(0.8, "riser"), (2.2, "chime"), (2.4, "pop_hi"), (3.4, "pop")]),
    Scene("आपका सबसे लंबा स्क्रॉलिंग रिकॉर्ड कितना है? कमेंट में बताओ। कल मिलते हैं, मेंटल मॉडल्स के साथ।", "", D.s8, min_dur=5.0,
          whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 24 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each snapped to the quietest point within 0.8 s (all in the silence between sentences); line check 8/8.
VO_CUTS = [4.96, 15.44, 26.06, 35.04, 44.5, 50.76, 58.7]

if __name__ == "__main__":
    import daily
    daily.run(24, "Choice Overload", SCENES, "day24_choice_overload", cuts=VO_CUTS)

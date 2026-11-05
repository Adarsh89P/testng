"""Day 23/45 · Cognitive Load, explained with Google Pay's home screen.

Cognitive load is the mental effort a task needs; working memory is small, so more things at once means more
mistakes. Google Pay puts four big actions on top (Scan QR, Pay contacts, Pay phone number, Bank transfer) and shows
everyday contacts by face, so paying needs almost no thinking. Day 02 pattern; the script makes the viewer feel the
load first (hold 7-3-9-1 while thinking about dinner) and ends by asking them to comment the four numbers.
Voice: Rakhi's Day 23 ElevenLabs Tisha K file at assets/voice/day23/full.mp3 (content-verified); script in
docs/scripts/day23.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 23, "Choice Overload"
W, H = 1080, 1920
GB = (0.26, 0.52, 0.96)                           # Google blue
GPAL = [(0.26, 0.52, 0.96), (0.92, 0.26, 0.21), (0.98, 0.74, 0.02), (0.20, 0.66, 0.33)]
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
NUMS = ["7", "3", "9", "1"]
ACTIONS = [("Scan any\nQR code", "qr"), ("Pay\ncontacts", "person"), ("Pay phone\nnumber", "phone"), ("Bank\ntransfer", "bank")]
PEOPLE = [("Maa", (0.85, 0.45, 0.35)), ("Rahul", (0.35, 0.55, 0.85)), ("Priya", (0.75, 0.40, 0.65)),
          ("Kirana", (0.40, 0.70, 0.45)), ("Papa", (0.80, 0.65, 0.30))]


def load_meter(c, x, y, level, a=1.0, label=True):
    """Horizontal 'dimaag ka load' meter, level 0..1 (green→red)."""
    w = 420
    c.fill_rrect(x, y, w, 34, 17, (0.20, 0.20, 0.22), a)
    col = GREEN if level < 0.4 else YELLOW if level < 0.7 else RED
    c.fill_rrect(x, y, max(34, w * level), 34, 17, col, a)
    if label: c.font(MONO, 22, True); c.text(x, y - 14, "dimaag ka load", DIM, a)


def face(c, x, y, r, col, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x, y, r, 0, 6.2832); c.c.fill()
    for ex in (-0.32, 0.32):
        c.c.new_path(); c.c.set_source_rgba(1, 1, 1, a); c.c.arc(x + ex * r, y - 0.15 * r, 0.09 * r, 0, 6.2832); c.c.fill()
    c.c.new_path(); c.c.arc(x, y + 0.05 * r, 0.42 * r, math.radians(25), math.radians(155))
    c.c.set_source_rgba(1, 1, 1, a); c.c.set_line_width(max(2, r * 0.08)); c.c.stroke(); c.c.new_path()


def action_icon(c, kind, x, y, s, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*GB, a); c.c.arc(x, y, 46 * s, 0, 6.2832); c.c.fill()
    col = (1, 1, 1)
    if kind == "qr":
        for dx, dy in [(-1, -1), (1, -1), (-1, 1)]:
            c.rrect_path(x + dx * 12 * s - 8 * s, y + dy * 12 * s - 8 * s, 16 * s, 16 * s, 3 * s)
            c.c.set_source_rgba(*col, a); c.c.set_line_width(3 * s); c.c.stroke()
        c.fill_rrect(x + 6 * s, y + 6 * s, 10 * s, 10 * s, 2 * s, col, a)
    elif kind == "person":
        c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x, y - 8 * s, 9 * s, 0, 6.2832); c.c.fill()
        c.c.new_path(); c.c.arc(x, y + 18 * s, 17 * s, math.pi, 2 * math.pi); c.c.fill()
    elif kind == "phone":
        c.rrect_path(x - 11 * s, y - 20 * s, 22 * s, 40 * s, 5 * s); c.c.set_source_rgba(*col, a); c.c.set_line_width(3 * s); c.c.stroke()
    else:
        c.c.new_path(); c.c.set_source_rgba(*col, a)
        c.c.move_to(x - 20 * s, y - 6 * s); c.c.line_to(x, y - 20 * s); c.c.line_to(x + 20 * s, y - 6 * s); c.c.close_path(); c.c.fill()
        for dx in (-12, 0, 12): c.c.rectangle(x + dx * s - 3 * s, y - 4 * s, 6 * s, 18 * s)
        c.c.fill(); c.c.rectangle(x - 20 * s, y + 15 * s, 40 * s, 4 * s); c.c.fill()
    c.c.new_path()


def gpay(c, a=1.0, people_k=1.0, tap=None):
    phone(c, PX, PY, PW, PH)
    c.font(SANS, 30, True)
    word = "G Pay"; x = X0 + 30
    for ch_, col in zip("G", GPAL): c.text(x, Y0 + 96, ch_, col, a)
    c.text(x + c.text_w("G "), Y0 + 96, "Pay", DOT, a)
    c.fill_rrect(X0 + 20, Y0 + 130, PW - 40, 56, 28, (0.18, 0.18, 0.20), a)
    c.font(SANS, 18, True); c.text(X0 + 50, Y0 + 165, "Pay friends and merchants", DIM, a)
    for i, (lab, kind) in enumerate(ACTIONS):
        x = X0 + 64 + i * 117; y = Y0 + 260
        action_icon(c, kind, x, y, 0.95, a)
        for j, ln in enumerate(lab.split("\n")):
            c.font(SANS, 15, True); c.text(x - c.text_w(ln) / 2, y + 74 + j * 20, ln, DOT, a)
    c.font(SANS, 22, True); c.text(X0 + 30, Y0 + 420, "People", DOT, a * people_k)
    for i, (nm, col) in enumerate(PEOPLE):
        kk = ease(min(1, max(0, people_k * 5 - i)))
        x = X0 + 64 + (i % 4) * 117; y = Y0 + 490 + (i // 4) * 120
        face(c, x, y, 36, col, a * kk)
        c.font(SANS, 16, True); c.text(x - c.text_w(nm) / 2, y + 60, nm, DOT, a * kk)
        if tap == i: ring(c, x, y, tap_t[0], tap_t[1], col=(1, 1, 1))


tap_t = [0.0, 0.0]


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # task: remember 7-3-9-1 while thinking about dinner
    def world(c):
        mono(c, "ye chaar number yaad rakho", 600, DOT, 40, chars=int(t * 24))
        for i, n in enumerate(NUMS):
            at = 1.0 + i * 0.5
            if t > at: dot_text(c, n, 200, W / 2 - 300 + i * 200, 820, ease(1 - (t - at) / 0.4), col=YELLOW)
        if t > 3.4:
            k = ease(min(1, (t - 3.4) / 0.5))
            c.fill_rrect(W / 2 - 380, 1000, 760, 150, 40, (0.95, 0.95, 0.96), k)
            for j, (dx, dy, rr) in enumerate([(-300, 170, 18), (-330, 200, 10)]):
                c.c.new_path(); c.c.set_source_rgba(0.95, 0.95, 0.96, k); c.c.arc(W / 2 + dx, 1000 + dy, rr, 0, 6.2832); c.c.fill()
            c.font(SANS, 34, True); c.text(W / 2 - c.text_w("aaj raat khaane mein kya?") / 2, 1090, "aaj raat khaane mein kya?", DARK, k)
            for j, f in enumerate(["dal?", "paneer?", "pizza?", "biryani?"]):
                if t > 4.0 + j * 0.3:
                    ang = t * 1.2 + j * 1.57
                    c.pill(W / 2 + math.cos(ang) * 330, 1300 + math.sin(ang) * 80, f, size=24, fam=SANS, col=DOT)
        lvl = min(1, max(0, (t - 1.0) / 2.0) * 0.45 + max(0, (t - 3.4) / 1.6) * 0.45)
        load_meter(c, W / 2 - 210, 1480, lvl)
    stage.compose(cv, t, d, world, K((0, (W / 2, 800), 1.15), (3.2, (W / 2, 850), 1.05), (d - 0.4, (W / 2, 1100), 0.95)), seed=2)
    hud(cv)


def s2(cv, t, d, st):                                     # "thoda bhaari laga na?" → Cognitive Load named
    def world(c):
        load_meter(c, W / 2 - 210, 560, 0.92)
        c.pill(W / 2, 680, "thoda bhaari laga na?", size=34, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > 1.4:
            c.pill(W / 2, 800, "isi ko kehte hain", size=26, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
            dot_text(c, "COGNITIVE", 110, W / 2, 920, ease(1 - (t - 1.4) / 0.8), col=GB)
            dot_text(c, "LOAD", 130, W / 2, 1060, ease(1 - (t - 1.6) / 0.8), col=GB)
            c.glow(W / 2, 980, 420, 0.07)
        mono(c, "samajhne mein dimaag ki mehnat", 1200, DOT, 34, chars=int(max(0, t - 2.8) * 26))
    stage.compose(cv, t, d, world, K((0, (W / 2, 640), 1.15), (1.4, (W / 2, 900), 1.0), (d - 0.4, (W / 2, 920), 1.03)), seed=3)
    hud(cv); flash(cv, t, 1.4)


def s3(cv, t, d, st):                                     # working memory is tiny: more at once → more mistakes
    def world(c):
        c.font(SANS, 48, True); c.text(W / 2 - c.text_w("dimaag ki jagah: bahut chhoti") / 2, 560, "dimaag ki jagah: bahut chhoti", GB)
        bx, by, bw, bh = W / 2 - 170, 800, 340, 300
        c.rrect_path(bx, by, bw, bh, 26); c.c.set_source_rgba(*DOT, 1); c.c.set_line_width(4); c.c.stroke()
        n = int(min(9, max(0, (t - 0.4) * 2.6)))
        for i in range(n):
            if i < 4:
                x = bx + 85 + (i % 2) * 170; y = by + 80 + (i // 2) * 140
                c._dot(x, y, 46, COLS[i % 6], 1)
            else:
                fall = (t - 0.4 - i / 2.6) * 600
                x = bx + bw + 60 + (i % 3) * 70; y = by + 40 + fall
                if y < 1500: c._dot(x, y, 30, COLS[i % 6], 0.9)
        if n > 4: c.pill(W / 2 + 280, 760, "overflow!", size=26, fam=SANS, col=DARK, bg=RED, bold=True)
        if t > 2.6:
            for j in range(min(3, int((t - 2.6) * 3))):
                c.font(SANS, 44, True); c.text(W / 2 - 330 + j * 60, 1250, "✗", RED)
            c.pill(W / 2, 1360, "zyaada cheezein = zyaada galtiyaan", size=28, fam=MONO, col=DARK, bg=RED, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 940), 1.05), (d - 0.4, (W / 2, 980), 1.0)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # Google Pay: four big buttons on top — no thinking needed
    def world(c):
        gpay(c, a=ease(min(1, t / 0.5)), people_k=0.0)
        for i in range(4):
            at = 1.0 + i * 0.55
            if t > at: ring(c, X0 + 64 + i * 117, Y0 + 260, t, at, col=GB)
        if t > 3.4: c.pill(PX, Y0 + 430, "bade-bade, saaf button", size=24, fam=SANS, col=DARK, bg=GB, bold=True)
        load_meter(c, W / 2 - 210, 1620, max(0.15, 0.9 - 0.75 * ease(min(1, max(0, (t - 3.4) / 1.0)))))
        if t > 4.4: c.pill(W / 2, 1700, "sochna hi nahi padta", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX, Y0 + 300), 1.35), (3.2, (PX, Y0 + 300), 1.35),
                                     (4.0, (PX, PY + 120), 0.95), (d - 0.4, (PX, PY + 140), 0.95)), seed=5)
    hud(cv)


TAP = 2.8
def s5(cv, t, d, st):                                     # contacts by face: no need to read names — see, tap
    def world(c):
        tap_t[0], tap_t[1] = t, TAP
        gpay(c, people_k=ease(min(1, t / 1.2)), tap=0 if t > TAP else None)
        if t > 1.4: c.pill(PX + 310, Y0 + 470, "roz waale log", size=24, fam=MONO, col=DOT)
        if TAP - 0.6 < t < TAP + 0.2:
            k = ease(min(1, (t - TAP + 0.6) / 0.6))
            c._dot(X0 + 64 + 200 * (1 - k), Y0 + 490 + 220 * (1 - k), 12, (1, 1, 1), 1)
        if t > TAP + 0.4:
            k = ease(min(1, (t - TAP - 0.4) / 0.4))
            c.fill_rrect(X0 + 20, Y0 + 700, PW - 40, 120, 18, GB, k)
            c.font(SANS, 26, True); c.text(X0 + 40, Y0 + 748, "Pay Maa", (1, 1, 1), k)
            c.font(SANS, 40, True); c.text(X0 + 40, Y0 + 796, "₹500", (1, 1, 1), k)
        if t > TAP + 1.0: white_pill(c, W / 2, 1650, "chehra dekho, aur tap", 38)
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + 520), 1.2), (d - 0.4, (PX, Y0 + 600), 1.15)),
                  punch=0.04 * max(0, 1 - abs(t - TAP) / 0.12), seed=6)
    hud(cv); flash(cv, t, TAP, 0.08)


def s6(cv, t, d, st):                                     # tip: less to read, less to remember, less to think
    ITEMS = [("kam padhna", "Aa", 0.6), ("kam yaad rakhna", "7391", 1.6), ("kam sochna", "?", 2.6)]
    def world(c):
        c.font(SANS, 50, True); c.text(W / 2 - c.text_w("dimaag se bojh hatao") / 2, 560, "dimaag se bojh hatao", GB)
        for j, (lab, glyph, at) in enumerate(ITEMS):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            y = 680 + j * 190
            c.fill_rrect(W / 2 - 380, y, 760, 150, 22, CARD, k)
            c.fill_rrect(W / 2 - 350, y + 25, 100, 100, 20, (0.20, 0.20, 0.24), k)
            c.font(SANS, 36 if len(glyph) < 3 else 26, True); c.text(W / 2 - 300 - c.text_w(glyph) / 2, y + 88, glyph, DIM, k)
            c.c.set_source_rgba(*RED, k); c.c.rectangle(W / 2 - 345, y + 74, 90 * k, 4); c.c.fill()
            c.font(SANS, 38, True); c.text(W / 2 - 210, y + 92, lab, DOT, k)
            c.font(SANS, 40, True); c.text(W / 2 + 300, y + 92, "✓", GREEN, k)
        lvl = max(0.12, 0.85 - 0.24 * sum(1 for _, _, at in ITEMS if t > at + 0.4))
        load_meter(c, W / 2 - 210, 1320, lvl)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (d - 0.4, (W / 2, 1000), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 23 script (docs/scripts/day23.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी थ्री। पर शुरू करने से पहले, आपके लिए एक छोटा सा काम।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("ये चार नंबर याद रखो। सात, तीन, नौ, एक। और साथ-साथ ये भी सोचो, आज रात खाने में क्या बनेगा?", "", s1, min_dur=6.0,
          whoosh=True, sfx=[(1.0 + i * 0.5, "pop_hi") for i in range(4)] + [(3.4, "pop")] + [(4.0 + j * 0.3, "pop_lo") for j in range(4)]),
    Scene("थोड़ा भारी लगा ना? इसी को कहते हैं, कॉग्निटिव लोड। किसी काम को समझने में, दिमाग़ को जितनी मेहनत लगती है।", "", s2,
          min_dur=5.6, whoosh=True, sfx=[(0.2, "buzz"), (1.4, "drop"), (2.8, "pop")]),
    Scene("और दिमाग़ की ये जगह, बहुत छोटी है। जितनी ज़्यादा चीज़ें एक साथ, उतनी ज़्यादा गलतियाँ।", "", s3, min_dur=5.0,
          whoosh=True, sfx=[(0.4 + i / 2.6, "pop") for i in range(9)] + [(2.6, "buzz")]),
    Scene("अब गूगल पे खोलो। सबसे ऊपर, बड़े-बड़े बटन। स्कैन क्यू आर, पे कॉन्टैक्ट्स, पे फ़ोन नंबर, बैंक ट्रांसफ़र। पैसे भेजते वक़्त, सोचना ही नहीं पड़ता।",
          "", s4, min_dur=6.6, whoosh=True, sfx=[(1.0 + i * 0.55, "pop_hi") for i in range(4)] + [(3.4, "riser"), (4.4, "chime")]),
    Scene("नीचे आपके रोज़ वाले लोग, उनकी फ़ोटो के साथ। नाम पढ़ने की भी ज़रूरत नहीं, चेहरा देखो, और टैप।", "", s5, min_dur=5.4,
          whoosh=True, sfx=[(i * 0.24, "pop") for i in range(5)] + [(TAP, "pop_hi"), (TAP + 0.4, "chime"), (TAP + 1.0, "ding")]),
    Scene("तो जब भी स्क्रीन डिज़ाइन करो, यूज़र के दिमाग़ से बोझ हटाओ। कम पढ़ना, कम याद रखना, कम सोचना।", "", s6, min_dur=5.6,
          whoosh=True, sfx=[(0.6, "pop_hi"), (1.6, "pop_hi"), (2.6, "pop_hi"), (3.2, "ding")]),
    Scene("वैसे, वो चार नंबर याद हैं? कमेंट में लिखो। कल मिलते हैं, चॉइस ओवरलोड के साथ।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = "auto"

if __name__ == "__main__":
    import daily
    daily.run(23, "Cognitive Load", SCENES, "day23_cognitive_load", cuts=VO_CUTS)

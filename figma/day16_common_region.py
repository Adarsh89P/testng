"""Day 16/45 · Law of Common Region, explained with Swiggy restaurant cards.

Elements inside a shared boundary (border or background) are read as one group. A flat list of names, ratings,
times and offers makes it unclear which rating belongs to which restaurant; Swiggy puts each restaurant's photo,
name, rating, time and offer inside its own card. Day 02 pattern. Voice: Rakhi's Day 16 ElevenLabs Tisha K file at
assets/voice/day16/full.mp3 (content-verified); script in docs/scripts/day16.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 16, "Law of Similarity"
W, H = 1080, 1920
SWG = (0.99, 0.46, 0.16)                          # Swiggy orange
PINK = (0.95, 0.35, 0.55)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
RESTOS = [("Meghana Foods", "4.5", "30 min", "50% OFF", (0.85, 0.45, 0.20)),
          ("Behrouz Biryani", "4.2", "25 min", "₹100 OFF", (0.55, 0.35, 0.75)),
          ("Pizza Hut", "4.0", "35 min", "BUY 1 GET 1", (0.85, 0.25, 0.25))]


def star(c, x, y, rating, a=1.0):
    c.fill_rrect(x, y - 22, 74, 30, 8, GREEN, a)
    c.font(SANS, 19, True); c.text(x + 10, y, rating + " ★", DARK, a)


def food_photo(c, x, y, w, h, col, a=1.0):
    c.fill_rrect(x, y, w, h, 14, col, a * 0.85)
    c.dellipse(x + w / 2, y + h * 0.62, w * 0.28, h * 0.18, a0=0, a1=180, spacing=6, r=2.4, col=(1, 1, 1), a=a)
    c.dots_path([(x + w * 0.22, y + h * 0.62), (x + w * 0.78, y + h * 0.62)], spacing=6, r=2.4, col=(1, 1, 1), a=a)


def resto_card(c, x, y, w, r, a=1.0, region=True):
    name, rating, tm, off, col = r
    if region: c.fill_rrect(x, y, w, 200, 18, CARD, a)
    food_photo(c, x + 14, y + 14, 150, 172, col, a)
    c.font(SANS, 15, True); c.text(x + 22, y + 176, off, (1, 1, 1), a)
    c.font(SANS, 24, True); c.text(x + 182, y + 54, name, DOT, a)
    star(c, x + 182, y + 100, rating, a)
    c.font(SANS, 19, True); c.text(x + 270, y + 100, "· " + tm, DIM, a)
    c.font(SANS, 18, True); c.text(x + 182, y + 140, "Biryani, North Indian", DIM, a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: ek box ke andar = ek group
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "COMMON REGION", 96, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=SWG)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "kya hai?", 980, DOT, 56, chars=int((t - 2.0) * 14))
        if t > 2.8:
            k = ease(min(1, max(0, (t - 3.6) / 0.8)))
            if k > 0: c.fill_rrect(W / 2 - 400, 1180, 380, 160, 28, (0.30, 0.17, 0.08), k)
            for i in range(6):
                x = W / 2 - 375 + i * 150
                c._dot(x, 1260, 22, SWG if (i < 3 and k > 0.5) else DOT, 1)
            if k >= 1: c.pill(W / 2, 1430, "ek box ke andar = ek group", size=30, fam=MONO, col=DARK, bg=SWG, bold=True)
        if t > 5.6: c.pill(W / 2, 1560, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=SWG, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (2.9, (W / 2, 1200), 1.0), (5.4, (W / 2, 1230), 1.02)), seed=2)
    hud(cv); flash(cv, t, 3.6, 0.08)


Q = 3.6
def s2(cv, t, d, st):                                     # flat list: which rating belongs to whom?
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 90, "Restaurants", DOT)
        rows = []
        for r in RESTOS:
            rows += [r[0], r[1] + " ★", r[2], r[3]]
        for i, s in enumerate(rows):
            k = ease(min(1, max(0, (t - 0.3 - i * 0.12) / 0.3)))
            c.font(SANS, 22, True); c.text(X0 + 40, Y0 + 160 + i * 52, s, DOT, k)
        if t > Q:
            ry = Y0 + 160 + 5 * 52 - 8                        # second rating row
            c.c.new_path(); c.c.set_source_rgba(*RED, 1); c.c.arc(X0 + 70, ry, 34, 0, 6.3); c.c.set_line_width(3); c.c.stroke()
            for ty in (Y0 + 160 - 8, Y0 + 160 + 4 * 52 - 8):
                c.dots_path([(X0 + 110, ry), (X0 + 260, ty)], spacing=9, r=2.6, col=RED)
                c.font(SANS, 34, True); c.text(X0 + 266, ty + 12, "?", RED)
        if t > Q + 0.9: white_pill(c, W / 2, 1640, "kaun si rating kiski?", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX, Y0 + 430), 1.2), (Q - 0.2, (PX, Y0 + 430), 1.2),
                                     (Q + 0.3, (PX + 40, Y0 + 300), 1.5), (d - 0.4, (PX + 40, Y0 + 300), 1.5)),
                  punch=0.05 * max(0, 1 - abs(t - Q) / 0.1), seed=3)
    hud(cv); flash(cv, t, Q, 0.1)


def s3(cv, t, d, st):                                     # Swiggy: one card per restaurant
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 60, 10, SWG); c.font(SANS, 26, True); c.text(X0 + 30, Y0 + 90, "Swiggy", DARK)
        for i, r in enumerate(RESTOS):
            k = ease(min(1, max(0, (t - 0.5 - i * 0.5) / 0.5)))
            if k <= 0: continue
            y = Y0 + 140 + i * 230 + (1 - k) * 60
            resto_card(c, X0 + 20, y, PW - 40, r, a=k)
        if t > 2.4:
            kk = ease(min(1, (t - 2.4) / 0.4))
            c.drrect(X0 + 12, Y0 + 132, PW - 24, 216, 22, spacing=7, r=2.2, col=SWG, a=kk)
        for i, lab in enumerate(["photo", "naam", "rating · time", "offer"]):
            if t > 2.8 + i * 0.35: c.pill(PX + 340, Y0 + 170 + i * 70, lab + " ✓", size=24, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 4.6: white_pill(c, W / 2, 1640, "sab ek hi card ke andar", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (2.2, ANCHOR, 1.0), (2.7, (PX + 130, Y0 + 260), 1.25),
                                     (4.4, (PX + 130, Y0 + 260), 1.25), (4.9, ANCHOR, 1.0), (d - 0.4, ANCHOR, 1.0)),
                  punch=0.04 * max(0, 1 - abs(t - 2.4) / 0.12), seed=4)
    hud(cv); flash(cv, t, 2.4, 0.08)


def s4(cv, t, d, st):                                     # law card: a border / background groups what's inside
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "COMMON REGION", 92, W / 2, 630, ease(1 - t / 0.8), col=SWG)
        l1 = "ek border ya background,"; l2 = "andar sab ek group"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 34, chars=n); mono(c, l2, 800, SWG, 34, chars=n - len(l1))
        bk = ease(min(1, max(0, (t - 2.6) / 0.6)))
        gk = ease(min(1, max(0, (t - 3.6) / 0.6)))
        if bk > 0:
            c.rrect_path(W / 2 - 420, 980, 400, 260, 26); c.c.set_source_rgba(*BLUE, bk); c.c.set_line_width(3); c.c.stroke()
        if gk > 0: c.fill_rrect(W / 2 + 20, 980, 400, 260, 26, (0.32, 0.12, 0.20), gk)
        for r in range(2):
            for col in range(6):
                x = W / 2 - 360 + col * 145 + (0 if col < 3 else 40) - (0 if col < 3 else 40)
                x = W / 2 - 340 + col * 120 + (60 if col >= 3 else 0)
                cc = BLUE if (col < 3 and bk > 0.5) else PINK if (col >= 3 and gk > 0.5) else DOT
                c._dot(x, 1060 + r * 100, 18, cc, 1)
        if bk >= 1: c.pill(W / 2 - 220, 1300, "border", size=28, fam=MONO, col=DARK, bg=BLUE, bold=True)
        if gk >= 1: c.pill(W / 2 + 220, 1300, "background", size=28, fam=MONO, col=DARK, bg=PINK, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1030), 1.0), (d - 0.4, (W / 2, 1060), 1.03)), seed=5)
    hud(cv); flash(cv, t, 2.6, 0.06)


def s5(cv, t, d, st):                                     # cards everywhere: each card a small world
    CARDS = [("Restaurant", ["photo", "4.5 ★", "30 min"], SWG), ("Product", ["₹1,199", "-40%", "Add"], YELLOW),
             ("Song", ["▶", "3:42", "♥"], GREEN), ("Ride", ["Auto", "₹86", "4 min"], BLUE)]
    def world(c):
        c.font(SANS, 52, True); c.text(W / 2 - c.text_w("cards = chhoti duniya") / 2, 560, "cards = chhoti duniya", SWG)
        for i, (title, items, col) in enumerate(CARDS):
            k = ease(min(1, max(0, (t - 0.6 - i * 0.45) / 0.5)))
            if k <= 0: continue
            x = W / 2 - 400 + (i % 2) * 420; y = 680 + (i // 2) * 340
            c.fill_rrect(x, y, 380, 300, 22, CARD, k)
            c.fill_rrect(x + 20, y + 20, 340, 120, 14, col, 0.8 * k)
            c.font(SANS, 28, True); c.text(x + 24, y + 186, title, DOT, k)
            for j, it in enumerate(items):
                c.font(SANS, 22, True); c.text(x + 24 + j * 115, y + 250, it, DIM, k)
        if t > 3.2: c.pill(W / 2, 1420, "apni poori jaankari ke saath", size=30, fam=MONO, col=DARK, bg=SWG, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.1), (d - 0.4, (W / 2, 1000), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T float info | DO keep it in one card
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        bits = [("Meghana Foods", -120, 720), ("4.5 ★", 60, 800), ("Behrouz", -80, 880), ("30 min", 90, 950),
                ("4.2 ★", -110, 1020), ("50% OFF", 40, 1090)]
        for s, dx, y in bits:
            c.font(SANS, 22, True); c.text(lx + dx - c.text_w(s) / 2, y, s, RED if t < 2.8 else DIM)
        c.pill(lx, 1180, "sab bikhra hua ✗", size=24, fam=SANS, col=RED)
        for i, r in enumerate(RESTOS[:2]):
            y = 690 + i * 220
            c.fill_rrect(rx - 200, y, 400, 190, 18, CARD)
            if t >= 2.8: c.rrect_path(rx - 200, y, 400, 190, 18); c.c.set_source_rgba(*GREEN, 1); c.c.set_line_width(2); c.c.stroke()
            food_photo(c, rx - 186, y + 14, 110, 162, r[4])
            c.font(SANS, 20, True); c.text(rx - 60, y + 50, r[0][:14], DOT)
            star(c, rx - 60, y + 96, r[1]); c.font(SANS, 17, True); c.text(rx + 24, y + 96, r[2], DIM)
            c.font(SANS, 17, True); c.text(rx - 60, y + 140, r[3], SWG)
        c.pill(rx, 1180, "ek card, poori info ✓", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "jo saath hai, ek box mein rakho", 34)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 16 script (docs/scripts/day16.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे सिक्सटीन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, लॉ ऑफ़ कॉमन रीजन क्या है? जो चीज़ें एक ही बॉक्स के अंदर होती हैं, दिमाग़ उन्हें एक साथ मान लेता है। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.4, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (2.8, "pop_lo"), (3.6, "riser"), (4.4, "chime"),
                                                 (5.6, "pop_hi")]),
    Scene("सोचो, अगर रेस्टोरेंट के नाम, रेटिंग, टाइम और ऑफ़र, सब एक लंबी लिस्ट में बिखरे हों। कौन सी रेटिंग किस रेस्टोरेंट की है, पता ही नहीं चलता।",
          "", s2, min_dur=6.4, whoosh=True, sfx=[(0.3 + i * 0.12, "tick") for i in range(12)] + [(Q, "buzz"), (Q + 0.9, "pop")]),
    Scene("अब स्विगी पे देखो, हर रेस्टोरेंट का अपना कार्ड है। फ़ोटो, नाम, रेटिंग, टाइम और ऑफ़र, सब एक ही कार्ड के अंदर।", "", s3,
          min_dur=6.4, whoosh=True, sfx=[(0.5 + i * 0.5, "pop") for i in range(3)] + [(2.4, "chime")]
          + [(2.8 + i * 0.35, "pop_hi") for i in range(4)] + [(4.6, "ding")]),
    Scene("यही है लॉ ऑफ़ कॉमन रीजन। एक बॉर्डर या बैकग्राउंड, अंदर की सारी चीज़ों को एक ग्रुप बना देता है।", "", s4,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "ding"), (2.6, "riser"), (3.2, "pop_hi"), (3.6, "riser"), (4.2, "pop_hi")]),
    Scene("इसीलिए ऐप्स में कार्ड्स इतने काम आते हैं, हर कार्ड एक छोटी सी दुनिया है, अपनी पूरी जानकारी के साथ।", "", s5,
          min_dur=6.0, whoosh=True, sfx=[(0.6 + i * 0.45, "pop") for i in range(4)] + [(3.2, "ding")]),
    Scene("डिज़ाइनर टिप, जो जानकारी एक साथ है, उसे एक ही कार्ड या बॉक्स में रखो, ताकि यूज़र को सोचना न पड़े।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 16 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [4.92, 16.22, 26.82, 35.86, 43.36, 50.86, 58.38]

if __name__ == "__main__":
    import daily
    daily.run(16, "Law of Common Region", SCENES, "day16_common_region", cuts=VO_CUTS)

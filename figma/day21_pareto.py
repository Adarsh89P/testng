"""Day 21/45 · Pareto Principle, explained with WhatsApp putting chats front and centre.

Roughly 80% of use comes from 20% of features. People install dozens of apps but open a handful daily; WhatsApp has
Status, Channels, Communities, Payments and Stickers, yet most of the day is chats, so chats are the first screen
and everything else is one tap away. Day 02 pattern; the script opens on the viewer's own phone and names the law
as the punchline. Voice: Rakhi's Day 21 ElevenLabs Tisha K file at assets/voice/day21/full.mp3 (content-verified);
script in docs/scripts/day21.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D
import day19_pragnanz as P                        # WhatsApp icons / screen (sets D.DAY on import; reset below)

D.DAY, D.NEXT = 21, "Parkinson's Law"
W, H = 1080, 1920
WA, WAD = P.WA, P.WAD
GOLD = (1.0, 0.78, 0.20)                          # the vital 20%
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = P.PX, P.PY, P.PW, P.PH
X0, Y0 = P.X0, P.Y0
DAILY = {3, 9, 14, 20, 27, 33}                    # the handful of apps opened every day


def app_grid(c, n, hi=0.0, a=1.0):
    for i in range(n):
        r, col = divmod(i, 5)
        x = X0 + 62 + col * 89; y = Y0 + 120 + r * 92
        daily = i in DAILY
        dim = 1 - 0.75 * hi if not daily else 1
        c.fill_rrect(x - 30, y - 30, 60, 60, 16, COLS[i % 6], 0.85 * dim * a)
        if daily and hi > 0.5:
            c.rrect_path(x - 36, y - 36, 72, 72, 20); c.c.set_source_rgba(*GOLD, a); c.c.set_line_width(4); c.c.stroke()


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # your phone: 40-60 apps, but you open 5-6 daily
    def world(c):
        phone(c, PX, PY, PW, PH)
        n = min(40, int(max(0, t - 0.3) * 22))
        hi = ease(min(1, max(0, (t - 4.4) / 0.6)))
        app_grid(c, n, hi)
        cnt = {0: "", 1: "chaalees?", 2: "saath?"}[0 if t < 1.6 else 1 if t < 2.6 else 2]
        if cnt: c.pill(PX + 330, Y0 + 200, cnt, size=30, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t > 3.4: c.pill(PX + 330, Y0 + 300, "roz kitne?", size=28, fam=MONO, col=DOT)
        if t > 5.0: white_pill(c, W / 2, 1640, "shaayad sirf 5-6", 40)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.0, (PX + 90, Y0 + 400), 1.12), (d - 0.4, (PX + 60, Y0 + 420), 1.1)),
                  punch=0.04 * max(0, 1 - abs(t - 4.4) / 0.12), seed=2)
    hud(cv); flash(cv, t, 4.4, 0.08)


CHAT = 3.8
def s2(cv, t, d, st):                                     # WhatsApp has lots of features — people mostly just chat
    FEATS = ["Status", "Channels", "Communities", "Payments", "Stickers"]
    def world(c):
        cx, cy = W / 2, 1000
        for i, f in enumerate(FEATS):
            at = 0.4 + i * 0.4
            if t < at: continue
            k = ease(min(1, (t - at) / 0.4))
            ang = -math.pi / 2 + i / len(FEATS) * 6.2832 + t * 0.15
            fade = 1 - 0.65 * ease(min(1, max(0, (t - CHAT) / 0.6)))
            c.pill(cx + math.cos(ang) * 330 * k, cy + math.sin(ang) * 280 * k, f, size=28, fam=SANS, col=DOT, a=fade)
        if t > 2.6: c.pill(W / 2, 600, "dher saare features", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        s = 1.0 + 0.6 * ease(min(1, max(0, (t - CHAT) / 0.6)))
        P.icon(c, "chats", cx, cy, 1.6 * s, WA)
        if t > CHAT + 0.6:
            c.font(SANS, 44, True); c.text(cx - c.text_w("bas chat.") / 2, cy + 190, "bas chat.", WA)
    stage.compose(cv, t, d, world, K((0, (W / 2, 1000), 1.0), (CHAT, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1040), 1.12)),
                  punch=0.05 * max(0, 1 - abs(t - CHAT) / 0.12), seed=3)
    hud(cv); flash(cv, t, CHAT, 0.08)


def s3(cv, t, d, st):                                     # app opens straight on Chats; the rest one tap away
    def world(c):
        k = ease(min(1, t / 0.6))
        P.wa_screen(c, labels=1.0, sel=0, a=k)
        if t > 0.8:
            c.drrect(X0 + 14, Y0 + 130, PW - 28, 500, 18, spacing=7, r=2.2, col=GOLD)
            c.pill(PX, Y0 + 660, "sabse pehle: chats", size=26, fam=SANS, col=DARK, bg=GOLD, bold=True)
        if t > 2.2:
            by = Y0 + PH - 110
            for i in range(1, 4): ring(c, X0 + 60 + i * 120, by, t, 2.2 + i * 0.2, col=DIM)
            c.pill(PX + 60, by - 90, "baaki sab: ek tap door", size=24, fam=MONO, col=DOT)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX, Y0 + 400), 1.12), (2.0, (PX, Y0 + 520), 1.12),
                                     (d - 0.4, (PX, Y0 + 560), 1.15)), seed=4)
    hud(cv)


def bar(c, x, y, w, split, lab_l, lab_r, cl, cr, k=1.0):
    h = 70
    c.fill_rrect(x, y, w * split * k, h, 12, cl)
    if k >= 1:
        c.fill_rrect(x + w * split + 6, y, w * (1 - split) - 6, h, 12, cr)
        c.font(SANS, 26, True); c.text(x + 16, y + 46, lab_l, DARK)
        c.font(SANS, 26, True); c.text(x + w * split + 22, y + 46, lab_r, DARK if cr != CARD else DIM)


def s4(cv, t, d, st):                                     # law named: 80/20
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "PARETO", 110, W / 2, 610, ease(1 - t / 0.8), col=GOLD)
        dot_text(c, "PRINCIPLE", 80, W / 2, 710, ease(1 - (t - 0.2) / 0.8), col=GOLD)
        if t > 1.8:
            dot_text(c, "80 / 20", 120, W / 2, 870, ease(1 - (t - 1.8) / 0.6), col=DOT)
        x, w = W / 2 - 400, 800
        if t > 3.0:
            c.font(SANS, 24, True); c.text(x, 1010, "features", DIM)
            bar(c, x, 1030, w, 0.2, "20%", "80%", GOLD, CARD, ease(min(1, (t - 3.0) / 0.6)))
        if t > 3.8:
            c.font(SANS, 24, True); c.text(x, 1180, "istemaal", DIM)
            bar(c, x, 1200, w, 0.8, "80%", "20%", GOLD, CARD, ease(min(1, (t - 3.8) / 0.6)))
        if t > 4.6:
            c.dots_path([(x + w * 0.1, 1110), (x + w * 0.4, 1190)], spacing=8, r=2.6, col=GOLD)
            c.pill(W / 2, 1360, "thode features, zyaada kaam", size=28, fam=MONO, col=DARK, bg=GOLD, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 660), 1.2), (1.8, (W / 2, 820), 1.0), (3.0, (W / 2, 1050), 1.0),
                                     (d - 0.4, (W / 2, 1070), 1.02)), seed=5)
    hud(cv); flash(cv, t, 1.8, 0.08)


def s5(cv, t, d, st):                                     # beyond apps: bugs per screen, sales per product
    def chart(c, x, y, title, vals, at, col):
        c.fill_rrect(x, y, 420, 560, 22, CARD)
        c.font(SANS, 28, True); c.text(x + 24, y + 50, title, DOT)
        k = ease(min(1, max(0, (t - at) / 0.9)))
        for i, v in enumerate(vals):
            bh = 380 * v * k
            c.fill_rrect(x + 30 + i * 46, y + 520 - bh, 34, bh, 6, col if i < 2 else (0.30, 0.30, 0.34))
        if k >= 1: c.pill(x + 210, y + 610, "2 se hi zyaada", size=24, fam=MONO, col=DARK, bg=col, bold=True)
    def world(c):
        c.font(SANS, 50, True); c.text(W / 2 - c.text_w("sirf apps mein nahi") / 2, 560, "sirf apps mein nahi", GOLD)
        vals = [1.0, 0.72, 0.18, 0.12, 0.09, 0.07, 0.05, 0.04]
        chart(c, W / 2 - 450, 660, "bugs / screen", vals, 0.5, RED)
        if t > 2.4: chart(c, W / 2 + 30, 660, "sale / product", vals, 2.6, GREEN)
    stage.compose(cv, t, d, world, K((0, (W / 2 - 240, 960), 1.2), (2.2, (W / 2 - 240, 960), 1.2), (3.0, (W / 2, 980), 1.0),
                                     (d - 0.4, (W / 2, 1000), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # exercise: find your users' 20%, put it first, polish it most
    ROWS = [("Search", 8), ("Settings", 2), ("Checkout", 9), ("Help", 1), ("Wishlist", 3), ("Share", 2), ("Reviews", 2),
            ("Themes", 1), ("Track order", 7), ("About", 1)]
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("aapka 20% kya hai?") / 2, 560, "aapka 20% kya hai?", GOLD)
        k = ease(min(1, max(0, (t - 1.4) / 1.2)))
        order = sorted(range(len(ROWS)), key=lambda i: -ROWS[i][1])
        for i, (lab, use) in enumerate(ROWS):
            ry = order.index(i)
            y = 650 + (i + (ry - i) * k) * 78
            top = ry < 2 and k >= 1
            c.fill_rrect(W / 2 - 360, y, 720, 64, 14, (0.30, 0.24, 0.06) if top else CARD)
            c.font(SANS, 26, True); c.text(W / 2 - 330, y + 42, lab, GOLD if top else DOT)
            c.fill_rrect(W / 2 + 80, y + 22, 25 * use * min(1, t / 1.0), 20, 8, GOLD if top else GREY)
            if top and t > 3.2: c.font(SANS, 22, True); c.text(W / 2 + 250, y + 42, "polish ✓", GREEN)
        if t > 3.0: c.pill(W / 2, 1460, "sabse aage + sabse zyaada polish", size=28, fam=MONO, col=DARK, bg=GOLD, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1020), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 21 script (docs/scripts/day21.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी वन। पैंतालीस यू एक्स लॉज़ का सफ़र, अब आधे के पार।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("अपना फ़ोन उठाओ, और गिनो। कितने ऐप्स हैं? चालीस? साठ? अब सोचो, रोज़ खोलते कितने हो? शायद, पाँच या छह।", "", s1,
          min_dur=6.2, whoosh=True, sfx=[(0.3 + i * 0.09, "tick") for i in range(20)] + [(1.6, "pop"), (2.6, "pop"), (3.4, "pop_lo"),
                                                                                       (4.4, "chime"), (5.0, "ding")]),
    Scene("वॉट्सऐप में भी यही होता है। स्टेटस, चैनल्स, कम्युनिटीज़, पेमेंट्स, स्टिकर्स, ढेर सारे फ़ीचर्स। पर ज़्यादातर लोग, दिन भर करते क्या हैं? बस चैट।",
          "", s2, min_dur=6.4, whoosh=True, sfx=[(0.4 + i * 0.4, "pop") for i in range(5)] + [(2.6, "pop_lo"), (CHAT, "drop")]),
    Scene("इसीलिए वॉट्सऐप खुलते ही, सबसे पहले आपकी चैट्स दिखती हैं। बाक़ी सब, एक टैप दूर।", "", s3, min_dur=4.6, whoosh=True,
          sfx=[(0.2, "pop_hi"), (0.8, "chime"), (2.2, "pop_lo")]),
    Scene("इसे कहते हैं, पेरेटो प्रिंसिपल, या अस्सी-बीस का रूल। अस्सी परसेंट इस्तेमाल, सिर्फ़ बीस परसेंट फ़ीचर्स से आता है।", "", s4,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "drop"), (1.8, "riser"), (3.0, "pop"), (3.8, "pop"), (4.6, "ding")]),
    Scene("और ये सिर्फ़ ऐप्स में नहीं। ज़्यादातर बग्स, कुछ ही स्क्रीन्स में मिलते हैं। ज़्यादातर सेल, कुछ ही प्रोडक्ट्स से आती है।", "", s5,
          min_dur=5.8, whoosh=True, sfx=[(0.5, "riser"), (1.4, "pop_hi"), (2.6, "riser"), (3.5, "pop_hi")]),
    Scene("तो डिज़ाइन शुरू करने से पहले, पता करो, आपके यूज़र्स का वो बीस परसेंट क्या है। उसे सबसे आगे रखो, और सबसे ज़्यादा पॉलिश करो।", "", s6,
          min_dur=6.4, whoosh=True, sfx=[(1.4, "riser"), (2.6, "chime"), (3.0, "ding"), (3.2, "pop_hi")]),
    Scene("कल का लॉ, पार्किंसन्स लॉ। मिलते हैं, डिज़ाइन विद राखी पे।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 21 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [5.14, 15.54, 26.92, 33.82, 41.64, 49.24, 58.6]

if __name__ == "__main__":
    import daily
    daily.run(21, "Pareto Principle", SCENES, "day21_pareto", cuts=VO_CUTS)

"""Day 27/45 · Scarcity, explained with Amazon's "Only 2 left in stock".

Things that are rare or running out feel more valuable: ten samosas, nobody hurries; one left, everyone wants it.
Amazon's small red "Only 2 left in stock" line pushes the hand to Buy Now, because losing feels stronger than gaining.
Twist: fake scarcity on every product is spotted and trust breaks, so show it only when it's real. Day 02 pattern.
Voice: Rakhi's Day 27 ElevenLabs Tisha K file at assets/voice/day27/full.mp3 (content-verified); script in
docs/scripts/day27.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 27, "Social Proof"
W, H = 1080, 1920
AMZ = (1.0, 0.60, 0.0)
AMY = (1.0, 0.85, 0.10)
STOCK = (0.95, 0.25, 0.25)                        # "only 2 left" red
SAMOSA = (0.85, 0.62, 0.25)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def samosa(c, x, y, s=1.0, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*SAMOSA, a)
    c.c.move_to(x, y - 34 * s); c.c.line_to(x + 36 * s, y + 26 * s); c.c.line_to(x - 36 * s, y + 26 * s); c.c.close_path(); c.c.fill()
    c.c.new_path(); c.c.set_source_rgba(0.65, 0.42, 0.12, a); c.c.set_line_width(2 * s)
    c.c.move_to(x - 10 * s, y + 4 * s); c.c.line_to(x + 12 * s, y + 4 * s); c.c.stroke(); c.c.new_path()


def product_page(c, stock_k=1.0, press=False):
    phone(c, PX, PY, PW, PH)
    c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 60, 10, (0.08, 0.11, 0.16)); c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 90, "amazon.in", DOT)
    c.fill_rrect(X0 + 30, Y0 + 130, PW - 60, 280, 16, CARD)
    c.dellipse(PX, Y0 + 270, 90, 90, spacing=7, r=2.4, col=DOT)
    c.dellipse(PX, Y0 + 270, 40, 40, spacing=6, r=2, col=DIM)
    c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 450, "Smart Watch Pro", DOT)
    c.font(SANS, 40, True); c.text(X0 + 30, Y0 + 505, "₹2,999", DOT)
    c.font(SANS, 18, True); c.text(X0 + 190, Y0 + 503, "M.R.P. ₹5,999", DIM)
    if stock_k > 0:
        pulse = 0.85 + 0.15 * math.sin(stock_k * 9)
        c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 555, "Only 2 left in stock.", STOCK, min(1, stock_k) * pulse)
    c.fill_rrect(X0 + 30, Y0 + 600 + (4 if press else 0), PW - 60, 70, 35, AMY)
    c.font(SANS, 24, True); c.text(PX - c.text_w("Add to Cart") / 2, Y0 + 645, "Add to Cart", DARK)
    c.fill_rrect(X0 + 30, Y0 + 690 + (4 if press else 0), PW - 60, 70, 35, AMZ)
    c.font(SANS, 24, True); c.text(PX - c.text_w("Buy Now") / 2, Y0 + 735, "Buy Now", DARK)


# ------------------------------------------------------------------ scenes
LAST = 3.0
def s1(cv, t, d, st):                                     # samosa plate: ten → nobody hurries; one left → everyone wants it
    def world(c):
        cx, cy = W / 2, 980
        c.dellipse(cx, cy, 330, 150, spacing=8, r=2.6, col=DOT)
        n = 10 if t < 1.2 else max(1, 10 - int((t - 1.2) * 6))
        pos = [(cx - 200 + (i % 5) * 100, cy - 40 + (i // 5) * 90) for i in range(10)]
        for i in range(n): samosa(c, *pos[i] if n > 1 else (cx, cy), 1.1)
        c.pill(W / 2, 640, f"{n} samose" if n > 1 else "1 samosa", size=34, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t < 1.6: c.pill(W / 2, 1240, "koi jaldi nahi…", size=28, fam=MONO, col=DOT)
        if t > LAST:
            k = ease(min(1, (t - LAST) / 0.8))
            for j in range(6):
                ang = j / 6 * 6.2832 + 0.3
                r = 420 - 220 * k
                c.dots_path([(cx + math.cos(ang) * 520, cy + math.sin(ang) * 380), (cx + math.cos(ang) * r, cy + math.sin(ang) * r * 0.7)],
                            spacing=10, r=3, col=COLS[j % 6])
                c._dot(cx + math.cos(ang) * r, cy + math.sin(ang) * r * 0.7, 18, COLS[j % 6], 1)
            ring(c, cx, cy, t, LAST, col=AMY)
        if t > LAST + 0.9: white_pill(c, W / 2, 1360, "achaanak sabko wahi chahiye!", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (LAST, (W / 2, 980), 1.15), (d - 0.4, (W / 2, 1060), 1.05)),
                  punch=0.05 * max(0, 1 - abs(t - LAST) / 0.12), seed=2)
    hud(cv); flash(cv, t, LAST, 0.08)


TAP = 3.6
def s2(cv, t, d, st):                                     # Amazon: small red line → hand goes straight to Buy Now
    def world(c):
        product_page(c, stock_k=(t - 1.0) if t > 1.0 else 0, press=TAP < t < TAP + 0.25)
        if t > 1.2:
            ring(c, X0 + 150, Y0 + 547, t, 1.2, col=STOCK)
            c.pill(PX + 120, Y0 + 445, "chhoti si laal line ↓", size=22, fam=MONO, col=DARK, bg=STOCK, bold=True)
        if TAP - 1.0 < t < TAP + 0.3:
            k = ease(min(1, (t - TAP + 1.0) / 1.0))
            c._dot(PX + 200 - 200 * k, Y0 + 900 - 175 * k, 13, (1, 1, 1), 1)
        if t > TAP + 0.4: white_pill(c, W / 2, 1660, "haath seedha Buy Now par", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX + 60, Y0 + 560), 1.3), (TAP - 0.6, (PX + 60, Y0 + 600), 1.25),
                                     (d - 0.4, (PX, Y0 + 640), 1.15)), punch=0.05 * max(0, 1 - abs(t - TAP) / 0.12), seed=3)
    hud(cv); flash(cv, t, TAP, 0.08)


def s3(cv, t, d, st):                                     # law named: rare / running out = more valuable
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "SCARCITY", 140, W / 2, 650, ease(1 - t / 0.8), col=STOCK)
        c.glow(W / 2, 650, 420, 0.07)
        k = min(1, max(0, (t - 1.4) / 2.4))
        n = 10 - int(9 * k)
        for i in range(10):
            on = i < n
            c.fill_rrect(W / 2 - 400 + i * 82, 900, 66, 120, 12, STOCK if on else (0.18, 0.18, 0.20))
        c.font(MONO, 30, True); c.text(W / 2 - 400, 880, f"stock: {n}", DOT)
        val = 0.2 + 0.8 * k
        c.font(SANS, 30, True); c.text(W / 2 - 400, 1120, "qeemat (lagti hai)", DIM)
        c.fill_rrect(W / 2 - 400, 1140, 800, 40, 20, (0.20, 0.20, 0.22))
        c.fill_rrect(W / 2 - 400, 1140, 800 * val, 40, 20, AMY)
        if t > 3.8: c.pill(W / 2, 1300, "kam = zyaada qeemti", size=32, fam=MONO, col=DARK, bg=STOCK, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1040), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


def s4(cv, t, d, st):                                     # why: fear of losing outweighs joy of gaining
    def world(c):
        c.font(SANS, 52, True); c.text(W / 2 - c.text_w("wajah seedhi hai") / 2, 560, "wajah seedhi hai", AMY)
        tilt = 0.32 * ease(min(1, max(0, (t - 1.0) / 1.0)))
        cx, cy = W / 2, 900
        L = 340
        x1, y1 = cx - L * math.cos(tilt), cy + L * math.sin(tilt)
        x2, y2 = cx + L * math.cos(tilt), cy - L * math.sin(tilt)
        c.dots_path([(cx, cy), (cx, cy + 420)], spacing=8, r=3, col=DOT)
        c.dots_path([(x1, y1), (x2, y2)], spacing=8, r=3, col=DOT)
        for (px, py, lab, col, w) in [(x1, y1, "khona", STOCK, 220), (x2, y2, "paana", GREEN, 150)]:
            c.dots_path([(px, py), (px - w / 2, py + 120)], spacing=7, r=2, col=DIM)
            c.dots_path([(px, py), (px + w / 2, py + 120)], spacing=7, r=2, col=DIM)
            c.fill_rrect(px - w / 2, py + 120, w, 80 + (40 if lab == "khona" else 0), 14, col)
            c.font(SANS, 30, True); c.text(px - c.text_w(lab) / 2, py + 172, lab, DARK)
        if t > 2.4: c.pill(W / 2, 1420, "kahin chhoot na jaaye… (FOMO)", size=30, fam=SANS, col=DARK, bg=AMY, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 1000), 1.02)), seed=5)
    hud(cv)


CATCH = 2.6
def s5(cv, t, d, st):                                     # twist: "only 2 left" on everything → user catches on, trust breaks
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("par dhyaan rahe") / 2, 560, "par dhyaan rahe", STOCK)
        for i in range(6):
            at = 0.3 + i * 0.25
            k = ease(min(1, max(0, (t - at) / 0.4)))
            x = W / 2 - 400 + (i % 3) * 280; y = 660 + (i // 3) * 300
            c.fill_rrect(x, y, 240, 260, 16, CARD, k)
            c.fill_rrect(x + 15, y + 15, 210, 140, 10, tuple(0.2 + cc * 0.35 for cc in COLS[i % 6]), k)
            c.font(SANS, 20, True); c.text(x + 15, y + 200, "Only 2 left!", STOCK, k)
            c.font(SANS, 18, True); c.text(x + 15, y + 235, "hamesha", DIM, k)
        if t > CATCH:
            c.pill(W / 2, 1300, "har jagah 'sirf 2'?", size=30, fam=SANS, col=DARK, bg=YELLOW, bold=True)
            tk = 1 - 0.85 * ease(min(1, (t - CATCH - 0.6) / 1.0))
            c.font(MONO, 24, True); c.text(W / 2 - 300, 1380, "bharosa", DIM)
            c.fill_rrect(W / 2 - 300, 1400, 600, 36, 18, (0.20, 0.20, 0.22))
            c.fill_rrect(W / 2 - 300, 1400, max(36, 600 * tk), 36, 18, GREEN if tk > 0.5 else STOCK)
        if t > CATCH + 1.8: c.pill(W / 2, 1500, "bharosa toot gaya", size=30, fam=SANS, col=DARK, bg=STOCK, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 1080), 0.98)),
                  punch=0.04 * max(0, 1 - abs(t - CATCH - 1.6) / 0.12), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # tip: show scarcity only when it's real
    ROWS = [("sachcha stock", "7 left · live update", GREEN, 0.5), ("sachchi deadline", "Sale ends 11:59 PM", GREEN, 1.3),
            ("jhootha darr", "ek baar ✓ · baar-baar ✗", STOCK, 2.4)]
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("tabhi dikhao, jab sach ho") / 2, 560, "tabhi dikhao, jab sach ho", AMY)
        for j, (lab, sub, col, at) in enumerate(ROWS):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            y = 660 + j * 200
            c.fill_rrect(W / 2 - 400, y, 800, 170, 22, CARD, k)
            c.fill_rrect(W / 2 - 400, y, 10, 170, 5, col, k)
            c.font(SANS, 38, True); c.text(W / 2 - 360, y + 72, lab, col, k)
            c.font(SANS, 26, True); c.text(W / 2 - 360, y + 124, sub, DOT, k)
        if t > 3.6: white_pill(c, W / 2, 1340, "real scarcity = trust + sales", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (d - 0.4, (W / 2, 990), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 27 script (docs/scripts/day27.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी सेवन। और आज, एक प्लेट समोसे से शुरू करते हैं।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("प्लेट में दस समोसे हों, तो कोई जल्दी नहीं करता। पर जैसे ही आख़िरी एक बचता है, अचानक सबको वही चाहिए।", "", s1, min_dur=5.6,
          whoosh=True, sfx=[(1.2 + i / 6, "pop_lo") for i in range(9)] + [(LAST, "drop"), (LAST + 0.9, "ding")]),
    Scene("ऐमज़ॉन पे भी यही होता है। प्रोडक्ट के नीचे, छोटी सी लाल लाइन। ओनली टू लेफ़्ट इन स्टॉक। और आपका हाथ, सीधा बाय नाउ पर।", "", s2,
          min_dur=6.2, whoosh=True, sfx=[(1.0, "pop"), (1.2, "buzz"), (TAP, "pop_hi"), (TAP + 0.2, "chime")]),
    Scene("इसे कहते हैं, स्कार्सिटी। जो चीज़ कम है, या जल्दी ख़त्म होने वाली है, वो हमें ज़्यादा क़ीमती लगती है।", "", s3, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "drop")] + [(1.4 + i * 0.27, "tick") for i in range(9)] + [(3.8, "ding")]),
    Scene("वजह सीधी है। हमें खोने का डर, पाने की ख़ुशी से ज़्यादा लगता है। कहीं छूट न जाए, बस यही सोच।", "", s4, min_dur=5.0,
          whoosh=True, sfx=[(1.0, "riser"), (2.0, "drop"), (2.4, "pop_hi")]),
    Scene("पर ध्यान रहे। अगर हर प्रोडक्ट पर हमेशा, सिर्फ़ दो बचे हैं लिखा हो, तो यूज़र समझ जाता है, और भरोसा टूट जाता है।", "", s5,
          min_dur=6.0, whoosh=True, sfx=[(0.3 + i * 0.25, "pop") for i in range(6)] + [(CATCH, "buzz"), (CATCH + 1.6, "drop")]),
    Scene("तो स्कार्सिटी तभी दिखाओ, जब वो सच में हो। सच्चा स्टॉक, सच्ची डेडलाइन। झूठा डर, एक बार चलता है, बार-बार नहीं।", "", s6,
          min_dur=6.2, whoosh=True, sfx=[(0.5, "pop_hi"), (1.3, "pop_hi"), (2.4, "buzz"), (3.6, "ding")]),
    Scene("आख़िरी बार ओनली फ़्यू लेफ़्ट देखकर, आपने क्या ख़रीदा था? कमेंट में बताओ। कल मिलते हैं, सोशल प्रूफ़ के साथ।", "", D.s8,
          min_dur=5.0, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 27 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [4.66, 13.12, 23.02, 30.54, 38.72, 47.54, 56.9]

if __name__ == "__main__":
    import daily
    daily.run(27, "Scarcity", SCENES, "day27_scarcity", cuts=VO_CUTS)

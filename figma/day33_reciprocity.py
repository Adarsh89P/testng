"""Day 33/45 · Reciprocity, explained with Canva's free templates.

When someone gives first, we want to give back. Canva gives templates, fonts and photos free (a post in five minutes,
no sign-up, no talk of money); then a small crown says Pro and people pay happily. In a restaurant study a small sweet
with the bill raised tips (Strohmetz et al., 2002). Give first, ask later; half-products or paywalls at every step
feel like cheating. Day 02 pattern; open-loop hook before the day number. Voice: Rakhi's Day 33 ElevenLabs Tisha K
file at assets/voice/day33/full.mp3 (content-verified); script in docs/scripts/day33.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 33, "Commitment & Consistency"
W, H = 1080, 1920
CAN = (0.0, 0.77, 0.80)                           # Canva teal
CPUR = (0.49, 0.30, 0.98)                         # Canva purple
GOLD = (1.0, 0.78, 0.25)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def crown(c, x, y, s=1.0, col=GOLD, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*col, a)
    pts = [(-20, 10), (-20, -8), (-10, 2), (0, -14), (10, 2), (20, -8), (20, 10)]
    c.c.move_to(x + pts[0][0] * s, y + pts[0][1] * s)
    for px, py in pts[1:]: c.c.line_to(x + px * s, y + py * s)
    c.c.close_path(); c.c.fill(); c.c.new_path()


def canva_head(c, a=1.0):
    phone(c, PX, PY, PW, PH)
    c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 70, 14, CPUR, a)
    c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 98, "Canva", (1, 1, 1), a)


def template(c, x, y, w, h, i, a=1.0, pro=False):
    col = COLS[i % 6]
    c.fill_rrect(x, y, w, h, 12, tuple(0.15 + cc * 0.5 for cc in col), a)
    c.fill_rrect(x + 12, y + 14, w * 0.6, 14, 6, (1, 1, 1), 0.8 * a)
    c.fill_rrect(x + 12, y + 36, w * 0.4, 10, 5, (1, 1, 1), 0.5 * a)
    c.c.new_path(); c.c.set_source_rgba(1, 1, 1, 0.35 * a); c.c.arc(x + w * 0.6, y + h * 0.62, h * 0.22, 0, 6.2832); c.c.fill()
    if pro:
        c.c.new_path(); c.c.set_source_rgba(0, 0, 0, 0.6 * a); c.c.arc(x + w - 24, y + 24, 18, 0, 6.2832); c.c.fill()
        crown(c, x + w - 24, y + 26, 0.6, GOLD, a)
    else:
        c.fill_rrect(x + w - 62, y + h - 34, 52, 24, 8, (0, 0, 0), 0.5 * a)
        c.font(SANS, 14, True); c.text(x + w - 54, y + h - 17, "FREE", (1, 1, 1), a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # Canva: thousands of free templates → post ready in 5 min, no sign-up
    def world(c):
        canva_head(c)
        n = min(8, int(t * 4) + 1)
        for i in range(n):
            template(c, X0 + 24 + (i % 2) * 220, Y0 + 140 + (i // 2) * 160, 208, 148, i)
        for j, (lab, at) in enumerate([("templates", 0.8), ("fonts", 1.3), ("photos", 1.8)]):
            if t > at: c.pill(PX + 285, Y0 + 170 + j * 70, lab + " · FREE", size=22, fam=SANS, col=DARK, bg=CAN, bold=True)
        if t > 2.8:
            secs = min(300, int((t - 2.8) * 200))
            c.pill(PX + 285, Y0 + 420, f"post ready · {secs // 60}:{secs % 60:02d}", size=22, fam=MONO, col=DOT)
        if t > 4.0: white_pill(c, W / 2, 1660, "na sign up, na paise ki baat", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 70, Y0 + 380), 1.12), (d - 0.4, (PX + 60, Y0 + 420), 1.1)), seed=2)
    hud(cv)


TAP = 3.4
def s2(cv, t, d, st):                                     # one day: a little crown, "Pro" — "itna diya hai, chalo le lete"
    def world(c):
        canva_head(c)
        for i in range(6):
            template(c, X0 + 24 + (i % 2) * 220, Y0 + 140 + (i // 2) * 160, 208, 148, i, pro=(i == 3))
        if t > 0.6: ring(c, X0 + 244 + 208 - 24, Y0 + 300 + 24, t, 0.6, col=GOLD)
        if t > 0.9: c.pill(PX + 285, Y0 + 320, "Pro", size=28, fam=SANS, col=DARK, bg=GOLD, bold=True)
        if t > 1.6:
            k = ease(min(1, (t - 1.6) / 0.5))
            c.fill_rrect(W / 2 - 360, 560, 720, 120, 40, (0.95, 0.95, 0.96), k)
            for j, (dx, dy, rr) in enumerate([(-280, 140, 16), (-310, 170, 9)]):
                c.c.new_path(); c.c.set_source_rgba(0.95, 0.95, 0.96, k); c.c.arc(W / 2 + dx, 560 + dy, rr, 0, 6.2832); c.c.fill()
            c.font(SANS, 30, True); c.text(W / 2 - c.text_w("itna kuch toh diya hai…") / 2, 632, "itna kuch toh diya hai…", DARK, k)
        pressed = TAP < t < TAP + 0.25
        c.fill_rrect(X0 + 30, Y0 + PH - 140 + (4 if pressed else 0), PW - 60, 80, 40, CPUR)
        crown(c, X0 + 90, Y0 + PH - 100, 0.8, GOLD)
        c.font(SANS, 26, True); c.text(X0 + 120, Y0 + PH - 90, "Try Canva Pro", (1, 1, 1))
        if TAP - 0.8 < t < TAP + 0.2:
            k = ease(min(1, (t - TAP + 0.8) / 0.8))
            c._dot(PX + 150 - 100 * k, Y0 + PH + 60 - 160 * k, 13, (1, 1, 1), 1)
        if t > TAP + 0.4: white_pill(c, W / 2, 1680, "chalo, is baar le hi lete hain", 36)
    stage.compose(cv, t, d, world, K((0, (PX + 60, Y0 + 420), 1.1), (1.4, (PX + 60, Y0 + 420), 1.1), (2.0, (W / 2, 900), 0.95),
                                     (d - 0.4, (W / 2, 960), 0.95)), punch=0.05 * max(0, 1 - abs(t - TAP) / 0.12), seed=3)
    hud(cv); flash(cv, t, TAP, 0.08)


def s3(cv, t, d, st):                                     # study: a small sweet with the bill → more tips
    def world(c):
        c.pill(W / 2, 560, "ek study", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        bx, by = W / 2 - 220, 680
        c.fill_rrect(bx, by, 440, 520, 16, (0.95, 0.93, 0.88))
        c.font(SANS, 30, True); c.text(bx + 30, by + 60, "BILL", DARK)
        for i, (nm, pr) in enumerate([("Paneer Tikka", "₹320"), ("Dal Makhani", "₹260"), ("Butter Naan ×4", "₹160")]):
            c.font(SANS, 24, True); c.text(bx + 30, by + 130 + i * 60, nm, DARK); c.text(bx + 410 - c.text_w(pr), by + 130 + i * 60, pr, DARK)
        c.font(SANS, 28, True); c.text(bx + 30, by + 340, "Total", DARK); c.text(bx + 410 - c.text_w("₹740"), by + 340, "₹740", DARK)
        if t > 1.0:
            k = ease(min(1, (t - 1.0) / 0.5))
            tx, ty = bx + 330, by + 450
            c.c.new_path(); c.c.set_source_rgba(*RED, k); c.c.move_to(tx - 60, ty - 18); c.c.line_to(tx - 34, ty); c.c.line_to(tx - 60, ty + 18)
            c.c.close_path(); c.c.fill(); c.c.move_to(tx + 60, ty - 18); c.c.line_to(tx + 34, ty); c.c.line_to(tx + 60, ty + 18); c.c.close_path(); c.c.fill()
            c.fill_rrect(tx - 36, ty - 22, 72, 44, 20, RED, k)
            c.pill(tx - 200, ty, "+ 1 toffee", size=26, fam=SANS, col=DARK, bg=GOLD, bold=True, a=k)
        if t > 2.4:
            g = ease(min(1, (t - 2.4) / 1.0))
            c.font(MONO, 26, True); c.text(W / 2 + 260, 900, "tip", DIM)
            c.fill_rrect(W / 2 + 260, 1180 - 100, 60, 100, 10, GREY)
            c.fill_rrect(W / 2 + 340, 1180 - 100 - 120 * g, 60, 100 + 120 * g, 10, GREEN)
            c.font(SANS, 20, True); c.text(W / 2 + 252, 1210, "bina", DIM); c.text(W / 2 + 330, 1210, "toffee", GREEN)
        if t > 3.6: white_pill(c, W / 2, 1320, "zyaada tip di!", 40)
    stage.compose(cv, t, d, world, K((0, (W / 2 - 40, 940), 1.05), (2.2, (W / 2 - 40, 940), 1.05), (d - 0.4, (W / 2 + 40, 1000), 1.0)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law named: someone gives first → we want to give back
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "RECIPROCITY", 108, W / 2, 640, ease(1 - t / 0.8), col=CAN)
        c.glow(W / 2, 640, 420, 0.07)
        lx, rx, y = W / 2 - 250, W / 2 + 250, 1050
        for x, col, lab in [(lx, CPUR, "app"), (rx, GOLD, "user")]:
            c.c.new_path(); c.c.set_source_rgba(*col, 1); c.c.arc(x, y, 70, 0, 6.2832); c.c.fill()
            c.font(SANS, 30, True); c.text(x - c.text_w(lab) / 2, y + 10, lab, DARK)
        k1 = ease(min(1, max(0, (t - 1.4) / 0.8))); k2 = ease(min(1, max(0, (t - 2.6) / 0.8)))
        c.dellipse(W / 2, y, 250, 150, a0=200, a1=340, spacing=8, r=3, col=CAN, a=k1)
        if k1 > 0: c.pill(W / 2, y - 190, "pehle deta hai", size=26, fam=SANS, col=DARK, bg=CAN, bold=True, a=k1)
        c.dellipse(W / 2, y, 250, 150, a0=20, a1=160, spacing=8, r=3, col=GOLD, a=k2)
        if k2 > 0: c.pill(W / 2, y + 190, "mann lautaane ko karta", size=26, fam=SANS, col=DARK, bg=GOLD, bold=True, a=k2)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.2, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1030), 1.02)), seed=5)
    hud(cv); flash(cv, t, 0.2)


def s5(cv, t, d, st):                                     # give first, then ask — users remember the favour, forget the ad
    def world(c):
        c.font(SANS, 52, True); c.text(W / 2 - c.text_w("pehle do, phir maango") / 2, 580, "pehle do, phir maango", CAN)
        steps = [("1 · do", "value, free", CAN, 0.5), ("2 · maango", "Pro / sign up", CPUR, 1.4)]
        for j, (lab, sub, col, at) in enumerate(steps):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            x = W / 2 - 380 + j * 400
            c.fill_rrect(x, 680, 360, 200, 24, col, k)
            c.font(SANS, 40, True); c.text(x + 30, 770, lab, DARK, k)
            c.font(SANS, 26, True); c.text(x + 30, 830, sub, DARK, k)
        if t > 2.4:
            k = ease(min(1, (t - 2.4) / 0.5))
            c.c.new_path(); c.c.set_source_rgba(*GOLD, k)
            hx, hy = W / 2 - 200, 1120
            c.c.move_to(hx, hy + 60); c.c.curve_to(hx - 90, hy, hx - 70, hy - 80, hx, hy - 36); c.c.curve_to(hx + 70, hy - 80, hx + 90, hy, hx, hy + 60)
            c.c.fill(); c.c.new_path()
            c.font(SANS, 28, True); c.text(hx - c.text_w("ehsaan: yaad") / 2, hy + 120, "ehsaan: yaad", GOLD, k)
            fa = 1 - 0.8 * ease(min(1, max(0, (t - 3.0) / 1.0)))
            c.fill_rrect(W / 2 + 100, hy - 60, 220, 120, 14, (0.85, 0.30, 0.40), fa)
            c.font(SANS, 34, True); c.text(W / 2 + 175, hy + 12, "AD", (1, 1, 1), fa)
            c.font(SANS, 28, True); c.text(W / 2 + 210 - c.text_w("ad: bhool gaye") / 2, hy + 120, "ad: bhool gaye", DIM, k)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 980), 1.0)), seed=6)
    hud(cv)


STAMP = 2.8
def s6(cv, t, d, st):                                     # warning: half-products / paywall every step = feels like cheating
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("par dhyaan rahe") / 2, 560, "par dhyaan rahe", RED)
        for i in range(5):
            at = 0.3 + i * 0.35
            k = ease(min(1, max(0, (t - at) / 0.3)))
            y = 660 + i * 120
            c.fill_rrect(W / 2 - 360, y, 720, 100, 18, CARD, k)
            c.font(SANS, 26, True); c.text(W / 2 - 320, y + 60, ["Template", "Font", "Download", "Resize", "Export"][i], DOT, k)
            c.fill_rrect(W / 2 + 200, y + 26, 120, 48, 24, RED, k)
            c.font(SANS, 20, True); c.text(W / 2 + 222, y + 58, "PAY ₹", DARK, k)
        if t > 2.0: c.pill(W / 2, 1290, "har qadam par paywall", size=28, fam=MONO, col=DARK, bg=YELLOW, bold=True)
        if t > STAMP:
            ks = ease(min(1, (t - STAMP) / 0.3))
            c.c.save(); c.c.translate(W / 2, 960); c.c.rotate(-0.2)
            c.rrect_path(-220 * ks, -70 * ks, 440 * ks, 140 * ks, 16); c.c.set_source_rgba(*RED, ks); c.c.set_line_width(8); c.c.stroke()
            c.font(SANS, int(76 * max(0.2, ks)), True); c.text(-c.text_w("DHOKHA") / 2, 26 * ks, "DHOKHA", RED, ks)
            c.c.restore()
        if t > 3.8: white_pill(c, W / 2, 1410, "len-den nahi, dhokha lagega", 34)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.02), (d - 0.4, (W / 2, 1030), 1.0)),
                  punch=0.06 * max(0, 1 - abs(t - STAMP) / 0.12), seed=8)
    hud(cv); flash(cv, t, STAMP, 0.1)


# Narration: the approved Day 33 script (docs/scripts/day33.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("कैनवा ने सब कुछ फ़्री दिया, फिर भी लाखों लोग ख़ुशी-ख़ुशी पैसे क्यों दे रहे हैं? डे थर्टी थ्री में, आज ये पहेली सुलझाते हैं।", "", D.s0,
          min_dur=4.8, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("आपने कैनवा खोला। हज़ारों टेम्पलेट्स, फ़ॉन्ट्स, फ़ोटोज़, सब फ़्री। पाँच मिनट में, आपकी इंस्टा पोस्ट तैयार। न साइन अप का झंझट, न पैसे की बात।",
          "", s1, min_dur=6.4, whoosh=True, sfx=[(i * 0.25, "pop") for i in range(8)] + [(0.8, "pop_hi"), (1.3, "pop_hi"), (1.8, "pop_hi"),
                                                                                     (2.8, "tick"), (4.0, "ding")]),
    Scene("फिर एक दिन, एक टेम्पलेट पर छोटा सा क्राउन दिखा। प्रो। और आपने सोचा, इतना कुछ तो दिया है, चलो इस बार ले ही लेते हैं।", "", s2,
          min_dur=6.0, whoosh=True, sfx=[(0.6, "chime"), (0.9, "pop_hi"), (1.6, "pop"), (TAP, "pop_hi"), (TAP + 0.4, "ding")]),
    Scene("एक स्टडी में, रेस्टोरेंट में बिल के साथ, बस एक छोटी सी टॉफ़ी दी गई। और लोगों ने, पहले से ज़्यादा टिप दी।", "", s3, min_dur=5.6,
          whoosh=True, sfx=[(0.3, "pop"), (1.0, "pop_hi"), (2.4, "riser"), (3.6, "ding")]),
    Scene("इसे कहते हैं, रेसिप्रोसिटी। जब कोई हमें पहले कुछ देता है, तो हमारा मन, बदले में कुछ लौटाने को करता है।", "", s4, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "drop"), (1.4, "riser"), (2.2, "pop_hi"), (2.6, "riser"), (3.4, "chime")]),
    Scene("पहले दो, फिर माँगो। यूज़र को एहसान याद रहता है, और ऐड भूल जाता है।", "", s5, min_dur=4.8, whoosh=True,
          sfx=[(0.5, "pop_hi"), (1.4, "pop_hi"), (2.4, "chime"), (3.0, "pop_lo")]),
    Scene("पर ध्यान रहे। अगर फ़्री के नाम पर अधूरी चीज़ दी, या हर क़दम पर पेवॉल लगा दिया, तो लेन-देन नहीं, धोखा लगेगा।", "", s6, min_dur=6.0,
          whoosh=True, sfx=[(0.3 + i * 0.35, "pop_lo") for i in range(5)] + [(2.0, "buzz"), (STAMP, "drop"), (3.8, "pop")]),
    Scene("किस ऐप ने आपको इतना फ़्री दिया, कि आपने ख़ुद पैसे दे दिए? कमेंट में बताओ। कल मिलते हैं, कमिटमेंट और कंसिस्टेंसी के साथ।", "", D.s8,
          min_dur=5.0, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = "auto"

if __name__ == "__main__":
    import daily
    daily.run(33, "Reciprocity", SCENES, "day33_reciprocity", cuts=VO_CUTS)

"""Day 22/45 · Parkinson's Law, explained with Amazon's saved address + one-tap checkout.

Work expands to fill the time it's given. A week for an assignment still means the last night; a ten-field checkout
gives users time to hesitate and abandon the cart. Amazon pre-selects the saved address and remembers the payment, so
the order is one tap. Day 02 pattern; the script opens on the last-night habit and names the law right after.
Voice: Rakhi's Day 22 ElevenLabs Tisha K file at assets/voice/day22/full.mp3 (content-verified); script in
docs/scripts/day22.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 22, "Cognitive Load"
W, H = 1080, 1920
AMZ = (1.0, 0.60, 0.0)                            # Amazon orange
AMY = (1.0, 0.85, 0.10)                           # Place-order yellow
TEAL = (0.20, 0.78, 0.85)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
FIELDS = ["Full name", "Mobile", "Pincode", "Flat / House", "Street", "Landmark", "City", "State", "Card number",
          "Expiry / CVV"]


def moon(c, x, y, r, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*AMY, a); c.c.arc(x, y, r, 0, 6.2832); c.c.fill()
    c.c.new_path(); c.c.set_source_rgba(0, 0, 0, a); c.c.arc(x + r * 0.45, y - r * 0.25, r * 0.85, 0, 6.2832); c.c.fill()


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # habit: a week for the assignment, done on the last night
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    def world(c):
        c.pill(W / 2, 560, "assignment: 1 hafta", size=32, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        for i, dname in enumerate(DAYS):
            x = W / 2 - 390 + i * 130; y = 760
            last = i == 6
            c.fill_rrect(x - 55, y - 70, 110, 150, 16, (0.30, 0.20, 0.08) if last and t > 3.4 else CARD)
            c.font(SANS, 24, True); c.text(x - c.text_w(dname) / 2, y - 30, dname, DOT)
            at = 0.6 + i * 0.4
            if t > at and not last:
                c.font(SANS, 40, True); c.text(x - 14, y + 40, "✗", RED)
                if i in (1, 4): c.pill(x, y + 120, "kal karenge", size=18, fam=MONO, col=DIM)
        if t > 3.4:
            moon(c, W / 2 + 390, 700, 26)
            for k in range(int(min(12, (t - 3.4) * 12))):
                c.dbar(W / 2 - 300, 1000 + k * 26, 600 - (k * 37) % 180, rows=1, gap=4, col=DOT)
            c.pill(W / 2 + 390, 900, "aakhri raat!", size=26, fam=SANS, col=DARK, bg=AMY, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 800), 1.1), (3.0, (W / 2, 800), 1.1), (3.8, (W / 2 + 200, 860), 1.25),
                                     (d - 0.4, (W / 2 + 200, 900), 1.2)), punch=0.04 * max(0, 1 - abs(t - 3.4) / 0.12), seed=2)
    hud(cv); flash(cv, t, 3.4, 0.08)


def s2(cv, t, d, st):                                     # law named: work expands to fill the time you give it
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "PARKINSON'S LAW", 92, W / 2, 620, ease(1 - t / 0.8), col=AMZ)
        c.glow(W / 2, 620, 420, 0.06)
        l1 = "kaam utna hi phailta hai,"; l2 = "jitna time do"
        n = int(max(0, t - 1.0) * 26)
        mono(c, l1, 740, DOT, 34, chars=n); mono(c, l2, 790, AMY, 34, chars=n - len(l1))
        k = ease(min(1, max(0, (t - 2.6) / 1.6)))
        for row, (lab, wmax, y) in enumerate([("1 din", 220, 960), ("1 hafta", 760, 1160)]):
            w = wmax if row == 0 else 220 + (wmax - 220) * k
            c.rrect_path(W / 2 - 380, y, wmax, 120, 18); c.c.set_source_rgba(*GREY, 1); c.c.set_line_width(2); c.c.stroke()
            c.fill_rrect(W / 2 - 372, y + 8, w - 16, 104, 14, AMZ, 0.85)
            c.font(SANS, 26, True); c.text(W / 2 - 360, y + 70, "kaam", DARK)
            c.font(MONO, 26, True); c.text(W / 2 - 380, y - 16, lab, DIM)
        if k >= 1: c.pill(W / 2, 1360, "same kaam, zyaada time = zyaada phailaav", size=26, fam=MONO, col=DARK, bg=AMY, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (2.2, (W / 2, 1000), 1.0), (d - 0.4, (W / 2, 1040), 1.02)), seed=3)
    hud(cv)


QUIT = 4.6
def s3(cv, t, d, st):                                     # long checkout: 10 fields → hesitation → cart abandoned
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 90, "Checkout", DOT)
        c.pill(X0 + PW - 90, Y0 + 80, "10 fields", size=20, fam=MONO, col=DARK, bg=RED, bold=True)
        for i, f in enumerate(FIELDS):
            y = Y0 + 130 + i * 66
            c.font(SANS, 15, True); c.text(X0 + 30, y, f, DIM)
            c.rrect_path(X0 + 30, y + 8, PW - 60, 40, 8); c.c.set_source_rgba(*GREY, 1); c.c.set_line_width(1.3); c.c.stroke()
            filled = t > 0.6 + i * 0.32 and i < 4
            if filled: c.dbar(X0 + 44, y + 22, 140 + (i * 37) % 120, rows=1, gap=4, col=DOT)
        if t > 2.0:
            for j, (dx, dy) in enumerate([(-120, 350), (130, 420), (0, 300)]):
                if t > 2.0 + j * 0.4: c.font(SANS, 56, True); c.text(PX + dx, Y0 + dy, "?", AMY)
            c.pill(PX + 320, Y0 + 300, "rukta hai…", size=24, fam=MONO, col=DOT)
        if t > 3.2: c.pill(PX + 320, Y0 + 380, "sochta hai…", size=24, fam=MONO, col=DOT)
        if t > QUIT:
            k = ease(min(1, (t - QUIT) / 0.6))
            c.c.new_path(); c.c.set_source_rgba(0, 0, 0, 0.65 * k); c.c.rectangle(X0, Y0, PW, PH); c.c.fill()
            c.fill_rrect(PX - 170, PY - 60, 340, 120, 20, RED, k)
            c.font(SANS, 30, True); c.text(PX - c.text_w("cart chhod diya") / 2, PY + 10, "cart chhod diya", DARK, k)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 80, Y0 + 420), 1.15), (QUIT, (PX + 80, Y0 + 420), 1.15),
                                     (d - 0.4, (PX, PY), 1.1)), punch=0.05 * max(0, 1 - abs(t - QUIT) / 0.12), seed=4)
    hud(cv); flash(cv, t, QUIT, 0.1)


TAP = 3.0
def s4(cv, t, d, st):                                     # Amazon: saved address pre-selected, payment remembered, one tap
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 60, 10, (0.08, 0.11, 0.16)); c.font(SANS, 24, True)
        c.text(X0 + 30, Y0 + 90, "amazon.in · Checkout", DOT)
        k1 = ease(min(1, max(0, (t - 0.5) / 0.4))); k2 = ease(min(1, max(0, (t - 1.4) / 0.4)))
        c.fill_rrect(X0 + 20, Y0 + 140, PW - 40, 150, 16, CARD, k1)
        c.font(SANS, 18, True); c.text(X0 + 40, Y0 + 176, "Deliver to", DIM, k1)
        c.font(SANS, 24, True); c.text(X0 + 40, Y0 + 210, "Rahul · Home", DOT, k1)
        c.font(SANS, 18, True); c.text(X0 + 40, Y0 + 240, "12, MG Road, Bengaluru 560001", DIM, k1)
        if k1 >= 1: c.pill(X0 + PW - 110, Y0 + 176, "saved ✓", size=18, fam=SANS, col=DARK, bg=GREEN, bold=True)
        c.fill_rrect(X0 + 20, Y0 + 310, PW - 40, 120, 16, CARD, k2)
        c.font(SANS, 18, True); c.text(X0 + 40, Y0 + 346, "Pay with", DIM, k2)
        c.font(SANS, 24, True); c.text(X0 + 40, Y0 + 382, "HDFC card ···· 4321", DOT, k2)
        if k2 >= 1: c.pill(X0 + PW - 120, Y0 + 346, "yaad hai ✓", size=18, fam=SANS, col=DARK, bg=GREEN, bold=True)
        c.font(SANS, 22, True); c.text(X0 + 40, Y0 + 480, "Order total: ₹1,499", DOT)
        pressed = TAP < t < TAP + 0.25
        c.fill_rrect(X0 + 30, Y0 + 520 + (4 if pressed else 0), PW - 60, 80, 40, AMY)
        c.font(SANS, 26, True); c.text(PX - c.text_w("Place your order") / 2, Y0 + 570, "Place your order", DARK)
        if TAP - 0.6 < t < TAP + 0.4:
            kk = ease(min(1, (t - TAP + 0.6) / 0.6))
            c._dot(PX + 180 - 180 * kk, Y0 + 760 - 200 * kk, 12, (1, 1, 1), 1)
        if t > TAP + 0.3:
            k = ease(min(1, (t - TAP - 0.3) / 0.5))
            c.c.new_path(); c.c.set_source_rgba(*GREEN, k); c.c.arc(PX, Y0 + 720, 60 * k, 0, 6.2832); c.c.fill()
            c.dots_path([(PX - 26, Y0 + 720), (PX - 6, Y0 + 742), (PX + 30, Y0 + 700)], spacing=5, r=3.4, col=(1, 1, 1), a=k)
            c.font(SANS, 26, True); c.text(PX - c.text_w("Order placed") / 2, Y0 + 820, "Order placed", GREEN, k)
        if t > TAP + 0.9: white_pill(c, W / 2, 1640, "bas ek tap", 42)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.4, (PX, Y0 + 380), 1.2), (d - 0.4, (PX, Y0 + 460), 1.12)),
                  punch=0.05 * max(0, 1 - abs(t - TAP) / 0.12), seed=5)
    hud(cv); flash(cv, t, TAP + 0.3, 0.1)


def s5(cv, t, d, st):                                     # short task = no time to stall or change your mind
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("chhota kaam = taalne ka time nahi") / 2, 560,
                                       "chhota kaam = taalne ka time nahi", AMY)
        lx, rx = W * 0.27, W * 0.73
        secs = min(180, int(t * 60))
        c.fill_rrect(lx - 200, 660, 400, 560, 22, CARD); c.fill_rrect(rx - 200, 660, 400, 560, 22, CARD)
        c.font(MONO, 64, True); c.text(lx - 110, 790, f"{secs // 60}:{secs % 60:02d}", RED)
        c.font(MONO, 64, True); c.text(rx - 110, 790, "0:05", GREEN)
        c.font(SANS, 24, True); c.text(lx - 170, 700, "10 fields", DIM); c.text(rx - 170, 700, "1 tap", DIM)
        for j, th in enumerate(["baad mein…", "price check…", "mann badal gaya"]):
            if t > 0.8 + j * 0.9: c.pill(lx, 900 + j * 90, th, size=22, fam=MONO, col=DOT)
        if t > 0.6:
            c.c.new_path(); c.c.set_source_rgba(*GREEN, 1); c.c.arc(rx, 1000, 70, 0, 6.2832); c.c.fill()
            c.dots_path([(rx - 30, 1000), (rx - 8, 1024), (rx + 34, 978)], spacing=5, r=3.6, col=(1, 1, 1))
            c.font(SANS, 26, True); c.text(rx - c.text_w("ho gaya") / 2, 1120, "ho gaya", GREEN)
        if t > 3.6: c.pill(lx, 1180, "cart chhoda ✗", size=24, fam=SANS, col=RED)
    stage.compose(cv, t, d, world, K((0, (W / 2, 920), 1.0), (d - 0.4, (W / 2, 940), 1.04)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # check: has the user already told us this? → fill it yourself
    ROWS = [("Naam", True), ("Mobile", True), ("Address", True), ("Gift note", False), ("Payment", True)]
    def world(c):
        c.font(SANS, 44, True); c.text(W / 2 - c.text_w("pehle hi bata chuka hai?") / 2, 560, "pehle hi bata chuka hai?", AMY)
        for i, (lab, known) in enumerate(ROWS):
            at = 0.6 + i * 0.55
            y = 660 + i * 130
            c.fill_rrect(W / 2 - 380, y, 760, 100, 16, CARD)
            c.font(SANS, 30, True); c.text(W / 2 - 350, y + 62, lab, DOT)
            if t > at:
                if known:
                    c.pill(W / 2 + 200, y + 50, "haan → khud bhar do ✓", size=22, fam=SANS, col=DARK, bg=GREEN, bold=True)
                else:
                    c.pill(W / 2 + 200, y + 50, "nahi → tabhi poochho", size=22, fam=SANS, col=DOT)
        if t > 3.8: white_pill(c, W / 2, 1400, "dobaara mat poochho", 38)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (d - 0.4, (W / 2, 990), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 22 script (docs/scripts/day22.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("आज है डे ट्वेंटी टू, और आज का लॉ, सीधा आपकी आदत से जुड़ा है।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("याद है? असाइनमेंट के लिए पूरा एक हफ़्ता मिलता था, फिर भी काम, आख़िरी रात को ही होता था।", "", s1, min_dur=5.4,
          whoosh=True, sfx=[(0.6 + i * 0.4, "pop_lo") for i in range(6)] + [(3.4, "drop")] + [(3.5 + i * 0.09, "tick") for i in range(12)]),
    Scene("इसे कहते हैं, पार्किंसन्स लॉ। काम उतना ही फैल जाता है, जितना टाइम आप उसे देते हो।", "", s2, min_dur=5.4, whoosh=True,
          sfx=[(0.2, "drop"), (2.6, "riser"), (4.2, "ding")]),
    Scene("ऐप्स में भी यही होता है। चेकआउट पे अगर दस फ़ील्ड भरने हों, नाम, फ़ोन, पिनकोड, शहर, गली, तो यूज़र रुकता है, सोचता है, और कई बार, कार्ट छोड़ के चला जाता है।",
          "", s3, min_dur=6.6, whoosh=True, sfx=[(0.6 + i * 0.32, "tick") for i in range(4)] + [(2.0, "pop_lo"), (2.4, "pop_lo"),
                                                                                        (2.8, "pop_lo"), (QUIT, "buzz")]),
    Scene("इसीलिए ऐमज़ॉन पे, सेव्ड एड्रेस पहले से चुना हुआ आता है, पेमेंट भी याद रहता है। बस एक टैप, और ऑर्डर प्लेस।", "", s4,
          min_dur=5.6, whoosh=True, sfx=[(0.5, "pop_hi"), (1.4, "pop_hi"), (TAP, "pop"), (TAP + 0.3, "chime"), (TAP + 0.9, "ding")]),
    Scene("जब काम छोटा होता है, तो यूज़र के पास टालने का, या मन बदलने का, टाइम ही नहीं बचता।", "", s5, min_dur=5.0,
          whoosh=True, sfx=[(0.6, "chime"), (0.8, "pop_lo"), (1.7, "pop_lo"), (2.6, "pop_lo"), (3.6, "buzz")]),
    Scene("तो अपने फ़्लो के हर स्टेप से पूछो, क्या ये बात यूज़र पहले ही बता चुका है? अगर हाँ, तो दोबारा मत पूछो, ख़ुद भर दो।", "", s6,
          min_dur=6.0, whoosh=True, sfx=[(0.6 + i * 0.55, "pop_hi" if i != 3 else "pop_lo") for i in range(5)] + [(3.8, "ding")]),
    Scene("आपने आख़िरी बार कौन सा काम, आख़िरी रात को किया था? कमेंट में बताओ। कल मिलते हैं, कॉग्निटिव लोड के साथ।", "", D.s8,
          min_dur=5.0, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = "auto"

if __name__ == "__main__":
    import daily
    daily.run(22, "Parkinson's Law", SCENES, "day22_parkinsons_law", cuts=VO_CUTS)

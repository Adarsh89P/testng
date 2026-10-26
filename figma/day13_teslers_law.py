"""Day 13/45 · Tesler's Law, explained with UPI scan-and-pay.

Every task has some complexity that can't be removed; the question is who carries it. UPI moves the bank details
(account number, IFSC, name) behind a QR code, so the system carries the complexity and paying feels simple.
Day 02 pattern. Voice: Rakhi's Day 13 ElevenLabs Tisha K file at assets/voice/day13/full.mp3 (content-verified);
script in docs/scripts/day13.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 13, "Postel's Law"
W, H = 1080, 1920
UPI = (0.30, 0.80, 0.55)                          # UPI green
UORANGE = (1.0, 0.55, 0.20)
VIOLET = (0.62, 0.45, 1.0)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
FIELDS = [("Account number", "50100234567891"), ("Confirm account", "50100234567819"), ("IFSC code", "HDFC0001234"),
          ("Name", "Rahul Sharma")]


def qr(c, cx, cy, s, a=1.0, col=DOT):
    """Dotted QR code (deterministic pattern + three finder squares)."""
    n = 13; cell = s / n; x0, y0 = cx - s / 2, cy - s / 2
    for i in range(n):
        for j in range(n):
            finder = (i < 3 and j < 3) or (i < 3 and j > n - 4) or (i > n - 4 and j < 3)
            on = finder or ((i * 7 + j * 11 + i * j) % 5 < 2)
            if on: c.c.set_source_rgba(*col, a); c.c.rectangle(x0 + j * cell + 1, y0 + i * cell + 1, cell - 2, cell - 2); c.c.fill()


def seesaw(c, cx, cy, tilt, a=1.0):
    """Seesaw with 'user' on the left, 'system' on the right; tilt>0 = heavy block on the user side."""
    L = 360; ang = tilt * 0.28
    x1, y1 = cx - L * math.cos(ang), cy + L * math.sin(ang)
    x2, y2 = cx + L * math.cos(ang), cy - L * math.sin(ang)
    c.dots_path([(x1, y1), (x2, y2)], spacing=8, r=3, col=DOT, a=a)
    c.dots_path([(cx - 40, cy + 70), (cx, cy), (cx + 40, cy + 70), (cx - 40, cy + 70)], spacing=7, r=2, col=DIM, a=a)
    bx, by = (x1 + 90 * math.cos(ang), y1 - 90 * math.sin(ang)) if tilt > 0 else (x2 - 90 * math.cos(ang), y2 + 90 * math.sin(ang))
    c.fill_rrect(bx - 70, by - 110, 140, 100, 12, UORANGE, a)
    c.font(SANS, 20, True); c.text(bx - 52, by - 52, "mushkil", DARK, a)
    c.person(x1 + 10, y1 - 60, 0.55) if tilt <= 0 else None
    c.pill(x1, y1 + 60, "user", size=24, fam=MONO, col=DOT, a=a)
    c.fill_rrect(x2 - 34, y2 - 80 if tilt > 0 else y2 - 70, 68, 60, 10, (0.15, 0.18, 0.25), a)
    c.pill(x2, y2 + 60, "system", size=24, fam=MONO, col=UPI, a=a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: mushkil kaun uthaye?
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "TESLER'S LAW", 110, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=UPI)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "kya hai?", 980, DOT, 56, chars=int((t - 2.0) * 14))
        if t > 3.0:
            tilt = 1 - 2 * ease(min(1, max(0, (t - 4.0) / 1.0)))
            seesaw(c, W / 2, 1250, tilt)
            c.pill(W / 2, 1450, "mushkil kaun uthaye?", size=30, fam=MONO, col=UORANGE)
        if t > 5.6: c.pill(W / 2, 1550, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=UPI, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1180), 1.0), (5.4, (W / 2, 1220), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


ERR = 3.6
def s2(cv, t, d, st):                                     # old bank transfer: user types everything, one typo
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 90, "Bank transfer", DOT)
        for i, (lab, val) in enumerate(FIELDS):
            y = Y0 + 150 + i * 130
            c.font(SANS, 20, True); c.text(X0 + 30, y, lab, DIM)
            bad = i == 1 and t > ERR
            c.rrect_path(X0 + 30, y + 14, PW - 60, 64, 12); c.c.set_source_rgba(*(RED if bad else GREY), 1); c.c.set_line_width(2.5 if bad else 1.4); c.c.stroke()
            n = int(max(0, (t - 0.4 - i * 0.7) * 22))
            c.font(MONO, 24, True); c.text(X0 + 46, y + 56, val[:n], RED if bad else DOT)
            if bad: c.font(SANS, 18, True); c.text(X0 + 30, y + 104, "account number match nahi hua", RED)
            st[f"f{i}"] = (PX, y + 46)
        c.fill_rrect(X0 + 30, Y0 + PH - 140, PW - 60, 80, 40, (0.25, 0.25, 0.28)); c.font(SANS, 26, True); c.text(PX - 30, Y0 + PH - 90, "Send", DIM)
        if t > 0.8: c.pill(PX + 340, Y0 + 300, "sab khud bharo", size=26, fam=MONO, col=DARK, bg=UORANGE, bold=True)
        if t > ERR + 0.6: white_pill(c, W / 2, 1640, "ek galti, paisa atak gaya", 36)
    f1 = st.get("f1", (PX, Y0 + 326))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (ERR - 0.4, ANCHOR, 1.0), (ERR, f1, 1.6), (d - 0.4, f1, 1.6)),
                  punch=0.05 * max(0, 1 - abs(t - ERR) / 0.1), seed=3)
    hud(cv); flash(cv, t, ERR, 0.12)


SCAN, AMT, PIN = 1.0, 2.2, 3.2
def s3(cv, t, d, st):                                     # UPI: scan QR -> amount -> PIN -> done
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 28, True); c.text(X0 + 30, Y0 + 90, "UPI · Scan & Pay", UPI)
        if t < AMT:                                          # camera view with QR and scan line
            c.drrect(PX - 170, Y0 + 180, 340, 340, 20, spacing=6, r=2, col=UPI)
            qr(c, PX, Y0 + 350, 240)
            sy = Y0 + 200 + ((t * 300) % 300)
            c.c.set_source_rgba(*UPI, 0.8); c.c.rectangle(PX - 160, sy, 320, 4); c.c.fill()
            if t > SCAN: c.pill(PX, Y0 + 580, "Rahul Sharma ✓", size=26, fam=SANS, col=DARK, bg=UPI, bold=True)
        else:
            c.font(SANS, 24, True); c.text(PX - c.text_w("Paying Rahul Sharma") / 2, Y0 + 200, "Paying Rahul Sharma", DOT)
            amt = "₹500"[:1 + int(min(3, (t - AMT) * 8))]
            c.font(SANS, 80, True); c.text(PX - c.text_w(amt) / 2, Y0 + 330, amt, DOT)
            if t > PIN:
                n = min(6, int((t - PIN) * 10))
                for i in range(6):
                    x = PX - 125 + i * 50
                    if i < n: c._dot(x, Y0 + 430, 11, DOT, 1)
                    else: c.dellipse(x, Y0 + 430, 11, 11, spacing=4, r=1.2, col=DIM)
            if t > PIN + 0.9:
                k = ease(min(1, (t - PIN - 0.9) / 0.5))
                c.c.set_source_rgba(*UPI, k); c.c.arc(PX, Y0 + 600, 70 * k, 0, 6.3); c.c.fill()
                c.dots_path([(PX - 30, Y0 + 600), (PX - 8, Y0 + 624), (PX + 34, Y0 + 578)], spacing=5, r=3.5, col=(1, 1, 1), a=k)
        for i, (lab, tt) in enumerate([("1 · scan", SCAN), ("2 · amount", AMT), ("3 · PIN", PIN)]):
            if t > tt: c.pill(PX + 340, Y0 + 260 + i * 90, lab, size=26, fam=MONO, col=DARK, bg=UPI, bold=True)
        if t > PIN + 1.5: white_pill(c, W / 2, 1640, "kaam ho gaya", 38)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.5, (PX, Y0 + 380), 1.3), (d - 0.4, (PX, Y0 + 420), 1.25)),
                  punch=0.05 * max(0, 1 - abs(t - PIN - 0.9) / 0.12), seed=4)
    hud(cv); flash(cv, t, PIN + 0.9, 0.12)


def s4(cv, t, d, st):                                     # law card: complexity moves from user to system
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "TESLER'S LAW", 104, W / 2, 630, ease(1 - t / 0.8), col=UPI)
        l1 = "mushkil khatam nahi hoti,"; l2 = "system use apne upar le sakta hai"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 34, chars=n); mono(c, l2, 800, UPI, 34, chars=n - len(l1))
        tilt = 1 - 2 * ease(min(1, max(0, (t - 2.6) / 1.2)))
        seesaw(c, W / 2, 1130, tilt)
        if t > 4.0: c.pill(W / 2 - 300, 1320, "user: aasaan", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > 4.4: c.pill(W / 2 + 300, 1320, "system: bhaari kaam", size=26, fam=MONO, col=UPI)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1040), 1.0), (d - 0.4, (W / 2, 1060), 1.03)), seed=5)
    hud(cv)


OPEN = 0.8
def s5(cv, t, d, st):                                     # behind the QR: bank details the system handles
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("UPI") / 2, 540, "UPI", UPI)
        k = ease(min(1, max(0, (t - OPEN) / 1.0)))
        qr(c, W / 2, 900 - 80 * k, 300, a=1 - 0.6 * k)
        details = [("Account", "50100234567891"), ("IFSC", "HDFC0001234"), ("Name", "Rahul Sharma"), ("Bank", "HDFC Bank")]
        for i, (lab, val) in enumerate(details):
            kk = ease(min(1, max(0, (t - OPEN - 0.4 - i * 0.3) / 0.5)))
            if kk <= 0: continue
            y = 1020 + i * 90
            c.fill_rrect(W / 2 - 280, y, 560, 70, 14, (0.12, 0.14, 0.13), kk)
            c.font(SANS, 22, True); c.text(W / 2 - 250, y + 44, lab, DIM, kk)
            c.font(MONO, 24, True); c.text(W / 2 + 250 - c.text_w(val), y + 44, val, UPI, kk)
        if t > OPEN + 2.2: c.pill(W / 2, 1420, "QR ke peeche · system sambhalta hai", size=28, fam=MONO, col=DARK, bg=UPI, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.2), (OPEN + 0.6, (W / 2, 900), 1.2), (OPEN + 1.6, (W / 2, 1100), 1.0),
                                     (d - 0.4, (W / 2, 1100), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T load the user | DO let the system handle it
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        for i in range(7):
            c.rrect_path(lx - 160, 680 + i * 62, 320, 48, 10); c.c.set_source_rgba(*(RED if t < 2.8 else GREY), 1); c.c.set_line_width(1.4); c.c.stroke()
            c.dbar(lx - 140, 698 + i * 62, 140, rows=1, gap=4, col=DIM)
        c.pill(lx, 1160, "sab user pe", size=26, fam=MONO, col=RED)
        qr(c, rx, 800, 180)
        c.fill_rrect(rx - 150, 940, 300, 60, 30, UPI); c.font(SANS, 24, True); c.text(rx - 80, 978, "auto-filled ✓", DARK)
        c.pill(rx, 1160, "system sambhale ✓", size=26, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "mushkil user pe mat daalo", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 13 script (docs/scripts/day13.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे थर्टीन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, टेस्लर्स लॉ क्या है? हर काम में कुछ मुश्किल तो रहती ही है, सवाल ये है कि वो कौन उठाए। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.6, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (3.0, "pop_lo"), (4.0, "riser"), (5.0, "pop_hi"), (5.6, "pop_hi")]),
    Scene("पहले पैसे भेजने के लिए, अकाउंट नंबर, आई एफ़ एस सी कोड, नाम, सब ख़ुद भरना पड़ता था। एक गलती, और पैसा अटक गया।", "", s2,
          min_dur=6.0, whoosh=True, sfx=[(0.4 + i * 0.12, "tick") for i in range(20)] + [(ERR, "buzz")]),
    Scene("अब यूपीआई में, बस क्यू आर कोड स्कैन करो, अमाउंट डालो, और पिन। काम हो गया।", "", s3,
          min_dur=5.4, whoosh=True, sfx=[(SCAN, "pop_hi"), (AMT, "pop")] + [(PIN + i * 0.1, "tick") for i in range(6)]
          + [(PIN + 0.9, "chime")]),
    Scene("यही है टेस्लर्स लॉ। मुश्किल ख़त्म नहीं होती, पर सिस्टम उसे अपने ऊपर ले सकता है, ताकि यूज़र को आसान लगे।", "", s4,
          min_dur=6.6, whoosh=True, sfx=[(0.2, "ding"), (2.6, "riser"), (3.8, "pop_hi"), (4.4, "pop")]),
    Scene("इसीलिए यूपीआई ने बैंक की सारी डिटेल्स क्यू आर कोड के पीछे छुपा दीं, सारा भारी काम सिस्टम करता है।", "", s5,
          min_dur=6.0, whoosh=True, sfx=[(OPEN, "riser")] + [(OPEN + 0.4 + i * 0.3, "pop") for i in range(4)] + [(OPEN + 2.2, "ding")]),
    Scene("डिज़ाइनर टिप, मुश्किल को यूज़र पे मत डालो, जितना हो सके, सिस्टम से ख़ुद संभालो।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 13 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each snapped to the quietest point within 0.8 s (all silent); line check 8/8.
VO_CUTS = [5.08, 15.84, 24.8, 31.08, 38.8, 46.16, 52.24]

if __name__ == "__main__":
    import daily
    daily.run(13, "Tesler's Law", SCENES, "day13_teslers_law", cuts=VO_CUTS)

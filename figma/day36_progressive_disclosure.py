"""Day 36/45 · Progressive Disclosure, explained with Google Maps step details on demand.

Show only what matters first, reveal the rest when the user asks. Maps shows 15 min · 6 km · Start; every turn only
when you tap Steps; while driving just the next turn ("200 m, turn right"). Twenty turns at once would confuse you at
the first one. Settings' "Advanced" and forms' "More options" are the same law; but don't hide so much users can't
find it — basics in front, the rest one labelled tap away. Day 02 pattern; counter-intuitive hook and a blue-ticks
teaser. Voice: Rakhi's Day 36 ElevenLabs Tisha K file at assets/voice/day36/full.mp3 (content-verified); script in
docs/scripts/day36.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 36, "Visibility of System Status"
W, H = 1080, 1920
GM = (0.26, 0.52, 0.96)                           # Google Maps blue
GMG = (0.12, 0.55, 0.30)                          # navigation green
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
STEPS = ["Head north on MG Road", "Turn right at Metro", "Keep left at flyover", "Turn left · 2nd Cross",
         "U-turn at signal", "Turn right · Lake Rd", "Slight left", "Turn right at park"]
ROUTE = [(X0 + 80, Y0 + 520), (X0 + 140, Y0 + 420), (X0 + 260, Y0 + 400), (X0 + 300, Y0 + 300), (X0 + 400, Y0 + 230)]


def map_bg(c, a=1.0, route_k=1.0):
    c.fill_rrect(X0 + 10, Y0 + 40, PW - 20, PH - 60, 30, (0.10, 0.12, 0.14), a)
    for i in range(7):
        c.c.set_source_rgba(0.20, 0.22, 0.25, a); c.c.rectangle(X0 + 10, Y0 + 90 + i * 90, PW - 20, 4); c.c.fill()
        c.c.rectangle(X0 + 40 + i * 70, Y0 + 40, 4, PH - 60); c.c.fill()
    c.dots_path(ROUTE, spacing=10, r=4.2, col=GM, a=a, reveal=route_k)
    c.c.new_path(); c.c.set_source_rgba(*GM, a); c.c.arc(*ROUTE[0], 12, 0, 6.2832); c.c.fill()
    c.c.new_path(); c.c.set_source_rgba(*RED, a); c.c.arc(*ROUTE[-1], 14, 0, 6.2832); c.c.fill(); c.c.new_path()


def sheet(c, y, a=1.0, steps_btn=True):
    c.fill_rrect(X0 + 10, y, PW - 20, Y0 + PH - 20 - y, 26, (0.16, 0.16, 0.18), a)
    c.font(SANS, 40, True); c.text(X0 + 40, y + 70, "15 min", GMG, a)
    c.font(SANS, 26, True); c.text(X0 + 200, y + 68, "(6 km)", DOT, a)
    c.fill_rrect(X0 + 40, y + 100, 190, 70, 35, GM, a)
    c.font(SANS, 28, True); c.text(X0 + 135 - c.text_w("Start") / 2, y + 146, "Start", (1, 1, 1), a)
    if steps_btn:
        c.rrect_path(X0 + 250, y + 100, 170, 70, 35); c.c.set_source_rgba(*GM, a); c.c.set_line_width(2.5); c.c.stroke()
        c.font(SANS, 26, True); c.text(X0 + 335 - c.text_w("Steps") / 2, y + 146, "Steps", GM, a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # destination entered: just 15 min · 6 km · Start
    def world(c):
        phone(c, PX, PY, PW, PH)
        map_bg(c, route_k=min(1, t / 1.2))
        k = ease(min(1, max(0, (t - 0.8) / 0.5)))
        sheet(c, Y0 + PH - 220 + (1 - k) * 220, k)
        for j, (lab, at) in enumerate([("15 min", 1.6), ("6 km", 2.2), ("Start", 2.8)]):
            if t > at: c.pill(PX + 290, Y0 + 520 + j * 80, f"{j + 1} · {lab}", size=24, fam=SANS, col=DARK, bg=GM, bold=True)
        if t > 3.8: white_pill(c, W / 2, 1660, "screen par bas teen cheezein", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.4, ANCHOR, 1.0), (2.0, (PX + 80, Y0 + 620), 1.15), (d - 0.4, (PX + 60, Y0 + 640), 1.12)), seed=2)
    hud(cv)


TAP, DRIVE = 0.8, 3.0
def s2(cv, t, d, st):                                     # tap Steps → every turn; drive starts → just the next turn
    def world(c):
        phone(c, PX, PY, PW, PH)
        if t < DRIVE:
            map_bg(c)
            k = ease(min(1, max(0, (t - TAP) / 0.6)))
            top = Y0 + PH - 220 - 420 * k
            sheet(c, top, 1.0)
            for i, s in enumerate(STEPS[:6]):
                kk = ease(min(1, max(0, (t - TAP - 0.3 - i * 0.12) / 0.3)))
                c.font(SANS, 20, True); c.text(X0 + 80, top + 220 + i * 56, s, DOT, kk)
                c.dots_path([(X0 + 50, top + 212 + i * 56), (X0 + 62, top + 202 + i * 56)], spacing=4, r=2, col=GM, a=kk)
            if TAP - 0.5 < t < TAP + 0.1:
                kk = ease(min(1, (t - TAP + 0.5) / 0.5)); c._dot(PX + 200 - 100 * kk, Y0 + PH + 60 - 340 * kk, 13, (1, 1, 1), 1)
            if t > TAP + 0.6: c.pill(PX + 290, Y0 + 400, "Steps = sirf tap par", size=22, fam=SANS, col=DARK, bg=GM, bold=True)
        else:
            map_bg(c)
            k = ease(min(1, (t - DRIVE) / 0.4))
            c.fill_rrect(X0 + 20, Y0 + 50, PW - 40, 130, 20, GMG, k)
            c.dots_path([(X0 + 60, Y0 + 140), (X0 + 60, Y0 + 90), (X0 + 100, Y0 + 90)], spacing=6, r=4, col=(1, 1, 1), a=k)
            c.c.new_path(); c.c.set_source_rgba(1, 1, 1, k); c.c.move_to(X0 + 98, Y0 + 78); c.c.line_to(X0 + 116, Y0 + 90)
            c.c.line_to(X0 + 98, Y0 + 102); c.c.close_path(); c.c.fill()
            c.font(SANS, 34, True); c.text(X0 + 140, Y0 + 110, "200 m", (1, 1, 1), k)
            c.font(SANS, 24, True); c.text(X0 + 140, Y0 + 150, "Turn right", (1, 1, 1), k)
            c.pill(PX + 290, Y0 + 115, "bas ek line", size=24, fam=SANS, col=DARK, bg=GMG, bold=True)
            if t > DRIVE + 1.0: white_pill(c, W / 2, 1660, "baaki sab, baad mein", 38)
    stage.compose(cv, t, d, world, K((0, (PX + 60, Y0 + 560), 1.12), (DRIVE - 0.2, (PX + 60, Y0 + 520), 1.12),
                                     (DRIVE + 0.4, (PX + 60, Y0 + 300), 1.2), (d - 0.4, (PX + 60, Y0 + 300), 1.2)),
                  punch=0.04 * max(0, 1 - abs(t - DRIVE) / 0.12), seed=3)
    hud(cv); flash(cv, t, DRIVE, 0.08)


def s3(cv, t, d, st):                                     # what if: all twenty turns at once → confused at the first turn
    def world(c):
        c.font(SANS, 44, True); c.text(W / 2 - c.text_w("agar sab ek saath…") / 2, 560, "agar sab ek saath…", RED)
        n = min(20, int(t * 9))
        for i in range(n):
            col_ = i % 2; row = i // 2
            x = W / 2 - 400 + col_ * 410; y = 640 + row * 64
            c.fill_rrect(x, y, 390, 54, 10, CARD)
            c.font(SANS, 20, True); c.text(x + 14, y + 35, f"{i + 1}. {STEPS[i % len(STEPS)]}", DIM if i > 2 else DOT)
        if t > 2.4:
            for j, (dx, dy) in enumerate([(-200, 300), (180, 420), (0, 560)]):
                if t > 2.4 + j * 0.3: c.font(SANS, 90, True); c.text(W / 2 + dx, 640 + dy, "?", YELLOW)
        if t > 3.4: white_pill(c, W / 2, 1360, "pehle hi mod par confuse", 38)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.0), (d - 0.4, (W / 2, 1000), 1.0)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law named: essentials first, the rest only when needed
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "PROGRESSIVE", 106, W / 2, 630, ease(1 - t / 0.8), col=GM)
        dot_text(c, "DISCLOSURE", 106, W / 2, 760, ease(1 - (t - 0.2) / 0.8), col=GM)
        k = ease(min(1, max(0, (t - 2.0) / 1.2)))
        c.fill_rrect(W / 2 - 320, 900, 640, 120, 22, GM)
        c.font(SANS, 32, True); c.text(W / 2 - 290, 975, "zaroori: pehle", DARK)
        for i in range(3):
            kk = ease(min(1, max(0, k * 3 - i)))
            if kk <= 0: continue
            y = 1040 + i * 90
            c.fill_rrect(W / 2 - 300, y, 600, 76, 16, CARD, kk)
            c.font(SANS, 26, True); c.text(W / 2 - 270, y + 48, ["detail 1", "detail 2", "detail 3"][i], DIM, kk)
        if t > 1.6: c.pill(W / 2 + 230, 1060, "baaki: jab chahiye", size=24, fam=SANS, col=DOT)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1060), 1.0), (d - 0.4, (W / 2, 1080), 1.02)), seed=5)
    hud(cv); flash(cv, t, 0.2)


def s5(cv, t, d, st):                                     # same law: Settings "Advanced", forms "More options"
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("sab yahi law hai") / 2, 560, "sab yahi law hai", GM)
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 200, 660, 400, 600, 24, CARD)
        c.font(SANS, 30, True); c.text(lx - 170, 720, "Settings", DOT)
        for i, r in enumerate(["Wi-Fi", "Display", "Sound"]):
            c.font(SANS, 24, True); c.text(lx - 170, 790 + i * 60, r, DOT)
        op = ease(min(1, max(0, (t - 1.0) / 0.6)))
        c.font(SANS, 24, True); c.text(lx - 170, 990, "Advanced  " + ("▾" if op > 0.5 else "›"), GM)
        for i, r in enumerate(["Developer", "Reset", "Backup"]):
            c.font(SANS, 20, True); c.text(lx - 150, 1050 + i * 50, r, DIM, op)
        c.fill_rrect(rx - 200, 660, 400, 600, 24, CARD)
        c.font(SANS, 30, True); c.text(rx - 170, 720, "Form", DOT)
        for i, r in enumerate(["Name", "Phone"]):
            c.rrect_path(rx - 170, 760 + i * 80, 340, 56, 10); c.c.set_source_rgba(*GREY, 1); c.c.set_line_width(1.5); c.c.stroke()
            c.font(SANS, 20, True); c.text(rx - 150, 796 + i * 80, r, DIM)
        op2 = ease(min(1, max(0, (t - 2.2) / 0.6)))
        c.font(SANS, 24, True); c.text(rx - 170, 960, "More options " + ("▴" if op2 > 0.5 else "▾"), GM)
        for i, r in enumerate(["GST number", "Landmark"]):
            c.rrect_path(rx - 170, 990 + i * 80, 340, 56, 10); c.c.set_source_rgba(*GREY, op2); c.c.set_line_width(1.5); c.c.stroke()
            c.font(SANS, 20, True); c.text(rx - 150, 1026 + i * 80, r, DIM, op2)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 980), 1.02)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # balance: don't over-hide; basics in front, rest one labelled tap away
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.6), ("DO", W * 0.73, t >= 2.6)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 200, 660, 400, 500, 24, CARD)
        c.font(SANS, 26, True); c.text(lx - 170, 720, "Home", DOT)
        c.font(SANS, 34, True); c.text(lx - 10, 860, "⋯", DIM)
        for j, (dx, dy) in enumerate([(-120, 980), (60, 1050)]):
            c.font(SANS, 60, True); c.text(lx + dx, dy, "?", YELLOW)
        c.pill(lx, 1220, "sab chhupa diya ✗", size=24, fam=SANS, col=RED)
        c.fill_rrect(rx - 200, 660, 400, 500, 24, CARD)
        c.font(SANS, 40, True); c.text(rx - 170, 760, "15 min", GMG)
        c.fill_rrect(rx - 170, 800, 160, 64, 32, GM); c.font(SANS, 24, True); c.text(rx - 132, 842, "Start", (1, 1, 1))
        c.font(SANS, 26, True); c.text(rx - 170, 940, "Steps ›", GM)
        c.font(SANS, 26, True); c.text(rx - 170, 1000, "More options ›", GM)
        c.pill(rx, 1220, "basics + 1 tap, saaf label ✓", size=22, fam=SANS, col=GREEN, bold=True)
        if t > 4.0: white_pill(c, W / 2, 1340, "itna mat chhupao ki dhoondhta reh jaaye", 30)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.2, (W * 0.27, 900), 1.45), (2.8, (W * 0.73, 900), 1.45),
                                     (3.8, (W * 0.73, 900), 1.45), (4.4, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 36 script (docs/scripts/day36.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("गूगल मैप्स, आपसे पूरा रास्ता छुपाता है। और इसी वजह से, आप रास्ता नहीं भटकते। डे थर्टी सिक्स में, आज ये उल्टा लॉजिक समझते हैं।", "", D.s0,
          min_dur=5.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("आपने मैप्स में डेस्टिनेशन डाला। स्क्रीन पर बस तीन चीज़ें। पंद्रह मिनट, छह किलोमीटर, और एक बड़ा सा, स्टार्ट बटन।", "", s1, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "riser"), (0.8, "pop"), (1.6, "pop_hi"), (2.2, "pop_hi"), (2.8, "pop_hi"), (3.8, "ding")]),
    Scene("हर मोड़ देखना है? तो स्टेप्स पर टैप करो। और ड्राइव शुरू होते ही, बस एक लाइन। दो सौ मीटर बाद, राइट लो। बाक़ी सब, बाद में।", "", s2,
          min_dur=6.0, whoosh=True, sfx=[(TAP, "pop")] + [(TAP + 0.3 + i * 0.12, "tick") for i in range(6)] + [(DRIVE, "chime"), (DRIVE + 1.0, "ding")]),
    Scene("अगर मैप्स पहले ही, सारे बीस मोड़ एक साथ दिखा देता, तो आप पहले ही मोड़ पर, कन्फ़्यूज़ हो जाते।", "", s3, min_dur=5.0, whoosh=True,
          sfx=[(i * 0.11, "tick") for i in range(20)] + [(2.4, "buzz"), (3.4, "drop")]),
    Scene("इसे कहते हैं, प्रोग्रेसिव डिस्क्लोज़र। पहले सिर्फ़ ज़रूरी चीज़ दिखाओ, और बाक़ी, तभी खोलो, जब यूज़र को सच में चाहिए।", "", s4, min_dur=6.0,
          whoosh=True, sfx=[(0.2, "drop"), (1.6, "pop"), (2.0, "pop_hi"), (2.4, "pop_hi"), (2.8, "pop_hi")]),
    Scene("सेटिंग्स में एडवांस्ड का बटन, फ़ॉर्म में मोर ऑप्शन्स, सब यही लॉ है।", "", s5, min_dur=4.4, whoosh=True,
          sfx=[(1.0, "pop_hi"), (2.2, "pop_hi"), (3.0, "ding")]),
    Scene("पर इतना भी मत छुपाओ, कि यूज़र ढूँढता रह जाए। बेसिक्स सामने, बाक़ी बस एक टैप दूर, और साफ़ लेबल के साथ।", "", s6, min_dur=6.0,
          whoosh=True, sfx=[(0.3, "buzz"), (2.8, "pop_hi"), (4.0, "ding")]),
    Scene("आपके फ़ोन की कौन सी ऐप, एक ही स्क्रीन पर सब कुछ ठूँस देती है? कमेंट में नाम लिखो। और कल, दो नीली लाइनों का राज़, जो दोस्ती तोड़ भी देती हैं।",
          "", D.s8, min_dur=5.6, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = "auto"

if __name__ == "__main__":
    import daily
    daily.run(36, "Progressive Disclosure", SCENES, "day36_progressive_disclosure", cuts=VO_CUTS)

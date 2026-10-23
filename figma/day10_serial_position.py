"""Day 10/45 · Serial Position Effect, explained with Instagram's bottom bar (Home first, Profile last).

People remember the first and last items of a list best and forget the middle, so the most important actions go
at the start and end. Day 02 pattern. Voice: Rakhi's Day 10 ElevenLabs Tisha K file at assets/voice/day10/full.mp3
(content-verified); script in docs/scripts/day10.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 10, "Aesthetic-Usability Effect"
W, H = 1080, 1920
IGPINK = (0.93, 0.25, 0.53)
IGPURPLE = (0.62, 0.36, 0.98)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
TABS = ["Home", "Search", "Reels", "Shop", "Profile"]


def icon(c, kind, x, y, s, col, a=1.0):
    if kind == "Home":
        c.dots_path([(x - 18 * s, y + 16 * s), (x - 18 * s, y - 4 * s), (x, y - 20 * s), (x + 18 * s, y - 4 * s), (x + 18 * s, y + 16 * s),
                     (x - 18 * s, y + 16 * s)], spacing=4, r=1.9, col=col, a=a)
    elif kind == "Search":
        c.dellipse(x - 4 * s, y - 4 * s, 13 * s, 13 * s, spacing=4, r=1.9, col=col, a=a)
        c.dots_path([(x + 6 * s, y + 6 * s), (x + 17 * s, y + 17 * s)], spacing=4, r=1.9, col=col, a=a)
    elif kind == "Reels":
        c.drrect(x - 18 * s, y - 18 * s, 36 * s, 36 * s, 9 * s, spacing=4, r=1.7, col=col, a=a)
        c.dots_path([(x - 5 * s, y - 7 * s), (x + 8 * s, y), (x - 5 * s, y + 7 * s), (x - 5 * s, y - 7 * s)], spacing=3, r=1.6, col=col, a=a)
    elif kind == "Shop":
        c.drrect(x - 16 * s, y - 8 * s, 32 * s, 26 * s, 5 * s, spacing=4, r=1.7, col=col, a=a)
        c.dellipse(x, y - 10 * s, 8 * s, 8 * s, a0=180, a1=360, spacing=3, r=1.6, col=col, a=a)
    else:  # Profile
        c.dellipse(x, y, 19 * s, 19 * s, spacing=4, r=1.9, col=col, a=a)
        c.c.set_source_rgba(*col, 0.85 * a); c.c.arc(x, y, 15 * s, 0, 6.3); c.c.fill()


def ig_screen(c, t, lit=None, dim_mid=0.0, a=1.0):
    """Instagram-style screen with the 5-tab bottom bar. Returns tab centres."""
    phone(c, PX, PY, PW, PH, a=a)
    c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 90, "Instagram", DOT, a)
    for i in range(5): c.dellipse(X0 + 70 + i * 88, Y0 + 170, 32, 32, spacing=5, r=1.5, col=IGPINK if i == 0 else DIM, a=a)   # stories
    c.drrect(X0 + 26, Y0 + 230, PW - 52, 420, 16, spacing=6, r=1.4, col=DIM, a=a)                                             # post
    c._dot(PX, Y0 + 440, 30, IGPURPLE, 0.6 * a)
    by = Y0 + PH - 90
    c.fill_rrect(X0 + 16, by - 50, PW - 32, 100, 0, (0.07, 0.07, 0.09), a)
    pos = []
    for i, tab in enumerate(TABS):
        x = X0 + 60 + i * (PW - 120) / 4
        end = i in (0, 4)
        on = lit is not None and end
        col = IGPINK if on else (GREY if (dim_mid > 0 and not end) else DOT)
        aa = a * (1 - 0.65 * dim_mid if (not end and dim_mid > 0) else 1)
        icon(c, tab, x, by, 1.1, col, aa)
        if on: c.glow(x, by, 50, 0.6)
        pos.append((x, by))
    return pos


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: pehla + aakhri = yaad
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "SERIAL POSITION", 92, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=IGPINK)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "EFFECT kya hai?", 980, DOT, 52, chars=int((t - 2.0) * 14))
        if t > 3.0:                                          # 7 items: first & last glow, middle fade
            fade = ease(min(1, max(0, (t - 3.8) / 1.0)))
            for i in range(7):
                x = 180 + i * 120; end = i in (0, 6)
                if end:
                    c.c.set_source_rgba(*IGPINK, 1); c.c.arc(x, 1180, 40, 0, 6.3); c.c.fill(); c.glow(x, 1180, 70, 0.6)
                    c.font(SANS, 30, True); c.text(x - 9, 1191, str(i + 1), DARK)
                else:
                    c.dellipse(x, 1180, 38, 38, spacing=6, r=2, col=GREY, a=1 - 0.7 * fade)
            c.pill(W / 2, 1320, "pehla + aakhri = yaad", size=30, fam=MONO, col=IGPINK)
        if t > 5.4: c.pill(W / 2, 1430, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=IGPINK, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1100), 1.0), (5.2, (W / 2, 1150), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


def s2(cv, t, d, st):                                     # Instagram bottom bar, 5 buttons
    def world(c):
        pos = ig_screen(c, t)
        st["bar"] = (PX, pos[0][1])
        for i, p in enumerate(pos):
            if t > 1.0 + i * 0.3: c.pill(p[0], p[1] - 70, str(i + 1), size=26, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t > 2.8: c.pill(PX, Y0 + PH + 70, "5 buttons", size=32, fam=MONO, col=DARK, bg=IGPINK, bold=True)
    b = st.get("bar", (PX, Y0 + PH - 90))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, b, 1.7), (d - 0.4, b, 1.7)), seed=3)
    hud(cv)


LIT = 0.6
def s3(cv, t, d, st):                                     # Home & Profile light up, the middle dims
    def world(c):
        dm = ease(min(1, max(0, (t - LIT - 1.2) / 0.8)))
        pos = ig_screen(c, t, lit=True if t > LIT else None, dim_mid=dm)
        st["bar"] = (PX, pos[0][1])
        if t > LIT:
            ring(c, *pos[0], t, LIT, IGPINK); ring(c, *pos[4], t, LIT + 0.5, IGPINK)
            c.pill(pos[0][0], pos[0][1] - 80, "pehla", size=26, fam=MONO, col=DARK, bg=IGPINK, bold=True)
        if t > LIT + 0.5: c.pill(pos[4][0], pos[4][1] - 80, "aakhri", size=26, fam=MONO, col=DARK, bg=IGPINK, bold=True)
        if t > LIT + 1.6:
            for i in (1, 2, 3): c.pill(pos[i][0], pos[i][1] - 80, "?", size=30, fam=MONO, col=GREY)
        if t > LIT + 2.6: white_pill(c, W / 2, Y0 + PH + 80, "beech wale? yaad hi nahi", 36)
    b = st.get("bar", (PX, Y0 + PH - 90))
    stage.compose(cv, t, d, world, K((0, b, 1.7), (d - 0.5, b, 1.7), (d, (PX, Y0 + PH - 40), 1.4)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law card: U-shaped memory curve
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "SERIAL POSITION", 88, W / 2, 630, ease(1 - t / 0.8), col=IGPINK)
        l1 = "shuruaat aur end yaad,"; l2 = "beech ka bhool jaate hain"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 36, chars=n); mono(c, l2, 800, IGPINK, 36, chars=n - len(l1))
        gx, gy, gw, gh = 190, 880, 720, 440
        c.dline(gx, gy + gh, gx + gw, gy + gh, spacing=9, r=1.8, col=DIM); c.dline(gx, gy, gx, gy + gh, spacing=9, r=1.8, col=DIM)
        c.font(MONO, 24); c.text(gx + gw - 200, gy + gh + 44, "list order →", DIM); c.text(gx - 30, gy - 20, "yaad ↑", DIM)
        k = ease((t - 2.0) / 2.4); m = int(k * 60)
        f = lambda u: 0.25 + 0.7 * ((2 * u - 1) ** 2) ** 1.2
        pts = [(gx + i / 60 * gw, gy + gh - f(i / 60) * gh) for i in range(61)]
        for i in range(m + 1):
            x, y = pts[i]; end = i < 12 or i > 48
            c._dot(x, y, 6, IGPINK if end else GREY, 1)
        if m > 0: c.glow(*pts[m], 50, 0.8)
        if m >= 6: c.pill(pts[3][0] + 80, pts[3][1] - 10, "pehla", size=26, fam=MONO, col=DARK, bg=IGPINK, bold=True)
        if m >= 30: c.pill(pts[30][0], pts[30][1] - 50, "beech", size=26, fam=MONO, col=GREY)
        if m >= 60: c.pill(pts[60][0] - 90, pts[60][1] - 10, "aakhri", size=26, fam=MONO, col=DARK, bg=IGPINK, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1050), 1.0), (d - 0.4, (W / 2, 1080), 1.03)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # Instagram puts the most important tabs first & last
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("Instagram") / 2, 540, "Instagram", IGPINK)
        pos = ig_screen(c, t, lit=True, dim_mid=0.4)
        st["bar"] = (PX, pos[0][1])
        if t > 0.8: c.pill(pos[0][0] + 20, pos[0][1] - 90, "sabse zaroori", size=24, fam=MONO, col=DARK, bg=IGPINK, bold=True)
        if t > 1.4: c.pill(pos[4][0] - 20, pos[4][1] - 90, "sabse zaroori", size=24, fam=MONO, col=DARK, bg=IGPINK, bold=True)
        if t > 3.0: white_pill(c, W / 2, Y0 + PH + 80, "Home pehle · Profile aakhir", 36)
    b = st.get("bar", (PX, Y0 + PH - 90))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, b, 1.6), (2.8, b, 1.6), (3.4, ANCHOR, 1.0)), seed=6)
    hud(cv)


def menu(c, cx, top, key_at, col):
    labels = ["Settings", "Help", "Pay now", "Offers", "About"] if key_at == 2 else ["Pay now", "Help", "Offers", "About", "Settings"]
    for i, lab in enumerate(labels):
        y = top + i * 88; key = lab == "Pay now"
        c.fill_rrect(cx - 170, y, 340, 70, 14, (0.28, 0.10, 0.18) if key else (0.12, 0.12, 0.14))
        c.rrect_path(cx - 170, y, 340, 70, 14); c.c.set_source_rgba(*(col if key else GREY), 1); c.c.set_line_width(2.5 if key else 1.2); c.c.stroke()
        c.font(SANS, 28, True); c.text(cx - 140, y + 46, lab, (1, 1, 1) if key else DOT)


def s6(cv, t, d, st):                                     # designer tip: DON'T key action in the middle | DO first/last
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        menu(c, W * 0.27, 680, 2, RED)
        c.pill(W * 0.27, 1160, "main action beech mein", size=24, fam=MONO, col=RED)
        menu(c, W * 0.73, 680, 0, GREEN)
        c.pill(W * 0.73, 1160, "pehle ya aakhri ✓", size=26, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "important = shuruaat ya end", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 10 script (docs/scripts/day10.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे टेन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, सीरियल पोज़िशन इफ़ेक्ट क्या है? लिस्ट की पहली और आख़िरी चीज़ सबसे ज़्यादा याद रहती है। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.4, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (3.0, "pop_hi"), (3.8, "pop_lo"), (5.4, "pop_hi")]),
    Scene("इंस्टाग्राम का नीचे वाला बार देखो। पाँच बटन्स हैं।", "", s2,
          min_dur=4.4, whoosh=True, sfx=[(1.0 + i * 0.3, "pop") for i in range(5)] + [(2.8, "ding")]),
    Scene("सबसे पहले होम, और सबसे आख़िर में आपकी प्रोफ़ाइल। बीच वाले बटन्स? शायद याद भी न हों।", "", s3,
          min_dur=5.6, whoosh=False, sfx=[(LIT, "pop_hi"), (LIT + 0.5, "pop_hi"), (LIT + 1.6, "buzz")]),
    Scene("यही है सीरियल पोज़िशन इफ़ेक्ट। हम लिस्ट की शुरुआत और एंड को सबसे अच्छे से याद रखते हैं, बीच का भूल जाते हैं।", "", s4,
          min_dur=6.8, whoosh=True, sfx=[(0.2, "ding"), (2.0, "riser"), (3.2, "pop"), (4.4, "pop_hi")]),
    Scene("इसीलिए इंस्टाग्राम सबसे ज़रूरी बटन्स, होम और प्रोफ़ाइल, को पहली और आख़िरी जगह पे रखता है।", "", s5,
          min_dur=5.8, whoosh=True, sfx=[(0.8, "pop"), (1.4, "pop"), (3.0, "ding")]),
    Scene("डिज़ाइनर टिप। सबसे इम्पॉर्टेंट एक्शन्स को लिस्ट की शुरुआत या एंड में रखो। बीच में कम ज़रूरी चीज़ें।", "", s6, min_dur=6.4,
          whoosh=True, sfx=[(0.3, "buzz"), (3.0, "pop_hi"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 10 file has only 1 long pause: line cuts found by aligning it to a TTS reading of the script, each snapped to
# the quietest point within 0.8 s (all silent); line check 8/8.
VO_CUTS = [5.38, 17.3, 21.5, 29.36, 38.66, 46.74, 55.34]

if __name__ == "__main__":
    import daily
    daily.run(10, "Serial Position Effect", SCENES, "day10_serial_position", cuts=VO_CUTS)

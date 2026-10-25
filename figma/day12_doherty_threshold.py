"""Day 12/45 · Doherty Threshold, explained with Instagram's like that turns red the instant you double-tap.

When a system responds in under ~400 ms, people stay in flow; slower and attention breaks. Instagram shows the like
immediately (optimistic UI) while the server catches up. Day 02 pattern. Voice: Rakhi's Day 12 ElevenLabs Tisha K
file at assets/voice/day12/full.mp3 (content-verified); script in docs/scripts/day12.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 12, "Tesler's Law"
W, H = 1080, 1920
IGPINK = (0.93, 0.25, 0.53)
HEART = (1.0, 0.25, 0.35)
TEAL = (0.25, 0.85, 0.85)
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def heart(c, x, y, s, col, a=1.0, fill=False):
    pts = []
    for i in range(41):
        u = i / 40 * 6.283
        pts.append((x + 16 * math.sin(u) ** 3 * s, y - (13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u)) * s))
    if fill:
        c.c.move_to(*pts[0])
        for p in pts[1:]: c.c.line_to(*p)
        c.c.close_path(); c.c.set_source_rgba(*col, a); c.c.fill()
    else:
        c.dots_path(pts, spacing=max(3.5, 3 * s), r=1.9, col=col, a=a, closed=True)


def spinner(c, x, y, r, t, col=GREY, a=1.0):
    for i in range(10):
        ang = t * 5 + i / 10 * 6.283
        c._dot(x + math.cos(ang) * r, y + math.sin(ang) * r, 5, col, a * (i + 1) / 10)


def post(c, t, liked_at=None, slow=False, a=1.0, title="Instagram"):
    """Instagram-style post. liked_at: time of the double tap. slow=True: the like only appears after 2 s."""
    phone(c, PX, PY, PW, PH, a=a)
    c.font(SANS, 30, True); c.text(X0 + 30, Y0 + 90, title, DOT if title == "Instagram" else RED, a)
    c.dellipse(X0 + 60, Y0 + 150, 22, 22, spacing=4, r=1.4, col=IGPINK, a=a); c.dbar(X0 + 96, Y0 + 144, 140, rows=2, gap=6, col=DIM, a=a)
    px0, py0, pw, ph = X0 + 20, Y0 + 190, PW - 40, 420
    c.drrect(px0, py0, pw, ph, 12, spacing=6, r=1.4, col=DIM, a=a)
    c._dot(PX, py0 + ph / 2, 60, (0.62, 0.36, 0.98), 0.45 * a); c._dot(PX - 90, py0 + ph / 2 + 70, 30, ORANGE, 0.4 * a)
    hx, hy = X0 + 60, py0 + ph + 50
    show = liked_at is not None and t >= liked_at + (2.0 if slow else 0.0)
    heart(c, hx, hy, 1.4, HEART if show else DOT, a, fill=show)
    c.font(SANS, 22, True); c.text(hx + 36, hy + 8, f"{1204 + (1 if show else 0)} likes", DOT, a)
    big = (PX, py0 + ph / 2)
    if show:
        k = (t - liked_at - (2.0 if slow else 0.0)) / 0.8
        if k < 1: heart(c, big[0], big[1], 5.5 * (0.6 + 0.6 * ease(min(1, k * 3))), (1, 1, 1), a * (1 - k) ** 0.6, fill=True)
    if slow and liked_at is not None and liked_at <= t < liked_at + 2.0:
        spinner(c, big[0], big[1], 40, t, (1, 1, 1), a)
    return big, (hx, hy)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # hook: 400 ms stopwatch, flow green / red
    def world(c):
        mono(c, "kya aapko pata hai?", 690, DOT, 58, chars=int(t * 16))
        if t > 1.2:
            dot_text(c, "DOHERTY THRESHOLD", 84, W / 2, 850, ease(1 - (t - 1.2) / 0.8), col=TEAL)
            c.glow(W / 2, 850, 420, 0.08)
        if t > 2.0: mono(c, "kya hai?", 980, DOT, 56, chars=int((t - 2.0) * 14))
        if t > 3.0:
            cx, cy, r = W / 2, 1210, 120
            c.dellipse(cx, cy, r, r, spacing=7, r=2.2, col=DOT)
            ms = min(800, int((t - 3.0) * 420))
            ang = -math.pi / 2 + ms / 800 * 2 * math.pi
            col = GREEN if ms <= 400 else RED
            c.dots_path([(cx, cy), (cx + math.cos(ang) * (r - 20), cy + math.sin(ang) * (r - 20))], spacing=8, r=2.6, col=col)
            a4 = -math.pi / 2 + math.pi; c._dot(cx + math.cos(a4) * r, cy + math.sin(a4) * r, 10, YELLOW, 1)
            c.pill(cx, cy + r + 50, f"{ms} ms", size=34, fam=MONO, col=DARK, bg=col, bold=True)
            c.pill(cx + 250, cy, "400 ms", size=26, fam=MONO, col=YELLOW)
        if t > 5.6: c.pill(W / 2, 1520, "aaj live app se samjhein →", size=34, fam=SANS, col=DARK, bg=TEAL, bold=True)
        for i in range(12):
            ang = t * 0.8 + i / 12 * 6.283
            c._dot(W / 2 + math.cos(ang) * 470, 850 + math.sin(ang) * 300, 5, COLS[i % 6], 0.8)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.3), (1.2, (W / 2, 850), 1.3), (2.1, (W / 2, 960), 1.0),
                                     (3.0, (W / 2, 1150), 1.0), (5.4, (W / 2, 1200), 1.05)), seed=2)
    hud(cv); flash(cv, t, 1.2)


TAP = 1.2
def s2(cv, t, d, st):                                     # Instagram: double tap -> heart red instantly
    def world(c):
        big, h = post(c, t, liked_at=TAP)
        st["big"] = big
        for k, dt in enumerate((0, 0.18)):
            tt = TAP - 0.25 + dt
            if tt - 0.12 < t < tt + 0.1: c._dot(big[0] + 10, big[1] + 12, 18, (1, 1, 1), 0.9)
        if t > TAP + 0.2: c.pill(PX + 330, h[1], "0.1 s ✓", size=32, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > TAP + 1.4: white_pill(c, W / 2, 1640, "usi pal laal!", 38)
    b = st.get("big", (PX, Y0 + 400))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, b, 1.35), (TAP + 1.2, b, 1.35), (TAP + 1.8, ANCHOR, 1.0)),
                  punch=0.05 * max(0, 1 - abs(t - TAP) / 0.1), seed=3)
    hud(cv)


STAP = 0.8
def s3(cv, t, d, st):                                     # App X: 2 s spinner, flow breaks
    def world(c):
        big, h = post(c, t, liked_at=STAP, slow=True, title="App X")
        st["big"] = big
        if STAP - 0.2 < t < STAP + 0.1: c._dot(big[0] + 10, big[1] + 12, 18, (1, 1, 1), 0.9)
        if STAP < t < STAP + 2.0: c.pill(PX + 330, big[1], f"{t - STAP:.1f} s...", size=32, fam=MONO, col=DARK, bg=YELLOW, bold=True)
        if t > STAP + 2.0: c.pill(PX + 330, big[1], "2.0 s ✗", size=32, fam=SANS, col=DARK, bg=RED, bold=True)
        if t > STAP + 2.6:
            for i in range(4):
                ang = -2.4 + i * 0.6
                c.pill(PX + math.cos(ang) * 320, PY + math.sin(ang) * 440, "?", size=34, fam=MONO, col=RED)
        if t > STAP + 3.0: white_pill(c, W / 2, 1640, "maza hi khatam", 38)
    b = st.get("big", (PX, Y0 + 400))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.5, b, 1.35), (STAP + 2.4, b, 1.35), (STAP + 3.0, ANCHOR, 1.0)), seed=4)
    hud(cv); flash(cv, t, STAP + 2.0, 0.1)


def s4(cv, t, d, st):                                     # law card: 400 ms line, flow ✓ / ✗
    def world(c):
        c.pill(W / 2, 520, "UX LAW", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "DOHERTY THRESHOLD", 80, W / 2, 630, ease(1 - t / 0.8), col=TEAL)
        l1 = "400 ms ke andar jawab ="; l2 = "user ka flow nahi toot-ta"
        n = int(max(0, t - 0.9) * 28)
        mono(c, l1, 750, DOT, 36, chars=n); mono(c, l2, 800, TEAL, 36, chars=n - len(l1))
        x0, x1, y = 160, 920, 1080
        c.fill_rrect(x0, y, x1 - x0, 30, 15, (0.2, 0.2, 0.23))
        xm = x0 + (x1 - x0) * 0.4
        k = ease(min(1, max(0, (t - 2.0) / 2.4)))
        xe = lerp(x0, x1, k)
        c.fill_rrect(x0, y, max(30, min(xe, xm) - x0), 30, 15, GREEN)
        if xe > xm: c.fill_rrect(xm, y, xe - xm, 30, 0, RED)
        c.dline(xm, y - 60, xm, y + 90, spacing=8, r=2.2, col=YELLOW)
        c.pill(xm, y - 90, "400 ms", size=30, fam=MONO, col=DARK, bg=YELLOW, bold=True)
        c.font(MONO, 24); c.text(x0, y + 80, "0", DIM); c.text(x1 - 60, y + 80, "1 s+", DIM)
        if k > 0.3: c.pill((x0 + xm) / 2, y + 170, "flow ✓", size=32, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if k > 0.8: c.pill((xm + x1) / 2, y + 170, "flow ✗", size=32, fam=SANS, col=DARK, bg=RED, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.3), (1.8, (W / 2, 1050), 1.0), (d - 0.4, (W / 2, 1080), 1.03)), seed=5)
    hud(cv)


T5 = 1.0
def s5(cv, t, d, st):                                     # Instagram shows the like instantly; the server catches up quietly
    def world(c):
        c.font(SANS, 60, True); c.text(W / 2 - c.text_w("Instagram") / 2, 540, "Instagram", IGPINK)
        big, h = post(c, t, liked_at=T5)
        st["h"] = h
        if t > T5:                                           # little "server" dot travelling in the background
            u = min(1, (t - T5) / 2.6)
            sx, sy = lerp(h[0], X0 + PW - 50, u), lerp(h[1], Y0 + 120, u)
            c._dot(sx, sy, 7, TEAL, 0.9 if u < 1 else 0.4)
            c.font(MONO, 18); c.text(X0 + PW - 150, Y0 + 100, "server..." if u < 1 else "synced ✓", TEAL)
        if t > T5 + 0.3: c.pill(PX - 330, h[1], "turant dikha", size=28, fam=MONO, col=DARK, bg=GREEN, bold=True)
        if t > T5 + 1.6: c.pill(PX + 330, Y0 + 120, "kaam peeche", size=28, fam=MONO, col=DARK, bg=TEAL, bold=True)
    hh = st.get("h", (X0 + 60, Y0 + 660))
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX, Y0 + 420), 1.25), (d - 0.4, (PX, Y0 + 420), 1.25)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # designer tip: DON'T no feedback | DO instant feedback + progress
    def world(c):
        for lab, x, on in [("DON'T", W * 0.27, t < 2.8), ("DO", W * 0.73, t >= 2.8)]:
            c.font(SANS, 72, True); c.text(x - c.text_w(lab) / 2, 560, lab, (RED if lab == "DON'T" else GREEN) if on else DIM)
        for yy in range(600, 1450, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 150, 760, 300, 90, 45, (0.25, 0.25, 0.28)); c.font(SANS, 28, True); c.text(lx - 52, 816, "Submit", DOT)
        tp = (t * 1.2) % 1.6
        if tp < 0.25: c._dot(lx + 10, 812, 16, (1, 1, 1), 0.9)
        c.font(SANS, 24); c.text(lx - 120, 920, "...kuch hua?", DIM)
        c.pill(lx, 1160, "koi feedback nahi", size=26, fam=MONO, col=RED)
        pressed = t > 3.2
        c.fill_rrect(rx - 150, 760, 300, 90, 45, GREEN if pressed else (0.25, 0.25, 0.28))
        c.font(SANS, 28, True); lab = "Sending ✓" if pressed else "Submit"; c.text(rx - c.text_w(lab) / 2, 816, lab, DARK if pressed else DOT)
        ring(c, rx, 805, t, 3.2, GREEN)
        if pressed:
            k = min(1, (t - 3.4) / 1.8)
            c.fill_rrect(rx - 150, 900, 300, 18, 9, (0.2, 0.2, 0.23)); c.fill_rrect(rx - 150, 900, max(18, 300 * k), 18, 9, TEAL)
            c.font(MONO, 20); c.text(rx - 150, 960, f"{int(k * 100)}%", TEAL)
        c.pill(rx, 1160, "turant feedback + progress", size=24, fam=SANS, col=GREEN, bold=True)
        if t > 5.0: white_pill(c, W / 2, 1300, "har tap ka turant jawab", 36)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 900), 1.45), (2.4, (W * 0.27, 900), 1.45), (3.0, (W * 0.73, 900), 1.45),
                                     (4.6, (W * 0.73, 900), 1.45), (5.2, ANCHOR, 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 12 script (docs/scripts/day12.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे ट्वेल्व।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("क्या आपको पता है, डोहर्टी थ्रेशोल्ड क्या है? ऐप जितनी जल्दी जवाब दे, हम उतना ज़्यादा उसमें खो जाते हैं। चलो, आज एक लाइव ऐप के थ्रू समझते हैं।",
          "", s1, min_dur=7.6, whoosh=True, sfx=[(1.2, "drop"), (2.0, "pop"), (3.0, "tick"), (3.5, "tick"), (3.95, "pop_hi"), (4.5, "buzz"), (5.6, "pop_hi")]),
    Scene("इंस्टाग्राम पे किसी फ़ोटो को डबल टैप करो, और दिल उसी पल लाल हो जाता है।", "", s2,
          min_dur=4.6, whoosh=True, clicks=[TAP - 0.25, TAP - 0.07], sfx=[(TAP, "pop_hi"), (TAP + 0.2, "chime")]),
    Scene("अब सोचो, अगर लाइक होने में दो सेकंड लगते, और लोडिंग घूमती रहती। मज़ा ही ख़त्म।", "", s3,
          min_dur=5.4, whoosh=True, clicks=[STAP - 0.1], sfx=[(STAP + i * 0.4, "tick") for i in range(5)] + [(STAP + 2.0, "buzz")]),
    Scene("यही है डोहर्टी थ्रेशोल्ड। अगर ऐप चार सौ मिलीसेकंड के अंदर जवाब दे, तो यूज़र का फ़्लो नहीं टूटता।", "", s4,
          min_dur=6.6, whoosh=True, sfx=[(0.2, "ding"), (2.0, "riser"), (3.0, "pop_hi"), (4.2, "buzz")]),
    Scene("इसीलिए इंस्टाग्राम लाइक तुरंत दिखा देता है, और सर्वर पे काम पीछे चुपचाप होता रहता है।", "", s5,
          min_dur=5.8, whoosh=True, clicks=[T5 - 0.1], sfx=[(T5, "pop_hi"), (T5 + 1.6, "pop"), (T5 + 2.6, "ding")]),
    Scene("डिज़ाइनर टिप, हर टैप का तुरंत फ़ीडबैक दो, और अगर टाइम लगे, तो प्रोग्रेस दिखाओ।", "", s6, min_dur=6.4,
          whoosh=True, clicks=[3.2], sfx=[(0.3, "buzz"), (3.22, "chime"), (5.0, "ding")]),
    Scene("ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

if __name__ == "__main__":
    import daily
    daily.run(12, "Doherty Threshold", SCENES, "day12_doherty_threshold")

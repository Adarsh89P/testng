"""Day 19/45 · Law of Prägnanz, explained with WhatsApp's simple icons.

People read complex or ambiguous images in the simplest form possible: broken, tangled arcs are seen as "five
circles". WhatsApp's bottom-bar icons (Chats, Updates, Communities, Calls) are built from two or three simple shapes,
so they're recognised at a glance even without labels; the same icons loaded with detail, shadows and colours blur
on a small screen. Day 02 pattern; the script opens with a "what do you see?" test and names the law before the app.
Voice: Rakhi's Day 19 ElevenLabs Tisha K file at assets/voice/day19/full.mp3 (content-verified); script in
docs/scripts/day19.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 19, "Occam's Razor"
W, H = 1080, 1920
WA = (0.15, 0.83, 0.40)                           # WhatsApp green
WAD = (0.04, 0.27, 0.20)                          # dark green selected pill
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2
RING_COLS = [BLUE, YELLOW, (0.85, 0.85, 0.88), GREEN, RED]
TABS = ["Chats", "Updates", "Communities", "Calls"]


def five_rings(c, cx, cy, r, split=0.0, a=1.0):
    """Olympic-style rings drawn as separate arc fragments; split>0 pulls the fragments apart."""
    centres = [(-2.2, 0), (0, 0), (2.2, 0), (-1.1, 1.0), (1.1, 1.0)]
    for i, (dx, dy) in enumerate(centres):
        x, y = cx + dx * r, cy + dy * r
        for j in range(4):
            a0 = j * 90 + 12; a1 = a0 + 66
            mid = math.radians((a0 + a1) / 2)
            ox, oy = math.cos(mid) * split * 40, math.sin(mid) * split * 40
            c.dellipse(x + ox, y + oy, r * 0.95, r * 0.95, a0=a0, a1=a1, spacing=6, r=3.6, col=RING_COLS[i], a=a)


def icon(c, kind, x, y, s=1.0, col=DOT, a=1.0, busy=0.0):
    """WhatsApp-style tab icons from 2–3 simple shapes. busy>0 adds clutter (gradient blobs, shadows, specks)."""
    if busy > 0:
        for k in range(14):
            ang = k * 2.39; rr = (8 + (k * 7) % 22) * s
            col2 = COLS[k % 6]
            c._dot(x + math.cos(ang) * rr * 1.6, y + math.sin(ang) * rr * 1.2, (4 + k % 5) * s, col2, 0.55 * busy * a)
        c.fill_rrect(x - 30 * s + 6, y - 26 * s + 8, 60 * s, 52 * s, 14 * s, (0, 0, 0), 0.6 * busy * a)
    if kind == "chats":
        c.rrect_path(x - 30 * s, y - 24 * s, 60 * s, 44 * s, 14 * s); c.c.set_source_rgba(*col, a); c.c.set_line_width(4 * s); c.c.stroke()
        c.c.new_path(); c.c.move_to(x - 18 * s, y + 18 * s); c.c.line_to(x - 26 * s, y + 32 * s); c.c.line_to(x - 6 * s, y + 20 * s)
        c.c.set_source_rgba(*col, a); c.c.set_line_width(4 * s); c.c.stroke()
    elif kind == "updates":
        c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x, y, 12 * s, 0, 6.2832); c.c.fill()
        for j in range(6):
            c.c.new_path(); c.c.arc(x, y, 26 * s, math.radians(j * 60 + 8), math.radians(j * 60 + 48))
            c.c.set_source_rgba(*col, a); c.c.set_line_width(4 * s); c.c.stroke()
    elif kind == "communities":
        for dx, dy, rr in [(-18, 6, 10), (18, 6, 10), (0, -6, 13)]:
            c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x + dx * s, y + dy * s, rr * s, 0, 6.2832); c.c.fill()
        c.c.new_path()
    elif kind == "calls":
        c.c.new_path(); c.c.arc(x + 6 * s, y - 6 * s, 26 * s, math.radians(100), math.radians(170))
        c.c.set_source_rgba(*col, a); c.c.set_line_width(9 * s); c.c.stroke()
        for (ex, ey) in [(-22, -14), (2, 18)]:
            c.fill_rrect(x + ex * s - 7 * s, y + ey * s - 7 * s, 16 * s, 14 * s, 4 * s, col, a)
    c.c.new_path()


KINDS = ["chats", "updates", "communities", "calls"]


def wa_screen(c, labels=1.0, sel=0, busy=0.0, a=1.0):
    phone(c, PX, PY, PW, PH)
    c.font(SANS, 32, True); c.text(X0 + 26, Y0 + 96, "WhatsApp", WA if busy == 0 else DOT, a)
    for i in range(5):
        y = Y0 + 150 + i * 96
        c.c.new_path(); c.c.set_source_rgba(*COLS[i % 6], 0.85 * a); c.c.arc(X0 + 60, y + 36, 28, 0, 6.2832); c.c.fill()
        c.dbar(X0 + 104, y + 24, 180, rows=1, gap=4, col=DOT); c.dbar(X0 + 104, y + 50, 260, rows=1, gap=4, col=DIM)
    by = Y0 + PH - 110
    c.c.new_path(); c.c.set_source_rgba(0.10, 0.10, 0.11, a); c.c.rectangle(X0 + 8, by - 50, PW - 16, 140); c.c.fill()
    for i, k in enumerate(KINDS):
        x = X0 + 60 + i * 120
        if i == sel and busy == 0: c.fill_rrect(x - 44, by - 26, 88, 52, 26, WAD, a)
        icon(c, k, x, by, 0.62, WA if (i == sel and busy == 0) else DOT, a, busy)
        if labels > 0:
            c.font(SANS, 16, True); c.text(x - c.text_w(TABS[i]) / 2, by + 56, TABS[i], DOT, labels * a)


# ------------------------------------------------------------------ scenes
SPLIT = 4.2
def s1(cv, t, d, st):                                     # test: what do you see? "5 circles" — really broken arcs
    def world(c):
        mono(c, "ek chhota sa test", 640, DOT, 50, chars=int(t * 18))
        if t > 1.0: mono(c, "kya dikh raha hai?", 720, YELLOW, 50, chars=int((t - 1.0) * 18))
        sp = ease(min(1, max(0, (t - SPLIT) / 1.0)))
        five_rings(c, W / 2, 1000, 95, split=sp, a=ease(min(1, t / 0.8)))
        if 2.6 < t < SPLIT: c.pill(W / 2, 1300, "5 gole?", size=40, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > SPLIT + 0.8: c.pill(W / 2, 1300, "asal mein: tooti-phooti lines", size=32, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 850), 1.1), (2.4, (W / 2, 1000), 1.15), (SPLIT, (W / 2, 1050), 1.15),
                                     (d - 0.4, (W / 2, 1050), 1.05)), punch=0.05 * max(0, 1 - abs(t - SPLIT) / 0.12), seed=2)
    hud(cv); flash(cv, t, SPLIT, 0.1)


MORPH = 1.6
def s2(cv, t, d, st):                                     # brain picks the simplest shape → law named
    def world(c):
        k = ease(min(1, max(0, (t - MORPH) / 1.4)))
        cx, cy = W / 2, 820
        pts = []
        for i in range(73):
            th = i / 72 * 6.2832
            wob = 60 * math.sin(th * 5 + 1.3) + 38 * math.cos(th * 9) + 25 * math.sin(th * 13 + 0.5)
            rr = 170 + wob * (1 - k)
            pts.append((cx + math.cos(th) * rr, cy + math.sin(th) * rr))
        c.dots_path(pts, spacing=7, r=3, col=YELLOW if k >= 1 else DOT)
        if t < MORPH: c.pill(W / 2, 1060, "ulajhi cheez", size=28, fam=MONO, col=DOT)
        elif k >= 1: c.pill(W / 2, 1060, "dimaag: sabse aasaan shape → ●", size=28, fam=SANS, col=DARK, bg=YELLOW, bold=True)
        if t > 3.6:
            c.pill(W / 2, 1180, "isi ko kehte hain", size=26, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
            dot_text(c, "LAW OF PRÄGNANZ", 86, W / 2, 1300, ease(1 - (t - 3.6) / 0.8), col=WA)
            c.glow(W / 2, 1300, 420, 0.08)
    stage.compose(cv, t, d, world, K((0, (W / 2, 820), 1.15), (3.2, (W / 2, 900), 1.0), (d - 0.4, (W / 2, 1060), 1.0)), seed=3)
    hud(cv); flash(cv, t, MORPH + 1.4, 0.08); flash(cv, t, 3.6)


def s3(cv, t, d, st):                                     # WhatsApp bottom bar: each icon = 2–3 simple shapes
    PARTS = [("1 bubble", 1.4), ("gole", 2.6), ("gole", 3.4), ("1 phone", 4.2)]
    def world(c):
        wa_screen(c, labels=1.0, sel=0)
        by = Y0 + PH - 110
        for i, (lab, at) in enumerate(PARTS):
            if t > at:
                x = X0 + 60 + i * 120
                ring(c, x, by, t, at, col=WA)
                c.pill(x, by - 100 - (i % 2) * 60, lab, size=22, fam=MONO, col=DARK, bg=WA, bold=True)
        if t > 0.6: c.pill(PX, Y0 + 640, "Chats · Updates · Communities · Calls", size=20, fam=SANS, col=DOT)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.8, (PX, Y0 + PH - 200), 1.45), (d - 0.4, (PX, Y0 + PH - 200), 1.4)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # labels hidden: still understood at a glance
    def world(c):
        lab = 1 - ease(min(1, max(0, (t - 0.4) / 0.6)))
        wa_screen(c, labels=lab, sel=int(min(3, max(0, (t - 1.4) / 0.6))) if t > 1.4 else 0)
        by = Y0 + PH - 110
        for i, nm in enumerate(TABS):
            at = 1.4 + i * 0.6
            if t > at:
                x = X0 + 60 + i * 120
                c.pill(x, by + 90, nm + " ✓", size=18, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 4.0: white_pill(c, W / 2, 1660, "ek jhalak mein samajh", 38)
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + PH - 200), 1.4), (d - 0.4, (PX, Y0 + PH - 180), 1.3)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # contrast: busy icons with detail, shadow and colour blur
    def world(c):
        busy = ease(min(1, max(0, (t - 0.6) / 1.2)))
        wa_screen(c, labels=0.0, sel=0, busy=busy)
        by = Y0 + PH - 110
        if t > 2.2:
            for i in range(4):
                c.font(SANS, 46, True); c.text(X0 + 48 + i * 120, by - 60, "?", RED)
        if t > 1.2: c.pill(PX, Y0 + 560, "detail + shadow + rang", size=26, fam=MONO, col=DARK, bg=RED, bold=True)
        if t > 3.2: white_pill(c, W / 2, 1660, "chhoti screen pe sab dhundhla", 36)
    stage.compose(cv, t, d, world, K((0, (PX, Y0 + PH - 200), 1.3), (d - 0.4, (PX, Y0 + PH - 160), 1.5)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # tip: fewest shapes → fastest understanding
    def world(c):
        c.font(SANS, 56, True); c.text(W / 2 - c.text_w("kam shapes, jaldi samajh") / 2, 560, "kam shapes, jaldi samajh", WA)
        k = ease(min(1, max(0, (t - 1.0) / 1.6)))
        n = int(round(12 - 9 * k))
        for i in range(12):
            if i >= n: continue
            ang = i * 0.52; rr = 150 * (1 - k)
            c._dot(W / 2 - 230 + math.cos(ang) * rr, 950 + math.sin(ang) * rr, 18, COLS[i % 6], 0.9)
        icon(c, "chats", W / 2 - 230, 950, 2.2 * k, WA, k)
        c.font(MONO, 34, True); c.text(W / 2 - 300, 1180, f"{n} shapes", DOT)
        c.font(SANS, 30, True); c.text(W / 2 + 80, 900, "ek bubble", DOT, k)
        c.font(SANS, 30, True); c.text(W / 2 + 80, 960, "+ ek tail", DOT, k)
        c.font(SANS, 30, True); c.text(W / 2 + 80, 1020, "= Chats", WA, k)
        if t > 3.4: white_pill(c, W / 2, 1360, "jitna simple, utni jaldi samajh", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.1), (d - 0.4, (W / 2, 1000), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 19 script (docs/scripts/day19.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("पैंतालीस यू एक्स लॉज़ का, डे नाइनटीन।", "", D.s0, min_dur=4.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("एक छोटा सा टेस्ट। स्क्रीन पे क्या दिख रहा है? ज़्यादातर लोग कहेंगे, पाँच गोले। पर असल में, ये तो बस टूटी-फूटी, उलझी हुई लाइनें हैं।",
          "", s1, min_dur=6.8, whoosh=True, sfx=[(0.2, "pop"), (1.0, "pop_hi"), (2.6, "ding"), (SPLIT, "drop"), (SPLIT + 0.8, "pop")]),
    Scene("हमारा दिमाग़ हमेशा सबसे आसान शेप ढूँढता है। उलझी चीज़ को भी, वो सबसे सिंपल तरीके से पढ़ लेता है। इसी को कहते हैं, लॉ ऑफ़ प्रैग्नैंज़।",
          "", s2, min_dur=6.4, whoosh=True, sfx=[(MORPH, "riser"), (MORPH + 1.4, "chime"), (3.6, "drop")]),
    Scene("अब वॉट्सऐप के नीचे देखो। चैट्स, अपडेट्स, कम्युनिटीज़, कॉल्स। हर आइकन, बस दो-तीन सिंपल शेप्स से बना है। एक बबल, एक फ़ोन, कुछ गोले।",
          "", s3, min_dur=6.0, whoosh=True, sfx=[(0.6, "pop"), (1.4, "pop_hi"), (2.6, "pop_hi"), (3.4, "pop_hi"), (4.2, "pop_hi")]),
    Scene("इसीलिए, बिना लेबल पढ़े भी, एक झलक में समझ आ जाता है, कौन सा आइकन क्या करता है।", "", s4,
          min_dur=5.4, whoosh=True, sfx=[(0.4, "pop_lo")] + [(1.4 + i * 0.6, "pop") for i in range(4)] + [(4.0, "ding")]),
    Scene("सोचो, अगर यही आइकन ढेर सारी डिटेल, शैडो और रंगों से भरे होते। छोटी स्क्रीन पे, सब धुंधला सा लगता।", "", s5,
          min_dur=5.4, whoosh=True, sfx=[(0.6, "riser"), (1.2, "pop"), (2.2, "buzz"), (3.2, "pop_lo")]),
    Scene("तो अगली बार आइकन बनाओ, तो कम से कम शेप्स में बात कहो। जितना सिंपल, उतनी जल्दी समझ।", "", s6, min_dur=5.6,
          whoosh=True, sfx=[(1.0, "riser"), (2.6, "chime"), (3.4, "ding")]),
    Scene("कल मिलेंगे ओकम्स रेज़र के साथ। पसंद आया हो तो शेयर करो, और डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0,
          whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = "auto"

if __name__ == "__main__":
    import daily
    daily.run(19, "Law of Prägnanz", SCENES, "day19_pragnanz", cuts=VO_CUTS)

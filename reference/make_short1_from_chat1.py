"""Render Short #1 "Why You're Always Broke" as a 1080x1920 stickman animation with voice, captions, SFX, music."""
import math, sys, subprocess, random
import numpy as np, cairo, soundfile as sf
from kokoro_onnx import Kokoro

OUT = sys.argv[1]            # output dir (contains voices/)
W, H, FPS, SR = 1080, 1920, 30, 24000
FONT = "Inter"
BG = (0.961, 0.945, 0.910)
INK = (0.08, 0.08, 0.09)
GREEN = (0.12, 0.62, 0.33)
RED = (0.86, 0.20, 0.18)
YEL = (1.0, 0.83, 0.0)
GOLD = (0.97, 0.74, 0.12)

# ---------------------------------------------------------------- script
LINES = [
    ("You earn more than you did three years ago. So why are you still broke? It's not your salary. It's your brain.",
     "You earn more than 3 years ago… so why are you STILL broke? It's not your salary. It's your brain.",
     "WHY ARE YOU STILL BROKE?"),
    ("Trap one: lifestyle creep. Every raise, you upgrade your phone, your bike, your food. Your income goes up, but so does everything else.",
     "Trap 1: lifestyle creep. Every raise, you upgrade your phone, your bike, your food. Income goes up… but so does everything else.",
     "TRAP 1: LIFESTYLE CREEP"),
    ("Trap two: your brain loves now. Five thousand rupees today feels better than fifty thousand later. So you buy, and future you pays.",
     "Trap 2: your brain loves NOW. ₹5,000 today feels better than ₹50,000 later. So you buy… and future-you pays.",
     "TRAP 2: YOUR BRAIN LOVES “NOW”"),
    ("Trap three: comparison. You see your friend's new car on Instagram, and suddenly, your perfectly fine life feels poor.",
     "Trap 3: comparison. You see your friend's new car on Instagram… and suddenly your perfectly fine life feels poor.",
     "TRAP 3: COMPARISON"),
    ("The fix? Next raise, save half of it before you even see it. Follow for part two: why middle class people stay middle class.",
     "The fix? Next raise, save HALF of it before you even see it. Follow for Part 2: why middle class people stay middle class.",
     "THE FIX: SAVE 50% OF EVERY RAISE"),
]

# ---------------------------------------------------------------- voice
k = Kokoro(f"{OUT}/voices/kokoro-v1.0.onnx", f"{OUT}/voices/voices-v1.0.bin")
LEAD, GAP = 0.35, 0.35
voice_parts, scenes = [np.zeros(int(LEAD * SR), np.float32)], []
t = LEAD
for spoken, shown, head in LINES:
    s, sr = k.create(spoken, voice="am_michael", speed=1.12, lang="en-us")
    assert sr == SR
    s = s.astype(np.float32)
    dur = len(s) / SR
    start = t - (LEAD if not scenes else 0)
    scenes.append(dict(start=start, vstart=t, vdur=dur, end=t + dur + GAP, shown=shown, head=head))
    voice_parts += [s, np.zeros(int(GAP * SR), np.float32)]
    t += dur + GAP
TOTAL = t + 0.6
voice = np.concatenate(voice_parts)
voice = np.pad(voice, (0, int(TOTAL * SR) - len(voice)))
print("total", round(TOTAL, 2), [round(s["end"] - s["start"], 2) for s in scenes])

# ---------------------------------------------------------------- captions (approximate word timing)
cap_chunks = []
for sc in scenes:
    words = sc["shown"].split()
    wts = np.array([len(w) + 2.5 for w in words], float)
    edges = sc["vstart"] + np.concatenate([[0], np.cumsum(wts)]) / wts.sum() * sc["vdur"]
    chunk = []
    for i, w in enumerate(words):
        chunk.append((w, edges[i], edges[i + 1]))
        if len(chunk) == 3 or w[-1] in ".?!…:," or i == len(words) - 1:
            cap_chunks.append(chunk)
            chunk = []

# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(p): p = clamp(p); return p * p * (3 - 2 * p)
def back(p):
    p = clamp(p); c1 = 1.9; return 1 + (c1 + 1) * (p - 1) ** 3 + c1 * (p - 1) ** 2
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def lerp(a, b, p): return a + (b - a) * p
def rad(d): return math.radians(d)
def pol(x, y, ang, l): return x + math.cos(rad(ang)) * l, y + math.sin(rad(ang)) * l

def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()

def font(c, size, bold=True):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)

def text_c(c, s, x, y, size, rgb=INK, bold=True):
    font(c, size, bold); e = c.text_extents(s)
    c.move_to(x - e.width / 2 - e.x_bearing, y); c.set_source_rgb(*rgb); c.show_text(s)

def stroke_style(c, lw, rgb=INK):
    c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_source_rgb(*rgb)

# ---------------------------------------------------------------- stickman
def stick(c, x, y, s=1.0, la=(150, 110), ra=(30, 70), ll=(105, 95), rl=(75, 85),
          mood="neutral", look=(0, 0), tilt=0, lean=0, alpha=1.0, tie=True):
    """(x,y)=hip. Angles in degrees (0=right, 90=down). Returns hand positions."""
    lw = 11 * s
    c.save(); c.push_group()
    neck = pol(x, y, -90 + lean, 175 * s)
    sh = pol(x, y, -90 + lean, 150 * s)
    stroke_style(c, lw)
    # legs
    for (a1, a2) in (ll, rl):
        k1 = pol(x, y, a1, 95 * s); f = pol(*k1, a2, 95 * s)
        c.move_to(x, y); c.line_to(*k1); c.line_to(*f); c.stroke()
    # body
    c.move_to(x, y); c.line_to(*neck); c.stroke()
    hands = []
    for (a1, a2) in (la, ra):
        e = pol(*sh, a1, 80 * s); h = pol(*e, a2, 75 * s); hands.append(h)
        c.move_to(*sh); c.line_to(*e); c.line_to(*h); c.stroke()
    if tie:
        tx, ty = pol(*neck, 90 + lean, 14 * s)
        c.move_to(tx, ty); c.line_to(tx - 11 * s, ty + 16 * s); c.line_to(tx, ty + 52 * s)
        c.line_to(tx + 11 * s, ty + 16 * s); c.close_path(); c.set_source_rgb(*GREEN); c.fill()
    # head
    r = 58 * s
    hx, hy = pol(*neck, -90 + lean + tilt, r + 4 * s)
    c.arc(hx, hy, r, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    stroke_style(c, lw); c.stroke()
    ex, ey = look[0] * 9 * s, look[1] * 7 * s
    c.save(); c.translate(hx, hy); c.rotate(rad(tilt + lean))
    for sx in (-1, 1):
        c.arc(sx * 20 * s + ex, -6 * s + ey, (8.5 if mood != "shock" else 10) * s, 0, 2 * math.pi)
        c.set_source_rgb(*INK); c.fill()
    stroke_style(c, 5.5 * s)
    for sx in (-1, 1):                                   # brows
        if mood == "sad":    a, b = (sx * 8, -30), (sx * 30, -24)
        elif mood == "shock": a, b = (sx * 10, -36), (sx * 30, -38)
        elif mood == "happy": a, b = (sx * 10, -30), (sx * 30, -33)
        else:                a, b = (sx * 10, -28), (sx * 30, -28)
        c.move_to(a[0] * s, a[1] * s); c.line_to(b[0] * s, b[1] * s); c.stroke()
    if mood == "happy":
        c.arc(0, 14 * s, 18 * s, rad(20), rad(160)); c.stroke()
    elif mood == "sad":
        c.arc(0, 36 * s, 15 * s, rad(205), rad(335)); c.stroke()
    elif mood == "shock":
        c.save(); c.translate(0, 26 * s); c.scale(1, 1.3); c.arc(0, 0, 9 * s, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*INK); c.fill()
    else:
        c.move_to(-10 * s, 24 * s); c.line_to(10 * s, 24 * s); c.stroke()
    c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(alpha); c.restore()
    return hands, (hx, hy)

# ---------------------------------------------------------------- props
def wallet(c, x, y, rot, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    rrect(c, -70 * s, -45 * s, 140 * s, 90 * s, 14 * s); c.set_source_rgb(0.55, 0.33, 0.17); c.fill_preserve()
    stroke_style(c, 7 * s); c.stroke()
    c.move_to(-70 * s, -8 * s); c.line_to(70 * s, -8 * s); c.stroke()
    c.arc(45 * s, 14 * s, 8 * s, 0, 2 * math.pi); c.set_source_rgb(*GOLD); c.fill()
    c.restore()

def moth(c, x, y, t, s=1.0):
    flap = abs(math.sin(t * 22)) * 0.8 + 0.2
    c.save(); c.translate(x, y)
    for sx in (-1, 1):
        c.save(); c.scale(sx, 1); c.translate(10 * s, -4 * s); c.scale(1.0 * flap, 1)
        c.arc(14 * s, 0, 18 * s, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.62, 0.60, 0.56); c.fill()
    c.save(); c.scale(0.5, 1.2); c.arc(0, 0, 10 * s, 0, 2 * math.pi); c.restore(); c.set_source_rgb(0.3, 0.29, 0.27); c.fill()
    c.restore()

def brain(c, x, y, s=1.0):
    c.set_source_rgb(0.97, 0.56, 0.66)
    for dx, dy, r in [(-38, 0, 38), (0, -18, 42), (38, 0, 38), (-18, 22, 32), (20, 22, 32)]:
        c.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); c.fill()
    stroke_style(c, 6 * s, (0.75, 0.30, 0.42))
    c.move_to(x, y - 50 * s); c.curve_to(x - 15 * s, y - 20 * s, x + 15 * s, y + 5 * s, x, y + 45 * s); c.stroke()
    c.arc(x - 30 * s, y, 14 * s, rad(200), rad(340)); c.stroke()
    c.arc(x + 32 * s, y + 5 * s, 14 * s, rad(200), rad(340)); c.stroke()

def phone(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot)
    rrect(c, -32 * s, -58 * s, 64 * s, 116 * s, 12 * s); c.set_source_rgb(*INK); c.fill()
    rrect(c, -25 * s, -48 * s, 50 * s, 92 * s, 6 * s); c.set_source_rgb(0.45, 0.75, 0.98); c.fill()
    c.restore()

def bike(c, x, y, s=1.0, color=(0.2, 0.45, 0.85)):
    stroke_style(c, 8 * s)
    for dx in (-55, 55):
        c.arc(x + dx * s, y, 30 * s, 0, 2 * math.pi); c.stroke()
    c.move_to(x - 55 * s, y); c.line_to(x - 10 * s, y - 45 * s); c.line_to(x + 40 * s, y - 45 * s); c.line_to(x + 55 * s, y); c.stroke()
    rrect(c, x - 30 * s, y - 70 * s, 70 * s, 30 * s, 12 * s); c.set_source_rgb(*color); c.fill()

def bicycle(c, x, y, s=1.0):
    stroke_style(c, 6 * s, (0.35, 0.35, 0.38))
    for dx in (-50, 50):
        c.arc(x + dx * s, y, 34 * s, 0, 2 * math.pi); c.stroke()
    c.move_to(x - 50 * s, y); c.line_to(x - 5 * s, y - 50 * s); c.line_to(x + 50 * s, y); c.line_to(x + 5 * s, y)
    c.line_to(x - 5 * s, y - 50 * s); c.move_to(x - 15 * s, y - 62 * s); c.line_to(x + 5 * s, y - 62 * s)
    c.move_to(x + 35 * s, y - 60 * s); c.line_to(x + 50 * s, y); c.stroke()

def pizza(c, x, y, s=1.0):
    c.move_to(x - 50 * s, y + 35 * s); c.line_to(x + 50 * s, y + 35 * s); c.line_to(x, y - 55 * s); c.close_path()
    c.set_source_rgb(0.98, 0.78, 0.32); c.fill_preserve(); stroke_style(c, 7 * s, (0.80, 0.45, 0.15)); c.stroke()
    for dx, dy in [(-15, 12), (14, 18), (0, -15)]:
        c.arc(x + dx * s, y + dy * s, 9 * s, 0, 2 * math.pi); c.set_source_rgb(*RED); c.fill()

def bag(c, x, y, s=1.0, glow=0.0):
    if glow > 0:
        g = cairo.RadialGradient(x, y, 10, x, y, 190 * s)
        g.add_color_stop_rgba(0, 1, 0.9, 0.3, 0.75 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.3, 0)
        c.set_source(g); c.arc(x, y, 190 * s, 0, 2 * math.pi); c.fill()
    c.move_to(x - 55 * s, y - 40 * s); c.line_to(x + 55 * s, y - 40 * s); c.line_to(x + 68 * s, y + 60 * s)
    c.line_to(x - 68 * s, y + 60 * s); c.close_path(); c.set_source_rgb(0.93, 0.33, 0.55); c.fill_preserve()
    stroke_style(c, 7 * s); c.stroke()
    c.arc(x, y - 40 * s, 28 * s, math.pi, 2 * math.pi); c.stroke()

def coin(c, x, y, r, alpha=1.0):
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(*GOLD, alpha); c.fill_preserve()
    c.set_line_width(max(2, r * 0.14)); c.set_source_rgba(0.75, 0.52, 0.05, alpha); c.stroke()

def coin_pile(c, x, y, s=1.0, alpha=1.0):
    for row, n in enumerate([5, 4, 3, 2, 1]):
        for i in range(n):
            coin(c, x + (i - (n - 1) / 2) * 38 * s, y - row * 30 * s, 22 * s, alpha)

def cash(c, x, y, s=1.0, rot=0, n=5):
    c.save(); c.translate(x, y); c.rotate(rot)
    for i in range(n):
        rrect(c, -60 * s, -28 * s - i * 9 * s, 120 * s, 56 * s, 6 * s)
        c.set_source_rgb(0.30, 0.68, 0.38); c.fill_preserve(); c.set_line_width(3 * s); c.set_source_rgb(0.12, 0.40, 0.20); c.stroke()
    font(c, 30 * s); e = c.text_extents("₹"); c.move_to(-e.width / 2 - e.x_bearing, 11 * s - (n - 1) * 9 * s)
    c.set_source_rgb(0.95, 1, 0.95); c.show_text("₹")
    c.restore()

def car(c, x, y, s=1.0, t=0):
    c.move_to(x - 120 * s, y); c.line_to(x - 120 * s, y - 40 * s); c.line_to(x - 60 * s, y - 45 * s)
    c.line_to(x - 30 * s, y - 85 * s); c.line_to(x + 50 * s, y - 85 * s); c.line_to(x + 85 * s, y - 45 * s)
    c.line_to(x + 120 * s, y - 38 * s); c.line_to(x + 120 * s, y); c.close_path()
    c.set_source_rgb(*RED); c.fill_preserve(); stroke_style(c, 6 * s); c.stroke()
    rrect(c, x - 20 * s, y - 75 * s, 60 * s, 28 * s, 5 * s); c.set_source_rgb(0.75, 0.9, 1); c.fill()
    for dx in (-70, 70):
        c.arc(x + dx * s, y, 24 * s, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
        c.arc(x + dx * s, y, 10 * s, 0, 2 * math.pi); c.set_source_rgb(0.8, 0.8, 0.8); c.fill()
    for i, (dx, dy) in enumerate([(-100, -110), (110, -100), (10, -130)]):
        sparkle(c, x + dx * s, y + dy * s, (14 + 8 * math.sin(t * 8 + i * 2)) * s)

def sparkle(c, x, y, r):
    c.move_to(x, y - r); c.line_to(x + r * 0.25, y - r * 0.25); c.line_to(x + r, y); c.line_to(x + r * 0.25, y + r * 0.25)
    c.line_to(x, y + r); c.line_to(x - r * 0.25, y + r * 0.25); c.line_to(x - r, y); c.line_to(x - r * 0.25, y - r * 0.25)
    c.close_path(); c.set_source_rgb(*YEL); c.fill()

def heart(c, x, y, r, alpha=1.0):
    c.move_to(x, y + r); c.curve_to(x - 2 * r, y - 0.3 * r, x - 0.8 * r, y - 1.6 * r, x, y - 0.5 * r)
    c.curve_to(x + 0.8 * r, y - 1.6 * r, x + 2 * r, y - 0.3 * r, x, y + r); c.set_source_rgba(0.93, 0.25, 0.40, alpha); c.fill()

def jar(c, x, y, s=1.0, fill=0.0, glow=0.0):
    if glow > 0:
        g = cairo.RadialGradient(x, y, 10, x, y, 230 * s)
        g.add_color_stop_rgba(0, 0.2, 0.85, 0.45, 0.55 * glow); g.add_color_stop_rgba(1, 0.2, 0.85, 0.45, 0)
        c.set_source(g); c.arc(x, y, 230 * s, 0, 2 * math.pi); c.fill()
    if fill > 0:
        h = 200 * s * fill
        rrect(c, x - 82 * s, y + 110 * s - h, 164 * s, h, 18 * s); c.set_source_rgb(0.30, 0.68, 0.38); c.fill()
    rrect(c, x - 90 * s, y - 100 * s, 180 * s, 220 * s, 28 * s); c.set_source_rgba(0.75, 0.92, 1, 0.35); c.fill_preserve()
    stroke_style(c, 7 * s); c.stroke()
    rrect(c, x - 70 * s, y - 128 * s, 140 * s, 30 * s, 8 * s); c.set_source_rgb(0.55, 0.55, 0.58); c.fill_preserve(); stroke_style(c, 6 * s); c.stroke()
    text_c(c, "SAVED", x, y + 20 * s, 40 * s, (1, 1, 1) if fill > 0.45 else INK)

def label(c, s, x, y, size, rgb=INK, bg=None, alpha=1.0):
    font(c, size); e = c.text_extents(s)
    if bg:
        rrect(c, x - e.width / 2 - 18, y - e.height - 14, e.width + 36, e.height + 28, 14); c.set_source_rgba(*bg, alpha); c.fill()
    c.move_to(x - e.width / 2 - e.x_bearing, y); c.set_source_rgba(*rgb, alpha); c.show_text(s)

def arrow_line(c, pts, rgb, lw=12):
    stroke_style(c, lw, rgb); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.stroke()
    (x1, y1), (x2, y2) = pts[-2], pts[-1]; a = math.atan2(y2 - y1, x2 - x1)
    c.move_to(x2 + math.cos(a) * 22, y2 + math.sin(a) * 22)
    c.line_to(x2 + math.cos(a + 2.4) * 30, y2 + math.sin(a + 2.4) * 30)
    c.line_to(x2 + math.cos(a - 2.4) * 30, y2 + math.sin(a - 2.4) * 30); c.close_path(); c.set_source_rgb(*rgb); c.fill()

# ---------------------------------------------------------------- scenes  (t = seconds into scene, d = scene length)
EVENTS = []   # (time, sfx)

def scene1(c, t, d, T0):
    flip = ease(seg(t, 1.3, 1.9))
    shake = math.sin(t * 40) * 0.18 * (seg(t, 1.9, 2.1) - seg(t, 3.6, 3.8))
    mood = "shock" if t > 2.2 else "neutral"
    raise_arm = ease(seg(t, 0.2, 0.8))
    hands, head = stick(c, 470, 1230, 1.55, la=(160, 120), ra=(lerp(60, -20, raise_arm), lerp(80, -60, raise_arm) + shake * 40),
                        mood=mood, look=(0.9, -0.6), tilt=6)
    hx, hy = hands[1]
    wallet(c, hx + 40, hy - 20, math.pi * flip + shake, 1.3)
    if t > 2.2:
        mt = t - 2.2
        moth(c, hx + 40 - mt * 140 + math.sin(mt * 5) * 50, hy + 30 - mt * 170, t, 1.4)
    if t > 4.3:
        p = back(seg(t, 4.3, 4.8))
        c.save(); c.translate(head[0] + 230, head[1] - 140); c.scale(p, p); brain(c, 0, 0, 1.25); c.restore()
        if t > 4.8: label(c, "!", head[0] + 330, head[1] - 210, 110, RED)

def scene2(c, t, d, T0):
    steps = [(110 + i * 215, 1560 - i * 125) for i in range(4)]
    # chart
    gp = ease(seg(t, 0.4, d * 0.9))
    cx0, cy0 = 640, 760
    stroke_style(c, 6, (0.6, 0.6, 0.6)); c.move_to(cx0, cy0 - 330); c.line_to(cx0, cy0); c.line_to(cx0 + 380, cy0); c.stroke()
    if gp > 0.02:
        pts_i = [(cx0 + 20, cy0 - 40), (cx0 + 20 + 330 * gp, cy0 - 40 - 250 * gp)]
        pts_e = [(cx0 + 40, cy0 - 10), (cx0 + 40 + 330 * gp, cy0 - 10 - 245 * gp)]
        arrow_line(c, pts_i, GREEN); arrow_line(c, pts_e, RED)
        label(c, "INCOME", cx0 + 110, cy0 - 230, 40, GREEN, alpha=clamp(gp * 3))
        label(c, "EXPENSES", cx0 + 280, cy0 + 60, 40, RED, alpha=clamp(gp * 3))
    for i, (sx, sy) in enumerate(steps):
        rrect(c, sx - 100, sy, 210, 1920 - sy, 6); c.set_source_rgb(0.86, 0.83, 0.76); c.fill_preserve()
        stroke_style(c, 6, (0.55, 0.52, 0.46)); c.stroke()
    items = [(0.28, lambda x, y, s: phone(c, x, y, s)), (0.36, lambda x, y, s: bike(c, x, y, s)),
             (0.44, lambda x, y, s: pizza(c, x, y, s)), (0.55, lambda x, y, s: bag(c, x, y, s))]
    for i, (when, fn) in enumerate(items):
        ta = when * d
        if i == 0: EVENTS.append((T0 + ta, "pop"))
        else: EVENTS.append((T0 + ta, "pop"))
        if t > ta:
            p = back(seg(t, ta, ta + 0.35)); sx, sy = steps[i]
            c.save(); c.translate(sx, sy + 70); c.scale(p, p); fn(0, 0, 0.9 if i != 1 else 0.75); c.restore()
    # climbing stickman
    prog = clamp(t / (d * 0.62)) * 3
    i0 = min(int(prog), 3); f = prog - i0
    a = steps[i0]; b = steps[min(i0 + 1, 3)]
    x = lerp(a[0], b[0], ease(f)); y = lerp(a[1], b[1], ease(f)) - math.sin(f * math.pi) * 40
    sw = math.sin(t * 9) * 25 if prog < 3 else 0
    stick(c, x, y - 190, 0.95, la=(110 + sw, 100 + sw), ra=(70 - sw, 80 - sw), ll=(90 + sw, 90 + sw), rl=(90 - sw, 90 - sw),
          mood="happy" if t < d * 0.7 else "shock", look=(1, 0))

def scene3(c, t, d, T0):
    fade_far = 1 - 0.65 * ease(seg(t, d * 0.2, d * 0.7))
    c.save(); s_far = lerp(1.0, 0.55, ease(seg(t, d * 0.2, d * 0.7)))
    coin_pile(c, 830, 1010, 0.9 * s_far, fade_far); c.restore()
    label(c, "₹50,000 LATER", 830, 1100, 46, GREEN, alpha=fade_far)
    glow = 0.6 + 0.4 * math.sin(t * 6)
    grab = ease(seg(t, d * 0.42, d * 0.55))
    if grab < 1:
        bag(c, 230, 1230, 1.25, glow); label(c, "₹5,000 NOW", 230, 1370, 50, RED)
    hands, head = stick(c, lerp(470, 420, grab), 1270, 1.45,
                        la=(lerp(160, 200, grab * 0 + ease(seg(t, d * 0.25, d * 0.42))), lerp(120, 190, ease(seg(t, d * 0.25, d * 0.42)))),
                        ra=(lerp(40, -40, grab), lerp(80, -70, grab)),
                        mood="happy", look=(-1, 0) if grab < 1 else (0.4, -0.5), lean=lerp(0, -8, ease(seg(t, d * 0.25, d * 0.42))) * (1 - grab))
    if grab >= 1:
        hx, hy = hands[1]; bag(c, hx + 10, hy + 40, 0.9, glow)
        EVENTS.append((T0 + d * 0.55, "cash"))
    if t > d * 0.72:
        p = ease(seg(t, d * 0.72, d * 0.85))
        stick(c, 830, 1280, 0.8, la=(120, 100), ra=(60, 80), mood="sad", look=(0, 0.6), alpha=p, tilt=-8)
        label(c, "FUTURE YOU", 830, 1470, 44, INK, alpha=p)
        # empty pockets
        for dx in (-40, 40):
            rrect(c, 830 + dx - 14, 1290, 28, 30, 5); c.set_source_rgba(1, 1, 1, p); c.fill()

def scene4(c, t, d, T0):
    bicycle(c, 870, 1540, 1.4)
    pop = back(seg(t, d * 0.18, d * 0.32))
    if pop > 0:
        c.save(); c.translate(540, 780); c.scale(pop, pop)
        rrect(c, -330, -250, 660, 470, 34); c.set_source_rgb(1, 1, 1); c.fill_preserve(); stroke_style(c, 8); c.stroke()
        rrect(c, -330, -250, 660, 70, 34); c.set_source_rgb(0.93, 0.30, 0.55); c.fill()
        label(c, "@friend", -200, -200, 36, (1, 1, 1))
        car(c, 70, 150, 1.25, t)
        stick(c, -190, 70, 0.55, la=(200, 230), ra=(-30, -60), mood="happy", look=(1, 0))
        for i in range(3):
            ht = t - d * 0.35 - i * 0.35
            if ht > 0: heart(c, 250 + i * 25, 130 - ht * 140, 22, clamp(1 - ht / 1.5))
        c.restore()
    sad = ease(seg(t, d * 0.55, d * 0.7))
    hands, head = stick(c, 470, 1420, 1.45, la=(lerp(110, 130, sad), lerp(-20, 30, sad)), ra=(lerp(70, 60, sad), lerp(-160, -120, sad)),
                        mood="sad" if sad > 0.3 else "neutral", look=(0, -1) if sad < 0.5 else (0.9, 0.5),
                        tilt=lerp(-6, 14, sad), lean=lerp(0, 5, sad))
    hx = (hands[0][0] + hands[1][0]) / 2; hy = (hands[0][1] + hands[1][1]) / 2
    phone(c, hx, hy - 10, 1.0, rad(lerp(-10, 15, sad)))

def scene5(c, t, d, T0):
    jar_fill = ease(seg(t, d * 0.42, d * 0.55)) * 0.55
    jar(c, 830, 1180, 1.2, jar_fill, glow=jar_fill * 1.6)
    appear = back(seg(t, 0.2, 0.6)); split = ease(seg(t, d * 0.2, d * 0.32)); fly = ease(seg(t, d * 0.32, d * 0.48))
    thumbs = ease(seg(t, d * 0.55, d * 0.62))
    hands, head = stick(c, 330, 1300, 1.35, la=(150, 110), ra=(lerp(40, -30, thumbs), lerp(80, -90, thumbs)),
                        mood="happy" if t > d * 0.48 else "neutral", look=(1, 0) if thumbs < 0.5 else (0.3, 0))
    if appear > 0 and fly < 1:
        bx, by = 560, 1080
        c.save(); c.translate(bx, by); c.scale(appear, appear); c.translate(-bx, -by)
        cash(c, bx - 70 * split, by, 1.1, 0, 4)
        fx = lerp(bx + 70 * split, 830, fly); fy = lerp(by, 1160, fly) - math.sin(fly * math.pi) * 260
        cash(c, fx, fy, 1.1 * (1 - 0.3 * fly), fly * 3.0, 4)
        c.restore()
    elif fly >= 1:
        cash(c, hands[0][0], hands[0][1] + 20, 0.8, -0.3, 3)
    if thumbs > 0:
        hx, hy = hands[1]; c.save(); c.translate(hx, hy); c.scale(thumbs, thumbs)
        rrect(c, -22, -10, 44, 40, 10); c.set_source_rgb(1, 1, 1); c.fill_preserve(); stroke_style(c, 6); c.stroke()
        rrect(c, -10, -42, 18, 38, 8); c.set_source_rgb(1, 1, 1); c.fill_preserve(); stroke_style(c, 6); c.stroke()
        c.restore()
    if t > d * 0.68:
        p = back(seg(t, d * 0.68, d * 0.78)) * (1 + 0.04 * math.sin(t * 7))
        c.save(); c.translate(540, 1770); c.scale(p, p)
        rrect(c, -330, -62, 660, 112, 56); c.set_source_rgb(*RED); c.fill()
        text_c(c, "FOLLOW FOR PART 2  →", 0, 18, 52, (1, 1, 1)); c.restore()

SCENES = [scene1, scene2, scene3, scene4, scene5]

# ---------------------------------------------------------------- frame composer
def headline(c, s, p):
    font(c, 66); words = s.split(); lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.text_extents(trial).width > 900 and cur: lines.append(cur); cur = w
        else: cur = trial
    lines.append(cur)
    y0 = 250
    c.save(); c.translate(540, y0); sc = back(p); c.scale(sc, sc); c.translate(-540, -y0)
    for i, ln in enumerate(lines):
        y = y0 + i * 92; e = c.text_extents(ln)
        rrect(c, 540 - e.width / 2 - 26, y - 66, e.width + 52, 88, 16); c.set_source_rgb(*YEL); c.fill()
        c.move_to(540 - e.width / 2 - e.x_bearing, y); c.set_source_rgb(*INK); c.show_text(ln)
    c.restore()

def captions(c, T):
    for ch in cap_chunks:
        if ch[0][1] - 0.05 <= T < ch[-1][2] + 0.05:
            font(c, 70); sp = c.text_extents(" ").x_advance
            widths = [c.text_extents(w).x_advance for w, _, _ in ch]
            total = sum(widths) + sp * (len(ch) - 1)
            x = 540 - total / 2; y = 1640
            for (w, a, b), wd in zip(ch, widths):
                active = a <= T < b + 0.08
                if active:
                    rrect(c, x - 10, y - 62, wd + 20, 84, 14); c.set_source_rgb(*GREEN); c.fill()
                c.move_to(x, y); c.text_path(w)
                c.set_source_rgb(1, 1, 1) if active else c.set_source_rgb(*INK); c.fill()
                x += wd + sp
            break

def render():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    c.set_antialias(cairo.ANTIALIAS_BEST)
    n = int(TOTAL * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                           "-pix_fmt", "yuv420p", f"{OUT}/video_only.mp4"], stdin=subprocess.PIPE)
    snaps = {int(sc["start"] * FPS + (sc["end"] - sc["start"]) * FPS * 0.62) for sc in scenes}
    for f in range(n):
        T = f / FPS
        idx = max(i for i, sc in enumerate(scenes) if T >= sc["start"] or i == 0)
        idx = min(idx, len(scenes) - 1)
        sc = scenes[idx]; t = T - sc["start"]; d = sc["end"] - sc["start"]
        if idx == len(scenes) - 1: d = max(d, TOTAL - sc["start"])
        c.set_source_rgb(*BG); c.paint()
        # subtle dot grid
        c.set_source_rgba(0, 0, 0, 0.035)
        for gx in range(40, W, 80):
            for gy in range(40, H, 80):
                c.rectangle(gx, gy, 4, 4)
        c.fill()
        # scene with pop-in transition
        pin = back(seg(t, 0, 0.3)) if idx > 0 else 1
        c.save(); c.translate(540, 1150); c.scale(lerp(0.92, 1, pin), lerp(0.92, 1, pin)); c.translate(-540, -1150)
        c.push_group(); SCENES[idx](c, t, d, sc["start"]); c.pop_group_to_source(); c.paint_with_alpha(clamp(t / 0.15) if idx else 1)
        c.restore()
        headline(c, sc["head"], seg(t, 0, 0.35))
        captions(c, T)
        # progress bar
        c.rectangle(0, 0, W * T / TOTAL, 12); c.set_source_rgb(*GREEN); c.fill()
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
        if f in snaps: surf.write_to_png(f"{OUT}/frame_{idx + 1}.png")
    ff.stdin.close(); ff.wait()

# ---------------------------------------------------------------- audio: sfx + music
def env(n, a, r):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    e *= np.exp(-np.arange(n) / (r * SR)); return e

def sfx(kind):
    if kind == "whoosh":
        n = int(0.4 * SR); noise = np.random.randn(n)
        k_ = np.exp(-np.linspace(-3, 3, n) ** 2); cut = np.convolve(noise, np.ones(12) / 12, "same")
        return 0.35 * cut * k_
    if kind == "pop":
        n = int(0.12 * SR); tt = np.arange(n) / SR; f = np.linspace(500, 1300, n)
        return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.03)
    if kind in ("ding", "cash"):
        n = int(0.9 * SR); tt = np.arange(n) / SR
        out = 0.25 * (np.sin(2 * np.pi * 1318 * tt) + 0.5 * np.sin(2 * np.pi * 2637 * tt)) * env(n, 0.002, 0.25)
        if kind == "cash":
            out[int(0.09 * SR):] += 0.25 * (np.sin(2 * np.pi * 1760 * tt[:n - int(0.09 * SR)])) * env(n - int(0.09 * SR), 0.002, 0.2)
            out[:int(0.05 * SR)] += 0.3 * np.random.randn(int(0.05 * SR)) * np.linspace(1, 0, int(0.05 * SR))
        return out
    return np.zeros(1)

def music(n):
    bpm = 100; beat = 60 / bpm; tt = np.arange(n) / SR; out = np.zeros(n)
    chords = [[261.6, 329.6, 392.0], [196.0, 246.9, 293.7], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6]]
    bar = beat * 4
    for b in range(int(n / SR / bar) + 1):
        ch = chords[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR))
        if s0 >= n: break
        seg_t = tt[s0:s1] - tt[s0]
        pad = sum(np.sin(2 * np.pi * f / 2 * seg_t) for f in ch) * 0.05 * np.minimum(1, seg_t / 0.4)
        out[s0:s1] += pad
        for i in range(8):                       # plucked arpeggio
            p0 = s0 + int(i * beat / 2 * SR); m = min(n - p0, int(0.4 * SR))
            if m <= 0: continue
            f = ch[[0, 1, 2, 1][i % 4]] * 2; pt = np.arange(m) / SR
            out[p0:p0 + m] += 0.06 * np.sin(2 * np.pi * f * pt) * np.exp(-pt / 0.12)
        k0 = s0; km = min(n - k0, int(0.15 * SR))           # soft kick on 1
        kt = np.arange(km) / SR; out[k0:k0 + km] += 0.18 * np.sin(2 * np.pi * (60 + 80 * np.exp(-kt / 0.03)) * kt) * np.exp(-kt / 0.08)
    return out

def mix():
    n = len(voice); track = voice.astype(np.float64) * 1.0
    m = music(n); track += m * 0.55
    ev = [(sc["start"], "whoosh") for sc in scenes[1:]] + [(scenes[0]["start"] + 2.2, "cash")]
    s5 = scenes[4]; ev.append((s5["start"] + (s5["end"] - s5["start"]) * 0.56, "ding"))
    seen = set()
    for tm, kd in EVENTS + ev:
        key = (round(tm, 1), kd)
        if key in seen: continue
        seen.add(key); x = sfx(kd); i0 = int(tm * SR); i1 = min(n, i0 + len(x))
        track[i0:i1] += x[:i1 - i0] * 0.8
    fade = int(0.6 * SR); track[-fade:] *= np.linspace(1, 0, fade)
    track /= max(1.0, np.abs(track).max() / 0.95)
    sf.write(f"{OUT}/audio.wav", track.astype(np.float32), SR)

render()
mix()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/video_only.mp4", "-i", f"{OUT}/audio.wav",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                f"{OUT}/why_youre_always_broke_short1.mp4"], check=True)
print("done", TOTAL)

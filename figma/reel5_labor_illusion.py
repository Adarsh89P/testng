"""Reel 5: 'UX designer ho? Labor Illusion kya hai?' - explained with Zomato, in the reference reel's minimal style.

Minimal dotted objects, mono labels, story opener, App A | App B split with dotted divider, dot-formed titles,
whole-frame dot break/form transitions, no captions (as in the reference).
"""
import sys, math
from engine import *
from fx import Stage, dot_text, flash, ring

W, H = 1080, 1920
ANCHOR = (W / 2, H / 2)
FULL = [(0, W / 2, H / 2, 1.0)]
stage = Stage(W, H, ANCHOR)
CPS = 22
GREEN = (0.35, 0.85, 0.55)


def K(*keys): return [(t, p[0], p[1], zz) for t, p, zz in keys]


def mono_label(c, s, y, col=DOT, size=30, chars=None):
    c.font(MONO, size); s2 = s if chars is None else s[:chars]
    c.text(W / 2 - c.text_w(s) / 2, y, s2, col)


def phone(c, cx, cy, w, h, stripes=True, a=1.0):
    x, y = cx - w / 2, cy - h / 2
    c.drrect(x, y, w, h, w * 0.17, spacing=5.5, r=1.6, a=a)
    c.drrect(x + 8, y + 8, w - 16, h - 16, w * 0.14, spacing=6.5, r=1.1, col=DIM, a=a)
    c.drrect(cx - w * 0.15, y + 18, w * 0.3, 14, 7, spacing=4.5, r=1.3, a=a)
    if stripes:
        for i in range(5):
            sx = x + w * (0.25 + 0.125 * i)
            c.dline(sx, y + 60, sx, y + h - 50, spacing=7, r=1.1, col=DIM, a=a)
        c.dline(cx - w * 0.15, y + h - 30, cx + w * 0.15, y + h - 30, spacing=5, r=1.2, a=a)
    return x, y


def spinner(c, cx, cy, t, r=22):
    for i in range(8):
        a = (t * 6 + i) % 8 / 8
        ang = i / 8 * 6.283
        c._dot(cx + math.cos(ang) * r, cy + math.sin(ang) * r, 3.2, DOT, 0.15 + 0.85 * a)


def mini_map(c, cx, cy, w, h, k):
    x0, y0 = cx - w / 2, cy - h / 2
    for gx in range(int(x0) + 14, int(x0 + w), 34): c.dline(gx, y0, gx, y0 + h, spacing=8, r=1.0, col=(0.28, 0.28, 0.3))
    for gy in range(int(y0) + 14, int(y0 + h), 34): c.dline(x0, gy, x0 + w, gy, spacing=8, r=1.0, col=(0.28, 0.28, 0.3))
    pts = [(x0 + 20, y0 + 20), (x0 + 20, y0 + h * 0.45), (x0 + w * 0.55, y0 + h * 0.45), (x0 + w * 0.55, y0 + h - 30), (x0 + w - 20, y0 + h - 30)]
    c.dots_path(pts, spacing=6, r=1.8)
    segs = list(zip(pts, pts[1:])); L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; d = k * sum(L)
    rx, ry = pts[-1]
    for (a, b), l in zip(segs, L):
        if d <= l: rx, ry = a[0] + (b[0] - a[0]) * d / l, a[1] + (b[1] - a[1]) * d / l; break
        d -= l
    c.glow(rx, ry, 30, 0.9); c._dot(rx, ry, 5, (1, 1, 1), 1)
    c._dot(pts[-1][0], pts[-1][1], 6, GREEN, 1)


def steps(c, x, y, t, t0, gap=58, names=("Order placed", "Preparing", "Rider assigned", "On the way"), size=22):
    lit = int(max(0, (t - t0) / 0.9)) + 1
    for i, n in enumerate(names):
        on = i < lit
        yy = y + i * gap
        if i < len(names) - 1:
            c.line(x, yy + 8, x, yy + gap - 8, GREEN if i < lit - 1 else (0.3, 0.3, 0.33), 2)
        c.c.set_source_rgba(*(GREEN if on else (0.3, 0.3, 0.33)), 1); c.c.arc(x, yy, 7, 0, 6.3); c.c.fill()
        if on and i == lit - 1: c.glow(x, yy, 26, 0.6)
        c.font(SANS, size, on); c.text(x + 22, yy + 8, n, DOT if on else DIM)
    return lit


def person(c, cx, cy, name, s=0.8):
    c.person(cx, cy, s); c.pill(cx, cy + 92 * s, name, size=22)


def split_labels(c, left, right, active):
    for lab, x, on in [(left, W * 0.27, active == 0), (right, W * 0.73, active == 1)]:
        c.font(SANS, 54, True); c.text(x - c.text_w(lab) / 2, 330, lab, DOT if on or active is None else DIM)
    for yy in range(400, 1500, 14): c._dot(W / 2, yy, 1.3, DIM, 0.8)


# ------------------------------------------------------------------ 1. hook
def s1(cv, t, d, st):
    def world(c):
        swarm(c, t, 60, 1150, 960, 450, n=140, a=0.45)
        mono_label(c, "UX designer ho?", 640, DOT, 40, chars=int(t * 14))
        if t > 1.4: dot_text(c, "LABOR ILLUSION", 104, W / 2, 860, ease(1 - (t - 1.4) / 0.9))
        if t > 2.6: mono_label(c, "kya hai?", 1010, DIM, 40, chars=int((t - 2.6) * 14))
    stage.compose(cv, t, d, world, FULL, form=0.0, seed=1)


# ------------------------------------------------------------------ 2. story
def s2(cv, t, d, st):
    def world(c):
        mono_label(c, "Friday · 9:47 PM", 300, DIM, 30, chars=int(t * 18))
        phone(c, W / 2, 820, 230, 430)
        c.line(W / 2, 1040, W / 2, 1210)
        person(c, W / 2, 1270, "Rohan")
        if t > 2.2: c.pill(W / 2 + 230, 700, "order: biryani", size=22, fam=MONO)
        if t > 3.2: c.pill(W / 2 + 230, 770, "eta: 30 min", size=22, fam=MONO)
        if t > 4.2: white_pill(c, W / 2, 1480, "live app: zomato", 24)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.25), (1.0, ANCHOR, 1.25), (2.4, ANCHOR, 1.0)), seed=2)


# ------------------------------------------------------------------ 3. split A | B
def s3(cv, t, d, st):
    def world(c):
        split_labels(c, "App A", "App B", None if t < 1.0 else (0 if t < 3.8 else 1))
        lx, rx, cy = W * 0.27, W * 0.73, 820
        x, y = phone(c, lx, cy, 200, 380, stripes=False)
        c.font(SANS, 20, True); c.text(lx - c.text_w("Order placed") / 2, cy - 30, "Order placed", DOT)
        spinner(c, lx, cy + 40, t)
        x, y = phone(c, rx, cy, 200, 380, stripes=False)
        mini_map(c, rx, cy - 30, 160, 230, min(1, t / (d + 2)))
        c.font(SANS, 18, True); c.text(rx - 62, cy + 140, "2.1 km away", DOT)
        for xx in (lx, rx): c.pill(xx, cy + 250, "wait: 30 min", size=22, fam=MONO)
        if t > 5.2: white_pill(c, W / 2, 1380, "same wait. alag feeling?", 24)
    stage.compose(cv, t, d, world, FULL, seed=3)


# ------------------------------------------------------------------ 4. App A anxiety
OPENS = [1.0, 1.8, 2.4, 3.0, 3.5, 3.9, 4.3]
def s4(cv, t, d, st):
    n = sum(1 for o in OPENS if t >= o)
    def world(c):
        split_labels(c, "App A", "App B", 0)
        lx, cy = W * 0.27, 820
        phone(c, lx, cy, 200, 380, stripes=False)
        c.font(SANS, 20, True); c.text(lx - c.text_w("Order placed") / 2, cy - 30, "Order placed", DOT)
        spinner(c, lx, cy + 40, t)
        for o in OPENS: ring(c, lx, cy, t, o)
        c.line(lx, cy + 200, lx, cy + 330)
        person(c, lx, cy + 390, "Rohan")
        if n: c.glow(lx, cy + 360, 60 + 6 * n, 0.25 + 0.05 * n)
        for i in range(min(n, 5)):
            ang = -2.4 + i * 0.55
            c.pill(lx + math.cos(ang) * 150, cy + 380 + math.sin(ang) * 120, "?", size=26, fam=MONO, col=BAD)
        c.pill(lx, cy - 260, f"app khola: {n} baar", size=22, fam=MONO, col=BAD if n > 3 else DOT)
        if t > 4.8: white_pill(c, lx, cy + 560, "30 min = 1 ghanta jaisa", 22)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (W * 0.27 + 90, 1020), 1.45), (d - 0.6, (W * 0.27 + 90, 1020), 1.45)),
                  punch=0.04 * sum(max(0, 1 - abs(t - o) / 0.1) for o in OPENS), seed=4)


# ------------------------------------------------------------------ 5. App B progress
def s5(cv, t, d, st):
    def world(c):
        split_labels(c, "App A", "App B", 1)
        rx, cy = W * 0.73, 820
        phone(c, rx, cy, 200, 380, stripes=False)
        mini_map(c, rx, cy - 70, 160, 150, min(1, 0.3 + t / 10))
        steps(c, rx - 72, cy + 40, t, 0.6, gap=34, size=15)
        c.line(rx, cy + 200, rx, cy + 330)
        person(c, rx, cy + 390, "Rohan")
        if t > 2.0: c.pill(rx - 210, cy + 380, "calm", size=24, fam=MONO, col=GREEN)
        if t > 4.6: white_pill(c, rx, cy + 560, "wait chhota lagta hai", 22)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (W * 0.73 - 90, 980), 1.5), (d - 0.6, (W * 0.73 - 90, 980), 1.5)), seed=5)


# ------------------------------------------------------------------ 6. the law
def s6(cv, t, d, st):
    def world(c):
        swarm(c, t, 60, 1250, 960, 420, n=120, a=0.35)
        c.pill(W / 2, 650, "UX LAW", size=24, fam=MONO, col=(0.02, 0.02, 0.03), bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "LABOR ILLUSION", 104, W / 2, 790, ease(1 - t / 0.9))
        l1, l2 = "kaam hota dikhe =", "wait chhota + value zyada"
        n = int(max(0, t - 1.0) * 20)
        mono_label(c, l1, 930, DOT, 34, chars=n); mono_label(c, l2, 985, GREEN, 34, chars=max(0, n - len(l1)))
        if t > 3.6: c.pill(W / 2, 1110, "Buell & Norton · Harvard Business School · 2011", size=20, fam=MONO)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.15), (d, ANCHOR, 1.0)), seed=6)


# ------------------------------------------------------------------ 7. zomato example
L7 = ["order received", "food is being prepared", "rider is on the way", "arriving in 9 min"]
def s7(cv, t, d, st):
    def world(c):
        mono_label(c, "live app · zomato", 300, DIM, 30)
        cx, cy = W / 2, 900
        phone(c, cx, cy, 300, 560, stripes=False)
        mini_map(c, cx, cy - 110, 240, 230, min(1, 0.4 + t / 12))
        lit = steps(c, cx - 110, cy + 60, t, 0.5, gap=46, names=tuple(L7), size=19)
        for i in range(min(lit, 4)):
            c.pill(cx + 300, cy + 60 + i * 46, ["update", "update", "live", "eta"][i], size=18, fam=MONO, col=GREEN)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.0), (1.0, (W / 2, 980), 1.35), (d, (W / 2, 980), 1.35)), seed=7)


# ------------------------------------------------------------------ 8. designer takeaway
def s8(cv, t, d, st):
    def world(c):
        split_labels(c, "DON'T", "DO", None if t < 1.2 else (0 if t < 2.6 else 1))
        lx, rx, cy = W * 0.27, W * 0.73, 820
        phone(c, lx, cy, 200, 380, stripes=False); spinner(c, lx, cy, t)
        c.pill(lx, cy + 250, "khaali spinner", size=22, fam=MONO, col=BAD)
        phone(c, rx, cy, 200, 380, stripes=False); steps(c, rx - 72, cy - 60, t, 0.8, gap=40, size=15)
        c.pill(rx, cy + 250, "progress dikhao", size=22, fam=MONO, col=GREEN)
        if t > 4.0: white_pill(c, W / 2, 1380, "follow · next UX law", 26)
    stage.compose(cv, t, d, world, FULL, brk=0.0, seed=8)


SCENES = [
    Scene("यू एक्स डिज़ाइनर हो? तो बताओ, लेबर इल्यूज़न क्या है?", "", s1, min_dur=4.6, whoosh=True),
    Scene("चलो समझते हैं, हमारे लाइव ऐप ज़ोमैटो से। फ्राइडे रात, नौ बजकर सैंतालीस मिनट। रोहन ने बिरयानी ऑर्डर की। डिलीवरी, तीस मिनट।",
          "", s2, min_dur=6.0, whoosh=True),
    Scene("अब दो ऐप्स सोचो। दोनों में इंतज़ार तीस मिनट। ऐप ए में सिर्फ लिखा है, ऑर्डर प्लेस्ड। ऐप बी में राइडर मैप पर चलता दिखता है।",
          "", s3, min_dur=7.0, whoosh=True),
    Scene("ऐप ए में रोहन बार बार ऐप खोलता है। कुछ बदलता ही नहीं। तीस मिनट, एक घंटे जैसे लगते हैं।",
          "", s4, min_dur=6.0, clicks=OPENS),
    Scene("ऐप बी में वही तीस मिनट, पर हर स्टेप दिखता है। खाना बन रहा है, राइडर निकल गया। रोहन शांत है।",
          "", s5, min_dur=6.0, whoosh=True),
    Scene("यही है लेबर इल्यूज़न। हार्वर्ड बिज़नेस स्कूल की रिसर्च कहती है, जब यूज़र को काम होता दिखता है, तो इंतज़ार कम खलता है, और वो सर्विस को ज़्यादा वैल्यू देता है।",
          "", s6, min_dur=8.0, whoosh=True),
    Scene("इसीलिए ज़ोमैटो में हर स्टेप का अपडेट आता है, और राइडर लाइव दिखता है।",
          "", s7, min_dur=5.5, whoosh=True),
    Scene("तो अगली बार डिज़ाइन में खाली स्पिनर मत दिखाओ, प्रोग्रेस दिखाओ। अगला यूएक्स लॉ जानने के लिए फॉलो करो।",
          "", s8, min_dur=6.0, whoosh=True),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=None, voice="bf_emma", lang="hi"), 1), "s")

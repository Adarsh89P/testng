"""Day 35/45 · Variable Reward, explained with Instagram's pull-to-refresh.

When a reward is unpredictable (sometimes yes, sometimes no) we keep checking: pull the feed down, the spinner turns,
maybe a new post, maybe not, and you pull again, like a slot-machine lever. Skinner's pigeons pecked steadily for
grain that came every time, but never stopped when it came only sometimes. The fun is in the waiting, not the reward.
Instagram itself added "You're all caught up" as a stopping point; delight with surprises, don't trap. Day 02 pattern;
bold pattern-interrupt hook. Voice: Rakhi's Day 35 ElevenLabs Tisha K file at assets/voice/day35/full.mp3
(content-verified); script in docs/scripts/day35.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 35, "Progressive Disclosure"
W, H = 1080, 1920
IGP = (0.88, 0.25, 0.55)                          # Instagram pink
IGO = (1.0, 0.60, 0.20)
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


def spinner(c, x, y, t, a=1.0, r=22):
    for i in range(10):
        ang = t * 7 + i * 0.63
        c._dot(x + math.cos(ang) * r, y + math.sin(ang) * r, 3 + i * 0.4, DOT, a * (0.2 + i * 0.08))


def post(c, y, i, a=1.0, new=False):
    c.c.new_path(); c.c.set_source_rgba(*COLS[i % 6], a); c.c.arc(X0 + 46, y + 26, 18, 0, 6.2832); c.c.fill()
    c.font(SANS, 18, True); c.text(X0 + 74, y + 32, ["priya", "rahul", "ananya", "kabir", "meera"][i % 5], DOT, a)
    c.fill_rrect(X0 + 16, y + 56, PW - 32, 250, 6, tuple(0.15 + cc * 0.4 for cc in COLS[(i + 2) % 6]), a)
    if new: c.pill(X0 + PW - 90, y + 30, "NEW", size=18, fam=SANS, col=DARK, bg=IGO, bold=True, a=a)


def pigeon(c, x, y, s=1.0, a=1.0, peck=0.0):
    c.c.new_path(); c.c.set_source_rgba(0.62, 0.64, 0.70, a); c.c.save(); c.c.translate(x, y); c.c.scale(1.3, 1.0)
    c.c.arc(0, 0, 40 * s, 0, 6.2832); c.c.restore(); c.c.fill()
    hx, hy = x + 46 * s, y - 30 * s + peck * 34 * s
    c.c.new_path(); c.c.set_source_rgba(0.55, 0.58, 0.66, a); c.c.arc(hx, hy, 20 * s, 0, 6.2832); c.c.fill()
    c.c.new_path(); c.c.set_source_rgba(1.0, 0.70, 0.20, a); c.c.move_to(hx + 18 * s, hy - 4 * s); c.c.line_to(hx + 34 * s, hy + 2 * s)
    c.c.line_to(hx + 18 * s, hy + 6 * s); c.c.close_path(); c.c.fill()
    c.c.new_path(); c.c.set_source_rgba(0, 0, 0, a); c.c.arc(hx + 6 * s, hy - 4 * s, 3.5 * s, 0, 6.2832); c.c.fill(); c.c.new_path()


# ------------------------------------------------------------------ scenes
PULLS = [(0.6, False), (2.4, True), (4.2, False)]
def s1(cv, t, d, st):                                     # pull feed down → spinner → maybe new, maybe not → pull again
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 30, True); c.text(X0 + 24, Y0 + 94, "Instagram", DOT)
        cur = None
        for at, new in PULLS:
            if t >= at: cur = (at, new)
        drop = 0
        if cur:
            lt = t - cur[0]
            drop = 120 * (math.sin(min(1, lt / 0.5) * math.pi / 2) if lt < 0.5 else max(0, 1 - (lt - 0.9) / 0.3) if lt > 0.9 else 1)
            if 0.4 < lt < 1.2: spinner(c, PX, Y0 + 150, t)
            if lt > 1.2:
                if cur[1]: c.pill(PX, Y0 + 150, "nayi post!", size=24, fam=SANS, col=DARK, bg=IGO, bold=True)
                else: c.pill(PX, Y0 + 150, "kuch nahi…", size=24, fam=SANS, col=DOT)
        for j in range(2):
            post(c, Y0 + 130 + drop + j * 330, j + (1 if (cur and cur[1] and t - cur[0] > 1.2) else 0),
                 new=(j == 0 and cur is not None and cur[1] and t - cur[0] > 1.2))
        if cur and t - cur[0] < 0.6:
            k = (t - cur[0]) / 0.6
            c._dot(PX + 60, Y0 + 260 + 140 * k, 14, (1, 1, 1), 1)
            c.dots_path([(PX + 60, Y0 + 250), (PX + 60, Y0 + 250 + 140 * k)], spacing=8, r=2.4, col=(1, 1, 1), a=0.6)
        if t > 1.0: c.pill(PX + 300, Y0 + 240, "shaayad haan…", size=22, fam=MONO, col=DOT)
        if t > 1.8: c.pill(PX + 300, Y0 + 320, "shaayad nahi…", size=22, fam=MONO, col=DOT)
        if t > 5.4: white_pill(c, W / 2, 1660, "aur aapne, phir se kheench diya", 34)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.4, (PX + 70, Y0 + 330), 1.15), (d - 0.4, (PX + 60, Y0 + 380), 1.12)), seed=2)
    hud(cv)


def s2(cv, t, d, st):                                     # Skinner's pigeons: every-time grain → calm; sometimes → never stop
    def world(c):
        c.pill(W / 2, 560, "ek mashhoor experiment", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        for j, (lab, rate, at) in enumerate([("har baar daana", 1.4, 0.4), ("kabhi-kabhi daana", 5.0, 2.4)]):
            cx = W * (0.27 + 0.46 * j)
            k = ease(min(1, max(0, (t - at) / 0.5)))
            c.fill_rrect(cx - 210, 680, 420, 560, 26, CARD, k)
            c.font(SANS, 28, True); c.text(cx - c.text_w(lab) / 2, 740, lab, DOT, k)
            if k > 0:
                peck = max(0, math.sin((t - at) * rate * 6.2832)) if t > at else 0
                pigeon(c, cx - 30, 960, 1.6, k, peck)
                n = int(max(0, t - at) * rate)
                c.font(MONO, 30, True); c.text(cx - 120, 1170, f"pecks: {n}", GOLD if j else DIM, k)
            if j == 0 and t > 1.8: c.pill(cx, 1300, "aaraam se khaate rahe", size=22, fam=SANS, col=DOT)
            if j == 1 and t > 3.6: c.pill(cx, 1300, "ruke hi nahi!", size=26, fam=SANS, col=DARK, bg=GOLD, bold=True)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 960), 1.15), (2.0, (W * 0.27, 960), 1.15), (2.8, (W / 2, 980), 1.0),
                                     (d - 0.4, (W / 2, 1000), 1.0)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # law named: unpredictable reward → we check again and again
    SYMS = [GOLD, IGP, GREEN, BLUE, IGO]
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "VARIABLE", 124, W / 2, 630, ease(1 - t / 0.8), col=IGP)
        dot_text(c, "REWARD", 124, W / 2, 770, ease(1 - (t - 0.2) / 0.8), col=IGP)
        c.fill_rrect(W / 2 - 330, 900, 660, 260, 30, (0.20, 0.10, 0.16))
        for i in range(3):
            stop = 1.6 + i * 0.5
            x = W / 2 - 200 + i * 200
            c.fill_rrect(x - 80, 930, 160, 200, 18, (0.08, 0.08, 0.09))
            idx = int(t * 14 + i * 3) % 5 if t < stop else [0, 0, 2][i]
            c.c.new_path(); c.c.set_source_rgba(*SYMS[idx], 1); c.c.arc(x, 1030, 50, 0, 6.2832); c.c.fill()
        c.dots_path([(W / 2 + 360, 920), (W / 2 + 360, 1100)], spacing=8, r=3, col=DOT)
        c._dot(W / 2 + 360, 910 + (60 if t < 1.0 else 0), 20, RED, 1)
        if t > 3.0: c.pill(W / 2, 1250, "kabhi mile, kabhi nahi", size=30, fam=SANS, col=DARK, bg=IGO, bold=True)
        if t > 3.8: c.pill(W / 2, 1350, "→ baar-baar check", size=28, fam=MONO, col=DOT)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1060), 1.0), (d - 0.4, (W / 2, 1100), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


def s4(cv, t, d, st):                                     # the fun is in the waiting: next reel, next like, next message
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("asli mazaa: intezaar") / 2, 560, "asli mazaa: intezaar", IGO)
        k = ease(min(1, max(0, (t - 0.4) / 1.0)))
        for j, (lab, h, col) in enumerate([("inaam", 140, GREY), ("intezaar", 320, IGP)]):
            x = W / 2 - 220 + j * 280
            c.fill_rrect(x, 1080 - h * k, 140, h * k, 14, col)
            c.font(SANS, 28, True); c.text(x + 70 - c.text_w(lab) / 2, 1130, lab, DOT)
        for i, lab in enumerate(["agli reel", "agla like", "agla message"]):
            at = 1.6 + i * 0.5
            if t > at:
                kk = ease(min(1, (t - at) / 0.4))
                c.pill(W / 2 - 300 + i * 300, 1280 - 30 * (1 - kk), lab + "…", size=28, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True, a=kk)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 1000), 1.02)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # Instagram's own stop: "You're all caught up"
    def world(c):
        phone(c, PX, PY, PW, PH)
        c.font(SANS, 30, True); c.text(X0 + 24, Y0 + 94, "Instagram", DOT)
        sc = min(1, t / 1.4) * 220
        post(c, Y0 + 130 - sc, 2)
        k = ease(min(1, max(0, (t - 1.0) / 0.6)))
        cy = Y0 + 560 - 60 * k
        c.c.new_path(); c.c.set_source_rgba(*IGP, k); c.c.arc(PX, cy, 54, 0, 6.2832); c.c.set_line_width(5); c.c.stroke()
        c.dots_path([(PX - 24, cy), (PX - 6, cy + 20), (PX + 28, cy - 18)], spacing=5, r=3.4, col=IGP, a=k)
        c.font(SANS, 28, True); c.text(PX - c.text_w("You're all caught up") / 2, cy + 100, "You're all caught up", DOT, k)
        c.font(SANS, 18, True); c.text(PX - c.text_w("You've seen all new posts") / 2, cy + 132, "You've seen all new posts", DIM, k)
        if t > 2.4: white_pill(c, W / 2, 1660, "matlab: bas, ab ruk sakte ho", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (1.0, (PX, Y0 + 500), 1.25), (d - 0.4, (PX, Y0 + 520), 1.2)), seed=6)
    hud(cv); flash(cv, t, 1.0, 0.06)


def s6(cv, t, d, st):                                     # tip: delight with surprises, don't trap; every feed needs a stopping point
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("designers ke liye") / 2, 560, "designers ke liye", IGO)
        rows = [("surprise se khushi", GREEN, "✓", 0.4), ("user ko phansaana", RED, "✗", 1.4), ("rukne ki jagah", GREEN, "✓", 2.4)]
        for j, (lab, col, mark, at) in enumerate(rows):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            y = 660 + j * 170
            c.fill_rrect(W / 2 - 400, y, 800, 140, 22, CARD, k)
            c.c.new_path(); c.c.set_source_rgba(*col, k); c.c.arc(W / 2 - 330, y + 70, 30, 0, 6.2832); c.c.fill()
            c.font(SANS, 30, True); c.text(W / 2 - 344, y + 82, mark, DARK, k)
            c.font(SANS, 34, True); c.text(W / 2 - 270, y + 84, lab, DOT, k)
        if t > 3.6: white_pill(c, W / 2, 1240, "har achhe feed mein, rukne ki jagah", 32)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 960), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 35 script (docs/scripts/day35.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("आपके हाथ में जो फ़ोन है, वो असल में एक स्लॉट मशीन है। और आप उसे, दिन में सौ बार चलाते हो। डे थर्टी फ़ाइव, चलो दिखाती हूँ कैसे।", "", D.s0,
          min_dur=5.0, sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("इंस्टाग्राम खोला। फ़ीड को नीचे खींचा, छोड़ा। एक छोटा सा स्पिनर घूमा। नई पोस्ट आएगी? शायद हाँ, शायद नहीं। और आपने, फिर से खींच दिया।", "", s1,
          min_dur=6.4, whoosh=True, sfx=[(a, "pop_lo") for a, _ in PULLS] + [(a + 1.2, "chime" if n else "pop") for a, n in PULLS]
          + [(5.4, "ding")]),
    Scene("एक मशहूर एक्सपेरिमेंट में, कबूतरों को चोंच मारने पर दाना मिलता था। जब दाना हर बार मिला, वो आराम से खाते रहे। पर जब दाना कभी-कभी मिला, तो वो रुके ही नहीं।",
          "", s2, min_dur=6.8, whoosh=True, sfx=[(0.4, "pop"), (2.4, "pop")] + [(2.6 + i * 0.2, "tick") for i in range(10)] + [(3.6, "ding")]),
    Scene("इसे कहते हैं, वेरिएबल रिवॉर्ड। जब इनाम पक्का न हो, कभी मिले, कभी नहीं, तो हम बार-बार चेक करते हैं।", "", s3, min_dur=5.6,
          whoosh=True, sfx=[(0.2, "drop"), (0.6, "riser"), (1.6, "pop_hi"), (2.1, "pop_hi"), (2.6, "pop_hi"), (3.0, "chime")]),
    Scene("असली मज़ा, इनाम में नहीं, उसके इंतज़ार में है। अगली रील, अगला लाइक, अगला मैसेज।", "", s4, min_dur=4.8, whoosh=True,
          sfx=[(0.4, "riser"), (1.6, "pop"), (2.1, "pop"), (2.6, "pop")]),
    Scene("इसीलिए इंस्टाग्राम ने ख़ुद, एक लाइन जोड़ी। यू आर ऑल कॉट अप। मतलब, बस, अब रुक सकते हो।", "", s5, min_dur=4.8, whoosh=True,
          sfx=[(1.0, "chime"), (2.4, "ding")]),
    Scene("तो डिज़ाइनर्स, सरप्राइज़ से ख़ुशी दो, पर यूज़र को फँसाओ मत। हर अच्छे फ़ीड में, रुकने की जगह भी होनी चाहिए।", "", s6, min_dur=5.6,
          whoosh=True, sfx=[(0.4, "pop_hi"), (1.4, "buzz"), (2.4, "pop_hi"), (3.6, "ding")]),
    Scene("सच बताओ, ये रील ख़त्म होते ही, आप रिफ़्रेश करने वाले हो ना? अगर हाँ, तो कमेंट में, रिफ़्रेश लिखो। कल का लॉ, आपकी भरी हुई स्क्रीन को हल्का कर देगा।",
          "", D.s8, min_dur=5.6, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = "auto"

if __name__ == "__main__":
    import daily
    daily.run(35, "Variable Reward", SCENES, "day35_variable_reward", cuts=VO_CUTS)

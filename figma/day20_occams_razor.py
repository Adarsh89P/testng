"""Day 20/45 · Occam's Razor, explained with the Google Search home page.

Among options that do the same job, choose the simplest; cut away everything extra. Around 2000, search portals
crammed news, weather, stocks, email and ads onto one page; Google showed a logo, a search box and two buttons.
Day 02 pattern; the script tells the then-and-now story first, names the law in the middle and ends with a
"would anything break if I removed you?" test. Voice: Rakhi's Day 20 ElevenLabs Tisha K file at
assets/voice/day20/full.mp3 (content-verified); script in docs/scripts/day20.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 20, "Pareto Principle"
W, H = 1080, 1920
G = [(0.26, 0.52, 0.96), (0.92, 0.26, 0.21), (0.98, 0.74, 0.02), (0.26, 0.52, 0.96), (0.20, 0.66, 0.33), (0.92, 0.26, 0.21)]
RAZ = (0.80, 0.85, 0.95)                          # razor steel
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
BX, BY, BW, BH = 90, 620, 900, 900               # browser window
PORTAL = [("News", 0, 0, 2, 1, BLUE), ("Mausam", 2, 0, 1, 1, YELLOW), ("Share", 0, 1, 1, 1, GREEN),
          ("Email", 1, 1, 1, 1, ORANGE), ("Ads", 2, 1, 1, 2, RED), ("Cricket", 0, 2, 1, 1, (0.6, 0.45, 0.9)),
          ("Horoscope", 1, 2, 1, 1, (0.9, 0.5, 0.7)), ("Shopping", 0, 3, 2, 1, (0.4, 0.75, 0.8)),
          ("Ads", 2, 3, 1, 1, RED)]


def browser(c, a=1.0, url="search.com"):
    c.fill_rrect(BX, BY, BW, BH, 22, (0.09, 0.09, 0.10), a)
    c.rrect_path(BX, BY, BW, BH, 22); c.c.set_source_rgba(*GREY, a); c.c.set_line_width(2); c.c.stroke()
    for i, col in enumerate([RED, YELLOW, GREEN]):
        c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(BX + 34 + i * 30, BY + 34, 9, 0, 6.2832); c.c.fill()
    c.fill_rrect(BX + 140, BY + 16, BW - 180, 36, 18, (0.18, 0.18, 0.20), a)
    c.font(SANS, 18, True); c.text(BX + 160, BY + 41, url, DIM, a)


def portal_blocks(c, k_in=1.0, k_out=0.0, flash_t=0.0):
    cw, ch = (BW - 80) / 3, 170
    for i, (lab, gx, gy, sw, sh, col) in enumerate(PORTAL):
        kk = ease(min(1, max(0, k_in * len(PORTAL) - i)))
        if kk <= 0: continue
        x = BX + 30 + gx * (cw + 10); y = BY + 80 + gy * (ch + 12)
        dx = (x + cw * sw / 2 - (BX + BW / 2)) * 1.6 * k_out; dy = (y - BY) * 0.4 * k_out
        a = kk * (1 - k_out)
        if a <= 0.01: continue
        blink = 0.25 * (0.5 + 0.5 * math.sin(flash_t * 9 + i)) if lab == "Ads" else 0
        c.fill_rrect(x + dx, y + dy, cw * sw + (sw - 1) * 10, ch * sh + (sh - 1) * 12, 12, col, (0.35 + blink) * a)
        c.font(SANS, 26, True); c.text(x + dx + 18, y + dy + 42, lab, DOT, a)
        c.dbar(x + dx + 18, y + dy + 70, cw * sw - 60, rows=3, gap=8, col=DOT)


def google_home(c, a=1.0, typed=""):
    c.font(SANS, 96, True)
    word = "Google"; x = W / 2 - c.text_w(word) / 2
    for ch_, col in zip(word, G):
        c.text(x, BY + 380, ch_, col, a); x += c.text_w(ch_)
    c.rrect_path(BX + 110, BY + 440, BW - 220, 76, 38); c.c.set_source_rgba(*GREY, a); c.c.set_line_width(2); c.c.stroke()
    c.dellipse(BX + 160, BY + 476, 14, 14, spacing=4, r=1.6, col=DIM, a=a)
    c.font(SANS, 26, True); c.text(BX + 190, BY + 488, typed, DOT, a)
    for i, lab in enumerate(["Google Search", "I'm Feeling Lucky"]):
        bx = W / 2 - 250 + i * 270
        c.fill_rrect(bx, BY + 560, 230, 60, 8, (0.20, 0.20, 0.22), a)
        c.font(SANS, 20, True); c.text(bx + 115 - c.text_w(lab) / 2, BY + 598, lab, DOT, a)


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # ~2000: portals stuffed with everything
    def world(c):
        browser(c)
        portal_blocks(c, k_in=min(1, t / 3.2), flash_t=t)
        c.pill(W / 2, 540, "san 2000 ke aaspaas", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        if t > 3.6: white_pill(c, W / 2, 1600, "sab ek hi page pe thunse hue", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 1070), 0.95), (d - 0.4, (W / 2, 1070), 1.05)), seed=2)
    hud(cv)


CLEAR = 0.4
def s2(cv, t, d, st):                                     # then Google: a logo, one box, two buttons. Bas.
    def world(c):
        browser(c, url="google.com")
        portal_blocks(c, 1.0, ease(min(1, max(0, (t - CLEAR) / 0.8))), t)
        if t > 1.3:
            k = ease(min(1, (t - 1.3) / 0.6))
            google_home(c, k)
        labels = [("1 logo", 1.6, BY + 330), ("1 search box", 2.3, BY + 478), ("2 button", 3.0, BY + 590)]
        for lab, at, y in labels:
            if t > at: c.pill(BX + BW - 130, y - 60, lab, size=24, fam=MONO, col=DARK, bg=YELLOW, bold=True)
        if t > 3.8: c.pill(W / 2, 1600, "bas.", size=60, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 1070), 1.05), (1.2, (W / 2, 1070), 1.05), (2.0, (W / 2, 1080), 1.12),
                                     (d - 0.4, (W / 2, 1100), 1.05)), punch=0.05 * max(0, 1 - abs(t - 3.8) / 0.12), seed=3)
    hud(cv); flash(cv, t, 1.3, 0.1)


def s3(cv, t, d, st):                                     # people came to search — only that, front and centre
    def world(c):
        browser(c, url="google.com")
        q = "pizza near me"
        typed = q[:int(max(0, (t - 1.0) * 10))]
        google_home(c, 1.0, typed)
        if 0.3 < t < 1.2:
            k = ease((t - 0.3) / 0.9)
            c._dot(BX + BW - 120 - (BW - 340) * k, BY + 760 - 280 * k, 10, (1, 1, 1), 1)
        if t > 1.0 and int(t * 3) % 2 and len(typed) < len(q):
            c.font(SANS, 26, True); w = c.text_w(typed); c.c.set_source_rgba(*DOT, 1); c.c.rectangle(BX + 192 + w, BY + 462, 3, 32); c.c.fill()
        if t > 2.6: c.pill(W / 2, 1600, "jo kaam karne aaye, sirf wahi saamne", size=30, fam=MONO, col=DARK, bg=GREEN, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 1100), 1.05), (1.0, (W / 2, 1100), 1.35), (d - 0.4, (W / 2, 1110), 1.3)), seed=4)
    hud(cv)


CUT = 3.0
def s4(cv, t, d, st):                                     # law named: same job → pick the simplest, cut the extras
    def world(c):
        c.pill(W / 2, 500, "is soch ka naam", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "OCCAM'S RAZOR", 100, W / 2, 620, ease(1 - t / 0.8), col=RAZ)
        c.glow(W / 2, 620, 420, 0.06)
        mono(c, "ek hi kaam, do tareeke?", 740, DOT, 34, chars=int(max(0, t - 0.9) * 28))
        mono(c, "simple wala chuno", 790, YELLOW, 34, chars=int(max(0, t - 1.8) * 28))
        k = ease(min(1, max(0, (t - CUT) / 0.7)))
        bxs = [(W / 2 - 330, 960), (W / 2 - 330, 1060), (W / 2 - 330, 1160), (W / 2 - 330, 1260)]
        for i, (x, y) in enumerate(bxs):
            if i == 0:
                c.fill_rrect(x, y, 660, 80, 14, GREEN, 1); c.font(SANS, 28, True); c.text(x + 24, y + 52, "search box", DARK)
            else:
                fall = k * (120 + i * 60)
                c.fill_rrect(x + k * 80, y + fall, 660, 80, 14, (0.25, 0.25, 0.28), 1 - k)
                c.font(SANS, 26, True); c.text(x + 24 + k * 80, y + fall + 52, ["news", "ads", "horoscope"][i - 1], DIM, 1 - k)
        bl = ease(min(1, max(0, (t - CUT + 0.4) / 0.5)))
        if 0 < bl and t < CUT + 1.2:
            yb = 1040 + 4
            c.dots_path([(W / 2 - 420, yb), (W / 2 - 420 + 840 * bl, yb)], spacing=6, r=3.4, col=RAZ)
        if t > CUT + 1.0: c.pill(W / 2, 1450, "extra cheezein: kaat do", size=30, fam=SANS, col=DARK, bg=RAZ, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 700), 1.25), (2.4, (W / 2, 1050), 1.0), (d - 0.4, (W / 2, 1080), 1.03)),
                  punch=0.05 * max(0, 1 - abs(t - CUT) / 0.12), seed=5)
    hud(cv); flash(cv, t, CUT, 0.1)


def s5(cv, t, d, st):                                     # the test: "if I remove you, does anything break?"
    ELEMS = [("Logo", True), ("Banner", False), ("Search box", True), ("Popup", False), ("Pay button", True),
             ("Badge", False)]
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("hata doon? kuch tootega?") / 2, 560, "hata doon? kuch tootega?", YELLOW)
        for i, (lab, keep) in enumerate(ELEMS):
            at = 0.8 + i * 0.5
            y = 660 + i * 125
            gone = (not keep) and t > at + 0.5
            k = 1 - ease(min(1, max(0, (t - at - 0.5) / 0.5))) if not keep else 1
            c.fill_rrect(W / 2 - 300 + (0 if keep else (1 - k) * 260), y, 600, 96, 16, CARD, k)
            c.font(SANS, 30, True); c.text(W / 2 - 270 + (0 if keep else (1 - k) * 260), y + 60, lab, DOT, k)
            if t > at:
                if keep: c.pill(W / 2 + 200, y + 48, "haan → rakho ✓", size=22, fam=SANS, col=DARK, bg=GREEN, bold=True)
                elif k > 0.05: c.pill(W / 2 + 200, y + 48, "nahi → hatao ✗", size=22, fam=SANS, col=DARK, bg=RED, bold=True, a=k)
        if t > 4.4: white_pill(c, W / 2, 1480, "jo zaroori nahi, use hata do", 36)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.05), (d - 0.4, (W / 2, 1020), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # closing line: design is done when nothing is left to remove
    def world(c):
        l1 = "design tab poora nahi hota"; l2 = "jab jodne ko kuch na bache,"; l3 = "balki tab,"; l4 = "jab hatane ko kuch na bache."
        mono(c, l1, 640, DIM, 36, chars=int(t * 26))
        mono(c, l2, 700, DOT, 40, chars=int(max(0, t - 1.0) * 26))
        if t > 2.2:
            k = ease(min(1, (t - 2.2) / 0.4))
            c.font(MONO, 40, True); w = c.text_w(l2)
            c.c.set_source_rgba(*RED, 1); c.c.rectangle(W / 2 - w / 2, 690, w * k, 4); c.c.fill()
        mono(c, l3, 800, DOT, 40, chars=int(max(0, t - 2.6) * 26))
        mono(c, l4, 860, YELLOW, 44, chars=int(max(0, t - 3.0) * 26))
        n = max(1, 7 - int(max(0, t - 1.0) * 1.6))
        for i in range(n):
            c.fill_rrect(W / 2 - 240, 1000 + i * 70, 480 if i == 0 else 480 - i * 40, 50, 12, GREEN if i == 0 else CARD, 1)
        if n == 1: c.font(SANS, 26, True); c.text(W / 2 - 220, 1034, "sirf zaroori", DARK)
    stage.compose(cv, t, d, world, K((0, (W / 2, 800), 1.15), (d - 0.4, (W / 2, 950), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 20 script (docs/scripts/day20.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("डे ट्वेंटी! पैंतालीस यू एक्स लॉज़ में, आधा रास्ता बस आने ही वाला है।", "", D.s0, min_dur=4.0,
          sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("सन दो हज़ार के आसपास, ज़्यादातर सर्च वेबसाइट्स ऐसी दिखती थीं। न्यूज़, मौसम, शेयर, ईमेल, ऐड्स, सब एक ही पेज पे ठुँसे हुए।",
          "", s1, min_dur=6.4, whoosh=True, sfx=[(i * 0.36, "pop") for i in range(9)] + [(3.6, "buzz")]),
    Scene("और फिर आया गूगल। एक लोगो, एक सर्च बॉक्स, और दो बटन। बस।", "", s2, min_dur=5.0, whoosh=True,
          sfx=[(CLEAR, "riser"), (1.3, "chime"), (1.6, "pop_hi"), (2.3, "pop_hi"), (3.0, "pop_hi"), (3.8, "drop")]),
    Scene("लोगों को यही तो चाहिए था। जो काम करने आए हो, सिर्फ़ वही सामने। बाक़ी सब, रास्ते से हटा दिया।", "", s3,
          min_dur=5.4, whoosh=True, sfx=[(1.0 + i * 0.1, "tick") for i in range(13)] + [(2.6, "ding")]),
    Scene("इस सोच का नाम है, ओकम्स रेज़र। अगर दो तरीके एक ही काम करें, तो जो सबसे सिंपल है, वही चुनो। बाक़ी एक्स्ट्रा चीज़ें, रेज़र से काट दो।",
          "", s4, min_dur=7.0, whoosh=True, sfx=[(0.2, "drop"), (CUT - 0.4, "riser"), (CUT, "buzz"), (CUT + 1.0, "ding")]),
    Scene("अपनी किसी भी स्क्रीन को खोलो, और हर एलिमेंट से पूछो, तुम्हें हटा दूँ, तो क्या कुछ टूटेगा? अगर नहीं, तो उसे हटा दो।", "", s5,
          min_dur=6.2, whoosh=True, sfx=[(0.8 + i * 0.5, "pop_hi" if i % 2 == 0 else "pop_lo") for i in range(6)] + [(4.4, "ding")]),
    Scene("क्योंकि डिज़ाइन तब पूरा नहीं होता जब जोड़ने को कुछ न बचे, बल्कि तब, जब हटाने को कुछ न बचे।", "", s6, min_dur=5.6,
          whoosh=True, sfx=[(2.2, "buzz"), (3.0, "riser"), (4.2, "chime")]),
    Scene("कल, डे ट्वेंटी वन, पेरेटो प्रिंसिपल। तब तक, डिज़ाइन विद राखी को फ़ॉलो करो।", "", D.s8, min_dur=5.0, whoosh=True,
          clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 20 file (model v4) has no pauses (break tags ignored): line cuts found by aligning it to a TTS reading of the
# script, each placed in the silence between sentences; line check 8/8.
VO_CUTS = [5.94, 16.34, 22.22, 28.94, 39.4, 47.74, 54.54]

if __name__ == "__main__":
    import daily
    daily.run(20, "Occam's Razor", SCENES, "day20_occams_razor", cuts=VO_CUTS)

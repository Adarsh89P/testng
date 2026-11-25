"""Day 37/45 · Visibility of System Status, explained with WhatsApp's ticks.

Users should always know, clearly and right away, what the system is doing. One grey tick = sent, two grey = delivered,
two blue = read (and then no reply…). Without ticks you'd only guess. Order tracking ("rider 2 min away"), download
progress bars and UPI's "processing" are the same law; when status is visible waits feel shorter, when nothing shows
five seconds feel like five minutes. Never leave users in the dark: every tap gets a response. Day 02 pattern; hook
pays off yesterday's teaser. Voice: Rakhi's Day 37 ElevenLabs Tisha K file at assets/voice/day37/full.mp3
(content-verified); script in docs/scripts/day37.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 37, "Recognition over Recall"
W, H = 1080, 1920
WA = (0.15, 0.83, 0.40)                           # WhatsApp green
WAB = (0.33, 0.73, 0.98)                          # read-receipt blue
BUB = (0.02, 0.36, 0.30)                          # sent bubble
RED, GREEN, BLUE, YELLOW, ORANGE, COLS = D.RED, D.GREEN, D.BLUE, D.YELLOW, D.ORANGE, D.COLS
ANCHOR = D.ANCHOR
stage = Stage(W, H, ANCHOR)
K, hud, mono, phone = D.K, D.hud, D.mono, D.phone
DARK = (0.05, 0.05, 0.05)
GREY = (0.40, 0.40, 0.44)
CARD = (0.13, 0.13, 0.15)
PX, PY, PW, PH = W / 2, 1060, 480, 880
X0, Y0 = PX - PW / 2, PY - PH / 2


def tick(c, x, y, s=1.0, col=GREY, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.set_line_width(3.2 * s)
    c.c.move_to(x - 8 * s, y); c.c.line_to(x - 2 * s, y + 6 * s); c.c.line_to(x + 10 * s, y - 8 * s); c.c.stroke(); c.c.new_path()


def ticks(c, x, y, state, s=1.0, a=1.0):
    """state 1 = sent (one grey), 2 = delivered (two grey), 3 = read (two blue)."""
    col = WAB if state == 3 else GREY
    tick(c, x, y, s, col, a)
    if state >= 2: tick(c, x + 9 * s, y, s, col, a)


def chat_head(c, name="Rahul"):
    phone(c, PX, PY, PW, PH)
    c.fill_rrect(X0 + 10, Y0 + 50, PW - 20, 76, 12, (0.07, 0.20, 0.17))
    c.c.new_path(); c.c.set_source_rgba(0.35, 0.55, 0.85, 1); c.c.arc(X0 + 56, Y0 + 88, 22, 0, 6.2832); c.c.fill()
    c.font(SANS, 26, True); c.text(X0 + 92, Y0 + 98, name, DOT)


def bubble(c, y, txt, state, a=1.0):
    c.font(SANS, 24, True); w = c.text_w(txt) + 110
    x = X0 + PW - 26 - w
    c.fill_rrect(x, y, w, 64, 16, BUB, a)
    c.font(SANS, 24, True); c.text(x + 20, y + 41, txt, DOT, a)
    c.font(SANS, 14, True); c.text(x + w - 88, y + 52, "9:41", DIM, a)
    if state: ticks(c, x + w - 34, y + 46, state, 1.0, a)


# ------------------------------------------------------------------ scenes
S1, S2, S3 = 0.6, 1.8, 3.2
def s1(cv, t, d, st):                                     # sent → delivered → read … and no reply
    def world(c):
        chat_head(c)
        state = 1 if t < S2 else 2 if t < S3 else 3
        if t > S1: bubble(c, Y0 + 200, "Kal movie chalein?", state)
        labs = [("1 grey: bhej diya", S1, GREY), ("2 grey: pahunch gaya", S2, GREY), ("2 blue: padh liya", S3, WAB)]
        for j, (lab, at, col) in enumerate(labs):
            if t > at: c.pill(PX + 280, Y0 + 300 + j * 80, lab, size=22, fam=SANS, col=DARK, bg=col if col != GREY else (0.75, 0.75, 0.78), bold=True)
        if t > S3 + 1.0:
            secs = int((t - S3 - 1.0) * 40)
            c.font(MONO, 28, True); c.text(X0 + 40, Y0 + 420, f"… {secs}s, koi reply nahi", DIM)
        if t > S3 + 2.0: white_pill(c, W / 2, 1660, "aur phir, reply nahi aaya", 36)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 70, Y0 + 300), 1.2), (d - 0.4, (PX + 60, Y0 + 340), 1.15)),
                  punch=0.05 * max(0, 1 - abs(t - S3) / 0.12), seed=2)
    hud(cv); flash(cv, t, S3, 0.08)


def s2(cv, t, d, st):                                     # what if there were no ticks? → only guessing
    def world(c):
        chat_head(c)
        bubble(c, Y0 + 200, "Kal movie chalein?", 0)
        c.font(SANS, 60, True); c.text(X0 + PW - 90, Y0 + 330, "?", YELLOW)
        thoughts = [("gaya ya nahi?", 0.8), ("phone band hai?", 1.6), ("padha ya nahi?", 2.4)]
        for j, (th, at) in enumerate(thoughts):
            if t > at:
                k = ease(min(1, (t - at) / 0.4))
                c.pill(PX - 40 + (j % 2) * 120, Y0 + 460 + j * 90, th, size=26, fam=SANS, col=DARK, bg=(0.95, 0.95, 0.96), bold=True, a=k)
        if t > 3.4: white_pill(c, W / 2, 1660, "bas andaaza lagaate rehte", 38)
    stage.compose(cv, t, d, world, K((0, (PX + 60, Y0 + 340), 1.15), (d - 0.4, (PX + 20, Y0 + 420), 1.1)), seed=3)
    hud(cv)


def s3(cv, t, d, st):                                     # law named: what's going on must be clear and immediate
    def world(c):
        c.pill(W / 2, 480, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "VISIBILITY OF", 100, W / 2, 600, ease(1 - t / 0.8), col=WA)
        dot_text(c, "SYSTEM STATUS", 100, W / 2, 720, ease(1 - (t - 0.2) / 0.8), col=WA)
        for j, (lab, at) in enumerate([("kya chal raha hai", 1.8), ("saaf", 2.6), ("turant", 3.2)]):
            if t > at:
                k = ease(min(1, (t - at) / 0.4))
                c.pill(W / 2 - 280 + j * 280, 900, lab, size=30, fam=SANS, col=DARK, bg=WA, bold=True, a=k)
        if t > 3.8:
            c.fill_rrect(W / 2 - 300, 1000, 600, 160, 24, CARD)
            ticks(c, W / 2 - 200, 1080, 1, 2.2); ticks(c, W / 2 - 30, 1080, 2, 2.2); ticks(c, W / 2 + 160, 1080, 3, 2.2)
    stage.compose(cv, t, d, world, K((0, (W / 2, 660), 1.15), (1.6, (W / 2, 900), 1.0), (d - 0.4, (W / 2, 930), 1.02)), seed=4)
    hud(cv); flash(cv, t, 0.2)


def s4(cv, t, d, st):                                     # same law: rider 2 min away, download progress, UPI processing
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("har jagah yahi law") / 2, 560, "har jagah yahi law", WA)
        cards = [(0.3, "Order tracking"), (1.4, "Download"), (2.5, "UPI payment")]
        for j, (at, title) in enumerate(cards):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            y = 650 + j * 240
            c.fill_rrect(W / 2 - 400, y, 800, 210, 24, CARD, k)
            c.font(SANS, 28, True); c.text(W / 2 - 370, y + 50, title, DOT, k)
            lt = t - at
            if j == 0:
                c.dots_path([(W / 2 - 360, y + 140), (W / 2 + 300, y + 140)], spacing=10, r=3, col=GREY, a=k)
                rx = W / 2 - 360 + 520 * min(1, lt / 2.0)
                c.c.new_path(); c.c.set_source_rgba(*ORANGE, k); c.c.arc(rx, y + 140, 16, 0, 6.2832); c.c.fill()
                c.c.new_path(); c.c.set_source_rgba(*GREEN, k); c.c.arc(W / 2 + 320, y + 140, 18, 0, 6.2832); c.c.fill()
                c.font(SANS, 24, True); c.text(W / 2 + 80, y + 52, "Rider 2 min door", ORANGE, k)
            elif j == 1:
                p = min(1, lt / 2.0)
                c.fill_rrect(W / 2 - 360, y + 120, 640, 30, 15, (0.25, 0.25, 0.28), k)
                c.fill_rrect(W / 2 - 360, y + 120, 640 * p, 30, 15, BLUE, k)
                c.font(MONO, 26, True); c.text(W / 2 + 300, y + 145, f"{int(p * 100)}%", DOT, k)
            else:
                for i in range(10):
                    ang = t * 7 + i * 0.63
                    c._dot(W / 2 - 320 + math.cos(ang) * 22, y + 135 + math.sin(ang) * 22, 3 + i * 0.4, DOT, k * (0.2 + i * 0.08))
                c.font(SANS, 28, True); c.text(W / 2 - 270, y + 145, "Processing…", DOT, k)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 990), 1.0)), seed=5)
    hud(cv)


def s5(cv, t, d, st):                                     # visible → waits feel short; blank → 5 sec feels like 5 min
    def world(c):
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 200, 640, 400, 560, 24, CARD); c.fill_rrect(rx - 200, 640, 400, 560, 24, (0.06, 0.06, 0.07))
        c.rrect_path(rx - 200, 640, 400, 560, 24); c.c.set_source_rgba(*GREY, 1); c.c.set_line_width(1.5); c.c.stroke()
        p = min(1, t / 3.0)
        c.fill_rrect(lx - 160, 860, 320, 26, 13, (0.25, 0.25, 0.28)); c.fill_rrect(lx - 160, 860, 320 * p, 26, 13, WA)
        c.font(SANS, 26, True); c.text(lx - 160, 830, "Uploading…", DOT)
        c.font(MONO, 30, True); c.text(lx - 60, 960, f"{int(p * 5)} sec", WA)
        c.pill(lx, 1260, "intezaar chhota lagta", size=24, fam=SANS, col=DARK, bg=WA, bold=True)
        c.font(MONO, 30, True); c.text(rx - 60, 960, f"{int(p * 5)} sec", DIM)
        if t > 1.6:
            c.font(SANS, 60, True); c.text(rx - 20, 860, "?", YELLOW)
        if t > 2.6: c.pill(rx, 1260, "= 5 minute jaisa", size=24, fam=SANS, col=DARK, bg=RED, bold=True)
        c.font(SANS, 34, True); c.text(lx - c.text_w("dikhta hai") / 2, 720, "dikhta hai", WA)
        c.text(rx - c.text_w("kuch nahi") / 2, 720, "kuch nahi", DIM)
    stage.compose(cv, t, d, world, K((0, (W / 2, 940), 1.0), (d - 0.4, (W / 2, 960), 1.02)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # tip: never leave users in the dark — every tap gets a response
    def world(c):
        c.font(SANS, 46, True); c.text(W / 2 - c.text_w("har tap ka jawaab do") / 2, 560, "har tap ka jawaab do", WA)
        items = [("ek tick", 0.6), ("ek spinner", 1.6), ("bas, ho gaya", 2.6)]
        for j, (lab, at) in enumerate(items):
            k = ease(min(1, max(0, (t - at) / 0.4)))
            if k <= 0: continue
            x = W / 2 - 300 + j * 300; y = 900
            c.c.new_path(); c.c.set_source_rgba(*CARD, k); c.c.arc(x, y, 110, 0, 6.2832); c.c.fill()
            if j == 0: ticks(c, x - 10, y + 6, 3, 4.0, k)
            elif j == 1:
                for i in range(10):
                    ang = t * 7 + i * 0.63
                    c._dot(x + math.cos(ang) * 44, y + math.sin(ang) * 44, 5 + i * 0.6, DOT, k * (0.2 + i * 0.08))
            else:
                c.c.new_path(); c.c.set_source_rgba(*GREEN, k); c.c.arc(x, y, 60, 0, 6.2832); c.c.fill()
                c.dots_path([(x - 26, y), (x - 6, y + 22), (x + 30, y - 20)], spacing=5, r=4, col=(1, 1, 1), a=k)
            c.font(SANS, 30, True); c.text(x - c.text_w(lab) / 2, y + 170, lab, DOT, k)
        if t > 3.6: white_pill(c, W / 2, 1240, "user ko kabhi andhere mein mat chhodo", 32)
    stage.compose(cv, t, d, world, K((0, (W / 2, 900), 1.05), (d - 0.4, (W / 2, 960), 1.0)), seed=8)
    hud(cv)


# Narration: the approved Day 37 script (docs/scripts/day37.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("दो नीली लाइनें, और कितनी दोस्तियाँ टूट गईं। डे थर्टी सेवन में, आज इन टिक्स का पूरा राज़।", "", D.s0, min_dur=4.6,
          sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("आपने मैसेज भेजा। एक ग्रे टिक, यानी भेज दिया। दो ग्रे टिक, यानी पहुँच गया। और दो नीले टिक, यानी पढ़ लिया। और फिर, रिप्लाई नहीं आया।", "", s1,
          min_dur=6.6, whoosh=True, sfx=[(S1, "pop"), (S2, "pop_hi"), (S3, "chime"), (S3 + 1.0, "tick"), (S3 + 2.0, "drop")]),
    Scene("अब सोचो, अगर ये टिक्स होते ही नहीं। मैसेज गया या नहीं, फ़ोन बंद है या नहीं, आप बस अंदाज़ा लगाते रहते।", "", s2, min_dur=5.4,
          whoosh=True, sfx=[(0.3, "buzz"), (0.8, "pop_lo"), (1.6, "pop_lo"), (2.4, "pop_lo"), (3.4, "pop")]),
    Scene("इसे कहते हैं, विज़िबिलिटी ऑफ़ सिस्टम स्टेटस। सिस्टम में क्या चल रहा है, यूज़र को हमेशा, साफ़ और तुरंत पता होना चाहिए।", "", s3, min_dur=6.0,
          whoosh=True, sfx=[(0.2, "drop"), (1.8, "pop_hi"), (2.6, "pop_hi"), (3.2, "pop_hi"), (3.8, "chime")]),
    Scene("ऑर्डर ट्रैकिंग में राइडर दो मिनट दूर, डाउनलोड की प्रोग्रेस बार, यूपीआई में प्रोसेसिंग, सब यही लॉ है।", "", s4, min_dur=5.6, whoosh=True,
          sfx=[(0.3, "pop"), (1.4, "pop"), (2.5, "pop"), (3.6, "ding")]),
    Scene("जब सब दिखता है, तो इंतज़ार भी छोटा लगता है। और जब कुछ नहीं दिखता, तो पाँच सेकंड भी, पाँच मिनट लगते हैं।", "", s5, min_dur=5.6,
          whoosh=True, sfx=[(0.3, "riser"), (1.6, "buzz"), (2.6, "drop")]),
    Scene("तो डिज़ाइनर्स, यूज़र को कभी अंधेरे में मत छोड़ो। हर टैप के बाद, कुछ तो जवाब दो। एक टिक, एक स्पिनर, या बस, हो गया।", "", s6, min_dur=6.0,
          whoosh=True, sfx=[(0.6, "pop_hi"), (1.6, "pop_hi"), (2.6, "chime"), (3.6, "ding")]),
    Scene("आप ब्लू टिक ऑन रखते हो, या ऑफ़? कमेंट में ऑन या ऑफ़ लिखो। और कल, एक छोटा सा हरा-लाल निशान, जो बिना पढ़े खाना चुनवा देता है।", "", D.s8,
          min_dur=5.6, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

VO_CUTS = [7.87, 19.61, 28.07, 37.17, 44.37, 52.61, 62.39]

if __name__ == "__main__":
    import daily
    daily.run(37, "Visibility of System Status", SCENES, "day37_system_status", cuts=VO_CUTS)

"""Day 32/45 · Endowment Effect, explained with Spotify Premium's free trial.

Once something is ours, or feels ours, we value it more. A month of free Premium (no ads, downloads, your own
playlist) ends with "Premium is going, your downloads too" and people pay without thinking. In the mug experiment
(Kahneman, Knetsch & Thaler, 1990) owners asked about twice what buyers offered. A trial isn't a gift, it's
ownership; designers should remind before charging and keep cancel to one tap. Day 02 pattern; the script opens on an
open-loop question before the day number. Voice: Rakhi's Day 32 ElevenLabs Tisha K file at
assets/voice/day32/full.mp3 (content-verified); script in docs/scripts/day32.md.
"""
import os, sys, math
from engine import *
from fx import Stage, dot_text, flash, ring
import day02_hicks_law as D

D.DAY, D.NEXT = 32, "Reciprocity"
W, H = 1080, 1920
SPOT = (0.12, 0.84, 0.38)                         # Spotify green
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
SONGS = ["Kesariya", "Apna Bana Le", "Tum Hi Ho", "Raataan Lambiyan", "Heeriye", "Chaleya"]


def spotify_logo(c, x, y, s=1.0, a=1.0):
    c.c.new_path(); c.c.set_source_rgba(*SPOT, a); c.c.arc(x, y, 26 * s, 0, 6.2832); c.c.fill()
    for i, (w, dy) in enumerate([(30, -8), (24, 2), (18, 11)]):
        c.c.new_path(); c.c.set_source_rgba(0, 0, 0, a); c.c.set_line_width((4 - i * 0.6) * s)
        c.c.arc(x, y + dy * s + 22 * s, (w + 6) * s, math.radians(240), math.radians(300)); c.c.stroke()
    c.c.new_path()


def mug(c, x, y, s=1.0, col=(0.95, 0.95, 0.96), a=1.0):
    c.fill_rrect(x - 40 * s, y - 50 * s, 80 * s, 100 * s, 14 * s, col, a)
    c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.set_line_width(10 * s)
    c.c.arc(x + 44 * s, y, 22 * s, -math.pi / 2, math.pi / 2); c.c.stroke(); c.c.new_path()


def person(c, x, y, col, a=1.0, s=1.0):
    c.c.new_path(); c.c.set_source_rgba(*col, a); c.c.arc(x, y - 70 * s, 34 * s, 0, 6.2832); c.c.fill()
    c.fill_rrect(x - 50 * s, y - 28 * s, 100 * s, 140 * s, 36 * s, col, a)


def song_row(c, y, nm, i, a=1.0, faded=False):
    c.fill_rrect(X0 + 20, y, PW - 40, 70, 12, CARD, a)
    c.fill_rrect(X0 + 32, y + 10, 50, 50, 8, tuple(0.2 + cc * 0.5 for cc in COLS[i % 6]), a * (0.4 if faded else 1))
    c.font(SANS, 22, True); c.text(X0 + 98, y + 44, nm, DIM if faded else DOT, a)
    c.c.new_path(); c.c.set_source_rgba(*(GREY if faded else SPOT), a)
    c.c.move_to(X0 + PW - 60, y + 26); c.c.line_to(X0 + PW - 60, y + 44); c.c.stroke()
    c.c.move_to(X0 + PW - 68, y + 38); c.c.line_to(X0 + PW - 60, y + 46); c.c.line_to(X0 + PW - 52, y + 38); c.c.stroke(); c.c.new_path()


# ------------------------------------------------------------------ scenes
def s1(cv, t, d, st):                                     # Spotify: a month of Premium free → no ads, downloads, your own playlist
    def world(c):
        phone(c, PX, PY, PW, PH)
        spotify_logo(c, X0 + 56, Y0 + 92)
        c.font(SANS, 28, True); c.text(X0 + 96, Y0 + 102, "Premium", DOT)
        c.fill_rrect(X0 + 20, Y0 + 140, PW - 40, 120, 18, (0.08, 0.30, 0.16))
        c.font(SANS, 30, True); c.text(X0 + 40, Y0 + 192, "1 mahina FREE", SPOT)
        c.font(SANS, 20, True); c.text(X0 + 40, Y0 + 230, "Try Premium · cancel anytime", DOT)
        for j, (lab, at) in enumerate([("bina ads ke gaane", 0.8), ("offline download", 1.6)]):
            if t > at: c.pill(PX + 285, Y0 + 180 + j * 80, lab + " ✓", size=22, fam=SANS, col=DARK, bg=SPOT, bold=True)
        if t > 2.4:
            c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 310, "Meri playlist ♥", DOT)
            n = min(len(SONGS), int((t - 2.4) * 2.2) + 1)
            for i in range(n): song_row(c, Y0 + 330 + i * 80, SONGS[i], i)
            c.pill(PX + 285, Y0 + 340, "aapki apni playlist", size=22, fam=SANS, col=DARK, bg=GOLD, bold=True)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 70, Y0 + 300), 1.15), (2.4, (PX + 60, Y0 + 400), 1.05),
                                     (d - 0.4, (PX + 60, Y0 + 460), 1.05)), seed=2)
    hud(cv)


PAY = 3.4
def s2(cv, t, d, st):                                     # month ends: "Premium is going, your downloads too" → paid without thinking
    def world(c):
        phone(c, PX, PY, PW, PH)
        spotify_logo(c, X0 + 56, Y0 + 92)
        c.font(SANS, 24, True); c.text(X0 + 30, Y0 + 170, "Meri playlist ♥", DOT)
        fade = ease(min(1, max(0, (t - 1.0) / 1.0))) if t < PAY else 0
        for i in range(6): song_row(c, Y0 + 190 + i * 80, SONGS[i], i, faded=fade > 0.5)
        if 0.6 < t < PAY + 0.6:
            k = ease(min(1, (t - 0.6) / 0.4))
            c.c.new_path(); c.c.set_source_rgba(0, 0, 0, 0.6 * k); c.c.rectangle(X0, Y0, PW, PH); c.c.fill()
            c.fill_rrect(X0 + 30, Y0 + 300, PW - 60, 330, 22, (0.15, 0.15, 0.17), k)
            c.font(SANS, 26, True); c.text(X0 + 56, Y0 + 360, "Premium kal khatam", RED, k)
            c.font(SANS, 20, True); c.text(X0 + 56, Y0 + 400, "Aapke 48 downloads bhi chale jaayenge", DOT, k)
            pressed = PAY < t < PAY + 0.25
            c.fill_rrect(X0 + 56, Y0 + 460 + (4 if pressed else 0), PW - 112, 70, 35, SPOT, k)
            c.font(SANS, 24, True); c.text(PX - c.text_w("Keep Premium") / 2, Y0 + 505, "Keep Premium", DARK, k)
            c.font(SANS, 18, True); c.text(PX - c.text_w("Not now") / 2, Y0 + 580, "Not now", DIM, k)
        if PAY - 0.8 < t < PAY + 0.2:
            k = ease(min(1, (t - PAY + 0.8) / 0.8))
            c._dot(PX + 170 - 170 * k, Y0 + 700 - 205 * k, 13, (1, 1, 1), 1)
        if t > PAY + 0.6:
            k = ease(min(1, (t - PAY - 0.6) / 0.4))
            c.fill_rrect(X0 + 30, Y0 + 680, PW - 60, 90, 18, (0.08, 0.30, 0.16), k)
            c.font(SANS, 24, True); c.text(X0 + 56, Y0 + 735, "✓ Plan renewed · paid", SPOT, k)
        if t > PAY + 1.0: white_pill(c, W / 2, 1660, "aur aapne, bina soche, pay kar diya", 34)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX, Y0 + 450), 1.15), (d - 0.4, (PX, Y0 + 520), 1.1)),
                  punch=0.05 * max(0, 1 - abs(t - PAY) / 0.12), seed=3)
    hud(cv); flash(cv, t, PAY, 0.08)


def s3(cv, t, d, st):                                     # mug experiment: owners ask about twice what buyers offer
    def world(c):
        c.pill(W / 2, 560, "ek mashhoor experiment", size=30, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        lx, rx = W * 0.27, W * 0.73
        k = ease(min(1, max(0, (t - 0.3) / 0.5)))
        person(c, lx, 900, (0.35, 0.55, 0.85), k); person(c, rx, 900, (0.85, 0.50, 0.35), k)
        mug(c, lx + 80, 900, 0.9, a=k)
        c.font(SANS, 28, True); c.text(lx - c.text_w("jiske paas mug") / 2, 1110, "jiske paas mug", DOT, k)
        c.font(SANS, 28, True); c.text(rx - c.text_w("khareedne waala") / 2, 1110, "khareedne waala", DOT, k)
        g = ease(min(1, max(0, (t - 1.6) / 1.2)))
        c.fill_rrect(lx - 50, 1460 - 240 * g, 100, 240 * g, 12, GOLD)
        c.fill_rrect(rx - 50, 1460 - 120 * g, 100, 120 * g, 12, GREY)
        if g >= 1:
            c.pill(lx, 1190, "bechunga: ₹₹", size=26, fam=SANS, col=DARK, bg=GOLD, bold=True)
            c.pill(rx, 1300, "doonga: ₹", size=26, fam=SANS, col=DOT, bg=GREY, bold=True)
        if t > 3.6: white_pill(c, W / 2, 1560, "lagbhag doguni qeemat!", 38)
    stage.compose(cv, t, d, world, K((0, (W / 2, 950), 1.0), (d - 0.4, (W / 2, 1080), 0.98)), seed=4)
    hud(cv)


def s4(cv, t, d, st):                                     # law named: what's ours (or feels ours) suddenly costs more
    def world(c):
        c.pill(W / 2, 500, "ise kehte hain", size=28, fam=MONO, col=DARK, bg=(0.95, 0.95, 0.96), bold=True)
        dot_text(c, "ENDOWMENT", 116, W / 2, 630, ease(1 - t / 0.8), col=GOLD)
        dot_text(c, "EFFECT", 130, W / 2, 770, ease(1 - (t - 0.2) / 0.8), col=GOLD)
        mug(c, W / 2 - 200, 1060, 1.3)
        if t > 1.8:
            k = ease(min(1, (t - 1.8) / 0.4))
            c.pill(W / 2 - 200, 940, "MERA", size=30, fam=SANS, col=DARK, bg=GOLD, bold=True, a=k)
        g = 0.3 + 0.7 * ease(min(1, max(0, (t - 2.2) / 1.2)))
        c.font(SANS, 26, True); c.text(W / 2 + 40, 980, "qeemat (lagti hai)", DIM)
        c.fill_rrect(W / 2 + 40, 1000, 340, 40, 20, (0.20, 0.20, 0.22))
        c.fill_rrect(W / 2 + 40, 1000, 340 * g, 40, 20, GOLD)
        if t > 3.6: c.pill(W / 2, 1300, "apni lagi = qeemat achaanak badhi", size=28, fam=MONO, col=DARK, bg=GOLD, bold=True)
    stage.compose(cv, t, d, world, K((0, (W / 2, 680), 1.2), (1.4, (W / 2, 1040), 1.0), (d - 0.4, (W / 2, 1080), 1.02)), seed=5)
    hud(cv); flash(cv, t, 0.2)


def s5(cv, t, d, st):                                     # trial isn't a gift — it's ownership; leaving feels like losing
    def world(c):
        lx, rx = W * 0.27, W * 0.73
        c.fill_rrect(lx - 90, 760, 180, 150, 14, (0.60, 0.25, 0.45))
        c.c.set_source_rgba(1, 1, 1, 0.8); c.c.rectangle(lx - 12, 760, 24, 150); c.c.rectangle(lx - 90, 820, 180, 24); c.c.fill()
        c.font(SANS, 34, True); c.text(lx - c.text_w("gift") / 2, 990, "gift", DIM)
        if t > 0.8: c.font(SANS, 70, True); c.text(lx - 22, 860, "✗", RED)
        k = ease(min(1, max(0, (t - 1.2) / 0.5)))
        c.c.new_path(); c.c.set_source_rgba(*GOLD, k)
        c.c.move_to(rx, 900); c.c.curve_to(rx - 120, 820, rx - 90, 700, rx, 760); c.c.curve_to(rx + 90, 700, rx + 120, 820, rx, 900)
        c.c.fill(); c.c.new_path()
        c.font(SANS, 34, True); c.text(rx - c.text_w("apnapan") / 2, 990, "apnapan", GOLD, k)
        if t > 2.4:
            c.pill(W / 2, 1180, "apni lagi → chhodna = khona", size=32, fam=SANS, col=DARK, bg=GOLD, bold=True)
        if t > 3.4: white_pill(c, W / 2, 1320, "trial koi gift nahi, ek apnapan hai", 34)
    stage.compose(cv, t, d, world, K((0, (W * 0.27, 880), 1.25), (1.0, (W * 0.27, 880), 1.25), (1.6, (W / 2, 950), 1.0),
                                     (d - 0.4, (W / 2, 1020), 1.0)), seed=6)
    hud(cv)


def s6(cv, t, d, st):                                     # ethics: remind before charging, one-tap cancel — trust > a month's money
    def world(c):
        phone(c, PX, PY, PW, PH)
        k = ease(min(1, max(0, (t - 0.4) / 0.5)))
        c.fill_rrect(X0 + 20, Y0 + 120 - 60 * (1 - k), PW - 40, 150, 20, (0.18, 0.18, 0.20), k)
        spotify_logo(c, X0 + 66, Y0 + 170, 0.8, k)
        c.font(SANS, 22, True); c.text(X0 + 104, Y0 + 168, "3 din mein charge hoga", DOT, k)
        c.font(SANS, 18, True); c.text(X0 + 104, Y0 + 200, "Trial khatam ho raha hai", DIM, k)
        if t > 1.4:
            c.fill_rrect(X0 + 40, Y0 + 300, PW - 80, 70, 35, (0.25, 0.25, 0.28))
            c.font(SANS, 24, True); c.text(PX - c.text_w("Cancel · 1 tap") / 2, Y0 + 345, "Cancel · 1 tap", DOT)
        for j, (lab, at) in enumerate([("pehle yaad dilao", 0.9), ("cancel aasaan", 1.8)]):
            if t > at: c.pill(PX + 280, Y0 + 180 + j * 150, lab + " ✓", size=22, fam=SANS, col=DARK, bg=GREEN, bold=True)
        if t > 2.8:
            c.font(SANS, 46, True); c.text(PX - c.text_w("bharosa > paise") / 2, Y0 + 520, "bharosa > paise", GOLD)
        if t > 3.6: white_pill(c, W / 2, 1660, "bharosa, ek mahine ke paison se qeemti", 32)
    stage.compose(cv, t, d, world, K((0, ANCHOR, 1.0), (0.6, (PX + 60, Y0 + 300), 1.15), (d - 0.4, (PX + 40, Y0 + 380), 1.1)), seed=8)
    hud(cv)


# Narration: the approved Day 32 script (docs/scripts/day32.md, Devanagari version). Voice-overs use exactly these lines.
SCENES = [
    Scene("एक फ़्री ट्रायल ने, आपसे हर महीने पैसे कैसे निकलवा लिए? डे थर्टी टू में, आज ये राज़ खुलेगा।", "", D.s0, min_dur=4.6,
          sfx=[(0.0, "riser"), (1.5, "pop_hi")]),
    Scene("स्पॉटिफ़ाई ने कहा, एक महीना प्रीमियम, बिल्कुल फ़्री। बिना ऐड्स के गाने, ऑफ़लाइन डाउनलोड, और धीरे-धीरे, आपकी अपनी प्लेलिस्ट।", "", s1,
          min_dur=6.0, whoosh=True, sfx=[(0.3, "chime"), (0.8, "pop_hi"), (1.6, "pop_hi")] + [(2.4 + i / 2.2, "pop") for i in range(6)]),
    Scene("फिर महीना ख़त्म, और स्क्रीन पर लिखा आया, प्रीमियम जाने वाला है, आपके डाउनलोड्स भी। और आपने, बिना सोचे, पे कर दिया।", "", s2,
          min_dur=6.0, whoosh=True, sfx=[(0.6, "buzz"), (1.0, "drop"), (PAY, "pop"), (PAY + 0.6, "chime"), (PAY + 1.0, "ding")]),
    Scene("एक मशहूर एक्सपेरिमेंट में, लोगों को एक साधारण सा कॉफ़ी मग दिया गया। और जिनके हाथ में मग था, उन्होंने उसे बेचने के लिए, लगभग दोगुनी क़ीमत माँगी।",
          "", s3, min_dur=6.6, whoosh=True, sfx=[(0.3, "pop"), (1.6, "riser"), (2.8, "pop_hi"), (3.6, "ding")]),
    Scene("इसे कहते हैं, एंडाउमेंट इफ़ेक्ट। जो चीज़ हमारी हो जाती है, या हमें अपनी लगने लगती है, उसकी क़ीमत, अचानक बढ़ जाती है।", "", s4,
          min_dur=6.0, whoosh=True, sfx=[(0.2, "drop"), (1.8, "pop_hi"), (2.2, "riser"), (3.6, "ding")]),
    Scene("ट्रायल कोई गिफ़्ट नहीं, एक अपनापन है। एक बार चीज़ अपनी लगी, तो छोड़ना, खोने जैसा लगता है।", "", s5, min_dur=5.2, whoosh=True,
          sfx=[(0.8, "buzz"), (1.2, "chime"), (2.4, "pop_hi"), (3.4, "ding")]),
    Scene("पर डिज़ाइनर्स, चार्ज से पहले याद ज़रूर दिलाओ, और कैंसल करना एक टैप में रखो। भरोसा, एक महीने के पैसों से ज़्यादा क़ीमती है।", "", s6,
          min_dur=6.0, whoosh=True, sfx=[(0.4, "pop"), (0.9, "pop_hi"), (1.4, "pop"), (1.8, "pop_hi"), (2.8, "chime"), (3.6, "ding")]),
    Scene("अभी अपना फ़ोन चेक करो, कितने फ़्री ट्रायल चुपचाप चल रहे हैं? नंबर कमेंट में लिखो। कल मिलते हैं, रेसिप्रोसिटी के साथ।", "", D.s8,
          min_dur=5.0, whoosh=True, clicks=[2.6], sfx=[(2.62, "chime")]),
]

# The Day 32 file (model v4) has no pauses (break tags ignored): line cuts found with tools/align_cuts.py, each in the
# silence between sentences; line check 8/8.
VO_CUTS = [7.35, 16.9, 25.39, 35.76, 44.64, 52.16, 61.89]

if __name__ == "__main__":
    import daily
    daily.run(32, "Endowment Effect", SCENES, "day32_endowment_effect", cuts=VO_CUTS)

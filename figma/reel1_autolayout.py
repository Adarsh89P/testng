"""Reel 1: 15 LPA vs 45 LPA Designer - Auto Layout (vertical, Hinglish, dotted style)."""
import sys, math
from engine import *
from card import *

W, H = 1080, 1920
CPS = 24  # typing chars/sec
CY = 650


def boxes_for(w=540, gap=16, pad=24, rows=1, btn="fill"):
    return card_layout((W - w) / 2, CY, w, gap=gap, pad=pad, title_rows=rows, btn_mode=btn)


def lerp_boxes(b0, b1, t):
    return {k: tuple(lerp(a, b, t) for a, b in zip(b0[k], b1[k])) if isinstance(b0[k], tuple) else b1[k] for k in b0}


def broken(rows=1):
    """Manual card: title grows but nothing below moved."""
    b = boxes_for(rows=1); b2 = boxes_for(rows=rows)
    b["title"] = b2["title"]; return b


def stage(cv, tag, lines, t, boxes, rows, a=1.0, offsets=None, tag_pop=0.0, start=0.0, label="Designer"):
    s = 1 + 0.25 * math.sin(math.pi * min(1, tag_pop)) if tag_pop < 1 else 1
    cv.pill(W / 2, 210, tag, size=32 * s, bold=True)
    chars = int(max(0, t - start) * CPS)
    cv.code_box(30, 270, W - 60, 250, lines, chars, cursor_on=(int(t * 2) % 2 == 0) or chars < sum(len(l) + 1 for l in lines))
    draw_card(cv, boxes, a=a, title_rows=rows, offsets=offsets)
    x, y, w, h = boxes["card"]
    if y + h + 20 < 1540: cv.line(W / 2, y + h + 4, W / 2, 1540)
    cv.person(W / 2, 1600, 1.0)
    cv.pill(W / 2, 1712, label, size=28)


def nchars(lines): return sum(len(l) + 1 for l in lines)
def span(lines, start=0.0): return [(start, start + nchars(lines) / CPS)]


# ------------------------------------------------------------------ scenes
L1 = ["// ek card, do designer"]
def s1(cv, t, d, st):
    stage(cv, "15 LPA", L1, t, boxes_for(), 1, a=ease(t / 1.0))

L2 = ["image.y  = 24   // drag", "title.y  = 348  // drag", "button.y = 520  // drag"]
def s2(cv, t, d, st):
    b = boxes_for()
    off = {"image": (0, 0), "title": (6, -3), "details": (-4, 5), "button": (10, 2)}
    stage(cv, "15 LPA", L2, t, b, 1, offsets=off)
    # cursor dragging the button around
    bx, by, bw, bh = b["button"]; k = (t % 2.4) / 2.4
    cv.cursor(bx + bw * 0.6 + 30 * math.sin(k * 6.28), by + bh * 0.5 + 12 * math.cos(k * 6.28))

L3 = ["title = 'Wireless Noise", "  Cancelling Headphones'"]
def s3(cv, t, d, st):
    grow = ease((t - 1.6) / 0.6)
    rows = 3 if grow > 0.5 else 1
    b = broken(rows)
    off = {"title": (6, -3), "details": (-4, 5), "button": (10, 2)}
    stage(cv, "15 LPA", L3, t, b, rows, offsets=off)
    if grow > 0.5:
        dx, dy, dw, dh = b["details"]
        pulse = 0.5 + 0.5 * math.sin(t * 6)
        cv.glow(dx + 80, dy + 14, 70, 0.6 + 0.4 * pulse)
        cv.pill(W - 150, dy + 10, "overlap!", size=28, fam=MONO, col=BAD)

L4 = ["// Shift + A", "auto-layout: vertical"]
def s4(cv, t, d, st):
    k = ease((t - 1.4) / 0.8)
    b0 = broken(3); b1 = boxes_for(gap=8, pad=12, rows=3)
    stage(cv, "45 LPA", L4, t, lerp_boxes(b0, b1, k), 3, tag_pop=t / 0.5)
    if 0 < k < 1:
        x, y, w, h = b1["card"]; cv.glow(x + w / 2, y + h / 2, 160, 0.35 * (1 - abs(2 * k - 1)))

L5 = ["auto-layout: vertical", "gap: 16", "padding: 24"]
def s5(cv, t, d, st):
    k = ease((t - 0.9) / 0.9); k2 = ease((t - 1.6) / 0.9)
    b = boxes_for(gap=lerp(8, 16, k), pad=lerp(12, 24, k2), rows=3)
    stage(cv, "45 LPA", L5, t, b, 3, start=-len(L5[0]) / CPS)
    measure_gap(cv, b, f"gap: {round(lerp(8, 16, k))}", a=min(1, t / 0.4))

L6 = ["title = 'Wireless Noise Cancelling", "  Headphones with 40h Battery", "  and Fast Charging'", "height: hug"]
def s6(cv, t, d, st):
    k = ease((t - 2.2) / 0.8)
    b = lerp_boxes(boxes_for(rows=3), boxes_for(rows=4), k)
    stage(cv, "45 LPA", L6, t, b, 4 if k > 0.3 else 3)
    if k > 0:
        x, y, w, h = b["card"]
        cv.pill(x - 70, y + h - 40, "hug", size=26, fam=MONO, col=GOOD, a=k)

L7 = ["width: fixed 270 -> 380", "button: fill container"]
def s7(cv, t, d, st):
    k = ease((t - 1.2) / 1.2) - ease((t - 3.4) / 1.0) * 0.5
    b = boxes_for(w=lerp(540, 760, k), rows=4)
    stage(cv, "45 LPA", L7, t, b, 4)
    x, y, w, h = b["card"]
    cv.cursor(x + w - 6, y + h / 2)
    cv.pill(W / 2, y + h + 50, f"width: {round(w / 2)}", size=26, fam=MONO, col=ACCENT)

L8 = ["// skill nahi, system", "follow for more figma"]
def s8(cv, t, d, st):
    b = boxes_for(w=650, rows=4)
    stage(cv, "45 LPA", L8, t, b, 4)
    cv.pill(160, 210, "15 LPA", size=26, a=0.35)


SCENES = [
    Scene("एक ही कार्ड, दो डिज़ाइनर। एक पंद्रह एल पी ए, और एक पैंतालीस एल पी ए। फर्क देखो।",
          "Ek card, do designer. 15 LPA vs 45 LPA. Fark dekho.", s1, type_spans=span(L1)),
    Scene("पंद्रह एल पी ए डिज़ाइनर, हर एलिमेंट को हाथ से खींच कर जगह पर रखता है।",
          "15 LPA designer: har element HAATH se drag karta hai.", s2, type_spans=span(L2)),
    Scene("फिर क्लाइंट ने टाइटल बदला, और पूरा कार्ड टूट गया। अब सब कुछ दोबारा खींचो।",
          "Client ne title badla... aur card TOOT gaya.", s3, type_spans=span(L3), hold=0.6),
    Scene("पैंतालीस एल पी ए डिज़ाइनर, बस शिफ्ट प्लस ए दबाता है। ऑटो लेआउट, वर्टिकल।",
          "45 LPA designer: bas SHIFT + A. Auto Layout, vertical.", s4, type_spans=span(L4), whoosh=True),
    Scene("गैप सोलह, पैडिंग चौबीस। हर एलिमेंट के बीच बराबर स्पेस, अपने आप।",
          "Gap 16, Padding 24. Har jagah EQUAL space, apne aap.", s5,
          type_spans=[(0, (len(L5[1]) + len(L5[2]) + 2) / CPS)]),
    Scene("अब टाइटल कितना भी लंबा करो, कार्ड खुद बढ़ता है। कोई ओवरलैप नहीं।",
          "Title kitna bhi lamba karo, card khud BADHTA hai.", s6, type_spans=span(L6), hold=0.4),
    Scene("और बटन फिल कंटेनर पर है, तो कार्ड चौड़ा करो, सब साथ में एडजस्ट होता है।",
          "Button = FILL. Card chauda karo, sab saath mein adjust.", s7, type_spans=span(L7), min_dur=5.0),
    Scene("फर्क टैलेंट का नहीं, सिस्टम का है। ऐसे ही फिग्मा ट्रिक्स के लिए फॉलो करो।",
          "Fark talent ka nahi, SYSTEM ka hai. Follow for Figma tricks!", s8, type_spans=span(L8), whoosh=True),
]

if __name__ == "__main__":
    out = sys.argv[1]
    print("duration", round(render(SCENES, out, W, H, cap_y=1810, voice="hf_beta"), 1), "s")

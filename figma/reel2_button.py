"""Reel 2: Figma workflow - build a button step by step (dotted style, Hinglish voice baked in)."""
import sys, math
from engine import *

W, H = 1080, 1920
CPS = 24
BX, BY = W / 2, 930          # button centre
PURPLE = (0.49, 0.36, 1.0)
LABEL = "Get Started"
STEPS = 8


def nchars(lines): return sum(len(l) + 1 for l in lines)
def span(lines, start=0.0): return [(start, start + nchars(lines) / CPS)]


def keys(cv, t, caps, y=600, at=0.3):
    """Keycap row; caps 'press' down at time `at`."""
    cv.font(MONO, 34, True)
    ws = [cv.text_w(k) + 46 for k in caps]; gap = 22
    x = W / 2 - (sum(ws) + gap * (len(ws) - 1)) / 2
    down = 1 if at <= t < at + 0.25 else 0
    for k, w in zip(caps, ws):
        if k == "+":
            cv.text(x + 6, y + 12, "+", DIM); x += w + gap; continue
        yy = y - 34 + down * 6
        cv.fill_rrect(x, yy + 8, w, 68, 14, (0.04, 0.04, 0.05))
        cv.fill_rrect(x, yy, w, 68, 14, PILL)
        cv.drrect(x, yy, w, 68, 14, spacing=6, r=1.5, a=0.8)
        cv.text(x + 23, yy + 45, k, DOT); x += w + gap


def button(cv, cx, cy, pad_v=16, pad_h=32, fill=0.0, radius=0.0, frame=1.0, label=LABEL,
           col=PURPLE, scale=1.0, txt_col=None, sel=False, a=1.0):
    """Draws the button. pad in Figma units (x2 px). fill 0..1, radius 0..1 (1 = full pill)."""
    cv.font(SANS, 44 * scale, True)
    tw = cv.text_w(label); th = 44 * scale
    w = tw + 2 * pad_h * 2 * scale; h = th + 2 * pad_v * 2 * scale
    x, y = cx - w / 2, cy - h / 2
    r = lerp(4, h / 2, radius) if radius > 0 else 2
    if fill > 0: cv.fill_rrect(x, y, w, h, r, col, fill * a)
    if frame > 0: cv.drrect(x, y, w, h, max(r, 2), spacing=6.5, r=1.8, a=frame * a * (1 - 0.6 * fill))
    tc = txt_col or tuple(lerp(d, 1.0, fill) for d in DOT)
    cv.text(cx - tw / 2, cy + th * 0.36, label, tc, a)
    if sel:
        cv.c.set_source_rgba(0.05, 0.6, 1.0, a); cv.c.set_line_width(2.5)
        cv.c.rectangle(x - 6, y - 6, w + 12, h + 12); cv.c.stroke()
        for hx, hy in [(x - 6, y - 6), (x + w + 6, y - 6), (x - 6, y + h + 6), (x + w + 6, y + h + 6)]:
            cv.c.set_source_rgba(1, 1, 1, a); cv.c.rectangle(hx - 6, hy - 6, 12, 12); cv.c.fill()
            cv.c.set_source_rgba(0.05, 0.6, 1.0, a); cv.c.rectangle(hx - 6, hy - 6, 12, 12); cv.c.stroke()
    return x, y, w, h


def stage(cv, step, title, lines, t, start=0.0, link_y=None):
    cv.pill(W / 2, 210, f"STEP {step}/{STEPS} · {title}", size=30, bold=True)
    chars = int(max(0, t - start) * CPS)
    done = chars >= nchars(lines)
    cv.code_box(30, 270, W - 60, 230, lines, chars, cursor_on=(not done) or int(t * 2) % 2 == 0)
    cv.line(W / 2, link_y or 1100, W / 2, 1540)
    cv.person(W / 2, 1600, 1.0)
    cv.pill(W / 2, 1712, "Designer", size=28)


def pad_bands(cv, x, y, w, h, pv, ph, a):
    cv.c.set_source_rgba(*ACCENT, 0.25 * a)
    for rx, ry, rw, rh in [(x, y, w, pv), (x, y + h - pv, w, pv), (x, y + pv, ph, h - 2 * pv), (x + w - ph, y + pv, ph, h - 2 * pv)]:
        cv.c.rectangle(rx, ry, rw, rh)
    cv.c.fill()


# ------------------------------------------------------------------ scenes
L1 = ["// Text tool", "press T", "type: 'Get Started'"]
def s1(cv, t, d, st):
    stage(cv, 1, "Text", L1, t)
    keys(cv, t, ["T"], at=0.6)
    n = int(max(0, t - 1.4) * 10)
    shown = LABEL[:n]
    cv.font(SANS, 44, True); tw = cv.text_w(shown)
    cv.text(BX - cv.text_w(LABEL) / 2, BY + 16, shown, DOT)
    if int(t * 3) % 2 == 0 or n < len(LABEL):
        cv.c.set_source_rgba(0.05, 0.6, 1.0, 1); cv.c.rectangle(BX - cv.text_w(LABEL) / 2 + tw + 3, BY - 26, 3, 52); cv.c.fill()

L2 = ["select text", "Shift + A   // auto layout"]
def s2(cv, t, d, st):
    stage(cv, 2, "Auto Layout", L2, t, link_y=BY + 40)
    keys(cv, t, ["Shift", "+", "A"], at=1.2)
    k = ease((t - 1.4) / 0.4)
    x, y, w, h = button(cv, BX, BY, pad_v=1, pad_h=1, frame=k, sel=t > 1.4)
    if 0 < k < 1: cv.glow(BX, BY, 180, 0.4 * (1 - k))
    if t > 1.8: cv.pill(BX, y + h + 60, "auto layout: horizontal", size=24, fam=MONO, col=GOOD)

L3 = ["padding:", "  top/bottom = 16", "  left/right = 32"]
def s3(cv, t, d, st):
    stage(cv, 3, "Padding", L3, t, link_y=BY + 80)
    kv = ease((t - 0.8) / 0.8); kh = ease((t - 1.8) / 0.8)
    pv, ph = lerp(1, 16, kv), lerp(1, 32, kh)
    x, y, w, h = button(cv, BX, BY, pad_v=pv, pad_h=ph, sel=True)
    pad_bands(cv, x, y, w, h, pv * 2, ph * 2, 1.0)
    cv.pill(BX, y - 50, f"pad: {round(pv)}", size=24, fam=MONO, col=ACCENT)
    cv.pill(x - 90, BY, f"{round(ph)}", size=24, fam=MONO, col=ACCENT)
    cv.pill(x + w + 90, BY, f"{round(ph)}", size=24, fam=MONO, col=ACCENT)

L4 = ["fill: #7C5CFF", "text: #FFFFFF"]
def s4(cv, t, d, st):
    stage(cv, 4, "Fill", L4, t, link_y=BY + 80)
    k = ease((t - 0.9) / 0.7)
    x, y, w, h = button(cv, BX, BY, fill=k, sel=True)
    cv.fill_rrect(x + w + 50, BY - 22, 44, 44, 10, PURPLE, k)
    cv.pill(x + w + 170, BY, "#7C5CFF", size=24, fam=MONO, a=max(0.001, k))

L5 = ["corner radius: 12"]
def s5(cv, t, d, st):
    stage(cv, 5, "Radius", L5, t, link_y=BY + 80)
    k = ease((t - 0.8) / 1.0)
    x, y, w, h = button(cv, BX, BY, fill=1, radius=k * 0.55, sel=True)
    cv.pill(BX, y - 50, f"radius: {round(12 * k)}", size=24, fam=MONO, col=ACCENT)

L6 = ["Ctrl + Alt + K   // Mac: Cmd+Opt+K", "name: Button/Primary"]
def s6(cv, t, d, st):
    stage(cv, 6, "Component", L6, t, link_y=BY + 80)
    keys(cv, t, ["Ctrl", "+", "Alt", "+", "K"], at=1.0)
    x, y, w, h = button(cv, BX, BY, fill=1, radius=0.55, frame=0)
    k = ease((t - 1.3) / 0.5)
    if k > 0:
        cv.c.set_source_rgba(*PURPLE, k); cv.c.set_line_width(2.5)
        cv.c.rectangle(x - 8, y - 8, w + 16, h + 16); cv.c.stroke()
        # component diamond + name
        dx, dy = x - 8, y - 40
        cv.c.move_to(dx + 10, dy - 10); cv.c.line_to(dx + 20, dy); cv.c.line_to(dx + 10, dy + 10); cv.c.line_to(dx, dy)
        cv.c.close_path(); cv.c.fill()
        cv.font(SANS, 24, True); cv.text(dx + 30, dy + 9, "Button/Primary", PURPLE, k)
        cv.glow(BX, BY, 200, 0.3 * (1 - k))

VY = [800, 960, 1120]
VARS = [("Default", PURPLE, 1.0), ("Hover", (0.60, 0.50, 1.0), 1.0), ("Pressed", (0.36, 0.25, 0.85), 0.96)]
L7 = ["add variant (+)", "  Default / Hover / Pressed"]
def variants(cv, k, hi=None):
    x0, x1 = BX - 260, BX + 260
    cv.c.save(); cv.c.set_dash([10, 7]); cv.c.set_source_rgba(*PURPLE, 0.9 * max(k[0], 0.01)); cv.c.set_line_width(2)
    cv.rrect_path(x0, VY[0] - 90, x1 - x0, VY[2] - VY[0] + 180, 16); cv.c.stroke(); cv.c.restore()
    for i, ((name, col, sc), kk) in enumerate(zip(VARS, k)):
        if kk <= 0: continue
        button(cv, BX + 40, VY[i], fill=1, radius=0.55, frame=0, col=col, scale=sc, a=kk)
        cv.pill(x0 - 10, VY[i], name, size=24, fam=MONO, col=(0.72, 0.62, 1.0) if hi == i else DOT, a=max(kk, 0.85))

def s7(cv, t, d, st):
    stage(cv, 7, "Variants", L7, t, link_y=VY[2] + 90)
    variants(cv, [1, ease((t - 1.2) / 0.5), ease((t - 2.2) / 0.5)])

L8 = ["prototype:", "  while hovering -> Hover", "  animation: smart animate"]
def s8(cv, t, d, st):
    stage(cv, 8, "Prototype", L8, t, link_y=VY[2] + 90)
    hover = (t % 3.0) > 1.5 and t > 2.0
    variants(cv, [1, 0.35, 0.35], hi=1 if hover else 0)
    # live preview: cursor moves onto default button and it turns into hover
    cx = lerp(BX + 420, BX + 80, ease(((t % 3.0) - 0.6) / 0.8)) if t > 2.0 else BX + 420
    if hover:
        cv.fill_rrect(BX - 220, VY[0] - 60, 520, 120, 10, BG)
        button(cv, BX + 40, VY[0], fill=1, radius=0.55, frame=0, col=VARS[1][1], scale=1.03)
    cv.cursor(cx, VY[0])
    # connector noodle between variants
    cv.c.set_source_rgba(0.05, 0.6, 1.0, 0.9); cv.c.set_line_width(3)
    cv.c.move_to(BX + 300, VY[0]); cv.c.curve_to(BX + 390, VY[0], BX + 390, VY[1], BX + 300, VY[1]); cv.c.stroke()
    cv.c.arc(BX + 300, VY[0], 7, 0, 6.3); cv.c.fill()

L9 = ["// button ready", "follow for more figma workflows"]
def s9(cv, t, d, st):
    cv.pill(W / 2, 210, "DONE · Button/Primary", size=30, bold=True)
    cv.code_box(30, 270, W - 60, 230, L9, int(t * CPS), cursor_on=int(t * 2) % 2 == 0)
    hover = (t % 2.0) > 1.0
    button(cv, BX, BY, fill=1, radius=0.55, frame=0, col=VARS[1][1] if hover else PURPLE, scale=1.03 if hover else 1)
    cv.line(W / 2, BY + 80, W / 2, 1540); cv.person(W / 2, 1600, 1.0); cv.pill(W / 2, 1712, "Designer", size=28)


SCENES = [
    Scene("फिग्मा में प्रो लेवल बटन बनाओ, सिर्फ आठ स्टेप में। स्टेप वन, टी दबाओ और टेक्स्ट लिखो, गेट स्टार्टेड।",
          "Figma mein PRO button, sirf 8 steps. Step 1: T dabao, text likho.", s1, type_spans=span(L1), min_dur=5.5),
    Scene("स्टेप टू, टेक्स्ट सेलेक्ट करो और शिफ्ट प्लस ए दबाओ। अब ये ऑटो लेआउट फ्रेम बन गया।",
          "Step 2: text select karo, SHIFT + A. Auto Layout frame ready.", s2, type_spans=span(L2)),
    Scene("स्टेप थ्री, पैडिंग। ऊपर नीचे सोलह, और लेफ्ट राइट बत्तीस।",
          "Step 3: Padding. Upar-neeche 16, left-right 32.", s3, type_spans=span(L3), min_dur=4.5),
    Scene("स्टेप फोर, फ्रेम को कलर दो, और टेक्स्ट को व्हाइट करो।",
          "Step 4: Frame ko FILL color do, text white.", s4, type_spans=span(L4)),
    Scene("स्टेप फाइव, कॉर्नर रेडियस बारह। बटन अब सॉफ्ट और मॉडर्न लगता है।",
          "Step 5: Corner radius 12. Soft aur modern.", s5, type_spans=span(L5)),
    Scene("स्टेप सिक्स, कंट्रोल ऑल्ट के दबाकर इसे कंपोनेंट बनाओ। मैक पर कमांड ऑप्शन के।",
          "Step 6: Ctrl + Alt + K. Ab ye COMPONENT hai.", s6, type_spans=span(L6), whoosh=True),
    Scene("स्टेप सेवन, प्लस पर क्लिक करके वेरिएंट्स बनाओ। डिफॉल्ट, होवर, और प्रेस्ड।",
          "Step 7: Variants banao: Default, Hover, Pressed.", s7, type_spans=span(L7), min_dur=4.5),
    Scene("स्टेप एट, प्रोटोटाइप में, वाइल होवरिंग, चेंज टू होवर, और स्मार्ट एनिमेट। अब बटन असली बटन जैसा रिएक्ट करता है।",
          "Step 8: Prototype: While hovering, Change to Hover, Smart Animate.", s8, type_spans=span(L8), min_dur=6.5),
    Scene("बस, आपका प्रो बटन तैयार है। ऐसे ही फिग्मा वर्कफ्लोज़ के लिए फॉलो करो।",
          "Button READY! Follow for more Figma workflows.", s9, type_spans=span(L9), whoosh=True),
]

if __name__ == "__main__":
    print("duration", round(render(SCENES, sys.argv[1], W, H, cap_y=1810), 1), "s")

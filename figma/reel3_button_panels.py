"""Reel 3: Figma button workflow with real-looking left/right panel click-through (vertical, Hinglish VO baked in).

Intro uses the reference reel's 15 LPA | 45 LPA split + dust 'crash'; then the Figma dark UI where the cursor
clicks tools, layers and Design/Prototype fields while the camera zooms like a screen recording.
"""
import sys
from engine import *
from figma_ui import *

W, H = 1080, 1920
PURPLE_HEX = "7C5CFF"
ui = UI()


def typed(s, t, t0, cps=9):
    return s[:max(0, min(len(s), int((t - t0) * cps)))]


def resolve(target, R):
    if isinstance(target, tuple) and len(target) == 2 and not isinstance(target[0], str): return target
    name, dx, dy = (target + (0, 0))[:3] if isinstance(target, tuple) else (target, 0, 0)
    r = R.get(name)
    return centre(r, dx, dy) if r else (UW / 2, UH / 2)


def cursor_at(t, st, pts):
    """pts [(t_arrive, target, click)] -> eased cursor; start = last position of previous scene."""
    start = st.setdefault("cur0", (UW / 2, UH / 2))
    prev_t, prev_p = 0.0, start
    for ta, tg, _ in pts:
        p = resolve(tg, ui.R)
        if t < ta:
            ts = max(prev_t, ta - 0.8)
            if t < ts: return prev_p
            e = ease((t - ts) / (ta - ts)); return (lerp(prev_p[0], p[0], e), lerp(prev_p[1], p[1], e))
        prev_t, prev_p = ta, p
    st["cur_end"] = prev_p
    return prev_p


def cam_at(t, keys):
    """keys [(t, target|'full', zoom)] resolved through ui.R."""
    res = [(kt, *(FULL if tg == "full" else (*resolve(tg, ui.R), z))) for kt, tg, z in keys]
    return Cam(res).at(t)


def header(cv, step, title, path):
    cv.pill(W / 2, 200, f"STEP {step}/8 · {title}", size=30, bold=True)
    cv.font(MONO, 24); tw = cv.text_w(path); cv.text(W / 2 - tw / 2, 262, path, DIM)


def keycaps(cv, t, caps, at, y=SY + UH - 80):
    if t < at - 0.4 or t > at + 1.6: return
    a = min(1, (t - at + 0.4) / 0.3) * min(1, (at + 1.6 - t) / 0.3)
    cv.font(MONO, 32, True)
    ws = [cv.text_w(k) + 44 for k in caps]; gap = 18
    x = W / 2 - (sum(ws) + gap * (len(caps) - 1)) / 2
    down = 6 if at <= t < at + 0.25 else 0
    for k, w in zip(caps, ws):
        if k == "+": cv.text(x + 8, y + 10, "+", DIM, a); x += w + gap; continue
        cv.fill_rrect(x, y - 30 + down, w, 64, 12, (0.08, 0.08, 0.09), a)
        cv.drrect(x, y - 30 + down, w, 64, 12, spacing=6, r=1.5, a=0.9 * a)
        cv.text(x + 22, y + 12 + down, k, DOT, a); x += w + gap


def screen(cv, t, st, draw_ui, cam_keys, cur_pts, step, title, path, caps=None):
    header(cv, step, title, path)
    pos = cursor_at(t, st, cur_pts)
    clicks = [ta for ta, _, c in cur_pts if c]
    frame_ui(cv, t, ui, Cam([(0, *cam_at(t, cam_keys))]), draw_ui, pos, clicks)
    if caps: keycaps(cv, t, *caps)


def clicks_of(pts): return [ta for ta, _, c in pts if c]


# ------------------------------------------------------------------ 0. hook: 15 vs 45 split
def s0(cv, t, d, st):
    lx, rx, cy = W * 0.27, W * 0.73, 900
    for yy in range(420, 1400, 14): cv._dot(W / 2, yy, 1.4, DIM, 0.8)
    cv.font(SANS, 54, True)
    cv.text(lx - cv.text_w("15 LPA") / 2, 330, "15 LPA", DOT if t < 3.2 else DIM)
    cv.text(rx - cv.text_w("45 LPA") / 2, 330, "45 LPA", DOT if t >= 3.2 else DIM)
    # left: hand-made box, text off-centre -> dissolves
    pts = st.setdefault("pts", sample_rrect(lx - 150, cy - 50, 300, 100, 520))
    k = ease((t - 2.2) / 1.4)
    dissolve(cv, pts, k)
    cv.font(SANS, 32, True); cv.text(lx - 112, cy + 18, "Get Started", DOT, max(0, 1 - k * 1.5))
    if k > 0.2: white_pill(cv, lx, cy + 140, "breaks", 26)
    # right: clean pill button
    cv.fill_rrect(rx - 150, cy - 46, 300, 92, 46, BTN)
    cv.font(SANS, 32, True); cv.text(rx - cv.text_w("Get Started") / 2, cy + 12, "Get Started", (1, 1, 1))
    cv.glow(rx, cy, 220, 0.18 + 0.08 * math.sin(t * 3))
    cv.pill(rx, cy + 140, "auto layout + component", size=22, fam=MONO)


# ------------------------------------------------------------------ 1. text tool
P1 = [(1.0, "tool_text", True), (2.0, (CX - 90, CY), True), (4.6, (CX + 60, CY + 120), False)]
def s1(cv, t, d, st):
    typing = t >= 2.2
    txt = typed("Get Started", t, 2.3)
    def draw(cv):
        ui.toolbar(cv, "text" if 1.0 <= t < 4.0 else "move")
        ui.left(cv, [("Get Started", "text", 0)] if typing else [], selected=0 if typing else None)
        ui.right(cv, "text" if typing else "none", {})
        def content(cv):
            if not typing: return
            cv.font(SANS, 30, True); full = cv.text_w("Get Started"); x0 = CX - full / 2
            cv.text(x0, CY + 11, txt, (1, 1, 1))
            if int(t * 3) % 2 == 0 or len(txt) < 11:
                cv.c.set_source_rgb(*F_BLUE); cv.c.rectangle(x0 + cv.text_w(txt) + 2, CY - 18, 2.5, 38); cv.c.fill()
            if len(txt) == 11 and t > 4.0: selection(cv, x0 - 4, CY - 22, full + 8, 44)
            ui.R["btn"] = (x0, CY - 22, full, 44)
        ui.canvas(cv, content)
    screen(cv, t, st, draw, [(0, "full", 1), (1.6, (CX, CY), 1.3)], P1, 1, "Text", "Toolbar › Text tool (T)")


# ------------------------------------------------------------------ 2. Shift+A
P2 = [(0.8, "btn", True), (3.0, "pad_h", False), (4.6, "layer0", False)]
def s2(cv, t, d, st):
    al = t >= 1.7
    def draw(cv):
        ui.toolbar(cv)
        ui.left(cv, [("Frame 1", "al", 0), ("Get Started", "text", 1)] if al else [("Get Started", "text", 0)], selected=0)
        ui.right(cv, "frame" if al else "text", {"w": "Hug", "h": "Hug", "pad_h": "0", "pad_v": "0"})
        ui.canvas(cv, lambda cv: draw_button(cv, ui, frame=al, sel="Hug × Hug" if al else True))
    screen(cv, t, st, draw, [(0, (CX, CY), 1.3), (1.9, "full", 1.0), (2.8, "gap", 1.4), (4.2, "layer0", 1.4)],
           P2, 2, "Auto Layout", "Select text › Shift + A", caps=(["Shift", "+", "A"], 1.6))


# ------------------------------------------------------------------ 3. padding
P3 = [(0.9, "pad_h", True), (2.4, "pad_v", True), (4.0, "btn", False)]
def s3(cv, t, d, st):
    ph = typed("32", t, 1.1, 6) or "0"; pv = typed("16", t, 2.6, 6) or "0"
    act = "pad_h" if 0.9 <= t < 2.4 else "pad_v" if 2.4 <= t < 3.4 else None
    def draw(cv):
        ui.toolbar(cv)
        ui.left(cv, [("Frame 1", "al", 0), ("Get Started", "text", 1)], selected=0)
        ui.right(cv, "frame", {"pad_h": ph, "pad_v": pv}, active=act)
        def content(cv):
            x, y, w, h = draw_button(cv, ui, pad_h=int(ph), pad_v=int(pv), sel="Hug × Hug")
            cv.c.set_source_rgba(*ACCENT, 0.25)
            pv_, ph_ = int(pv), int(ph)
            for r in [(x, y, w, pv_), (x, y + h - pv_, w, pv_), (x, y + pv_, ph_, h - 2 * pv_), (x + w - ph_, y + pv_, ph_, h - 2 * pv_)]:
                cv.c.rectangle(*r)
            cv.c.fill()
        ui.canvas(cv, content)
    screen(cv, t, st, draw, [(0, "full", 1), (0.6, "pad_h", 1.4), (3.4, "pad_h", 1.4), (4.2, (CX, CY), 1.3)],
           P3, 3, "Padding", "Right panel › Auto layout › Padding")


# ------------------------------------------------------------------ 4. fill
P4 = [(1.0, "fill_add", True), (2.0, "fill_hex", True), (4.2, "btn", False)]
def s4(cv, t, d, st):
    has = t >= 1.1
    hx = typed(PURPLE_HEX, t, 2.3, 9)
    done = len(hx) == 6 and t > 3.1
    val = (hx if 2.0 <= t < 3.1 else ("D9D9D9" if not done else PURPLE_HEX)) if has else None
    rgb = BTN if done else (0.85, 0.85, 0.85)
    def draw(cv):
        ui.toolbar(cv)
        ui.left(cv, [("Frame 1", "al", 0), ("Get Started", "text", 1)], selected=0)
        ui.right(cv, "frame", {"pad_h": "32", "pad_v": "16", "fill": val, "fill_rgb": rgb}, active="fill_hex" if 2.0 <= t < 3.1 else None)
        ui.canvas(cv, lambda cv: draw_button(cv, ui, pad_h=32, pad_v=16, fill=rgb if has else None,
                                             text_col=(1, 1, 1) if done or not has else (0.1, 0.1, 0.1), sel="Hug × Hug"))
    screen(cv, t, st, draw, [(0, "full", 1), (0.6, "fill_add", 1.4), (3.3, "fill_add", 1.4), (4.0, (CX, CY), 1.3)],
           P4, 4, "Fill", "Right panel › Fill › +")


# ------------------------------------------------------------------ 5. radius
P5 = [(0.9, "radius", True), (3.2, "btn", False)]
def s5(cv, t, d, st):
    rv = typed("12", t, 1.1, 6) or "0"
    def draw(cv):
        ui.toolbar(cv)
        ui.left(cv, [("Frame 1", "al", 0), ("Get Started", "text", 1)], selected=0)
        ui.right(cv, "frame", {"pad_h": "32", "pad_v": "16", "fill": PURPLE_HEX, "fill_rgb": BTN, "radius": rv},
                 active="radius" if 0.9 <= t < 2.0 else None)
        ui.canvas(cv, lambda cv: draw_button(cv, ui, pad_h=32, pad_v=16, fill=BTN, radius=int(rv), sel="Hug × Hug"))
    screen(cv, t, st, draw, [(0, "full", 1), (0.5, "radius", 1.4), (2.1, "radius", 1.4), (2.8, (CX, CY), 1.4)],
           P5, 5, "Corner radius", "Right panel › Frame › Radius")


# ------------------------------------------------------------------ 6. component + rename
P6 = [(0.6, "btn", True), (2.4, "layer0", True), (2.55, "layer0", True), (4.6, "layer0", False)]
def s6(cv, t, d, st):
    comp = t >= 1.3
    name = typed("Button/Primary", t, 2.8, 11)
    renaming = 2.55 <= t < 4.3
    final = name if t >= 2.8 else "Frame 1"
    def draw(cv):
        ui.toolbar(cv)
        layers = [(final, "comp" if comp else "al", 0), ("Get Started", "text", 1)]
        ui.left(cv, layers, selected=0, rename=(0, name) if renaming else None)
        ui.right(cv, "component" if comp else "frame",
                 {"comp_name": final, "pad_h": "32", "pad_v": "16", "fill": PURPLE_HEX, "fill_rgb": BTN, "radius": "12"})
        def content(cv):
            x, y, w, h = draw_button(cv, ui, pad_h=32, pad_v=16, fill=BTN, radius=12, sel=not comp)
            if comp:
                selection(cv, x, y, w, h, col=F_PURPLE)
                ui.icon_comp(cv, x, y - 30, F_PURPLE); cv.font(SANS, 16, True); cv.text(x + 22, y - 16, final, F_PURPLE)
        ui.canvas(cv, content)
    screen(cv, t, st, draw, [(0, (CX, CY), 1.3), (2.0, "layer0", 1.4), (4.4, "layer0", 1.4), (5.0, "full", 1.0)],
           P6, 6, "Component", "Ctrl+Alt+K › Layers › double-click to rename", caps=(["Ctrl", "+", "Alt", "+", "K"], 1.2))


# ------------------------------------------------------------------ 7. variants
VAR_Y = [CY - 130, CY, CY + 130]
VAR = [("Default", BTN), ("Hover", BTN_HOVER), ("Pressed", BTN_PRESS)]
def variant_set(cv, n, hover_default=False):
    if n > 1:
        cv.c.save(); cv.c.set_dash([8, 6]); cv.c.set_source_rgb(*F_PURPLE); cv.c.set_line_width(2)
        top, bot = VAR_Y[0] - 70, VAR_Y[n - 1] + 60
        cv.rrect_path(CX - 165, top, 330, bot - top, 10); cv.c.stroke(); cv.c.restore()
        ui.R["set"] = (CX - 165, top, 330, bot - top)
    for i in range(n):
        nm, col = VAR[i]
        if i == 0 and hover_default: col = BTN_HOVER
        cy = VAR_Y[i] if n > 1 else CY
        draw_button(cv, ui, cy=cy, pad_h=32, pad_v=16, fill=col, radius=12, name=f"var{i}",
                    scale=1.03 if (i == 0 and hover_default) else 1.0)
        if n > 1:
            cv.font(SANS, 15, True); cv.text(CX - 150, cy - 40, f"State={nm}", F_PURPLE)


P7 = [(1.0, "add_variant", True), (2.0, "add_variant", True), (4.4, "set", False)]
def s7(cv, t, d, st):
    n = 1 + (t >= 1.1) + (t >= 2.1)
    def draw(cv):
        ui.toolbar(cv)
        lay = [("Button/Primary", "comp", 0), ("Get Started", "text", 1)] if n == 1 else \
              [("Button", "set", 0)] + [(f"State={VAR[i][0]}", "comp", 1) for i in range(n)]
        ui.left(cv, lay, selected=0)
        ui.right(cv, "set", {"comp_name": "Button" if n > 1 else "Button/Primary", "variants": True,
                             "state": "Default", "pad_h": "32", "pad_v": "16", "fill": PURPLE_HEX, "fill_rgb": BTN, "radius": "12"})
        ui.canvas(cv, lambda cv: variant_set(cv, n))
    screen(cv, t, st, draw, [(0, "full", 1), (0.6, "add_variant", 1.4), (2.6, "add_variant", 1.4), (3.4, (CX, CY), 1.3)],
           P7, 7, "Variants", "Right panel › Properties › +")


# ------------------------------------------------------------------ 8. prototype
P8 = [(0.8, "tab_proto", True), (1.6, "inter_add", True), (2.4, "trigger", True), (3.2, "menu_While hovering", True),
      (4.6, (CX + 260, VAR_Y[0]), False), (5.4, ("var0", 30, 0), False)]
def s8(cv, t, d, st):
    tab = "proto" if t >= 0.9 else "design"
    inter = t >= 1.7
    menu = 2.5 <= t < 3.3
    trig = "While hovering" if t >= 3.3 else "On click"
    hover = t >= 5.4
    def draw(cv):
        ui.toolbar(cv)
        ui.left(cv, [("Button", "set", 0)] + [(f"State={v[0]}", "comp", 1) for v in VAR], selected=1)
        ui.right(cv, "set", {"comp_name": "Button", "variants": True, "state": "Default", "pad_h": "32", "pad_v": "16",
                             "fill": PURPLE_HEX, "fill_rgb": BTN, "radius": "12",
                             "inter": inter, "trigger": trig, "dest": "Hover", "menu": menu,
                             "menu_hi": "While hovering" if t > 2.9 else None}, tab=tab, active="trigger" if menu else None)
        def content(cv):
            variant_set(cv, 3, hover_default=hover)
            if inter:
                cv.c.set_source_rgb(*F_BLUE); cv.c.set_line_width(3)
                x0 = CX + 140
                cv.c.move_to(x0, VAR_Y[0]); cv.c.curve_to(x0 + 70, VAR_Y[0], x0 + 70, VAR_Y[1], x0 + 8, VAR_Y[1]); cv.c.stroke()
                cv.c.arc(x0, VAR_Y[0], 6, 0, 6.3); cv.c.fill()
                cv.c.move_to(x0 + 8, VAR_Y[1] - 7); cv.c.line_to(x0, VAR_Y[1]); cv.c.line_to(x0 + 8, VAR_Y[1] + 7); cv.c.fill()
        ui.canvas(cv, content)
    screen(cv, t, st, draw, [(0, "full", 1), (0.5, "tab_proto", 1.4), (1.4, "inter_row", 1.4), (3.8, "inter_row", 1.4),
                             (4.6, (CX, CY), 1.4)], P8, 8, "Prototype", "Prototype tab › Interaction › While hovering")


# ------------------------------------------------------------------ 9. outro
def s9(cv, t, d, st):
    cy = 880; hov = (t % 2.0) > 1.0
    cv.font(SANS, 54, True); cv.text(W / 2 - cv.text_w("45 LPA") / 2, 330, "45 LPA", DOT)
    for yy in range(420, 1400, 14): cv._dot(W / 2 - 330, yy, 1.4, DIM, 0.5)
    swarm(cv, t, 120, 1100, 840, 360, n=160, a=0.6)
    col = BTN_HOVER if hov else BTN; s = 1.04 if hov else 1.0
    cv.fill_rrect(W / 2 - 160 * s, cy - 48 * s, 320 * s, 96 * s, 22, col)
    cv.font(SANS, 34, True); cv.text(W / 2 - cv.text_w("Get Started") / 2, cy + 12, "Get Started", (1, 1, 1))
    cv.glow(W / 2, cy, 240, 0.2)
    white_pill(cv, W / 2, cy + 150, "Button/Primary · 3 variants", 24)
    cv.cursor(W / 2 + (40 if hov else 260), cy + (10 if hov else 120))


SCENES = [
    Scene("पंद्रह एल पी ए डिज़ाइनर बटन ऐसे बनाता है, और पैंतालीस एल पी ए ऐसे। चलो फिग्मा में स्टेप बाय स्टेप देखते हैं।",
          "15 LPA vs 45 LPA button. Figma mein step by step dekho.", s0, min_dur=6.0, whoosh=True),
    Scene("स्टेप वन। टूलबार में टेक्स्ट टूल पर क्लिक करो, फिर कैनवास पर क्लिक करके लिखो, गेट स्टार्टेड।",
          "Step 1: Toolbar mein TEXT tool, canvas pe click, likho Get Started.", s1, min_dur=5.4,
          clicks=clicks_of(P1), type_spans=[(2.3, 3.5)]),
    Scene("स्टेप टू। टेक्स्ट सेलेक्ट करके शिफ्ट प्लस ए। राइट पैनल में ऑटो लेआउट सेक्शन आ गया, और लेफ्ट पैनल में फ्रेम वन।",
          "Step 2: SHIFT + A. Right panel mein Auto Layout, left mein Frame 1.", s2, min_dur=5.6, clicks=clicks_of(P2) + [1.6]),
    Scene("स्टेप थ्री। राइट पैनल में पैडिंग डालो। हॉरिज़ॉन्टल बत्तीस, और वर्टिकल सोलह।",
          "Step 3: Padding: horizontal 32, vertical 16.", s3, min_dur=5.0, clicks=clicks_of(P3), type_spans=[(1.1, 1.5), (2.6, 3.0)]),
    Scene("स्टेप फोर। फिल में प्लस पर क्लिक करो, और अपना ब्रांड कलर डालो।",
          "Step 4: Fill mein + click, brand color daalo.", s4, min_dur=5.0, clicks=clicks_of(P4), type_spans=[(2.3, 3.0)]),
    Scene("स्टेप फाइव। कॉर्नर रेडियस में बारह लिखो।",
          "Step 5: Corner radius 12.", s5, min_dur=3.8, clicks=clicks_of(P5), type_spans=[(1.1, 1.5)]),
    Scene("स्टेप सिक्स। कंट्रोल ऑल्ट के से कंपोनेंट बनाओ। फिर लेफ्ट पैनल में डबल क्लिक करके नाम रखो, बटन स्लैश प्राइमरी।",
          "Step 6: Ctrl+Alt+K = Component. Layer rename: Button/Primary.", s6, min_dur=5.6,
          clicks=clicks_of(P6) + [1.2], type_spans=[(2.8, 4.1)], whoosh=True),
    Scene("स्टेप सेवन। राइट पैनल में प्लस से वेरिएंट्स जोड़ो। डिफॉल्ट, होवर, और प्रेस्ड।",
          "Step 7: + se Variants: Default, Hover, Pressed.", s7, min_dur=5.0, clicks=clicks_of(P7)),
    Scene("स्टेप एट। प्रोटोटाइप टैब में इंटरैक्शन जोड़ो, और ऑन क्लिक को बदलो, वाइल होवरिंग। अब होवर करो, बटन रिएक्ट करता है।",
          "Step 8: Prototype: While hovering → Hover. Ab button REACT karta hai.", s8, min_dur=6.6, clicks=clicks_of(P8)),
    Scene("बस, आठ स्टेप में प्रो बटन तैयार। ऐसे ही फिग्मा वर्कफ्लोज़ के लिए फॉलो करो।",
          "8 steps, PRO button ready. Follow for Figma workflows!", s9, min_dur=4.5, whoosh=True),
]


def carry_cursor(scenes):
    """Each scene's cursor starts where the previous one ended."""
    wrapped = []
    for s in scenes:
        def mk(fn):
            def d(cv, t, dur, st):
                if st.get("_fn") is not fn:
                    st["_fn"] = fn
                    if "cur_end" in st: st["cur0"] = st.pop("cur_end")
                fn(cv, t, dur, st)
            return d
        s.draw = mk(s.draw); wrapped.append(s)
    return wrapped


if __name__ == "__main__":
    print("duration", round(render(carry_cursor(SCENES), sys.argv[1], W, H, cap_y=1800), 1), "s")

"""Figma dark-mode editor mock (toolbar, Layers panel, canvas, Design/Prototype panel) for vertical reels.

The UI is drawn in its own coordinate space (UW x UH) and mapped onto the screen through a camera,
so scenes can zoom into a panel like a screen recording. Every interactive control records its rect
in `ui.R[name]` while drawing, and the cursor aims at those rects.
"""
import math
from dots import *

UW, UH = 1080, 1360           # UI space
SX, SY = 0, 290               # where the UI window sits on the 1080x1920 screen
TB, LP, RP = 58, 280, 340     # toolbar height, left panel width, right panel width

F_BG = (0.17, 0.17, 0.17)     # panel bg #2C2C2C
F_CANVAS = (0.118, 0.118, 0.118)
F_LINE = (0.27, 0.27, 0.27)
F_TXT = (1, 1, 1)
F_SUB = (0.70, 0.70, 0.70)
F_FIELD = (0.22, 0.22, 0.22)
F_BLUE = (0.05, 0.60, 1.0)
F_PURPLE = (0.59, 0.28, 1.0)
F_SEL = (0.10, 0.30, 0.50)
BTN = (0.49, 0.36, 1.0)
BTN_HOVER = (0.60, 0.50, 1.0)
BTN_PRESS = (0.36, 0.25, 0.85)


class UI:
    def __init__(self):
        self.R = {}

    # --------------------------------------------------------------- primitives
    def t(self, cv, x, y, s, size=19, col=F_TXT, bold=False, fam=SANS):
        cv.font(fam, size, bold); cv.text(x, y, s, col); return cv.text_w(s)

    def field(self, cv, name, x, y, w, label, value, active=False, h=38):
        cv.fill_rrect(x, y, w, h, 6, F_FIELD)
        if active:
            cv.rrect_path(x, y, w, h, 6); cv.c.set_source_rgb(*F_BLUE); cv.c.set_line_width(2); cv.c.stroke()
        lw = 0
        if label: lw = self.t(cv, x + 10, y + 25, label, 16, F_SUB) + 10
        self.t(cv, x + 10 + lw, y + 25, value, 18, F_TXT)
        if active and int(cv._now * 2.5) % 2 == 0:
            cv.font(SANS, 18); vx = x + 10 + lw + cv.text_w(value) + 2
            cv.c.set_source_rgb(1, 1, 1); cv.c.rectangle(vx, y + 9, 2, 20); cv.c.fill()
        self.R[name] = (x, y, w, h)

    def section(self, cv, x, y, title, plus=None):
        cv.line(x - 16, y - 14, x - 16 + RP, y - 14, F_LINE, 1)
        self.t(cv, x, y + 12, title, 18, F_TXT, True)
        if plus:
            self.t(cv, x + RP - 60, y + 14, "+", 26, F_SUB); self.R[plus] = (x + RP - 70, y - 10, 36, 36)
        return y + 36

    def icon_frame(self, cv, x, y, col):
        cv.c.set_source_rgb(*col); cv.c.set_line_width(2)
        for a in (4, 12):
            cv.c.move_to(x + a, y); cv.c.line_to(x + a, y + 16); cv.c.move_to(x, y + a); cv.c.line_to(x + 16, y + a)
        cv.c.stroke()

    def icon_al(self, cv, x, y, col):
        cv.c.set_source_rgb(*col)
        for i in range(3): cv.c.rectangle(x + 2, y + 1 + i * 6, 12, 3)
        cv.c.fill()

    def icon_comp(self, cv, x, y, col, size=8):
        c = cv.c; c.set_source_rgb(*col); cx, cy = x + 8, y + 8
        for dx, dy in [(0, -5), (5, 0), (0, 5), (-5, 0)]:
            c.move_to(cx + dx, cy + dy - 3); c.line_to(cx + dx + 3, cy + dy); c.line_to(cx + dx, cy + dy + 3)
            c.line_to(cx + dx - 3, cy + dy); c.close_path()
        c.fill()

    def icon_set(self, cv, x, y, col):
        cv.c.save(); cv.c.set_dash([3, 2]); cv.c.set_source_rgb(*col); cv.c.set_line_width(1.6)
        cv.c.rectangle(x, y, 16, 16); cv.c.stroke(); cv.c.restore(); self.icon_comp(cv, x, y, col)

    # --------------------------------------------------------------- regions
    def toolbar(self, cv, tool="move"):
        cv.c.set_source_rgb(*F_BG); cv.c.rectangle(0, 0, UW, TB); cv.c.fill()
        cv.line(0, TB, UW, TB, F_LINE, 1)
        tools = [("move", "▲"), ("frame", "#"), ("rect", "□"), ("pen", "✒"), ("text", "T"), ("hand", "✋"), ("comment", "◯")]
        x = 16
        for name, g in tools:
            if name == tool: cv.fill_rrect(x, 10, 40, 38, 7, F_BLUE)
            if name == "move":
                c = cv.c; c.set_source_rgb(1, 1, 1); c.move_to(x + 14, y0 := 18); c.line_to(x + 14, 40)
                c.line_to(x + 19, 34); c.line_to(x + 23, 42); c.line_to(x + 26, 40); c.line_to(x + 22, 33); c.line_to(x + 28, 33)
                c.close_path(); c.fill()
            elif name == "frame": self.icon_frame(cv, x + 12, 21, (1, 1, 1))
            elif name == "text": self.t(cv, x + 12, 38, "T", 22, (1, 1, 1), True)
            elif name == "rect":
                cv.c.set_source_rgb(1, 1, 1); cv.c.set_line_width(2); cv.c.rectangle(x + 12, 21, 16, 16); cv.c.stroke()
            elif name == "pen":
                cv.c.set_source_rgb(1, 1, 1); cv.c.set_line_width(2); cv.c.move_to(x + 12, 38); cv.c.line_to(x + 28, 22); cv.c.stroke()
            elif name == "hand":
                cv.c.new_path(); cv.c.set_source_rgb(1, 1, 1); cv.c.arc(x + 20, 30, 8, 0, 6.3); cv.c.set_line_width(2); cv.c.stroke()
            else:
                cv.c.new_path(); cv.c.set_source_rgb(1, 1, 1); cv.c.set_line_width(2); cv.c.arc(x + 20, 29, 9, 0, 6.3); cv.c.stroke()
            self.R["tool_" + name] = (x, 10, 40, 38); x += 50
        self.t(cv, UW / 2 - 70, 36, "Button Design", 18, F_TXT, True)
        cv.c.set_source_rgb(1, 1, 1); cv.c.move_to(UW - 150, 20); cv.c.line_to(UW - 150, 40); cv.c.line_to(UW - 134, 30)
        cv.c.close_path(); cv.c.fill(); self.R["play"] = (UW - 160, 12, 36, 36)
        cv.fill_rrect(UW - 110, 12, 94, 36, 7, F_BLUE); self.t(cv, UW - 88, 37, "Share", 17, (1, 1, 1), True)

    def left(self, cv, layers, selected=None, rename=None):
        cv.c.set_source_rgb(*F_BG); cv.c.rectangle(0, TB, LP, UH - TB); cv.c.fill()
        cv.line(LP, TB, LP, UH, F_LINE, 1)
        self.t(cv, 18, TB + 34, "Layers", 18, F_TXT, True); self.t(cv, 100, TB + 34, "Assets", 18, F_SUB)
        cv.line(0, TB + 54, LP, TB + 54, F_LINE, 1)
        self.t(cv, 18, TB + 86, "Page 1", 17, F_SUB)
        cv.line(0, TB + 106, LP, TB + 106, F_LINE, 1)
        y = TB + 120
        for i, (name, kind, depth) in enumerate(layers):
            if name == selected or i == selected:
                cv.c.set_source_rgb(*F_SEL); cv.c.rectangle(0, y, LP, 40); cv.c.fill()
            x = 18 + depth * 22
            col = F_PURPLE if kind in ("comp", "set") else F_SUB
            if kind == "text": self.t(cv, x + 2, y + 27, "T", 18, col, True)
            elif kind == "al": self.icon_al(cv, x, y + 12, col)
            elif kind == "frame": self.icon_frame(cv, x, y + 12, col)
            elif kind == "comp": self.icon_comp(cv, x, y + 12, col)
            elif kind == "set": self.icon_set(cv, x, y + 12, col)
            shown = name if rename is None or i != rename[0] else rename[1]
            tc = F_PURPLE if kind in ("comp", "set") else F_TXT
            if rename is not None and i == rename[0]:
                cv.fill_rrect(x + 26, y + 6, LP - x - 40, 28, 4, F_CANVAS)
                cv.rrect_path(x + 26, y + 6, LP - x - 40, 28, 4); cv.c.set_source_rgb(*F_BLUE); cv.c.set_line_width(2); cv.c.stroke()
            self.t(cv, x + 32, y + 27, shown, 18, tc)
            self.R[f"layer{i}"] = (0, y, LP, 40); y += 40

    def right(self, cv, mode, v, tab="design", active=None):
        """mode: none|text|frame|component|set. v: dict of values. active: name of field being edited."""
        x0 = UW - RP
        cv.c.set_source_rgb(*F_BG); cv.c.rectangle(x0, TB, RP, UH - TB); cv.c.fill()
        cv.line(x0, TB, x0, UH, F_LINE, 1)
        self.t(cv, x0 + 18, TB + 34, "Design", 18, F_TXT if tab == "design" else F_SUB, True)
        w = self.t(cv, x0 + 110, TB + 34, "Prototype", 18, F_TXT if tab == "proto" else F_SUB, True)
        self.R["tab_design"] = (x0 + 10, TB + 8, 90, 40); self.R["tab_proto"] = (x0 + 102, TB + 8, w + 16, 40)
        ux = x0 + 18 if tab == "design" else x0 + 110
        cv.c.set_source_rgb(1, 1, 1); cv.c.rectangle(ux, TB + 46, 70 if tab == "design" else w, 3); cv.c.fill()
        cv.line(x0, TB + 54, UW, TB + 54, F_LINE, 1)
        x, y = x0 + 16, TB + 84
        if tab == "proto": return self._proto(cv, x, y, v, active)
        if mode == "none":
            y = self.section(cv, x, y, "Page")
            cv.fill_rrect(x, y, 24, 24, 4, F_CANVAS); self.t(cv, x + 36, y + 19, "1E1E1E", 17); return
        if mode in ("component", "set"):
            self.icon_comp(cv, x, y - 4, F_PURPLE)
            self.t(cv, x + 26, y + 10, v.get("comp_name", "Button/Primary"), 18, F_PURPLE, True); y += 40
            if mode == "set" or v.get("variants"):
                y = self.section(cv, x, y + 14, "Properties", plus="add_variant")
                self.field(cv, "prop_state", x, y, RP - 36, "State", v.get("state", "Default")); y += 56
        if mode == "text":
            y = self.section(cv, x, y, "Text")
            self.field(cv, "font", x, y, RP - 36, "", "Inter"); y += 48
            self.field(cv, "weight", x, y, 150, "", "Bold"); self.field(cv, "size", x + 160, y, 148, "", "44"); y += 62
            y = self.section(cv, x, y, "Fill")
            cv.fill_rrect(x, y + 6, 26, 26, 4, (1, 1, 1)); self.t(cv, x + 38, y + 26, "FFFFFF", 18); self.t(cv, x + 200, y + 26, "100%", 18, F_SUB)
            return
        # frame-like
        y = self.section(cv, x, y + (10 if mode != "frame" else 0), "Frame")
        self.field(cv, "w", x, y, 150, "W", v.get("w", "Hug")); self.field(cv, "h", x + 160, y, 148, "H", v.get("h", "Hug")); y += 48
        self.field(cv, "radius", x, y, 150, "◜", v.get("radius", "0"), active == "radius"); y += 62
        y = self.section(cv, x, y, "Auto layout")
        for i, g in enumerate(["↓", "→", "↵"]):
            on = (i == 1)
            cv.fill_rrect(x + i * 46, y, 40, 38, 6, F_SEL if on else F_FIELD)
            self.t(cv, x + i * 46 + 11, y + 27, g, 20, F_BLUE if on else F_SUB, True)
        self.field(cv, "gap", x + 150, y, 158, "⇿", v.get("gap", "10")); y += 50
        self.field(cv, "pad_h", x, y, 150, "|◻|", v.get("pad_h", "0"), active == "pad_h")
        self.field(cv, "pad_v", x + 160, y, 148, "⊟", v.get("pad_v", "0"), active == "pad_v"); y += 50
        # alignment grid
        cv.fill_rrect(x, y, 96, 72, 6, F_FIELD)
        for r in range(3):
            for c in range(3):
                cx, cy = x + 18 + c * 30, y + 14 + r * 22
                if (c, r) == (1, 1): cv.fill_rrect(cx - 8, cy - 6, 16, 12, 3, F_BLUE)
                else: cv.c.set_source_rgb(0.5, 0.5, 0.5); cv.c.arc(cx, cy, 2, 0, 6.3); cv.c.fill()
        self.R["align"] = (x, y, 96, 72); y += 96
        y = self.section(cv, x, y, "Fill", plus="fill_add")
        if v.get("fill"):
            cv.fill_rrect(x, y + 6, 26, 26, 4, v.get("fill_rgb", (0.85, 0.85, 0.85)))
            self.field(cv, "fill_hex", x + 36, y, 150, "", v["fill"], active == "fill_hex")
            self.t(cv, x + 210, y + 26, "100%", 18, F_SUB)
            self.R["fill_swatch"] = (x, y + 6, 26, 26); y += 56
        else: y += 10
        y = self.section(cv, x, y + 6, "Stroke", plus="stroke_add")

    def _proto(self, cv, x, y, v, active):
        y = self.section(cv, x, y, "Interactions", plus="inter_add")
        if v.get("inter"):
            cv.fill_rrect(x, y, RP - 36, 132, 8, F_FIELD)
            if active == "trigger": cv.rrect_path(x, y, RP - 36, 44, 8); cv.c.set_source_rgb(*F_BLUE); cv.c.set_line_width(2); cv.c.stroke()
            self.t(cv, x + 12, y + 29, v.get("trigger", "On click"), 18, F_TXT, True); self.R["trigger"] = (x, y, RP - 36, 44)
            self.t(cv, x + 12, y + 72, "Change to", 17, F_SUB); self.t(cv, x + 140, y + 72, v.get("dest", "Hover"), 17, F_TXT)
            self.t(cv, x + 12, y + 112, "Smart animate", 17, F_SUB); self.t(cv, x + 160, y + 112, "300ms", 17, F_TXT)
            self.R["inter_row"] = (x, y, RP - 36, 132)
            if v.get("menu"):
                mx, my = x + 20, y + 46
                cv.fill_rrect(mx, my, 240, 170, 8, (0.12, 0.12, 0.12))
                for i, it in enumerate(["On click", "On drag", "While hovering", "While pressing"]):
                    if it == v.get("menu_hi"): cv.fill_rrect(mx + 6, my + 6 + i * 40, 228, 36, 5, F_BLUE)
                    self.t(cv, mx + 18, my + 31 + i * 40, it, 17)
                    self.R["menu_" + it] = (mx + 6, my + 6 + i * 40, 228, 36)

    def canvas(self, cv, content):
        cv.c.set_source_rgb(*F_CANVAS); cv.c.rectangle(LP, TB, UW - LP - RP, UH - TB); cv.c.fill()
        cv.c.set_source_rgba(1, 1, 1, 0.07)            # dot grid = brand's dotted look
        for gx in range(LP + 20, UW - RP, 32):
            for gy in range(TB + 20, UH, 32):
                cv.c.rectangle(gx, gy, 1.6, 1.6)
        cv.c.fill()
        cv.c.save(); cv.c.rectangle(LP, TB, UW - LP - RP, UH - TB); cv.c.clip()
        content(cv); cv.c.restore()


# ------------------------------------------------------------------- canvas objects
CX, CY = LP + (UW - LP - RP) / 2, 560


def draw_button(cv, ui, cx=CX, cy=CY, pad_v=0, pad_h=0, fill=None, radius=0, label="Get Started",
                text_col=(1, 1, 1), frame=True, sel=False, name="btn", alpha=1.0, scale=1.0):
    cv.font(SANS, 30 * scale, True); tw = cv.text_w(label); th = 30 * scale
    w, h = tw + 2 * pad_h * scale, th + 10 + 2 * pad_v * scale
    x, y = cx - w / 2, cy - h / 2
    if fill: cv.fill_rrect(x, y, w, h, max(radius, 0.01), fill, alpha)
    elif frame: cv.drrect(x, y, w, h, max(radius, 2), spacing=5.5, r=1.4, a=0.8 * alpha)
    cv.text(cx - tw / 2, cy + th * 0.36, label, text_col, alpha)
    ui.R[name] = (x, y, w, h)
    if sel: selection(cv, x, y, w, h, sel if isinstance(sel, str) else None)
    return x, y, w, h


def selection(cv, x, y, w, h, badge=None, col=F_BLUE):
    c = cv.c; c.set_source_rgb(*col); c.set_line_width(2); c.rectangle(x, y, w, h); c.stroke()
    for hx, hy in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
        c.set_source_rgb(1, 1, 1); c.rectangle(hx - 5, hy - 5, 10, 10); c.fill()
        c.set_source_rgb(*col); c.set_line_width(1.5); c.rectangle(hx - 5, hy - 5, 10, 10); c.stroke()
    if badge:
        cv.font(SANS, 15, True); bw = cv.text_w(badge) + 14
        cv.fill_rrect(x + w / 2 - bw / 2, y + h + 10, bw, 24, 4, col); cv.text(x + w / 2 - bw / 2 + 7, y + h + 27, badge, (1, 1, 1))


# ------------------------------------------------------------------- camera + cursor
class Cam:
    """Keyframes [(t, focus_x, focus_y, zoom)] in UI space; eased between keys."""
    def __init__(self, keys): self.keys = keys

    def at(self, t):
        k = self.keys
        if t <= k[0][0]: return k[0][1:]
        for (t0, *a), (t1, *b) in zip(k, k[1:]):
            if t < t1:
                e = ease((t - t0) / max(1e-6, t1 - t0)); return tuple(lerp(p, q, e) for p, q in zip(a, b))
        return k[-1][1:]


FULL = (UW / 2, UH / 2, 1.0)


def focus(rect, zoom):
    x, y, w, h = rect; return (x + w / 2, y + h / 2, zoom)


def apply_cam(cv, fx, fy, z):
    vw, vh = UW / z, UH / z
    fx = min(max(fx, vw / 2), UW - vw / 2); fy = min(max(fy, vh / 2), UH - vh / 2)
    cv.c.translate(SX + UW / 2, SY + UH / 2); cv.c.scale(z, z); cv.c.translate(-fx, -fy)


class CursorPath:
    """Waypoints [(t_arrive, (x,y), click)] in UI space; eased travel between them."""
    def __init__(self, start, pts): self.start, self.pts = start, pts

    def at(self, t):
        prev_t, prev_p = 0.0, self.start
        for ta, p, _ in self.pts:
            if t < ta:
                tstart = max(prev_t, ta - 0.9)
                if t < tstart: return prev_p
                e = ease((t - tstart) / (ta - tstart)); return (lerp(prev_p[0], p[0], e), lerp(prev_p[1], p[1], e))
            prev_t, prev_p = ta, p
        return prev_p

    def clicks(self): return [ta for ta, _, c in self.pts if c]


def centre(rect, dx=0, dy=0):
    x, y, w, h = rect; return (x + w / 2 + dx, y + h / 2 + dy)


def draw_cursor(cv, pos, t, clicks):
    x, y = pos; cv.c.new_path()
    for ct in clicks:
        if 0 <= t - ct < 0.35:
            k = (t - ct) / 0.35
            cv.c.set_source_rgba(*F_BLUE, 0.6 * (1 - k)); cv.c.arc(x, y, 10 + 30 * k, 0, 6.3); cv.c.fill()
    cv.cursor(x, y, 0.9)


def frame_ui(cv, t, ui, cam, draw_ui, cur=None, clicks=()):
    """Render window + UI through camera; cursor drawn in UI space so it zooms with the view."""
    cv._now = t
    cv.c.save()
    cv.rrect_path(SX + 8, SY, UW - 16, UH, 22); cv.c.clip()
    apply_cam(cv, *cam.at(t))
    draw_ui(cv)
    if cur: draw_cursor(cv, cur, t, clicks)
    cv.c.restore()
    cv.rrect_path(SX + 8, SY, UW - 16, UH, 22); cv.c.set_source_rgba(1, 1, 1, 0.18); cv.c.set_line_width(2); cv.c.stroke()

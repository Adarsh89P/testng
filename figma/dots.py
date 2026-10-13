"""Dotted line-art engine (black bg, white dot outlines, mono code box, pill labels).

Style reference: "15 LPA vs 45 LPA" system-design reels. Everything is pycairo, so
frames are antialiased and fast enough to pipe straight into ffmpeg.
"""
import math
import cairo

BG = (0.012, 0.012, 0.02)
DOT = (0.92, 0.92, 0.94)
DIM = (0.42, 0.42, 0.46)
LINE = (0.30, 0.30, 0.33)
PILL = (0.11, 0.11, 0.125)
BOX = (0.075, 0.075, 0.085)
CODE = (0.80, 0.80, 0.82)
ACCENT = (1.0, 0.36, 0.62)      # measurement pink, used sparingly
GOOD = (0.35, 0.85, 0.55)
BAD = (1.0, 0.38, 0.35)
MONO, SANS = "JetBrains Mono", "Inter"


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        self.c = cairo.Context(self.surf)

    def clear(self):
        self.c.set_source_rgb(*BG); self.c.paint()

    def raw(self):
        self.surf.flush(); return bytes(self.surf.get_data())

    def png(self, p):
        self.surf.write_to_png(p)

    # ------------------------------------------------------------ dots
    def _dot(self, x, y, r, col, a):
        c = self.c
        c.set_source_rgba(*col, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()

    def dots_path(self, pts, spacing=7, r=1.9, col=DOT, a=1.0, closed=False, reveal=1.0):
        """Place dots evenly along a polyline. reveal in [0,1] draws only the first part."""
        if closed: pts = list(pts) + [pts[0]]
        segs, total = [], 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0); segs.append((x0, y0, x1, y1, L)); total += L
        limit, d, acc = total * reveal, 0.0, 0.0
        for x0, y0, x1, y1, L in segs:
            while d <= acc + L and d <= limit:
                t = (d - acc) / L if L else 0
                self._dot(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, col, a)
                d += spacing
            acc += L

    def dline(self, x0, y0, x1, y1, **k):
        self.dots_path([(x0, y0), (x1, y1)], **k)

    def drrect(self, x, y, w, h, rad, **k):
        pts, n = [], 10
        for cx, cy, a0 in [(x + w - rad, y + rad, -90), (x + w - rad, y + h - rad, 0),
                           (x + rad, y + h - rad, 90), (x + rad, y + rad, 180)]:
            for i in range(n + 1):
                a = math.radians(a0 + 90 * i / n)
                pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        self.dots_path(pts, closed=True, **k)

    def dellipse(self, cx, cy, rx, ry, a0=0, a1=360, **k):
        n = max(24, int(max(rx, ry) * 0.6))
        pts = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        self.dots_path(pts, **k)

    def dbar(self, x, y, w, rows=2, gap=7, **k):
        """Text placeholder: a short band of dot rows."""
        for i in range(rows):
            self.dline(x, y + i * gap, x + w, y + i * gap, spacing=gap, **k)

    # ------------------------------------------------------------ plain strokes
    def line(self, x0, y0, x1, y1, col=LINE, wdt=1.4, a=1.0):
        c = self.c; c.set_source_rgba(*col, a); c.set_line_width(wdt)
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()

    def rrect_path(self, x, y, w, h, r):
        c = self.c; r = min(r, w / 2, h / 2)
        c.new_sub_path()
        c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
        c.close_path()

    def fill_rrect(self, x, y, w, h, r, col, a=1.0):
        self.rrect_path(x, y, w, h, r); self.c.set_source_rgba(*col, a); self.c.fill()

    def glow(self, x, y, r=40, a=1.0):
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.95 * a); g.add_color_stop_rgba(0.15, 1, 1, 1, 0.55 * a)
        g.add_color_stop_rgba(1, 1, 1, 1, 0)
        self.c.set_source(g); self.c.arc(x, y, r, 0, 2 * math.pi); self.c.fill()

    # ------------------------------------------------------------ text
    def font(self, fam, size, bold=False):
        self.c.select_font_face(fam, cairo.FONT_SLANT_NORMAL,
                                cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        self.c.set_font_size(size)

    def text_w(self, s):
        return self.c.text_extents(s).x_advance

    def text(self, x, y, s, col=CODE, a=1.0):
        self.c.set_source_rgba(*col, a); self.c.move_to(x, y); self.c.show_text(s)

    def pill(self, cx, cy, s, size=30, fam=SANS, col=DOT, bg=PILL, a=1.0, bold=False):
        self.font(fam, size, bold); tw = self.text_w(s); h = size * 1.6; w = tw + size * 1.2
        self.fill_rrect(cx - w / 2, cy - h / 2, w, h, h / 2, bg, a)
        self.text(cx - tw / 2, cy + size * 0.36, s, col, a)
        return w, h

    def code_box(self, x, y, w, h, lines, chars, cursor_on=True, size=34):
        """Typing code box. `chars` = number of characters revealed so far."""
        self.fill_rrect(x, y, w, h, 18, BOX)
        self.font(MONO, size); lh = size * 1.32
        left, cx, cy = chars, x + 36, y + 36 + size
        for i, ln in enumerate(lines):
            shown = ln[:max(0, left)]; left -= len(ln) + 1
            self.text(cx, cy + i * lh, shown)
            if 0 <= left + len(ln) + 1 <= len(ln) or (left < 0 and shown != ln):
                if cursor_on:
                    tx = cx + self.text_w(shown)
                    self.c.set_source_rgba(*CODE, 0.9); self.c.rectangle(tx + 2, cy + i * lh - size * 0.8, size * 0.5, size)
                    self.c.fill()
                return
        if cursor_on:  # finished: cursor after last line
            ln = lines[-1] if lines else ""
            tx = cx + self.text_w(ln); i = max(0, len(lines) - 1)
            self.c.set_source_rgba(*CODE, 0.9); self.c.rectangle(tx + 2, cy + i * lh - size * 0.8, size * 0.5, size); self.c.fill()

    # ------------------------------------------------------------ icons
    def person(self, cx, cy, s=1.0, **k):
        for r in (22, 14, 7):
            self.dellipse(cx, cy - 30 * s, r * s, r * s, spacing=5.2 * s, r=1.7 * s, **k)
        for r in (52, 42, 32):
            self.dellipse(cx, cy + 40 * s, r * s, r * s * 0.9, 190, 350, spacing=5.6 * s, r=1.7 * s, **k)

    def cursor(self, x, y, s=1.0, a=1.0):
        c = self.c; pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (27, 24)]
        c.move_to(x, y)
        for px, py in pts[1:]: c.line_to(x + px * s, y + py * s)
        c.close_path(); c.set_source_rgba(1, 1, 1, a); c.fill_preserve()
        c.set_source_rgba(0, 0, 0, a); c.set_line_width(1.5); c.stroke()


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t

"""Dotted product card with real auto-layout maths, so gap/padding/resizing animate truthfully."""
from dots import *


def card_layout(x, y, w, gap=16, pad=24, title_rows=1, btn_mode="fill", btn_text_w=150,
                fixed_h=None, scale=2.0):
    """Return element boxes (in px) for a vertical auto-layout card. Figma units * scale."""
    g, p = gap * scale, pad * scale
    inner = w - 2 * p
    items = [("image", 150 * scale), ("title", (22 * title_rows + 6 * (title_rows - 1)) * scale),
             ("details", 40 * scale), ("button", 44 * scale)]
    boxes, cy = {}, y + p
    for name, h in items:
        bw = inner
        if name == "button" and btn_mode == "hug": bw = btn_text_w * scale + 48 * scale
        if name == "button" and btn_mode == "fixed": bw = 140 * scale
        boxes[name] = (x + p, cy, bw, h); cy += h + g
    hug_h = cy - g + p - y
    h = fixed_h * scale if fixed_h else hug_h
    boxes["card"] = (x, y, w, h)
    boxes["_hug_h"] = hug_h
    return boxes


def draw_card(cv, boxes, a=1.0, title_rows=1, label="Add to cart", sp=6.5, r=1.8,
              offsets=None, clip=False):
    """Draw the card. offsets={name:(dx,dy)} simulates sloppy manual placement."""
    offsets = offsets or {}
    k = dict(spacing=sp, r=r, a=a)
    x, y, w, h = boxes["card"]
    cv.drrect(x, y, w, h, 28, **k)
    if clip:
        cv.c.save(); cv.rrect_path(x, y, w, h, 28); cv.c.clip()
    ox, oy = offsets.get("image", (0, 0))
    ix, iy, iw, ih = boxes["image"]; ix += ox; iy += oy
    cv.drrect(ix, iy, iw, ih, 18, **k)
    cv.dellipse(ix + iw * 0.72, iy + ih * 0.32, ih * 0.11, ih * 0.11, spacing=sp * 0.8, r=r, a=a)
    cv.dots_path([(ix + 20, iy + ih - 20), (ix + iw * 0.32, iy + ih * 0.45), (ix + iw * 0.5, iy + ih * 0.7),
                  (ix + iw * 0.65, iy + ih * 0.55), (ix + iw - 20, iy + ih - 20)], **k)
    ox, oy = offsets.get("title", (0, 0))
    tx, ty, tw, th = boxes["title"]; tx += ox; ty += oy
    row = th / title_rows if title_rows else th
    for i in range(title_rows):
        cv.dbar(tx, ty + i * row + row * 0.2, tw * (0.95 if i < title_rows - 1 else 0.6), rows=3, gap=sp, r=r * 1.1, a=a)
    ox, oy = offsets.get("details", (0, 0))
    dx, dy, dw, dh = boxes["details"]; dx += ox; dy += oy
    cv.dbar(dx, dy + 6, dw * 0.8, rows=2, gap=sp, r=r * 0.9, col=DIM, a=a)
    cv.dbar(dx, dy + dh - 18, dw * 0.3, rows=2, gap=sp, r=r, a=a)
    ox, oy = offsets.get("button", (0, 0))
    bx, by, bw, bh = boxes["button"]; bx += ox; by += oy
    cv.fill_rrect(bx, by, bw, bh, bh / 2, PILL, a)
    cv.drrect(bx, by, bw, bh, bh / 2, **k)
    cv.font(SANS, bh * 0.36, True); lw = cv.text_w(label)
    cv.text(bx + bw / 2 - lw / 2, by + bh * 0.63, label, DOT, a)
    if clip: cv.c.restore()


def measure_gap(cv, boxes, gap_label, a=1.0, side="right"):
    """Pink gap bands between stacked items with a pill showing the value."""
    names = ["image", "title", "details", "button"]
    x, y, w, h = boxes["card"]
    for n0, n1 in zip(names, names[1:]):
        _, y0, _, h0 = boxes[n0]; _, y1, _, _ = boxes[n1]
        top, bot = y0 + h0, y1
        if bot - top < 2: continue
        cv.c.set_source_rgba(*ACCENT, 0.28 * a); cv.c.rectangle(x + 8, top, w - 16, bot - top); cv.c.fill()
        cv.line(x + w + 18, top, x + w + 18, bot, ACCENT, 2, a)
        cv.pill(x + w + 80, (top + bot) / 2, gap_label, size=24, fam=MONO, col=ACCENT, a=a)


def measure_pad(cv, boxes, pad_label, a=1.0):
    x, y, w, h = boxes["card"]; ix, iy, iw, ih = boxes["image"]
    p = ix - x
    cv.c.set_source_rgba(*ACCENT, 0.22 * a)
    for rx, ry, rw, rh in [(x, y, w, p), (x, y + h - p, w, p), (x, y, p, h), (x + w - p, y, p, h)]:
        cv.c.rectangle(rx, ry, rw, rh)
    cv.c.fill()
    cv.pill(x + w / 2, y - 36, pad_label, size=24, fam=MONO, col=ACCENT, a=a)

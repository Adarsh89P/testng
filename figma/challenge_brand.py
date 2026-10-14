"""Brand an existing reel as '45 Days · 45 UX Challenge' without touching its voice.

Adds a short dot-formed intro, a DAY xx/45 badge + 45-dot progress row on every frame, and an end card
teasing the next day. The original audio is kept bit-for-bit after the intro (only shifted by the intro).

usage: python3 challenge_brand.py IN.mp4 OUT.mp4 --day 1 --next "Hick's Law"
"""
import argparse, json, math, os, subprocess, tempfile
import numpy as np, cairo, soundfile as sf
from dots import *
from fx import dot_text
from engine import whoosh, SR, M
from kokoro_onnx import Kokoro

W, H, FPS = 1080, 1920, 30
TOTAL = 45
INTRO = 2.6
INTRO_VOICE = "पैंतालीस दिन, पैंतालीस यू एक्स लॉज़। डे {day_hi}।"
DAYS_HI = {1: "वन", 2: "टू", 3: "थ्री", 4: "फोर", 5: "फाइव", 6: "सिक्स", 7: "सेवन", 8: "एट", 9: "नाइन", 10: "टेन"}


def surface_for(buf):
    return cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_ARGB32, W, H, W * 4)


class Wrap(Canvas):
    """Canvas API over an existing BGRA frame buffer."""
    def __init__(self, buf):
        self.w, self.h = W, H
        self.surf = surface_for(buf); self.c = cairo.Context(self.surf)


def badge(cv, day, a=1.0):
    cv.c.set_source_rgba(*BG, 0.85 * a); cv.c.rectangle(0, 70, W, 205); cv.c.fill()
    white_pill(cv, W / 2, 120, f"DAY {day:02d}/{TOTAL} · UX CHALLENGE", 30)
    x0, x1 = 110, W - 110
    for i in range(TOTAL):
        x = x0 + (x1 - x0) * i / (TOTAL - 1)
        on = i < day
        cv._dot(x, 182, 5.5 if on else 3.2, (1, 1, 1) if on else (0.36, 0.36, 0.4), a)
        if on and i == day - 1: cv.glow(x, 182, 22, 0.8 * a)


def end_card(cv, t_left, day, nxt):
    """Shown over the final seconds (t_left counts down to 0)."""
    k = min(1, (3.0 - t_left) / 0.4)
    cv.c.set_source_rgba(*BG, 0.9 * k); cv.c.rectangle(0, 1560, W, 260); cv.c.fill()
    white_pill(cv, W / 2, 1630, f"kal · Day {day + 1:02d}: {nxt}", 36)
    if t_left < 2.4: cv.pill(W / 2, 1725, f"follow for all {TOTAL}", size=30, fam=MONO)


BLUE = (0.0, 0.584, 0.965)
WATERMARK = "Design with Rakhi · @rakhi.ux"


def watermark(cv, text=WATERMARK, a=0.55):
    """Small persistent channel watermark under the progress dots (Instagram's bottom ~400px is covered by the caption)."""
    cv.font(MONO, 26, True); tw = cv.text_w(text); x, y = W / 2 - tw / 2, 252
    cv.fill_rrect(x - 18, y - 30, tw + 36, 44, 22, (0, 0, 0), 0.35 * a / 0.55)
    cv.c.set_source_rgba(1, 1, 1, a); cv.c.move_to(x, y); cv.c.show_text(text)


def avatar(cv, cx, cy, r, path, k=1.0):
    """Circular-cropped profile photo (if provided)."""
    img = cairo.ImageSurface.create_from_png(path)
    s = 2 * r / min(img.get_width(), img.get_height())
    c = cv.c; c.save(); c.arc(cx, cy, r, 0, 6.2832); c.clip()
    c.translate(cx - img.get_width() * s / 2, cy - img.get_height() * s / 2); c.scale(s, s)
    c.set_source_surface(img, 0, 0); c.paint_with_alpha(k); c.restore()
NEXT_LABEL = "kal · Day {day:02d}"
OUTRO_VOICE = "ऐसे और यू एक्स लॉज़ के लिए, डिज़ाइन विद राखी को फॉलो करो।"


def outro_frame(cv, t, day, brand, handle, tap_at=1.5, photo=None):
    """'Follow Design with Rakhi' card: dotted avatar, name, handle, and a Follow button that gets tapped."""
    cv.clear()
    for y in range(18, H, 36):
        for x in range(18, W, 36): cv._dot(x, y, 1.2, (0.2, 0.2, 0.23), 1.0)
    k = ease(t / 0.5)
    cx, ay = W / 2, 720
    # dotted avatar rings + dot-matrix initial
    for i, r in enumerate((150, 128, 106)):
        cv.dellipse(cx, ay, r * k, r * k, spacing=8 - i, r=2.4 - 0.4 * i, a=1.0)
    cv.glow(cx, ay, 200, 0.12 * k)
    if photo:
        avatar(cv, cx, ay, 98, photo, k)
    else:
        cv.font(SANS, 130, True); tw = cv.text_w("R")
        cv.text(cx - tw / 2, ay + 46, "R", (1, 1, 1), k)
    # name + handle
    cv.font(SANS, 76, True); s1 = brand; cv.text(cx - cv.text_w(s1) / 2, 980, s1, (1, 1, 1), k)
    cv.font(MONO, 40); s2 = "@" + handle; cv.text(cx - cv.text_w(s2) / 2, 1050, s2, (0.75, 0.75, 0.78), k)
    cv.font(MONO, 30); s3 = "45 days · 45 UX laws · live apps"
    cv.text(cx - cv.text_w(s3) / 2, 1110, s3, DIM, k)
    # follow button
    tapped = t >= tap_at
    pop = 1 + 0.08 * math.sin(math.pi * min(1, max(0, (t - tap_at) / 0.25))) if tapped else 1 - 0.04 * max(0, 1 - abs(t - tap_at + 0.08) / 0.08)
    bw, bh = 420 * pop, 104 * pop; bx, by = cx - bw / 2, 1220 - bh / 2
    if tapped:
        cv.fill_rrect(bx, by, bw, bh, 22, (0.17, 0.17, 0.19))
        cv.font(SANS, 44, True); lab = "Following ✓"
        cv.text(cx - cv.text_w(lab) / 2, 1220 + 16, lab, (1, 1, 1))
        # celebration dots
        lt = t - tap_at
        if lt < 1.2:
            for i in range(28):
                ang = i / 28 * 6.283; d = 80 + 260 * ease(lt / 1.2)
                cv._dot(cx + math.cos(ang) * d * 1.3, 1220 + math.sin(ang) * d * 0.7, 4, BLUE if i % 2 else (1, 1, 1), max(0, 1 - lt / 1.2))
    else:
        cv.fill_rrect(bx, by, bw, bh, 22, BLUE, k)
        cv.font(SANS, 48, True); lab = "Follow"
        cv.text(cx - cv.text_w(lab) / 2, 1220 + 17, lab, (1, 1, 1), k)
    # tap finger/cursor
    if 0.6 < t < tap_at + 0.6:
        tx = lerp(cx + 330, cx + 40, ease((t - 0.6) / (tap_at - 0.6 - 0.05)))
        ty = lerp(1450, 1235, ease((t - 0.6) / (tap_at - 0.6 - 0.05)))
        if abs(t - tap_at) < 0.35:
            q = max(0, (t - tap_at) / 0.35)
            cv.c.set_source_rgba(1, 1, 1, 0.45 * (1 - q)); cv.c.arc(cx + 40, 1235, 20 + 50 * q, 0, 6.3); cv.c.fill()
        cv._dot(tx, ty, 16, (1, 1, 1), 0.9)
    if t > tap_at + 0.4: white_pill(cv, cx, 1400, NEXT_LABEL.format(day=day + 1), 34)
    badge(cv, day)


INTRO_PHRASES = [("पैंतालीस दिन,", "45 din,"), ("पैंतालीस यू एक्स लॉज़।", "45 UX laws."), ("डे {day_hi}।", "Day {day}.")]
OUTRO_PHRASES = [("ऐसे और यू एक्स लॉज़ के लिए,", "Aise aur UX laws ke liye,"), ("डिज़ाइन विद राखी को फॉलो करो।", "Design with Rakhi ko follow karo.")]
CC_Y = 1545


def cc_draw(cv, t, cues, hold=0.3):
    """Stylish karaoke captions: spoken words white, current word pops with a blue glow underline, upcoming dim."""
    cue = None
    for i, c in enumerate(cues):
        nxt = cues[i + 1]["t0"] if i + 1 < len(cues) else 1e9
        if c["t0"] <= t < min(c["t1"] + hold, nxt): cue = c; break
    if not cue: return
    words = cue["text"].split()
    lens = np.cumsum([len(w) + 1 for w in words]); lens = lens / lens[-1]
    prog = (t - cue["t0"]) / max(0.01, cue["t1"] - cue["t0"])
    cur = int(np.searchsorted(lens, min(prog, 0.999), side="right"))
    size = 46; cv.font(SANS, size, True); space = cv.text_w(" ")
    lines, line, wmax = [], [], 900
    for i, w in enumerate(words):
        test = sum(cv.text_w(x) + space for _, x in line) + cv.text_w(w)
        if line and test > wmax: lines.append(line); line = []
        line.append((i, w))
    lines.append(line)
    lh = size * 1.32; total_h = lh * len(lines)
    bw = max(sum(cv.text_w(x) for _, x in ln) + space * (len(ln) - 1) for ln in lines) + 64
    k = min(1, (t - cue["t0"]) / 0.15)
    top = CC_Y - total_h / 2 - 18
    cv.fill_rrect(W / 2 - bw / 2, top, bw, total_h + 36, 30, (0.03, 0.03, 0.05), 0.82 * k)
    cv.c.set_source_rgba(1, 1, 1, 0.10 * k); cv.rrect_path(W / 2 - bw / 2, top, bw, total_h + 36, 30); cv.c.set_line_width(1.5); cv.c.stroke()
    for li, ln in enumerate(lines):
        lw = sum(cv.text_w(x) for _, x in ln) + space * (len(ln) - 1)
        x = W / 2 - lw / 2; y = top + 18 + lh * li + size * 1.0
        for i, w in ln:
            ww = cv.text_w(w)
            if i < cur: col, a = (1, 1, 1), 1.0
            elif i == cur: col, a = (1, 1, 1), 1.0
            else: col, a = (0.55, 0.55, 0.6), 0.9
            if i == cur:
                cv.glow(x + ww / 2, y + 12, ww * 0.7, 0.18)
                cv.fill_rrect(x, y + 10, ww, 5, 2.5, BLUE, 1.0)
                cv.text(x, y, w, col, a * k)
            else:
                cv.text(x, y, w, col, a * k)
            x += ww + space


def timed(phrases, start, dur, synth_len):
    lens = np.array([synth_len(d) for d, _ in phrases], float); w = lens / lens.sum()
    out, t = [], start
    for (d, r), f in zip(phrases, w):
        out.append({"t0": t, "t1": t + f * dur, "text": r}); t += f * dur
    return out


def intro_frame(cv, t, day):
    cv.clear()
    swarm(cv, t, 60, 1150, 960, 500, n=150, a=0.45)
    dot_text(cv, "45 DAYS", 140, W / 2, 760, ease(1 - t / 0.9))
    if t > 0.7:
        s = "45 UX LAWS · CHALLENGE"; n = int((t - 0.7) * 26)
        cv.font(MONO, 44); cv.text(W / 2 - cv.text_w(s) / 2, 900, s[:n], (0.85, 0.85, 0.88))
    if t > 1.5: white_pill(cv, W / 2, 1020, f"DAY {day:02d}", 40)
    if t > 1.7: cv.font(MONO, 30); cv.text(W / 2 - cv.text_w("live apps se seekho") / 2, 1110, "live apps se seekho", DIM)
    badge(cv, day, a=min(1, t / 0.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--day", type=int, default=1); ap.add_argument("--next", default="Hick's Law")
    ap.add_argument("--voice", default="hf_beta"); ap.add_argument("--speed", type=float, default=1.05)
    ap.add_argument("--no-intro-voice", action="store_true")
    ap.add_argument("--brand", default="Design with Rakhi"); ap.add_argument("--handle", default="rakhi.ux")
    ap.add_argument("--no-outro", action="store_true")
    ap.add_argument("--photo", default=None, help="profile photo (png/jpg) for the outro avatar")
    ap.add_argument("--watermark", default=WATERMARK)
    ap.add_argument("--cc", default=None, help="JSON phrase cues for the source video (from cc_build.py)")
    ap.add_argument("--cut-at", type=float, default=None, help="end the source here (e.g. drop its own follow CTA)")
    ap.add_argument("--hide-box", default=None, help="x,y,w,h area to blank in the source's last 0.6 s (old CTA pill)")
    a = ap.parse_args()
    global INTRO, NEXT_LABEL
    NEXT_LABEL = "kal · Day {day:02d}: " + a.next
    if a.photo and not a.photo.lower().endswith(".png"):
        png = os.path.join(tempfile.mkdtemp(), "avatar.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.photo, png], check=True); a.photo = png
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.inp],
                               capture_output=True, text=True).stdout)
    tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(a.out)))
    vid = os.path.join(tmp, "v.mp4"); wav = os.path.join(tmp, "a.wav")

    # audio: intro whoosh + silence, then the ORIGINAL track unchanged
    orig = subprocess.run(["ffmpeg", "-v", "error", "-i", a.inp, "-vn", "-ac", "2", "-ar", "48000", "-f", "f32le", "-"],
                          capture_output=True, check=True).stdout
    orig = np.frombuffer(orig, np.float32).reshape(-1, 2)
    if a.cut_at:
        a.cut_at = round(a.cut_at * FPS) / FPS
        orig = orig[:int(48000 * a.cut_at)].copy(); fl = int(48000 * 0.06)
        orig[-fl:] *= np.linspace(1, 0, fl)[:, None]
        dur = a.cut_at
    vo = None; intro_vo_len = 0.0; outro_vo_len = 0.0
    if not a.no_intro_voice:
        # same engine/voice/speed as the original narration, no extra processing, so it sounds continuous
        k = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
        line = INTRO_VOICE.format(day_hi=DAYS_HI.get(a.day, str(a.day)))
        v, vsr = k.create(line, voice=a.voice, speed=a.speed, lang="hi")
        v = np.interp(np.linspace(0, len(v) - 1, int(len(v) * 48000 / vsr)), np.arange(len(v)), v).astype(np.float32)
        # match loudness to the original's speech (RMS of its louder half of 50 ms frames)
        m = orig.mean(1); fl = 2400
        e = np.array([np.sqrt(np.mean(m[i:i + fl] ** 2)) for i in range(0, len(m) - fl, fl)])
        target = np.sqrt(np.mean(e[e >= np.median(e)] ** 2))
        ve = np.array([np.sqrt(np.mean(v[i:i + fl] ** 2)) for i in range(0, len(v) - fl, fl)])
        v *= target / (np.sqrt(np.mean(ve[ve >= np.median(ve)] ** 2)) + 1e-9)
        vo = v; intro_vo_len = len(v) / 48000
        INTRO = max(INTRO, 0.35 + len(v) / 48000 + 0.45)
    INTRO = math.ceil(INTRO * FPS) / FPS          # whole frames, so audio and video intros match exactly
    intro = np.zeros((int(48000 * INTRO), 2), np.float32)
    if vo is not None:
        i0 = int(48000 * 0.35); intro[i0:i0 + len(vo), 0] += vo; intro[i0:i0 + len(vo), 1] += vo
    w = whoosh(0.5); w = np.interp(np.linspace(0, len(w) - 1, int(len(w) * 2)), np.arange(len(w)), w).astype(np.float32)
    peak = np.abs(orig).max() or 1.0
    intro[:len(w), 0] += w * 0.35 * peak; intro[:len(w), 1] += w * 0.35 * peak
    tail = np.zeros((0, 2), np.float32); OUTRO, TAP = 0.0, 1.5
    if not a.no_outro:
        k2 = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
        v2, vsr = k2.create(OUTRO_VOICE, voice=a.voice, speed=a.speed, lang="hi")
        v2 = np.interp(np.linspace(0, len(v2) - 1, int(len(v2) * 48000 / vsr)), np.arange(len(v2)), v2).astype(np.float32)
        if vo is not None:
            v2 *= np.sqrt(np.mean(vo ** 2)) / (np.sqrt(np.mean(v2 ** 2)) + 1e-9)
        outro_vo_len = len(v2) / 48000
        OUTRO = math.ceil(max(3.4, 0.3 + len(v2) / 48000 + 0.9) * FPS) / FPS
        TAP = min(OUTRO - 1.2, 0.3 + len(v2) / 48000 * 0.8)
        tail = np.zeros((int(48000 * OUTRO), 2), np.float32)
        i0 = int(48000 * 0.3); tail[i0:i0 + len(v2), 0] += v2; tail[i0:i0 + len(v2), 1] += v2
        tt = np.arange(int(48000 * 0.04)) / 48000
        clk = (np.random.randn(len(tt)) * np.exp(-tt * 900) * 0.6 + np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 300) * 0.25) * peak * 0.6
        j = int(48000 * TAP); tail[j:j + len(clk), 0] += clk; tail[j:j + len(clk), 1] += clk
    # pad original to a whole number of frames so the outro starts exactly on a frame boundary
    nfr = int(round(len(orig) / 48000 * FPS)); need = int(48000 * nfr / FPS)
    orig = orig[:need] if len(orig) >= need else np.concatenate([orig, np.zeros((need - len(orig), 2), np.float32)])
    sf.write(wav, np.concatenate([intro, orig, tail]), 48000, subtype="FLOAT")

    cues = []
    if a.cc:
        kk = Kokoro(f"{M}/kokoro-v1.0.onnx", f"{M}/voices-v1.0.bin")
        slen = lambda d: len(kk.create(d, voice=a.voice, speed=a.speed, lang="hi")[0])
        if intro_vo_len:
            ip = [(d.format(day_hi=DAYS_HI.get(a.day, str(a.day))), r.format(day=a.day)) for d, r in INTRO_PHRASES]
            cues += timed(ip, 0.35, intro_vo_len, slen)
        src = json.load(open(a.cc))
        src = [c for c in src if not a.cut_at or c["t0"] < a.cut_at - 0.05]
        cues += [{"t0": c["t0"] + INTRO, "t1": min(c["t1"], a.cut_at or 1e9) + INTRO, "text": c["text"]} for c in src]
        if outro_vo_len:
            cues += timed(OUTRO_PHRASES, INTRO + nfr / FPS + 0.3, outro_vo_len, slen)
    last_src_cue = max([c["t1"] for c in cues if c["t0"] < INTRO + nfr / FPS], default=0)

    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    cv = Canvas(W, H)
    for f in range(int(INTRO * FPS)):
        intro_frame(cv, f / FPS, a.day); watermark(cv, a.watermark); cc_draw(cv, f / FPS, cues); enc.stdin.write(cv.raw())
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.inp, "-f", "rawvideo", "-pix_fmt", "bgra", "-"], stdout=subprocess.PIPE)
    fsz, f = W * H * 4, 0
    while True:
        raw = dec.stdout.read(fsz)
        if len(raw) < fsz: break
        if f >= nfr: break
        buf = bytearray(raw); fr = Wrap(buf); t = f / FPS
        if a.hide_box and dur - t < 0.6:
            hx, hy, hw, hh = map(float, a.hide_box.split(",")); fr.c.set_source_rgb(*BG); fr.c.rectangle(hx, hy, hw, hh); fr.c.fill()
        badge(fr, a.day)
        if not a.cut_at and dur - t < 3.0 and INTRO + t > last_src_cue + 0.2: end_card(fr, dur - t, a.day, a.next)
        watermark(fr, a.watermark); cc_draw(fr, INTRO + t, cues)
        fr.surf.flush(); enc.stdin.write(bytes(buf)); f += 1
    dec.stdout.close(); dec.kill(); dec.wait()      # source may be cut early: stop the decoder instead of waiting on it
    while f < nfr:                       # keep video frame count equal to the padded audio
        enc.stdin.write(bytes(buf)); f += 1
    for g in range(int(round(OUTRO * FPS))):
        outro_frame(cv, g / FPS, a.day, a.brand, a.handle, tap_at=TAP, photo=a.photo); watermark(cv, a.watermark)
        cc_draw(cv, INTRO + nfr / FPS + g / FPS, cues); enc.stdin.write(cv.raw())
    enc.stdin.close(); enc.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", a.out], check=True)
    print("done", a.out, round(INTRO + f / FPS + OUTRO, 1), "s")


if __name__ == "__main__":
    main()

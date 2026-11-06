// Short 3 — समुद्र मंथन में विष्णु के अनेक रूप. One choreography, shared by both styles.
// frame(t) → { items, cam, mood, lamps }. Times come from the pauses in audio/voice.mp3 (59.2 s).
export const W = 1080, H = 1920, DUR = 60.0, GY = 1300;
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const seg = (t, a, b) => clamp((t - a) / (b - a));
export const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
export const eo = t => 1 - Math.pow(1 - clamp(t), 3);
export const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
export const mul = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1], A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3], A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
export const T = (x, y) => [1, 0, 0, 1, x, y];
export const R = r => [Math.cos(r), Math.sin(r), -Math.sin(r), Math.cos(r), 0, 0];
export const Sc = (sx, sy = sx) => [sx, 0, 0, sy, 0, 0];
export const ap = (M, [x, y]) => [M[0] * x + M[2] * y + M[4], M[1] * x + M[3] * y + M[5]];
const place = (x, y, s = 1, sx = 1, r = 0) => mul(mul(T(x, y), Sc(sx * s, s)), R(r));

export const CUES = [
  [0.00, 0.96, 'क्या आपको पता है...'], [1.37, 3.60, 'कि समुद्र मंथन के समय भगवान विष्णु'], [3.60, 6.06, 'एक साथ कई रूपों में उपस्थित थे?'],
  [6.80, 8.40, 'विष्णु पुराण के अनुसार,'], [8.40, 9.90, 'जब देवता और दैत्य'], [9.90, 11.80, 'मंदराचल पर्वत को मथानी'], [11.80, 14.30, 'और नागराज वासुकि को रस्सी बनाकर'], [14.30, 16.48, 'क्षीरसागर को मथने लगे...'],
  [16.80, 18.97, 'तो भगवान ने स्वयं सब कुछ सँभाला।'],
  [19.79, 21.20, 'पहला रूप — कच्छप।'], [21.97, 25.20, 'समुद्र के बीच, विशाल कछुए का रूप लेकर'], [25.20, 28.66, 'उन्होंने घूमते हुए मंदराचल को अपनी पीठ पर धारण किया।'],
  [29.28, 30.08, 'दूसरा रूप —'], [30.59, 34.00, 'देवताओं के बीच खड़े होकर वे वासुकि को खींच रहे थे।'],
  [34.55, 35.23, 'तीसरा रूप —'], [35.68, 37.28, 'दैत्यों के बीच भी वही थे।'],
  [37.79, 38.51, 'चौथा रूप —'], [39.00, 43.24, 'एक विशाल रूप में वे पर्वत के शिखर पर बैठकर उसे थामे हुए थे।'],
  [44.25, 45.89, 'और अपनी अदृश्य शक्ति से'], [46.12, 48.00, 'वे वासुकि में भी बल भर रहे थे...'], [48.36, 49.44, 'और देवताओं में भी।'],
  [50.03, 50.99, 'एक ही भगवान...'], [51.37, 52.09, 'नीचे भी,'], [52.43, 53.05, 'ऊपर भी,'], [53.33, 54.17, 'दोनों ओर भी।'],
  [54.76, 55.77, 'पूरी कथा देखिए —'], [56.11, 57.67, 'समुद्र मंथन के रहस्य।'], [58.14, 59.10, 'जय श्री हरि।'],
];
export const cueAt = t => { for (let i = 0; i < CUES.length; i++) { const [a, b, s] = CUES[i], nx = CUES[i + 1] ? CUES[i + 1][0] : DUR; if (t >= a && t < Math.min(nx, b + .6)) return [s, t - a]; } return null; };
export function pr(t, t0, t1 = 1e9, din = .5, dout = .6) {
  if (t < t0 || t > t1 + dout) return null;
  if (t < t0 + din) { const u = eo((t - t0) / din); return { a: u, k: 1 + .2 * (1 - u), b: 12 * (1 - u) }; }
  if (t > t1) { const u = ss((t - t1) / dout); return { a: 1 - u, k: 1 + .25 * u, b: 14 * u }; }
  return { a: 1, k: 1, b: 0 };
}
const flare = (t, t0, d = .45) => { if (t < t0) return 0; const u = (t - t0) / d; return u < 1 ? lerp(.1, 1, eo(u)) + .35 * Math.sin(u * Math.PI) : 1; };
const pulse = (t, t0) => t < t0 ? 0 : Math.exp(-(t - t0) * 2.2);

// where everything stands in the churning tableau
const MB = [540, GY + 40], MS = .85, PEAK = [540, GY + 40 - 690 * MS];
const ROPE_Y = GY - 190, KURMA = [540, GY + 40];
const VDEVA = [745, GY + 12], VASURA = [335, GY + 12];
const END = 54.3;

export function frame(t) {
  const items = [];
  const add = (id, M, t0, t1, o = {}) => { const e = pr(t, t0, t1, o.din, o.dout); if (!e) return; items.push({ id, M: mul(M, Sc(e.k)), a: e.a * (o.a ?? 1), b: e.b, t0, jit: o.jit ?? 1 }); };

  // —— 1 · hook: Vishnu, then his forms appear around him ——
  add('hook', place(540, 400, 1), 1.37, 5.95);
  add('vishnu', place(540, 1470, 1.05), .2, 5.95, { din: .7 });
  [[190, 1330, .42, 3.6], [890, 1330, .42, 4.0], [250, 900, .34, 4.4], [830, 900, .34, 4.8]].forEach(([x, y, s, t0], i) => add('vishnu', place(x, y, s, i % 2 ? -1 : 1), t0, 5.95, { a: .55 }));

  // —— the churning tableau: 6.8 → 54.3 ——
  const churn = ss(seg(t, 14.5, 15.3)), ph = Math.max(0, t - 14.5) * 2.2, pull = churn * Math.sin(ph * Math.PI);
  add('sea0', place(0, GY - 10 + (1 - eo(seg(t, 6.8, 7.6))) * 300), 6.8, END, { jit: 0 });
  const kRise = (1 - eo(seg(t, 20.85, 22.0))) * 260;
  add('kurma', place(KURMA[0], KURMA[1] + kRise, 1.15), 20.85, END, { din: .6, jit: 0 });
  add('mandaraB', place(MB[0], MB[1], MS, 1, churn * .018 * Math.sin(ph * Math.PI * .5)), 10.0, END, { jit: 0 });
  const ve = pr(t, 11.9, END);
  if (ve) {
    for (let k = 0; k < 4; k++) { const off = (ph * 34 + k * 90) % 360, y = MB[1] - 430 * MS + off * .8 * MS, edge = Math.sin(off / 360 * Math.PI); items.push({ id: 'wrap', M: mul(place(540, y, MS), Sc(ve.k)), a: ve.a * edge, b: ve.b, t0: 11.9, jit: 0 }); }
    items.push({ id: 'vasuki', M: mul(place(610 + pull * 16, ROPE_Y), Sc(ve.k)), a: ve.a, b: ve.b, t0: 11.9, jit: 0 });
  }
  add('daitya0', place(215, GY + 12, .72, 1, -.07 - .05 * pull), 9.2, END, { seed: 1 });
  add('daitya1', place(100, GY + 12, .68, 1, -.07 - .05 * pull), 9.4, END);
  add('deva0', place(868, GY + 12, .72, -1, .07 + .05 * pull), 8.6, END);
  add('deva1', place(985, GY + 12, .68, -1, .07 + .05 * pull), 8.8, END);
  // Vishnu among the devas, among the daityas, and vast upon the summit
  add('vishnu', place(VDEVA[0], VDEVA[1], .62, -1, .05 + .04 * pull), 30.59, END, { din: .6 });
  add('vishnu', place(VASURA[0], VASURA[1], .62, 1, -.05 - .04 * pull), 35.68, END, { din: .6 });
  add('vishnu', place(PEAK[0], PEAK[1] + 8, .92), 39.0, END, { din: .7 });
  add('sea1', place(0, GY + 120 + (1 - eo(seg(t, 6.8, 7.6))) * 340), 6.8, END, { jit: 0 });

  // —— the unseen strength: golden sparks into Vasuki, then into the devas ——
  const SRC = [[PEAK[0], PEAK[1] - 380], [KURMA[0] + 200, KURMA[1] + 40], [VDEVA[0], VDEVA[1] - 300], [VASURA[0], VASURA[1] - 300]];
  for (let i = 0; i < 72; i++) {
    const toDevas = i >= 52, t0 = toDevas ? 48.2 + hash(i) * .6 : 44.2 + hash(i) * 2.9, d = 1.5;
    if (t < t0 || t > t0 + d) continue;
    const u = ss((t - t0) / d), [sx, sy] = SRC[i % 4], tx = toDevas ? [868, 985][i % 2] : 90 + hash(i * 3) * 900, ty = toDevas ? GY - 220 : ROPE_Y;
    add('spark', place(lerp(sx, tx, u), lerp(sy, ty, u) - Math.sin(u * Math.PI) * 160, 1.5 + hash(i * 7) * .8, 1, t * 3 + i), t0, t0 + d - .3, { din: .2, dout: .3, a: Math.sin(u * Math.PI), jit: 0 });
  }
  if (t > 16.8 && t < 18.9) for (let i = 0; i < 14; i++) { const u = seg(t, 16.8 + hash(i) * .4, 18.6); if (u <= 0 || u >= 1) continue; const a = i / 14 * 2 * Math.PI + u * 2; add('spark', place(540 + Math.cos(a) * (120 + u * 320), 820 + Math.sin(a) * (120 + u * 260), 1.4, 1, u * 6), 16.8, 18.9, { din: .1, a: Math.sin(u * Math.PI), jit: 0 }); }

  // —— end card ——
  add('title', place(540, 560, .9), 54.76, 1e9, { din: .6 });
  add('vishnu', place(540, GY + 80, 1.0), 56.11, 1e9, { din: .7 });

  // —— camera ——
  const key = (pts) => { let c = pts[0][1]; for (let i = 1; i < pts.length; i++) { const [ta, ca] = pts[i - 1], [tb, cb] = pts[i]; if (t >= ta) c = ca.map((v, j) => lerp(v, cb[j], ss(seg(t, ta, tb)))); } return c; };
  let cam = key([[0, [540, 940, 1.05]], [6.6, [540, 940, 1.05]], [7.4, [540, 1000, 1.0]], [16.4, [540, 990, 1.06]], [19.8, [540, 990, 1.06]], [21.0, [540, 1250, 1.24]], [28.7, [540, 1240, 1.26]], [29.6, [600, 1080, 1.2]], [30.6, [640, 1060, 1.25]], [34.5, [640, 1060, 1.25]], [35.6, [440, 1060, 1.25]], [37.7, [440, 1060, 1.25]], [38.9, [540, 860, 1.15]], [43.6, [540, 860, 1.15]], [44.5, [540, 1000, 1.02]], [49.8, [540, 1000, 1.0]], [54.3, [540, 1000, 1.0]], [54.9, [540, 960, 1.05]]]);
  cam = cam.slice();
  for (const h of [20.85, 39.0]) if (t >= h && t < h + .45) cam[2] += .08 * (1 - eo((t - h) / .45));

  // —— lamps (shadow puppetry) ——
  const L = [];
  if (t < 6.4) L.push([540, 1050, flare(t, .2), 1], [540, 700, .5 * flare(t, 1.37), .6]);
  else if (t < END) {
    L.push([300, 800, .55, .6], [780, 800, .55, .6], [540, 1200, .5, .6]);
    L.push([540, 850, 1.2 * pulse(t, 16.8), 1]);
    L.push([540, 1430, flare(t, 20.85) * .9 + 1.2 * pulse(t, 51.37), 1]);
    L.push([VDEVA[0], 1050, flare(t, 30.59) * .7 + 1.0 * pulse(t, 53.33), 1], [VASURA[0], 1050, flare(t, 35.68) * .7 + 1.0 * pulse(t, 53.33), 1]);
    L.push([540, 560, flare(t, 39.0) * .9 + 1.2 * pulse(t, 52.43), 1]);
  } else L.push([540, 560, flare(t, 54.76), .8], [540, 1150, flare(t, 56.11) + .4 * flare(t, 58.14), 1]);

  const fade = ss(seg(t, 59.4, 60.0)) + (1 - ss(seg(t, 0, .25)));
  const flash = Math.max(pulse(t, 16.8), pulse(t, 39.0) * .6) * .35;
  return { items, cam, lamps: L, mood: { anger: 0, drain: 0, flash: clamp(flash), fade: clamp(fade), hero: t > 54.7 ? 1 : 0 } };
}

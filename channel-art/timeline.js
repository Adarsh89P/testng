// Short 4 — वासुकि का मुख और पूँछ. Times come from the pauses in audio/voice.mp3 (56.8 s).
export const W = 1080, H = 1920, DUR = 57.6, GY = 1300;
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
  [0.00, 1.05, 'क्या आपको पता है...'], [1.51, 4.60, 'कि समुद्र मंथन में दैत्यों को वासुकि के मुख की ओर...'], [4.60, 7.70, 'भगवान विष्णु ने स्वयं खड़ा किया था?'],
  [8.55, 9.90, 'विष्णु पुराण के अनुसार,'], [10.17, 12.60, 'जब मंदराचल पर्वत को मथानी'], [12.60, 15.02, 'और नागराज वासुकि को रस्सी बनाया गया...'],
  [15.28, 18.50, 'तो भगवान ने दैत्यों को नाग के मुख की ओर रखा,'], [18.84, 20.71, 'और देवताओं को पूँछ की ओर।'],
  [21.88, 23.05, 'फिर मंथन शुरू हुआ।'], [23.73, 28.09, 'वासुकि की हर साँस के साथ उसके मुख से प्रचंड ज्वाला निकलती...'], [28.47, 31.65, 'और वह ज्वाला दैत्यों के तेज को झुलसाती गई।'],
  [32.18, 36.35, 'और उन्हीं साँसों से उठे बादल... हवा के साथ पूँछ की ओर बहे,'], [36.70, 41.22, 'और वहाँ बरसकर देवताओं को शीतलता और नई शक्ति देते रहे।'],
  [41.85, 42.67, 'एक ही नाग...'], [43.20, 44.02, 'एक ओर अग्नि,'], [44.33, 45.41, 'दूसरी ओर वर्षा।'],
  [45.91, 47.31, 'यही था भगवान का उपाय —'], [47.76, 49.11, 'कि परिश्रम दोनों करें,'], [49.57, 51.72, 'पर बल केवल देवताओं का बढ़े।'],
  [52.31, 53.29, 'पूरी कथा देखिए —'], [53.68, 55.29, 'समुद्र मंथन के रहस्य।'], [55.75, 56.60, 'जय श्री हरि।'],
];
export const cueAt = t => { for (let i = 0; i < CUES.length; i++) { const [a, b, s] = CUES[i], nx = CUES[i + 1] ? CUES[i + 1][0] : DUR; if (t >= a && t < Math.min(nx, b + .6)) return [s, t - a]; } return null; };
export function pr(t, t0, t1 = 1e9, din = .5, dout = .6) {
  if (t < t0 || t > t1 + dout) return null;
  if (t < t0 + din) { const u = eo((t - t0) / din); return { a: u, k: 1 + .2 * (1 - u), b: 12 * (1 - u) }; }
  if (t > t1) { const u = ss((t - t1) / dout); return { a: 1 - u, k: 1 + .25 * u, b: 14 * u }; }
  return { a: 1, k: 1, b: 0 };
}
const pulse = (t, t0) => t < t0 ? 0 : Math.exp(-(t - t0) * 2.2);

const MB = [540, GY + 40], MS = .85, PEAK = [540, GY + 40 - 690 * MS];
const ROPE_Y = GY - 190, VX = 610, MOUTH = [VX - 500, ROPE_Y - 205];
const END = 52.0;

export function frame(t) {
  const items = [];
  const add = (id, M, t0, t1, o = {}) => { const e = pr(t, t0, t1, o.din, o.dout); if (!e) return; items.push({ id, M: mul(M, Sc(e.k)), a: e.a * (o.a ?? 1), b: e.b, t0, jit: o.jit ?? 1 }); };
  const flick = Math.floor(t * 12) % 2;

  // —— 1 · hook: the serpent's head breathing fire, a daitya before it ——
  add('hook', place(540, 400, 1), 1.51, 7.6);
  add('vasuki', place(360 + 528 * 1.6, 1060 + 214 * 1.6, 1.6), .2, 7.6, { din: .7, jit: 0 });
  add('daitya0', place(830, GY + 60, .78, -1, .08 + .06 * ss(seg(t, 4.2, 5))), 2.6, 7.6);
  if (t > 3.9 && t < 7.7) add('fire' + flick, place(405, 1045, 1.45 + .15 * Math.sin(t * 6), 1, 1.62), 3.9, 7.5, { din: .3, jit: 0 });

  // —— the churning tableau: 8.55 → 52 ——
  const churn = ss(seg(t, 21.88, 22.6)), ph = Math.max(0, t - 21.88) * 2.2, pull = churn * Math.sin(ph * Math.PI);
  add('sea0', place(0, GY - 10 + (1 - eo(seg(t, 8.55, 9.3))) * 300), 8.55, END, { jit: 0 });
  add('mandaraB', place(MB[0], MB[1], MS, 1, churn * .018 * Math.sin(ph * Math.PI * .5)), 10.17, END, { jit: 0 });
  const ve = pr(t, 12.6, END);
  if (ve) {
    for (let k = 0; k < 4; k++) { const off = (ph * 34 + k * 90) % 360, y = MB[1] - 430 * MS + off * .8 * MS, edge = Math.sin(off / 360 * Math.PI); items.push({ id: 'wrap', M: mul(place(540, y, MS), Sc(ve.k)), a: ve.a * edge, b: ve.b, t0: 12.6, jit: 0 }); }
    items.push({ id: 'vasuki', M: mul(place(VX + pull * 16, ROPE_Y), Sc(ve.k)), a: ve.a, b: ve.b, t0: 12.6, jit: 0 });
  }
  // the daityas, placed at the head: they weaken in the flames
  const scorch = ss(seg(t, 28.47, 31.0));
  add('daitya0', place(235, GY + 12 + scorch * 22, .72, 1, -.07 - .05 * pull - scorch * .14), 15.28, END);
  add('daitya1', place(130, GY + 12 + scorch * 22, .68, 1, -.07 - .05 * pull - scorch * .12), 15.5, END);
  // the devas, at the tail
  const lift = ss(seg(t, 37.5, 40.5));
  add('deva0', place(868, GY + 12 - lift * 8, .72, -1, .07 + .05 * pull), 18.84, END);
  add('deva1', place(985, GY + 12 - lift * 8, .68, -1, .07 + .05 * pull), 19.1, END);
  // Vishnu stands between them while he places them
  add('vishnu', place(540, GY + 140, .5), 15.28, 21.7, { din: .6 });
  add('sea1', place(0, GY + 120 + (1 - eo(seg(t, 8.55, 9.3))) * 340), 8.55, END, { jit: 0 });

  // fire from every breath (a pulse every 1.6 s), strongest on "एक ओर अग्नि"
  const breath = t > 23.6 && t < END ? .55 + .45 * Math.max(0, Math.sin((t - 23.6) / 1.6 * Math.PI * 2)) + 1.0 * pulse(t, 43.2) : 0;
  if (breath > .05) add('fire' + flick, place(MOUTH[0] + 40, MOUTH[1] + 30, .55 + .45 * breath, 1, 1.9), 23.73, END, { din: .4, jit: 0, a: clamp(breath) });
  for (let i = 0; i < 4; i++) { const st = 28.6 + i * .7; if (t > st && t < st + 3.2 && t < END) { const u = seg(t, st, st + 3.2); add('smoke' + (i % 2), place(150 + i * 45 + Math.sin(t + i) * 20, GY - 340 - u * 420, .7 + u * .7, 1, Math.sin(t * .8 + i) * .2), st, END, { a: Math.sin(u * Math.PI) * .8, din: .01, jit: 0 }); } }
  // clouds from the same breath drift along to the tail and rain on the devas
  const cl = [[32.18, 860, 560, 1.05], [32.7, 1000, 660, .85]];
  cl.forEach(([t0, x, y, s], i) => {
    const u = ss(seg(t, t0, t0 + 3.6));
    add('cloud', place(lerp(MOUTH[0] + 40, x, u), lerp(MOUTH[1] - 80, y, u), lerp(.35, s, u)), t0, END, { din: .6, jit: 0 });
    const rainOn = ss(seg(t, 36.7, 37.2)) * (1 - ss(seg(t, 41.4, 41.9))) + pulse(t, 44.33) * 1.2;
    if (rainOn > .03) add('rain' + flick, place(x, y + 50, s), 36.7, END, { din: .01, a: clamp(rainOn), jit: 0 });
  });
  for (let i = 0; i < 18; i++) { const st = 38.0 + hash(i) * 3.0; if (t < st || t > st + 1.4) continue; const u = (t - st) / 1.4; add('spark', place(830 + hash(i * 3) * 200, GY - 60 - u * 360, 1.2, 1, t * 3 + i), st, st + 1.1, { din: .15, dout: .3, a: Math.sin(u * Math.PI), jit: 0 }); }
  // the Lord's plan: vast upon the summit; strength flows only to the devas
  add('vishnu', place(PEAK[0], PEAK[1] + 8, .92), 45.91, END, { din: .7 });
  for (let i = 0; i < 24; i++) { const t0 = 49.5 + hash(i) * 1.6, d = 1.3; if (t < t0 || t > t0 + d) continue; const u = ss((t - t0) / d), tx = [868, 985][i % 2]; add('spark', place(lerp(PEAK[0], tx, u), lerp(PEAK[1] - 380, GY - 220, u) - Math.sin(u * Math.PI) * 160, 1.6, 1, t * 3 + i), t0, t0 + d - .3, { din: .2, dout: .3, a: Math.sin(u * Math.PI), jit: 0 }); }

  // —— end card ——
  add('title', place(540, 560, .9), 52.31, 1e9, { din: .6 });
  add('vishnu', place(540, GY + 80, 1.0), 53.68, 1e9, { din: .7 });

  // —— camera (kept inside the painted plate) ——
  const key = pts => { let c = pts[0][1]; for (let i = 1; i < pts.length; i++) { const [ta, ca] = pts[i - 1], [tb, cb] = pts[i]; if (t >= ta) c = ca.map((v, j) => lerp(v, cb[j], ss(seg(t, ta, tb)))); } return c; };
  const cam = key([[0, [540, 960, 1.04]], [8.3, [540, 960, 1.04]], [9.0, [540, 1000, 1.0]], [23.6, [540, 1000, 1.0]], [25.0, [450, 1020, 1.2]], [31.8, [450, 1020, 1.2]], [33.5, [500, 980, 1.12]], [36.4, [630, 1000, 1.2]], [41.4, [630, 1000, 1.2]], [42.2, [540, 1000, 1.0]], [45.6, [540, 1000, 1.0]], [46.6, [540, 940, 1.0]], [51.9, [540, 940, 1.0]], [52.6, [540, 960, 1.05]]]).slice();
  for (const h of [43.2, 44.33]) if (t >= h && t < h + .4) cam[2] += .05 * (1 - eo((t - h) / .4));

  const fire = t > 23.7 && t < 31.8 ? ss(seg(t, 23.7, 25)) * .7 : (t < 7.6 && t > 3.9 ? .5 : 0) + pulse(t, 43.2) * .6;
  const fade = ss(seg(t, 57.0, 57.6)) + (1 - ss(seg(t, 0, .25)));
  const flash = pulse(t, 45.91) * .3;
  return { items, cam, lamps: [], mood: { anger: clamp(fire), drain: 0, flash: clamp(flash), fade: clamp(fade), hero: t > 52.3 ? 1 : 0 } };
}

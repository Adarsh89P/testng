// Shared timeline toolkit for Shorts 5–9.
export const W = 1080, H = 1920, GY = 1300;
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
export const place = (x, y, s = 1, sx = 1, r = 0) => mul(mul(T(x, y), Sc(sx * s, s)), R(r));
export const pulse = (t, t0, k = 2.2) => t < t0 ? 0 : Math.exp(-(t - t0) * k);
export function pr(t, t0, t1 = 1e9, din = .5, dout = .6) {
  if (t < t0 || t > t1 + dout) return null;
  if (t < t0 + din) { const u = eo((t - t0) / din); return { a: u, k: 1 + .2 * (1 - u), b: 12 * (1 - u) }; }
  if (t > t1) { const u = ss((t - t1) / dout); return { a: 1 - u, k: 1 + .25 * u, b: 14 * u }; }
  return { a: 1, k: 1, b: 0 };
}
export const adder = (items, t) => (id, M, t0, t1, o = {}) => { const e = pr(t, t0, t1, o.din, o.dout); if (!e) return; items.push({ id, M: mul(M, Sc(e.k)), a: e.a * (o.a ?? 1), b: e.b, t0, jit: 0 }); };
export const key = (t, pts) => { let c = pts[0][1]; for (let i = 1; i < pts.length; i++) { const [ta, ca] = pts[i - 1], [tb, cb] = pts[i]; if (t >= ta) c = ca.map((v, j) => lerp(v, cb[j], ss(seg(t, ta, tb)))); } return c.slice(); };
export const rise = (t, t0, d = 1.0, h = 300) => h * (1 - eo(seg(t, t0, t0 + d)));
// subtitles longer than ~34 characters are split at the space nearest the middle, time shared by length
export function splitCues(cues, max = 34) {
  const out = [];
  for (const [a, b, s] of cues) {
    if ([...s].length <= max) { out.push([a, b, s]); continue; }
    const mid = s.length / 2; let best = -1;
    for (let i = 0; i < s.length; i++) if (s[i] === ' ' && (best < 0 || Math.abs(i - mid) < Math.abs(best - mid))) best = i;
    const s1 = s.slice(0, best), s2 = s.slice(best + 1), tm = a + (b - a) * s1.length / (s1.length + s2.length);
    out.push(...splitCues([[a, tm, s1], [tm, b, s2]], max));
  }
  return out;
}
export const makeCueAt = (CUES, DUR) => t => { for (let i = 0; i < CUES.length; i++) { const [a, b, s] = CUES[i], nx = CUES[i + 1] ? CUES[i + 1][0] : DUR; if (t >= a && t < Math.min(nx, b + .6)) return [s, t - a]; } return null; };

// —— reusable stagings ——
export const MB = [540, GY + 40], MS = .85, ROPE_Y = GY - 190;
export function seaBack(add, t, t0, t1) { add('sea0', place(0, GY - 10 + (1 - eo(seg(t, t0, t0 + .8))) * 300), t0, t1); }
export function seaFront(add, t, t0, t1) { add('sea1', place(0, GY + 120 + (1 - eo(seg(t, t0, t0 + .8))) * 340), t0, t1); }
export function tableau(add, items, t, t0, t1, churnAt = t0) {
  const churn = ss(seg(t, churnAt, churnAt + .7)), ph = Math.max(0, t - churnAt) * 2.2, pull = churn * Math.sin(ph * Math.PI);
  add('mandaraB', place(MB[0], MB[1], MS, 1, churn * .018 * Math.sin(ph * Math.PI * .5)), t0, t1);
  const ve = pr(t, t0 + .2, t1);
  if (ve) {
    for (let k = 0; k < 4; k++) { const off = (ph * 34 + k * 90) % 360, y = MB[1] - 430 * MS + off * .8 * MS; items.push({ id: 'wrap', M: mul(place(540, y, MS), Sc(ve.k)), a: ve.a * Math.sin(off / 360 * Math.PI), b: ve.b, t0: t0 + .2, jit: 0 }); }
    items.push({ id: 'vasuki', M: mul(place(610 + pull * 16, ROPE_Y), Sc(ve.k)), a: ve.a, b: ve.b, t0: t0 + .2, jit: 0 });
  }
  add('daitya0', place(235, GY + 12, .72, 1, -.07 - .05 * pull), t0 + .3, t1);
  add('daitya1', place(130, GY + 12, .68, 1, -.07 - .05 * pull), t0 + .4, t1);
  add('deva0', place(868, GY + 12, .72, -1, .07 + .05 * pull), t0 + .3, t1);
  add('deva1', place(985, GY + 12, .68, -1, .07 + .05 * pull), t0 + .4, t1);
}
export function sparkRing(add, t, t0, t1, cx, cy, r = 160, n = 12) {
  if (t < t0 || t > t1 + .4) return;
  for (let i = 0; i < n; i++) { const a = i / n * 2 * Math.PI + t * .8, rr = r * (1 + .15 * Math.sin(t * 3 + i)); add('spark', place(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * .8, 1.1 + .4 * Math.sin(t * 4 + i), 1, t * 2 + i), t0, t1, { din: .3, a: .9 }); }
}
export function sparkRise(add, t, t0, t1, x0, x1, y0, h = 400, n = 14, seed = 1) {
  for (let i = 0; i < n; i++) { const st = t0 + hash(i * 3.1 + seed) * Math.max(.1, t1 - t0 - 1.2); if (t < st || t > st + 1.4) continue; const u = (t - st) / 1.4; add('spark', place(lerp(x0, x1, hash(i * 7 + seed)), y0 - u * h, 1.2, 1, t * 3 + i), st, st + 1.1, { din: .15, dout: .3, a: Math.sin(u * Math.PI) }); }
}
export function endCard(add, t, t0, tv, withLakshmi = false) {
  add('title', place(540, 560, .9), t0, 1e9, { din: .6 });
  if (withLakshmi) { add('lakshmi', place(400, GY + 80, .85), tv, 1e9, { din: .7 }); add('vishnu', place(700, GY + 80, .9, -1), tv, 1e9, { din: .7 }); }
  else add('vishnu', place(540, GY + 80, 1.0), tv, 1e9, { din: .7 });
}

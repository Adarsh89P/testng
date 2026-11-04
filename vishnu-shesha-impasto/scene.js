// Vishnu on Shesha (Anantashayana) — Impasto Oil Painting test frame
// Engine (engine/impasto.js, engine/plate.js) copied from the library's Impasto style.
// A flat, value-planned reference illustration is painted with Ref, then turned into
// palette-knife strokes by paintRef; light then rakes across the paint height field.
import { Impasto, Strokes, KNIFE, DAB, hex } from './engine/impasto.js';
import { Ref, paintRef } from './engine/plate.js';

const W = 1920, H = 1080, PI = Math.PI;
const lin = (x0, y0, x1, y1, stops) => c => { const g = c.createLinearGradient(x0, y0, x1, y1); stops.forEach(([o, col]) => g.addColorStop(o, col)); return g; };
const rad = (x, y, r0, r1, stops) => c => { const g = c.createRadialGradient(x, y, r0, x, y, r1); stops.forEach(([o, col]) => g.addColorStop(o, col)); return g; };
const Ell = (x, y, rx, ry, rot = 0) => c => c.ellipse(x, y, rx, ry, rot, 0, 2 * PI);

// —— geometry helpers ——
function curve(ctrl, per = 12) {
  const out = [], n = ctrl.length;
  for (let i = 0; i < n - 1; i++) {
    const p0 = ctrl[Math.max(0, i - 1)], p1 = ctrl[i], p2 = ctrl[i + 1], p3 = ctrl[Math.min(n - 1, i + 2)];
    for (let k = 0; k < per; k++) {
      const t = k / per, t2 = t * t, t3 = t2 * t;
      out.push([0, 1].map(j => .5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)));
    }
  }
  out.push(ctrl[n - 1]); return out;
}
const line = (a, b, n = 10) => Array.from({ length: n + 1 }, (_, i) => [a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n]);
const arcPts = (cx, cy, r, a0, a1, n = 14) => Array.from({ length: n + 1 }, (_, i) => { const a = a0 + (a1 - a0) * i / n; return [cx + Math.cos(a) * r, cy + Math.sin(a) * r]; });
function outline(pts, w, round = true) {
  const n = pts.length, L = [], R = [], wf = u => (typeof w === 'function' ? w(u) : w) / 2;
  for (let i = 0; i < n; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const l = Math.hypot(dx, dy) || 1; dx /= l; dy /= l;
    const ww = wf(i / (n - 1));
    L.push([pts[i][0] - dy * ww, pts[i][1] + dx * ww]); R.push([pts[i][0] + dy * ww, pts[i][1] - dx * ww]);
  }
  const cap = (e, sgn) => {
    const a = pts[Math.max(0, e - 1)], b = pts[Math.min(n - 1, e + 1)], ang = Math.atan2(b[1] - a[1], b[0] - a[0]) + (sgn > 0 ? 0 : PI), ww = wf(e / (n - 1)), o = [];
    for (let k = 1; k < 12; k++) { const t = ang + PI / 2 - k * PI / 12; o.push([pts[e][0] + Math.cos(t) * ww, pts[e][1] + Math.sin(t) * ww]); }
    return o;
  };
  return round ? [...L, ...cap(n - 1, 1), ...R.reverse(), ...cap(0, -1)] : [...L, ...R.reverse()];
}
const Poly = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
const Smooth = pts => c => {
  const n = pts.length, m = i => [(pts[i % n][0] + pts[(i + 1) % n][0]) / 2, (pts[i % n][1] + pts[(i + 1) % n][1]) / 2];
  const s = m(0); c.moveTo(s[0], s[1]); for (let i = 1; i <= n; i++) { const p = pts[i % n], q = m(i); c.quadraticCurveTo(p[0], p[1], q[0], q[1]); } c.closePath();
};
const xf = (pts, x, y, a, s = 1) => pts.map(([px, py]) => [x + (px * Math.cos(a) - py * Math.sin(a)) * s, y + (px * Math.sin(a) + py * Math.cos(a)) * s]);

// —— the same staging as the shadow-puppet frame ——
const SPINE = [
  ...curve([[1720, 940], [1640, 912], [1540, 892], [1440, 884]], 10),
  ...line([1440, 884], [520, 884], 40).slice(1),
  ...arcPts(520, 850, 34, PI / 2, 1.5 * PI).slice(1),
  ...line([520, 816], [1390, 816], 40).slice(1),
  ...arcPts(1390, 784, 32, PI / 2, -PI / 2).slice(1),
  ...line([1390, 752], [540, 752], 40).slice(1),
  ...curve([[540, 752], [470, 736], [432, 680], [426, 600], [450, 520], [500, 456], [560, 418]], 10).slice(1)
];
const HALO = [700, 500], CHAKRA = [852, 474];

function drawRef(R) {
  // 1 · sky: night cobalt at the top, warming to peach and gold toward the halo and the horizon
  R.fill(Poly([[0, 0], [W, 0], [W, 900], [0, 900]]), lin(0, 0, 0, 900, [[0, '#141c48'], [.35, '#2c3274'], [.7, '#7a5a8e'], [1, '#e2a274']]), { dir: -6, fallback: -6, group: 'sky', maxR: 60, detail: 2.4 });
  // the divine radiance behind the god, laid in the sky's group so its edge is lost, strokes radiating out
  R.fill(Ell(HALO[0], HALO[1], 470, 400), rad(HALO[0], HALO[1], 30, 470, [[0, '#fff2c0'], [.28, '#f8d27a'], [.6, '#e49a62'], [1, 'rgba(122,90,142,0)']]), { dir: { radial: HALO }, group: 'sky', maxR: 44, detail: 1.6 });
  // 2 · the Ocean of Milk: cream crests over cool lilac troughs, horizontal knife planes
  R.fill(Poly([[0, 860], [W, 860], [W, H], [0, H]]), lin(0, 860, 0, H, [[0, '#f4e8d0'], [.4, '#cbbcd0'], [1, '#6e6490']]), { dir: 0, fallback: 0, group: 'sea', maxR: 28, aj: .2 });
  for (let k = 0; k < 6; k++) {
    const y = 900 + k * 30 + (k % 2) * 6;
    R.fill(c => { c.moveTo(0, y); for (let x = 0; x <= W; x += 40) c.lineTo(x, y + Math.sin(x / 90 + k * 1.7) * 7); c.lineTo(W, y + 9); for (let x = W; x >= 0; x -= 40) c.lineTo(x, y + 9 + Math.sin(x / 90 + k * 1.7) * 7); c.closePath(); },
      k % 2 ? 'rgba(110,98,150,.55)' : 'rgba(255,246,226,.75)', { dir: 0, group: 'sea', maxR: 14, aj: .15 });
  }

  // 3 · Shesha: one long body; each coil lit from above, shadowed below
  const body = outline(SPINE, u => u < .1 ? 10 + 54 * Math.sin(u / .1 * PI / 2) : u > .86 ? 64 - 14 * (u - .86) / .14 : 64, false);
  R.fill(Poly(body), '#2f7a5e', { dir: 0, follow: 6, group: 'shesha', maxR: 14, hgt: 1.15 });
  // shading painted only inside the serpent's own silhouette
  const inBody = (rect, fillFn) => { const c = R.ctx; c.save(); c.beginPath(); Poly(body)(c); c.clip(); c.beginPath(); Poly(rect)(c); c.fillStyle = fillFn(c); c.fill(); c.restore(); };
  for (const [y, x0, x1] of [[884, 440, 1780], [816, 440, 1440], [752, 500, 1440]])
    inBody([[x0, y - 34], [x1, y - 34], [x1, y + 34], [x0, y + 34]], lin(0, y - 32, 0, y + 32, [[0, '#9fdcae'], [.35, '#4ea27a'], [.75, '#1f5a48'], [1, '#123c34']]));
  inBody([[380, 400], [600, 400], [600, 718], [380, 718]], lin(400, 0, 580, 0, [[0, '#164838'], [.5, '#3f9270'], [1, '#8fd2a4']]));
  // pale belly scales on the inside of the neck
  R.line(c => { const p = curve([[478, 742], [452, 690], [446, 600], [466, 520], [512, 462]], 8); c.moveTo(...p[0]); p.forEach(q => c.lineTo(...q)); }, '#d8d49a', 14, { group: 'belly', maxR: 4, dir: 'edge' });
  // the hood canopy
  const B = [566, 420];
  [[-.72, .84], [-.42, .94], [-.12, 1.02], [.18, 1.1], [.48, 1.02], [.78, .94], [1.08, .84]].forEach(([a, s], i) => {
    const L = 175 * s, bx = B[0] + Math.sin(a) * 26, by = B[1] - Math.cos(a) * 26 + Math.abs(a) * 14;
    const outer = xf([[-11, 0], [-20, -L * .3], [-36, -L * .58], [-44, -L * .76], [-36, -L * .92], [-18, -L * .99], [0, -L * .97], [18, -L * .99], [36, -L * .92], [44, -L * .76], [36, -L * .58], [20, -L * .3], [11, 0]], bx, by, a);
    const inner = xf([[-5, -L * .16], [-14, -L * .38], [-28, -L * .6], [-32, -L * .76], [-22, -L * .87], [0, -L * .85], [22, -L * .87], [32, -L * .76], [28, -L * .6], [14, -L * .38], [5, -L * .16]], bx, by, a);
    const [hx, hy] = xf([[0, -L * 1.0]], bx, by, a)[0];
    R.fill(Smooth(outer), lin(hx - 60, hy, hx + 60, hy, [[0, '#1c5a46'], [.5, '#3c9272'], [1, '#246a52']]), { dir: (a * 180 / PI) - 90, follow: 6, group: 'hood' + i, maxR: 9, hgt: 1.1 });
    R.fill(Smooth(inner), lin(hx, hy, bx, by, [[0, '#f6e6a8'], [1, '#c9b070']]), { dir: (a * 180 / PI) - 90, group: 'hoodin' + i, maxR: 7 });
    for (const sx of [-13, 13]) { const [mx, my] = xf([[sx, -L * .72]], bx, by, a)[0]; R.fill(Ell(mx, my, 7, 7), '#1a3a30', { maxR: 2.5, group: 'spec' + i + sx }); }
    R.fill(Ell(hx, hy - 6, 17, 13, a), '#2c7a5c', { maxR: 5, group: 'shd' + i });
    for (const ex of [-7, 7]) { const [qx, qy] = xf([[ex, -L * 1.0 - 8]], bx, by, a)[0]; R.fill(Ell(qx, qy, 3, 2.4), '#f4d040', { maxR: 1.5, group: 'eye' + i + ex }); }
  });

  // 4 · Vishnu — ultramarine skin lit from the halo, cadmium-yellow silk, gold
  const skin = (x0, y0, x1, y1) => lin(x0, y0, x1, y1, [[0, '#6a8ae0'], [.5, '#3456b4'], [1, '#1c2d74']]);
  let gid = 0;
  const limb = (pts, w0, w1) => { const P = curve(pts, 8); R.fill(Poly(outline(P, u => w0 + (w1 - w0) * u)), skin(P[0][0], P[0][1] - 30, P[0][0] + 40, P[0][1] + 40), { dir: 'edge', fallback: Math.atan2(P.at(-1)[1] - P[0][1], P.at(-1)[0] - P[0][0]) * 180 / PI, group: 'limb' + gid++, maxR: 6, hgt: 1.1 }); return P; };
  const bangle = (P, u, r) => { const [x, y] = P[Math.round(u * (P.length - 1))]; R.fill(Ell(x, y, r * .55, r), '#f2c447', { maxR: 2.5, group: 'bng' + gid++ }); };
  const hand = (p, a) => R.fill(Smooth(xf([[-8, -10], [10, -11], [20, -6], [22, 0], [18, 7], [6, 10], [-8, 9]], p[0], p[1], a)), '#4a6cd0', { maxR: 3, group: 'hand' + gid++ });
  const arm = (sh, el, hd) => { const A = limb([sh, el], 34, 26); bangle(A, .25, 13); const F = limb([el, hd], 26, 19); bangle(F, .9, 10); hand(hd, Math.atan2(hd[1] - el[1], hd[0] - el[0])); };
  arm([694, 676], [758, 604], [836, 530]);           // discus hand
  arm([678, 670], [700, 596], [736, 532]);           // conch hand
  arm([664, 684], [604, 738], [592, 666]);           // the arm that pillows the head
  // torso
  const T = curve([[662, 690], [740, 694], [820, 700], [905, 706]], 8);
  R.fill(Poly(outline(T, u => u < .4 ? 104 - 20 * u : u < .75 ? 96 - 60 * (u - .4) : 75 + 40 * (u - .75))), skin(660, 640, 760, 760), { dir: 0, follow: 8, group: 'torso', maxR: 9, hgt: 1.1 });
  R.line(c => { const p = curve([[680, 650], [722, 694], [792, 733], [868, 744], [912, 732]], 8); c.moveTo(...p[0]); p.forEach(q => c.lineTo(...q)); }, lin(680, 0, 912, 0, [[0, '#e8502e'], [.5, '#f07a3a'], [1, '#d63a2a']]), 15, { group: 'garland', maxR: 4, hgt: 1.3 });
  for (const [x, y] of [[700, 670], [750, 712], [810, 738], [868, 744]]) R.fill(Ell(x, y, 8, 8), '#fff0c8', { maxR: 2.5, group: 'flw' + x });
  R.line(c => { c.moveTo(690, 642); c.quadraticCurveTo(760, 700, 850, 752); }, '#f6ecc0', 3.5, { group: 'thread', maxR: 1.5, dir: 'edge' });
  R.line(c => { const p = curve([[650, 668], [672, 694], [700, 712]], 6); c.moveTo(...p[0]); p.forEach(q => c.lineTo(...q)); }, '#f2c447', 12, { group: 'neck', maxR: 3 });
  // pitambara
  const D = curve([[892, 708], [990, 712], [1088, 712]], 8);
  R.fill(Poly(outline(D, u => 100 - 42 * u)), lin(0, 656, 0, 760, [[0, '#ffe066'], [.45, '#f4bc2a'], [1, '#b87812']]), { dir: 'edge', fallback: 80, group: 'dhoti', maxR: 9, hgt: 1.2 });
  R.line(c => { const p = curve([[892, 756], [990, 740], [1088, 734]], 6); c.moveTo(...p[0]); p.forEach(q => c.lineTo(...q)); }, '#c8321e', 10, { group: 'hem', maxR: 3 });
  R.fill(Smooth([[890, 668], [918, 656], [930, 690], [910, 712], [886, 700]]), '#b8261c', { maxR: 4, group: 'knot' });
  // legs and feet
  const L1 = limb([[1060, 690], [1150, 678], [1222, 694]], 42, 26); bangle(L1, .92, 10);
  const L2 = limb([[1080, 714], [1170, 716], [1258, 718]], 46, 28); bangle(L2, .92, 10);
  for (const [x, y, a] of [[1258, 718, -.25], [1222, 694, -.35]]) R.fill(Smooth(xf([[-6, -12], [20, -16], [40, -12], [44, -4], [30, 6], [-4, 12]], x, y, a)), '#4466c8', { maxR: 3, group: 'foot' + x });
  // the resting arm with the gada
  arm([694, 704], [786, 742], [866, 716]);
  R.line(c => { c.moveTo(858, 724); c.lineTo(962, 618); }, '#7a4a1c', 7, { group: 'shaft', maxR: 2 });
  R.fill(Ell(972, 606, 24, 30, .78), rad(962, 594, 4, 34, [[0, '#fff2a0'], [.5, '#e8b030'], [1, '#9a6414']]), { dir: 'edge', group: 'gada', maxR: 5, hgt: 1.3 });
  // the head: profile facing the feet, a tall crown
  const N = [636, 668], HK = 1.5, hp = pts => pts.map(([x, y]) => [N[0] + x * HK, N[1] + y * HK]);
  R.fill(Smooth(hp([[-2, -64], [-18, -64], [-30, -58], [-34, -40], [-32, -14], [-26, 10], [-14, 18], [-6, 7], [-10, -10], [-9, -26], [-5, -40], [-6, -56]])), '#10142c', { dir: 90, group: 'hair', maxR: 4 });
  R.fill(Poly(hp([[-6, 8], [8, 6], [9, -6], [13, -12], [18, -15], [19.5, -19], [21, -21.5], [19.5, -23.2], [22.5, -24.5], [21.5, -28], [24, -29.5], [27.5, -32.5], [22, -42], [18.5, -52], [17.5, -60], [17, -65], [-2, -64], [-6, -56], [-5, -40], [-9, -26], [-10, -10]])),
    lin(N[0] - 15, 0, N[0] + 40, 0, [[0, '#2a3c90'], [.6, '#4a6cd0'], [1, '#7a98ec']]), { dir: 'edge', fallback: 90, group: 'face', maxR: 3, detail: .7 });
  R.fill(Ell(N[0] + 10 * HK, N[1] - 44 * HK, 5, 2.2), '#0c0f22', { maxR: 1.2, group: 'eye' });
  R.line(c => { c.moveTo(N[0] + 17 * HK, N[1] - 51 * HK); c.quadraticCurveTo(N[0] + 8 * HK, N[1] - 54 * HK, N[0] - 4 * HK, N[1] - 55 * HK); }, '#0c0f22', 3, { group: 'brow', maxR: 1.2 });
  R.line(c => { c.moveTo(N[0] + 14 * HK, N[1] - 62 * HK); c.lineTo(N[0] + 14 * HK, N[1] - 53 * HK); }, '#e83020', 3, { group: 'tilak', maxR: 1.2 });
  R.fill(Poly(hp([[-26, -62], [19, -64], [17, -80], [13, -108], [7, -132], [1, -142], [-5, -132], [-13, -108], [-20, -80]])), lin(N[0] - 30, 0, N[0] + 30, 0, [[0, '#a8701a'], [.45, '#f4c440'], [.7, '#fff0a8'], [1, '#d8a02a']]), { dir: 90, follow: 8, group: 'crown', maxR: 5, hgt: 1.4 });
  R.fill(Ell(N[0] - 3 * HK, N[1] - 96 * HK, 6, 7), '#d8202a', { maxR: 2, group: 'jewel' });
  R.fill(Ell(N[0] - 4 * HK, N[1] - 28 * HK, 10, 10), '#f2c447', { maxR: 2.5, group: 'ear' });
  // Sudarshana chakra: the purest, hottest colour in the picture
  const [cx, cy] = CHAKRA;
  R.fill(Ell(cx, cy, 84, 84), rad(cx, cy, 40, 84, [[0, '#ffd040'], [.5, '#ff8a2a'], [1, '#d8401c']]), { dir: { radial: CHAKRA }, group: 'flames', maxR: 7, hgt: 1.3 });
  R.fill(Ell(cx, cy, 52, 52), '#ffe27a', { dir: { radial: CHAKRA, off: 90 }, group: 'rim', maxR: 4, hgt: 1.4 });
  R.fill(Ell(cx, cy, 40, 40), '#fffbe6', { dir: { radial: CHAKRA }, group: 'wheel', maxR: 4 });
  for (let k = 0; k < 12; k++) { const a = k * PI / 6; R.line(c => { c.moveTo(cx + Math.cos(a) * 10, cy + Math.sin(a) * 10); c.lineTo(cx + Math.cos(a) * 40, cy + Math.sin(a) * 40); }, '#e8a020', 4, { group: 'spoke' + k, maxR: 1.6 }); }
  R.fill(Ell(cx, cy, 11, 11), '#d88a18', { maxR: 2.5, group: 'hub' });
  // Panchajanya
  R.fill(Smooth(xf([[-30, 6], [-26, -12], [-12, -26], [8, -30], [26, -20], [34, -4], [26, 12], [10, 26], [-4, 34], [-14, 26]], 744, 494, -.5)), rad(752, 480, 4, 42, [[0, '#fffaf0'], [.6, '#f0e2c8'], [1, '#b8a088']]), { dir: 'edge', group: 'conch', maxR: 4, hgt: 1.3 });
  // 5 · lotuses on the milk
  for (const [x, y, s] of [[300, 948, 1], [1580, 960, 1.1], [1130, 1000, .8]]) {
    R.fill(Ell(x, y + 8 * s, 62 * s, 12 * s), '#3c7a4a', { dir: 0, group: 'pad' + x, maxR: 6 });
    R.fill(c => { for (const a of [-1.05, -.62, -.25, .25, .62, 1.05, 0]) { const h = (a === 0 ? 72 : 70 - Math.abs(a) * 22) * s, pts = xf([[0, 0], [-15, -h * .4], [0, -h], [15, -h * .4]], x, y, a); Smooth(pts)(c); } },
      lin(0, y - 70 * s, 0, y, [[0, '#ffb0b0'], [.5, '#f05a6a'], [1, '#b42a4a']]), { dir: 'edge', fallback: 90, group: 'lotus' + x, maxR: 5, hgt: 1.2 });
  }
}

// reflections of the radiance on the milk: explicit stacks of short horizontal knife dabs
function reflections(st) {
  let s = 7;
  const r = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  for (const [x0, w, cols] of [[HALO[0], 220, ['#fff0c0', '#f8d27a', '#f0b070']], [CHAKRA[0], 90, ['#ffe27a', '#ff9a3a']]])
    for (let k = 0; k < 46; k++) {
      const y = 905 + r() * 160, spread = w * (.4 + (y - 900) / 220), x = x0 + (r() - .5) * 2 * spread;
      st.push({ x, y, ang: (r() - .5) * .08, len: 18 + r() * 40, wid: 4 + r() * 4, c: hex(cols[k % cols.length]), type: KNIFE, alpha: .85 - (y - 900) / 260, hgt: .7, seed: 500 + k });
    }
}

const canvasEl = document.getElementById('c');
const E = new Impasto(canvasEl, { W, H, ss: 2 });
const R = new Ref(W, H, 1);
drawRef(R);
const st = paintRef(R, { R: [44, 22, 11, 5.5, 2.8], T: 12, seed: 17 });
reflections(st);
const batch = E.batch(st.data()), tex = E.texture(R.ctx.canvas);
const cam = { x: W / 2, y: H / 2, zoom: 1 };

window.render = t => {
  E.begin();
  const o = { cam, t, grey: 0, reveal: -1e6 };
  E.under(tex, W, H, o); E.draw(batch, o);
  E.finish({ expo: 1.03, sat: 1.07, contrast: 1.05, vig: .3, spec: .28, shin: 26 });
};
window.DUR = 1;
window.render(0);
window.READY = true;

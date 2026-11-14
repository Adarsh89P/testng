// Style-neutral character & prop library for the series.
// Every character is a set of PARTS; a part is a list of SHAPES in local coordinates (facing right).
// Shapes carry a colour KEY, an optional carving pattern (for shadow puppetry) and optional oil hints.
// Two renderers read this: puppet.js (dyed hide, carved) and oil.js (palette-knife strokes).
//
// shape = { p: path(ctx), c: colourKey, pat?, ink? (outline width, 0 = none), open? (outline only: open-cut face),
//           line? (stroke p with width line), beads? ([[x,y]...], r), oil?: {maxR, dir}, rule? }
export const PI = Math.PI;

// —— path helpers (plain Canvas2D, no dependencies) ——
export const S = pts => c => { const n = pts.length, m = i => [(pts[i % n][0] + pts[(i + 1) % n][0]) / 2, (pts[i % n][1] + pts[(i + 1) % n][1]) / 2]; const s = m(0); c.moveTo(s[0], s[1]); for (let i = 1; i <= n; i++) { const p = pts[i % n], q = m(i); c.quadraticCurveTo(p[0], p[1], q[0], q[1]); } c.closePath(); };
export const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
export const L = pts => c => { c.moveTo(pts[0][0], pts[0][1]); if (pts.length === 2) { c.lineTo(pts[1][0], pts[1][1]); return; } for (let i = 1; i < pts.length - 1; i++) { const mx = (pts[i][0] + pts[i + 1][0]) / 2, my = (pts[i][1] + pts[i + 1][1]) / 2; c.quadraticCurveTo(pts[i][0], pts[i][1], mx, my); } c.lineTo(pts.at(-1)[0], pts.at(-1)[1]); };
export const E = (x, y, rx, ry, r = 0) => c => { c.moveTo(x + rx * Math.cos(r), y + rx * Math.sin(r)); c.ellipse(x, y, rx, ry, r, 0, 2 * PI); };
export const C = (x, y, r) => E(x, y, r, r);
export function curve(ctrl, per = 8) {
  const out = [], n = ctrl.length;
  for (let i = 0; i < n - 1; i++) {
    const p0 = ctrl[Math.max(0, i - 1)], p1 = ctrl[i], p2 = ctrl[i + 1], p3 = ctrl[Math.min(n - 1, i + 2)];
    for (let k = 0; k < per; k++) { const t = k / per, t2 = t * t, t3 = t2 * t; out.push([0, 1].map(j => .5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3))); }
  }
  out.push(ctrl[n - 1]); return out;
}
// a limb / band along control points, round ends; w = [w0, w1]
export function B(ctrl, w0, w1 = w0, round = true) {
  const pts = ctrl.length > 2 ? curve(ctrl) : curve(ctrl, 6), n = pts.length, Lf = [], R = [], wf = u => (w0 + (w1 - w0) * u) / 2;
  for (let i = 0; i < n; i++) { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)]; let dx = b[0] - a[0], dy = b[1] - a[1]; const l = Math.hypot(dx, dy) || 1; dx /= l; dy /= l; const ww = wf(i / (n - 1)); Lf.push([pts[i][0] - dy * ww, pts[i][1] + dx * ww]); R.push([pts[i][0] + dy * ww, pts[i][1] - dx * ww]); }
  const cap = (e, sg) => { const a = pts[Math.max(0, e - 1)], b = pts[Math.min(n - 1, e + 1)], ang = Math.atan2(b[1] - a[1], b[0] - a[0]) + (sg > 0 ? 0 : PI), ww = wf(e / (n - 1)), o = []; for (let k = 1; k < 10; k++) { const t = ang + PI / 2 - k * PI / 10; o.push([pts[e][0] + Math.cos(t) * ww, pts[e][1] + Math.sin(t) * ww]); } return o; };
  const out = round ? [...Lf, ...cap(n - 1, 1), ...R.reverse(), ...cap(0, -1)] : [...Lf, ...R.reverse()];
  return P(out);
}
// transform a path into a head's coordinate space (neck point N, scale k)
export const X = (N, k, path) => c => { c.save(); c.translate(N[0], N[1]); c.scale(k, k); path(c); c.restore(); };
const XP = (N, k, pts) => pts.map(([x, y]) => [N[0] + x * k, N[1] + y * k]);

// —— faces (profile, facing right; neck at 0,0; top of head ≈ −65) ——
export const FACE = [[-6, 6], [8, 6], [9, -6], [13, -12], [18, -15], [19.5, -19], [21, -21.5], [19.5, -23.2], [22.5, -24.5], [21.5, -28], [24, -29.5], [27.5, -32.5], [22, -42], [18.5, -52], [17.5, -60], [17, -65], [-2, -64], [-6, -56], [-5, -40], [-9, -26], [-10, -10]];
export const FACEF = [[-6, 6], [7, 6], [8, -6], [12, -12], [16, -15], [17.5, -19], [19, -21.5], [17.8, -23], [20.5, -24.5], [19.8, -28], [22, -30], [24.5, -33], [20, -42], [17, -52], [16.5, -60], [16, -65], [-2, -64], [-6, -56], [-5, -40], [-9, -26], [-10, -10]];
export function face(N, k, o = {}) {
  const F = o.female ? FACEF : FACE, sh = [];
  if (o.solid) sh.push({ p: X(N, k, P(F)), c: o.skin, ink: 2 });
  else sh.push({ p: X(N, k, L(F.slice(1, 17))), c: o.skinLine || 'ink', open: true, ink: 2.2, skin: o.skin || 'skin' });
  const eye = o.fierce ? [[17, -47], [5, -50], [14, -42]] : [[15, -44], [8, -47.5], [-1, -45.5]];
  sh.push({ p: X(N, k, L(eye)), c: 'ink', line: 1.6 });
  sh.push({ p: X(N, k, C(o.female ? 9.5 : 10, -44, 1.9)), c: 'ink', ink: 0 });
  sh.push({ p: X(N, k, S(o.fierce ? [[19, -53], [0, -60], [-6, -58], [2, -54], [12, -52]] : [[17.5, -51], [10, -53.5], [0, -55], [-6, -57], [-5, -55], [2, -52.4], [10, -50.8], [17, -49.4]])), c: 'ink', ink: 0 });
  sh.push({ p: X(N, k, L([[20.3, -23.4], [17, -21.6], [15, -22.8]])), c: o.female ? 'red' : 'ink', line: o.female ? 2 : 1.3 });
  return sh;
}
export const hairBack = (N, k, col = 'ink', long = 0) => ({ p: X(N, k, S([[-2, -64], [-18, -66], [-30, -58], [-34, -40], [-33, -14 + long * .4], [-27, 8 + long], [-15, 14 + long], [-6, 7], [-10, -10], [-9, -26], [-5, -40], [-6, -56]])), c: col, pat: { t: 'slits', n: 6 } });
export const crownTall = (N, k, h = 1) => ({ p: X(N, k, P([[-26, -62], [19, -64], [17, -84], [12, -112 * h], [5, -142 * h], [0, -152 * h], [-5, -142 * h], [-12, -112 * h], [-20, -84]])), c: 'gold', pat: { t: 'lattice', s: 7 }, oil: { maxR: 4, dir: 90 } });
export const earring = (N, k) => ({ p: X(N, k, C(-4, -28, 6.5)), c: 'gold', pat: { t: 'coin' } });
export const neck = (N, k, col) => ({ p: X(N, k, P([[-6, 2], [9, 2], [12, 16], [-8, 16]])), c: col, ink: 0 });

// generic arm part: pivot = shoulder at (0,0), hanging down; hand at HAND
export const HAND = [34, 170];
function armPart(skin, sleeve, o = {}) {
  const sh = [];
  sh.push({ p: B([[0, 0], [8, 90]], 26, 21), c: sleeve || skin });
  sh.push({ p: B([[8, 90], [34, 168]], 21, 16), c: skin });
  if (o.bangle) sh.push({ p: E(30, 152, 12, 6, 1.2), c: o.bangle, pat: { t: 'coin' } });
  sh.push({ p: S([[22, 160], [44, 162], [50, 178], [40, 188], [24, 184]]), c: skin });
  return { box: [-30, -30, 70, 200], shapes: sh };
}

// ================= CHARACTERS =================
// —— Durvasa: fierce sage. Saffron cloth, ash-marked forehead, tall matted jata, grey beard, rudraksha, staff ——
export function durvasa() {
  const N = [6, -405], k = 1.4, sh = [];
  sh.push({ p: B([[-62, -560], [-44, 8]], 8, 8), c: 'wood' });                           // staff
  sh.push({ p: B([[-6, -250], [-30, -130], [-40, -8]], 30, 20), c: 'skinAsh' });
  sh.push({ p: B([[10, -250], [28, -130], [44, -8]], 30, 20), c: 'skinAsh' });
  for (const x of [-40, 44]) sh.push({ p: S([[x - 12, -12], [x + 24, -12], [x + 28, 2], [x - 14, 4]]), c: 'skinAsh' });
  sh.push({ p: P([[-46, -305], [44, -305], [54, -220], [60, -122], [30, -110], [4, -118], [-24, -108], [-50, -118], [-60, -220]]), c: 'saffron', pat: { t: 'folds' } });
  sh.push({ p: B([[-50, -300], [0, -290], [50, -298]], 16, 16, false), c: 'saffron2' });
  sh.push({ p: B([[-20, -385], [-46, -322], [-48, -258]], 22, 17), c: 'skinAsh' });       // back arm on the staff
  sh.push({ p: C(-47, -250, 11), c: 'skinAsh' });
  sh.push({ p: S([[-36, -300], [-42, -350], [-34, -394], [0, -410], [32, -396], [42, -350], [36, -300]]), c: 'skinAsh', pat: { t: 'ribs' } });
  sh.push({ p: B([[-34, -396], [2, -350], [36, -304]], 24, 24, false), c: 'saffron2', pat: { t: 'folds' } });   // uttariya
  sh.push({ beads: curve([[-12, -402], [4, -352], [24, -318], [30, -306]]), r: 4.2, c: 'rudraksha' });
  sh.push(neck(N, k, 'skinAsh'));
  sh.push(hairBack(N, k, 'hairBrown', 22));
  sh.push({ p: X(N, k, S([[-24, -60], [-30, -82], [-22, -104], [-6, -114], [8, -104], [8, -80], [0, -64]])), c: 'hairBrown', pat: { t: 'coils' } });   // jata
  sh.push({ beads: XP(N, k, [[-24, -76], [-14, -78], [-4, -78], [5, -77]]), r: 3, c: 'rudraksha' });
  sh.push(...face(N, k, { fierce: true, skin: 'skinAsh' }));
  sh.push({ p: X(N, k, S([[8, -8], [21, -16], [23, -4], [18, 16], [8, 36], [-6, 40], [-12, 22], [-8, 2]])), c: 'beard', pat: { t: 'slits', n: 5 } });
  for (const y of [-61, -58, -55]) sh.push({ p: X(N, k, L([[4, y], [16.5, y]])), c: 'ashMark', line: 1.8 });   // tripundra
  sh.push({ p: X(N, k, C(13, -57.5, 1.4)), c: 'red', ink: 0 });
  return { body: { box: [-110, -600, 110, 20], shapes: sh }, arm: armPart('skinAsh', null, { bangle: 'rudraksha' }), shoulder: [14, -388] };
}

// —— Vidyadhari: celestial maiden in flight. Origin at the hip ——
export function vidyadhari() {
  const N = [6, -122], k = 1.28, sh = [];
  sh.push({ p: B([[-30, -100], [-90, -200], [10, -250], [112, -196], [86, -120]], 14, 10), c: 'jade', pat: { t: 'beads' } });   // scarf
  sh.push({ p: B([[-4, -104], [-40, -140], [-58, -184]], 17, 12), c: 'skinF' });
  sh.push({ p: C(-60, -190, 9), c: 'skinF' });
  sh.push({ p: S([[-30, -22], [30, -22], [44, 26], [-14, 70], [-110, 62], [-180, 30], [-120, 8]]), c: 'red', pat: { t: 'lattice', s: 11 } });
  sh.push({ p: B([[-150, 34], [-80, 50], [0, 40]], 8, 8, false), c: 'gold' });
  sh.push({ p: S([[-22, -20], [-26, -70], [-16, -112], [8, -120], [26, -106], [28, -62], [20, -20]]), c: 'gold', pat: { t: 'scales' } });
  sh.push({ p: B([[14, -108], [60, -82], [104, -86]], 17, 12), c: 'skinF' });                 // arm forward, holding the garland
  sh.push({ p: C(110, -86, 9), c: 'skinF' });
  sh.push({ beads: curve([[-10, -112], [4, -96], [20, -104]]), r: 3, c: 'gold' });
  sh.push(neck(N, k, 'skinF'));
  sh.push({ p: X(N, k, S([[-2, -64], [-18, -68], [-32, -58], [-36, -30], [-36, 10], [-30, 40], [-18, 44], [-8, 8], [-10, -10], [-9, -26], [-5, -40], [-6, -56]])), c: 'ink', pat: { t: 'slits', n: 7 } });
  sh.push({ p: X(N, k, C(-24, -66, 12)), c: 'ink', pat: { t: 'plum', at: [[-24, -66]], r: 4 } });
  sh.push(...face(N, k, { female: true, skin: 'skinF' }));
  sh.push({ p: X(N, k, C(15, -55, 1.6)), c: 'red', ink: 0 });
  sh.push(earring(N, k));
  return { body: { box: [-200, -270, 140, 90], shapes: sh }, hand: [110, -82] };
}

// —— Indra: king of the devas, seated. Tall gold crown, red armour, the vajra. Origin at the seat ——
export function indra() {
  const N = [6, -148], k = 1.38, sh = [];
  sh.push({ p: B([[-14, -128], [-44, -162], [-42, -214]], 20, 16), c: 'skinI' });
  sh.push({ p: B([[-42, -300], [-42, -190]], 9, 9), c: 'gold' });                              // vajra grip
  for (const y of [-300, -190]) { const s = y < -250 ? -1 : 1; sh.push({ p: P([[-42, y], [-60, y + s * 34], [-52, y + s * 14], [-42, y + s * 46], [-32, y + s * 14], [-24, y + s * 34]]), c: 'gold' }); }
  sh.push({ p: C(-44, -214, 10), c: 'skinI' });
  sh.push({ p: B([[-8, -18], [66, -8]], 40, 34), c: 'red2' });                               // thigh
  sh.push({ p: B([[66, -10], [78, 82]], 30, 22), c: 'skinI' });                               // shin
  sh.push({ p: S([[66, 80], [100, 78], [104, 92], [64, 94]]), c: 'skinI' });
  sh.push({ p: S([[-36, -20], [-42, -82], [-36, -132], [0, -150], [34, -136], [42, -82], [36, -20]]), c: 'red', pat: { t: 'scalesOpen' } });
  sh.push({ p: S([[-30, -132], [0, -150], [32, -134], [26, -110], [0, -102], [-24, -112]]), c: 'gold', pat: { t: 'lattice', s: 6 } });   // collar
  sh.push({ p: B([[-38, -30], [40, -30]], 14, 14, false), c: 'gold', pat: { t: 'coin' } });
  sh.push(neck(N, k, 'skinI'));
  sh.push(hairBack(N, k, 'ink', 6));
  sh.push(...face(N, k, { skin: 'skinI' }));
  sh.push({ p: X(N, k, L([[22, -25], [14, -27], [8, -24]])), c: 'ink', line: 1.6 });            // moustache
  sh.push(crownTall(N, k, 1.05));
  sh.push({ p: X(N, k, C(-2, -98, 5)), c: 'red', ink: 1 });
  sh.push(earring(N, k));
  return { body: { box: [-110, -380, 130, 110], shapes: sh }, arm: armPart('skinI', 'red', { bangle: 'gold' }), shoulder: [16, -132] };
}

// —— Airavata: the white elephant with four tusks. Origin on the ground under the body ——
export function airavata() {
  const sh = [];
  for (const [x, c] of [[-150, 'eleD'], [110, 'eleD'], [-112, 'ele'], [148, 'ele']]) { sh.push({ p: B([[x, -180], [x + 4, -8]], 58, 50), c, pat: { t: 'wrinkles' } }); sh.push({ p: L([[x - 18, -14], [x + 22, -14]]), c: 'ink', line: 1.4 }); }
  sh.push({ p: L([[-205, -260], [-232, -200], [-226, -150]]), c: 'ink', line: 3 });
  sh.push({ p: S([[-205, -170], [-196, -290], [-112, -352], [20, -362], [146, -334], [206, -272], [214, -192], [154, -142], [-150, -142]]), c: 'ele', pat: { t: 'wrinkles' } });
  sh.push({ p: S([[-136, -334], [86, -348], [104, -186], [-126, -182]]), c: 'red', pat: { t: 'lattice', s: 12 } });   // caparison
  sh.push({ p: B([[-130, -186], [-10, -180], [104, -188]], 12, 12, false), c: 'gold', pat: { t: 'coin' } });
  sh.push({ beads: curve([[-126, -176], [-10, -168], [100, -176]]), r: 5, c: 'gold' });
  sh.push({ p: S([[150, -332], [224, -354], [272, -322], [288, -260], [272, -200], [232, -170], [180, -182]]), c: 'ele' });
  sh.push({ p: S([[214, -350], [262, -340], [270, -300], [236, -292], [210, -312]]), c: 'gold', pat: { t: 'lattice', s: 6 } });   // forehead ornament
  sh.push({ p: S([[160, -322], [118, -300], [108, -228], [140, -186], [188, -210], [192, -284]]), c: 'eleD', pat: { t: 'wrinkles' } });   // ear
  sh.push({ p: C(246, -268, 4.5), c: 'ink', ink: 0 });
  for (const [y0, dx, c] of [[-196, 0, 'ivory'], [-186, -14, 'ivory2']]) { sh.push({ p: B([[250 + dx, y0], [296 + dx, y0 + 20], [330 + dx, y0 - 8]], 13, 4), c }); sh.push({ p: B([[244 + dx, y0 + 6], [288 + dx, y0 + 34], [318 + dx, y0 + 22]], 11, 4), c }); }
  return { body: { box: [-250, -380, 350, 10], shapes: sh }, trunk: { box: [-40, -20, 60, 240], shapes: [{ p: B([[0, 0], [16, 60], [14, 130], [0, 190], [-12, 216]], 44, 16), c: 'ele', pat: { t: 'rings' } }] }, trunkBase: [266, -212], trunkTip: [-12, 216], seat: [-30, -352], headTop: [226, -362] };
}

// —— devas and daityas (generic) ——
export function deva(v = 0) {
  const N = [8, -362], k = 1.45, sh = [], cl = v ? 'orange' : 'red';
  sh.push({ p: B([[-8, -190], [-58, -4]], 32, 22), c: cl }); sh.push({ p: B([[10, -190], [46, -4]], 32, 22), c: cl });
  for (const x of [-58, 46]) sh.push({ p: S([[x - 16, -12], [x + 24, -12], [x + 28, 4], [x - 18, 6]]), c: 'ink' });
  sh.push({ p: P([[-40, -262], [40, -262], [50, -205], [62, -128], [34, -116], [8, -124], [-18, -114], [-46, -122], [-64, -128], [-52, -205]]), c: 'gold', pat: { t: 'lattice', s: 11 } });
  sh.push({ p: S([[-32, -250], [-40, -300], [-32, -348], [0, -364], [32, -348], [42, -300], [34, -250]]), c: 'red', pat: { t: 'scalesOpen' } });
  sh.push({ p: B([[-38, -256], [40, -256]], 16, 16, false), c: 'gold', pat: { t: 'coin' } });
  sh.push({ p: B([[12, -338], [40, -290], [70, -262]], 22, 16), c: 'skin' }); sh.push({ p: C(74, -258, 11), c: 'skin' });
  sh.push(neck(N, k, 'skin')); sh.push(hairBack(N, k)); sh.push(...face(N, k)); sh.push(crownTall(N, k, .8));
  return { body: { box: [-110, -520, 120, 16], shapes: sh } };
}
export function daitya(v = 0) {
  const N = [8, -362], k = 1.45, sh = [], cl = v ? 'green' : 'crim';
  sh.push({ p: B([[-8, -190], [-58, -4]], 34, 24), c: cl }); sh.push({ p: B([[10, -190], [46, -4]], 34, 24), c: cl });
  for (const x of [-58, 46]) sh.push({ p: S([[x - 16, -12], [x + 24, -12], [x + 28, 4], [x - 18, 6]]), c: 'ink' });
  sh.push({ p: P([[-40, -262], [40, -262], [50, -205], [62, -128], [34, -116], [8, -124], [-18, -114], [-46, -122], [-64, -128], [-52, -205]]), c: 'jade', pat: { t: 'lattice', s: 11 } });
  sh.push({ p: S([[-34, -250], [-44, -300], [-34, -350], [0, -366], [34, -350], [46, -300], [36, -250]]), c: 'teal', pat: { t: 'scalesOpen' } });
  sh.push({ p: B([[12, -338], [52, -300], [96, -296]], 24, 18), c: 'skinD' });
  sh.push({ p: B([[96, -296], [150, -330]], 8, 8), c: 'wood' }); sh.push({ p: P([[146, -350], [176, -340], [156, -318]]), c: 'iron' });   // spear
  sh.push({ p: C(98, -294, 12), c: 'skinD' });
  sh.push(neck(N, k, 'skinD')); sh.push(hairBack(N, k));
  sh.push(...face(N, k, { solid: true, skin: 'skinD', fierce: true }));
  sh.push({ p: X(N, k, P([[18, -16], [22, -9], [15, -12]])), c: 'ivory', ink: 0 });
  for (const s of [1, -1]) sh.push({ p: X(N, k, P([[-6 + s * 8, -62], [-4 + s * 24, -94], [-14 + s * 34, -102], [-2 + s * 14, -82], [-14 + s * 2, -64]])), c: 'ivory' });
  sh.push({ p: X(N, k, P([[-24, -62], [18, -64], [10, -78], [4, -70], [-4, -84], [-10, -70], [-18, -80]])), c: 'red' });
  return { body: { box: [-110, -520, 190, 16], shapes: sh } };
}

// —— Vishnu: blue, four-armed, kirita crown, yellow silk, chakra, conch, gada, lotus ——
export function vishnu() {
  const N = [8, -410], k = 1.5, sh = [];
  sh.push(...chakraShapes(-70, -560, 44));                                                           // upper back hand: chakra
  sh.push({ p: B([[-14, -388], [-60, -470], [-68, -530]], 22, 16), c: 'skinV' }); sh.push({ p: C(-68, -534, 11), c: 'skinV' });
  sh.push({ p: B([[-10, -380], [-54, -320], [-60, -250]], 22, 16), c: 'skinV' });                    // lower back hand on the gada
  sh.push({ p: B([[-60, -260], [-70, -40]], 9, 9), c: 'wood' }); sh.push({ p: E(-60, -262, 22, 28), c: 'gold', pat: { t: 'scales' } });
  sh.push({ p: B([[-8, -250], [-34, -130], [-38, -8]], 32, 22), c: 'skinV' }); sh.push({ p: B([[12, -250], [26, -130], [40, -8]], 32, 22), c: 'skinV' });
  for (const x of [-38, 40]) { sh.push({ p: S([[x - 14, -12], [x + 24, -12], [x + 28, 4], [x - 16, 6]]), c: 'skinV' }); sh.push({ p: E(x, -26, 14, 6), c: 'gold', pat: { t: 'coin' } }); }
  sh.push({ p: P([[-46, -300], [46, -300], [56, -210], [64, -108], [36, -96], [8, -104], [-20, -94], [-48, -104], [-64, -110], [-56, -210]]), c: 'gold', pat: { t: 'lattice', s: 11 } });
  sh.push({ p: B([[-50, -120], [0, -104], [54, -118]], 10, 10, false), c: 'red' });
  sh.push({ p: S([[-38, -300], [-44, -350], [-36, -398], [0, -414], [34, -400], [44, -350], [38, -300]]), c: 'skinV', pat: { t: 'plums' } });
  sh.push({ p: B([[-30, -394], [-8, -330], [20, -300], [40, -300]], 13, 13, false), c: 'red', pat: { t: 'beads' } });     // vanamala
  sh.push({ p: L([[-26, -398], [10, -340], [34, -300]]), c: 'gold', line: 2.4 });                     // sacred thread
  sh.push({ p: B([[16, -388], [62, -460], [70, -520]], 22, 16), c: 'skinV' }); sh.push({ p: C(72, -524, 11), c: 'skinV' });
  sh.push(...conchShapes(82, -552, 1));                                                              // upper front hand: conch
  sh.push({ p: B([[18, -380], [50, -330], [70, -330]], 22, 16), c: 'skinV' });                       // lower front hand: lotus
  sh.push(...lotusShapes(86, -340, .55));
  sh.push(neck(N, k, 'skinV')); sh.push(hairBack(N, k, 'ink', 14)); sh.push(...face(N, k, { skinLine: 'skinV', skin: 'skinV' }));
  sh.push({ p: X(N, k, L([[14.2, -62], [14.2, -54]])), c: 'red', line: 2.2 });
  sh.push(crownTall(N, k, 1.0)); sh.push(earring(N, k));
  return { body: { box: [-130, -660, 140, 20], shapes: sh } };
}
// —— Shiva: ash-blue, matted jata with the crescent moon and Ganga, serpent at the throat, tiger skin, trident ——
export function shiva() {
  const N = [8, -410], k = 1.5, sh = [];
  sh.push({ p: B([[-60, -640], [-60, -10]], 9, 9), c: 'wood' });
  sh.push({ p: P([[-104, -650], [-100, -610], [-70, -598], [-66, -640], [-60, -680], [-54, -640], [-50, -598], [-20, -610], [-16, -650], [-30, -616], [-50, -604], [-60, -606], [-70, -604], [-90, -616]]), c: 'iron', pat: { t: 'lattice', s: 7 } });
  sh.push({ p: P([[-88, -580], [-32, -580], [-56, -556], [-32, -530], [-88, -530], [-64, -556]]), c: 'red', pat: { t: 'lattice', s: 7 } });   // damaru
  sh.push({ p: B([[-14, -388], [-48, -320], [-60, -250]], 22, 16), c: 'skinS' }); sh.push({ p: C(-60, -246, 11), c: 'skinS' });
  sh.push({ p: B([[-8, -250], [-34, -130], [-38, -8]], 32, 22), c: 'skinS' }); sh.push({ p: B([[12, -250], [26, -130], [40, -8]], 32, 22), c: 'skinS' });
  for (const x of [-38, 40]) sh.push({ p: S([[x - 14, -12], [x + 24, -12], [x + 28, 4], [x - 16, 6]]), c: 'skinS' });
  sh.push({ p: S([[-50, -300], [50, -300], [66, -190], [40, -150], [0, -170], [-40, -146], [-66, -190]]), c: 'tiger', pat: { t: 'stripes' } });
  sh.push({ p: S([[-38, -300], [-44, -350], [-36, -398], [0, -414], [34, -400], [44, -350], [38, -300]]), c: 'skinS', pat: { t: 'ribs' } });
  sh.push({ p: B([[-34, -404], [0, -382], [30, -398], [36, -380], [0, -366], [-30, -380]], 16, 12), c: 'serpent', pat: { t: 'scales' } });   // serpent at the throat
  sh.push({ p: E(40, -372, 12, 9, -.4), c: 'serpent' });
  sh.push({ beads: curve([[-20, -396], [2, -340], [30, -310]]), r: 4, c: 'rudraksha' });
  sh.push({ p: B([[16, -388], [56, -330], [84, -296]], 22, 16), c: 'skinS' }); sh.push({ p: C(88, -292, 11), c: 'skinS' });   // abhaya
  sh.push(neck(N, k, 'skinS'));
  sh.push(hairBack(N, k, 'hairBrown', 30));
  sh.push({ p: X(N, k, S([[-26, -60], [-32, -86], [-24, -114], [-6, -124], [10, -112], [10, -84], [0, -64]])), c: 'hairBrown', pat: { t: 'coils' } });
  sh.push({ p: X(N, k, P([[6, -118], [22, -124], [30, -112], [24, -116], [12, -112]])), c: 'moon' });   // crescent
  sh.push({ p: X(N, k, L([[-12, -122], [-22, -140], [-16, -158]])), c: 'ganga', line: 4 });
  sh.push(...face(N, k, { skinLine: 'skinS', skin: 'skinS' }));
  sh.push({ p: X(N, k, E(14, -58, 1.4, 3.2)), c: 'red', ink: 0 });                                      // third eye
  for (const y of [-63, -61]) sh.push({ p: X(N, k, L([[4, y], [16, y]])), c: 'ashMark', line: 1.4 });
  return { body: { box: [-130, -700, 130, 20], shapes: sh } };
}
// —— Brahma: three of four faces visible, white beards, red and gold, the Vedas and the kamandalu ——
export function brahma() {
  const N = [8, -410], k = 1.42, sh = [];
  sh.push({ p: B([[-14, -388], [-50, -320], [-58, -250]], 22, 16), c: 'skinB' });
  sh.push({ p: S([[-80, -262], [-40, -262], [-34, -226], [-60, -212], [-86, -226]]), c: 'brass', pat: { t: 'coin' } });   // kamandalu
  sh.push({ p: B([[-8, -250], [-34, -130], [-38, -8]], 32, 22), c: 'skinB' }); sh.push({ p: B([[12, -250], [26, -130], [40, -8]], 32, 22), c: 'skinB' });
  for (const x of [-38, 40]) sh.push({ p: S([[x - 14, -12], [x + 24, -12], [x + 28, 4], [x - 16, 6]]), c: 'skinB' });
  sh.push({ p: P([[-46, -300], [46, -300], [56, -210], [64, -108], [36, -96], [8, -104], [-20, -94], [-48, -104], [-64, -110], [-56, -210]]), c: 'red', pat: { t: 'lattice', s: 11 } });
  sh.push({ p: S([[-38, -300], [-44, -350], [-36, -398], [0, -414], [34, -400], [44, -350], [38, -300]]), c: 'saffron', pat: { t: 'folds' } });
  sh.push({ p: B([[16, -388], [56, -340], [86, -330]], 22, 16), c: 'skinB' });
  sh.push({ p: P([[70, -356], [130, -352], [130, -322], [70, -326]]), c: 'palm', pat: { t: 'leaves' } });   // the Vedas
  sh.push(neck(N, k, 'skinB'));
  // two side faces behind the main face (the fourth is hidden)
  for (const [dx, dy, s] of [[-30, -6, .9], [-56, -12, .8]]) {
    const n2 = [N[0] + dx, N[1] + dy];
    sh.push({ p: X(n2, k * s, P([[-26, -62], [19, -64], [16, -82], [8, -106], [0, -118], [-8, -106], [-18, -82]])), c: 'gold2', pat: { t: 'lattice', s: 6 } });
    sh.push({ p: X(n2, k * s, P(FACE.map(([x, y]) => [-x, y]))), c: 'skinB2', ink: 1.6 });
    sh.push({ p: X(n2, k * s, S([[-8, -8], [-21, -16], [-23, -4], [-18, 20], [-8, 40], [6, 44], [12, 22], [8, 2]])), c: 'beard', pat: { t: 'slits', n: 4 } });
  }
  sh.push(hairBack(N, k, 'ink', 8));
  sh.push(...face(N, k, { skinLine: 'ink', skin: 'skinB' }));
  sh.push({ p: X(N, k, S([[8, -8], [21, -16], [23, -4], [18, 20], [8, 42], [-6, 46], [-12, 24], [-8, 2]])), c: 'beard', pat: { t: 'slits', n: 5 } });
  sh.push({ p: X(N, k, P([[-26, -62], [19, -64], [16, -84], [8, -110], [0, -124], [-8, -110], [-18, -84]])), c: 'gold', pat: { t: 'lattice', s: 7 } });
  return { body: { box: [-170, -620, 150, 20], shapes: sh } };
}

// ================= PROPS & SCENERY =================
export function chakraShapes(x, y, R) {
  const sh = [];
  for (let i = 0; i < 16; i++) { const a = i * 2 * PI / 16, a1 = a - .16, a2 = a + .16; sh.push({ p: P([[x + Math.cos(a1) * R, y + Math.sin(a1) * R], [x + Math.cos(a) * (R + 22), y + Math.sin(a) * (R + 22)], [x + Math.cos(a2) * R, y + Math.sin(a2) * R]]), c: i % 2 ? 'flame' : 'red', ink: 1.2 }); }
  sh.push({ p: c => { C(x, y, R)(c); c.moveTo(x + R - 10, y); c.arc(x, y, R - 10, 0, 2 * PI, true); }, c: 'gold', rule: 'evenodd', pat: { t: 'beadRing', x, y, r: R - 5 } });
  for (let i = 0; i < 12; i++) { const a = i * PI / 6; sh.push({ p: L([[x + Math.cos(a) * 9, y + Math.sin(a) * 9], [x + Math.cos(a) * (R - 9), y + Math.sin(a) * (R - 9)]]), c: 'gold', line: 3.4 }); }
  sh.push({ p: C(x, y, 11), c: 'gold', pat: { t: 'coin' } });
  return sh;
}
export function conchShapes(x, y, s = 1) {
  const pts = [[-30, 6], [-26, -12], [-12, -26], [8, -30], [26, -20], [34, -4], [26, 12], [10, 26], [-4, 34], [-14, 26]].map(([a, b]) => [x + a * s, y + b * s]);
  return [{ p: S(pts), c: 'conch', pat: { t: 'slits', n: 4 } }, { p: L(Array.from({ length: 30 }, (_, i) => { const a = i / 29 * PI * 3, r = 13 * s * (1 - i / 36); return [x + 10 * s + Math.cos(a) * r, y - 5 * s + Math.sin(a) * r]; })), c: 'ink', line: 1.4 }];
}
export function lotusShapes(x, y, s = 1) {
  const sh = [];
  for (const [a, h, c] of [[-1.05, 46, 'crim'], [1.05, 46, 'crim'], [-.62, 58, 'pink'], [.62, 58, 'pink'], [-.25, 66, 'pink'], [.25, 66, 'pink'], [0, 72, 'pink2']]) {
    const pts = [[0, 0], [-17, -h * .35], [-12, -h * .8], [0, -h], [12, -h * .8], [17, -h * .35]].map(([px, py]) => { const X_ = px * Math.cos(a) - py * Math.sin(a), Y_ = px * Math.sin(a) + py * Math.cos(a); return [x + X_ * s, y + Y_ * s]; });
    sh.push({ p: S(pts), c, pat: { t: 'vein' } });
  }
  return sh;
}
// the divine garland: hanging loop (origin = where it is held) or lying on the ground
export function garland(lying = false) {
  const sh = [], cols = ['red', 'gold', 'flowerW', 'flame'];
  const pts = lying ? Array.from({ length: 22 }, (_, i) => { const a = i / 22 * 2 * PI; return [Math.cos(a) * 80, Math.sin(a) * 20]; }) : curve([[-46, 0], [-50, 50], [-26, 96], [0, 108], [26, 96], [50, 50], [46, 0]], 6).filter((_, i) => i % 2 === 0);
  if (!lying) sh.push({ p: L([[-46, 0], [-20, -12], [20, -12], [46, 0]]), c: 'leaf', line: 4 });
  pts.forEach(([x, y], i) => { sh.push({ p: E(x, y + 6, 10, 6, i * .7), c: 'leaf', ink: 1 }); });
  pts.forEach(([x, y], i) => { const r = 11; const pp = []; for (let k = 0; k < 10; k++) { const a = k * PI / 5 + i, rr = k % 2 ? r * .55 : r; pp.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); } sh.push({ p: S(pp), c: cols[i % 4], pat: { t: 'hole' }, ink: 1.1, oil: { maxR: 2.5 } }); });
  if (!lying) sh.push({ p: S([[-8, 108], [8, 108], [12, 140], [0, 150], [-12, 140]]), c: 'red', pat: { t: 'slits', n: 2 } });
  return { box: lying ? [-100, -36, 100, 40] : [-70, -30, 70, 160], shapes: sh };
}
export function tree(v = 0) {
  const sh = [{ p: B([[0, 0], [-6, -160], [10, -300]], 46, 22), c: 'wood', pat: { t: 'bark' } }];
  const blobs = v ? [[-90, -330, 96], [90, -340, 98], [0, -450, 120], [-70, -480, 74], [70, -500, 76]] : [[-80, -320, 84], [80, -310, 88], [0, -420, 108], [-50, -500, 70], [60, -480, 70]];
  for (const [x, y, r] of blobs) sh.push({ p: C(x, y, r), c: v ? 'green' : 'jade', pat: { t: 'leafHoles', x, y, r } });
  return { box: [-200, -600, 200, 10], shapes: sh };
}
export function shrub(wilted = false) {
  const sh = [];
  for (let i = -3; i <= 3; i++) {
    const a = i * .28, L_ = 170 - Math.abs(i) * 18, droop = wilted ? (i >= 0 ? 1 : -1) * (.9 + Math.abs(i) * .12) : 0;
    const tip = wilted ? [Math.sin(a) * L_ * .6 + droop * 60, -L_ * .45] : [Math.sin(a) * L_, -Math.cos(a) * L_];
    const mid = wilted ? [Math.sin(a) * L_ * .45, -L_ * .55] : [Math.sin(a) * L_ * .5, -Math.cos(a) * L_ * .5];
    sh.push({ p: B([[0, 0], mid, tip], 10, 3), c: wilted ? 'dry' : 'green' });
    sh.push({ p: E(tip[0], tip[1], 22, 11, Math.atan2(tip[1] - mid[1], tip[0] - mid[0])), c: wilted ? 'dry2' : 'jade', pat: { t: 'vein' } });
  }
  return { box: [-200, -200, 200, 10], shapes: sh };
}
export function kund() {   // the yajna altar
  return { box: [-170, -120, 170, 10], shapes: [
    { p: P([[-160, 0], [160, 0], [140, -40], [-140, -40]]), c: 'brick', pat: { t: 'bricks' } },
    { p: P([[-136, -40], [136, -40], [116, -80], [-116, -80]]), c: 'brick2', pat: { t: 'bricks' } },
    { p: P([[-110, -80], [110, -80], [92, -110], [-92, -110]]), c: 'brick', pat: { t: 'bricks' } }] };
}
export function fire(v = 0) {
  const sh = [];
  for (let i = 0; i < 7; i++) { const x = -70 + i * 23, h = 120 + ((i * 37 + v * 53) % 70), d = (i + v) % 2 ? 1 : -1; sh.push({ p: c => { c.moveTo(x - 18, 0); c.bezierCurveTo(x - 26, -h * .3, x - 8 * d, -h * .55, x + 6 * d, -h * .82); c.bezierCurveTo(x + 12 * d, -h * .95, x + 22 * d, -h * 1.02, x + 24 * d, -h * .9); c.bezierCurveTo(x + 20 * d, -h * .93, x + 14 * d, -h * .88, x + 14 * d, -h * .76); c.bezierCurveTo(x + 22, -h * .5, x + 24, -h * .22, x + 18, 0); c.closePath(); }, c: i % 2 ? 'flame' : 'red' }); }
  return { box: [-110, -220, 110, 10], shapes: sh };
}
export function petal() { const pp = []; for (let k = 0; k < 10; k++) { const a = k * PI / 5, r = k % 2 ? 6 : 12; pp.push([Math.cos(a) * r, Math.sin(a) * r]); } return { box: [-16, -16, 16, 16], shapes: [{ p: S(pp), c: 'flame', pat: { t: 'hole' }, ink: 1 }] }; }
export function cloudProp() { return { box: [-210, -100, 210, 90], shapes: [{ p: S([[-180, 40], [-170, -10], [-120, -50], [-60, -40], [-20, -80], [50, -70], [90, -30], [150, -50], [190, 0], [170, 50], [80, 60], [0, 50], [-90, 64]]), c: 'cloud', pat: { t: 'clouds' } }] }; }

export const ROSTER = { durvasa, vidyadhari, indra, airavata, deva, daitya, vishnu, shiva, brahma };

export function ground() {
  const top = c => { c.moveTo(-200, 400); c.lineTo(-200, 10); for (let x = -200; x <= 1300; x += 60) c.quadraticCurveTo(x + 30, -8 + Math.sin(x * .02) * 6, x + 60, 6); c.lineTo(1300, 400); c.closePath(); };
  const sh = [{ p: top, c: 'earth', pat: { t: 'strataG' } }];
  for (let x = -150; x < 1260; x += 46) sh.push({ p: B([[x, 8], [x + 8, -26 - (x * 7 % 18)]], 6, 2), c: 'green', ink: 1 });
  return { box: [-200, -50, 1300, 400], shapes: sh };
}
export function sea(v = 0) {
  const step = v ? 160 : 118, amp = v ? 40 : 30;
  const top = c => { c.moveTo(-200, 700); c.lineTo(-200, 0); for (let x = -200, i = 0; x < 1300; x += step, i++) { const y = Math.sin(i * 1.7 + v * 2) * 6; c.quadraticCurveTo(x + step * .35, y - amp, x + step * .62, y - amp * .55); c.quadraticCurveTo(x + step * .78, y - amp * .2, x + step, y); } c.lineTo(1300, 700); c.closePath(); };
  return { box: [-200, -amp - 20, 1300, 700], shapes: [{ p: top, c: v ? 'milk2' : 'milk', pat: { t: 'waves', r: v ? 20 : 15 } }] };
}
export function mandara() {
  return { box: [-200, -720, 200, 10], shapes: [
    { p: S([[-178, 0], [-160, -200], [-128, -380], [-86, -540], [-44, -650], [0, -690], [44, -650], [90, -540], [130, -380], [160, -200], [178, 0]]), c: 'rock', pat: { t: 'strataM' } },
    { p: B([[-176, -200], [0, -250], [176, -300]], 40, 40), c: 'serpent', pat: { t: 'scalesOpen' } },
    { p: B([[-170, -330], [0, -380], [160, -430]], 38, 38), c: 'serpent', pat: { t: 'scalesOpen' } }] };
}
export function smoke(v = 0) {
  const sg = v % 2 ? 1 : -1;
  return { box: [-80, -260, 80, 30], shapes: [{ p: B([[0, 0], [sg * 26, -60], [-sg * 18, -130], [sg * 24, -190], [-sg * 8, -240]], 46, 6), c: 'smoke', pat: { t: 'slits', n: 3 } }] };
}
// lettered plaque: dark board, letters cut (puppet) or painted light (oil)
export function plaque(lines, w, h) {
  return { box: [-w / 2, -h / 2, w / 2, h / 2], shapes: [
    { p: c => c.roundRect(-w / 2, -h / 2, w, h, 26), c: 'board', pat: { t: 'border', w, h } },
    ...lines.map(([text, y, size]) => ({ text, x: 0, y, size, c: 'letter' }))] };
}
export const PROPS = { garland, tree, shrub, kund, fire, petal, cloudProp, ground, sea, mandara, smoke, plaque };

// —— Short 3: the churning apparatus ——
export function kurma() {   // Vishnu as the tortoise; origin at the top of the shell
  const sh = [];
  for (const [x, y, a] of [[-200, 100, .5], [200, 100, -.5], [-150, 130, .9], [150, 130, -.9]]) sh.push({ p: E(x, y, 62, 22, a), c: 'jade', pat: { t: 'vein' } });
  sh.push({ p: S([[220, 50], [276, 28], [322, 44], [314, 76], [252, 86]]), c: 'jade', pat: { t: 'scales' } });
  sh.push({ p: C(296, 46, 4.5), c: 'ink', ink: 0 });
  sh.push({ p: c => { c.moveTo(-250, 110); c.bezierCurveTo(-240, -20, 240, -20, 250, 110); c.closePath(); }, c: 'green', pat: { t: 'hexes' } });
  sh.push({ p: B([[-250, 106], [0, 118], [250, 106]], 16, 16, false), c: 'gold', pat: { t: 'beads' } });
  return { box: [-280, -10, 340, 170], shapes: sh };
}
export function mandaraBare() {
  const sh = [{ p: S([[-178, 0], [-160, -200], [-128, -380], [-86, -540], [-44, -650], [0, -690], [44, -650], [90, -540], [130, -380], [160, -200], [178, 0]]), c: 'rock', pat: { t: 'strataM' } }];
  for (const [x, y, s] of [[-40, -640, 1], [10, -672, 1.2], [52, -628, .9]]) sh.push({ p: P([[x, y + 6], [x - 18 * s, y - 2], [x, y - 46 * s], [x + 18 * s, y - 2]]), c: 'green', pat: { t: 'scales' } });
  return { box: [-200, -730, 200, 10], shapes: sh };
}
export function wrap() { return { box: [-200, -40, 200, 40], shapes: [{ p: B([[-190, 24], [0, -2], [190, -26]], 40, 40), c: 'serpent', pat: { t: 'scalesOpen' } }] }; }
export function vasuki() {   // the rope: head at the left (the daityas' side), tail at the right
  const sh = [{ p: B([[-500, 0], [0, 0], [470, 0], [540, -12]], 40, 14), c: 'serpent', pat: { t: 'scalesOpen' } }];
  sh.push({ p: B([[-500, 0], [-540, -60], [-528, -120]], 40, 36), c: 'serpent', pat: { t: 'scalesOpen' } });
  sh.push({ p: S([[-540, -110], [-574, -150], [-566, -196], [-528, -212], [-490, -196], [-484, -150], [-512, -110]]), c: 'green', pat: { t: 'lattice', s: 8 } });
  sh.push({ p: E(-528, -214, 18, 13), c: 'jade' }); sh.push({ p: C(-534, -216, 3), c: 'ink', ink: 0 }); sh.push({ p: C(-522, -216, 3), c: 'ink', ink: 0 });
  return { box: [-600, -240, 560, 30], shapes: sh };
}
export function spark() {
  const pts = []; for (let k = 0; k < 8; k++) { const a = k * PI / 4, r = k % 2 ? 6 : 20; pts.push([Math.cos(a) * r, Math.sin(a) * r]); }
  return { box: [-24, -24, 24, 24], shapes: [{ p: P(pts), c: 'flame', pat: { t: 'hole' }, ink: 1.2, oil: { maxR: 2 } }] };
}

// —— Short 4: rain from Vasuki's breath ——
export function rain(v = 0) {
  const sh = [];
  for (let k = 0; k < 18; k++) { const x = -200 + k * 23 + v * 10, y = 10 + ((k * 37 + v * 19) % 70); sh.push({ p: L([[x, y], [x - 18, y + 150 + ((k * 53) % 60)]]), c: 'ganga', line: 2.6 }); }
  return { box: [-240, 0, 240, 300], shapes: sh };
}

// Markandeya in impasto palette-knife paint: every plate is a flat, value-planned illustration turned into knife strokes
import { Ref, paintRef } from './engine/plate.js';
import { P, E, lin, rad, hash } from './common.js';

export const SW = 2112, SH = 1188, GY = 850, LX = 1056;
const loc = (ox, oy, fn) => c => { c.save(); c.translate(ox, oy); fn(c); c.restore(); };
const REV = (x, y) => Math.hypot(x - LX, (y - (GY - 300)) * 1.6) / 1400;      // knife sweep of colour from the linga outwards
const blob = (R, cx, cy, rx, ry, col, props = {}) => R.fill(c => c.ellipse(cx, cy, rx, ry, 0, 0, 7), col, props);

// ------------------------------------------------------------ backgrounds
function ground(R, top, cols) {
  const bands = [[top, top + 40, 14], [top + 40, top + 110, 20], [top + 110, top + 230, 28], [top + 230, SH, 38]];
  bands.forEach(([y0, y1, r]) => R.fill(P([[0, y0], [SW, y0], [SW, y1], [0, y1]]), lin(0, y0, 0, y1, cols), { dir: 2, fallback: 2, group: 'gr', maxR: r, jit: .09, aj: .3 }));
}
function tree(R, x, y, s, light, dark, trunk) {
  R.fill(P([[x - 22 * s, y], [x - 14 * s, y - 190 * s], [x + 14 * s, y - 190 * s], [x + 26 * s, y]]), trunk, { dir: 90, maxR: 10, group: 'tk' + x });
  [[0, -270, 150], [-110, -220, 110], [110, -230, 115], [-50, -340, 100], [60, -330, 95]].forEach(([dx, dy, r], i) => blob(R, x + dx * s, y + dy * s, r * s, r * .8 * s, lin(0, y + dy * s - r * s, 0, y + dy * s + r * s, [[0, light], [1, dark]]), { dir: -20 + i * 15, maxR: 16, group: 'cn' + x + i, jit: .12 }));
}
export function buildDusk() {
  const R = new Ref(SW, SH, 1), HZ = 640;
  R.fill(P([[0, 0], [SW, 0], [SW, HZ + 60], [0, HZ + 60]]), lin(0, 0, 0, HZ, [[0, '#1f2a9c'], [.3, '#6a38b4'], [.55, '#e0489a'], [.78, '#ff8a3a'], [1, '#ffd25a']]), { dir: -6, fallback: -6, group: 'sky', maxR: 40, jit: .08, detail: 2.2, aj: .3 });
  R.fill(c => c.arc(LX, HZ - 20, 170, 0, 7), rad(LX, HZ - 20, 10, 170, [[0, '#fffbd0'], [.6, '#ffd860'], [1, '#ff9a3c']]), { dir: { radial: [LX, HZ - 20], off: 90 }, maxR: 18, group: 'sky', jit: .05 });
  const cloud = (x, y, w, h, top, und) => R.fill(c => { c.ellipse(x, y, w, h, 0, 0, 7); c.ellipse(x - w * .55, y + h * .3, w * .6, h * .7, 0, 0, 7); c.ellipse(x + w * .6, y + h * .35, w * .55, h * .6, 0, 0, 7); }, lin(0, y - h, 0, y + h, [[0, top], [.65, top], [1, und]]), { dir: -4, fallback: -4, group: 'sky', maxR: 28, detail: 1.6, aj: .3 });
  cloud(420, 190, 300, 58, '#7c3fc0', '#ff6a8a'); cloud(1650, 150, 340, 62, '#5a36b8', '#ff7ea0'); cloud(1000, 330, 260, 40, '#b05ad0', '#ffa070'); cloud(1900, 410, 230, 34, '#c46ad0', '#ffb070'); cloud(180, 470, 220, 30, '#d46ad0', '#ffb878');
  // Kailash-like peaks: violet with rose snow
  R.fill(P([[0, HZ + 20], [160, 470], [330, 560], [520, 380], [760, HZ - 30], [1000, 480], [1230, HZ - 40], [1490, 410], [1720, 560], [1900, 450], [SW, HZ + 20]]), lin(0, 380, 0, HZ, [[0, '#8a5ad0'], [1, '#4a3a9a']]), { dir: 70, fallback: 70, group: 'mt', maxR: 22 });
  R.fill(P([[420, 440], [520, 380], [610, 450], [560, 430], [520, 470], [470, 430]]), '#ffd6ec', { dir: 40, maxR: 7, group: 'snow1' });
  R.fill(P([[1400, 450], [1490, 410], [1570, 470], [1520, 455], [1490, 490], [1450, 456]]), '#ffd6ec', { dir: 40, maxR: 7, group: 'snow2' });
  R.fill(P([[0, HZ + 50], [300, HZ - 10], [700, HZ + 30], [1100, HZ - 20], [1500, HZ + 30], [1800, HZ], [SW, HZ + 40], [SW, HZ + 140], [0, HZ + 140]]), lin(0, HZ - 20, 0, HZ + 140, [[0, '#1fa08a'], [1, '#157a6a']]), { dir: 80, fallback: 80, group: 'hill', maxR: 20 });
  ground(R, HZ + 110, [[0, '#f4a840'], [.15, '#d8703a'], [.5, '#a03a4a'], [1, '#5a2a5a']]);
  tree(R, 250, GY + 30, 1.35, '#35d080', '#128a4a', '#7a3a2a'); tree(R, 1900, GY + 20, 1.0, '#40d890', '#148a50', '#7a3a2a');
  // the shrine terrace under the linga
  R.fill(P([[LX - 310, GY - 10], [LX + 310, GY - 10], [LX + 380, GY + 70], [LX - 380, GY + 70]]), lin(0, GY - 10, 0, GY + 70, [[0, '#ffe0c0'], [1, '#e08a9a']]), { dir: 0, maxR: 12, group: 'step1' });
  R.fill(P([[LX - 380, GY + 70], [LX + 380, GY + 70], [LX + 440, GY + 150], [LX - 440, GY + 150]]), lin(0, GY + 70, 0, GY + 150, [[0, '#f4b0b0'], [1, '#b05a8a']]), { dir: 0, maxR: 14, group: 'step2' });
  // marigolds and lamps in the foreground
  for (let k = 0; k < 60; k++) { const x = 40 + hash(k * 3) * 2030, y = GY + 120 + hash(k * 5 + 1) * 190, r = 8 + hash(k * 7) * 10, col = ['#ff9a1f', '#ffc02a', '#ff5a2a', '#ff7aa0'][k % 4]; blob(R, x, y, r, r * .8, col, { type: 2, maxR: 6, group: 'fl' + k }); }
  for (const x of [LX - 330, LX - 200, LX + 200, LX + 330]) { blob(R, x, GY + 20, 20, 9, '#b0402a', { maxR: 5, group: 'diya' + x }); blob(R, x, GY + 8, 7, 12, '#ffe060', { maxR: 3, group: 'fl' + x }); }
  const st = paintRef(R, { R: [44, 22, 10, 5, 2.6], T: 12, seed: 5, rev: REV });
  return { strokes: st, ref: R };
}
export function buildDay() {     // the boy's home, bright morning
  const R = new Ref(SW, SH, 1), HZ = 640;
  R.fill(P([[0, 0], [SW, 0], [SW, HZ + 60], [0, HZ + 60]]), lin(0, 0, 0, HZ, [[0, '#2f8fe8'], [.5, '#7fd0ff'], [1, '#fff0a0']]), { dir: -6, fallback: -6, group: 'sky', maxR: 40, jit: .07, detail: 2 });
  for (const [x, y, w, h] of [[500, 200, 260, 50], [1500, 140, 320, 58], [1000, 330, 220, 36]]) R.fill(c => { c.ellipse(x, y, w, h, 0, 0, 7); c.ellipse(x - w * .5, y + h * .3, w * .6, h * .7, 0, 0, 7); c.ellipse(x + w * .6, y + h * .3, w * .5, h * .6, 0, 0, 7); }, lin(0, y - h, 0, y + h, [[0, '#ffffff'], [1, '#ffd0c0']]), { dir: -4, group: 'sky', maxR: 26, detail: 1.6 });
  R.fill(P([[0, HZ + 40], [260, 500], [560, 580], [900, 470], [1300, 590], [1700, 500], [SW, HZ + 40]]), lin(0, 470, 0, HZ + 40, [[0, '#6aa0f0'], [1, '#4a7ad0']]), { dir: 70, group: 'mt', maxR: 22 });
  R.fill(P([[0, HZ + 40], [400, HZ - 10], [900, HZ + 30], [1500, HZ - 10], [SW, HZ + 30], [SW, HZ + 150], [0, HZ + 150]]), lin(0, HZ - 10, 0, HZ + 150, [[0, '#46c860'], [1, '#2a9a48']]), { dir: 80, group: 'hill', maxR: 20 });
  ground(R, HZ + 120, [[0, '#86e050'], [.2, '#4cc040'], [.6, '#c89040'], [1, '#8a5a3a']]);
  // hut: thatch roof, terracotta wall, door
  const hx = 470, hy = GY + 10;
  R.fill(P([[hx - 230, hy - 170], [hx, hy - 330], [hx + 230, hy - 170]]), lin(0, hy - 330, 0, hy - 170, [[0, '#ffd23a'], [1, '#e8902a']]), { dir: 20, maxR: 12, group: 'roof' });
  R.fill(P([[hx - 170, hy - 170], [hx + 170, hy - 170], [hx + 170, hy], [hx - 170, hy]]), lin(0, hy - 170, 0, hy, [[0, '#f09a6a'], [1, '#c8603a']]), { dir: 90, maxR: 12, group: 'wall' });
  R.fill(P([[hx - 40, hy - 120], [hx + 40, hy - 120], [hx + 40, hy], [hx - 40, hy]]), '#4a2a5a', { dir: 90, maxR: 8, group: 'door' });
  R.fill(P([[hx + 80, hy - 120], [hx + 140, hy - 120], [hx + 140, hy - 70], [hx + 80, hy - 70]]), '#ffe27a', { maxR: 6, group: 'win' });
  tree(R, 1620, GY + 20, 1.2, '#50e08a', '#16944c', '#8a4a2a'); tree(R, 120, GY + 20, .9, '#60e898', '#1a9a52', '#8a4a2a');
  for (let k = 0; k < 70; k++) { const x = 30 + hash(k * 3) * 2050, y = GY + 90 + hash(k * 5 + 1) * 230, r = 7 + hash(k * 7) * 9, col = ['#ff5a8a', '#ffd020', '#ffffff', '#ff8a2a', '#b070ff'][k % 5]; blob(R, x, y, r, r * .8, col, { type: 2, maxR: 6, group: 'f' + k }); }
  const st = paintRef(R, { R: [44, 22, 10, 5, 2.6], T: 12, seed: 7 });
  return { strokes: st, ref: R };
}

// ------------------------------------------------------------ the shrine: linga on its yoni, garlanded
export const LGW = 760, LGH = 620, LGX = 380, LGY = 540;
export function buildLinga() {
  const R = new Ref(LGW, LGH, 1.4), X = LGX, Y = LGY, o = (a, b) => [a + X, b + Y];
  // (no halo disc: the raking light and the lamps do that)
  R.fill(P([o(-250, 6), o(-170, -30), o(170, -30), o(250, 6), o(330, 14), o(250, 46), o(-250, 46)].map(([x, y]) => [x, y])), lin(0, Y - 30, 0, Y + 46, [[0, '#ff6a9a'], [1, '#c02a6a']]), { dir: 0, maxR: 9, group: 'yoni' });
  R.fill(c => { c.moveTo(X - 100, Y - 24); c.lineTo(X - 100, Y - 270); c.bezierCurveTo(X - 100, Y - 440, X + 100, Y - 440, X + 100, Y - 270); c.lineTo(X + 100, Y - 24); c.closePath(); }, lin(X - 100, 0, X + 100, 0, [[0, '#3a3aa8'], [.45, '#6a5ad8'], [1, '#2a2678']]), { dir: 90, fallback: 90, maxR: 14, group: 'lg', jit: .08 });
  for (const [dy, w] of [[-330, 90], [-296, 98], [-262, 100]]) R.line(c => { c.moveTo(X - w, Y + dy + 14); c.quadraticCurveTo(X, Y + dy + 40, X + w, Y + dy + 14); }, '#fff3d8', 10, { dir: 0, maxR: 4, group: 'ash' + dy });
  for (let k = 0; k < 12; k++) { const a = Math.PI * k / 11, x = X - 108 + 216 * k / 11, y = Y - 120 + 70 * Math.sin(a); blob(R, x, y, 14, 12, k % 2 ? '#ff7a1a' : '#ffc02a', { type: 2, maxR: 5, group: 'gar' + k }); }
  R.fill(P([o(0, -430), o(-30, -470), o(0, -452), o(30, -470)]), '#3ad06a', { maxR: 4, group: 'bilva' });
  const st = paintRef(R, { R: [26, 13, 6.5, 3.2, 2], T: 10, seed: 11 });
  return { strokes: st, ref: R };
}

// ------------------------------------------------------------ figures (feet at the origin of their plate)
export const BW = 360, BH = 440, BX = 160, BY = 420;
export function buildBoy(hug) {
  const R = new Ref(BW, BH, 2), X = BX, Y = BY, p = pts => P(pts.map(([x, y]) => [x + X, y + Y])), sk = '#f4a878', sh = '#d9805a';
  const arm = (pts, w) => R.line(c => pts.forEach(([x, y], i) => i ? c.lineTo(x + X, y + Y) : c.moveTo(x + X, y + Y)), sk, w, { dir: 'edge', maxR: 5, group: 'arm' + pts[1][1] });
  R.fill(p([[-30, -90], [30, -90], [44, -30], [50, 0], [-50, 0], [-44, -30]]), lin(0, Y - 90, 0, Y, [[0, '#fff6e0'], [1, '#ffd8a0']]), { dir: 90, maxR: 7, group: 'dh' });
  R.fill(p([[-34, -92], [34, -92], [34, -76], [-34, -76]]), '#ff7a1a', { dir: 0, maxR: 5, group: 'sash' });
  R.fill(p([[-24, -92], [26, -92], [20, -170], [-18, -170]]), sk, { dir: 90, maxR: 6, group: 'tor' });
  R.line(c => { c.moveTo(X - 16, Y - 168); c.lineTo(X + 20, Y - 100); }, '#fff2d0', 4, { dir: 'edge', maxR: 3, group: 'thr' });
  if (hug) { arm([[2, -158], [60, -146], [112, -128]], 15); arm([[8, -146], [66, -132], [118, -112]], 15); } else { arm([[0, -160], [26, -136], [44, -168]], 13); arm([[6, -156], [30, -134], [46, -166]], 13); }
  R.fill(c => c.arc(X + 4, Y - 200, 28, 0, 7), sk, { dir: 'edge', maxR: 5, group: 'hd' });
  R.fill(P([[X + 28, Y - 202], [X + 42, Y - 192], [X + 28, Y - 186]]), sk, { maxR: 3, group: 'nose' });
  blob(R, X - 12, Y - 236, 14, 14, '#2a1a4a', { maxR: 4, group: 'knot' }); R.fill(P([[X - 22, Y - 218], [X + 14, Y - 226], [X + 26, Y - 210], [X - 20, Y - 204]]), '#2a1a4a', { dir: 0, maxR: 4, group: 'hair' });
  for (const dy of [-208, -202]) R.line(c => { c.moveTo(X + 6, Y + dy); c.lineTo(X + 24, Y + dy + 1); }, '#fff3d0', 3, { maxR: 2, group: 'ash' + dy });
  R.line(c => { c.moveTo(X + 14, Y - 196); c.lineTo(X + 24, Y - 195); }, '#3a1a2a', 3, { maxR: 2, group: 'eye' });
  const st = paintRef(R, { R: [16, 8, 4, 2.4], T: 9, seed: hug ? 13 : 14 });
  return { strokes: st, ref: R };
}
export const DW = 340, DH = 430, DX = 150, DY = 410;
export function buildDuta() {
  const R = new Ref(DW, DH, 2), X = DX, Y = DY, p = pts => P(pts.map(([x, y]) => [x + X, y + Y]));
  R.fill(p([[-30, -90], [30, -90], [42, -30], [50, 0], [-50, 0], [-42, -30]]), lin(0, Y - 90, 0, Y, [[0, '#3ad090'], [1, '#128a60']]), { dir: 90, maxR: 7, group: 'dh' });
  R.fill(p([[-34, -92], [38, -92], [30, -180], [-30, -180]]), '#d8402a', { dir: 90, maxR: 7, group: 'tor' });
  R.line(c => { c.moveTo(X, Y - 160); c.lineTo(X + 70, Y - 170); c.lineTo(X + 100, Y - 140); }, '#d8402a', 16, { maxR: 5, group: 'ar1' });
  R.fill(c => c.arc(X + 4, Y - 214, 30, 0, 7), '#e0502a', { maxR: 5, group: 'hd' });
  for (const s of [-1, 1]) R.fill(P([[X + 4 + s * 18, Y - 232], [X + 4 + s * 36, Y - 280], [X + 4 + s * 8, Y - 240]]), '#fff0d0', { maxR: 3, group: 'horn' + s });
  R.line(c => { c.moveTo(X + 8, Y - 224); c.lineTo(X + 26, Y - 220); }, '#2a0a1a', 4, { maxR: 2, group: 'eye' });
  const st = paintRef(R, { R: [16, 8, 4, 2.4], T: 9, seed: 17 });
  return { strokes: st, ref: R };
}
export const YW = 820, YH = 700, YOX = 430, YOY = 640;
export function buildYama() {       // Yama on his buffalo, facing left
  const R = new Ref(YW, YH, 1.4), X = YOX, Y = YOY, p = pts => P(pts.map(([x, y]) => [x + X, y + Y]));
  const buf = lin(0, Y - 300, 0, Y, [[0, '#7a62d8'], [1, '#2a1f6a']]);
  for (const x of [-120, -78, 78, 120]) R.fill(p([[x - 18, -80], [x + 18, -80], [x + 13, 6], [x - 13, 6]]), '#2a1f6a', { dir: 90, maxR: 6, group: 'leg' + x });
  R.fill(c => c.ellipse(X, Y - 150, 170, 80, 0, 0, 7), buf, { dir: 0, fallback: 0, maxR: 14, group: 'bd' });
  R.fill(c => c.ellipse(X - 205, Y - 118, 66, 46, .35, 0, 7), '#3a2e86', { dir: 20, maxR: 8, group: 'hd' });
  for (const dx of [0, 24]) R.fill(P([[X - 222 + dx, Y - 140], [X - 280 + dx, Y - 190], [X - 270 + dx, Y - 250], [X - 240 + dx, Y - 190], [X - 206 + dx, Y - 148]]), '#fff0d0', { dir: 60, maxR: 5, group: 'hn' + dx });
  R.line(c => { c.moveTo(X - 232, Y - 128); c.lineTo(X - 208, Y - 120); }, '#ff4040', 5, { maxR: 2, group: 'be' });
  R.line(c => { c.moveTo(X + 170, Y - 150); c.quadraticCurveTo(X + 230, Y - 120, X + 240, Y - 50); }, '#2a1f6a', 14, { maxR: 5, group: 'tail' });
  R.fill(p([[-30, -250], [38, -250], [30, -350], [-24, -350]]), lin(0, Y - 350, 0, Y - 250, [[0, '#2ec88a'], [1, '#0f8a5a']]), { dir: 90, maxR: 8, group: 'tor' });
  R.fill(p([[-38, -236], [48, -236], [58, -176], [-48, -176]]), '#e02a45', { dir: 0, maxR: 8, group: 'cl' });
  R.fill(c => c.arc(X + 6, Y - 388, 38, 0, 7), '#22b87a', { dir: 'edge', maxR: 6, group: 'face' });
  R.fill(P([[X - 26, Y - 392], [X - 48, Y - 380], [X - 26, Y - 366]]), '#22b87a', { maxR: 3, group: 'nose' });
  R.line(c => { c.moveTo(X - 18, Y - 402); c.lineTo(X - 38, Y - 394); }, '#ff2a2a', 5, { maxR: 2, group: 'e1' });
  R.line(c => { c.moveTo(X + 8, Y - 402); c.lineTo(X - 8, Y - 396); }, '#ff2a2a', 5, { maxR: 2, group: 'e2' });
  R.line(c => { c.moveTo(X - 24, Y - 372); c.quadraticCurveTo(X - 40, Y - 364, X - 52, Y - 376); }, '#1a0a2a', 4, { maxR: 2, group: 'mu' });
  R.fill(P([[X - 30, Y - 420], [X - 38, Y - 490], [X - 8, Y - 450], [X + 8, Y - 505], [X + 24, Y - 450], [X + 50, Y - 488], [X + 46, Y - 420]]), lin(0, Y - 505, 0, Y - 420, [[0, '#fff0a0'], [1, '#ffb82a']]), { dir: 90, maxR: 6, group: 'cr' });
  R.line(c => { c.moveTo(X + 24, Y - 330); c.lineTo(X - 40, Y - 366); c.lineTo(X - 84, Y - 448); }, '#22b87a', 18, { maxR: 5, group: 'ar1' });
  R.line(c => { c.moveTo(X + 34, Y - 322); c.lineTo(X + 92, Y - 276); c.lineTo(X + 104, Y - 256); }, '#22b87a', 18, { maxR: 5, group: 'ar2' });
  R.line(c => { c.moveTo(X + 106, Y - 256); c.lineTo(X + 114, Y - 420); }, '#a05a2a', 8, { maxR: 3, group: 'mace' });
  R.fill(c => c.arc(X + 116, Y - 432, 28, 0, 7), '#ffc02a', { maxR: 4, group: 'mh' });
  const st = paintRef(R, { R: [26, 13, 6.5, 3.2, 2], T: 10, seed: 19 });
  return { strokes: st, ref: R };
}
export const NW = 360, NH = 280;
export function buildNoose() {
  const R = new Ref(NW, NH, 1.5);
  R.line(c => c.ellipse(NW / 2, NH / 2, 120, 90, 0, 0, 7), '#ff7a1a', 26, { dir: 'edge', maxR: 6, group: 'ring' });
  R.line(c => c.ellipse(NW / 2, NH / 2, 120, 90, 0, 0, 7), '#ffd02a', 9, { dir: 'edge', maxR: 3, group: 'ring2' });
  R.fill(P([[NW / 2 + 110, NH / 2 - 20], [NW / 2 + 170, NH / 2 - 60], [NW / 2 + 176, NH / 2 - 40], [NW / 2 + 120, NH / 2]]), '#c0401a', { maxR: 6, group: 'tailn' });
  return { strokes: paintRef(R, { R: [14, 7, 3.5, 2], T: 9, seed: 23 }), ref: R };
}

export const SHW = 900, SHH = 1000, SHX = 380, SHY = 940;
export function buildShiva(palm) {
  const R = new Ref(SHW, SHH, 1.1), X = SHX, Y = SHY, p = pts => P(pts.map(([x, y]) => [x + X, y + Y])), sk = '#cfe4ff';
  const limb = (pts, w, col, g) => R.line(c => pts.forEach(([x, y], i) => i ? c.lineTo(x + X, y + Y) : c.moveTo(x + X, y + Y)), col, w, { dir: 'edge', maxR: 7, group: g });
  R.line(c => { c.moveTo(X - 120, Y - 700); c.lineTo(X - 120, Y + 6); }, '#a06a2a', 12, { maxR: 4, group: 'staff' });
  R.fill(p([[-160, -640], [-150, -720], [-134, -660], [-120, -660], [-106, -740], [-92, -660], [-78, -660], [-64, -720], [-56, -640], [-120, -600]]), lin(0, Y - 740, 0, Y - 600, [[0, '#fff0a0'], [1, '#ffb82a']]), { dir: 90, maxR: 5, group: 'tri' });
  limb([[-20, -480], [-84, -430], [-116, -400]], 26, sk, 'farArm');
  R.fill(p([[-60, -260], [60, -260], [80, -100], [92, 0], [-92, 0], [-80, -100]]), lin(0, Y - 260, 0, Y, [[0, '#ffa030'], [1, '#e05a1a']]), { dir: 80, maxR: 9, group: 'dh' });
  for (let k = 0; k < 8; k++) R.line(c => { c.moveTo(X - 70 + k * 18, Y - 250 + (k % 3) * 10); c.lineTo(X - 56 + k * 18, Y - 150 + (k % 2) * 40); }, '#3a1a2a', 7, { maxR: 3, group: 'tg' + k });
  R.fill(p([[-62, -258], [66, -258], [56, -490], [-54, -490]]), lin(X - 60, 0, X + 60, 0, [[0, '#e8f2ff'], [1, '#9cc0f4']]), { dir: 90, maxR: 10, group: 'tor' });
  for (const y of [-400, -378, -356]) R.line(c => { c.moveTo(X - 40, Y + y); c.lineTo(X + 44, Y + y + 5); }, '#5a5aa8', 5, { maxR: 3, group: 'as' + y });
  limb([[-42, -480], [0, -450], [52, -486]], 15, '#2fcf6a', 'snake');
  R.fill(c => c.ellipse(X - 48, Y - 486, 20, 26, 0, 0, 7), '#2fcf6a', { maxR: 4, group: 'hood' });
  R.fill(p([[-10, -520], [28, -520], [28, -556], [-10, -556]]), sk, { maxR: 5, group: 'neck' });
  R.fill(c => c.ellipse(X + 8, Y - 540, 18, 14, 0, 0, 7), '#2a5ae0', { maxR: 3, group: 'throat' });
  R.fill(c => c.arc(X + 10, Y - 590, 48, 0, 7), lin(0, Y - 640, 0, Y - 540, [[0, '#f2f8ff'], [1, '#bcd4fa']]), { dir: 'edge', maxR: 6, group: 'hd' });
  R.fill(P([[X + 52, Y - 596], [X + 76, Y - 576], [X + 52, Y - 560]]), '#cfe4ff', { maxR: 4, group: 'nose' });
  R.line(c => { c.moveTo(X + 22, Y - 604); c.lineTo(X + 52, Y - 600); }, '#2a1a4a', 5, { maxR: 2, group: 'eye' });
  R.line(c => { c.moveTo(X + 42, Y - 566); c.lineTo(X + 62, Y - 568); }, '#c02a4a', 4, { maxR: 2, group: 'mouth' });
  R.line(c => { c.moveTo(X + 44, Y - 640); c.lineTo(X + 46, Y - 622); }, '#ff2a4a', 5, { maxR: 2, group: 'eye3' });
  R.fill(c => { c.moveTo(X - 52, Y - 560); c.bezierCurveTo(X - 80, Y - 640, X - 40, Y - 720, X + 20, Y - 730); c.bezierCurveTo(X + 80, Y - 730, X + 74, Y - 650, X + 50, Y - 640); c.bezierCurveTo(X + 20, Y - 660, X - 10, Y - 640, X - 30, Y - 560); c.closePath(); }, lin(0, Y - 730, 0, Y - 560, [[0, '#4a3ab8'], [1, '#1f1a5a']]), { dir: 70, maxR: 8, group: 'jata' });
  R.fill(c => { c.moveTo(X + 52, Y - 742); c.arc(X + 20, Y - 762, 40, -.4, Math.PI * 1.1, true); c.arc(X + 34, Y - 766, 30, Math.PI * 1.05, -.2); c.closePath(); }, '#ffe9a0', { dir: 'edge', maxR: 5, group: 'moon' });
  R.line(c => { c.moveTo(X - 40, Y - 700); c.bezierCurveTo(X - 120, Y - 650, X - 150, Y - 540, X - 150, Y - 430); }, '#4fe0f0', 14, { dir: 'edge', maxR: 5, group: 'ganga' });
  if (palm) { limb([[40, -480], [110, -482], [148, -560]], 26, sk, 'nearArm'); R.fill(c => c.ellipse(X + 154, Y - 586, 24, 32, .2, 0, 7), sk, { maxR: 5, group: 'palm' }); R.line(c => { c.moveTo(X + 154, Y - 604); c.lineTo(X + 154, Y - 570); }, '#e87a7a', 5, { maxR: 2, group: 'pl' }); }
  const st = paintRef(R, { R: [30, 15, 7.5, 3.8, 2.2], T: 10, seed: 29 });
  return { strokes: st, ref: R };
}

// ------------------------------------------------------------ painted lettering (laid in with the knife)
export function buildText(str, sub, w, h, big, small, col1 = '#fff2c0', col2 = '#ffb83a') {
  const R = new Ref(w, h, 1), F = '"Noto Serif Devanagari"';
  R.fill(P([[8, 8], [w - 8, 8], [w - 8, h - 8], [8, h - 8]]), lin(0, 0, 0, h, [[0, '#2a2a98'], [.55, '#6a2aa8'], [1, '#d03a7a']]), { dir: 0, fallback: 0, maxR: 26, group: 'bg', jit: .08, detail: 1.6 });
  R.text(str, w / 2, sub ? h * .56 : h * .66, `700 ${big}px ${F}`, lin(0, 20, 0, h * .6, [[0, col1], [1, col2]]), { dir: 'edge', fallback: 20, maxR: 6, group: 't' });
  if (sub) R.text(sub, w / 2, h * .84, `600 ${small}px ${F}`, '#ffe6b0', { dir: 'edge', fallback: 10, maxR: 4, group: 's' });
  const st = paintRef(R, { R: [26, 12, 6, 3, 2], T: 10, seed: 31, app: (x, y) => x / w * .9 + y / h * .05 });
  return { strokes: st, ref: R };
}

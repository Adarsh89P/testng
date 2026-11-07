// Neelkanth: extra plates (sea, Mandara mountain with Vasuki, devas and asuras, poison sky). Kailash, Shiva, linga and lettering come from scenes.js
import { Ref, paintRef } from './engine/plate.js';
import { P, lin, rad, hash } from './common.js';
import { SW, SH } from './scenes.js';

const blob = (R, cx, cy, rx, ry, col, props = {}) => R.fill(c => c.ellipse(cx, cy, rx, ry, 0, 0, 7), col, props);
export const SEA_Y = 640, FEET_Y = 760;

export function buildSea() {
  const R = new Ref(SW, SH, 1);
  R.fill(P([[0, 0], [SW, 0], [SW, SEA_Y + 40], [0, SEA_Y + 40]]), lin(0, 0, 0, SEA_Y, [[0, '#2a48b8'], [.35, '#6a7ae0'], [.7, '#ffa890'], [1, '#ffe2a0']]), { dir: -6, fallback: -6, group: 'sky', maxR: 40, jit: .08, detail: 2.2, aj: .3 });
  R.fill(c => c.arc(1056, SEA_Y - 70, 190, 0, 7), rad(1056, SEA_Y - 70, 10, 190, [[0, '#fffbd0'], [.6, '#ffd860'], [1, '#ffa050']]), { dir: { radial: [1056, SEA_Y - 70], off: 90 }, maxR: 18, group: 'sky', jit: .05 });
  const cloud = (x, y, w, h, top, und) => R.fill(c => { c.ellipse(x, y, w, h, 0, 0, 7); c.ellipse(x - w * .55, y + h * .3, w * .6, h * .7, 0, 0, 7); c.ellipse(x + w * .6, y + h * .35, w * .55, h * .6, 0, 0, 7); }, lin(0, y - h, 0, y + h, [[0, top], [.65, top], [1, und]]), { dir: -4, fallback: -4, group: 'sky', maxR: 28, detail: 1.6, aj: .3 });
  cloud(360, 170, 300, 56, '#8a8ae8', '#ffa8b0'); cloud(1700, 140, 340, 60, '#7a7ae0', '#ffb0a8'); cloud(1180, 300, 240, 36, '#b890e0', '#ffc090'); cloud(160, 400, 220, 30, '#d4a0e0', '#ffc898');
  // far shore
  R.fill(P([[0, SEA_Y + 20], [200, SEA_Y - 40], [520, SEA_Y - 8], [820, SEA_Y - 50], [1300, SEA_Y - 20], [1600, SEA_Y - 60], [1900, SEA_Y - 20], [SW, SEA_Y - 40], [SW, SEA_Y + 40], [0, SEA_Y + 40]]), lin(0, SEA_Y - 60, 0, SEA_Y + 40, [[0, '#4a62b8'], [1, '#33509a']]), { dir: 70, fallback: 70, group: 'shore', maxR: 16 });
  // the milk-ocean: layered bands of teal, with foam crests
  const bands = [[SEA_Y, SEA_Y + 70, '#3ac0c8', '#2a98b8', 14, 5], [SEA_Y + 70, SEA_Y + 170, '#2a98b8', '#1f70a8', 18, 9], [SEA_Y + 170, SEA_Y + 300, '#1f70a8', '#1a4a98', 24, 14], [SEA_Y + 300, SH, '#1a4a98', '#14307a', 30, 20]];
  bands.forEach(([y0, y1, a, b, r, amp], i) => {
    const pts = [[0, y1]]; for (let x = 0; x <= SW; x += 48) pts.push([x, y0 + Math.sin(x * .011 + i * 2) * amp + Math.sin(x * .027 + i) * amp * .4]); pts.push([SW, y1]);
    R.fill(P(pts), lin(0, y0, 0, y1, [[0, a], [1, b]]), { dir: 0, fallback: 0, group: 'sea' + i, maxR: r, jit: .09 });
  });
  for (let k = 0; k < 26; k++) { const y = SEA_Y + 30 + hash(k * 3) * 380, x = hash(k * 5 + 2) * SW, w = 90 + hash(k * 7) * 170; R.line(c => { c.moveTo(x, y); c.quadraticCurveTo(x + w / 2, y - 14 - hash(k) * 10, x + w, y); }, k % 3 ? '#e8fbff' : '#a8f0ff', 6 + hash(k * 11) * 5, { dir: 0, maxR: 5, group: 'foam' + k }); }
  return { strokes: paintRef(R, { R: [44, 22, 10, 5, 2.6], T: 12, seed: 61 }), ref: R };
}

export const MW = 760, MH = 700, MOX = 380, MOY = 660;     // Mandara, base centre at (MOX,MOY)
export function buildMountain() {
  const R = new Ref(MW, MH, 1.2), X = MOX, Y = MOY, p = pts => P(pts.map(([x, y]) => [x + X, y + Y]));
  R.fill(p([[-330, 0], [-250, -230], [-150, -330], [-70, -470], [0, -610], [60, -500], [140, -380], [250, -250], [330, 0]]), lin(0, Y - 610, 0, Y, [[0, '#f6c88a'], [.35, '#d8884a'], [1, '#8a4a7a']]), { dir: 70, fallback: 70, maxR: 22, group: 'mt', jit: .08 });
  R.fill(p([[0, -610], [60, -500], [140, -380], [250, -250], [330, 0], [120, 0], [60, -260]]), lin(X, 0, X + 330, 0, [[0, '#a85a8a'], [1, '#5a3a8a']]), { dir: 60, maxR: 16, group: 'shade' });
  R.fill(p([[-70, -470], [0, -610], [30, -540], [-10, -500], [-40, -520]]), '#fff0f4', { dir: 40, maxR: 7, group: 'snow' });
  for (const [dx, dy, r] of [[-200, -110, 60], [-120, -200, 46], [160, -120, 52], [110, -250, 40], [-40, -150, 50]]) blob(R, X + dx, Y + dy, r, r * .7, lin(0, Y + dy - r, 0, Y + dy + r, [[0, '#58d878'], [1, '#1a9a58']]), { type: 2, maxR: 12, group: 'tr' + dx, jit: .1 });
  // Vasuki's coils, three turns round the mountain
  for (const [dy, w, k] of [[-120, 300, 0], [-200, 250, 1], [-280, 200, 2]]) {
    R.line(c => { c.moveTo(X - w, Y + dy + 20); c.bezierCurveTo(X - w * .5, Y + dy + 70, X + w * .5, Y + dy + 70, X + w, Y + dy + 20); }, '#38d890', 30, { dir: 0, maxR: 8, group: 'coil' + k });
    R.line(c => { c.moveTo(X - w, Y + dy + 16); c.bezierCurveTo(X - w * .5, Y + dy + 62, X + w * .5, Y + dy + 62, X + w, Y + dy + 16); }, '#c8ffd8', 8, { dir: 0, maxR: 3, group: 'coilh' + k });
  }
  return { strokes: paintRef(R, { R: [30, 15, 7.5, 3.8, 2.2], T: 10, seed: 63 }), ref: R };
}

export const RW = SW, RH = 260, RPY = 130;      // the serpent used as a rope, plate drawn at world y offset
export function buildRope(yRope) {
  const R = new Ref(RW, RH, 1.1);
  const path = c => { c.moveTo(290, RPY + 10); c.bezierCurveTo(600, RPY + 70, 800, RPY + 30, 1056, RPY + 60); c.bezierCurveTo(1300, RPY + 30, 1500, RPY + 70, 1790, RPY + 10); };
  R.line(path, '#1f9a60', 38, { dir: 'edge', maxR: 7, group: 'rope' });
  R.line(path, '#46e090', 24, { dir: 'edge', maxR: 5, group: 'rope2' });
  R.line(c => { c.moveTo(290, RPY + 4); c.bezierCurveTo(600, RPY + 62, 800, RPY + 22, 1056, RPY + 52); c.bezierCurveTo(1300, RPY + 22, 1500, RPY + 62, 1790, RPY + 4); }, '#d8ffe8', 6, { dir: 'edge', maxR: 3, group: 'ropeh' });
  // hood and head at the asura end (right), tail at the deva end (left)
  R.fill(c => { c.moveTo(1790, RPY + 10); c.bezierCurveTo(1800, RPY - 60, 1880, RPY - 60, 1900, RPY + 10); c.bezierCurveTo(1880, RPY + 50, 1810, RPY + 50, 1790, RPY + 10); }, '#1f9a60', { dir: 90, maxR: 8, group: 'hood' });
  R.fill(c => c.ellipse(1850, RPY + 10, 30, 22, 0, 0, 7), '#46e090', { maxR: 6, group: 'head' });
  R.line(c => { c.moveTo(1862, RPY + 6); c.lineTo(1880, RPY + 4); }, '#ff2a2a', 4, { maxR: 2, group: 'eye' });
  R.fill(P([[290, RPY - 4], [220, RPY + 24], [290, RPY + 24]]), '#1f9a60', { maxR: 5, group: 'tail' });
  return { strokes: paintRef(R, { R: [22, 11, 5.5, 2.8], T: 9, seed: 65 }), ref: R };
}

// a puller / supplicant. kind: 'deva' | 'asura'; pose: 'pull' | 'pray'. Faces right; mirror to face left.
export const PW = 340, PH = 440, PX = 150, PY = 420;
export function buildFigure(kind, pose) {
  const R = new Ref(PW, PH, 1.8), X = PX, Y = PY, p = pts => P(pts.map(([x, y]) => [x + X, y + Y]));
  const dv = kind === 'deva', sk = dv ? '#f0a878' : '#4aa878', dh1 = dv ? '#4a8af0' : '#e04a3a', dh2 = dv ? '#2a52b8' : '#a02a3a', gold = '#ffd23a';
  const limb = (pts, w, col, g) => R.line(c => pts.forEach(([x, y], i) => i ? c.lineTo(x + X, y + Y) : c.moveTo(x + X, y + Y)), col, w, { dir: 'edge', maxR: 5, group: g });
  const kneel = pose === 'pray';
  if (kneel) {
    R.fill(p([[-70, 0], [70, 0], [60, -70], [-60, -70]]), lin(0, Y - 70, 0, Y, [[0, dh1], [1, dh2]]), { dir: 0, maxR: 8, group: 'dh' });
  } else {
    limb([[-12, -100], [-34, -4]], 26, dh2, 'l1'); limb([[16, -100], [44, -4]], 26, dh2, 'l2');
    R.fill(p([[-40, -100], [40, -100], [48, -50], [-48, -50]]), lin(0, Y - 100, 0, Y - 50, [[0, dh1], [1, dh2]]), { dir: 0, maxR: 7, group: 'dh' });
  }
  const ty = kneel ? -76 : -100, lean = kneel ? 0 : 22;
  R.fill(p([[-26, ty], [26, ty], [24 + lean, ty - 100], [-24 + lean, ty - 100]]), sk, { dir: 90, maxR: 6, group: 'tor' });
  R.fill(p([[-28, ty - 70], [28, ty - 70], [26 + lean, ty - 100], [-26 + lean, ty - 100]]), dv ? '#fff0c0' : '#ffb04a', { maxR: 4, group: 'sash' });
  if (kneel) { limb([[0, ty - 92], [30, ty - 60], [46, ty - 98]], 14, sk, 'a1'); limb([[6, ty - 90], [32, ty - 58], [48, ty - 96]], 14, sk, 'a2'); }
  else { limb([[lean, ty - 92], [lean + 50, ty - 84], [lean + 96, ty - 90]], 15, sk, 'a1'); limb([[lean - 4, ty - 84], [lean + 46, ty - 74], [lean + 96, ty - 82]], 15, sk, 'a2'); }
  R.fill(c => c.arc(X + lean + 2, Y + ty - 126, 26, 0, 7), sk, { dir: 'edge', maxR: 5, group: 'hd' });
  R.fill(P([[X + lean + 24, Y + ty - 128], [X + lean + 38, Y + ty - 118], [X + lean + 24, Y + ty - 112]]), sk, { maxR: 3, group: 'nose' });
  R.line(c => { c.moveTo(X + lean + 12, Y + ty - 130); c.lineTo(X + lean + 22, Y + ty - 129); }, '#2a1a2a', 3, { maxR: 2, group: 'eye' });
  if (dv) R.fill(P([[X + lean - 22, Y + ty - 148], [X + lean - 18, Y + ty - 188], [X + lean - 4, Y + ty - 164], [X + lean + 4, Y + ty - 194], [X + lean + 14, Y + ty - 164], [X + lean + 26, Y + ty - 186], [X + lean + 26, Y + ty - 148]]), lin(0, Y + ty - 194, 0, Y + ty - 148, [[0, '#fff2a0'], [1, gold]]), { dir: 90, maxR: 5, group: 'cr' });
  else { for (const s of [-1, 1]) R.fill(P([[X + lean + s * 16, Y + ty - 146], [X + lean + s * 34, Y + ty - 196], [X + lean + s * 6, Y + ty - 152]]), '#fff0d0', { maxR: 3, group: 'hn' + s }); R.fill(c => c.ellipse(X + lean - 4, Y + ty - 142, 28, 12, 0, 0, 7), '#2a1a3a', { maxR: 4, group: 'hr' }); }
  return { strokes: paintRef(R, { R: [18, 9, 4.5, 2.4], T: 9, seed: dv ? (kneel ? 71 : 72) : (kneel ? 73 : 74) }), ref: R };
}

export function buildPoisonSky() {       // dark green-violet wash laid over the sea scene when Halahala rises
  const R = new Ref(SW, SH, 1);
  R.fill(P([[0, 0], [SW, 0], [SW, SH], [0, SH]]), lin(0, 0, 0, SH, [[0, '#0c1a28'], [.45, '#2a1a4a'], [.75, '#1a4a3a'], [1, '#0c2a22']]), { dir: -8, fallback: -8, group: 'ps', maxR: 40, jit: .1, detail: 2 });
  return { strokes: paintRef(R, { R: [48, 24, 12, 6], T: 10, seed: 67 }), ref: R };
}

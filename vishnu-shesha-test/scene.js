// Vishnu on Shesha (Anantashayana) — Shadow Puppetry test frame
// Engine (carve.js, gl.js, stage.js) copied from the library's Shadow Puppetry style.
import { makeGL } from './gl.js';
import { canvas, piece, fill, cut, cutLine, ink, within, smooth, poly, scalesOpen, scales, lattice, coin, cloud, beads, beadLine, plum, waves, meander, rivet, flameTongue, cutTaper, DYE } from './carve.js';
import { drawFrame } from './stage.js';

const W = 1920, H = 1080;
const [trc, tr] = canvas(W, H), [frc, fr] = canvas(W, H);
const GL = makeGL(document.getElementById('gl'));
await document.fonts.load('400 46px "IM Fell English"');
await document.fonts.load('italic 400 46px "IM Fell English"');

const CAM = [960, 560, .93];
const C = [CAM[2], 0, 0, CAM[2], 960 - CAM[0] * CAM[2], 540 - CAM[1] * CAM[2]];
const PI = Math.PI;
let SEED = 0;

// —— helpers ——
// a piece of hide drawn in world coordinates (box in world px), multiplied onto the transmission canvas
function put(box, fn, ss = 2) {
  const p = piece(box, fn, { seed: ++SEED, ss });
  tr.save(); tr.setTransform(...C); tr.globalCompositeOperation = 'multiply';
  tr.drawImage(p.c, p.x0, p.y0, p.w, p.h); tr.restore();
}
// Catmull-Rom sample through control points
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
// closed outline of a band along a centre line; w = width or w(u)
function band(pts, w, round = false) {
  const n = pts.length, L = [], R = [];
  for (let i = 0; i < n; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const l = Math.hypot(dx, dy) || 1; dx /= l; dy /= l;
    const ww = (typeof w === 'function' ? w(i / (n - 1)) : w) / 2;
    L.push([pts[i][0] - dy * ww, pts[i][1] + dx * ww]); R.push([pts[i][0] + dy * ww, pts[i][1] - dx * ww]);
  }
  const cap = (e, sgn) => {
    const a = pts[Math.max(0, e - 1)], b = pts[Math.min(n - 1, e + 1)], ang = Math.atan2(b[1] - a[1], b[0] - a[0]) + (sgn > 0 ? 0 : PI);
    const ww = (typeof w === 'function' ? w(e / (n - 1)) : w) / 2, out = [];
    for (let k = 1; k < 12; k++) { const t = ang + PI / 2 - k * PI / 12; out.push([pts[e][0] + Math.cos(t) * ww, pts[e][1] + Math.sin(t) * ww]); }
    return out;
  };
  const out = round ? [...L, ...cap(n - 1, 1), ...R.reverse(), ...cap(0, -1)] : [...L, ...R.reverse()];
  return q => poly(q, out);
}
const line = (a, b, n = 10) => Array.from({ length: n + 1 }, (_, i) => [a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n]);
const bbox = (pts, pad) => { const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]); return [Math.min(...xs) - pad, Math.min(...ys) - pad, Math.max(...xs) + pad, Math.max(...ys) + pad]; };

// —— the Ocean of Milk: two liftable strips of raw hide ——
function ocean() {
  const strip = (y0, step, amp, col, r, wcut, seedOff) => {
    const top = q => {
      q.moveTo(-260, 1250); q.lineTo(-260, y0);
      for (let x = -260, i = 0; x < 2200; x += step, i++) {
        const y = y0 + Math.sin(i * 1.7 + seedOff) * 6;
        q.quadraticCurveTo(x + step * .35, y - amp, x + step * .62, y - amp * .55);   // crest
        q.quadraticCurveTo(x + step * .78, y - amp * .2, x + step, y);
      }
      q.lineTo(2200, 1250); q.closePath();
    };
    put([-260, y0 - amp - 20, 2200, 1250], g => {
      fill(g, col, top);
      within(g, top, () => {
        waves(g, -260, y0 + 22, 2200, 1250, r, wcut);
        for (let x = -260 + step * .5, i = 0; x < 2200; x += step, i++) cloud(g, x + 4, y0 - amp * .2 + 6, amp * .42, 2.2, 1.6, i % 2 ? 1 : -1);
      });
      ink(g, 2.2, top);
    });
  };
  strip(888, 118, 30, DYE.white, 15, 2.4, 0);
  strip(962, 160, 40, DYE.hide, 20, 3.2, 2);
}
function lotus(x, y, s) {
  put([x - 70 * s, y - 80 * s, x + 70 * s, y + 30 * s], g => {
    const pad = q => q.ellipse(x, y + 8 * s, 62 * s, 13 * s, 0, 0, 2 * PI);
    fill(g, DYE.green, pad); within(g, pad, () => { for (let k = -4; k <= 4; k++) cutLine(g, 1.4, q => { q.moveTo(x, y + 8 * s); q.lineTo(x + k * 15 * s, y + (k % 2 ? 18 : 2) * s); }); }); ink(g, 1.6, pad);
    for (const [a, h, col] of [[-1.05, 46, DYE.crim], [1.05, 46, DYE.crim], [-.62, 58, DYE.red], [.62, 58, DYE.red], [-.25, 66, DYE.red], [.25, 66, DYE.red], [0, 72, DYE.orange]]) {
      g.save(); g.translate(x, y); g.rotate(a); g.scale(s, s);
      const pet = q => { q.moveTo(0, 0); q.bezierCurveTo(-17, -h * .35, -12, -h * .8, 0, -h); q.bezierCurveTo(12, -h * .8, 17, -h * .35, 0, 0); q.closePath(); };
      fill(g, col, pet); within(g, pet, () => cutTaper(g, [[0, -6], [-2, -h * .45], [0, -h * .82]], 4)); ink(g, 1.4, pet);
      g.restore();
    }
  });
}

// —— Shesha: one long jointless body, tail in the sea, three coils, neck rising at the left ——
const arcPts = (cx, cy, r, a0, a1, n = 14) => Array.from({ length: n + 1 }, (_, i) => { const a = a0 + (a1 - a0) * i / n; return [cx + Math.cos(a) * r, cy + Math.sin(a) * r]; });
const SPINE = [
  ...curve([[1720, 940], [1640, 912], [1540, 892], [1440, 884]], 10),
  ...line([1440, 884], [520, 884], 40).slice(1),
  ...arcPts(520, 850, 34, PI / 2, 1.5 * PI).slice(1),                 // left bend: bottom → middle
  ...line([520, 816], [1390, 816], 40).slice(1),
  ...arcPts(1390, 784, 32, PI / 2, -PI / 2).slice(1),                 // right bend: middle → top
  ...line([1390, 752], [540, 752], 40).slice(1),
  ...curve([[540, 752], [470, 736], [432, 680], [426, 600], [450, 520], [500, 456], [560, 418]], 10).slice(1)
];
function shesha() {
  const n = SPINE.length;
  const wfn = u => u < .1 ? 10 + 54 * Math.sin(u / .1 * PI / 2) : u > .86 ? 64 - 14 * (u - .86) / .14 : 64;
  const body = band(SPINE, wfn);
  put(bbox(SPINE, 50), g => {
    fill(g, DYE.jade, body, 'nonzero');
    within(g, body, () => scalesOpen(g, 360, 400, 1760, 970, 9));
    // belly plates: a dark seam along each coil
    ink(g, 1.4, q => poly(q, SPINE.slice(Math.round(n * .2), Math.round(n * .8)), false), 'rgba(26,16,10,.55)');
    ink(g, 2.4, body);
  });
  // the hood canopy: seven hoods fanned over the god's head
  const B = [566, 420];
  const hoods = [[-.72, .84], [-.42, .94], [-.12, 1.02], [.18, 1.1], [.48, 1.02], [.78, .94], [1.08, .84]];
  for (const [a, s] of hoods) {
    const L = 175 * s;
    put([B[0] - 260, B[1] - 260, B[0] + 260, B[1] + 60], g => {
      g.translate(B[0] + Math.sin(a) * 26, B[1] - Math.cos(a) * 26 + Math.abs(a) * 14); g.rotate(a);
      const outer = q => smooth(q, [[-11, 0], [-20, -L * .3], [-36, -L * .58], [-44, -L * .76], [-36, -L * .92], [-18, -L * .99], [0, -L * .97], [18, -L * .99], [36, -L * .92], [44, -L * .76], [36, -L * .58], [20, -L * .3], [11, 0]]);
      const inner = q => smooth(q, [[-5, -L * .16], [-14, -L * .38], [-28, -L * .6], [-32, -L * .76], [-22, -L * .87], [0, -L * .85], [22, -L * .87], [32, -L * .76], [28, -L * .6], [14, -L * .38], [5, -L * .16]]);
      fill(g, DYE.green, outer);
      within(g, outer, () => scales(g, -44, -L * 1.05, 44, 0, 6, 1.3));
      fill(g, DYE.hide, inner);
      within(g, inner, () => { lattice(g, -30, -L * .86, 30, -L * .12, 9, 1.9); });
      // the spectacle mark: two coin holes joined by a carved arc
      coin(g, -13, -L * .72, 7); coin(g, 13, -L * .72, 7);
      cutLine(g, 2.2, q => q.arc(0, -L * .64, 14, 1.12 * PI, 1.88 * PI));
      ink(g, 1.6, inner); ink(g, 2.2, outer);
      // the small serpent head at the tip: eyes and a forked tongue
      const hy = -L * 1.0, hd = q => smooth(q, [[-15, hy + 6], [-17, hy - 6], [-9, hy - 16], [0, hy - 20], [9, hy - 16], [17, hy - 6], [15, hy + 6], [0, hy + 10]]);
      fill(g, DYE.green, hd); within(g, hd, () => scales(g, -18, hy - 20, 18, hy + 10, 3.6, 1));
      cut(g, q => { q.ellipse(-7, hy - 4, 3.4, 2.4, -.3, 0, 2 * PI); q.moveTo(10.4, hy - 4); q.ellipse(7, hy - 4, 3.4, 2.4, .3, 0, 2 * PI); });
      ink(g, 1.6, hd);
      ink(g, 1.4, q => { q.moveTo(0, hy - 20); q.lineTo(0, hy - 30); q.lineTo(-4, hy - 36); q.moveTo(0, hy - 30); q.lineTo(4, hy - 36); }, DYE.crim);
    });
  }
}

// —— Vishnu ——
const facePts = [[-6, 6], [8, 6], [9, -6], [13, -12], [18, -15], [19.5, -19], [21, -21.5], [19.5, -23.2], [22.5, -24.5], [21.5, -28], [24, -29.5], [27.5, -32.5], [22, -42], [18.5, -52], [17.5, -60], [17, -65], [-2, -64], [-6, -56], [-5, -40], [-9, -26], [-10, -10]];
const hairPts = [[-2, -64], [-18, -64], [-30, -58], [-34, -40], [-32, -14], [-26, 10], [-14, 18], [-6, 7], [-10, -10], [-9, -26], [-4.5, -33], [-5, -40], [-6, -56]];
const N = [636, 668], HK = 1.5;
function head() {
  put([N[0] - 100, N[1] - 260, N[0] + 90, N[1] + 50], g => {
    g.translate(N[0], N[1]); g.scale(HK, HK);
    const neck = q => poly(q, [[-6, 2], [9, 2], [14, 26], [-10, 26]]);
    fill(g, DYE.blue, neck);
    const hair = q => smooth(q, hairPts);
    fill(g, DYE.ink, hair);
    within(g, hair, () => { for (let k = 0; k < 7; k++) cutLine(g, .8, q => { q.moveTo(-6 - k * 3.5, -60); q.quadraticCurveTo(-26 - k, -36 + k * 2, -18 - k * 1.5, 10 + k); }); });
    // open-cut face: only the outline and features are left as hide
    ink(g, 2.4, q => poly(q, facePts.slice(1, 17), false), DYE.blue);
    ink(g, 1.5, q => { q.moveTo(15.5, -44.2); q.quadraticCurveTo(8, -47.5, -1, -45.5); });
    ink(g, 1.1, q => { q.moveTo(15, -43.4); q.quadraticCurveTo(8, -40.5, 1.5, -43.6); });
    g.beginPath(); g.arc(10, -44, 1.8, 0, 2 * PI); g.fillStyle = DYE.ink; g.fill();
    fill(g, DYE.ink, q => smooth(q, [[17.5, -51], [10, -53.5], [0, -55], [-6, -57], [-5, -55], [2, -52.4], [10, -50.8], [17, -49.4]]));
    ink(g, 1.2, q => { q.moveTo(20.3, -23.4); q.quadraticCurveTo(17, -21.6, 15, -22.8); });
    ink(g, 1.2, q => { q.moveTo(16.5, -14.5); q.quadraticCurveTo(7, -9, -4, -22); });
    ink(g, 2.2, q => { q.moveTo(14.2, -62); q.lineTo(14.2, -54); }, DYE.red);             // tilak
    // kirita crown
    const crown = q => poly(q, [[-26, -62], [19, -64], [17, -80], [13, -108], [7, -132], [1, -142], [-5, -132], [-13, -108], [-20, -80]]);
    fill(g, DYE.yellow, crown);
    within(g, crown, () => {
      lattice(g, -20, -128, 16, -86, 7, 1.5);
      beadLine(g, -24, -70, 17, -71, 1.3, 4.5); meander(g, -22, -76, 15, 3.4, 1);
      coin(g, -3, -96, 4.5);
    });
    ink(g, 1.6, crown);
    g.save(); g.translate(1, -141); g.beginPath(); flameTongue(g, 18, 10, 1); g.fillStyle = DYE.orange; g.fill(); g.lineWidth = 1.2; g.strokeStyle = DYE.ink; g.stroke(); g.restore();
    // side flare of the crown and the makara earring
    const flare = q => smooth(q, [[-22, -78], [-38, -92], [-44, -80], [-34, -70], [-24, -68]]);
    fill(g, DYE.red, flare); cloud(g, -36, -82, 4.6, 0, 1, -1); ink(g, 1.3, flare);
    const ear = q => q.arc(-4, -28, 7, 0, 2 * PI);
    fill(g, DYE.gold, ear); coin(g, -4, -28, 4.2); ink(g, 1.2, ear);
  }, 3);
}
function limb(pts, w0, w1, col, deco) {
  const P = curve(pts, 8), b = band(P, u => w0 + (w1 - w0) * u, true);
  put(bbox(P, Math.max(w0, w1)), g => {
    fill(g, col, b, 'nonzero');
    if (deco) within(g, b, () => deco(g, P));
    ink(g, 1.8, b);
  });
}
function hand(p, a, s = 1) {
  put([p[0] - 30, p[1] - 30, p[0] + 30, p[1] + 30], g => {
    g.translate(p[0], p[1]); g.rotate(a); g.scale(s, s);
    const h = q => smooth(q, [[-8, -9], [10, -10], [19, -6], [21, 0], [17, 6], [6, 9], [-8, 8]]);
    fill(g, DYE.blue, h); ink(g, 1.4, h);
    ink(g, .9, q => { q.moveTo(8, -3); q.lineTo(18, -2); q.moveTo(8, 3); q.lineTo(17, 4); });
  });
}
function bangle(g, P, u, w) { const i = Math.round(u * (P.length - 1)), [x, y] = P[i]; g.save(); g.beginPath(); g.arc(x, y, w, 0, 2 * PI); g.fillStyle = DYE.gold; g.fill(); g.restore(); coin(g, x, y, w * .55); }
function arm(sh, el, hd, dye = DYE.blue) {
  limb([sh, el], 34, 26, dye, (g, P) => bangle(g, P, .25, 12));
  limb([el, hd], 26, 19, dye, (g, P) => bangle(g, P, .9, 9));
  hand(hd, Math.atan2(hd[1] - el[1], hd[0] - el[0]));
  return [el];
}
function vishnu() {
  // the two raised hands behind: conch and discus
  const jC = arm([694, 676], [758, 604], [836, 530]);
  const jD = arm([678, 670], [700, 596], [736, 532]);
  // propping arm under the head
  const jA = arm([664, 684], [604, 738], [592, 666]);
  // torso, lying on its side
  const T = curve([[662, 690], [740, 694], [820, 700], [905, 706]], 8);
  const tb = band(T, u => u < .4 ? 104 - 20 * u : u < .75 ? 96 - 60 * (u - .4) : 75 + 40 * (u - .75), true);
  put(bbox(T, 60), g => {
    fill(g, DYE.blue, tb, 'nonzero');
    within(g, tb, () => {
      for (const [x, y] of [[720, 676], [770, 708], [812, 684], [856, 714]]) plum(g, x, y, 5);
      // vanamala: the forest garland, a red strip of carved blossoms
      const gar = band(curve([[676, 644], [720, 690], [790, 730], [870, 742], [912, 730]], 8), 13);
      fill(g, DYE.red, gar, 'nonzero');
      within(g, gar, () => beadLine(g, 676, 644, 912, 738, 2.2, 9));
      beads(g, curve([[680, 650], [722, 694], [792, 733], [868, 744]], 6), 2.4);
      ink(g, 1.2, gar);
      // the sacred thread
      ink(g, 2.4, q => { q.moveTo(690, 642); q.quadraticCurveTo(760, 700, 850, 752); }, DYE.yellow);
      // necklace
      const nk = band(curve([[650, 668], [672, 694], [700, 712]], 6), 12);
      fill(g, DYE.gold, nk, 'nonzero'); within(g, nk, () => beadLine(g, 650, 668, 700, 712, 2, 7)); ink(g, 1.1, nk);
    });
    ink(g, 2.2, tb);
  });
  // pitambara: the yellow silk dhoti
  const Dh = curve([[892, 708], [990, 712], [1088, 712]], 8);
  const db = band(Dh, u => 100 - 42 * u, true);
  put(bbox(Dh, 60), g => {
    fill(g, DYE.yellow, db, 'nonzero');
    within(g, db, () => {
      lattice(g, 880, 650, 1100, 770, 12, 2.4);
      for (let k = 0; k < 6; k++) cutLine(g, 1.6, q => { q.moveTo(915 + k * 26, 666 + k * 2); q.quadraticCurveTo(930 + k * 28, 712, 920 + k * 30, 752 - k * 3); });
    });
    // red border along the hem
    const hem = band(curve([[892, 756], [990, 738], [1088, 734]], 6), 10);
    fill(g, DYE.red, hem, 'nonzero'); within(g, hem, () => meander(g, 892, 760, 1088, 4, 1.1)); ink(g, 1.2, hem);
    // sash knot
    const knot = q => smooth(q, [[890, 668], [918, 656], [930, 690], [910, 712], [886, 700]]);
    fill(g, DYE.crim, knot); cloud(g, 908, 684, 9, .5, 1.5); ink(g, 1.5, knot);
    ink(g, 2.2, db);
  });
  // legs: one stretched, one drawn up behind it
  const anklet = (g, P) => bangle(g, P, .92, 9);
  limb([[1060, 690], [1150, 678], [1222, 694]], 42, 26, DYE.blue, anklet);
  limb([[1080, 714], [1170, 716], [1258, 718]], 46, 28, DYE.blue, anklet);
  for (const [x, y, a] of [[1258, 718, -.25], [1222, 694, -.35]]) put([x - 30, y - 40, x + 60, y + 30], g => {
    g.translate(x, y); g.rotate(a);
    const f = q => smooth(q, [[-6, -12], [20, -16], [40, -12], [44, -4], [30, 6], [-4, 12]]);
    fill(g, DYE.blue, f); ink(g, 1.4, f); ink(g, .9, q => { q.moveTo(34, -10); q.lineTo(38, -3); });
  });
  // the resting front arm with the gada
  arm([694, 704], [786, 742], [866, 716]);
  put([840, 580, 1010, 730], g => {
    ink(g, 5, q => { q.moveTo(858, 724); q.lineTo(962, 618); }, DYE.brown);
    const bulb = q => q.ellipse(972, 606, 24, 30, .78, 0, 2 * PI);
    fill(g, DYE.gold, bulb); within(g, bulb, () => { for (let k = -2; k <= 2; k++) cutTaper(g, [[958 + k * 8, 584 + k * 6], [972 + k * 8, 606 + k * 1], [984 + k * 8, 628 - k * 4]], 4); }); ink(g, 1.8, bulb);
    const cap = q => q.arc(990, 588, 6, 0, 2 * PI); fill(g, DYE.red, cap); ink(g, 1.1, cap);
  });
  // Sudarshana chakra: a wheel cut almost entirely away, flames around the rim
  const [cx, cy] = [852, 474], R = 50;
  put([cx - 90, cy - 90, cx + 90, cy + 90], g => {
    for (let k = 0; k < 18; k++) {
      g.save(); g.translate(cx, cy); g.rotate(k * 2 * PI / 18); g.translate(0, -R + 4);
      g.beginPath(); flameTongue(g, 26, 12, k % 2 ? 1 : -1); g.fillStyle = k % 2 ? DYE.orange : DYE.red; g.fill(); g.lineWidth = 1.2; g.strokeStyle = DYE.ink; g.stroke(); g.restore();
    }
    const wheel = q => { q.arc(cx, cy, R, 0, 2 * PI); };
    fill(g, DYE.gold, wheel);
    cut(g, q => q.arc(cx, cy, R - 11, 0, 2 * PI));
    g.save(); g.fillStyle = DYE.gold; g.strokeStyle = DYE.gold; g.lineWidth = 3.4;
    for (let k = 0; k < 12; k++) { const a = k * PI / 6; g.beginPath(); g.moveTo(cx + Math.cos(a) * 10, cy + Math.sin(a) * 10); g.lineTo(cx + Math.cos(a) * (R - 10), cy + Math.sin(a) * (R - 10)); g.stroke(); }
    g.beginPath(); g.arc(cx, cy, 13, 0, 2 * PI); g.fill(); g.restore();
    coin(g, cx, cy, 8);
    beads(g, Array.from({ length: 24 }, (_, k) => [cx + Math.cos(k * PI / 12) * (R - 5.5), cy + Math.sin(k * PI / 12) * (R - 5.5)]), 2);
    ink(g, 1.6, wheel); ink(g, 1.2, q => q.arc(cx, cy, R - 11, 0, 2 * PI));
  }, 3);
  // Panchajanya: the conch
  const [sx, sy] = [744, 494];
  put([sx - 50, sy - 50, sx + 50, sy + 50], g => {
    g.translate(sx, sy); g.rotate(-.5);
    const shell = q => smooth(q, [[-30, 6], [-26, -12], [-12, -26], [8, -30], [26, -20], [34, -4], [26, 12], [10, 26], [-4, 34], [-14, 26]]);
    fill(g, DYE.hide2, shell);
    within(g, shell, () => { for (let k = 0; k < 5; k++) cutTaper(g, [[-18 + k * 8, 18 - k * 4], [-6 + k * 9, -2 - k * 3], [6 + k * 6, -22 + k]], 3.2); });
    ink(g, 1.6, q => { for (let i = 0; i <= 40; i++) { const a = i / 40 * PI * 3, r = 14 * (1 - i / 48); const x = 12 + Math.cos(a) * r, y = -6 + Math.sin(a) * r; i ? q.lineTo(x, y) : q.moveTo(x, y); } });
    ink(g, 2, shell);
  });
  // rivets at every joint
  tr.save(); tr.setTransform(...C);
  for (const p of [N, [664, 684], [694, 676], [678, 670], [694, 704], ...jA, ...jC, ...jD, [786, 742], [905, 706], [1088, 712], [1060, 690]]) rivet(tr, p[0], p[1], 4);
  tr.restore();
}
function rods() {
  tr.save(); tr.setTransform(...C); tr.globalCompositeOperation = 'multiply';
  tr.strokeStyle = 'rgba(70,55,40,.6)'; tr.lineCap = 'round';
  for (const [a, b, w] of [[[640, 640], [520, 1250], 2.6], [[836, 530], [1000, 1250], 2.2], [[736, 532], [800, 1250], 2.2], [[470, 600], [260, 1250], 2.6], [[1300, 816], [1420, 1250], 2.4]]) {
    tr.lineWidth = w; tr.beginPath(); tr.moveTo(...a); tr.lineTo(...b); tr.stroke();
    tr.fillStyle = 'rgba(40,28,18,.7)'; tr.beginPath(); tr.arc(a[0], a[1], 3.2, 0, 2 * PI); tr.fill();
  }
  tr.restore();
}
// the storyteller's placard
function placard(text) {
  const g = fr; g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
  g.font = 'italic 400 44px "IM Fell English"';
  const tw = g.measureText(text).width, seal = 46, w = 22 + seal + 20 + tw + 36, h = 70, x = 960 - w / 2, y = 1080 - 50 - h;
  g.shadowColor = 'rgba(0,0,0,.55)'; g.shadowBlur = 18; g.shadowOffsetY = 4;
  const gr = g.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, 'rgba(46,22,14,.94)'); gr.addColorStop(1, 'rgba(22,10,7,.94)');
  g.fillStyle = gr; g.beginPath(); g.roundRect(x, y, w, h, 6); g.fill(); g.shadowColor = 'transparent';
  g.strokeStyle = 'rgba(168,129,63,.8)'; g.lineWidth = 1.5; g.beginPath(); g.roundRect(x + 6, y + 6, w - 12, h - 12, 3); g.stroke();
  const sx = x + 22, sy = y + (h - seal) / 2;
  g.fillStyle = '#b3261b'; g.beginPath(); g.roundRect(sx, sy, seal, seal, 4); g.fill();
  // a carved lotus in the seal
  g.fillStyle = '#f6dcc0';
  for (const a of [-.9, -.45, 0, .45, .9]) { g.save(); g.translate(sx + seal / 2, sy + seal * .74); g.rotate(a); g.beginPath(); g.ellipse(0, -11, 4.2, 11, 0, 0, 2 * PI); g.fill(); g.restore(); }
  g.fillStyle = '#f3e2bf'; g.textBaseline = 'middle'; g.fillText(text, sx + seal + 20, y + h / 2 + 2);
  g.restore();
}

function render(t) {
  SEED = 0;
  tr.setTransform(1, 0, 0, 1, 0, 0); tr.globalCompositeOperation = 'source-over'; tr.fillStyle = '#fff'; tr.fillRect(0, 0, W, H);
  fr.setTransform(1, 0, 0, 1, 0, 0); fr.clearRect(0, 0, W, H);
  ocean();
  shesha();
  vishnu();
  head();
  lotus(300, 948, 1); lotus(1580, 960, 1.1); lotus(1130, 1000, .8);
  rods();
  drawFrame(fr, C, .85);
  placard('Vishnu rests upon Shesha, on the Ocean of Milk');
  const fl = k => 1 + .04 * Math.sin(t * 23 + k * 2.1);
  const lamps = [[852, 474, 1 * fl(0), 1.15], [520, 330, .72 * fl(1), .55], [1350, 620, .8 * fl(2), .45]];
  const n = lamps.reduce((a, l) => a + l[2], 0);
  GL.render(trc, frc, { lamps, cam: CAM, expo: 1.4 / Math.sqrt(n), sigB: 720, sigC: 130, amb: .24, vign: .6, sat: 1.16, contrast: .15, bloom: .32, time: t });
}
window.render = render; window.DUR = 1;
render(0);
window.READY = true;

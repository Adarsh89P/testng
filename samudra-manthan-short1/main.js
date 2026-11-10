// समुद्र मंथन — शॉर्ट 1: विष किसने ग्रहण किया?  (Shadow Puppetry, 1080×1920, 24 fps)
// Engine: carve.js + gl.js from the library's Shadow Puppetry style. Timing = the user's voice (audio/voice.mp3).
import { makeGL } from './gl.js';
import { canvas, piece, fill, cut, cutLine, ink, within, smooth, poly, scalesOpen, scales, lattice, coin, cloud, beads, beadLine, plum, waves, meander, flameTongue, cutTaper, strata, DYE } from './carve.js';

const W = 1080, H = 1920, PI = Math.PI;
const [trc, tr] = canvas(W, H), [frc, fr] = canvas(W, H);
const GL = makeGL(document.getElementById('gl'));
await document.fonts.load('700 90px "FreeSerif"', 'विष किसने ग्रहण किया समुद्र मंथन रहस्य');
await document.fonts.load('400 50px "FreeSerif"', 'विष्णु पुराण');
export const DUR = 57.0;

// —— maths ——
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
function curve(ctrl, per = 12) {
  const out = [], n = ctrl.length;
  for (let i = 0; i < n - 1; i++) {
    const p0 = ctrl[Math.max(0, i - 1)], p1 = ctrl[i], p2 = ctrl[i + 1], p3 = ctrl[Math.min(n - 1, i + 2)];
    for (let k = 0; k < per; k++) { const t = k / per, t2 = t * t, t3 = t2 * t; out.push([0, 1].map(j => .5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3))); }
  }
  out.push(ctrl[n - 1]); return out;
}
function band(pts, w, round = false) {
  const n = pts.length, L = [], R = [], wf = u => (typeof w === 'function' ? w(u) : w) / 2;
  for (let i = 0; i < n; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const l = Math.hypot(dx, dy) || 1; dx /= l; dy /= l; const ww = wf(i / (n - 1));
    L.push([pts[i][0] - dy * ww, pts[i][1] + dx * ww]); R.push([pts[i][0] + dy * ww, pts[i][1] - dx * ww]);
  }
  const cap = (e, sgn) => { const a = pts[Math.max(0, e - 1)], b = pts[Math.min(n - 1, e + 1)], ang = Math.atan2(b[1] - a[1], b[0] - a[0]) + (sgn > 0 ? 0 : PI), ww = wf(e / (n - 1)), o = []; for (let k = 1; k < 12; k++) { const t = ang + PI / 2 - k * PI / 12; o.push([pts[e][0] + Math.cos(t) * ww, pts[e][1] + Math.sin(t) * ww]); } return o; };
  const out = round ? [...L, ...cap(n - 1, 1), ...R.reverse(), ...cap(0, -1)] : [...L, ...R.reverse()];
  return q => poly(q, out);
}
let SEED = 0;
const mk = (box, fn, ss_ = 2) => piece(box, g => { g.lineJoin = 'round'; fn(g); }, { seed: ++SEED, ss: ss_ });
const limbIn = (g, pts, w0, w1, col, lw = 1.6) => { const b = band(curve(pts, 6), u => w0 + (w1 - w0) * u, true); fill(g, col, b, 'nonzero'); ink(g, lw, b); return b; };

// ================= SPRITES =================
const S = {};
// —— the Ocean of Milk: two strips ——
function seaStrip(step, amp, col, r, wcut, off) {
  const top = q => { q.moveTo(-160, 760); q.lineTo(-160, 0); for (let x = -160, i = 0; x < 1240; x += step, i++) { const y = Math.sin(i * 1.7 + off) * 6; q.quadraticCurveTo(x + step * .35, y - amp, x + step * .62, y - amp * .55); q.quadraticCurveTo(x + step * .78, y - amp * .2, x + step, y); } q.lineTo(1240, 760); q.closePath(); };
  return mk([-160, -amp - 20, 1240, 760], g => {
    fill(g, col, top);
    within(g, top, () => { waves(g, -160, 22, 1240, 760, r, wcut); for (let x = -160 + step * .5, i = 0; x < 1240; x += step, i++) cloud(g, x + 4, -amp * .2 + 6, amp * .42, 2.2, 1.6, i % 2 ? 1 : -1); });
    ink(g, 2.2, top);
  }, 1.5);
}
S.seaB = seaStrip(118, 30, DYE.white, 15, 2.4, 0);
S.seaF = seaStrip(160, 40, DYE.hide, 20, 3.2, 2);

// —— lettered plaques: dark hide, letters cut out so they glow ——
function plaque(lines, w, h, opt = {}) {
  return mk([-w / 2, -h / 2, w / 2, h / 2], g => {
    const body = q => { q.roundRect(-w / 2, -h / 2, w, h, 26); };
    fill(g, '#3a1a0e', body);
    cutLine(g, 2.4, q => q.roundRect(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32, 16));
    within(g, q => q.roundRect(-w / 2 + 26, -h / 2 + 26, w - 52, h - 52, 12), () => {});
    meander(g, -w / 2 + 40, -h / 2 + 34, w / 2 - 40, 5, 1.5); meander(g, -w / 2 + 40, h / 2 - 22, w / 2 - 40, 5, 1.5);
    g.save(); g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000'; g.textAlign = 'center'; g.textBaseline = 'middle';
    for (const [txt, y, size] of lines) { g.font = `700 ${size}px "FreeSerif"`; g.fillText(txt, 0, y); }
    g.restore();
    for (const x of [-w / 2 + 40, w / 2 - 40]) { coin(g, x, 0, 12); }
    ink(g, 3, body);
  }, 2);
}
S.hook = plaque([['विष किसने', -50, 104], ['ग्रहण किया?', 72, 104]], 800, 300);
S.title = plaque([['समुद्र मंथन', -78, 112], ['के रहस्य', 44, 104], ['विष्णु पुराण के अनुसार', 132, 44]], 860, 390);

// —— palm-leaf manuscript (pothi) ——
function pothi(label) {
  return mk([-280, -80, 280, 80], g => {
    for (const [y, col] of [[-44, DYE.brown], [44, DYE.brown]]) { const cv = q => q.roundRect(-270, y - 14, 540, 28, 10); fill(g, col, cv); within(g, cv, () => meander(g, -255, y + 6, 255, 4.5, 1.3)); ink(g, 1.6, cv); }
    const leaf = q => q.roundRect(-258, -30, 516, 60, 8);
    fill(g, DYE.hide2, leaf);
    within(g, leaf, () => { for (let k = -2; k <= 2; k++) cutLine(g, 1, q => { q.moveTo(-250, k * 11); q.lineTo(250, k * 11 + 1); }); });
    ink(g, 1.6, leaf);
    for (const x of [-170, 170]) { cut(g, q => q.arc(x, 0, 7, 0, 2 * PI)); ink(g, 3, q => { q.moveTo(x, -60); q.quadraticCurveTo(x + 6, 0, x, 62); }, DYE.red); }
    if (label) { g.save(); g.font = '700 46px "FreeSerif"'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = DYE.ink; g.fillText(label, 0, 2); g.restore(); }
  }, 2);
}
S.pothiVP = pothi('विष्णु पुराण'); S.pothiA = pothi(''); S.pothiB = pothi('');

// —— Shiva's trident with the damaru ——
S.trishul = mk([-120, -60, 120, 560], g => {
  const sh = q => q.roundRect(-9, 40, 18, 510, 6); fill(g, DYE.brown, sh); within(g, sh, () => beadLine(g, 0, 60, 0, 540, 2, 14)); ink(g, 1.6, sh);
  const head = q => { q.moveTo(-90, -40); q.quadraticCurveTo(-96, 40, -20, 62); q.lineTo(20, 62); q.quadraticCurveTo(96, 40, 90, -40); q.quadraticCurveTo(70, 10, 30, 22); q.lineTo(14, -50); q.lineTo(0, -60); q.lineTo(-14, -50); q.lineTo(-30, 22); q.quadraticCurveTo(-70, 10, -90, -40); q.closePath(); };
  fill(g, DYE.yellow, head); within(g, head, () => { lattice(g, -90, -60, 90, 62, 10, 2); coin(g, 0, 38, 9); }); ink(g, 2, head);
  // damaru: an hourglass drum tied below the prongs
  const dm = q => { q.moveTo(-44, 110); q.lineTo(44, 110); q.lineTo(6, 150); q.lineTo(44, 190); q.lineTo(-44, 190); q.lineTo(-6, 150); q.closePath(); };
  fill(g, DYE.red, dm); within(g, dm, () => { lattice(g, -44, 110, 44, 190, 9, 1.8); }); ink(g, 1.8, dm);
  ink(g, 2, q => { q.moveTo(-6, 150); q.quadraticCurveTo(-70, 170, -60, 230); q.moveTo(6, 150); q.quadraticCurveTo(70, 170, 64, 226); }, DYE.ink);
  for (const [x, y] of [[-60, 232], [64, 228]]) { const b = q => q.arc(x, y, 7, 0, 2 * PI); fill(g, DYE.gold, b); ink(g, 1.2, b); }
}, 2);
S.ring = mk([-170, -170, 170, 170], g => {
  const r = q => { q.arc(0, 0, 160, 0, 2 * PI); q.arc(0, 0, 118, 0, 2 * PI, true); };
  fill(g, DYE.teal, r); within(g, r, () => { for (let k = 0; k < 24; k++) { const a = k * PI / 12; coin(g, Math.cos(a) * 139, Math.sin(a) * 139, 9); } }); ink(g, 2, r);
}, 2);

// —— moon ——
S.moon = mk([-80, -80, 80, 80], g => {
  const m = q => { q.arc(0, 0, 70, 0, 2 * PI); q.moveTo(58, -18); q.arc(28, -18, 58, 0, 2 * PI, true); };
  fill(g, DYE.yellow, m, 'evenodd'); within(g, m, () => beadLine(g, -52, -30, -30, 52, 2.4, 9)); ink(g, 2, m);
}, 2);

// —— smoke wisps (dark, carved) ——
S.smoke = [0, 1, 2, 3].map(v => mk([-80, -260, 80, 30], g => {
  const sgn = v % 2 ? 1 : -1, P = curve([[0, 0], [sgn * 26, -60], [-sgn * 18, -130], [sgn * 24, -190], [-sgn * 8, -240]], 8);
  const b = band(P, u => 46 * (1 - u) + 6, true);
  fill(g, '#2b1a33', b, 'nonzero'); within(g, b, () => { for (let k = 0; k < 4; k++) cutTaper(g, P.slice(4 + k * 6, 14 + k * 6).map(([x, y]) => [x + sgn * 6, y]), 4); });
  ink(g, 1.4, b);
}, 2));

// —— generic puppet figure: deva or daitya, facing right, origin at the feet ——
const facePts = [[-6, 6], [8, 6], [9, -6], [13, -12], [18, -15], [19.5, -19], [21, -21.5], [19.5, -23.2], [22.5, -24.5], [21.5, -28], [24, -29.5], [27.5, -32.5], [22, -42], [18.5, -52], [17.5, -60], [17, -65], [-2, -64], [-6, -56], [-5, -40], [-9, -26], [-10, -10]];
function figure(kind, v = 0) {
  const D = kind === 'deva';
  const skin = D ? DYE.skin : DYE.teal, cloth = D ? (v ? DYE.orange : DYE.red) : (v ? DYE.green : DYE.crim);
  return mk([-120, -520, 150, 16], g => {
    limbIn(g, [[-8, -190], [-58, -4]], 32, 22, cloth); limbIn(g, [[10, -190], [46, -4]], 32, 22, cloth);
    for (const x of [-58, 46]) fill(g, DYE.ink, q => smooth(q, [[x - 16, -12], [x + 24, -12], [x + 28, 4], [x - 18, 6]]));
    const sk = q => smooth(q, [[-42, -252], [42, -252], [62, -150], [0, -128], [-62, -150]]);
    fill(g, D ? DYE.yellow : DYE.jade, sk); within(g, sk, () => lattice(g, -64, -252, 64, -128, 11, 2.2)); ink(g, 1.8, sk);
    const to = q => smooth(q, [[-32, -250], [-40, -300], [-32, -348], [0, -364], [32, -348], [42, -300], [34, -250]]);
    fill(g, D ? DYE.red : DYE.teal, to); within(g, to, () => scalesOpen(g, -44, -366, 46, -250, 7)); ink(g, 2, to);
    const belt = q => q.roundRect(-38, -262, 78, 18, 4); fill(g, DYE.gold, belt); within(g, belt, () => { for (let x = -28; x < 36; x += 14) coin(g, x, -253, 5); }); ink(g, 1.3, belt);
    limbIn(g, [[12, -338], [62, -302]], 24, 19, D ? DYE.orange : DYE.jade); limbIn(g, [[62, -302], [104, -276]], 19, 15, skin);
    fill(g, skin, q => q.arc(108, -275, 11, 0, 2 * PI)); ink(g, 1.3, q => q.arc(108, -275, 11, 0, 2 * PI));
    // head
    g.save(); g.translate(8, -362); g.scale(1.45, 1.45);
    fill(g, skin, q => poly(q, [[-6, 2], [9, 2], [12, 12], [-8, 12]]));
    fill(g, DYE.ink, q => smooth(q, [[-2, -64], [-18, -64], [-30, -58], [-34, -40], [-32, -14], [-26, 8], [-14, 14], [-6, 7], [-10, -10], [-9, -26], [-5, -40], [-6, -56]]));
    if (D) {   // open-cut face
      ink(g, 2.2, q => poly(q, facePts.slice(1, 17), false));
      ink(g, 1.4, q => { q.moveTo(15.5, -44.2); q.quadraticCurveTo(8, -47.5, -1, -45.5); });
      g.beginPath(); g.arc(10, -44, 1.8, 0, 2 * PI); g.fillStyle = DYE.ink; g.fill();
      fill(g, DYE.ink, q => smooth(q, [[17.5, -51], [10, -53.5], [0, -55], [-6, -57], [-5, -55], [2, -52.4], [10, -50.8], [17, -49.4]]));
      ink(g, 1.2, q => { q.moveTo(20.3, -23.4); q.quadraticCurveTo(17, -21.6, 15, -22.8); });
      const cr = q => poly(q, [[-24, -62], [18, -64], [15, -84], [8, -110], [0, -122], [-8, -110], [-16, -84]]);
      fill(g, DYE.yellow, cr); within(g, cr, () => { lattice(g, -20, -116, 16, -72, 6, 1.3); beadLine(g, -22, -68, 16, -69, 1.2, 4.4); }); ink(g, 1.5, cr);
    } else {   // solid fierce face, horns
      fill(g, DYE.teal, q => poly(q, facePts));
      cut(g, q => { q.moveTo(17, -46); q.lineTo(6, -49); q.lineTo(14, -42); q.closePath(); });
      fill(g, DYE.ink, q => poly(q, [[19, -50], [0, -60], [-6, -58], [2, -54]]));
      ink(g, 1.6, q => { q.moveTo(20, -20); q.lineTo(12, -18); }, DYE.ink);
      fill(g, DYE.white, q => poly(q, [[18, -16], [22, -10], [16, -12]]));
      ink(g, 2, q => poly(q, facePts));
      for (const s of [1, -1]) { const h = q => { q.moveTo(-6 + s * 8, -62); q.quadraticCurveTo(-4 + s * 24, -92, -14 + s * 34, -100); q.quadraticCurveTo(-2 + s * 14, -82, -14 + s * 2, -64); q.closePath(); }; fill(g, DYE.hide, h); ink(g, 1.4, h); }
      const cr = q => poly(q, [[-24, -62], [18, -64], [10, -78], [4, -70], [-4, -84], [-10, -70], [-18, -80]]);
      fill(g, DYE.red, cr); ink(g, 1.4, cr);
    }
    g.restore();
  }, 2);
}
S.deva = [figure('deva', 0), figure('deva', 1)];
S.daitya = [figure('daitya', 0), figure('daitya', 1)];

// —— Mandara, Vasuki, Kurma ——
S.mountain = mk([-190, -720, 190, 10], g => {
  const m = q => smooth(q, [[-178, 0], [-160, -200], [-128, -380], [-86, -540], [-44, -650], [0, -690], [44, -650], [90, -540], [130, -380], [160, -200], [178, 0]]);
  fill(g, DYE.gold, m); within(g, m, () => { strata(g, -190, 190, x => -560 + Math.abs(x) * 1.1 + Math.sin(x / 30) * 8, 9, 60, 5); lattice(g, -60, -640, 60, -560, 12, 2.2); }); ink(g, 2.4, m);
  for (const [x, y, s] of [[-40, -640, 1], [10, -672, 1.2], [52, -628, .9]]) { const tr_ = q => { q.moveTo(x, y + 6); q.lineTo(x - 18 * s, y - 2); q.lineTo(x, y - 46 * s); q.lineTo(x + 18 * s, y - 2); q.closePath(); }; fill(g, DYE.green, tr_); within(g, tr_, () => scales(g, x - 20, y - 46, x + 20, y + 6, 4, 1)); ink(g, 1.3, tr_); }
}, 2);
S.wrap = mk([-200, -40, 200, 40], g => {
  const b = band(curve([[-190, 24], [0, -2], [190, -26]], 8), 40, true);
  fill(g, DYE.jade, b, 'nonzero'); within(g, b, () => scalesOpen(g, -200, -40, 200, 40, 7)); ink(g, 2, b);
}, 2);
S.rope = mk([-560, -24, 560, 24], g => {
  const b = q => q.roundRect(-560, -20, 1120, 40, 20); fill(g, DYE.jade, b); within(g, b, () => scalesOpen(g, -560, -24, 560, 24, 7)); ink(g, 2, b);
}, 1.5);
S.vhead = mk([-60, -260, 120, 30], g => {
  const neck = band(curve([[0, 20], [-10, -60], [10, -140], [40, -190]], 8), u => 40 - 8 * u);
  fill(g, DYE.jade, neck); within(g, neck, () => scalesOpen(g, -60, -200, 80, 30, 7)); ink(g, 2, neck);
  const hood = q => smooth(q, [[10, -150], [-16, -200], [-6, -250], [40, -262], [86, -236], [96, -196], [70, -160]]);
  fill(g, DYE.green, hood); within(g, hood, () => { lattice(g, -10, -260, 90, -160, 9, 1.8); coin(g, 30, -214, 7); coin(g, 58, -212, 7); }); ink(g, 2, hood);
  const hd = q => smooth(q, [[70, -240], [110, -236], [120, -222], [100, -210], [70, -214]]);
  fill(g, DYE.jade, hd); cut(g, q => q.arc(96, -228, 3.4, 0, 2 * PI)); ink(g, 1.6, hd);
}, 2);
S.fire = [0, 1].map(v => mk([-20, -120, 260, 120], g => {
  for (let k = 0; k < 7; k++) {
    g.save(); g.translate(0, 0); g.rotate(-.5 + k * .17 + (v ? .06 : -.04)); g.translate(30, 0); g.rotate(PI / 2);
    g.beginPath(); flameTongue(g, 150 + hash(k + v * 9) * 70, 36, k % 2 ? 1 : -1); g.fillStyle = k % 2 ? DYE.orange : DYE.red; g.fill(); g.lineWidth = 1.4; g.strokeStyle = DYE.ink; g.stroke(); g.restore();
  }
}, 2));
S.cloud = mk([-200, -90, 200, 90], g => {
  const c = q => smooth(q, [[-180, 40], [-170, -10], [-120, -50], [-60, -40], [-20, -80], [50, -70], [90, -30], [150, -50], [190, 0], [170, 50], [80, 60], [0, 50], [-90, 64]]);
  fill(g, DYE.teal, c); within(g, c, () => { for (const [x, y, f] of [[-120, 0, 1], [-30, -20, -1], [60, -10, 1], [140, 10, -1]]) cloud(g, x, y, 24, .6, 2, f); }); ink(g, 2, c);
}, 2);
S.rain = [0, 1].map(v => mk([-180, 0, 180, 260], g => { for (let k = 0; k < 16; k++) { const x = -160 + k * 21 + v * 9, y = 10 + hash(k * 3 + v) * 60; ink(g, 2.4, q => { q.moveTo(x, y); q.lineTo(x - 14, y + 140 + hash(k) * 60); }, DYE.teal); } }, 2));
S.kurma = mk([-260, -20, 300, 160], g => {
  for (const [x, y, a] of [[-180, 120, .5], [180, 120, -.5]]) { const f = q => q.ellipse(x, y, 60, 22, a, 0, 2 * PI); fill(g, DYE.jade, f); ink(g, 1.6, f); }
  const hd = q => smooth(q, [[200, 60], [250, 40], [290, 54], [282, 82], [230, 90]]); fill(g, DYE.jade, hd); cut(g, q => q.arc(268, 56, 4, 0, 2 * PI)); ink(g, 1.6, hd);
  const sh = q => { q.moveTo(-230, 120); q.bezierCurveTo(-220, -10, 220, -10, 230, 120); q.closePath(); };
  fill(g, DYE.green, sh);
  within(g, sh, () => { for (let r = 0; r < 4; r++) for (let c = -5; c <= 5; c++) { const x = c * 42 + (r % 2) * 21, y = 20 + r * 30; cut(g, q => { for (let k = 0; k < 6; k++) { const a = k * PI / 3 + PI / 6; const px = x + Math.cos(a) * 15, py = y + Math.sin(a) * 12; k ? q.lineTo(px, py) : q.moveTo(px, py); } q.closePath(); }); } });
  ink(g, 2.2, sh);
}, 2);

// —— the treasures ——
S.cow = mk([-200, -260, 220, 10], g => {
  for (const x of [-120, -80, 90, 130]) limbIn(g, [[x, -110], [x + (x > 0 ? 4 : -4), -6]], 20, 14, DYE.hide2);
  const body = q => smooth(q, [[-150, -150], [-120, -196], [-20, -200], [60, -206], [110, -220], [150, -170], [146, -110], [80, -96], [-60, -94], [-150, -110]]);
  fill(g, DYE.hide, body);
  const cl = q => smooth(q, [[-80, -196], [70, -206], [80, -120], [-70, -112]]);
  fill(g, DYE.red, cl); within(g, cl, () => { lattice(g, -90, -210, 90, -110, 12, 2.2); }); ink(g, 1.6, cl);
  beadLine(g, -76, -114, 76, -122, 3, 12);
  ink(g, 2.2, body);
  const hump = q => smooth(q, [[96, -214], [116, -244], [140, -230], [146, -200]]); fill(g, DYE.hide, hump); ink(g, 1.6, hump);
  const head = q => smooth(q, [[140, -200], [176, -214], [204, -186], [206, -150], [180, -136], [150, -160]]); fill(g, DYE.hide, head); ink(g, 2, head);
  cut(g, q => q.ellipse(180, -184, 5, 3, 0, 0, 2 * PI));
  ink(g, 2.6, q => { q.moveTo(170, -212); q.quadraticCurveTo(160, -250, 188, -256); q.moveTo(180, -210); q.quadraticCurveTo(196, -240, 214, -236); }, DYE.ink);
  fill(g, DYE.gold, q => q.arc(178, -152, 9, 0, 2 * PI));
  ink(g, 2.4, q => { q.moveTo(-148, -150); q.quadraticCurveTo(-190, -110, -176, -40); }, DYE.ink); fill(g, DYE.ink, q => q.ellipse(-176, -36, 8, 14, 0, 0, 2 * PI));
}, 2);
S.tree = mk([-180, -520, 180, 10], g => {
  const tk = band(curve([[0, 0], [-6, -140], [8, -260]], 6), u => 44 - 26 * u); fill(g, DYE.brown, tk); within(g, tk, () => strata(g, -30, 30, x => -40 + x * .2, 6, 36, 2)); ink(g, 2, tk);
  for (const [x, y, r] of [[-90, -300, 90], [80, -310, 92], [0, -400, 110], [-60, -440, 70], [70, -450, 72]]) {
    const c = q => q.arc(x, y, r, 0, 2 * PI); fill(g, DYE.green, c);
    within(g, c, () => { for (let k = 0; k < 9; k++) { const a = hash(k * 7 + x) * 2 * PI, d = r * .65 * hash(k * 3 + y); plum(g, x + Math.cos(a) * d, y + Math.sin(a) * d, 6); ink(g, 2, q => { q.moveTo(x + Math.cos(a) * d, y + Math.sin(a) * d + 4); q.lineTo(x + Math.cos(a) * d, y + Math.sin(a) * d + 12); }, DYE.orange); } });
    ink(g, 1.8, c);
  }
}, 2);
S.apsara = mk([-120, -500, 140, 10], g => {
  const skirt = q => smooth(q, [[-20, -250], [30, -250], [80, -120], [110, -10], [30, 0], [-60, -4], [-90, -40], [-50, -150]]);
  fill(g, DYE.red, skirt); within(g, skirt, () => { lattice(g, -100, -250, 120, 0, 12, 2.2); }); ink(g, 2, skirt);
  ink(g, 6, q => { q.moveTo(-90, -30); q.quadraticCurveTo(10, -4, 108, -16); }, DYE.gold);
  const to = q => smooth(q, [[-18, -250], [32, -252], [36, -310], [20, -352], [-10, -350], [-24, -300]]); fill(g, DYE.yellow, to); within(g, to, () => scalesOpen(g, -26, -352, 38, -250, 6)); ink(g, 1.8, to);
  limbIn(g, [[18, -338], [70, -380], [96, -430]], 16, 11, DYE.skin);
  limbIn(g, [[-6, -336], [-60, -318], [-96, -340]], 16, 11, DYE.skin);
  const veil = q => { q.moveTo(-100, -350); q.bezierCurveTo(-130, -470, 90, -520, 100, -436); q.lineTo(90, -430); q.bezierCurveTo(70, -490, -110, -460, -92, -350); q.closePath(); };
  fill(g, DYE.jade, veil); within(g, veil, () => beadLine(g, -100, -380, 90, -470, 2, 10)); ink(g, 1.4, veil);
  g.save(); g.translate(8, -352); g.scale(1.3, 1.3);
  ink(g, 2, q => poly(q, facePts.slice(1, 17), false));
  g.beginPath(); g.arc(10, -44, 1.6, 0, 2 * PI); g.fillStyle = DYE.ink; g.fill();
  fill(g, DYE.ink, q => smooth(q, [[-2, -64], [-18, -66], [-30, -58], [-32, -40], [-26, -20], [-12, -14], [-8, -30], [-5, -40], [-6, -56]]));
  fill(g, DYE.ink, q => q.arc(-26, -66, 12, 0, 2 * PI)); plum(g, -26, -66, 4);
  g.restore();
}, 2);

// —— Nagas ——
S.naga = [0, 1, 2].map(v => mk([-90, -420, 90, 20], g => {
  const sg = v === 1 ? -1 : 1, P = curve([[0, 20], [sg * 30, -80], [-sg * 24, -190], [sg * 10, -280], [0, -320]], 8);
  const b = band(P, u => 46 - 16 * u); fill(g, v === 2 ? DYE.teal : DYE.jade, b); within(g, b, () => scalesOpen(g, -90, -330, 90, 20, 7)); ink(g, 2, b);
  const hood = q => smooth(q, [[-14, -290], [-56, -330], [-62, -380], [-30, -410], [0, -414], [30, -410], [62, -380], [56, -330], [14, -290]]);
  fill(g, DYE.green, hood); within(g, hood, () => { lattice(g, -60, -412, 60, -290, 9, 1.8); coin(g, -18, -366, 8); coin(g, 18, -366, 8); }); ink(g, 2.2, hood);
  const hd = q => q.ellipse(0, -414, 22, 15, 0, 0, 2 * PI); fill(g, DYE.jade, hd); cut(g, q => { q.ellipse(-9, -416, 4, 3, 0, 0, 2 * PI); q.moveTo(13, -416); q.ellipse(9, -416, 4, 3, 0, 0, 2 * PI); }); ink(g, 1.6, hd);
}, 2));

// —— chakra and conch for "जय श्री हरि" ——
S.chakra = mk([-100, -100, 100, 100], g => {
  const R = 56;
  for (let k = 0; k < 18; k++) { g.save(); g.rotate(k * 2 * PI / 18); g.translate(0, -R + 4); g.beginPath(); flameTongue(g, 30, 13, k % 2 ? 1 : -1); g.fillStyle = k % 2 ? DYE.orange : DYE.red; g.fill(); g.lineWidth = 1.3; g.strokeStyle = DYE.ink; g.stroke(); g.restore(); }
  fill(g, DYE.gold, q => q.arc(0, 0, R, 0, 2 * PI)); cut(g, q => q.arc(0, 0, R - 12, 0, 2 * PI));
  g.save(); g.strokeStyle = DYE.gold; g.fillStyle = DYE.gold; g.lineWidth = 4; for (let k = 0; k < 12; k++) { const a = k * PI / 6; g.beginPath(); g.moveTo(Math.cos(a) * 11, Math.sin(a) * 11); g.lineTo(Math.cos(a) * (R - 11), Math.sin(a) * (R - 11)); g.stroke(); } g.beginPath(); g.arc(0, 0, 14, 0, 2 * PI); g.fill(); g.restore();
  coin(g, 0, 0, 9); ink(g, 1.8, q => q.arc(0, 0, R, 0, 2 * PI));
}, 2);
S.conch = mk([-70, -70, 70, 70], g => {
  g.rotate(-.5);
  const sh = q => smooth(q, [[-40, 8], [-35, -16], [-16, -35], [10, -40], [35, -27], [45, -5], [35, 16], [13, 35], [-5, 45], [-19, 35]]);
  fill(g, DYE.hide2, sh); within(g, sh, () => { for (let k = 0; k < 5; k++) cutTaper(g, [[-24 + k * 11, 24 - k * 5], [-8 + k * 12, -3 - k * 4], [8 + k * 8, -29 + k]], 4.2); });
  ink(g, 2, q => { for (let i = 0; i <= 40; i++) { const a = i / 40 * PI * 3, r = 18 * (1 - i / 48), x = 16 + Math.cos(a) * r, y = -8 + Math.sin(a) * r; i ? q.lineTo(x, y) : q.moveTo(x, y); } });
  ink(g, 2.4, sh);
}, 2);

// ================= STAGE OVERLAY (frame, built once) =================
const [stc, st] = canvas(W, H);
{
  const lac = '#2a0d08', gold = '#8a6430';
  st.fillStyle = lac; st.fillRect(0, 0, W, 96); st.fillRect(0, H - 110, W, 110); st.fillRect(0, 0, 30, H); st.fillRect(W - 30, 0, 30, H);
  st.fillStyle = '#46140c'; st.fillRect(30, 22, W - 60, 52); st.fillRect(30, H - 92, W - 60, 40);
  st.strokeStyle = gold; st.lineWidth = 2.5;
  for (let x = 40; x < W - 60; x += 100) { st.beginPath(); for (let i = 0; i <= 30; i++) { const a = i / 30 * PI * 2.1, r = 22 * (1 - i / 30 * .75), px = x + 50 + Math.cos(a) * r, py = 48 + Math.sin(a) * r * .7; i ? st.lineTo(px, py) : st.moveTo(px, py); } st.stroke(); }
  st.strokeRect(36, 18, W - 72, 60); st.strokeRect(36, H - 96, W - 72, 48);
  st.globalCompositeOperation = 'lighter';
  const sp = (x0, y0, x1, y1, gx0, gy0, gx1, gy1) => { const gr = st.createLinearGradient(gx0, gy0, gx1, gy1); gr.addColorStop(0, 'rgba(255,170,90,.28)'); gr.addColorStop(1, 'rgba(255,150,70,0)'); st.fillStyle = gr; st.fillRect(x0, y0, x1 - x0, y1 - y0); };
  sp(0, 96, W, 150, 0, 96, 0, 150); sp(0, H - 170, W, H - 110, 0, H - 110, 0, H - 170);
  st.globalCompositeOperation = 'source-over';
}

// ================= SUBTITLES (timed to the voice) =================
const CUES = [
  [0.00, 1.02, 'क्या आपको पता है...'],
  [1.44, 4.00, 'कि समुद्र मंथन से निकला भयंकर विष —'], [4.27, 5.77, 'भगवान शिव ने नहीं पिया था?'],
  [6.35, 7.42, 'कम से कम...'], [7.82, 9.34, 'विष्णु पुराण तो यही कहता है।'],
  [9.98, 11.40, 'जब देवता और दैत्य,'], [11.40, 13.20, 'मंदराचल पर्वत को मथानी'], [13.20, 15.60, 'और नागराज वासुकि को रस्सी बनाकर'],
  [15.60, 17.60, 'क्षीरसागर को मथ रहे थे...'], [17.60, 19.60, 'तब समुद्र से एक-एक करके'], [19.60, 21.21, 'दिव्य रत्न निकले।'],
  [21.79, 22.56, 'कामधेनु...'], [22.82, 23.84, 'पारिजात वृक्ष...'], [24.11, 24.79, 'अप्सराएँ...'],
  [25.07, 26.28, 'और शीतल चंद्रमा,'], [26.63, 29.22, 'जिसे महादेव ने अपने मस्तक पर धारण किया।'],
  [29.77, 31.52, 'और फिर... उठा विष।'], [31.87, 34.18, 'भयंकर... जलता हुआ विष।'],
  [34.73, 36.40, 'अधिकतर कथाओं में हम सुनते हैं'], [36.40, 38.10, 'कि शिव जी ने यह विष पिया,'], [38.10, 39.38, 'और नीलकंठ कहलाए।'],
  [39.82, 41.40, 'पर विष्णु पुराण के पहले अंश'], [41.40, 43.19, 'के नौवें अध्याय में लिखा है —'], [43.58, 45.64, 'इस विष को नागों ने ग्रहण कर लिया।'],
  [46.77, 47.53, 'एक ही कथा...'], [48.03, 50.40, 'अलग-अलग पुराणों में, अलग-अलग रूप।'],
  [50.92, 51.90, 'पूरी कथा देखिए —'], [52.27, 53.84, 'समुद्र मंथन के रहस्य।'], [54.31, 55.40, 'जय श्री हरि।'],
];
const cueAt = t => { for (let i = 0; i < CUES.length; i++) { const [a, b, s] = CUES[i], nx = CUES[i + 1] ? CUES[i + 1][0] : DUR; if (t >= a && t < Math.min(nx, b + .6)) return [s, t - a]; } return null; };
function subtitle(t) {
  const c = cueAt(t); if (!c) return;
  const [text, u] = c, a = ss(u / .15), g = fr;
  g.save(); g.globalAlpha = a; g.font = '700 54px "FreeSerif"';
  const tw = g.measureText(text).width, seal = 52, w = Math.min(1000, 24 + seal + 20 + tw + 36), h = 88, x = W / 2 - w / 2, y = 1488 + (1 - a) * 14;
  g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 20; g.shadowOffsetY = 4;
  const gr = g.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, 'rgba(46,22,14,.94)'); gr.addColorStop(1, 'rgba(22,10,7,.94)');
  g.fillStyle = gr; g.beginPath(); g.roundRect(x, y, w, h, 8); g.fill(); g.shadowColor = 'transparent';
  g.strokeStyle = 'rgba(168,129,63,.85)'; g.lineWidth = 1.6; g.beginPath(); g.roundRect(x + 7, y + 7, w - 14, h - 14, 4); g.stroke();
  const sx = x + 24, sy = y + (h - seal) / 2;
  g.fillStyle = '#b3261b'; g.beginPath(); g.roundRect(sx, sy, seal, seal, 4); g.fill();
  g.fillStyle = '#f6dcc0'; for (const an of [-.9, -.45, 0, .45, .9]) { g.save(); g.translate(sx + seal / 2, sy + seal * .76); g.rotate(an); g.beginPath(); g.ellipse(0, -12, 4.6, 12, 0, 0, 2 * PI); g.fill(); g.restore(); }
  g.fillStyle = '#f3e2bf'; g.textBaseline = 'middle'; g.textAlign = 'left';
  const maxW = w - (seal + 80); g.fillText(text, sx + seal + 20, y + h / 2 + 3, maxW);
  g.restore();
}

// ================= DRAWING =================
let CM = [1, 0, 0, 1, 0, 0];
function spr(p, x, y, o = {}) {
  const { r = 0, s = 1, a = 1, b = 0, sx = 1 } = o; if (a <= .002) return;
  tr.save(); tr.setTransform(...CM); tr.translate(x, y); tr.rotate(r); tr.scale(s * sx, s);
  tr.globalCompositeOperation = 'multiply'; tr.globalAlpha = a; if (b > .4) tr.filter = `blur(${b.toFixed(1)}px)`;
  tr.drawImage(p.c, p.x0, p.y0, p.w, p.h); tr.restore();
}
// press on (large + blurred → sharp) and lift off (grow, blur, fade)
function pr(t, t0, t1 = 1e9, din = .5, dout = .7) {
  if (t < t0 || t > t1 + dout) return null;
  if (t < t0 + din) { const u = eo((t - t0) / din); return { a: u, k: 1 + .22 * (1 - u), b: 12 * (1 - u) }; }
  if (t > t1) { const u = ss((t - t1) / dout); return { a: 1 - u, k: 1 + .28 * u, b: 14 * u }; }
  return { a: 1, k: 1, b: 0 };
}
const trem = (t, k) => [2.2 * Math.sin(t * 1.7 + k * 3.1) + 1.1 * Math.sin(t * 3.3 + k), 1.6 * Math.sin(t * 1.3 + k * 1.7), .012 * Math.sin(t * 1.1 + k * 2.3)];
function put(p, t, t0, t1, x, y, o = {}) {
  const e = pr(t, t0, t1, o.din, o.dout); if (!e) return false;
  const [dx, dy, dr] = o.still ? [0, 0, 0] : trem(t, o.seed ?? x);
  spr(p, x + dx, y + dy, { r: (o.r || 0) + dr, s: (o.s || 1) * e.k, a: e.a * (o.a ?? 1), b: e.b, sx: o.sx || 1 }); return true;
}
// rising from the sea: offset that eases out
const rise = (t, t0, d = .8, h = 220) => h * (1 - eo((t - t0) / d));

const SEA_Y = 1250;
function sea(t) {
  const e = pr(t, 1.2, 1e9, .7); if (!e) return;
  const lift = (1 - eo(seg(t, 1.2, 1.9))) * 220;
  spr(S.seaB, Math.sin(t * .5) * 10, SEA_Y + lift + Math.sin(t * .8) * 3, { a: e.a });
  spr(S.seaF, Math.sin(t * .4 + 1) * -14, SEA_Y + 70 + lift * 1.2 + Math.sin(t * .9 + 2) * 4, { a: e.a });
}
// a deterministic field of rising smoke wisps
function smokeField(t, t0, t1, n, x0, x1, opt = {}) {
  for (let i = 0; i < n; i++) {
    const st_ = t0 + hash(i * 3.3 + (opt.seed || 0)) * (opt.spread ?? 2.5); if (t < st_) continue;
    const life = 4.2, u = ((t - st_) % life) / life;
    if (opt.once && t - st_ > life) continue;
    let x = lerp(x0, x1, hash(i * 7.1 + (opt.seed || 0))) + Math.sin(t * 1.2 + i) * 26, y = SEA_Y + 10 - u * (opt.h ?? 700), s = .7 + u * .9, a = Math.sin(u * PI) * .9;
    if (opt.to) { const k = ss(seg(t, opt.to.t0 + hash(i) * .4, opt.to.t1)); if (k > 0) { const [tx, ty] = opt.to.fn(i); x = lerp(x, tx, k); y = lerp(y, ty, k); s *= 1 - k * .85; } }
    const fade = 1 - ss(seg(t, t1, t1 + .6));
    spr(S.smoke[i % 4], x, y, { r: Math.sin(t * .9 + i) * .25, s, a: a * fade });
  }
}

// ================= LAMPS =================
const fl = (t, k) => 1 + .05 * Math.sin(t * 7.3 + k * 2.1) + .03 * Math.sin(t * 23 + k);
function flare(t, t0, d = .45) { if (t < t0) return 0; const u = (t - t0) / d; return u < 1 ? lerp(.1, 1, eo(u)) + .35 * Math.sin(u * PI) : 1; }
function lamps(t) {
  const L = [];
  const add = (x, y, I, core = .8) => { if (I > .01) L.push([x, y, I, core]); };
  if (t < 10) { add(540, 700, flare(t, .15)); add(540, 1050, .7 * flare(t, 1.44)); }
  else if (t < 21.6) { add(540, 640, 1); add(200, 900, .75 * flare(t, 10.8)); add(880, 900, .75 * flare(t, 10.0)); }
  else if (t < 29.7) { const b = flare(t, 21.6); add(290, 1000, b); add(840, 900, .9 * flare(t, 22.82)); add(560, 950, .8 * flare(t, 24.11)); add(540, 500, 1.1 * flare(t, 25.07)); }
  else if (t < 34.6) { // the poison: lamps snuffed one by one
    const sn = k => 1 - ss(seg(t, 29.8 + k * .4, 30.0 + k * .4));
    add(290, 1000, sn(0)); add(840, 900, sn(1)); add(560, 950, sn(2)); add(540, 700, .85);
  }
  else if (t < 46.75) { add(540, 760, 1); add(540, 1150, .6 * flare(t, 43.58)); }
  else if (t < 50.7) { add(540, 860, 1); add(300, 700, .6 * flare(t, 48.03)); add(780, 1000, .6 * flare(t, 49.22)); }
  else { const away = ss(seg(t, 55.6, 56.9)); add(lerp(540, 1300, away), 700, flare(t, 50.92) * (1 - away)); add(lerp(300, 1100, away), 1060, .7 * flare(t, 54.31) * (1 - away)); add(lerp(780, 1500, away), 1060, .7 * flare(t, 54.31) * (1 - away)); }
  return L.map((l, k) => [l[0], l[1], l[2] * fl(t, k), l[3]]);
}

// ================= CAMERA =================
function camAt(t) {
  let cx = 540, cy = 900, z = 1.12;
  if (t >= 10 && t < 21.6) { const u = ss(seg(t, 12, 21.4)); z = lerp(1.1, 1.18, u); cy = lerp(930, 960, u); }
  for (const h of [31.87, 32.95, 4.27]) if (t >= h && t < h + .5) { const u = (t - h) / .5; z += .1 * (1 - eo(u)); }
  return [cx, cy, z];
}

// ================= THE FILM =================
function scene(t) {
  // —— 1 · hook ——
  put(S.hook, t, .3, 9.75, 540, 430, { din: .55 });
  smokeField(t, 1.6, 6.2, 5, 360, 720, { seed: 1, h: 520 });
  put(S.trishul, t, 4.27, 6.25, 540, 780, { s: .8 });
  put(S.pothiVP, t, 6.35, 9.75, 540, 960);

  // —— 2 · the churning ——
  const churn = ss(seg(t, 15.6, 16.4)) * (1 - ss(seg(t, 21.1, 21.5))), ph = Math.max(0, t - 15.6) * 2.4;
  const pull = churn * Math.sin(ph * PI);    // the rope goes back and forth
  const ROPE_Y = SEA_Y - 240;
  if (t > 9.9 && t < 22.2) {
    put(S.kurma, t, 12.5, 21.4, 540, SEA_Y + 20, { still: true });
    put(S.mountain, t, 12.2, 21.4, 540, SEA_Y + 10, { still: true, r: churn * .02 * Math.sin(ph * PI * .5) });
    const ve = pr(t, 14.0, 21.4);
    if (ve) {
      spr(S.rope, -40 + pull * 14, ROPE_Y, { a: ve.a, b: ve.b, s: 1 });
      spr(S.vhead, 92 + pull * 14, ROPE_Y + 10, { a: ve.a, b: ve.b });
      for (let k = 0; k < 4; k++) { const off = ((ph * 34 + k * 90) % 360); const y = SEA_Y + 10 - 430 + off * .8, edge = Math.sin(off / 360 * PI); spr(S.wrap, 540, y, { a: ve.a * edge, b: ve.b }); }
    }
    for (const [i, x, k] of [[0, 262, 0], [1, 172, 1]]) put(S.daitya[i], t, 10.8 + k * .2, 21.3, x, SEA_Y + 4, { r: -.07 - .05 * pull, seed: 10 + k, s: .86 - k * .07 });
    for (const [i, x, k] of [[0, 818, 0], [1, 908, 1]]) put(S.deva[i], t, 10.0 + k * .2, 21.3, x, SEA_Y + 4, { sx: -1, r: .07 + .05 * pull, seed: 20 + k, s: .86 - k * .07 });
    if (churn > .02) {
      const f = Math.floor(t * 12) % 2;
      spr(S.fire[f], 175 + pull * 14, ROPE_Y - 210, { r: .5, s: .55, a: churn * .95 });
      put(S.cloud, t, 16.5, 21.2, 860, 610);
      if (t > 16.9 && t < 21.3) spr(S.rain[Math.floor(t * 12) % 2], 860, 660, { a: churn * .85 });
    }
  }
  // —— 3 · the treasures ——
  put(S.cow, t, 21.79, 26.35, 290, SEA_Y + 6 + rise(t, 21.79), { s: .9, din: .6 });
  put(S.tree, t, 22.82, 26.4, 850, SEA_Y + 6 + rise(t, 22.82), { s: .82, din: .6 });
  put(S.apsara, t, 24.11, 26.45, 570, SEA_Y + 6 + rise(t, 24.11), { s: .9, din: .6 });
  if (t > 25.07 && t < 30.2) { // the moon rises, then settles on the trident
    const up = eo(seg(t, 25.07, 26.3)), down = ss(seg(t, 27.0, 28.2));
    const y = lerp(lerp(SEA_Y, 470, up), 642, down), e = pr(t, 25.07, 29.45);
    if (e) spr(S.moon, 540, y, { a: e.a, b: e.b, s: (1 - down * .35) * e.k, r: -.3 });
  }
  put(S.trishul, t, 26.63, 29.45, 540, 720, { s: .95 });

  // —— 4 · the poison ——
  smokeField(t, 29.9, 34.5, 16, 120, 960, { seed: 4, spread: 2.2, h: 900 });

  // —— 5 · "most tellings" ——
  put(S.ring, t, 38.1, 39.85, 540, 760, { s: 1.05 });
  put(S.trishul, t, 34.73, 39.82, 540, 720, { s: .95 });
  smokeField(t, 34.6, 39.9, 8, 150, 930, { seed: 5, spread: 1.2, h: 640, to: { t0: 36.4, t1: 39.2, fn: i => [540 + (hash(i) - .5) * 80, 760 + (hash(i * 2) - .5) * 60] } });

  // —— 6 · the Nagas ——
  put(S.pothiVP, t, 39.95, 43.4, 540, 640, { s: .9 });
  const NX = [150, 345, 540, 735, 930];
  smokeField(t, 39.6, 45.7, 10, 200, 880, { seed: 6, spread: 1.6, h: 520, to: { t0: 43.9, t1: 45.5, fn: i => [NX[i % 5], SEA_Y - 300 * .9] } });
  NX.forEach((x, k) => { const t0 = 43.58 + [2, 1, 0, 1, 2][k] * .14; put(S.naga[k % 3], t, t0, 46.55, x, SEA_Y + 12 + rise(t, t0, .7, 260), { s: .9 - Math.abs(k - 2) * .05, sx: k > 2 ? -1 : 1, seed: 30 + k }); });

  // —— 7 · one story, many Puranas ——
  put(S.pothiA, t, 46.8, 50.55, 540, 650, { r: -.06, s: .9 });
  put(S.pothiVP, t, 48.03, 50.6, 540, 860, { r: .03, s: .95 });
  put(S.pothiB, t, 49.22, 50.65, 540, 1070, { r: -.02, s: .9 });

  // —— 8 · end card ——
  put(S.title, t, 50.92, 1e9, 540, 720, { din: .6 });
  put(S.chakra, t, 54.31, 1e9, 300, 1060, { s: 1.2, r: t * .25 });
  put(S.conch, t, 54.45, 1e9, 780, 1060, { s: 1.3 });
}

function render(t) {
  const cam = camAt(t), z = cam[2];
  CM = [z, 0, 0, z, W / 2 - cam[0] * z, H / 2 - cam[1] * z];
  tr.setTransform(1, 0, 0, 1, 0, 0); tr.globalCompositeOperation = 'source-over'; tr.globalAlpha = 1; tr.filter = 'none';
  tr.fillStyle = '#fff'; tr.fillRect(0, 0, W, H);
  sea(t); scene(t);
  fr.setTransform(1, 0, 0, 1, 0, 0); fr.clearRect(0, 0, W, H); fr.drawImage(stc, 0, 0);
  if (new URLSearchParams(location.search).get('thumb')) {
    const g = fr; g.save(); g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round';
    const line = (txt, y, size, col, w) => { g.font = `700 ${size}px "FreeSerif"`; g.strokeStyle = '#2a0d08'; g.lineWidth = w; g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 16; g.strokeText(txt, W / 2, y); g.shadowBlur = 0; g.fillStyle = col; g.fillText(txt, W / 2, y); };
    line('समुद्र मंथन का विष', 270, 106, '#fff4dc', 14);
    line('शिव ने नहीं पिया?', 420, 126, '#ffcf4a', 16);
    line('विष्णु पुराण का रहस्य', 1600, 76, '#fff4dc', 12);
    g.restore();
  } else subtitle(t);
  const L = lamps(t), n = Math.max(.35, L.reduce((a, l) => a + l[2], 0));
  const poison = ss(seg(t, 29.8, 31)) * (1 - ss(seg(t, 34.3, 35.2)));
  const fade = ss(seg(t, 56.2, 57.0)) + (1 - ss(seg(t, 0, .25)));
  GL.render(trc, frc, {
    lamps: L, cam, expo: 1.3 / Math.sqrt(n), sigB: 760, sigC: 150, amb: .28, time: t,
    haze: poison * 3.5, vign: .55 + poison * .25, sat: 1.18, contrast: .17, bloom: .32,
    lcol: [1, lerp(.77, .58, poison), lerp(.46, .32, poison)], fade: clamp(fade), fadeCol: [0, 0, 0], rect: [0, 0, W, H]
  });
}
window.render = render; window.DUR = DUR;
render(0);
window.READY = true;

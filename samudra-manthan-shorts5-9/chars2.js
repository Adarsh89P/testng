// New characters and props for Shorts 5–9 (same shape language as chars.js).
import { S, P, L, E, C, B, X, curve, face, hairBack, crownTall, earring, neck, lotusShapes, PI } from './chars.js';

// —— a goddess / divine woman, standing, facing right; origin at the feet ——
// o: { skin, sari, border, blouse, crown: 'tall' | 'tiara' | 'bun', arms4, hold: 'lotus' | 'kalash' | 'pot' | 'abhaya', pose: 'stand' | 'dance' }
export function goddess(o = {}) {
  const N = [6, -404], k = 1.45, sh = [], skin = o.skin || 'skinF', dance = o.pose === 'dance';
  if (o.arms4) {   // back hands raised, each holding a lotus
    sh.push({ p: B([[-12, -386], [-54, -452], [-62, -508]], 18, 14), c: skin }); sh.push({ p: C(-62, -512, 10), c: skin });
    sh.push(...lotusShapes(-62, -520, .55));
    sh.push({ p: B([[14, -386], [56, -452], [64, -508]], 18, 14), c: skin }); sh.push({ p: C(64, -512, 10), c: skin });
    sh.push(...lotusShapes(64, -520, .55));
  }
  // back arm
  sh.push(dance ? { p: B([[-10, -380], [-62, -360], [-110, -390]], 18, 13), c: skin } : { p: B([[-10, -380], [-40, -320], [-46, -262]], 18, 13), c: skin });
  // flowing pallu behind
  sh.push({ p: B([[-26, -392], [-60, -300], [-76, -180], [-70, -90]], 26, 14), c: o.border || 'gold', pat: { t: 'beads' } });
  // sari skirt, flared
  const sk = dance ? [[-40, -300], [42, -300], [90, -170], [128, -24], [40, 4], [-60, 0], [-104, -30], [-76, -170]] : [[-42, -300], [42, -300], [64, -160], [82, -12], [30, 4], [-24, 0], [-82, -12], [-66, -160]];
  sh.push({ p: P(sk), c: o.sari || 'red', pat: { t: 'lattice', s: 11 } });
  sh.push({ p: B(dance ? [[-104, -26], [10, 2], [126, -22]] : [[-82, -14], [0, 2], [82, -14]], 14, 14, false), c: o.border || 'gold', pat: { t: 'coin' } });
  // torso: bare midriff, blouse, belt, pallu across the chest
  sh.push({ p: S([[-28, -300], [-34, -345], [-28, -392], [0, -406], [26, -394], [34, -345], [28, -300]]), c: skin });
  sh.push({ p: S([[-30, -350], [-30, -392], [0, -406], [26, -394], [30, -352], [0, -344]]), c: o.blouse || 'gold', pat: { t: 'scales' } });
  sh.push({ p: B([[-36, -304], [38, -304]], 12, 12, false), c: 'gold', pat: { t: 'coin' } });
  sh.push({ p: B([[-26, -396], [8, -350], [36, -304]], 20, 20, false), c: o.border || 'gold', pat: { t: 'beads' } });
  sh.push({ beads: curve([[-14, -402], [6, -376], [24, -396]]), r: 3.4, c: 'gold' });
  // front arm and what it holds
  const hold = o.hold || 'none';
  if (dance) { sh.push({ p: B([[16, -386], [54, -440], [70, -500]], 18, 13), c: skin }); sh.push({ p: C(72, -504, 10), c: skin }); }
  else if (hold === 'abhaya') { sh.push({ p: B([[16, -384], [46, -340], [80, -344]], 18, 13), c: skin }); sh.push({ p: S([[74, -360], [92, -364], [96, -340], [80, -330]]), c: skin }); for (let i = 0; i < 6; i++) sh.push({ p: C(86 + (i % 2) * 8, -310 + i * 26, 6), c: 'gold', pat: { t: 'coin' } }); }
  else { sh.push({ p: B([[16, -384], [48, -336], [84, -330]], 18, 13), c: skin }); sh.push({ p: C(88, -330, 10), c: skin }); }
  if (hold === 'lotus') sh.push(...lotusShapes(96, -340, .6));
  if (hold === 'kalash' || hold === 'pot') sh.push(...kalashShapes(100, -330, hold === 'pot' ? .6 : .75, hold === 'kalash'));
  // head
  sh.push(neck(N, k, skin));
  sh.push({ p: X(N, k, S([[-2, -64], [-18, -68], [-32, -58], [-36, -30], [-36, 10], [-30, 44], [-18, 48], [-8, 8], [-10, -10], [-9, -26], [-5, -40], [-6, -56]])), c: 'ink', pat: { t: 'slits', n: 7 } });
  sh.push(...face(N, k, { female: true, skin }));
  sh.push({ p: X(N, k, C(15, -55, 1.6)), c: 'red', ink: 0 });
  sh.push({ p: X(N, k, C(22.5, -25, 2.2)), c: 'gold', ink: 0 });
  sh.push(earring(N, k));
  if (o.crown === 'tall') sh.push(crownTall(N, k, .9));
  else if (o.crown === 'tiara') sh.push({ p: X(N, k, P([[-24, -60], [16, -64], [12, -78], [4, -72], [-2, -86], [-8, -72], [-16, -80]])), c: 'gold', pat: { t: 'lattice', s: 5 } });
  else { sh.push({ p: X(N, k, C(-24, -66, 13)), c: 'ink' }); sh.push({ p: X(N, k, C(-24, -78, 5)), c: 'flowerW', ink: 1 }); sh.push({ p: X(N, k, C(-34, -68, 5)), c: 'flowerW', ink: 1 }); }
  return { body: { box: [-170, -620, 170, 20], shapes: sh } };
}

// the amrit kalash (also a plain pot): origin at its centre
export function kalashShapes(x, y, s = 1, glow = true) {
  const sh = [];
  if (glow) sh.push({ p: E(x, y - 76 * s, 34 * s, 16 * s), c: 'amrit', ink: 0, oil: { maxR: 3 } });
  sh.push({ p: S([[-44, 4], [-40, -30], [-20, -50], [20, -50], [40, -30], [44, 4], [30, 36], [-30, 36]].map(([a, b]) => [x + a * s, y + b * s])), c: 'gold', pat: { t: 'lattice', s: 8 } });
  sh.push({ p: P([[-18, -50], [18, -50], [14, -64], [-14, -64]].map(([a, b]) => [x + a * s, y + b * s])), c: 'gold2' });
  sh.push({ p: E(x, y - 66 * s, 26 * s, 7 * s), c: 'gold2' });
  for (const a of [-.6, 0, .6]) sh.push({ p: E(x + Math.sin(a) * 18 * s, y - 74 * s, 6 * s, 14 * s, a), c: 'leaf', ink: 1 });
  sh.push({ p: B([[x - 40 * s, y - 6 * s], [x + 40 * s, y - 6 * s]], 6 * s, 6 * s, false), c: 'red', ink: 1 });
  return sh;
}
export function kalash() { return { box: [-60, -110, 60, 50], shapes: kalashShapes(0, 0, 1, true) }; }

// —— Dhanvantari: robed in white, golden skin, crown, the amrit kalash held to the chest ——
export function dhanvantari(withKalash = true) {
  const N = [8, -410], k = 1.5, sh = [];
  sh.push({ p: B([[-12, -388], [-46, -320], [-54, -256]], 22, 16), c: 'skinI' }); sh.push({ p: C(-54, -250, 11), c: 'skinI' });
  sh.push({ p: B([[-8, -250], [-30, -130], [-34, -8]], 32, 22), c: 'skinI' }); sh.push({ p: B([[12, -250], [26, -130], [40, -8]], 32, 22), c: 'skinI' });
  for (const x of [-34, 40]) sh.push({ p: S([[x - 14, -12], [x + 24, -12], [x + 28, 4], [x - 16, 6]]), c: 'skinI' });
  sh.push({ p: P([[-46, -300], [46, -300], [56, -210], [64, -100], [36, -90], [8, -98], [-20, -88], [-48, -98], [-64, -104], [-56, -210]]), c: 'white', pat: { t: 'folds' } });
  sh.push({ p: S([[-38, -300], [-44, -350], [-36, -398], [0, -414], [34, -400], [44, -350], [38, -300]]), c: 'skinI', pat: { t: 'ribs' } });
  sh.push({ p: B([[-34, -398], [0, -352], [38, -304]], 26, 26, false), c: 'white', pat: { t: 'folds' } });
  sh.push({ beads: curve([[-20, -404], [2, -370], [26, -396]]), r: 3.6, c: 'gold' });
  sh.push({ p: B([[16, -388], [48, -344], [70, -330]], 22, 16), c: 'skinI' });
  if (withKalash) sh.push(...kalashShapes(84, -318, .8, true)); else sh.push({ p: C(76, -330, 11), c: 'skinI' });
  sh.push(neck(N, k, 'skinI')); sh.push(hairBack(N, k, 'ink', 14));
  sh.push(...face(N, k, { skin: 'skinI' }));
  sh.push({ p: X(N, k, L([[14.2, -62], [14.2, -54]])), c: 'red', line: 2.2 });
  sh.push(crownTall(N, k, .85)); sh.push(earring(N, k));
  return { body: { box: [-130, -640, 170, 20], shapes: sh } };
}

// —— Kamadhenu (Surabhi): white cow, red caparison, gilded horns. Origin on the ground ——
export function kamadhenu() {
  const sh = [];
  for (const x of [-120, -80, 90, 130]) sh.push({ p: B([[x, -110], [x + (x > 0 ? 4 : -4), -6]], 20, 14), c: x === -80 || x === 130 ? 'eleD' : 'ele' });
  for (const x of [-120, -80, 90, 130]) sh.push({ p: E(x + (x > 0 ? 4 : -4), -6, 11, 6), c: 'gold', ink: 1 });
  sh.push({ p: S([[-150, -150], [-120, -196], [-20, -200], [60, -206], [110, -220], [150, -170], [146, -110], [80, -96], [-60, -94], [-150, -110]]), c: 'ele', pat: { t: 'wrinkles' } });
  sh.push({ p: S([[-80, -196], [70, -206], [80, -120], [-70, -112]]), c: 'red', pat: { t: 'lattice', s: 12 } });
  sh.push({ beads: curve([[-76, -114], [0, -110], [76, -122]]), r: 4, c: 'gold' });
  sh.push({ p: S([[96, -214], [116, -244], [140, -230], [146, -200]]), c: 'ele' });
  sh.push({ p: S([[140, -200], [176, -214], [204, -186], [206, -150], [180, -136], [150, -160]]), c: 'ele' });
  sh.push({ p: C(180, -184, 4), c: 'ink', ink: 0 });
  sh.push({ p: B([[168, -212], [158, -250], [186, -258]], 8, 4), c: 'gold' }); sh.push({ p: B([[180, -210], [196, -240], [214, -236]], 8, 4), c: 'gold' });
  sh.push({ p: C(178, -152, 9), c: 'gold', pat: { t: 'coin' } });
  sh.push({ p: L([[-148, -150], [-190, -110], [-176, -40]]), c: 'ink', line: 3 }); sh.push({ p: E(-176, -36, 8, 14), c: 'ink' });
  return { body: { box: [-210, -280, 230, 16], shapes: sh } };
}
export function moon() {
  return { box: [-80, -80, 80, 80], shapes: [{ p: c => { c.moveTo(70, 0); c.arc(0, 0, 70, 0, 2 * PI); c.moveTo(86, -18); c.arc(28, -18, 58, 0, 2 * PI, true); }, c: 'moon', rule: 'evenodd', pat: { t: 'beads' } }] };
}
export function lotusThrone() {
  const sh = [{ p: E(0, 6, 190, 30), c: 'green', pat: { t: 'vein' } }];
  sh.push(...lotusShapes(0, 0, 2.3));
  return { box: [-220, -190, 220, 40], shapes: sh };
}
export function river() {   // the Ganga, falling from the sky
  const pts = [[-40, 0], [10, 160], [-30, 340], [20, 520], [0, 640]];
  return { box: [-120, -20, 120, 660], shapes: [{ p: B(pts, 70, 46), c: 'ganga', pat: { t: 'waves', r: 10 } }, { p: L(pts.map(([x, y]) => [x + 12, y])), c: 'milk', line: 3 }] };
}
export function stream() {   // water poured from a kalash
  return { box: [-30, -10, 60, 300], shapes: [{ p: B([[0, 0], [20, 120], [30, 290]], 22, 10), c: 'ganga', pat: { t: 'slits', n: 3 } }] };
}
export function throne() {
  return { box: [-200, -560, 200, 20], shapes: [
    { p: P([[-12, -560], [12, -560], [10, -380], [-10, -380]]), c: 'gold2' },
    { p: c => { c.moveTo(-170, -500); c.quadraticCurveTo(0, -620, 170, -500); c.lineTo(150, -470); c.quadraticCurveTo(0, -560, -150, -470); c.closePath(); }, c: 'red', pat: { t: 'beads' } },
    { p: S([[-150, -380], [-150, -250], [-110, -60], [110, -60], [150, -250], [150, -380], [0, -420]]), c: 'gold', pat: { t: 'lattice', s: 12 } },
    { p: P([[-180, -60], [180, -60], [160, 0], [-160, 0]]), c: 'gold2', pat: { t: 'coin' } }] };
}
export function naga(v = 0) {
  const sg = v === 1 ? -1 : 1, pts = [[0, 20], [sg * 30, -80], [-sg * 24, -190], [sg * 10, -280], [0, -320]];
  return { box: [-90, -440, 90, 30], shapes: [
    { p: B(pts, 46, 30), c: v === 2 ? 'teal' : 'jade', pat: { t: 'scalesOpen' } },
    { p: S([[-14, -290], [-56, -330], [-62, -380], [-30, -410], [0, -414], [30, -410], [62, -380], [56, -330], [14, -290]]), c: 'green', pat: { t: 'lattice', s: 9 } },
    { p: E(0, -414, 22, 15), c: 'jade' }, { p: C(-9, -416, 3), c: 'ink', ink: 0 }, { p: C(9, -416, 3), c: 'ink', ink: 0 }] };
}
export function pothi(label = '') {
  const sh = [];
  for (const y of [-44, 44]) sh.push({ p: c => c.roundRect(-270, y - 14, 540, 28, 10), c: 'wood', pat: { t: 'beads' } });
  sh.push({ p: c => c.roundRect(-258, -30, 516, 60, 8), c: 'palm', pat: { t: 'leaves' } });
  for (const x of [-170, 170]) sh.push({ p: L([[x, -60], [x + 6, 0], [x, 62]]), c: 'red', line: 3 });
  if (label) sh.push({ text: label, x: 0, y: 2, size: 46, c: 'ink', dark: true });
  return { box: [-280, -80, 280, 80], shapes: sh };
}

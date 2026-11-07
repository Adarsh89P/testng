// Character sheet: every god and character has their own look (iconography), painted in muted, earthy oil palette
import { Ref, paintRef } from './engine/plate.js';
import { P, lin, hash } from './common.js';
export const GW = 560, GH = 600, GX = 280, GY0 = 560;
const mk = () => { const R = new Ref(GW, GH, 1.5), X = GX, Y = GY0;
  const o = pts => pts.map(([x, y]) => [x + X, y + Y]);
  return { R, X, Y,
    poly: (pts, col, g, p = {}) => R.fill(P(o(pts)), col, { dir: 'edge', maxR: 7, group: g, ...p }),
    el: (x, y, rx, ry, col, g, rot = 0, p = {}) => R.fill(c => c.ellipse(x + X, y + Y, rx, ry, rot, 0, 7), col, { dir: 'edge', maxR: 6, group: g, ...p }),
    ln: (pts, w, col, g, p = {}) => R.line(c => pts.forEach(([x, y], i) => i ? c.lineTo(x + X, y + Y) : c.moveTo(x + X, y + Y)), col, w, { dir: 'edge', maxR: 5, group: g, ...p }),
    arc: (x, y, r, a0, a1, w, col, g) => R.line(c => c.arc(x + X, y + Y, r, a0, a1), col, w, { dir: 'edge', maxR: 4, group: g }),
    done: seed => ({ strokes: paintRef(R, { R: [26, 13, 6.5, 3.2, 2], T: 10, seed }), ref: R }) }; };
const eye = (m, x, y) => m.ln([[x, y], [x + 14, y + 1]], 3, '#2a1a2a', 'eye' + x + y);
const crown = (m, x, y, h, w, col) => { m.poly([[x - w, y], [x - w * .7, y - h], [x - w * .2, y - h * .55], [x, y - h * 1.1], [x + w * .2, y - h * .55], [x + w * .7, y - h], [x + w, y]], col, 'cr' + x, { dir: 90 }); };

export function vishnu() {      // blue skin, four arms (conch, discus, mace, lotus), yellow dhoti, tall crown, Kaustubha gem
  const m = mk(), sk = '#4f7bc9';
  m.el(0, 4, 120, 22, '#e8a8b8', 'lotus'); for (let k = -3; k <= 3; k++) m.el(k * 30, -6, 16, 34, k % 2 ? '#f0b8c4' : '#e29aae', 'pt' + k, k * .22);
  m.poly([[-46, -100], [46, -100], [64, -30], [74, -8], [-74, -8], [-64, -30]], '#e3b43a', 'dh', { dir: 80 });
  m.poly([[-44, -102], [44, -102], [38, -250], [-38, -250]], sk, 'tor', { dir: 90 });
  m.poly([[-44, -102], [44, -102], [44, -118], [-44, -118]], '#c8921a', 'belt');
  m.ln([[-34, -244], [-20, -190], [0, -176], [20, -190], [34, -244]], 7, '#f0d870', 'garland');
  m.el(0, -196, 11, 13, '#d83a4a', 'gem');
  m.ln([[-40, -236], [-96, -210], [-120, -280]], 17, sk, 'a1'); m.ln([[40, -236], [96, -210], [120, -280]], 17, sk, 'a2');
  m.ln([[-40, -224], [-98, -160], [-112, -140]], 17, sk, 'a3'); m.ln([[40, -224], [98, -160], [112, -140]], 17, sk, 'a4');
  m.el(-122, -292, 20, 26, '#fff4e0', 'conch', .4); m.arc(122, -300, 26, 0, 6.28, 9, '#e8c040', 'chakra'); for (let k = 0; k < 8; k++) m.ln([[122, -300], [122 + Math.cos(k * .785) * 26, -300 + Math.sin(k * .785) * 26]], 4, '#e8c040', 'sp' + k);
  m.ln([[116, -138], [128, -90]], 10, '#c8921a', 'gada'); m.el(114, -150, 17, 22, '#d8a828', 'gadah');
  m.el(-114, -134, 17, 13, '#e88aa0', 'lot2');
  m.el(0, -278, 28, 32, sk, 'hd'); m.poly([[24, -280], [38, -270], [24, -262]], sk, 'nose'); eye(m, 4, -286);
  m.ln([[-8, -300], [8, -300]], 4, '#e8e0f0', 'tilak');
  crown(m, 0, -300, 90, 30, '#d9a82a'); m.el(0, -350, 7, 7, '#d83a4a', 'cj');
  return m.done(41);
}
export function brahma() {     // four faces (three seen), white beard, Veda, water pot, rosary; on a lotus
  const m = mk(), sk = '#d9894a';
  m.el(0, 6, 130, 20, '#e8c8a8', 'lotus'); for (let k = -3; k <= 3; k++) m.el(k * 32, -6, 17, 34, k % 2 ? '#f3d9bc' : '#ebc29a', 'pt' + k, k * .22);
  m.poly([[-48, -100], [48, -100], [66, -30], [76, -6], [-76, -6], [-66, -30]], '#ecdfc4', 'dh', { dir: 80 });
  m.poly([[-44, -102], [44, -102], [38, -240], [-38, -240]], sk, 'tor', { dir: 90 });
  m.ln([[-30, -236], [30, -140]], 7, '#f4e8d0', 'thread');
  m.ln([[-40, -226], [-92, -200], [-110, -250]], 16, sk, 'a1'); m.ln([[40, -226], [92, -200], [110, -250]], 16, sk, 'a2');
  m.ln([[-40, -212], [-96, -160], [-108, -136]], 16, sk, 'a3'); m.ln([[40, -212], [96, -160], [108, -136]], 16, sk, 'a4');
  m.poly([[-130, -274], [-96, -274], [-96, -240], [-130, -240]], '#c0402a', 'veda'); m.ln([[-122, -266], [-104, -266]], 3, '#f0d890', 'v1');
  m.el(114, -260, 15, 20, '#c88a3a', 'pot'); m.arc(-110, -136, 14, 0, 6.28, 4, '#6a3a1a', 'mala'); m.el(112, -124, 14, 11, '#f0a0b0', 'lot');
  for (const [dx, hr, z] of [[-56, 26, 'l'], [56, 26, 'r']]) { m.el(dx, -274, hr, 32, '#e8a468', 'h' + z); m.ln([[dx - 8, -280], [dx + 8, -280]], 3, '#2a1a2a', 'fe' + z); m.poly([[dx - 18, -256], [dx + 18, -256], [dx, -226]], '#f6f0e4', 'fb' + z); }
  m.el(0, -278, 30, 34, sk, 'hd'); m.poly([[24, -280], [38, -270], [24, -262]], sk, 'nose'); eye(m, 2, -286);
  m.poly([[-24, -262], [24, -262], [14, -214], [0, -196], [-14, -214]], '#f6f0e4', 'beard', { dir: 90 });
  m.poly([[-34, -304], [-30, -352], [0, -332], [30, -352], [34, -304]], '#c8a02a', 'cr');
  return m.done(43);
}
export function parvati() {    // red sari with gold border, crown, lotus, bindi
  const m = mk(), sk = '#e1a07a';
  m.poly([[-48, -110], [48, -110], [66, -34], [80, -4], [-80, -4], [-66, -34]], '#bf3a4a', 'sari', { dir: 80 });
  m.poly([[-80, -12], [80, -12], [80, -4], [-80, -4]], '#e4b43a', 'bord');
  m.poly([[-40, -112], [40, -112], [34, -250], [-34, -250]], '#e4b43a', 'blouse', { dir: 90 });
  m.poly([[-34, -250], [-6, -250], [44, -150], [34, -110]], '#bf3a4a', 'pallu');
  m.ln([[-34, -236], [-84, -200], [-98, -168]], 15, sk, 'a1'); m.ln([[34, -236], [86, -204], [96, -250]], 15, sk, 'a2');
  m.el(98, -262, 16, 12, '#f2a0b8', 'lotus'); m.el(-98, -164, 11, 11, sk, 'hand');
  m.ln([[-24, -246], [-12, -200], [0, -186], [12, -200], [24, -246]], 6, '#f0d870', 'neck');
  m.el(0, -278, 28, 32, sk, 'hd'); m.poly([[24, -280], [36, -270], [24, -262]], sk, 'nose'); eye(m, 2, -286); m.el(18, -294, 3, 3, '#d82a3a', 'bindi');
  m.el(-14, -286, 34, 40, '#2a1a3a', 'hair', .3, { dir: 90 });
  m.el(0, -278, 28, 32, sk, 'hd2'); eye(m, 2, -286);
  crown(m, 0, -304, 62, 24, '#d9a82a');
  return m.done(47);
}
export function ganesha() {    // elephant head, one tusk, big ears, pot belly, modak bowl, mouse
  const m = mk(), sk = '#d98a5a';
  m.poly([[-52, -90], [52, -90], [70, -26], [80, -4], [-80, -4], [-70, -26]], '#c0402a', 'dh', { dir: 80 });
  m.el(0, -150, 70, 76, sk, 'belly'); m.ln([[-50, -170], [50, -170]], 6, '#e8c040', 'belt');
  m.el(0, -240, 40, 42, sk, 'chest');
  m.ln([[-40, -236], [-96, -210], [-108, -250]], 18, sk, 'a1'); m.ln([[40, -236], [96, -216], [112, -178]], 18, sk, 'a2');
  m.ln([[-40, -224], [-100, -176], [-96, -140]], 18, sk, 'a3'); m.ln([[40, -224], [96, -150], [82, -112]], 18, sk, 'a4');
  m.el(86, -100, 24, 12, '#e8c040', 'bowl'); for (const [x, y] of [[76, -112], [88, -116], [98, -110]]) m.el(x, y, 7, 7, '#f0a830', 'mod' + x);
  m.el(-108, -262, 12, 12, '#c0402a', 'axe');
  m.el(-52, -300, 40, 46, '#e8a878', 'earL', .3); m.el(52, -300, 40, 46, '#e8a878', 'earR', -.3);
  m.el(0, -304, 44, 50, sk, 'hd');
  m.ln([[0, -278], [10, -236], [30, -200], [52, -196], [58, -214]], 20, sk, 'trunk');
  m.poly([[-22, -282], [-34, -234], [-14, -258]], '#fff6e4', 'tuskL'); 
  m.el(-14, -312, 5, 5, '#2a1a2a', 'eL'); m.el(16, -312, 5, 5, '#2a1a2a', 'eR');
  crown(m, 0, -344, 52, 28, '#d9a82a'); m.ln([[-10, -328], [10, -328]], 4, '#f0e8d0', 'tilak');
  m.el(-104, -10, 22, 14, '#8a7a72', 'mouse'); m.el(-84, -16, 8, 8, '#8a7a72', 'mh'); m.ln([[-126, -10], [-150, -4]], 3, '#8a7a72', 'tail');
  return m.done(49);
}
export function nandi() {      // Shiva's white bull, garlanded, with a bell
  const m = mk(), wh = '#f0e8d4';
  for (const x of [-110, -76, 84, 118]) { m.poly([[x - 16, -70], [x + 16, -70], [x + 12, -4], [x - 12, -4]], wh, 'leg' + x, { dir: 90 }); m.poly([[x - 13, -14], [x + 13, -14], [x + 12, -4], [x - 12, -4]], '#8a5a3a', 'hf' + x); }
  m.el(0, -140, 150, 72, wh, 'bd', 0, { dir: 0, fallback: 0 }); m.el(86, -208, 54, 50, '#e6dcc4', 'hump');
  m.el(-166, -150, 54, 42, wh, 'hd', .3); m.ln([[-170, -176], [-200, -210], [-196, -236]], 10, '#8a6a4a', 'hornL'); m.ln([[-152, -184], [-150, -226], [-126, -244]], 10, '#8a6a4a', 'hornR');
  m.el(-120, -170, 22, 14, wh, 'ear', -.4); m.el(-194, -136, 14, 12, '#d8a8a0', 'nose'); m.el(-176, -158, 5, 5, '#2a1a2a', 'eye');
  m.ln([[-120, -130], [-100, -90], [-110, -60]], 8, '#d8a82a', 'garl'); m.el(-108, -56, 9, 12, '#e8b830', 'bell');
  m.ln([[150, -150], [180, -110], [176, -60]], 9, wh, 'tail'); m.poly([[-60, -208], [60, -208], [60, -196], [-60, -196]], '#bf3a4a', 'cloth');
  return m.done(53);
}
export function narasimha() {  // lion-faced avatar: golden mane, claws, fierce
  const m = mk(), sk = '#e08a3a';
  m.poly([[-50, -100], [50, -100], [68, -30], [78, -6], [-78, -6], [-68, -30]], '#e8c040', 'dh', { dir: 80 });
  m.poly([[-44, -102], [44, -102], [40, -246], [-40, -246]], sk, 'tor', { dir: 90 });
  m.ln([[-40, -236], [-100, -270], [-124, -320]], 18, sk, 'a1'); m.ln([[40, -236], [100, -270], [124, -320]], 18, sk, 'a2');
  for (const x of [-128, 128]) for (const dx of [-10, 0, 10]) m.poly([[x + dx - 3, -322], [x + dx + 3, -322], [x + dx * 1.6, -350]], '#fff4e0', 'cl' + x + dx);
  m.ln([[-40, -216], [-100, -168], [-118, -142]], 17, sk, 'a3'); m.ln([[40, -216], [100, -168], [118, -142]], 17, sk, 'a4');
  for (let k = 0; k < 18; k++) { const a = k / 18 * Math.PI * 2; m.poly([[Math.cos(a) * 40, -286 + Math.sin(a) * 44], [Math.cos(a + .2) * 80, -286 + Math.sin(a + .2) * 86], [Math.cos(a + .4) * 40, -286 + Math.sin(a + .4) * 44]], k % 2 ? '#d8982a' : '#c8782a', 'ma' + k); }
  m.el(0, -284, 46, 48, '#e8a050', 'face'); m.el(0, -268, 26, 18, '#f0c880', 'muz');
  m.ln([[-24, -300], [-8, -294]], 5, '#2a1a1a', 'bL'); m.ln([[24, -300], [8, -294]], 5, '#2a1a1a', 'bR');
  m.el(-16, -290, 6, 6, '#ffe060', 'eL'); m.el(16, -290, 6, 6, '#ffe060', 'eR'); m.poly([[-6, -276], [6, -276], [0, -262]], '#b04a2a', 'nose');
  m.poly([[-14, -258], [-8, -240], [-4, -258]], '#fff4e0', 'fangL'); m.poly([[14, -258], [8, -240], [4, -258]], '#fff4e0', 'fangR');
  return m.done(59);
}

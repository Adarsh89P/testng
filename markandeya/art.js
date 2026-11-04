// Samudra Manthan: every puppet and set piece, carved in code with the shadow-puppet engine (carve.js)
import { piece, fill, cut, cutLine, ink, within, smooth, poly, cloud, beads, beadLine, coin, lattice, scalesOpen, scales, waves, strata, flameTongue, cutTaper, DYE } from './carve.js';

const ell = (q, x, y, rx, ry, r = 0) => { q.moveTo(x + rx * Math.cos(r), y + rx * Math.sin(r)); q.ellipse(x, y, rx, ry, r, 0, Math.PI * 2); };
const circ = (q, x, y, r) => { q.moveTo(x + r, y); q.arc(x, y, r, 0, Math.PI * 2); };
const limb = (g, pts, w, col) => {
  for (const [ww, c] of [[w + 4, DYE.ink], [w, col]]) {
    g.save(); g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]));
    g.strokeStyle = c; g.lineWidth = ww; g.lineJoin = g.lineCap = 'round'; g.stroke(); g.restore();
  }
};
const FONT = '"Noto Serif Devanagari"';

function figure(kind) {          // a puller of the serpent: deva (open face, blue dhoti, tall crown) or asura (solid red face, horns)
  const d = kind === 'deva';
  const skin = d ? DYE.skin : '#b23a22', c1 = d ? DYE.blue : DYE.green, c2 = d ? DYE.gold : DYE.orange;
  return piece([-70, -310, 150, 12], g => {
    limb(g, [[2, -168], [40, -158], [74, -196]], 12, skin);
    const legs = q => smooth(q, [[-30, -100], [30, -100], [40, -40], [50, 0], [-50, 0], [-40, -40]]);
    fill(g, c1, legs); within(g, legs, () => scalesOpen(g, -60, -96, 60, 4, 7)); ink(g, 2, legs);
    fill(g, c2, q => q.rect(-32, -114, 64, 18)); ink(g, 1.6, q => q.rect(-32, -114, 64, 18));
    const torso = q => poly(q, d ? [[-26, -100], [28, -100], [24, -176], [-22, -176]] : [[-32, -100], [36, -100], [30, -176], [-28, -176]]);
    fill(g, skin, torso); ink(g, 2, torso);
    fill(g, c2, q => poly(q, [[-22, -176], [-6, -176], [28, -122], [18, -112]]));
    beadLine(g, -12, -170, 18, -148, 2.2, 7);
    // head
    fill(g, skin, q => { circ(q, 4, d ? -204 : -206, d ? 24 : 28); });
    fill(g, skin, q => poly(q, [[26, -208], [38, -198], [26, -194]]));
    ink(g, 2, q => circ(q, 4, d ? -204 : -206, d ? 24 : 28));
    cutLine(g, 2.4, q => { q.moveTo(12, -210); q.lineTo(24, -208); });
    cutLine(g, 1.6, q => { q.moveTo(18, -192); q.lineTo(30, -194); });
    if (d) {   // tall gold crown, open-cut
      const cr = q => poly(q, [[-20, -222], [-16, -280], [-2, -246], [6, -292], [16, -248], [28, -278], [30, -222]]);
      fill(g, DYE.gold, cr); ink(g, 2, cr); beads(g, [[-6, -240], [8, -250], [18, -240]], 3); cut(g, q => circ(q, 6, -262, 5));
    } else {   // horns and wild hair
      const hr = q => smooth(q, [[-18, -226], [-34, -262], [-14, -296], [-24, -250], [-6, -228]]);
      fill(g, DYE.hide, hr); ink(g, 2, hr);
      const hr2 = q => smooth(q, [[10, -230], [30, -262], [20, -300], [22, -252], [22, -230]]);
      fill(g, DYE.hide, hr2); ink(g, 2, hr2);
      fill(g, DYE.ink, q => poly(q, [[-24, -210], [-34, -236], [-10, -232], [8, -234], [-6, -226]]));
    }
    limb(g, [[6, -166], [46, -146], [84, -184]], 14, skin);
    fill(g, skin, q => circ(q, 88, -185, 9)); ink(g, 1.6, q => circ(q, 88, -185, 9));
  }, { seed: d ? 3 : 5 });
}

function seaStrip() {
  return piece([-1300, -10, 1300, 300], g => {
    const top = q => { q.moveTo(-1300, 6); for (let x = -1300; x <= 1300; x += 20) q.lineTo(x, 6 + 5 * Math.sin(x / 38)); q.lineTo(1300, 300); q.lineTo(-1300, 300); q.closePath(); };
    fill(g, DYE.teal, top);
    within(g, top, () => { fill(g, DYE.blue, q => q.rect(-1300, 120, 2600, 200)); waves(g, -1300, 30, 1300, 280, 11, 1.8); });
    ink(g, 2.4, q => { q.moveTo(-1300, 6); for (let x = -1300; x <= 1300; x += 20) q.lineTo(x, 6 + 5 * Math.sin(x / 38)); });
  }, { seed: 11 });
}
function shore() {
  return piece([-420, -24, 420, 280], g => {
    const sh = q => smooth(q, [[-420, 0], [-300, -14], [-120, -10], [60, -22], [260, -12], [420, 4], [420, 280], [-420, 280]]);
    fill(g, DYE.brown, sh);
    within(g, sh, () => { strata(g, -420, 420, x => 8 + 4 * Math.sin(x / 50), 8, 26, 3.4); coin(g, -300, 90, 10); coin(g, 120, 140, 9); });
    ink(g, 2.4, sh);
  }, { seed: 17 });
}
function mountain() {
  const out = q => smooth(q, [[-330, 30], [-262, -110], [-180, -240], [-104, -330], [-52, -408], [-6, -432], [44, -424], [104, -334], [186, -236], [264, -108], [330, 30]]);
  return piece([-340, -450, 340, 40], g => {
    fill(g, DYE.orange, out);
    within(g, out, () => {
      fill(g, DYE.green, q => q.rect(-340, -450, 680, 150));
      strata(g, -340, 340, x => -300 + Math.abs(x) * .55, 9, 38, 5);
      for (const [x, y, r] of [[-130, -200, 20], [140, -150, 22], [-30, -90, 18], [60, -250, 17], [-190, -80, 16]]) cloud(g, x, y, r, x, 1.8, x > 0 ? 1 : -1);
      coin(g, 10, -370, 11); coin(g, -60, -330, 9);
    });
    ink(g, 2.6, out);
  }, { seed: 23 });
}
function serpent() {    // Vasuki: scaled body, tail at the left, three-headed hood at the right
  return piece([-780, -70, 840, 70], g => {
    const body = q => { q.moveTo(-770, 0); q.quadraticCurveTo(-500, -36, -200, -22); q.quadraticCurveTo(300, -4, 560, -20); q.lineTo(640, -10); q.lineTo(640, 18); q.quadraticCurveTo(300, 30, -200, 28); q.quadraticCurveTo(-500, 30, -770, 0); q.closePath(); };
    fill(g, DYE.jade, body);
    within(g, body, () => { scalesOpen(g, -780, -40, 640, 40, 8); fill(g, DYE.yellow, q => q.rect(-780, 14, 1420, 6)); });
    ink(g, 2.4, body);
    for (const [dy, s, col] of [[-12, 1, DYE.jade], [0, 1.25, DYE.green], [14, 1, DYE.jade]]) {   // three hoods
      const hd = q => smooth(q, [[600, dy - 10 * s], [650, dy - 46 * s], [708, dy - 40 * s], [748, dy - 6 * s], [708, dy + 28 * s], [650, dy + 36 * s], [600, dy + 14 * s]]);
      fill(g, col, hd); within(g, hd, () => lattice(g, 600, dy - 50 * s, 760, dy + 40 * s, 12, 2.4)); ink(g, 2, hd);
      cut(g, q => circ(q, 726, dy - 8 * s, 4)); cutLine(g, 1.4, q => { q.moveTo(750, dy + 2 * s); q.lineTo(782, dy + 4 * s); });
    }
  }, { seed: 31 });
}
function wrap() {      // coil of the serpent round the mountain
  return piece([-250, -34, 250, 34], g => {
    const b = q => { q.moveTo(-246, -6); q.quadraticCurveTo(0, -42, 246, -6); q.lineTo(246, 14); q.quadraticCurveTo(0, -18, -246, 14); q.closePath(); };
    fill(g, DYE.jade, b); within(g, b, () => scalesOpen(g, -250, -40, 250, 30, 7)); ink(g, 2.2, b);
  }, { seed: 33 });
}
function kurma() {
  return piece([-200, -120, 230, 100], g => {
    fill(g, DYE.gold, q => circ(q, 168, -10, 50)); cut(g, q => circ(q, 168, -10, 36));       // halo ring
    for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; cutLine(g, 2.6, q => { q.moveTo(168, -10); q.lineTo(168 + Math.cos(a) * 36, -10 + Math.sin(a) * 36); }); }
    fill(g, DYE.skin, q => ell(q, -96, 44, 44, 17, .35)); ink(g, 1.8, q => ell(q, -96, 44, 44, 17, .35));
    fill(g, DYE.skin, q => ell(q, 76, 52, 44, 17, -.3)); ink(g, 1.8, q => ell(q, 76, 52, 44, 17, -.3));
    fill(g, DYE.skin, q => poly(q, [[-146, 24], [-196, 38], [-146, 34]]));
    const shell = q => { q.moveTo(-150, 14); q.bezierCurveTo(-150, -86, 150, -86, 150, 14); q.closePath(); };
    fill(g, DYE.green, shell);
    within(g, shell, () => { lattice(g, -150, -90, 150, 14, 26, 3.4); fill(g, DYE.orange, q => q.rect(-150, -6, 300, 22)); scalesOpen(g, -150, -4, 150, 16, 7); });
    ink(g, 2.6, shell);
    const nk = q => poly(q, [[120, -8], [172, -26], [172, 12], [124, 24]]);
    fill(g, DYE.blue, nk); ink(g, 2, nk);
    fill(g, DYE.blue, q => ell(q, 178, -6, 34, 28)); ink(g, 2, q => ell(q, 178, -6, 34, 28));
    fill(g, DYE.gold, q => poly(q, [[160, -26], [166, -62], [178, -38], [190, -64], [196, -28]])); ink(g, 1.8, q => poly(q, [[160, -26], [166, -62], [178, -38], [190, -64], [196, -28]]));
    cutLine(g, 2.4, q => { q.moveTo(184, -12); q.lineTo(198, -10); });
    cutLine(g, 1.6, q => { q.moveTo(188, 8); q.lineTo(202, 6); });
  }, { seed: 41 });
}
function puff() {
  return piece([-220, -200, 220, 200], g => {
    const blob = q => { for (const [x, y, r] of [[0, 0, 150], [-90, 40, 95], [90, 30, 105], [-40, -90, 85], [60, -80, 80], [0, 100, 70]]) circ(q, x, y, r); };
    fill(g, '#47303a', blob, 'nonzero');
    within(g, blob, () => { cloud(g, -50, -20, 38, 0, 3, 1); cloud(g, 70, 20, 30, 2, 3, -1); cloud(g, 0, 90, 22, 1, 2.6, 1); cloud(g, -20, -100, 26, 3, 2.6, -1); });
    ink(g, 3, blob);
  }, { seed: 47, tex: true });
}

function title() {
  const w = 1120, h = 330;
  return piece([-w / 2 - 30, -h / 2 - 30, w / 2 + 30, h / 2 + 30], g => {
    const outer = q => { const r = 24; q.moveTo(-w / 2 + r, -h / 2); q.lineTo(w / 2 - r, -h / 2); q.quadraticCurveTo(w / 2 + 12, -h / 2 - 12, w / 2, -h / 2 + r); q.lineTo(w / 2, h / 2 - r); q.quadraticCurveTo(w / 2 + 12, h / 2 + 12, w / 2 - r, h / 2); q.lineTo(-w / 2 + r, h / 2); q.quadraticCurveTo(-w / 2 - 12, h / 2 + 12, -w / 2, h / 2 - r); q.lineTo(-w / 2, -h / 2 + r); q.quadraticCurveTo(-w / 2 - 12, -h / 2 - 12, -w / 2 + r, -h / 2); q.closePath(); };
    fill(g, '#3a1a10', outer);
    const band = q => { outer(q); q.rect(-w / 2 + 24, -h / 2 + 24, w - 48, h - 48); };
    fill(g, DYE.red, band);
    within(g, band, () => { for (let x = -w / 2 + 30; x < w / 2 - 20; x += 26) { coin(g, x, -h / 2 + 12, 6); coin(g, x, h / 2 - 12, 6); } });
    ink(g, 2.5, outer); ink(g, 1.8, q => q.rect(-w / 2 + 24, -h / 2 + 24, w - 48, h - 48));
    g.save(); g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000'; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
    g.font = `700 150px ${FONT}`; g.fillText('समुद्र मंथन', 0, 30);
    g.font = `600 50px ${FONT}`; g.fillText('समुद्र से निकले रत्न', 0, 108);
    g.restore();
  }, { ss: 2, seed: 51 });
}

function shiva(bowl = true) {      // Shiva with the bowl of poison raised to his lips; trident in the other hand
  const sk = '#ecdcc0';
  return piece([-170, -440, 200, 20], g => {
    // trident staff and prongs (behind)
    ink(g, 5, q => { q.moveTo(-70, -430); q.lineTo(-70, 14); }, DYE.brown);
    const tri = q => poly(q, [[-98, -400], [-92, -440], [-84, -404], [-76, -404], [-70, -452], [-64, -404], [-56, -404], [-48, -440], [-42, -400], [-70, -380]]);
    fill(g, DYE.gold, tri); ink(g, 2, tri);
    // far arm (trident)
    limb(g, [[-8, -290], [-46, -262], [-70, -240]], 15, sk);
    // dhoti: tiger skin
    const legs = q => smooth(q, [[-44, -172], [46, -172], [56, -60], [64, 0], [-64, 0], [-54, -60]]);
    fill(g, DYE.orange, legs);
    within(g, legs, () => { for (let k = 0; k < 9; k++) ink(g, 5, q => { q.moveTo(-60 + k * 14, -170 + (k % 3) * 8); q.lineTo(-44 + k * 14, -80 + (k % 2) * 30); }, '#2a140c'); });
    ink(g, 2.2, legs);
    const torso = q => poly(q, [[-38, -172], [42, -172], [36, -296], [-34, -296]]);
    fill(g, sk, torso); ink(g, 2.2, torso);
    // sacred ash stripes, serpent round the shoulders
    for (const y of [-246, -232, -218]) ink(g, 2.4, q => { q.moveTo(-26, y); q.lineTo(30, y + 4); }, '#4a3a30');
    limb(g, [[-30, -290], [0, -274], [34, -292]], 9, DYE.green);
    fill(g, DYE.green, q => ell(q, -34, -296, 11, 14)); cut(g, q => circ(q, -34, -298, 2.4));
    beadLine(g, -22, -286, 28, -284, 2.4, 8);
    // neck + head
    fill(g, sk, q => q.rect(-6, -322, 24, 32));
    fill(g, sk, q => circ(q, 8, -346, 32)); fill(g, sk, q => poly(q, [[34, -350], [48, -338], [34, -332]]));
    ink(g, 2.2, q => circ(q, 8, -346, 32));
    cutLine(g, 2.6, q => { q.moveTo(18, -352); q.lineTo(34, -350); });          // eye
    cutLine(g, 2, q => { q.moveTo(24, -334); q.lineTo(38, -336); });            // mouth
    cutLine(g, 2.4, q => { q.moveTo(28, -372); q.lineTo(30, -362); });          // third eye
    for (const y of [-376, -368]) ink(g, 2, q => { q.moveTo(0, y); q.lineTo(32, y + 4); }, '#4a3a30');
    // matted hair, crescent moon, flowing river
    const jata = q => smooth(q, [[-34, -330], [-40, -380], [-30, -430], [-6, -454], [22, -440], [40, -404], [38, -374], [12, -388], [-8, -370]]);
    fill(g, DYE.ink, jata); within(g, jata, () => { cloud(g, -16, -410, 16, 0, 2.2, 1); cloud(g, 14, -420, 12, 2, 2.2, -1); cutLine(g, 2, q => { q.moveTo(-30, -350); q.quadraticCurveTo(-20, -390, -14, -430); }); });
    fill(g, DYE.yellow, q => { q.moveTo(30, -442); q.arc(14, -452, 26, -.4, Math.PI * 1.1, true); q.arc(22, -454, 20, Math.PI * 1.05, -.2); q.closePath(); });
    if (bowl) {
      limb(g, [[12, -292], [52, -262], [50, -330]], 15, sk);
      const bw = q => { q.moveTo(26, -346); q.lineTo(70, -346); q.quadraticCurveTo(62, -312, 48, -312); q.quadraticCurveTo(32, -312, 26, -346); q.closePath(); };
      fill(g, DYE.gold, bw); ink(g, 2, bw); cut(g, q => ell(q, 48, -330, 8, 5));
    } else {          // palm raised: abhaya, "fear not"
      limb(g, [[12, -292], [62, -296], [84, -350]], 15, sk);
      fill(g, sk, q => ell(q, 86, -364, 13, 17, .2)); ink(g, 1.8, q => ell(q, 86, -364, 13, 17, .2));
      cutLine(g, 1.6, q => { q.moveTo(86, -372); q.lineTo(86, -356); });
    }
    // rivets
    for (const [x, y] of [[-8, -290], [12, -292]]) { g.beginPath(); g.arc(x, y, 3, 0, 7); g.fillStyle = '#b58a5e'; g.fill(); }
  }, { seed: 61 });
}

// —— the ratnas ——
function cow() {
  return piece([-100, -90, 110, 100], g => {
    const wh = DYE.white;
    for (const x of [-46, -20, 26, 48]) { fill(g, wh, q => q.rect(x - 6, 16, 12, 56)); ink(g, 1.8, q => q.rect(x - 6, 16, 12, 56)); fill(g, DYE.brown, q => q.rect(x - 7, 64, 14, 10)); }
    const body = q => ell(q, 0, 0, 64, 36); fill(g, wh, body); within(g, body, () => lattice(g, -70, -40, 70, 40, 15, 2.6)); ink(g, 2.4, body);
    fill(g, wh, q => ell(q, 62, -30, 24, 17, -.5)); ink(g, 2, q => ell(q, 62, -30, 24, 17, -.5));
    fill(g, DYE.gold, q => poly(q, [[54, -44], [50, -66], [62, -48]])); fill(g, DYE.gold, q => poly(q, [[72, -44], [80, -64], [78, -42]]));
    cutLine(g, 2.2, q => { q.moveTo(66, -36); q.lineTo(74, -34); });
    limb(g, [[-62, -10], [-86, 20], [-80, 54]], 5, DYE.hide2);
    fill(g, DYE.red, q => poly(q, [[-30, -34], [30, -34], [24, -6], [-24, -6]])); beadLine(g, -24, -20, 24, -20, 3, 9);
    fill(g, DYE.gold, q => circ(q, 66, -34, 5)); cut(g, q => circ(q, 66, -34, 2));
  }, { seed: 71 });
}
function horse() {
  return piece([-100, -110, 110, 100], g => {
    const wh = DYE.white;
    for (const x of [-48, -28, 22, 42]) { fill(g, wh, q => poly(q, [[x - 7, 14], [x + 7, 14], [x + 4, 74], [x - 6, 74]])); ink(g, 1.8, q => poly(q, [[x - 7, 14], [x + 7, 14], [x + 4, 74], [x - 6, 74]])); }
    const body = q => ell(q, -4, 0, 58, 28); fill(g, wh, body); within(g, body, () => lattice(g, -70, -30, 70, 30, 14, 2.4)); ink(g, 2.4, body);
    const neck = q => poly(q, [[24, -14], [50, -80], [74, -76], [52, 6]]); fill(g, wh, neck); ink(g, 2, neck);
    fill(g, wh, q => ell(q, 78, -70, 24, 11, .55)); ink(g, 2, q => ell(q, 78, -70, 24, 11, .55));
    cutLine(g, 2.2, q => { q.moveTo(76, -80); q.lineTo(84, -76); });
    for (let k = 0; k < 5; k++) { const bx = 30 + k * 5, by = -20 - k * 15; fill(g, DYE.gold, q => poly(q, [[bx, by], [bx - 20, by - 6], [bx - 6, by - 20]])); }
    fill(g, DYE.gold, q => { q.moveTo(-58, -6); q.bezierCurveTo(-96, -20, -100, 30, -84, 62); q.bezierCurveTo(-80, 20, -66, 8, -58, 6); q.closePath(); }); ink(g, 1.8, q => { q.moveTo(-58, -6); q.bezierCurveTo(-96, -20, -100, 30, -84, 62); });
    fill(g, DYE.red, q => poly(q, [[-22, -26], [26, -26], [20, -2], [-18, -2]])); beadLine(g, -16, -14, 18, -14, 2.6, 8);
  }, { seed: 73 });
}
function elephant() {
  return piece([-110, -100, 130, 110], g => {
    const gr = DYE.hide;
    for (const x of [-52, -22, 22, 50]) { fill(g, gr, q => q.rect(x - 11, 20, 22, 64)); ink(g, 1.8, q => q.rect(x - 11, 20, 22, 64)); }
    const body = q => ell(q, -6, 0, 66, 46); fill(g, gr, body); ink(g, 2.4, body);
    fill(g, DYE.red, q => poly(q, [[-40, -44], [36, -44], [30, 10], [-34, 10]])); within(g, q => poly(q, [[-40, -44], [36, -44], [30, 10], [-34, 10]]), () => { coin(g, -16, -22, 8); coin(g, 14, -22, 8); coin(g, 0, -4, 7); });
    ink(g, 2, q => poly(q, [[-40, -44], [36, -44], [30, 10], [-34, 10]]));
    const head = q => ell(q, 56, -14, 34, 38); fill(g, gr, head); ink(g, 2.4, head);
    const ear = q => ell(q, 38, -12, 24, 34, .15); fill(g, DYE.hide2, ear); within(g, ear, () => cloud(g, 38, -12, 18, 0, 2.4, 1)); ink(g, 2, ear);
    limb(g, [[80, 4], [100, 40], [92, 74], [78, 78]], 18, gr);
    fill(g, DYE.white, q => poly(q, [[70, 8], [104, 22], [112, 36], [96, 24], [68, 18]])); ink(g, 1.6, q => poly(q, [[70, 8], [104, 22], [112, 36], [96, 24], [68, 18]]));
    cutLine(g, 2.2, q => { q.moveTo(70, -26); q.lineTo(80, -24); });
    fill(g, DYE.gold, q => poly(q, [[44, -48], [68, -50], [72, -34], [48, -30]])); beads(g, [[54, -42], [64, -40]], 2.4);
  }, { seed: 79 });
}
function gem() {
  return piece([-110, -110, 110, 110], g => {
    for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; cutTaper(g, [[Math.cos(a) * 66, Math.sin(a) * 66], [Math.cos(a) * 94, Math.sin(a) * 94]], 8); }
    const outer = q => poly(q, [[-48, -8], [-30, -42], [30, -42], [48, -8], [0, 56]]);
    fill(g, DYE.red, outer);
    within(g, outer, () => { cutLine(g, 2.2, q => { q.moveTo(-48, -8); q.lineTo(48, -8); }); cutLine(g, 2, q => { q.moveTo(-30, -42); q.lineTo(-12, -8); q.lineTo(0, 56); }); cutLine(g, 2, q => { q.moveTo(30, -42); q.lineTo(12, -8); q.lineTo(0, 56); }); cut(g, q => circ(q, 0, -22, 8)); });
    ink(g, 2.6, outer);
  }, { seed: 83 });
}
function tree() {
  return piece([-110, -130, 110, 100], g => {
    const tk = q => poly(q, [[-10, 70], [-6, -20], [6, -20], [12, 70], [30, 82], [-30, 82]]); fill(g, DYE.brown, tk); ink(g, 2, tk);
    const can = q => { circ(q, 0, -62, 54); circ(q, -50, -30, 40); circ(q, 50, -30, 40); circ(q, -20, -96, 34); circ(q, 28, -92, 32); };
    fill(g, DYE.jade, can, 'nonzero');
    within(g, can, () => { for (let k = 0; k < 26; k++) { const a = k * 2.4, r = 20 + (k % 5) * 14; cut(g, q => ell(q, Math.cos(a) * r, -60 + Math.sin(a) * r * .8, 7, 3.5, a)); } });
    ink(g, 2.4, can);
    for (const [x, y] of [[-40, -22], [36, -50], [4, -84], [-22, -64]]) { fill(g, DYE.orange, q => circ(q, x, y, 9)); coin(g, x, y, 5); }
  }, { seed: 89 });
}
function apsara() {   // Rambha, dancing
  return piece([-100, -130, 100, 110], g => {
    limb(g, [[-8, -52], [-48, -86], [-34, -122]], 8, DYE.skin); limb(g, [[8, -52], [50, -80], [40, -118]], 8, DYE.skin);
    const skirt = q => smooth(q, [[-18, -14], [18, -14], [60, 70], [30, 82], [0, 74], [-30, 82], [-60, 70]]);
    fill(g, DYE.crim, skirt); within(g, skirt, () => { scalesOpen(g, -64, -12, 64, 86, 8); fill(g, DYE.gold, q => q.rect(-64, 60, 128, 8)); }); ink(g, 2, skirt);
    const tor = q => poly(q, [[-16, -60], [16, -60], [14, -12], [-14, -12]]); fill(g, DYE.gold, tor); ink(g, 2, tor);
    fill(g, DYE.skin, q => circ(q, 2, -78, 17)); ink(g, 2, q => circ(q, 2, -78, 17)); fill(g, DYE.skin, q => poly(q, [[16, -80], [26, -73], [16, -70]]));
    cutLine(g, 2, q => { q.moveTo(8, -82); q.lineTo(16, -81); });
    const cr = q => poly(q, [[-14, -92], [-10, -118], [0, -100], [8, -122], [16, -96]]); fill(g, DYE.gold, cr); ink(g, 1.6, cr);
    limb(g, [[-14, 56], [-52, 100]], 9, DYE.skin);
    fill(g, DYE.green, q => poly(q, [[-60, -126], [-30, -118], [-34, -100], [-60, -110]]));
  }, { seed: 91 });
}
function lakshmi() {
  return piece([-110, -120, 110, 110], g => {
    fill(g, DYE.gold, q => circ(q, 0, -34, 62)); cut(g, q => circ(q, 0, -34, 50));
    for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; cutTaper(g, [[Math.cos(a) * 52, -34 + Math.sin(a) * 52], [Math.cos(a) * 80, -34 + Math.sin(a) * 80]], 6); }
    for (let k = -2; k <= 2; k++) { const p = q => ell(q, k * 28, 62 - Math.abs(k) * 6, 17, 38, k * .38); fill(g, DYE.crim, p); within(g, p, () => cutLine(g, 1.6, q => { q.moveTo(k * 28, 30); q.lineTo(k * 28, 90); })); ink(g, 2, p); }
    const bd = q => poly(q, [[-24, 38], [24, 38], [18, -26], [-18, -26]]); fill(g, DYE.red, bd); within(g, bd, () => lattice(g, -26, -26, 26, 40, 11, 2)); ink(g, 2, bd);
    fill(g, DYE.skin, q => circ(q, 0, -44, 20)); ink(g, 2, q => circ(q, 0, -44, 20)); fill(g, DYE.skin, q => poly(q, [[16, -46], [27, -38], [16, -34]]));
    cutLine(g, 2.2, q => { q.moveTo(6, -50); q.lineTo(15, -48); });
    const cr = q => poly(q, [[-16, -60], [-12, -88], [0, -68], [10, -92], [18, -62]]); fill(g, DYE.gold, cr); ink(g, 1.6, cr);
    limb(g, [[-14, -14], [-46, 6], [-48, -22]], 8, DYE.skin); fill(g, DYE.crim, q => circ(q, -48, -28, 9)); coin(g, -48, -28, 5);
    limb(g, [[14, -14], [44, 6], [50, -14]], 8, DYE.skin);
  }, { seed: 97 });
}
function varuni() {
  return piece([-90, -110, 90, 110], g => {
    const jar = q => { q.moveTo(-18, -80); q.lineTo(18, -80); q.lineTo(20, -54); q.bezierCurveTo(70, -34, 70, 70, 30, 86); q.lineTo(-30, 86); q.bezierCurveTo(-70, 70, -70, -34, -20, -54); q.closePath(); };
    fill(g, DYE.teal, jar); within(g, jar, () => { fill(g, DYE.gold, q => q.rect(-80, -34, 160, 12)); cloud(g, 0, 20, 30, 0, 3, 1); beadLine(g, -52, 62, 52, 62, 2.6, 10); }); ink(g, 2.6, jar);
    fill(g, DYE.gold, q => q.rect(-24, -92, 48, 14)); ink(g, 2, q => q.rect(-24, -92, 48, 14));
    for (const [x, y] of [[-48, -50], [54, -62], [40, -96]]) { fill(g, DYE.red, q => circ(q, x, y, 8)); cut(g, q => circ(q, x, y, 3)); }
  }, { seed: 101 });
}
function chandra() {
  return piece([-100, -100, 100, 100], g => {
    for (let k = 0; k < 10; k++) { const a = k * Math.PI / 5 + .3; cutTaper(g, [[Math.cos(a) * 72, Math.sin(a) * 72], [Math.cos(a) * 96, Math.sin(a) * 96]], 7); }
    const cres = q => { q.moveTo(20, -66); q.arc(0, 0, 66, -1.25, 1.25, false); q.arc(26, 0, 54, 1.0, -1.0, true); q.closePath(); };
    fill(g, DYE.yellow, cres); within(g, cres, () => { beads(g, [[-30, -10], [-44, 20], [-20, 40], [-40, -34]], 3.4); cloud(g, -32, 6, 16, 0, 2.2, 1); }); ink(g, 2.6, cres);
    for (const [x, y] of [[44, -50], [60, 20], [34, 60]]) { fill(g, DYE.white, q => circ(q, x, y, 5)); cut(g, q => circ(q, x, y, 2)); }
  }, { seed: 103 });
}
function conch() {
  return piece([-110, -90, 110, 90], g => {
    const sh = q => smooth(q, [[-96, -6], [-50, -52], [10, -62], [62, -34], [74, 14], [40, 50], [-20, 54], [-60, 30]]);
    fill(g, DYE.hide, sh);
    within(g, sh, () => { for (let k = 0; k < 6; k++) cutLine(g, 2.4, q => { q.arc(30 - k * 14, 0, 62 - k * 10, -1.9, 1.9); }); fill(g, DYE.orange, q => ell(q, 70, 6, 18, 36)); });
    ink(g, 2.6, sh); ink(g, 1.8, q => ell(q, 70, 6, 18, 36));
    for (let k = 0; k < 7; k++) { const a = -1.2 + k * .4; fill(g, DYE.hide, q => poly(q, [[Math.cos(a) * 62 + 2, Math.sin(a) * 58 - 2], [Math.cos(a) * 82 + 4, Math.sin(a) * 78 - 4], [Math.cos(a + .1) * 62 + 2, Math.sin(a + .1) * 58 - 2]])); }
  }, { seed: 107 });
}
function dhanvantari() {
  return piece([-120, -350, 120, 14], g => {
    limb(g, [[-12, -250], [-64, -262], [-56, -318]], 13, DYE.skin);
    limb(g, [[12, -250], [64, -262], [56, -318]], 13, DYE.skin);
    const dh = q => smooth(q, [[-34, -104], [34, -104], [46, -36], [56, 0], [-56, 0], [-46, -36]]);
    fill(g, DYE.white, dh); within(g, dh, () => { scalesOpen(g, -60, -100, 60, 4, 7); fill(g, DYE.gold, q => q.rect(-60, -110, 120, 14)); }); ink(g, 2, dh);
    const torso = q => poly(q, [[-30, -104], [30, -104], [28, -250], [-28, -250]]); fill(g, DYE.skin, torso); ink(g, 2.2, torso);
    beadLine(g, -22, -240, 22, -210, 2.6, 8);
    fill(g, DYE.crim, q => poly(q, [[-28, -250], [-10, -250], [26, -170], [16, -160]]));
    fill(g, DYE.skin, q => circ(q, 0, -276, 24)); ink(g, 2, q => circ(q, 0, -276, 24));
    cutLine(g, 2.4, q => { q.moveTo(-12, -282); q.lineTo(-2, -280); }); cutLine(g, 2.4, q => { q.moveTo(6, -282); q.lineTo(16, -280); });
    cutLine(g, 1.8, q => { q.moveTo(-8, -262); q.lineTo(8, -262); });
    const cr = q => poly(q, [[-22, -294], [-18, -332], [-4, -304], [0, -338], [4, -304], [18, -332], [22, -294]]); fill(g, DYE.gold, cr); ink(g, 2, cr); beads(g, [[0, -318]], 3);
    fill(g, DYE.green, q => poly(q, [[60, -318], [92, -306], [88, -288], [60, -300]]));
    fill(g, DYE.skin, q => circ(q, -56, -320, 8)); fill(g, DYE.skin, q => circ(q, 56, -320, 8));
  }, { seed: 109 });
}
function kalash() {
  return piece([-70, -90, 70, 80], g => {
    const pot = q => { q.moveTo(-20, -52); q.lineTo(20, -52); q.lineTo(24, -30); q.bezierCurveTo(70, -14, 66, 60, 26, 70); q.lineTo(-26, 70); q.bezierCurveTo(-66, 60, -70, -14, -24, -30); q.closePath(); };
    fill(g, DYE.gold, pot);
    within(g, pot, () => { cut(g, q => ell(q, 0, 16, 16, 22)); fill(g, DYE.crim, q => q.rect(-70, -20, 140, 10)); beadLine(g, -46, 52, 46, 52, 2.4, 9); });
    ink(g, 2.6, pot);
    fill(g, DYE.gold, q => ell(q, 0, -58, 26, 10)); ink(g, 2, q => ell(q, 0, -58, 26, 10)); cut(g, q => ell(q, 0, -58, 18, 5));
    for (let k = 0; k < 9; k++) { const a = -Math.PI * .85 + k * Math.PI * .85 / 4; cutTaper(g, [[Math.cos(a) * 36, -58 + Math.sin(a) * 36], [Math.cos(a) * 70, -58 + Math.sin(a) * 60]], 8); }
  }, { seed: 113 });
}
function spot() { return piece([-20, -20, 20, 20], g => { fill(g, '#1d3f9a', q => circ(q, 0, 0, 14)); }, { tex: false }); }


function boy(hug) {
  return piece([-70, -176, 110, 12], g => {
    const sk = DYE.skin;
    const dh = q => smooth(q, [[-20, -62], [20, -62], [28, -20], [32, 0], [-32, 0], [-28, -20]]);
    fill(g, DYE.white, dh); within(g, dh, () => fill(g, DYE.orange, q => q.rect(-40, -66, 80, 9))); ink(g, 1.8, dh);
    const to = q => poly(q, [[-16, -62], [18, -62], [14, -112], [-14, -112]]); fill(g, sk, to); ink(g, 1.8, to);
    ink(g, 2, q => { q.moveTo(-12, -110); q.lineTo(14, -70); }, DYE.brown);
    fill(g, sk, q => circ(q, 2, -134, 19)); ink(g, 1.8, q => circ(q, 2, -134, 19)); fill(g, sk, q => poly(q, [[19, -136], [28, -129], [19, -126]]));
    cutLine(g, 2, q => { q.moveTo(8, -139); q.lineTo(17, -138); });
    fill(g, DYE.ink, q => circ(q, -8, -158, 9)); for (const y of [-148, -144]) ink(g, 1.5, q => { q.moveTo(-2, y); q.lineTo(14, y + 1); }, '#4a3a30');
    if (hug) { limb(g, [[2, -106], [40, -100], [76, -88]], 11, sk); limb(g, [[6, -98], [44, -90], [80, -76]], 11, sk); }
    else { limb(g, [[0, -106], [18, -90], [30, -114]], 10, sk); limb(g, [[4, -104], [20, -88], [32, -112]], 10, sk); fill(g, sk, q => circ(q, 32, -114, 8)); }
  }, { seed: 121 });
}
function linga() {
  return piece([-150, -270, 190, 34], g => {
    const yoni = q => smooth(q, [[-118, 4], [-80, -22], [80, -22], [118, 4], [182, 8], [118, 28], [-118, 28]]);
    fill(g, DYE.crim, yoni); within(g, yoni, () => beadLine(g, -100, 10, 160, 14, 3, 12)); ink(g, 2.4, yoni);
    const cyl = q => { q.moveTo(-54, -18); q.lineTo(-54, -170); q.bezierCurveTo(-54, -262, 54, -262, 54, -170); q.lineTo(54, -18); q.closePath(); };
    fill(g, DYE.hide2, cyl);
    within(g, cyl, () => { cut(g, q => ell(q, 0, -120, 16, 26)); for (const y of [-196, -176, -156]) ink(g, 3.2, q => { q.moveTo(-54, y); q.quadraticCurveTo(0, y + 16, 54, y); }, '#3a2414'); });
    ink(g, 2.6, cyl);
    for (let k = 0; k < 9; k++) { const x = -54 + k * 13.5, y = -60 + 22 * Math.sin(Math.PI * k / 8); fill(g, DYE.red, q => circ(q, x, y, 6)); cut(g, q => circ(q, x, y, 2)); }
    fill(g, DYE.green, q => poly(q, [[0, -252], [-14, -272], [0, -262], [14, -272]])); ink(g, 1.6, q => poly(q, [[0, -252], [-14, -272], [0, -262], [14, -272]]));
  }, { seed: 127 });
}
function yama() {      // Yama on his buffalo, facing left, noose hand raised, mace in the other
  const dark = '#43312b';
  return piece([-250, -380, 260, 40], g => {
    for (const x of [-96, -62, 62, 96]) { fill(g, dark, q => poly(q, [[x - 14, -60], [x + 14, -60], [x + 10, 6], [x - 10, 6]])); ink(g, 2, q => poly(q, [[x - 14, -60], [x + 14, -60], [x + 10, 6], [x - 10, 6]])); }
    const bd = q => ell(q, 0, -112, 134, 64); fill(g, dark, bd); within(g, bd, () => lattice(g, -140, -180, 140, -50, 16, 3)); ink(g, 2.6, bd);
    const hd = q => ell(q, -150, -92, 54, 38, .35); fill(g, dark, hd); ink(g, 2.4, hd);
    for (const dx of [0, 18]) { const hn = q => smooth(q, [[-170 + dx, -112], [-216 + dx, -150], [-206 + dx, -204], [-184 + dx, -150], [-158 + dx, -118]]); fill(g, DYE.hide, hn); ink(g, 2, hn); }
    cutLine(g, 2.6, q => { q.moveTo(-176, -102); q.lineTo(-158, -96); });
    limb(g, [[134, -124], [176, -92], [190, -40]], 9, dark);
    const tor = q => poly(q, [[-24, -170], [34, -170], [26, -270], [-20, -270]]); fill(g, DYE.green, tor); within(g, tor, () => beadLine(g, -16, -250, 24, -200, 2.6, 8)); ink(g, 2.2, tor);
    fill(g, DYE.red, q => poly(q, [[-30, -158], [40, -158], [48, -112], [-38, -112]])); ink(g, 2, q => poly(q, [[-30, -158], [40, -158], [48, -112], [-38, -112]]));
    fill(g, DYE.green, q => circ(q, 6, -296, 30)); fill(g, DYE.green, q => poly(q, [[-22, -300], [-40, -290], [-22, -280]])); ink(g, 2.2, q => circ(q, 6, -296, 30));
    cutLine(g, 3, q => { q.moveTo(-14, -308); q.lineTo(-30, -302); }); cutLine(g, 3, q => { q.moveTo(6, -308); q.lineTo(-8, -304); });
    ink(g, 2.6, q => { q.moveTo(-22, -286); q.quadraticCurveTo(-34, -280, -44, -290); }, DYE.ink);
    const cr = q => poly(q, [[-24, -320], [-30, -378], [-8, -340], [6, -388], [20, -340], [40, -376], [38, -320]]); fill(g, DYE.gold, cr); ink(g, 2, cr); cut(g, q => circ(q, 6, -352, 5));
    limb(g, [[20, -258], [-30, -286], [-62, -352]], 14, DYE.green); fill(g, DYE.green, q => circ(q, -64, -358, 10));
    limb(g, [[28, -250], [70, -214], [80, -196]], 14, DYE.green);
    ink(g, 5, q => { q.moveTo(82, -196); q.lineTo(88, -330); }, DYE.brown);
    fill(g, DYE.gold, q => circ(q, 88, -340, 22)); cut(g, q => circ(q, 88, -340, 8)); ink(g, 2, q => circ(q, 88, -340, 22));
  }, { seed: 131 });
}
function noose() {
  return piece([-100, -80, 100, 80], g => {
    const ring = (w, col) => { g.save(); g.beginPath(); g.ellipse(0, 0, 60, 46, 0, 0, Math.PI * 2); g.strokeStyle = col; g.lineWidth = w; g.stroke(); g.restore(); };
    ring(16, DYE.ink); ring(11, DYE.brown);
    for (let k = 0; k < 24; k++) { const a = k * Math.PI / 12; cutLine(g, 1.4, q => { q.moveTo(Math.cos(a) * 54, Math.sin(a) * 41); q.lineTo(Math.cos(a + .18) * 66, Math.sin(a + .18) * 51); }); }
    fill(g, DYE.brown, q => poly(q, [[54, -10], [92, -30], [96, -18], [60, 4]])); ink(g, 2, q => poly(q, [[54, -10], [92, -30], [96, -18], [60, 4]]));
  }, { seed: 137 });
}
function hut() {
  return piece([-180, -230, 180, 12], g => {
    const roof = q => poly(q, [[-170, -118], [0, -226], [170, -118]]); fill(g, DYE.gold, roof); within(g, roof, () => { for (let y = -214; y < -118; y += 14) cutLine(g, 2.2, q => { q.moveTo(-190, y + 60); q.lineTo(190, y + 60); }); }); ink(g, 2.6, roof);
    const wall = q => q.rect(-120, -118, 240, 118); fill(g, DYE.hide2, wall); within(g, wall, () => { cut(g, q => { q.rect(-26, -92, 52, 92); }); lattice(g, 40, -110, 116, -50, 12, 2.4); }); ink(g, 2.6, wall);
    fill(g, DYE.green, q => circ(q, 150, -80, 0.1));
  }, { seed: 139 });
}
function hourglass() {
  return piece([-60, -100, 60, 100], g => {
    for (const y of [-88, 80]) { fill(g, DYE.gold, q => q.rect(-46, y, 92, 14)); ink(g, 2, q => q.rect(-46, y, 92, 14)); }
    const gl = q => { q.moveTo(-38, -74); q.lineTo(38, -74); q.lineTo(5, 0); q.lineTo(38, 80); q.lineTo(-38, 80); q.lineTo(-5, 0); q.closePath(); };
    fill(g, DYE.teal, gl); within(g, gl, () => { fill(g, DYE.orange, q => poly(q, [[-30, -66], [30, -66], [4, -4], [-4, -4]])); fill(g, DYE.orange, q => poly(q, [[-28, 76], [28, 76], [8, 36], [-8, 36]])); cut(g, q => q.rect(-1.5, -4, 3, 40)); }); ink(g, 2.4, gl);
  }, { seed: 141 });
}
function plaque(w, h, lines) {
  return piece([-w / 2 - 30, -h / 2 - 30, w / 2 + 30, h / 2 + 30], g => {
    const outer = q => { const r = 24; q.moveTo(-w / 2 + r, -h / 2); q.lineTo(w / 2 - r, -h / 2); q.quadraticCurveTo(w / 2 + 12, -h / 2 - 12, w / 2, -h / 2 + r); q.lineTo(w / 2, h / 2 - r); q.quadraticCurveTo(w / 2 + 12, h / 2 + 12, w / 2 - r, h / 2); q.lineTo(-w / 2 + r, h / 2); q.quadraticCurveTo(-w / 2 - 12, h / 2 + 12, -w / 2, h / 2 - r); q.lineTo(-w / 2, -h / 2 + r); q.quadraticCurveTo(-w / 2 - 12, -h / 2 - 12, -w / 2 + r, -h / 2); q.closePath(); };
    fill(g, '#3a1a10', outer);
    const band = q => { outer(q); q.rect(-w / 2 + 24, -h / 2 + 24, w - 48, h - 48); };
    fill(g, DYE.red, band);
    within(g, band, () => { for (let x = -w / 2 + 30; x < w / 2 - 20; x += 26) { coin(g, x, -h / 2 + 12, 6); coin(g, x, h / 2 - 12, 6); } });
    ink(g, 2.5, outer); ink(g, 1.8, q => q.rect(-w / 2 + 24, -h / 2 + 24, w - 48, h - 48));
    g.save(); g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000'; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
    for (const L of lines) { g.font = L.font; g.fillText(L.text, 0, L.y); }
    g.restore();
  }, { ss: 2, seed: 143 });
}
function aura() {
  return piece([-300, -300, 300, 300], g => {
    for (let k = 0; k < 28; k++) { g.save(); g.translate(0, 0); g.rotate(k * Math.PI * 2 / 28); g.translate(0, -214); fill(g, k % 2 ? DYE.orange : DYE.yellow, q => flameTongue(q, 64, 34, k % 2 ? 1 : -1)); ink(g, 1.8, q => flameTongue(q, 64, 34, k % 2 ? 1 : -1)); g.restore(); }
    const ring = q => { circ(q, 0, 0, 226); circ(q, 0, 0, 190); };
    fill(g, DYE.gold, ring); within(g, ring, () => { for (let k = 0; k < 36; k++) { const a = k * Math.PI / 18; cut(g, q => circ(q, Math.cos(a) * 208, Math.sin(a) * 208, 6)); } });
    ink(g, 2.4, q => circ(q, 0, 0, 226)); ink(g, 2.4, q => circ(q, 0, 0, 190));
  }, { seed: 149 });
}

export function buildArt() {
  const F = '"Noto Serif Devanagari"';
  return {
    asura: figure('asura'), shore: shore(), shiva: shiva(false), boyHug: boy(true), boyPray: boy(false), linga: linga(), yama: yama(), noose: noose(),
    hut: hut(), hourglass: hourglass(), aura: aura(), tree: null,
    num: plaque(560, 330, [{ text: '१६', font: `700 190px ${F}`, y: 40 }, { text: 'वर्ष', font: `600 64px ${F}`, y: 118 }]),
    kal: plaque(900, 250, [{ text: 'कालांतक', font: `700 150px ${F}`, y: 50 }, { text: 'काल का अंत करने वाले', font: `600 44px ${F}`, y: 104 }]),
    end: plaque(1080, 330, [{ text: 'मार्कंडेय', font: `700 160px ${F}`, y: 30 }, { text: 'अटूट भक्ति की कथा', font: `600 52px ${F}`, y: 108 }])
  };
}

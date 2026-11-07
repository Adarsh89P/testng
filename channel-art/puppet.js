// Shadow Puppetry renderer: every shape of chars.js becomes dyed, carved hide on a lamp-lit cloth.
import { makeGL } from './gl.js';
import { canvas, piece, fill, cut, cutLine, ink, within, scalesOpen, scales, lattice, coin, cloud, beads, beadLine, plum, waves, meander, cutTaper, strata, DYE } from './carve.js';
import * as CH from './chars.js';
import { W, H, DUR, frame, mul, T, Sc, R, lerp, seg, ss, clamp, hash } from './timeline.js';
import { theatreFrame, placard } from './overlay.js';

export const COL = {
  ink: DYE.ink, red: DYE.red, red2: DYE.crim, crim: DYE.crim, gold: DYE.yellow, gold2: DYE.gold, saffron: DYE.orange, saffron2: '#c45a1c', orange: DYE.orange, flame: DYE.orange,
  green: DYE.green, jade: DYE.jade, teal: DYE.teal, skin: DYE.skin, skinF: '#f0cf9a', skinI: '#e9c27c', skinAsh: '#cdb698', skinV: DYE.blue, skinS: '#5c84ae', skinB: '#d99a3c', skinB2: '#c78a30', skinD: '#2c6a6a',
  hairBrown: DYE.brown, beard: '#b9a68c', ashMark: '#7a6a58', rudraksha: '#5a2e14', wood: DYE.brown, iron: '#4a4a56', ivory: '#ecdcb8', ivory2: '#dcc69c', ele: '#d6cbb8', eleD: '#bfb19c',
  brass: DYE.gold, palm: DYE.hide2, conch: '#e6d6b6', pink: '#d65c74', pink2: '#e6889c', leaf: DYE.green, flowerW: '#f0e2c0', dry: '#9a7638', dry2: '#b28844', brick: '#a5452a', brick2: '#8a3822',
  cloud: DYE.teal, tiger: '#d9862a', serpent: DYE.jade, moon: '#f0d070', ganga: '#3a86ae', earth: '#8a5a2a', milk: DYE.white, milk2: DYE.hide, rock: DYE.gold, smoke: '#2b1a33', board: '#3a1a0e', letter: '#000'
};

// —— bounding box of a shape (sampled once, cached) ——
const scratch = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
function bboxOf(sh, box) {
  if (sh._bb) return sh._bb;
  const [x0, y0, x1, y1] = box, st = 3; let bx0 = 1e9, by0 = 1e9, bx1 = -1e9, by1 = -1e9;
  scratch.setTransform(1, 0, 0, 1, 0, 0); scratch.beginPath(); sh.p(scratch);
  for (let y = y0; y <= y1; y += st) for (let x = x0; x <= x1; x += st) if (scratch.isPointInPath(x, y, sh.rule || 'nonzero')) { if (x < bx0) bx0 = x; if (x > bx1) bx1 = x; if (y < by0) by0 = y; if (y > by1) by1 = y; }
  return (sh._bb = bx1 < bx0 ? box : [bx0, by0, bx1, by1]);
}
export { bboxOf };

function pattern(g, pat, bb) {
  const [x0, y0, x1, y1] = bb, w = x1 - x0, h = y1 - y0, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, m = Math.min(w, h);
  switch (pat.t) {
    case 'lattice': return lattice(g, x0, y0, x1, y1, pat.s || 10, Math.max(1.3, (pat.s || 10) * .2));
    case 'scales': return scales(g, x0, y0, x1, y1, 5, 1.1);
    case 'scalesOpen': return scalesOpen(g, x0, y0, x1, y1, 6.5);
    case 'coils': return scales(g, x0, y0, x1, y1, 7, 1.5);
    case 'coin': return coin(g, cx, cy, m * .3);
    case 'hole': return cut(g, q => q.arc(cx, cy, m * .18, 0, 2 * Math.PI));
    case 'beads': return beadLine(g, x0 + 4, cy, x1 - 4, cy, 1.8, 7);
    case 'folds': for (let x = x0 + 10; x < x1 - 6; x += 16) cutTaper(g, [[x, y0 + 8], [x + 4, cy], [x - 2, y1 - 8]], 3.2); return;
    case 'slits': { const n = pat.n || 4; for (let i = 0; i < n; i++) { const x = lerp(x0, x1, (i + .5) / n); cutTaper(g, [[x, y0 + 5], [x + 3, cy], [x - 1, y1 - 5]], 2.4); } return; }
    case 'ribs': for (let k = 1; k <= 3; k++) cutLine(g, 1.5, q => { q.moveTo(x0 + w * .25, y0 + k * h / 4.5); q.quadraticCurveTo(cx, y0 + k * h / 4.5 + 6, x1 - w * .25, y0 + k * h / 4.5); }); return;
    case 'plum': for (const [x, y] of pat.at) plum(g, x, y, pat.r || 4); return;
    case 'plums': for (let i = 0; i < 6; i++) plum(g, x0 + w * (.2 + .6 * hash(i * 3.1)), y0 + h * (.2 + .6 * hash(i * 5.7)), 4.5); return;
    case 'wrinkles': for (let y = y0 + 14; y < y1 - 6; y += 22) for (let x = x0 + 12 + (y % 3) * 6; x < x1 - 10; x += 34) cutLine(g, 1.2, q => q.arc(x, y, 9, 1.1 * Math.PI, 1.9 * Math.PI)); return;
    case 'rings': for (let y = y0 + 12; y < y1 - 6; y += 15) cutLine(g, 1.4, q => { q.moveTo(x0, y); q.lineTo(x1, y + 3); }); return;
    case 'stripes': for (let i = 0; i < 7; i++) { const x = lerp(x0 + 10, x1 - 10, i / 6); ink(g, 5, q => { q.moveTo(x, y0 + 6); q.quadraticCurveTo(x + 10, cy, x - 4, y1 - 10); }, DYE.ink); } return;
    case 'beadRing': return beads(g, Array.from({ length: 22 }, (_, k) => [pat.x + Math.cos(k * Math.PI / 11) * pat.r, pat.y + Math.sin(k * Math.PI / 11) * pat.r]), 2);
    case 'vein': return w > h ? cutTaper(g, [[x0 + w * .15, cy], [cx, cy - 2], [x1 - w * .15, cy]], 3) : cutTaper(g, [[cx, y1 - h * .1], [cx + 2, cy], [cx, y0 + h * .15]], 3);
    case 'leaves': for (let y = y0 + 6; y < y1 - 3; y += 7) cutLine(g, 1, q => { q.moveTo(x0 + 4, y); q.lineTo(x1 - 4, y); }); return;
    case 'bark': for (let x = x0 + 8; x < x1 - 4; x += 11) cutTaper(g, [[x, y1 - 10], [x + 3, cy], [x - 2, y0 + 10]], 2.6); return;
    case 'leafHoles': for (let i = 0; i < 8; i++) { const a = hash(i * 7 + pat.x) * 6.28, d = pat.r * .62 * Math.sqrt(hash(i * 3 + pat.y)); plum(g, pat.x + Math.cos(a) * d, pat.y + Math.sin(a) * d, 5.5); } cloud(g, pat.x - pat.r * .3, pat.y + pat.r * .2, pat.r * .22, 0, 2, 1); return;
    case 'bricks': for (let y = y0 + 10, r = 0; y < y1; y += 13, r++) { cutLine(g, 1.6, q => { q.moveTo(x0, y); q.lineTo(x1, y); }); for (let x = x0 + (r % 2) * 14; x < x1; x += 28) cutLine(g, 1.6, q => { q.moveTo(x, y - 13); q.lineTo(x, y); }); } return;
    case 'clouds': for (const [x, y, f] of [[cx - w * .3, cy, 1], [cx, cy - h * .15, -1], [cx + w * .3, cy, 1]]) cloud(g, x, y, m * .2, .6, 2, f); return;
    case 'strataG': return strata(g, x0, x1, x => y0 + 30 + Math.sin(x * .01) * 10, 6, 46, 4);
    case 'strataM': return strata(g, x0, x1, x => y0 + 120 + Math.abs(x) * 1.1 + Math.sin(x / 30) * 8, 9, 62, 5);
    case 'waves': return waves(g, x0, y0 + 40, x1, y1, pat.r || 15, 2.6);
    case 'hexes': for (let r = 0; r < 5; r++) for (let c = -7; c <= 7; c++) { const x = cx + c * 40 + (r % 2) * 20, y = y0 + 22 + r * 28; cut(g, q => { for (let k = 0; k < 6; k++) { const an = k * Math.PI / 3 + Math.PI / 6, px = x + Math.cos(an) * 14, py = y + Math.sin(an) * 11; k ? q.lineTo(px, py) : q.moveTo(px, py); } q.closePath(); }); } return;
    case 'border': { cutLine(g, 2.4, q => q.roundRect(-pat.w / 2 + 16, -pat.h / 2 + 16, pat.w - 32, pat.h - 32, 16)); meander(g, -pat.w / 2 + 40, -pat.h / 2 + 34, pat.w / 2 - 40, 5, 1.5); meander(g, -pat.w / 2 + 40, pat.h / 2 - 22, pat.w / 2 - 40, 5, 1.5); return; }
  }
}
let SEED = 0;
export function sprite(part) {
  return piece(part.box, g => {
    g.lineJoin = 'round';
    for (const sh of part.shapes) {
      if (sh.text) { g.save(); g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000'; g.font = `700 ${sh.size}px "FreeSerif"`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(sh.text, sh.x, sh.y); g.restore(); continue; }
      const col = COL[sh.c] || sh.c;
      if (sh.beads) { for (const [x, y] of sh.beads) { fill(g, col, q => q.arc(x, y, sh.r, 0, 2 * Math.PI)); cut(g, q => q.arc(x, y, sh.r * .3, 0, 2 * Math.PI)); } continue; }
      if (sh.line) { ink(g, sh.line, sh.p, col); continue; }
      if (sh.open) { ink(g, sh.ink || 2, sh.p, col); continue; }
      fill(g, col, sh.p, sh.rule || 'nonzero');
      if (sh.pat) within(g, sh.p, () => pattern(g, sh.pat, bboxOf(sh, part.box)));
      if (sh.ink !== 0) ink(g, sh.ink || 1.6, sh.p);
    }
  }, { seed: ++SEED, ss: 2 });
}

export async function setup(q) {
  const cv = document.getElementById('gl'); cv.width = W; cv.height = H;
  const [trc, tr] = canvas(W, H), [frc, fr] = canvas(W, H);
  const GL = makeGL(cv);
  await document.fonts.load('700 90px "FreeSerif"', 'समुद्र मंथन के अनेक रूप रहस्य विष्णु पुराण');
  const DV = CH.durvasa(), VD = CH.vidyadhari(), IN = CH.indra(), EL = CH.airavata();
  const SP = {
    'durvasa.body': sprite(DV.body), 'durvasa.arm': sprite(DV.arm), vidyadhari: sprite(VD.body), 'indra.body': sprite(IN.body), 'indra.arm': sprite(IN.arm),
    'airavata.body': sprite(EL.body), 'airavata.trunk': sprite(EL.trunk), garland: sprite(CH.garland()), garlandL: sprite(CH.garland(true)),
    tree0: sprite(CH.tree(0)), tree1: sprite(CH.tree(1)), ground: sprite(CH.ground()), deva0: sprite(CH.deva(0).body), deva1: sprite(CH.deva(1).body),
    daitya0: sprite(CH.daitya(0).body), daitya1: sprite(CH.daitya(1).body), vishnu: sprite(CH.vishnu().body), kund: sprite(CH.kund()),
    fire0: sprite(CH.fire(0)), fire1: sprite(CH.fire(1)), shrubF: sprite(CH.shrub(false)), shrubW: sprite(CH.shrub(true)), petal: sprite(CH.petal()),
    smoke0: sprite(CH.smoke(0)), smoke1: sprite(CH.smoke(1)), sea0: sprite(CH.sea(0)), sea1: sprite(CH.sea(1)), mandara: sprite(CH.mandara()),
    kurma: sprite(CH.kurma()), mandaraB: sprite(CH.mandaraBare()), wrap: sprite(CH.wrap()), vasuki: sprite(CH.vasuki()), spark: sprite(CH.spark()),
    hook: sprite(CH.plaque([['विष्णु के', -52, 100], ['अनेक रूप', 66, 100]], 760, 300)),
    title: sprite(CH.plaque([['समुद्र मंथन', -78, 112], ['के रहस्य', 44, 104], ['विष्णु पुराण के अनुसार', 132, 44]], 860, 390)),
  };
  const FRAME = theatreFrame();
  let CM = [1, 0, 0, 1, 0, 0];
  const draw = (id, M, a = 1, b = 0) => { const p = SP[id]; if (!p || a <= .002) return; tr.save(); tr.setTransform(...mul(CM, M)); tr.globalCompositeOperation = 'multiply'; tr.globalAlpha = a; if (b > .4) tr.filter = `blur(${b.toFixed(1)}px)`; tr.drawImage(p.c, p.x0, p.y0, p.w, p.h); tr.restore(); };
  const clear = () => { tr.setTransform(1, 0, 0, 1, 0, 0); tr.globalCompositeOperation = 'source-over'; tr.globalAlpha = 1; tr.filter = 'none'; tr.fillStyle = '#fff'; tr.fillRect(0, 0, W, H); fr.setTransform(1, 0, 0, 1, 0, 0); fr.clearRect(0, 0, W, H); };

  if (q.get('test') === 'sheet') {   // character model sheet
    const SH = { shiva: sprite(CH.shiva().body), brahma: sprite(CH.brahma().body) };
    Object.assign(SP, SH);
    return () => {
      clear(); CM = [1, 0, 0, 1, 0, 0];
      const cells = [['durvasa.body', 'दुर्वासा', 180, 720, .82], ['vidyadhari', 'विद्याधरी', 540, 560, .85], ['vishnu', 'विष्णु', 900, 720, .78],
        ['shiva', 'शिव', 180, 1340, .76], ['brahma', 'ब्रह्मा', 540, 1340, .78], ['deva0', 'देवता', 830, 1340, .72], ['daitya0', 'दैत्य', 990, 1340, .72]];
      for (const [id, , x, y, s] of cells) draw(id, mul(T(x, y), Sc(s)));
      draw('durvasa.arm', mul(mul(T(180, 720), Sc(.82)), mul(T(...DV.shoulder), R(.1))));
      // Indra on Airavata
      const ME = mul(T(560, 1800), Sc(-.78, .78)); draw('airavata.body', ME); draw('airavata.trunk', mul(mul(ME, T(...EL.trunkBase)), R(.05)));
      const seat = [560 + 30 * .78, 1800 - 352 * .78], MI = mul(T(...seat), Sc(-.78, .78)); draw('indra.body', MI); draw('indra.arm', mul(mul(MI, T(...IN.shoulder)), R(.2)));
      draw('garland', mul(T(900, 1560), Sc(1.2)));
      fr.save(); fr.font = '700 40px "FreeSerif"'; fr.textAlign = 'center'; fr.fillStyle = '#2a140c';
      for (const [, name, x, y] of cells) fr.fillText(name, x, y + 50);
      fr.fillText('इंद्र और ऐरावत', 330, 1860); fr.fillText('दिव्य माला', 900, 1720);
      fr.font = '700 44px "FreeSerif"'; fr.fillText('पात्र — छाया कठपुतली', 540, 70); fr.restore();
      GL.render(trc, frc, { cam: [540, 960, 1], rect: [0, 0, W, H], lamps: [[540, 600, 1, .5], [540, 1400, 1, .5]], expo: 1.25, sigB: 900, sigC: 300, amb: .35, vign: .2, sat: 1.12, contrast: .14, bloom: .2 });
    };
  }

  const fl = (t, k) => 1 + .05 * Math.sin(t * 7.3 + k * 2.1) + .03 * Math.sin(t * 23 + k);
  const flare = (t, t0, d = .45) => { if (t < t0) return 0; const u = (t - t0) / d; return u < 1 ? lerp(.1, 1, 1 - Math.pow(1 - u, 3)) + .35 * Math.sin(u * Math.PI) : 1; };
  return t => {
    const F = frame(t), [cx, cy, z] = F.cam, m = F.mood;
    CM = [z, 0, 0, z, W / 2 - cx * z, H / 2 - cy * z];
    clear();
    for (const it of F.items) {
      let M = it.M;
      if (it.jit) { const k = it.id.length * 3.7; M = mul(M, mul(T(2.2 * Math.sin(t * 1.7 + k) + 1.1 * Math.sin(t * 3.3 + k * 2), 1.5 * Math.sin(t * 1.3 + k)), R(.01 * Math.sin(t * 1.1 + k)))); }
      draw(it.id, M, it.a, it.b);
    }
    fr.drawImage(FRAME, 0, 0); placard(fr, t);
    const L = F.lamps;
    const n = Math.max(.35, L.reduce((a, l) => a + l[2], 0));
    GL.render(trc, frc, {
      lamps: L.map((l, k) => [l[0], l[1], l[2] * fl(t, k), l[3]]), cam: F.cam, expo: 1.3 / Math.sqrt(n), sigB: 760, sigC: 150, amb: .28, time: t,
      haze: m.anger * 2.2, vign: .55 + m.drain * .2, sat: 1.18 - m.drain * .45, contrast: .17, bloom: .32,
      lcol: [1, lerp(.77, .5, m.anger), lerp(.46, .3, m.anger)], fade: clamp(m.fade + m.flash * .75), fadeCol: m.flash > 0 ? [1, .93, .8] : [0, 0, 0], rect: [0, 0, W, H]
    });
  };
}

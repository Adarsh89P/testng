// Oil Painting (impasto) renderer: every part of chars.js is painted as a flat, value-planned
// reference (light from the upper left), turned into palette-knife strokes, and moved as a whole.
import { Impasto, Strokes } from './impasto.js';
import { Ref, paintRef } from './plate.js';
import * as CH from './chars.js';
import { W, H, DUR, frame, mul, T, Sc, R, lerp, seg, ss, clamp } from './timeline.js';
import { oilSub } from './overlay.js';
import { bboxOf } from './puppet.js';

const COL = {
  ink: '#1a1420', red: '#c8321e', red2: '#9a1e1a', crim: '#8e1a24', gold: '#f2b830', gold2: '#d89a28', saffron: '#ee7a1e', saffron2: '#d6601a', orange: '#f08a2a', flame: '#ff9a2a',
  green: '#2f8a48', jade: '#3aa07a', teal: '#2a6e8a', skin: '#e8b48a', skinF: '#f0c29a', skinI: '#e6b070', skinAsh: '#c9b4a0', skinV: '#3456b8', skinS: '#6a8cbc', skinB: '#e0a04a', skinB2: '#cc8a3a', skinD: '#2e7070',
  hairBrown: '#5a3420', beard: '#e4dccc', ashMark: '#f6f2ea', rudraksha: '#6a3418', wood: '#6a4224', iron: '#5a5e6e', ivory: '#f6ecd4', ivory2: '#e8d8b4', ele: '#ece6dc', eleD: '#cfc4b6',
  brass: '#d8a040', palm: '#d8b878', conch: '#f6eee0', pink: '#ee6a86', pink2: '#f6a0b4', leaf: '#3a8a3a', flowerW: '#fff4dc', dry: '#a48040', dry2: '#c09850', brick: '#b04a2a', brick2: '#8e3a22',
  cloud: '#4a7ea0', tiger: '#e8922a', serpent: '#3a9a6a', moon: '#fff0a0', ganga: '#5ab0e0', earth: '#8a5a2a', milk: '#f6ecda', milk2: '#e2d4c4', rock: '#c89a48', smoke: '#3a2a44', board: '#3a1a0e', letter: '#f8e2a8'
};
const hexRGB = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mix = (h, t, k) => { const a = hexRGB(h), b = hexRGB(t); return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(',')})`; };
const shade = (h, bb, ox, oy) => c => { const g = c.createLinearGradient(bb[0] - ox, bb[1] - oy, bb[2] - ox, bb[3] - oy); g.addColorStop(0, mix(h, '#fff2d8', .22)); g.addColorStop(.5, h); g.addColorStop(1, mix(h, '#20183a', .32)); return g; };

function paintPart(part) {
  const [x0, y0, x1, y1] = part.box, w = x1 - x0, h = y1 - y0, sc = Math.min(1, Math.sqrt(260000 / (w * h)));
  const Rf = new Ref(w, h, sc), mv = p => c => { c.save(); c.translate(-x0, -y0); p(c); c.restore(); };
  part.shapes.forEach((sh, i) => {
    const g = 'g' + i;
    if (sh.text) { Rf.text(sh.text, sh.x - x0, sh.y - y0 + sh.size * .36, `700 ${sh.size}px "FreeSerif"`, COL.letter, { group: g, maxR: 1.4, align: 'center' }); return; }
    const col = COL[sh.c] || sh.c;
    if (sh.beads) { sh.beads.forEach(([x, y], j) => Rf.fill(mv(CH.C(x, y, sh.r * 1.1)), mix(col, '#fff0d0', .15), { group: g + 'b' + j, maxR: 2 })); return; }
    if (sh.line) { Rf.line(mv(sh.p), col, Math.max(2.6, sh.line * 1.5), { group: g, maxR: 1.4, dir: 'edge' }); return; }
    const bb = bboxOf(sh, part.box), m = Math.min(bb[2] - bb[0], bb[3] - bb[1]);
    const props = { group: g, maxR: sh.oil?.maxR ?? clamp(m / 7, 2, 12), dir: sh.oil?.dir ?? 'edge', fallback: 90, hgt: 1.1, detail: .9, rule: sh.rule };
    if (sh.open) { Rf.fill(mv(sh.p), shade(COL[sh.skin] || COL.skin, bb, x0, y0), { ...props, maxR: 3, detail: .7 }); Rf.line(mv(sh.p), mix(COL[sh.skin] || COL.skin, '#1a1420', .55), 2.6, { group: g + 'o', maxR: 1.2 }); return; }
    Rf.fill(mv(sh.p), shade(col, bb, x0, y0), props);
    if (sh.pat?.t === 'stripes') for (let k = 0; k < 7; k++) { const x = lerp(bb[0] + 10, bb[2] - 10, k / 6); Rf.line(mv(c => { c.moveTo(x, bb[1] + 6); c.quadraticCurveTo(x + 10, (bb[1] + bb[3]) / 2, x - 4, bb[3] - 10); }), '#2a1a10', 6, { group: g + 's' + k, maxR: 2 }); }
    if (sh.pat?.t === 'lattice' || sh.pat?.t === 'scalesOpen' || sh.pat?.t === 'scales') {   // brocade glints: a few light dabs
      for (let k = 0; k < 6; k++) { const x = lerp(bb[0], bb[2], .2 + .6 * ((k * 37) % 10) / 10), y = lerp(bb[1], bb[3], .2 + .6 * ((k * 53) % 10) / 10); Rf.tint(mv(CH.C(x, y, 3)), mix(col, '#fff6dc', .55)); }
    }
  });
  const st = paintRef(Rf, { R: [14, 7, 3.6, 2].map(r => r * sc), T: 11, seed: part.shapes.length * 7 + w, app: (x, y, lv) => x / w * .55 + y / h * .25 + lv * .04 });
  return { st, ref: Rf, w, h, x0, y0 };
}

// —— backgrounds ——
function forestPlate() {
  const Rf = new Ref(W, H, .5), lin = (x0, y0, x1, y1, s) => c => { const g = c.createLinearGradient(x0, y0, x1, y1); s.forEach(([o, col]) => g.addColorStop(o, col)); return g; };
  Rf.fill(CH.P([[0, 0], [W, 0], [W, 1240], [0, 1240]]), lin(0, 0, 0, 1240, [[0, '#24436a'], [.45, '#5f7aa0'], [.8, '#e0aa7a'], [1, '#f4cc8a']]), { dir: -4, fallback: -4, group: 'sky', maxR: 60, detail: 2.4 });
  Rf.fill(CH.E(520, 820, 420, 300), c => { const g = c.createRadialGradient(520, 820, 20, 520, 820, 420); g.addColorStop(0, '#fff0c4'); g.addColorStop(1, 'rgba(240,190,130,0)'); return g; }, { dir: { radial: [520, 820] }, group: 'sky', maxR: 40 });
  Rf.fill(c => { c.moveTo(0, 1240); for (let x = 0; x <= W; x += 60) c.lineTo(x, 1080 - Math.sin(x / 160) * 50 - Math.sin(x / 70) * 16); c.lineTo(W, 1240); c.closePath(); }, lin(0, 1000, 0, 1240, [[0, '#7a6a9a'], [1, '#5a4a7a']]), { dir: 0, group: 'hills', maxR: 30 });
  for (const [x, y, r, col] of [[-40, 1060, 260, '#2a4a3a'], [180, 1130, 170, '#34583e'], [900, 1080, 230, '#2e4c3c'], [1120, 1000, 280, '#24402e']]) Rf.fill(CH.E(x, y, r, r * .9), col, { dir: 'edge', group: 'f' + x, maxR: 26 });
  Rf.fill(CH.P([[0, 1240], [W, 1240], [W, H], [0, H]]), lin(0, 1240, 0, H, [[0, '#c4925a'], [.35, '#9a6a3c'], [1, '#4a3224']]), { dir: 0, fallback: 0, group: 'ground', maxR: 30 });
  Rf.fill(c => { c.moveTo(380, 1240); c.lineTo(700, 1240); c.lineTo(980, H); c.lineTo(120, H); c.closePath(); }, lin(0, 1240, 0, H, [[0, '#e6c08a'], [1, '#a87a4a']]), { dir: 90, group: 'path', maxR: 24 });
  return { st: paintRef(Rf, { R: [44, 22, 11, 5.5].map(r => r * .5), T: 12, seed: 3, app: (x, y, lv) => y / H * .7 + lv * .05 }), ref: Rf };
}
function nightPlate() {
  const Rf = new Ref(W, H, .5), lin = (x0, y0, x1, y1, s) => c => { const g = c.createLinearGradient(x0, y0, x1, y1); s.forEach(([o, col]) => g.addColorStop(o, col)); return g; };
  Rf.fill(CH.P([[0, 0], [W, 0], [W, H], [0, H]]), lin(0, 0, 0, H, [[0, '#141a44'], [.35, '#2c2f6e'], [.65, '#6a4a86'], [.85, '#c08a7a'], [1, '#3a2a4a']]), { dir: -6, fallback: -6, group: 'sky', maxR: 60, detail: 2.4 });
  Rf.fill(CH.E(540, 820, 470, 470), c => { const g = c.createRadialGradient(540, 820, 20, 540, 820, 470); g.addColorStop(0, '#fff0c0'); g.addColorStop(.3, '#f6c878'); g.addColorStop(.7, '#d48a62'); g.addColorStop(1, 'rgba(106,74,134,0)'); return g; }, { dir: { radial: [540, 820] }, group: 'sky', maxR: 44, detail: 1.6 });
  return { st: paintRef(Rf, { R: [44, 22, 11, 5.5].map(r => r * .5), T: 12, seed: 5, app: (x, y, lv) => Math.hypot(x - 540, y - 820) / 1400 + lv * .05 }), ref: Rf };
}

export async function setup(q) {
  await document.fonts.load('700 90px "FreeSerif"', 'समुद्र मंथन मुख या पूँछ रहस्य विष्णु पुराण');
  const cv = document.getElementById('gl'), ov = document.getElementById('ov'), og = ov.getContext('2d');
  const E = new Impasto(cv, { W, H, ss: +(q.get('ss') || 1.5) });
  const DV = CH.durvasa(), VD = CH.vidyadhari(), IN = CH.indra(), EL = CH.airavata();
  const parts = {
    'durvasa.body': DV.body, 'durvasa.arm': DV.arm, vidyadhari: VD.body, 'indra.body': IN.body, 'indra.arm': IN.arm, 'airavata.body': EL.body, 'airavata.trunk': EL.trunk,
    garland: CH.garland(), garlandL: CH.garland(true), tree0: CH.tree(0), tree1: CH.tree(1), deva0: CH.deva(0).body, deva1: CH.deva(1).body, daitya0: CH.daitya(0).body, daitya1: CH.daitya(1).body,
    vishnu: CH.vishnu().body, kund: CH.kund(), fire0: CH.fire(0), fire1: CH.fire(1), shrubF: CH.shrub(false), shrubW: CH.shrub(true), petal: CH.petal(), smoke0: CH.smoke(0), smoke1: CH.smoke(1),
    sea0: CH.sea(0), sea1: CH.sea(1), mandara: CH.mandara(),
    kurma: CH.kurma(), mandaraB: CH.mandaraBare(), wrap: CH.wrap(), vasuki: CH.vasuki(), spark: CH.spark(), cloud: CH.cloudProp(), rain0: CH.rain(0), rain1: CH.rain(1),
    hook: CH.plaque([['मुख या', -52, 104], ['पूँछ?', 66, 104]], 640, 300), title: CH.plaque([['समुद्र मंथन', -78, 112], ['के रहस्य', 44, 104], ['विष्णु पुराण के अनुसार', 132, 44]], 860, 390),
  };
  const sheet = q.get('test') === 'sheet';
  if (sheet) { parts.shiva = CH.shiva().body; parts.brahma = CH.brahma().body; }
  const P = {};
  for (const [id, part] of Object.entries(parts)) { const p = paintPart(part); P[id] = { b: E.batch(p.st.data()), tex: E.texture(p.ref.ctx.canvas), w: p.w, h: p.h, x0: p.x0, y0: p.y0 }; }
  const FP = forestPlate(), NP = nightPlate();
  const plate = s => ({ b: E.batch(s.st.data()), tex: E.texture(s.ref.ctx.canvas) });
  const FOREST = plate(FP), NIGHT = plate(NP);
  const drawPart = (id, M, o) => {
    const p = P[id]; if (!p || o.alpha <= .002) return;
    const Mo = mul(M, T(p.x0, p.y0)), ua = clamp((o.t - (o.t0 ?? -1e6)) / .45);
    E.under(p.tex, p.w, p.h, { M: Mo, cam: o.cam, alpha: o.alpha * ua, grey: 0, reveal: -1e6 });
    E.draw(p.b, { M: Mo, cam: o.cam, t: o.t, alpha: o.alpha, appear: o.t0 ?? -1e6, appDur: .45, grey: 0, reveal: -1e6 });
  };
  const drawPlate = (pl, cam, t, t0, appDur = .7) => { E.under(pl.tex, W, H, { cam, alpha: clamp((t - t0) / appDur), grey: 0, reveal: -1e6 }); E.draw(pl.b, { cam, t, appear: t0, appDur, grey: 0, reveal: -1e6 }); };

  if (sheet) return () => {
    const cam = { x: W / 2, y: H / 2, zoom: 1 }, o = { cam, t: 10, alpha: 1 };
    E.begin(); drawPlate(FOREST, cam, 10, -10);
    const cells = [['durvasa.body', 180, 720, .82], ['vidyadhari', 540, 560, .85], ['vishnu', 900, 720, .78], ['shiva', 180, 1340, .76], ['brahma', 540, 1340, .78], ['deva0', 830, 1340, .72], ['daitya0', 990, 1340, .72]];
    for (const [id, x, y, s] of cells) drawPart(id, mul(T(x, y), Sc(s)), o);
    drawPart('durvasa.arm', mul(mul(T(180, 720), Sc(.82)), mul(T(...DV.shoulder), R(.1))), o);
    const ME = mul(T(560, 1800), Sc(-.78, .78)); drawPart('airavata.body', ME, o); drawPart('airavata.trunk', mul(mul(ME, T(...EL.trunkBase)), R(.05)), o);
    const MI = mul(T(560 + 30 * .78, 1800 - 352 * .78), Sc(-.78, .78)); drawPart('indra.body', MI, o); drawPart('indra.arm', mul(mul(MI, T(...IN.shoulder)), R(.2)), o);
    drawPart('garland', mul(T(900, 1560), Sc(1.2)), o);
    E.finish({ expo: 1.02, sat: 1.06, contrast: 1.04, vig: .25 });
    og.clearRect(0, 0, W, H); og.font = '700 40px "FreeSerif"'; og.textAlign = 'center'; og.fillStyle = '#fff4dc'; og.shadowColor = 'rgba(0,0,0,.7)'; og.shadowBlur = 8;
    [['दुर्वासा', 180, 770], ['विद्याधरी', 540, 610], ['विष्णु', 900, 770], ['शिव', 180, 1390], ['ब्रह्मा', 540, 1390], ['देवता', 830, 1390], ['दैत्य', 990, 1390], ['इंद्र और ऐरावत', 330, 1860], ['दिव्य माला', 900, 1720]].forEach(([s, x, y]) => og.fillText(s, x, y));
    og.font = '700 44px "FreeSerif"'; og.fillText('पात्र — तैल चित्र', 540, 70);
  };

  return t => {
    const F = frame(t), [cx, cy, z] = F.cam, m = F.mood, cam = { x: cx, y: cy, zoom: z };
    E.begin();
    drawPlate(NIGHT, cam, t, -10);                                 // the night sky over the Ocean of Milk
    // oil paint is opaque: the Kurma is painted in front of the front wave so it stays visible
    const items = F.items.filter(i => i.id !== 'ground'), k = items.filter(i => i.id === 'kurma'), rest = items.filter(i => i.id !== 'kurma');
    const at = rest.findIndex(i => i.id === 'sea1'); if (at >= 0) rest.splice(at + 1, 0, ...k); else rest.push(...k);
    for (const it of rest) drawPart(it.id, it.M, { cam, t, alpha: it.a, t0: it.t0 });
    const post = { expo: 1.03, sat: 1.08, contrast: 1.05, vig: .3, spec: .26, shin: 26 };
    if (m.anger > 0) { post.lightCol = [1, lerp(.95, .62, m.anger), lerp(.9, .46, m.anger)]; post.expo += .06 * m.anger; post.vig += .15 * m.anger; }
    if (m.drain > 0) { post.sat = lerp(1.08, .28, m.drain); post.expo = lerp(1.03, .86, m.drain); post.vig += .2 * m.drain; }
    post.expo = (post.expo + m.flash * .8) * (1 - m.fade);
    E.finish(post);
    og.clearRect(0, 0, W, H);
    if (q.get('thumb')) {   // cover image: big title instead of the subtitle
      og.save(); og.textAlign = 'center'; og.textBaseline = 'middle'; og.lineJoin = 'round';
      const gv = og.createLinearGradient(0, 120, 0, 760); gv.addColorStop(0, 'rgba(18,10,30,.72)'); gv.addColorStop(1, 'rgba(18,10,30,0)'); og.fillStyle = gv; og.fillRect(0, 0, W, 800);
      const line = (txt, y, size, col, w) => { og.font = `700 ${size}px "FreeSerif"`; og.strokeStyle = '#1e0c06'; og.lineWidth = w; og.shadowColor = 'rgba(0,0,0,.8)'; og.shadowBlur = 20; og.strokeText(txt, W / 2, y); og.shadowBlur = 0; og.fillStyle = col; og.fillText(txt, W / 2, y); };
      line('वासुकि का मुख', 290, 118, '#fff4dc', 14);
      line('दैत्यों को क्यों?', 440, 130, '#ffcf4a', 16);
      line('एक ओर अग्नि · दूसरी ओर वर्षा', 1650, 70, '#fff4dc', 11);
      og.restore();
    } else oilSub(og, t);
  };
}

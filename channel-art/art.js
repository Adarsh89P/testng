// Channel art for ग्रंथ रहस्य, painted with the same oil engine as the videos.
// ?art=banner (2560×1440) | profile (800×800)
import { Impasto } from './impasto.js';
import { Ref, paintRef } from './plate.js';
import * as CH from './chars.js';
import { mul, T, Sc, lerp, clamp } from './timeline.js';
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


const q = new URLSearchParams(location.search), ART = q.get('art') || 'banner';
const W = ART === 'banner' ? 2560 : 800, H = ART === 'banner' ? 1440 : 800;
await document.fonts.load('700 150px "FreeSerif"', 'ग्रंथ रहस्य शास्त्रों की अनसुनी कथाएँ रंगों में पुराण रामायण महाभारत उपनिषद');
const cv = document.getElementById('gl'), ov = document.getElementById('ov');
for (const c of [cv, ov]) { c.width = W; c.height = H; c.style.width = W + 'px'; c.style.height = H + 'px'; }
const E = new Impasto(cv, { W, H, ss: 1.5 }), og = ov.getContext('2d');
const lin = (x0, y0, x1, y1, s) => c => { const g = c.createLinearGradient(x0, y0, x1, y1); s.forEach(([o, col]) => g.addColorStop(o, col)); return g; };
const radial = (x, y, r, s) => c => { const g = c.createRadialGradient(x, y, 10, x, y, r); s.forEach(([o, col]) => g.addColorStop(o, col)); return g; };

// —— the painted plate ——
const HX = ART === 'banner' ? 1300 : 400, HY = ART === 'banner' ? 690 : 400, HR = ART === 'banner' ? 640 : 380;
const sc = ART === 'banner' ? .4 : .7, plate = new Ref(W, H, sc);
plate.fill(CH.P([[0, 0], [W, 0], [W, H], [0, H]]), lin(0, 0, 0, H, [[0, '#121844'], [.45, '#2a2c6c'], [.75, '#5c447e'], [1, '#2a1e3e']]), { dir: -6, fallback: -6, group: 'sky', maxR: 60, detail: 2.4 });
plate.fill(CH.E(HX, HY, HR, HR * (ART === 'banner' ? .78 : 1)), radial(HX, HY, HR, [[0, '#fff2c4'], [.3, '#f6c878'], [.65, '#d4866a'], [1, 'rgba(92,68,126,0)']]), { dir: { radial: [HX, HY] }, group: 'sky', maxR: 44, detail: 1.5 });
if (ART === 'banner') {
  plate.fill(c => { c.moveTo(0, H); c.lineTo(0, 1180); for (let x = 0; x <= W; x += 80) c.lineTo(x, 1180 + Math.sin(x / 130) * 14); c.lineTo(W, H); c.closePath(); }, lin(0, 1180, 0, H, [[0, '#f4e8d2'], [.5, '#cbbcd0'], [1, '#7a6a96']]), { dir: 0, fallback: 0, group: 'sea', maxR: 26 });
  for (const [x, h] of [[220, 520], [2340, 560]]) plate.fill(CH.S([[x - 260, 1200], [x - 120, 1200 - h * .55], [x, 1200 - h], [x + 120, 1200 - h * .55], [x + 260, 1200]]), '#3a2e5c', { dir: 90, group: 'm' + x, maxR: 22 });
}
const pst = paintRef(plate, { R: [44, 22, 11, 5.5].map(r => r * sc), T: 12, seed: 9 });
const PL = { b: E.batch(pst.data()), tex: E.texture(plate.ctx.canvas) };

// —— painted parts ——
const parts = [];
const addPart = (part, M) => { const p = paintPart(part); parts.push({ b: E.batch(p.st.data()), tex: E.texture(p.ref.ctx.canvas), w: p.w, h: p.h, M: mul(M, T(p.x0, p.y0)) }); };
if (ART === 'profile') {
  addPart({ box: [-150, -150, 150, 150], shapes: CH.chakraShapes(0, 0, 110) }, mul(T(400, 400), Sc(2.05)));
} else {
  addPart(CH.vishnu().body, mul(T(690, 1150), Sc(.98)));
  addPart({ box: [-140, -110, 140, 12], shapes: CH.lotusShapes(0, 0, 1.45) }, mul(T(1880, 1000), Sc(1.35)));
  addPart({ box: [-150, -150, 150, 150], shapes: CH.chakraShapes(0, 0, 110) }, mul(T(1900, 640), Sc(.95)));
}

window.render = () => {
  const cam = { x: W / 2, y: H / 2, zoom: 1 };
  E.begin();
  E.under(PL.tex, W, H, { cam, grey: 0, reveal: -1e6 }); E.draw(PL.b, { cam, grey: 0, reveal: -1e6 });
  for (const p of parts) { E.under(p.tex, p.w, p.h, { M: p.M, cam, grey: 0, reveal: -1e6 }); E.draw(p.b, { M: p.M, cam, grey: 0, reveal: -1e6 }); }
  E.finish({ expo: 1.04, sat: 1.1, contrast: 1.05, vig: .28, spec: .26, shin: 26 });
  og.clearRect(0, 0, W, H);
  if (ART === 'banner') {   // text stays inside the 1546×423 safe area (x 507–2053, y 508–931)
    og.save(); og.textAlign = 'center'; og.textBaseline = 'middle'; og.lineJoin = 'round';
    // a soft dark plane behind the words so they read over the bright halo
    const gv = og.createRadialGradient(1330, 740, 40, 1330, 740, 640); gv.addColorStop(0, 'rgba(24,14,40,.55)'); gv.addColorStop(1, 'rgba(24,14,40,0)');
    og.fillStyle = gv; og.fillRect(0, 0, W, H);
    const line = (txt, y, size, fillCol, w) => { og.font = `700 ${size}px "FreeSerif"`; og.strokeStyle = '#2a1408'; og.lineWidth = w; og.shadowColor = 'rgba(10,5,20,.8)'; og.shadowBlur = 24; og.strokeText(txt, 1330, y); og.shadowBlur = 0; og.fillStyle = fillCol; og.fillText(txt, 1330, y); };
    line('ग्रंथ रहस्य', 640, 200, '#ffd970', 14);
    line('शास्त्रों की अनसुनी कथाएँ — रंगों में', 800, 66, '#fff4dc', 9);
    line('पुराण  •  रामायण  •  महाभारत  •  उपनिषद', 885, 46, '#ffe0a0', 8);
    og.restore();
  }
};
window.DUR = 1; window.render(); window.READY = true;

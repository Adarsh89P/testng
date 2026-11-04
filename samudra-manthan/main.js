// Samudra Manthan: the 14 ratnas. Shadow Puppetry. Timeline = one source of truth (picture, captions, sound cues)
import { makeGL } from './gl.js';
import { canvas, drawPiece, DYE } from './carve.js';
import { clamp, lerp, seg, ss, eo, eio, back, hash } from '/core/lib.js';
import { drawFrame, drawAudience } from './stage.js';
import { buildArt } from './art.js';

const qs = new URLSearchParams(location.search);
const W = 1920, H = 1080;
const [trc, tr] = canvas(W, H), [frc, fr] = canvas(W, H);
const GL = makeGL(document.getElementById('gl'));
for (const w of ['600', '700']) await document.fonts.load(`${w} 40px "Noto Serif Devanagari"`, 'समुद्र मंथन कामधेनु उच्चैःश्रवा पाञ्चजन्य');
const A = buildArt();
const E = (t, a, b) => ss(seg(t, a, b));

// ---------- timeline (film seconds; the voice-over starts at OFF) ----------
const OFF = 1.5, DUR = 54;
const CAPS = [   // [voice start, voice end, text]  (times are in the voice file)
  [0.00, 3.17, 'समुद्र के किनारे, देवता और असुर मिले।'],
  [3.66, 7.37, 'मंदराचल मथनी बना, और नाग वासुकि रस्सी।'],
  [8.04, 11.86, 'कछुए के रूप में विष्णु ने पर्वत को अपनी पीठ पर थाम लिया।'],
  [12.38, 16.46, 'मंथन शुरू हुआ, और सबसे पहले निकला हलाहल विष।'],
  [16.96, 18.00, 'अंधकार छा गया।'],
  [18.58, 21.95, 'तब शिव ने वह विष पिया, और कंठ नीला हुआ।'],
  [21.95, 23.49, 'वे नीलकंठ कहलाए।'],
  [24.10, 29.28, 'फिर निकलीं कामधेनु गाय, उच्चैःश्रवा घोड़ा और ऐरावत हाथी।'],
  [29.78, 33.07, 'कौस्तुभ मणि, कल्पवृक्ष, और अप्सरा रंभा।'],
  [33.55, 37.62, 'फिर लक्ष्मी, वारुणी, चंद्रमा, और पाञ्चजन्य शंख।'],
  [38.08, 42.17, 'अंत में धन्वंतरि प्रकट हुए, हाथ में अमृत का कलश लिए।'],
  [42.68, 45.89, 'पुराणों में सूची थोड़ी बदलती है, पर कथा वही है।'],
  [46.39, 48.67, 'अमृत से पहले, विष पीना पड़ा।']
].map(([a, b, text]) => ({ t0: a + OFF, t1: b + OFF + .35, text }));
window.SUBS = CAPS;

const T = { titleIn: .3, titleOut: 4.3, mount: 5.3, snake: 7.0, pull: 8.8, kurma: 9.9, lift: 10.3, poison: 13.9, dark: 18.4, shiva: 19.8, drink: 20.8, throat: 22.2, shivaOut: 24.4, smokeGone: 22.0,
  crown: 40.4, amrit: 42.0, pullback: 44.0, carry0: 48.0, carry1: 52.6 };
// the ratnas: [key, label, time it appears, slot x, slot y, scale, lamp?]
const RATNA = [
  ['cow', 'कामधेनु', 26.1, 160, 330, 1.45, 1], ['horse', 'उच्चैःश्रवा', 27.5, 300, 235, 1.45, 1], ['elephant', 'ऐरावत', 28.8, 470, 330, 1.35, 1],
  ['gem', 'कौस्तुभ', 31.7, 640, 235, 1.35, 1], ['tree', 'कल्पवृक्ष', 32.7, 810, 330, 1.35, 1], ['apsara', 'रंभा', 34.0, 1110, 235, 1.45, 1],
  ['lakshmi', 'लक्ष्मी', 35.7, 1280, 330, 1.4, 1], ['varuni', 'वारुणी', 36.8, 1430, 235, 1.4, 0], ['chandra', 'चंद्रमा', 37.8, 1600, 330, 1.35, 1], ['conch', 'पाञ्चजन्य', 38.9, 1765, 235, 1.12, 0]
];
const GROUND = 800, ROPE = 615, PEAK = 406, MREST = GROUND - 40, MS = .82, PEAK2 = MREST - 432 * MS;
const DEVA_X = [120, 240, 360, 480, 600], ASURA_X = [1320, 1440, 1560, 1680, 1800];

// ---------- camera ----------
const kick = (t, t0, a = .1) => t >= t0 ? a * Math.max(0, 1 - (t - t0) / .28) : 0;
function camAt(t) {
  let c = [960, 540, 1];
  const L = (a, b, u) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)];
  if (t < 4.6) c = [960, 540, 1];
  else if (t < 6.4) c = L([960, 540, 1], [960, 560, 1.12], eio(seg(t, 4.6, 6.4)));
  else if (t < 9.3) c = L([960, 560, 1.12], [960, 600, 1.16], seg(t, 6.4, 9.3));
  else if (t < 10.5) c = L([960, 600, 1.16], [960, 690, 1.6], eio(seg(t, 9.3, 10.5)));
  else if (t < 11.9) c = [960, 690, 1.6];
  else if (t < 13.2) c = L([960, 690, 1.6], [960, 540, 1], eio(seg(t, 11.9, 13.2)));
  else if (t < 19.4) c = [960, 540, 1];
  else if (t < 21.2) c = L([960, 540, 1], [960, 470, 1.3], eio(seg(t, 19.4, 21.2)));
  else if (t < 22.2) c = L([960, 470, 1.3], [985, 380, 2.1], eio(seg(t, 21.2, 22.2)));
  else if (t < 24.0) c = [985, 380, 2.1];
  else if (t < 25.4) c = L([985, 380, 2.1], [960, 540, 1], eio(seg(t, 24.0, 25.4)));
  else if (t < 40) c = [960, 540, 1];
  else if (t < 42.6) c = L([960, 540, 1], [960, 330, 1.35], eio(seg(t, 40, 42.6)));
  else if (t < 44.0) c = [960, 330, 1.35];
  else if (t < 46.6) c = L([960, 330, 1.35], [960, 540, .86], eio(seg(t, 44, 46.6)));
  else c = [960, 540, .86];
  c = [c[0], c[1], c[2] * (1 + kick(t, T.poison) + kick(t, T.dark, .12) + kick(t, T.throat, .08) + kick(t, 40.5, .06))];
  if (c[2] >= 1) { c[0] = clamp(c[0], 960 / c[2], 1920 - 960 / c[2]); c[1] = clamp(c[1], 540 / c[2], 1080 - 540 / c[2]); }
  return c;
}
const camM = ([cx, cy, z]) => [z, 0, 0, z, 960 - cx * z, 540 - cy * z];
let C = camM([960, 540, 1]), SA = 1;

// ---------- drawing helpers ----------
function put(p, x, y, o = {}) {
  const { rot = 0, sx = 1, sy = 1, blur = 0, flip = 1, free = false } = o; const a = (o.a ?? 1) * (free ? 1 : SA);
  if (a <= 0.01) return;
  tr.save(); tr.setTransform(C[0], C[1], C[2], C[3], C[4], C[5]); tr.translate(x, y); tr.rotate(rot); tr.scale(sx * flip, sy);
  tr.globalCompositeOperation = 'multiply'; tr.globalAlpha = a; if (blur > .4) tr.filter = `blur(${blur}px)`;
  drawPiece(tr, p); tr.restore();
}
const press = (t, t0, d = .5) => { const u = eo(seg(t, t0, t0 + d)); return { sx: 1 + (1 - u) * .55, sy: 1 + (1 - u) * .55, blur: (1 - u) * 18, a: Math.min(1, u * 2.2) }; };
const lift = (t, t0, d = .9) => { const u = ss(seg(t, t0, t0 + d)); return { sx: 1 + u * .45, sy: 1 + u * .45, blur: u * 20, a: 1 - u }; };
function label(text, x, y, a) {
  if (a <= .01) return;
  tr.save(); tr.setTransform(C[0], C[1], C[2], C[3], C[4], C[5]); tr.globalCompositeOperation = 'multiply'; tr.globalAlpha = a;
  tr.font = `700 36px "Noto Serif Devanagari"`; tr.textAlign = 'center'; tr.textBaseline = 'alphabetic'; tr.fillStyle = '#4a2410'; tr.fillText(text, x, y); tr.restore();
}

// ---------- scene ----------
const lampDim = t => 1 - .78 * E(t, 14.2, 16.6) * (1 - E(t, 19.6, 21.4));
const pulling = t => t >= T.pull && t < 24 ? Math.sin((t - T.pull) * 2 * Math.PI / 1.7) : 0;
function drawScene(t) {
  SA = 1 - .96 * E(t, 19.4, 20.2) * (1 - E(t, 24.0, 25.2));
  tr.setTransform(1, 0, 0, 1, 0, 0); tr.globalCompositeOperation = 'source-over'; tr.globalAlpha = 1; tr.filter = 'none'; tr.fillStyle = '#fff'; tr.fillRect(0, 0, W, H);
  const pl = pulling(t), sway = Math.sin(t * 1.3) * 10;
  // mountain: appears sunk, then lifted by Kurma
  const lifted = E(t, T.lift, T.lift + 1.5);
  const mY = MREST + 190 * (1 - lifted) + (T.mount <= t ? 0 : 400), mRot = (1 - lifted) * .07 + (t > T.pull ? Math.sin((t - T.pull) * 2 * Math.PI / 1.7) * .012 : 0);
  const mp = press(t, T.mount, .6);
  if (t >= T.mount) put(A.mountain, 960, mY, { rot: mRot, sx: mp.sx * MS, sy: mp.sy * MS, a: mp.a, blur: mp.blur });
  // ratna icons in the sky (behind the pullers)
  for (const [key, text, t0, x, y, s] of RATNA) {
    if (t < t0) continue; const p = press(t, t0, .55), fl = t >= 44 ? 1 : 1;
    put(A.ratna[key], x, y + Math.sin(t * 1.7 + x) * 4, { sx: s * p.sx, sy: s * p.sy, a: p.a * fl, blur: p.blur, rot: Math.sin(t * 1.1 + x) * .02 });
    label(text, x, y + 118, E(t, t0 + .3, t0 + .9));
  }
  // Dhanvantari on the peak with the pot of amrit
  if (t >= T.crown) {
    const u = eo(seg(t, T.crown, T.crown + 1.4)), p = press(t, T.crown, .8);
    put(A.dhanv, 960, PEAK + 140 * (1 - u), { sx: .86 * p.sx, sy: .86 * p.sy, a: p.a, blur: p.blur, rot: Math.sin(t * 1.4) * .012 });
    const kT = E(t, T.amrit - .6, T.amrit + .5);
    put(A.kalash, 960 + 4, PEAK - 338 * .86 - 34 - 20 * kT + Math.sin(t * 3) * 2, { sx: 1.0 * kT, sy: 1.0 * kT, a: kT });
    label('धन्वंतरि', 960, PEAK + 64, E(t, T.crown + .8, T.crown + 1.3) * 0);
  }
  // sea, shores
  put(A.sea, 960 + Math.sin(t * .9) * 26, GROUND, {}); put(A.sea, 960 - 90 + Math.sin(t * .7 + 1) * 34, GROUND + 70, { a: .9 });
  put(A.shore, 280, GROUND - 8, {}); put(A.shore, 1640, GROUND - 8, { flip: -1 });
  // Kurma under the mountain
  if (t >= T.kurma) { const p = press(t, T.kurma, .6); put(A.kurma, 960, GROUND + 14 + (1 - lifted) * 50, { sx: p.sx * 1.45, sy: p.sy * 1.45, a: p.a, blur: p.blur, rot: Math.sin(t * 1.2) * .01 }); }
  // serpent: slides in, coils, then the rope is pulled
  if (t >= T.snake) {
    const u = eo(seg(t, T.snake, T.snake + 1.2)), shift = -pl * 22;
    for (const [dy, r] of [[-30, .035], [30, -.035]]) put(A.wrap, 960, ROPE + dy, { rot: r, a: u, sx: .78, sy: .8 });
    put(A.serpent, 960 + shift + (1 - u) * 1100, ROPE, { rot: Math.sin(t * 1.9) * .004 });
  }
  // pullers
  const bob = Math.abs(Math.sin(t * 5));
  DEVA_X.forEach((x, i) => {
    const e = ss(seg(t, 2.0 + i * .18, 4.1 + i * .18)); if (e <= 0) return;
    const lean = pl * -.09; const walk = e < 1 ? bob * 6 : 0;
    put(A.deva, x - (1 - e) * 800 - pl * 14, GROUND - walk, { rot: lean, sx: 1.15, sy: 1.15 });
  });
  ASURA_X.forEach((x, i) => {
    const e = ss(seg(t, 2.1 + i * .18, 4.2 + i * .18)); if (e <= 0) return;
    const lean = -pl * -.09; const walk = e < 1 ? bob * 6 : 0;
    put(A.asura, x + (1 - e) * 800 - pl * 14, GROUND - walk, { rot: -lean, sx: 1.2, sy: 1.2, flip: -1 });
  });
  // title plaque
  if (t < 5.3) {
    const ti = press(t, T.titleIn, .6), to = lift(t, T.titleOut, .9), pin = t < T.titleOut;
    const q = pin ? ti : to; put(A.title, 960, 330, { sx: q.sx, sy: q.sy, a: q.a, blur: q.blur });
  }
  // Halahala smoke, Shiva
  smoke(t);
  if (t >= T.shiva && t < 25.6) {
    const p = t < T.shivaOut ? press(t, T.shiva, .7) : lift(t, T.shivaOut, 1);
    put(A.shiva, 960, 830, { sx: 1.5 * p.sx, sy: 1.5 * p.sy, a: p.a, blur: p.blur, rot: Math.sin(t * 1.5) * .008, free: true });
    const bl = E(t, T.throat, T.throat + .8) * (t < T.shivaOut ? 1 : p.a);
    put(A.spot, 960 + 4 * 1.5 * 1 + 6, 830 - 306 * 1.5, { sx: 1.4, sy: 1.8, a: bl * .95, free: true });
  }
}
function smoke(t) {
  const c1 = eo(seg(t, T.poison, T.dark)), c2 = 1 - ss(seg(t, T.shiva + .3, T.smokeGone));
  if (t < T.poison || c2 <= 0.01) return;
  const M = [1005, 830 - 340 * 1.5];
  for (let k = 0; k < 13; k++) {
    const ang = -Math.PI * (.05 + .9 * hash(k * 3 + 1)), dist = 380 + 800 * hash(k * 5 + 2), R = 190 + 230 * hash(k * 7 + 3);
    const bx = 960 + Math.cos(ang) * dist * c1, by = 760 + Math.sin(ang) * dist * .75 * c1;
    const x = lerp(M[0], bx, c2), y = lerp(M[1], by, c2), s = (R / 200) * (.25 + .75 * c1) * (.15 + .85 * c2) * .95;
    put(A.puff, x, y + Math.sin(t * 2 + k) * 8, { sx: s, sy: s, a: .85, rot: k, free: true });
  }
}

// ---------- lamps ----------
function lamps(t) {
  const out = [], dim = lampDim(t);
  const carry = ss(seg(t, T.carry0, T.carry1)), end = 1 - ss(seg(t, 52.6, 53.8));
  out.push([lerp(960, 2500, carry * carry), 540, (.9 + .1 * Math.sin(t * 7)) * dim * (t < 1.0 ? E(t, .3, 1.0) : 1) * (t >= T.carry0 ? 1 : 1), .95]);
  RATNA.forEach(([, , t0, x, y, , lamp], i) => {
    if (!lamp || t < t0) return;
    const u = back(seg(t, t0, t0 + .5), 2.2), off = 1 - ss(seg(t, T.carry0 + i * .16, T.carry0 + i * .16 + .5));
    out.push([x, y, .4 * u * dim * off, .9]);
  });
  if (t >= T.crown) { const u = back(seg(t, T.crown, T.crown + .7), 2.4), off = 1 - ss(seg(t, T.carry0 + 1.8, T.carry0 + 2.4)); out.push([960, 230, .8 * u * off, .95]); }
  return out.map(l => [l[0], l[1], l[2] * end, l[3]]);
}

// ---------- front layer: frame, audience, captions ----------
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function drawCap(text, a, slide) {
  fr.save(); fr.setTransform(1, 0, 0, 1, 0, 0); fr.globalAlpha = a; fr.font = `600 46px "Noto Serif Devanagari"`;
  const tw = fr.measureText(text).width, seal = 52, w = 28 + seal + 22 + tw + 40, h = 92, x = 960 - w / 2, y = 1080 - 40 - h + slide * 18;
  fr.shadowColor = 'rgba(0,0,0,.55)'; fr.shadowBlur = 18; fr.shadowOffsetY = 4;
  const gr = fr.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, 'rgba(46,22,14,.94)'); gr.addColorStop(1, 'rgba(22,10,7,.94)');
  fr.fillStyle = gr; rr(fr, x, y, w, h, 6); fr.fill(); fr.shadowColor = 'transparent';
  fr.strokeStyle = 'rgba(168,129,63,.8)'; fr.lineWidth = 1.5; rr(fr, x + 6, y + 6, w - 12, h - 12, 3); fr.stroke();
  const sx = x + 28, sy = y + (h - seal) / 2; fr.fillStyle = '#b3261b'; rr(fr, sx, sy, seal, seal, 4); fr.fill();
  fr.strokeStyle = 'rgba(255,220,190,.55)'; fr.lineWidth = 1.2; rr(fr, sx + 4, sy + 4, seal - 8, seal - 8, 2); fr.stroke();
  fr.font = `700 25px "Noto Serif Devanagari"`; fr.fillStyle = '#f6dcc0'; fr.textAlign = 'center'; fr.textBaseline = 'alphabetic'; fr.fillText('कथा', sx + seal / 2, sy + seal / 2 + 9);
  fr.font = `600 46px "Noto Serif Devanagari"`; fr.fillStyle = '#f3e2bf'; fr.textAlign = 'left'; fr.fillText(text, sx + seal + 22, y + h / 2 + 17);
  fr.restore();
}

function render(t) {
  fr.setTransform(1, 0, 0, 1, 0, 0); fr.clearRect(0, 0, W, H); fr.globalAlpha = 1; fr.filter = 'none';
  const cam = camAt(t); C = camM(cam);
  drawScene(t);
  const L = lamps(t), nEff = L.reduce((a, l) => a + l[2], 0);
  if (cam[2] < 1.02) drawFrame(fr, C, clamp(nEff, 0, 3) / 1.5);
  const aud = t < 4.6 ? 1 - E(t, 3.8, 4.6) : E(t, 44.5, 46.5) * .9; if (aud > 0) drawAudience(fr, aud, t);
  if (!qs.get('nosub')) for (const s of CAPS) if (t >= s.t0 && t < s.t1) { const a = Math.min(E(t, s.t0, s.t0 + .2), 1 - E(t, s.t1 - .25, s.t1)); drawCap(s.text, a, 1 - eo(seg(t, s.t0, s.t0 + .22))); }
  const expo = 1.5 / Math.sqrt(Math.max(1, nEff));
  GL.render(trc, frc, { lamps: L, cam, sigB: 700, sigC: 120, amb: .3, expo, time: t, vign: .45, sat: 1.1, contrast: .15, bloom: .28 + .2 * clamp((nEff - 1) / 8, 0, 1) });
}

// ---------- sound cues for the mixer ----------
function events() {
  const ev = [], add = (type, t, o = {}) => ev.push({ type, t: +t.toFixed(3), ...o });
  add('drum', T.titleIn + .1, { v: 1 }); add('gong', T.titleIn + .1, { v: .8 });
  add('lift', T.titleOut); add('drum', T.mount, { v: .8 }); add('lift', T.snake, { v: .6 }); add('drum', T.kurma, { v: .9 }); add('gong', T.kurma, { v: .6 });
  for (let k = 0; k < 7; k++) add('pull', T.pull + k * 1.7, { v: .7 });
  for (let k = 0; k < 12; k++) add('heart', T.poison + 0.2 + k * .62, { v: .5 + (k % 2) * .3 });
  add('gong', T.poison, { v: 1 }); add('gong', T.dark, { v: .8 });
  add('gong', T.shiva, { v: .7 }); add('drum', T.drink, { v: .6 }); add('gulp', T.drink + 1.0); add('gulp', T.drink + 1.5); add('gong', T.throat, { v: 1 });
  add('lift', T.shivaOut, { v: .6 });
  RATNA.forEach(([, , t0], i) => { add('tick', t0, { i }); add('drum', t0, { v: .5 }); });
  add('gong', T.crown, { v: 1 }); add('chime', T.amrit); add('drum', T.crown, { v: .9 });
  add('lift', T.carry0, { v: .7 }); add('gong', 53.0, { v: .6 });
  ev.push({ type: 'vo', t: OFF });
  return ev.sort((a, b) => a.t - b.t);
}
window.EV = events(); window.T = T; window.DUR = DUR; window.render = render;
render(parseFloat(qs.get('t') ?? '15'));
window.READY = true;

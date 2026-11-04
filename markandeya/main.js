// Markandeya: the boy who made Yama stop. Shadow Puppetry. Hook first. Timeline = one source of truth (picture, captions, sound cues)
import { makeGL } from './gl.js';
import { canvas, drawPiece } from './carve.js';
import { clamp, lerp, seg, ss, eo, eio, back, hash } from '/core/lib.js';
import { drawFrame, drawAudience } from './stage.js';
import { buildArt } from './art.js';

const qs = new URLSearchParams(location.search);
const W = 1920, H = 1080;
const [trc, tr] = canvas(W, H), [frc, fr] = canvas(W, H);
const GL = makeGL(document.getElementById('gl'));
for (const w of ['600', '700']) await document.fonts.load(`${w} 40px "Noto Serif Devanagari"`, 'मार्कंडेय कालांतक १६ वर्ष');
const A = buildArt();
const E = (t, a, b) => ss(seg(t, a, b));

// ---------- timeline (film seconds; the voice-over starts at OFF) ----------
const OFF = 1.0, DUR = 56;
const CAPS = [   // [voice start, voice end, text]
  [0.00, 5.77, 'क्या आप जानते हैं, एक बालक की भक्ति के आगे मृत्यु के देवता यम को भी रुकना पड़ा था?'],
  [6.24, 9.25, 'और उसे बचाने के लिए, स्वयं शिव प्रकट हुए।'],
  [10.05, 14.01, 'ऋषि मृकंडु के पुत्र मार्कंडेय की आयु केवल सोलह वर्ष थी,'],
  [14.55, 16.77, 'यह उन्हें जन्म से पहले ही बता दिया गया था।'],
  [17.39, 22.24, 'जब सोलहवाँ वर्ष आया, वे शिवलिंग को कसकर थामकर पूजा में बैठ गए।'],
  [22.78, 27.82, 'यम के दूत उन्हें ले जा न सके, तब यम स्वयं आए और उन्होंने अपना पाश फेंका।'],
  [28.32, 31.11, 'वह पाश बालक के साथ शिवलिंग पर भी जा गिरा।'],
  [31.61, 36.07, 'तभी शिवलिंग से शिव प्रकट हुए, और उन्होंने यम को पीछे हटा दिया।'],
  [36.53, 38.80, 'इसी कारण शिव कालांतक कहलाए,'],
  [39.19, 41.31, 'यानी काल का अंत करने वाले।'],
  [41.88, 45.66, 'शिव ने मार्कंडेय को सदा सोलह वर्ष का रहने का वरदान दिया।'],
  [46.16, 50.14, 'कहते हैं, अटूट भक्ति के आगे काल को भी झुकना पड़ता है।']
].map(([a, b, text]) => ({ t0: a + OFF, t1: b + OFF + .3, text }));
window.SUBS = CAPS;

const T = {
  yamaIn: .3, flashIn: 10.8, flashOut: 18.0, hut: 11.0, num: 12.6, glass: 16.0, boyRun: 18.4, yamaBack: 25.0, dutas: 24.0, throw0: 28.0, throw1: 29.3,
  shiva: 32.7, yamaOut: 33.2, snap: 33.5, kal: 38.0, glassOut: 40.5, boon: 43.0, bow: 47.4, carry0: 51.0, carry1: 54.0, end: 52.2
};
const GROUND = 790, LX = 960;
// ---------- camera ----------
const kick = (t, t0, a = .1) => t >= t0 ? a * Math.max(0, 1 - (t - t0) / .28) : 0;
function camAt(t) {
  const L = (a, b, u) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)];
  let c = [960, 540, 1];
  if (t < 7.3) c = L([960, 560, 1], [1010, 540, 1.14], eio(seg(t, 0, 7.3)));
  else if (t < 10.8) c = L([1010, 540, 1.14], [960, 640, 1.5], eio(seg(t, 7.3, 10.2)));
  else if (t < 18.0) c = [960, 560, 1];
  else if (t < 19.2) c = L([960, 560, 1], [940, 600, 1.2], eio(seg(t, 18, 19.2)));
  else if (t < 23.5) c = [940, 600, 1.2];
  else if (t < 25.0) c = L([940, 600, 1.2], [1020, 560, 1], eio(seg(t, 23.5, 25)));
  else if (t < 28.0) c = [1020, 560, 1];
  else if (t < 30.5) c = L([1020, 560, 1], [960, 620, 1.55], eio(seg(t, 28, 29.4)));
  else if (t < 32.4) c = [960, 620, 1.55];
  else if (t < 34.5) c = L([960, 620, 1.55], [960, 500, 1.0], eio(seg(t, 32.6, 34.5)));
  else if (t < 43) c = [960, 520, 1];
  else if (t < 46) c = L([960, 520, 1], [900, 540, 1.12], eio(seg(t, 43, 46)));
  else c = L([900, 540, 1.12], [960, 540, .86], eio(seg(t, 46.5, 49.5)));
  c = [c[0], c[1], c[2] * (1 + kick(t, T.shiva, .14) + kick(t, T.snap, .08) + kick(t, 7.2, .07))];
  if (c[2] >= 1) { c[0] = clamp(c[0], 960 / c[2], 1920 - 960 / c[2]); c[1] = clamp(c[1], 540 / c[2], 1080 - 540 / c[2]); }
  return c;
}
const camM = ([cx, cy, z]) => [z, 0, 0, z, 960 - cx * z, 540 - cy * z];
let C = camM([960, 540, 1]), GA = 1, GB = 0;

// ---------- helpers ----------
function put(p, x, y, o = {}) {
  const { rot = 0, sx = 1, sy = 1, blur = 0, flip = 1, grp = 'A' } = o;
  const a = (o.a ?? 1) * (grp === 'A' ? GA : grp === 'B' ? GB : 1);
  if (a <= 0.01) return;
  tr.save(); tr.setTransform(C[0], C[1], C[2], C[3], C[4], C[5]); tr.translate(x, y); tr.rotate(rot); tr.scale(sx * flip, sy);
  tr.globalCompositeOperation = 'multiply'; tr.globalAlpha = a; if (blur > .4) tr.filter = `blur(${blur}px)`;
  drawPiece(tr, p); tr.restore();
}
const press = (t, t0, d = .5) => { const u = eo(seg(t, t0, t0 + d)); return { sx: 1 + (1 - u) * .55, sy: 1 + (1 - u) * .55, blur: (1 - u) * 18, a: Math.min(1, u * 2.2) }; };
const lift = (t, t0, d = .9) => { const u = ss(seg(t, t0, t0 + d)); return { sx: 1 + u * .45, sy: 1 + u * .45, blur: u * 20, a: 1 - u }; };
function rope(x0, y0, x1, y1, sag, a = 1) {
  tr.save(); tr.setTransform(C[0], C[1], C[2], C[3], C[4], C[5]); tr.globalCompositeOperation = 'multiply'; tr.globalAlpha = a * GA;
  tr.strokeStyle = '#4a2a14'; tr.lineWidth = 7; tr.lineCap = 'round'; tr.beginPath(); tr.moveTo(x0, y0); tr.quadraticCurveTo((x0 + x1) / 2, (y0 + y1) / 2 + sag, x1, y1); tr.stroke(); tr.restore();
}

// ---------- scene ----------
const YS = 1.25, YX = 1480;
const yamaX = t => t < 9.6 ? YX + 0 : t < 10.8 ? YX + 900 * ss(seg(t, 9.6, 10.8)) : t < T.yamaBack ? YX + 900 : t < 26.6 ? lerp(YX + 900, YX, eo(seg(t, T.yamaBack, 26.6))) : t < T.yamaOut ? YX : lerp(YX, YX + 900, ss(seg(t, T.yamaOut, 35.2))) + 0;
const yamaBack = t => t >= 46.4 ? E(t, 46.4, 47.4) : 0;
function drawScene(t) {
  GA = (1 - E(t, 10.5, 11.1) * (1 - E(t, 17.9, 18.5)));
  GB = E(t, 10.8, 11.4) * (1 - E(t, 17.6, 18.2));
  tr.setTransform(1, 0, 0, 1, 0, 0); tr.globalCompositeOperation = 'source-over'; tr.globalAlpha = 1; tr.filter = 'none'; tr.fillStyle = '#fff'; tr.fillRect(0, 0, W, H);
  for (const x of [420, 1260, 1900]) put(A.shore, x, GROUND + 10, { grp: 'x' });
  // —— group B: the flashback (hut, boy, the number 16, the glass of time) ——
  if (GB > .01) {
    put(A.hut, 420, GROUND, { sx: 1.5, sy: 1.5, grp: 'B' });
    const pb = press(t, T.hut, .5);
    put(A.boyPray, 760, GROUND, { sx: 1.7 * pb.sx, sy: 1.7 * pb.sy, a: pb.a, blur: pb.blur, grp: 'B', rot: Math.sin(t * 1.3) * .01 });
    if (t >= T.num) { const p = t < 17 ? press(t, T.num, .6) : lift(t, 17.2, .7); put(A.num, 1360, 360, { sx: p.sx * .95, sy: p.sy * .95, a: p.a, blur: p.blur, grp: 'B' }); }
    if (t >= T.glass) { const p = press(t, T.glass, .6), sp = Math.sin(t * 2) * .02; put(A.hourglass, 1000, 560, { sx: 2.3 * p.sx, sy: 2.3 * p.sy, a: p.a, blur: p.blur, rot: sp, grp: 'B' }); }
  }
  // —— group A: the shrine ——
  const ld = Math.sin(t * 9) * .004;
  put(A.linga, LX, GROUND, { sx: 1.25, sy: 1.25, rot: ld, grp: 'A' });
  // the boy: kneels at the linga, then clings to it
  const bp = t < 18.4 ? 0 : eo(seg(t, T.boyRun, T.boyRun + 1.1)), bx = lerp(700, LX - 125, t < 18.4 ? 1 : bp), shake = t > 24 && t < 32.4 ? Math.sin(t * 38) * 1.4 : 0;
  if (t < 10.5 || t >= 18.4) {
    const boyT = t >= 43.4 && t < 47 ? A.boyPray : t >= 43.4 ? A.boyPray : A.boyHug;
    const bxx = t >= 43.4 ? lerp(LX - 125, 640, ss(seg(t, 43.4, 44.6))) : (t < 18.4 ? LX - 125 : bx);
    put(boyT, bxx + shake, GROUND, { sx: 1.35, sy: 1.35, rot: t < 18.4 ? 0 : Math.sin(t * 1.4) * .006, grp: 'A' });
  }
  // Yama's messengers: tug, fail, fall back
  if (t >= T.dutas && t < 26.6) {
    const e = ss(seg(t, T.dutas, T.dutas + .8)), pull = Math.sin((t - T.dutas) * 9) * .5 + .5, fade = 1 - E(t, 25.8, 26.6);
    for (const [k, off] of [[0, 0], [1, 120]]) {
      const x0 = 340 + off - (1 - e) * 500, x1 = 780 + off * .35;
      put(A.asura, x0 + pull * 18 * (k ? -1 : 1) - 0, GROUND, { sx: .95, sy: .95, rot: -.05 - pull * .08, a: fade, grp: 'A' });
      rope(x0 + 86, GROUND - 175, bx0(t) + 20, GROUND - 120, 24, fade);
    }
  }
  // Yama on his buffalo, noose raised
  const px = yamaX(t), ys = YS * (t < 7 ? 1 + .12 * E(t, 0, 7) : 1);
  const showYama = t < 10.9 || (t >= T.yamaBack && t < 37);
  if (showYama) {
    const ent = t < 3 ? ss(seg(t, T.yamaIn, 2.4)) : 1, ex = (1 - ent) * 700;
    const bow = t > 46 ? 0 : 0;
    const hurt = t >= T.shiva ? E(t, T.shiva, T.shiva + 1.4) : 0;
    put(A.yama, px + ex, GROUND, { sx: ys, sy: ys, rot: -hurt * .12 + Math.sin(t * 1.6) * .006, blur: t >= T.shiva ? hurt * 6 : 0, grp: 'A', a: t >= 35 ? 1 - E(t, 34.6, 36.2) : 1 });
    // the noose in his hand, swinging; flies at the boy
    const hx = px + ex - 62 * ys, hy = GROUND - 345 * ys;
    if (t < T.throw0 && t < 10.9 || (t >= T.yamaBack && t < T.throw0)) put(A.noose, hx, hy + 30, { sx: .6, sy: .6, rot: Math.sin(t * 2.2) * .35 + .3, grp: 'A' });
    else if (t >= T.throw0 && t < T.throw1) { const u = eo(seg(t, T.throw0, T.throw1)); put(A.noose, lerp(hx, LX, u), lerp(hy, GROUND - 140, u) - Math.sin(Math.PI * u) * 120, { sx: lerp(.6, 3.3, u), sy: lerp(.6, 1.8, u), rot: u * 7, grp: 'A' }); }
  }
  // the noose lies round boy and linga until Shiva breaks it
  if (t >= T.throw1 && t < 35) {
    const snap = t >= T.snap ? ss(seg(t, T.snap, T.snap + 1)) : 0;
    put(A.noose, LX - snap * 60, GROUND - 140 + snap * 140, { sx: 3.3, sy: 1.8, rot: -snap * .6, a: 1 - snap, grp: 'A' });
    if (t >= T.snap) put(A.noose, LX + snap * 70, GROUND - 140 + snap * 160, { sx: 3.3, sy: 1.8, rot: snap * .7, a: 1 - snap, grp: 'A' });
  }
  // Shiva: out of the linga
  if (t >= T.shiva) {
    const bowl = t >= T.boon ? -1 : 1, p = press(t, T.shiva, .8), u = eo(seg(t, T.shiva, T.shiva + 1.2)), sc = 1.5 * (.7 + .3 * u);
    const lf = t >= 51.4 ? lift(t, 51.4, 1.4) : { sx: 1, sy: 1, a: 1, blur: 0 };
    put(A.aura, LX + (bowl < 0 ? 40 : 0), GROUND - 560, { sx: p.sx * .95, sy: p.sy * .95, a: .85 * p.a * lf.a, blur: p.blur, rot: t * .12, grp: 'x' });
    put(A.shiva, LX + (bowl < 0 ? 30 : -10), GROUND + 10, { sx: sc * p.sx * lf.sx, sy: sc * p.sy * lf.sy, a: p.a * lf.a, blur: p.blur + lf.blur, flip: bowl, rot: Math.sin(t * 1.5) * .008, grp: 'x' });
  }
  if (t >= T.kal && t < 42.4) { const p = t < 41.4 ? press(t, T.kal, .6) : lift(t, 41.4, .8); put(A.kal, 560, 190, { sx: .8 * p.sx, sy: .8 * p.sy, a: p.a, blur: p.blur, grp: 'x' }); }
  if (t >= T.kal + 2.4 && t < T.boon + 3.2) { const p = t < T.glassOut ? press(t, T.kal + 2.4, .5) : lift(t, T.glassOut, .7); put(A.hourglass, 1420, 600, { sx: 1.6 * p.sx, sy: 1.6 * p.sy, a: p.a, blur: p.blur, rot: -.2 * E(t, T.glassOut, T.glassOut + 1), grp: 'x' }); }
  if (t >= T.boon + .2 && t < 50.4) { const p = t < 49.6 ? press(t, T.boon + .2, .6) : lift(t, 49.6, .7); put(A.num, 1500, 300, { sx: .85 * p.sx, sy: .85 * p.sy, a: p.a, blur: p.blur, grp: 'x' }); }
  // Yama returns and bows
  if (t >= 46.4 && t < 51.4) { const u = yamaBack(t); put(A.yama, lerp(2300, 1560, eo(seg(t, 46.4, 47.6))), GROUND, { sx: YS * .95, sy: YS * .95, rot: u > 0 ? -.12 * ss(seg(t, 47.8, 48.8)) : 0, grp: 'x', a: 1 - E(t, 50.6, 51.4) }); }
  // end plaque
  if (t >= T.end) { const p = press(t, T.end, .8); put(A.end, 960, 400, { sx: p.sx, sy: p.sy, a: p.a, blur: p.blur, grp: 'x' }); }
}
const bx0 = t => t < 18.4 ? 700 : LX - 125;

// ---------- lamps ----------
function lamps(t) {
  const out = [], carry = ss(seg(t, T.carry0, T.carry1)), end = 1 - ss(seg(t, 54, 55.6));
  const dread = 1 - .35 * E(t, 18, 24) * (1 - E(t, T.shiva, T.shiva + .6));
  out.push([lerp(960, 2500, carry * carry), 440, (.95 + .08 * Math.sin(t * 7)) * (t < .8 ? E(t, 0, .8) * .9 + .1 : 1) * dread, .95]);
  out.push([LX, GROUND - 140, (.25 + .5 * E(t, 18.4, 30)) * (t < 11 || t > 17.5 ? 1 : .4), .9]);
  if (t >= T.shiva) { const u = back(seg(t, T.shiva, T.shiva + .7), 2.4); out.push([960, 330, .8 * u, .95]); out.push([520, 520, .3 * u, .9]); out.push([1400, 520, .3 * u, .9]); }
  const off = 1 - E(t, T.carry0 + 1, T.carry0 + 2.4);
  return out.map((l, i) => [l[0], l[1], l[2] * end * (i > 1 ? off : 1), l[3]]);
}

// ---------- front layer ----------
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function drawCap(text, a, slide) {
  fr.save(); fr.setTransform(1, 0, 0, 1, 0, 0); fr.globalAlpha = a;
  let fs = 46; fr.font = `600 ${fs}px "Noto Serif Devanagari"`; let tw = fr.measureText(text).width;
  if (tw > 1500) { fs = 40; fr.font = `600 ${fs}px "Noto Serif Devanagari"`; tw = fr.measureText(text).width; }
  const seal = 52, w = 28 + seal + 22 + tw + 40, h = 92, x = 960 - w / 2, y = 1080 - 40 - h + slide * 18;
  fr.shadowColor = 'rgba(0,0,0,.55)'; fr.shadowBlur = 18; fr.shadowOffsetY = 4;
  const gr = fr.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, 'rgba(46,22,14,.94)'); gr.addColorStop(1, 'rgba(22,10,7,.94)');
  fr.fillStyle = gr; rr(fr, x, y, w, h, 6); fr.fill(); fr.shadowColor = 'transparent';
  fr.strokeStyle = 'rgba(168,129,63,.8)'; fr.lineWidth = 1.5; rr(fr, x + 6, y + 6, w - 12, h - 12, 3); fr.stroke();
  const sx = x + 28, sy = y + (h - seal) / 2; fr.fillStyle = '#b3261b'; rr(fr, sx, sy, seal, seal, 4); fr.fill();
  fr.strokeStyle = 'rgba(255,220,190,.55)'; fr.lineWidth = 1.2; rr(fr, sx + 4, sy + 4, seal - 8, seal - 8, 2); fr.stroke();
  fr.font = `700 25px "Noto Serif Devanagari"`; fr.fillStyle = '#f6dcc0'; fr.textAlign = 'center'; fr.textBaseline = 'alphabetic'; fr.fillText('कथा', sx + seal / 2, sy + seal / 2 + 9);
  fr.font = `600 ${fs}px "Noto Serif Devanagari"`; fr.fillStyle = '#f3e2bf'; fr.textAlign = 'left'; fr.fillText(text, sx + seal + 22, y + h / 2 + 17);
  fr.restore();
}
function render(t) {
  fr.setTransform(1, 0, 0, 1, 0, 0); fr.clearRect(0, 0, W, H); fr.globalAlpha = 1; fr.filter = 'none';
  const cam = camAt(t); C = camM(cam);
  drawScene(t);
  const L = lamps(t), nEff = L.reduce((a, l) => a + l[2], 0);
  if (cam[2] < 1.02) drawFrame(fr, C, clamp(nEff, 0, 3) / 1.5);
  const aud = t < 1.2 ? 0 : E(t, 47.6, 49.6) * .9; if (aud > 0) drawAudience(fr, aud, t);
  if (!qs.get('nosub')) for (const s of CAPS) if (t >= s.t0 && t < s.t1) { const a = Math.min(E(t, s.t0, s.t0 + .2), 1 - E(t, s.t1 - .25, s.t1)); drawCap(s.text, a, 1 - eo(seg(t, s.t0, s.t0 + .22))); }
  // colour of the light: ominous red-ochre during the hook and the threat, warm gold once Shiva appears
  const warm = E(t, T.shiva - .1, T.shiva + .8), lcol = [1, lerp(.55, .77, warm), lerp(.32, .46, warm)], hot = [1, lerp(.68, .9, warm), lerp(.4, .62, warm)];
  GL.render(trc, frc, { lamps: L, cam, sigB: 700, sigC: 120, amb: .3, expo: 1.6 / Math.sqrt(Math.max(1, nEff)), time: t, vign: .5, sat: 1.1, contrast: .16, bloom: .28 + .2 * clamp((nEff - 1) / 4, 0, 1), lcol, hotcol: hot });
}

// ---------- sound cues ----------
function events() {
  const ev = [], add = (type, t, o = {}) => ev.push({ type, t: +t.toFixed(3), ...o });
  add('drum', .35, { v: 1 }); add('gong', .35, { v: .8 }); add('lift', 9.7, { v: .6 }); add('heart', 6.9, { v: .6 });
  add('drum', 7.1, { v: .9 }); add('gong', 7.1, { v: .6 });
  add('lift', T.flashIn, { v: .5 }); add('tick', T.hut, { i: 0 }); add('drum', T.num, { v: .7 }); add('tick', T.num, { i: 2 }); add('tick', T.glass, { i: 4 });
  for (let k = 0; k < 6; k++) add('heart', 19.5 + k * .7, { v: .5 + (k % 2) * .3 });
  add('drum', T.boyRun, { v: .6 });
  for (let k = 0; k < 7; k++) add('pull', T.dutas + .3 + k * .62, { v: .6 });
  add('gong', T.dutas, { v: .6 }); add('drum', T.yamaBack + .6, { v: .9 }); add('gong', T.yamaBack + .6, { v: .8 });
  add('lift', T.throw0, { v: .9 }); add('drum', T.throw1, { v: 1 });
  for (let k = 0; k < 8; k++) add('heart', 29.4 + k * .4, { v: .7 + (k % 2) * .3 });
  add('gong', T.shiva, { v: 1 }); add('drum', T.shiva, { v: 1 }); add('snap', T.snap); add('lift', T.yamaOut, { v: .8 });
  add('tick', T.kal, { i: 6 }); add('gong', T.kal, { v: .7 }); add('lift', T.glassOut, { v: .5 });
  add('chime', T.boon); add('tick', T.boon + .2, { i: 7 });
  add('lift', T.bow, { v: .5 }); add('gong', T.end, { v: .8 }); add('gong', 54.2, { v: .5 });
  ev.push({ type: 'vo', t: OFF });
  return ev.sort((a, b) => a.t - b.t);
}
window.EV = events(); window.T = T; window.DUR = DUR; window.render = render;
render(parseFloat(qs.get('t') ?? '15'));
window.READY = true;

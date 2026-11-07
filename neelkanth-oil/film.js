// Neelkanth (oil painting / palette knife). Sea of milk churned -> Halahala rises -> gods run -> they pray to Shiva -> he drinks it,
// Parvati holds his throat -> blue throat -> water poured on the linga. All timing is in "tn" = seconds of the final film (voice-over starts at 1.0 s).
import { Impasto, Strokes, hex, KNIFE, DAB } from './engine/impasto.js';
import { strokePath } from './engine/plate.js';
import { SW, SH, GY, LX, buildDusk, buildLinga, buildShiva, buildText, LGW, LGH, LGX, LGY, SHW, SHH, SHX, SHY } from './scenes.js';
import { buildSea, buildMountain, buildRope, buildFigure, buildPoisonSky, MW, MH, MOX, MOY, RW, RH, PW, PH, PX, PY } from './scenes2.js';
import { GW, GH, GX, GY0, parvati } from './gods.js';
import { clamp, lerp, ss, seg, eo, eio, hash } from './common.js';

const W = 1920, H = 1080, OFFX = 96, OFFY = 54;
const mul = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1], A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3], A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
const TR = (x, y) => [1, 0, 0, 1, x, y], SC = (s, sy = s) => [s, 0, 0, sy, 0, 0], RO = a => [Math.cos(a), Math.sin(a), -Math.sin(a), Math.cos(a), 0, 0];
const E_ = (t, a, b) => ss(seg(t, a, b));
const OFF = 1.0, DURN = 80.0;
const CAPS = [
  [0.00, 4.30, 'शिव के 108 नामों में से आज हम जानेंगे: नीलकंठ।'],
  [4.95, 5.76, 'क्या आप जानते हैं,'],
  [6.15, 10.43, 'समुद्र मंथन में अमृत से पहले, सबसे पहले ज़हर निकला था?'],
  [11.26, 16.54, 'बहुत समय पहले, देवता और असुर अमृत पाने के लिए समुद्र मंथन कर रहे थे।'],
  [17.19, 19.14, 'मंदराचल पर्वत मथनी बना,'],
  [19.49, 21.17, 'और नाग वासुकि रस्सी।'],
  [21.76, 25.26, 'तभी समुद्र से निकला हलाहल नाम का भयंकर विष।'],
  [25.72, 29.23, 'कहा जाता है, उसकी ज्वाला से तीनों लोक जलने लगे।'],
  [29.73, 34.18, 'देवता घबरा गए, असुर भाग खड़े हुए, और कोई उसे सँभाल न सका।'],
  [34.70, 36.16, 'तब सबने शिव को पुकारा:'],
  [36.55, 38.34, 'महादेव, हमें बचाइए।'],
  [38.83, 41.82, 'शिव ने सृष्टि की रक्षा के लिए वह विष पी लिया।'],
  [42.34, 46.09, 'कुछ कथाओं के अनुसार, माता पार्वती ने उनका कंठ थाम लिया,'],
  [46.48, 47.78, 'और विष वहीं रुक गया।'],
  [48.31, 51.07, 'विष के प्रभाव से शिव का गला नीला पड़ गया।'],
  [51.56, 53.63, 'तभी से वे कहलाए, नीलकंठ।'],
  [54.08, 59.60, 'मान्यता है कि उस विष की गर्मी शांत करने के लिए ही शिवलिंग पर जल चढ़ाया जाता है।'],
  [60.28, 65.15, 'तो दोस्तों, शिव के 108 नामों में से आज हमने जाना: नीलकंठ,'],
  [65.49, 67.58, 'यानी जिनका कंठ नीला है।'],
  [68.09, 74.96, 'पूरी कथा विस्तार से जानने के लिए, यूट्यूब चैनल पर पूरा वीडियो देखिए, और चैनल को सब्सक्राइब ज़रूर कीजिए।'],
  [75.44, 76.93, 'हर हर महादेव।']
].map(([a, b, text]) => ({ t0: a + OFF, t1: b + OFF + .3, text }));

// camera keyframes: [tn, x, y, zoom] (world centre; OFFX/OFFY added)
const KF = [[0, 1056, 600, 1], [6, 1090, 560, 1.1], [11.2, 1056, 600, 1], [12.2, 1056, 600, 1], [18, 1056, 560, 1.12], [19.6, 1056, 560, 1.12], [20.8, 1500, 640, 1.45], [22.6, 1700, 600, 1.5],
  [24, 1056, 600, 1.0], [28, 1056, 560, 1.2], [30.7, 1056, 640, 1.0], [35.2, 1056, 620, 1.0], [35.7, 1056, 600, 1.0], [38.5, 1056, 600, 1.05], [39.8, 1010, 560, 1.15], [41.8, 1000, 440, 1.8], [47.5, 1000, 430, 1.8],
  [49, 1000, 400, 2.0], [53, 1000, 400, 2.2], [54.6, 1010, 420, 1.9], [55.4, 1056, 640, 1.1], [60.6, 1056, 600, 1.0], [66, 1056, 560, .92], [90, 1056, 560, .92]];
function camAt(t) {
  let i = 0; while (i < KF.length - 2 && t > KF[i + 1][0]) i++;
  const [a, b] = [KF[i], KF[i + 1]], u = eio(seg(t, a[0], b[0]));
  let x = lerp(a[1], b[1], u), y = lerp(a[2], b[2], u), z = lerp(a[3], b[3], u);
  if (t >= 22.8 && t < 35) { x += Math.sin(t * 31) * 3 * E_(t, 22.8, 24); y += Math.cos(t * 27) * 3 * E_(t, 22.8, 24); }
  x += OFFX; y += OFFY; const hx = W / 2 / z, hy = H / 2 / z;
  return { x: clamp(x, hx, SW - hx), y: clamp(y, hy, SH - hy), zoom: z };
}

let E, P = {}, dyn, capEl;
const up = (built, w, h, ox = 0, oy = 0) => ({ b: E.batch(built.strokes.data()), tex: E.texture(built.ref.ctx.canvas), w, h, ox, oy });
export async function setup(canvas) {
  for (const w of ['600', '700']) await document.fonts.load(`${w} 40px "Noto Serif Devanagari"`, 'नीलकंठ हलाहल शिव के १०८ नामों');
  E = new Impasto(canvas, { W, H, ss: +(new URLSearchParams(location.search).get('ss') || 1) }); dyn = new Strokes(8192);
  P.dusk = up(buildDusk(), SW, SH); P.sea = up(buildSea(), SW, SH); P.pois = up(buildPoisonSky(), SW, SH);
  P.mtn = up(buildMountain(), MW, MH, MOX, MOY); P.rope = up(buildRope(), RW, RH);
  P.dPull = up(buildFigure('deva', 'pull'), PW, PH, PX, PY); P.aPull = up(buildFigure('asura', 'pull'), PW, PH, PX, PY);
  P.dPray = up(buildFigure('deva', 'pray'), PW, PH, PX, PY); P.aPray = up(buildFigure('asura', 'pray'), PW, PH, PX, PY);
  P.linga = up(buildLinga(), LGW, LGH, LGX, LGY); P.shiva = up(buildShiva(true), SHW, SHH, SHX, SHY); P.parv = up(parvati(), GW, GH, GX, GY0);
  P.open = up(buildText('नीलकंठ', 'जिनका कंठ नीला है', 1160, 380, 190, 60), 1160, 380);
  P.nil = up(buildText('नीलकंठ', 'जिनका कंठ नीला है', 980, 290, 160, 48), 980, 290);
  P.end2 = up(buildText('नीलकंठ', 'शिव के १०८ नामों में से', 1160, 380, 190, 60), 1160, 380);
  P.cta = up(buildText('पूरा वीडियो देखिए', 'यूट्यूब चैनल को सब्सक्राइब करें', 1160, 380, 120, 56), 1160, 380);
  P.hari = up(buildText('हर हर महादेव', 'शिव के १०८ नाम', 1160, 380, 150, 56), 1160, 380);
  for (const k in P) P[k].name = k;
  capEl = document.createElement('div');
  capEl.style.cssText = 'position:fixed;left:50%;bottom:38px;transform:translateX(-50%);max-width:1560px;text-align:center;font:600 44px/1.35 "Noto Serif Devanagari",serif;color:#fff4d6;background:rgba(30,12,60,.72);padding:10px 34px 14px;border-radius:12px;border:2px solid rgba(255,200,90,.7);opacity:0;white-space:normal';
  document.body.appendChild(capEl);
  window.DUR = DURN;
  return frame;
}
const SKIP = (new URLSearchParams(location.search).get('skip') || '').split(',');
function plate(pl, o) {
  if (SKIP.includes(pl.name)) return;
  const M = o.M || [1, 0, 0, 1, 0, 0], Mu = mul(M, TR(-pl.ox, -pl.oy));
  const inTrans = o.appear !== undefined && o.t < o.appear + (o.appDur ?? .5);
  const ua = o.appear === undefined ? 1 : seg(o.t, o.appear + (o.appDur ?? .5) * .55, o.appear + (o.appDur ?? .5));
  if (!o.noUnder && ua > 0) E.under(pl.tex, pl.w, pl.h, { ...o, M: Mu, alpha: (o.alpha ?? 1) * ua });
  E.draw(pl.b, { ...o, M: Mu, appear: inTrans ? o.appear : -1e6, appDur: .14 });
}
const flush = o => { if (dyn.n) E.drawNow(dyn.data(), o); dyn.clear(); };
const COLS = ['#ffd23a', '#ff7ab0', '#4fe0f0', '#ff9a2a', '#b080ff', '#7affb0'];
const PCOL = ['#0e1a1c', '#1c4a34', '#4a2a7a', '#102a3a', '#2a6a4a', '#5a1a6a'];
const BLUE = ['#1e3ad8', '#3a6af0', '#7ac0ff', '#2a1aa0', '#a8e0ff'];

// Shiva (feet at SH_X, SH_Y, scale SH_S) and the points we need on him
const SH_X = 976, SH_Y = 870, SH_S = .85;
const onShiva = (rx, ry) => [SH_X + rx * SH_S, SH_Y + ry * SH_S];
const PALM = onShiva(154, -586), MOUTH = onShiva(55, -566), THROAT = onShiva(8, -540), HEAD = onShiva(10, -600);

function orb(x, y, r, t, a, seed) {      // a ball of Halahala: dark knife strokes with an orange rim
  if (r < 2 || a <= 0) return;
  for (let k = 0; k < 26; k++) { const an = k / 26 * 6.283 + t * 1.3, rr = r * (.2 + .75 * hash(k * 3 + seed)); dyn.push({ x: x + Math.cos(an) * rr, y: y + Math.sin(an) * rr, ang: an + 1.2, len: r * .9, wid: r * .45, c: hex(PCOL[k % 6]), c2: hex(PCOL[(k + 2) % 6]), type: KNIFE, seed: k + seed, hgt: 1, alpha: a }); }
  for (let k = 0; k < 18; k++) { const an = k / 18 * 6.283 - t * 2.1; dyn.push({ x: x + Math.cos(an) * r * .98, y: y + Math.sin(an) * r * .98, ang: an + 1.57, len: r * .7, wid: r * .22, c: hex('#ff9a2a'), c2: hex('#ffe060'), type: KNIFE, seed: k + seed + 40, hgt: .8, alpha: a * .9 }); }
}

function frame(tn) {
  const t = tn, cam = camAt(tn), base = { t, cam, grey: 0, reveal: -1e6 };
  const seaA = E_(t, 10.9, 12.2) * (1 - E_(t, 34.8, 35.7));
  const isSea = seaA > .01, kail = seaA < .99;
  E.begin();
  plate(P.dusk, base);
  if (isSea) {
    plate(P.sea, { ...base, alpha: seaA });
    // rope (Vasuki), pullers, mountain
    const wob = Math.sin(t * 1.6) * .03;
    plate(P.rope, { ...base, alpha: seaA, M: TR(0, 551 - 140) });
    const flee = E_(t, 30.7, 34.8), recoil = E_(t, 25.8, 26.8) * (1 - E_(t, 30.0, 30.7));
    const fa = seaA * (1 - E_(t, 33.6, 34.8));
    const devx = [210, 340, 470, 600], asx = [1880, 1750, 1620, 1490];
    for (let k = 0; k < 4; k++) {
      const sw = Math.sin(t * 3.2 + k * .9) * .06;
      const ox = -flee * 900 - recoil * 18, ang = sw - recoil * .12 - flee * .1;
      plate(P.dPull, { ...base, alpha: fa, M: mul(TR(devx[k] + ox, 760 + (k % 2) * 8), mul(RO(ang), SC(1.1))) });
      const ax = asx[k] + flee * 900 + recoil * 18;
      plate(P.aPull, { ...base, alpha: fa, M: mul(TR(ax, 760 + (k % 2) * 8), mul(RO(-sw + recoil * .12 + flee * .1), SC(-1.1, 1.1))) });
    }
    plate(P.mtn, { ...base, alpha: seaA, M: mul(TR(1056, 724), RO(wob)) });
    // foam churned up around the mountain's foot
    for (let k = 0; k < 44; k++) { const a = k / 44 * 6.283 + t * (.5 + hash(k) * .4), rx = 250 + 80 * hash(k * 2), x = 1056 + Math.cos(a) * rx, y = 738 + Math.sin(a) * 26; if (Math.sin(a) < -.2) continue; dyn.push({ x, y, ang: Math.cos(a) * .4, len: 34 + 22 * hash(k * 3), wid: 10, c: hex(k % 3 ? '#e8fbff' : '#a8f0ff'), c2: hex('#ffffff'), type: DAB, seed: k, hgt: .5, alpha: seaA * .9 }); }
    flush({ ...base, run: 0 });
    // Halahala rises: the world darkens, a plume of black-green smoke and flame climbs out of the sea
    const pu = E_(t, 22.8, 27.2), wash = .26 * E_(t, 23.4, 26.6) * (1 - E_(t, 34.2, 35.6));
    if (wash > .01) plate(P.pois, { ...base, alpha: wash * seaA });
    if (pu > 0.01 && t < 35.7) {
      const fade = 1 - E_(t, 34.4, 35.6);
      for (let k = 0; k < 190; k++) {
        const age = (t * .22 + hash(k * 3)) % 1, hgt = 220 + 560 * pu, sp = 60 + 300 * age * pu;
        const x = 1056 + 40 + Math.sin(k * 7.3 + age * 5 + t) * sp * (.6 + hash(k)) * .9, y = 700 - age * hgt - 30 * hash(k * 5);
        dyn.push({ x, y, ang: -1.57 + Math.sin(k + t) * .6, len: 90 + 170 * age * pu, wid: 34 + 80 * age * pu, c: hex(PCOL[k % 6]), c2: hex(PCOL[(k + 3) % 6]), type: KNIFE, seed: k + 9, hgt: 1, alpha: pu * fade * (1 - age * .55) });
      }
      for (let k = 0; k < 110; k++) {     // flames licking round the base and sparks
        const age = (t * .7 + hash(k * 11)) % 1, x = 1056 + 40 + (hash(k * 13) - .5) * 520 * pu, y = 720 - age * (120 + 260 * pu * hash(k));
        dyn.push({ x, y, ang: -1.57 + Math.sin(k * 3 + t * 4) * .5, len: 50 + 110 * (1 - age) * pu, wid: 20 + 24 * (1 - age), c: hex('#ffe060'), c2: hex(k % 2 ? '#ff7a1a' : '#e02a1a'), type: DAB, seed: k + 300, hgt: .6, alpha: pu * fade * (1 - age) });
      }
      flush({ ...base, run: 0 });
    }
  }
  if (kail) {
    const ka = 1 - seaA, ent = t >= 34.9 ? E_(t, 35.2, 36.2) : E_(t, .2, 1.2);
    // devas and asuras, kneeling before Shiva
    if (t >= 34.9 && t < 43.4) {
      const pa = E_(t, 35.2, 35.9) * (1 - E_(t, 42.2, 43.3));
      [[470, 0], [590, 1], [710, 0]].forEach(([x, k]) => plate(P.dPray, { ...base, alpha: pa, M: mul(TR(x - (1 - pa) * 60, GY + 60 + k * 14), SC(1.25)) }));
      [[1500, 0], [1620, 1], [1740, 0]].forEach(([x, k]) => plate(P.aPray, { ...base, alpha: pa, M: mul(TR(x + (1 - pa) * 60, GY + 60 + k * 14), SC(-1.25, 1.25)) }));
    }
    // Shiva, with a halo of knife strokes
    const shA = ent * ka * (t >= 54.4 ? 1 - E_(t, 54.4, 55.2) : 1);
    if (shA > .01) {
      const hx = HEAD[0] + 4, hy = HEAD[1] + 10;
      for (let k = 0; k < 60; k++) { const an = k / 60 * 6.283 + t * .25, r = 300 + 10 * Math.sin(t * 3 + k); dyn.push({ x: hx + Math.cos(an) * r, y: hy + Math.sin(an) * r, ang: an + 1.57, len: 110, wid: 26, c: hex(COLS[k % 6]), c2: hex(COLS[(k + 2) % 6]), type: KNIFE, seed: k + 3, hgt: 1, alpha: shA * .85 }); }
      for (let k = 0; k < 40; k++) { const an = k / 40 * 6.283 - t * .3, r = 232; dyn.push({ x: hx + Math.cos(an) * r, y: hy + Math.sin(an) * r, ang: an + 1.57, len: 80, wid: 16, c: hex(COLS[(k + 3) % 6]), c2: hex('#fff4c0'), type: KNIFE, seed: k + 90, hgt: .8, alpha: shA * .8 }); }
      flush({ ...base, run: 0 });
      plate(P.shiva, { ...base, alpha: shA, M: mul(TR(SH_X, SH_Y), SC(SH_S)) });
      // the Halahala in his palm, lifted to the lips, swallowed
      if (t >= 39.8 && t < 42.9) {
        const g = E_(t, 39.8, 40.5), mv = E_(t, 40.9, 41.9), r = 46 * g * (1 - E_(t, 41.6, 42.0)), x = lerp(PALM[0], MOUTH[0], mv), y = lerp(PALM[1], MOUTH[1], mv) - 24 * (1 - g);
        orb(x, y, r, t, shA, 500);
      }
      // Parvati's hand on his throat; the poison held there
      if (t >= 43.2 && t < 49.6) {
        const pa = E_(t, 43.2, 44.0) * (1 - E_(t, 48.6, 49.6));
        const pr = 22 * E_(t, 42.2, 42.9) * (1 - E_(t, 48.0, 49.2)) * (1 + .1 * Math.sin(t * 9));
        orb(THROAT[0] + 6, THROAT[1] + 4, pr, t, shA, 700);
        strokePath(dyn, [[1230, 560], [1140, 540], [1050, 490], [996, 436]], { wid: 16, c: hex('#e1a07a'), c2: hex('#f4b890'), type: KNIFE, step: 18, seed: 77, alpha: pa });
        dyn.push({ x: 990, y: 432, ang: 0, len: 30, wid: 26, c: hex('#f4b890'), c2: hex('#e1a07a'), type: DAB, seed: 78, hgt: .6, alpha: pa });
        flush({ ...base, run: 0 });
      }
      // the throat turns blue
      if (t >= 48.6) {
        const bu = E_(t, 48.8, 51.4), pulse = 1 + .08 * Math.sin(t * 4);
        for (let k = 0; k < 42; k++) { const an = k / 42 * 6.283, rr = (7 + 15 * hash(k * 5)) * bu * pulse; dyn.push({ x: THROAT[0] + 4 + Math.cos(an) * rr * .8, y: THROAT[1] + 18 + Math.sin(an) * rr, ang: an + 1.2, len: 16 * bu + 3, wid: 9 * bu + 2, c: hex(BLUE[k % 5]), c2: hex(BLUE[(k + 2) % 5]), type: KNIFE, seed: k + 600, hgt: 1, alpha: shA * bu }); }
        flush({ ...base, run: 0 });
      }
    }
    if (t >= 42.2 && t < 54.8) {          // Parvati
      const pa = E_(t, 42.2, 43.2) * (1 - E_(t, 54.0, 54.8));
      plate(P.parv, { ...base, alpha: pa * ka, M: mul(TR(lerp(1500, 1250, E_(t, 42.2, 43.4)), SH_Y), SC(-1.5, 1.5)) });
    }
    // linga and water, once Shiva has gone
    if (t >= 54.6) {
      const la = E_(t, 54.6, 55.6);
      plate(P.linga, { ...base, alpha: la, M: TR(LX, GY + 12) });
      const wa = E_(t, 55.4, 56.2) * (1 - E_(t, 60.0, 60.9));
      if (wa > .01) {
        const topY = GY + 12 - 418;
        for (let k = 0; k < 34; k++) { const y = 120 + ((k * 31 + t * 520) % (topY - 100)); dyn.push({ x: LX + Math.sin(k * 3 + t * 8) * 7, y, ang: 1.57, len: 56, wid: 14, c: hex(k % 3 ? '#bff0ff' : '#ffffff'), c2: hex('#6ac8ff'), type: KNIFE, seed: k + 800, hgt: .7, alpha: wa }); }
        for (let k = 0; k < 22; k++) { const an = -Math.PI * (.1 + .8 * hash(k + 7)) + Math.sin(t * 6 + k) * .1, rr = 24 + 52 * ((t * 2 + hash(k)) % 1); dyn.push({ x: LX + Math.cos(an) * rr * 1.4, y: topY + 6 + Math.sin(an) * rr * .6, ang: an, len: 20, wid: 9, c: hex('#ffffff'), c2: hex('#9adfff'), type: DAB, seed: k + 900, hgt: .5, alpha: wa * .9 }); }
        for (const s of [-1, 1]) for (let k = 0; k < 12; k++) { const y = topY + 40 + ((k * 33 + t * 140) % 360), x = LX + s * (96 - (y - topY) * .02) + Math.sin(k) * 3; dyn.push({ x, y, ang: 1.57, len: 36, wid: 11, c: hex('#d8f6ff'), c2: hex('#7ad0ff'), type: KNIFE, seed: k + 950 + s, hgt: .6, alpha: wa * .85 }); }
        flush({ ...base, run: 0 });
      }
    }
    // diya flames
    if (t < 11.5 || t >= 35) for (const x of [LX - 330, LX - 200, LX + 200, LX + 330]) dyn.push({ x, y: GY + 8, ang: -1.57, len: 26 + 5 * Math.sin(t * 9 + x), wid: 14, c: hex('#fff0a0'), c2: hex('#ff9a2a'), type: DAB, seed: Math.floor(t * 8) + x, hgt: .6, alpha: ka });
    flush({ ...base, run: 0 });
  }
  // plaques laid in with the knife (screen space)
  const c0 = { x: W / 2, y: H / 2, zoom: 1 }, sc0 = { t, cam: c0, grey: 0, reveal: -1e6 };
  if (t >= 1.4 && t < 8.9) plate(P.open, { ...sc0, M: mul(TR(496, 24), SC(.8)), alpha: 1 - E_(t, 8.1, 8.9), appear: 1.4, appDur: 1.2 });
  if (t >= 52.6 && t < 55.2) plate(P.nil, { ...sc0, M: TR(120, 70), alpha: 1 - E_(t, 54.5, 55.2), appear: 52.6, appDur: 1.0 });
  if (t >= 61.2 && t < 69.2) plate(P.end2, { ...sc0, M: TR(380, 130), alpha: 1 - E_(t, 68.5, 69.2), appear: 61.2, appDur: 1.2 });
  if (t >= 69.4 && t < 76.3) plate(P.cta, { ...sc0, M: TR(380, 130), alpha: 1 - E_(t, 75.6, 76.3), appear: 69.4, appDur: 1.2 });
  if (t >= 76.5) plate(P.hari, { ...sc0, M: TR(380, 130), appear: 76.5, appDur: 1.0 });
  E.finish({ sat: .74, vig: .25 });
  let txt = '', a = 0;
  for (const s of CAPS) if (tn >= s.t0 && tn < s.t1) { txt = s.text; a = Math.min(E_(tn, s.t0, s.t0 + .2), 1 - E_(tn, s.t1 - .25, s.t1)); }
  capEl.textContent = txt; capEl.style.opacity = new URLSearchParams(location.search).get('nosub') ? 0 : a;
  document.getElementById('c').style.opacity = clamp(1 - E_(tn, DURN - 1.8, DURN - .2));
}

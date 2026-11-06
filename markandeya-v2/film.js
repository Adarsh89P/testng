// Markandeya (oil painting / palette knife). Same voice-over and timing as the shadow-puppet film; the world is colourful,
// drains to grey when the noose falls, and is re-laid in full colour by the knife when Shiva appears.
import { Impasto, Strokes, hex, KNIFE, DAB } from './engine/impasto.js';
import { strokePath } from './engine/plate.js';
import { SW, SH, GY, LX, buildDusk, buildDay, buildLinga, buildBoy, buildDuta, buildYama, buildNoose, buildShiva, buildText, LGW, LGH, LGX, LGY, BW, BH, BX, BY, DW, DH, DX, DY, YW, YH, YOX, YOY, NW, NH, SHW, SHH, SHX, SHY } from './scenes.js';
import { clamp, lerp, ss, seg, eo, eio, back } from './common.js';

const NEVER = 1e6, W = 1920, H = 1080, OFFX = 96, OFFY = 54;
const mul = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1], A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3], A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
const TR = (x, y) => [1, 0, 0, 1, x, y], SC = (s, sy = s) => [s, 0, 0, sy, 0, 0], RO = a => [Math.cos(a), Math.sin(a), -Math.sin(a), Math.cos(a), 0, 0];
const E_ = (t, a, b) => ss(seg(t, a, b));
const OFF = 1.0, DURN = 72.5;
// new time -> old (shadow-film) time: the scene logic below was timed on the first recording
const AN = [[0,0],[14.7,7.2],[18.1,10.8],[25.3,18.0],[25.8,18.4],[31.2,24.0],[32.2,25.0],[34.4,28.0],[35.7,29.3],[39.9,32.7],[40.7,33.5],[44.8,38.0],[47.4,41.4],[50.4,43.0],[54.4,46.4],[58.8,51.4],[59.8,52.2],[72.5,56.0]];
const M = tn => { for (let i = 0; i < AN.length - 1; i++) { const [a, b] = AN[i], [c, d] = AN[i + 1]; if (tn <= c) return b + (d - b) * (tn - a) / (c - a); } return AN[AN.length - 1][1]; };
const CAPS = [
  [0.00, 4.43, 'शिव के 108 नामों में से आज हम जानेंगे: मृत्युंजय,'],
  [4.87, 7.08, 'यानी मृत्यु को जीतने वाले।'],
  [7.61, 13.28, 'क्या आप जानते हैं, एक बालक की भक्ति के आगे मृत्यु के देवता यम को भी रुकना पड़ा था?'],
  [13.72, 16.66, 'और उसे बचाने के लिए, स्वयं शिव प्रकट हुए।'],
  [17.44, 21.44, 'ऋषि मृकंडु के पुत्र मार्कंडेय की आयु केवल सोलह वर्ष थी,'],
  [21.92, 24.07, 'यह उन्हें जन्म से पहले ही बता दिया गया था।'],
  [24.63, 29.11, 'जब सोलहवाँ वर्ष आया, वे शिवलिंग को कसकर थामकर पूजा में बैठ गए।'],
  [29.67, 34.74, 'यम के दूत उन्हें ले जा न सके, तब यम स्वयं आए और उन्होंने अपना पाश फेंका।'],
  [35.27, 38.20, 'वह पाश बालक के साथ शिवलिंग पर भी जा गिरा।'],
  [38.75, 43.05, 'तभी शिवलिंग से शिव प्रकट हुए, और उन्होंने यम को पीछे हटा दिया।'],
  [43.62, 46.00, 'इसी कारण शिव कालांतक कहलाए,'],
  [46.37, 48.60, 'यानी काल का अंत करने वाले।'],
  [49.17, 53.09, 'शिव ने मार्कंडेय को सदा सोलह वर्ष का रहने का वरदान दिया।'],
  [53.67, 58.64, 'तो दोस्तों, शिव के 108 नामों में से आज हमने जाना: मृत्युंजय।'],
  [59.19, 66.04, 'पूरी कथा विस्तार से जानने के लिए, यूट्यूब चैनल पर पूरा वीडियो देखिए, और चैनल को सब्सक्राइब ज़रूर कीजिए।'],
  [66.53, 68.58, 'हर हर महादेव।']
].map(([a, b, text]) => ({ t0: a + OFF, t1: b + OFF + .3, text }));
const T = { flashIn: 10.8, flashOut: 18.0, num: 12.6, boyRun: 18.4, dutas: 24.0, yamaBack: 25.0, throw0: 28.0, throw1: 29.3, shiva: 32.7, snap: 33.5, kal: 38.0, boon: 43.0, end: 52.2 };
const YX = 1480 + OFFX;
const kick = (t, t0, a = .1) => t >= t0 ? a * Math.max(0, 1 - (t - t0) / .28) : 0;
function camRaw(t) {
  const L = (a, b, u) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)];
  if (t < 7.3) return L([960, 560, 1], [1010, 540, 1.14], eio(seg(t, 0, 7.3)));
  if (t < 10.8) return L([1010, 540, 1.14], [960, 640, 1.5], eio(seg(t, 7.3, 10.2)));
  if (t < 18.0) return [960, 560, 1];
  if (t < 19.2) return L([960, 560, 1], [940, 600, 1.2], eio(seg(t, 18, 19.2)));
  if (t < 23.5) return [940, 600, 1.2];
  if (t < 25.0) return L([940, 600, 1.2], [1020, 560, 1], eio(seg(t, 23.5, 25)));
  if (t < 28.0) return [1020, 560, 1];
  if (t < 30.5) return L([1020, 560, 1], [960, 620, 1.55], eio(seg(t, 28, 29.4)));
  if (t < 32.4) return [960, 620, 1.55];
  if (t < 34.5) return L([960, 620, 1.55], [960, 500, 1.0], eio(seg(t, 32.6, 34.5)));
  if (t < 43) return [960, 520, 1];
  if (t < 46) return L([960, 520, 1], [900, 540, 1.12], eio(seg(t, 43, 46)));
  return L([900, 540, 1.12], [960, 540, .9], eio(seg(t, 46.5, 49.5)));
}
function camAt(t) {
  let [x, y, z] = camRaw(t); z *= 1 + kick(t, T.throw0, .05) + kick(t, T.shiva, .14) + kick(t, T.snap, .08) + kick(t, 7.2, .07);
  x += OFFX; y += OFFY; const hx = W / 2 / z, hy = H / 2 / z;
  return { x: clamp(x, hx, SW - hx), y: clamp(y, hy, SH - hy), zoom: z };
}

let E, P = {}, dyn, capEl;
const up = (built, w, h, ox = 0, oy = 0) => ({ b: E.batch(built.strokes.data()), tex: E.texture(built.ref.ctx.canvas), w, h, ox, oy });
export async function setup(canvas) {
  for (const w of ['600', '700']) await document.fonts.load(`${w} 40px "Noto Serif Devanagari"`, 'मार्कंडेय कालांतक १६ वर्ष');
  E = new Impasto(canvas, { W, H, ss: +(new URLSearchParams(location.search).get("ss") || 1) }); dyn = new Strokes(8192);
  P.dusk = up(buildDusk(), SW, SH); P.day = up(buildDay(), SW, SH);
  P.linga = up(buildLinga(), LGW, LGH, LGX, LGY);
  P.boyH = up(buildBoy(true), BW, BH, BX, BY); P.boyP = up(buildBoy(false), BW, BH, BX, BY);
  P.duta = up(buildDuta(), DW, DH, DX, DY); P.yama = up(buildYama(), YW, YH, YOX, YOY); P.noose = up(buildNoose(), NW, NH, NW / 2, NH / 2);
  P.shiva = up(buildShiva(true), SHW, SHH, SHX, SHY);
  P.num = up(buildText('१६', 'वर्ष', 620, 380, 210, 70), 620, 380); P.kal = up(buildText('कालांतक', 'काल का अंत करने वाले', 980, 290, 160, 48), 980, 290);
  P.open = up(buildText('मृत्युंजय', 'मृत्यु को जीतने वाले', 1160, 380, 190, 60), 1160, 380);
  P.end2 = up(buildText('मृत्युंजय', 'शिव के १०८ नामों में से', 1160, 380, 190, 60), 1160, 380);
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
  if (!o.noUnder && ua > 0 && !SKIP.includes('under')) E.under(pl.tex, pl.w, pl.h, { ...o, M: Mu, alpha: (o.alpha ?? 1) * ua });
  E.draw(pl.b, { ...o, M: Mu, appear: inTrans ? o.appear : -1e6, appDur: .14 });
}
const flush = o => { if (dyn.n) E.drawNow(dyn.data(), o); dyn.clear(); };
const COLS = ['#ffd23a', '#ff7ab0', '#4fe0f0', '#ff9a2a', '#b080ff', '#7affb0'];

function frame(tn) {
  const t = M(tn);
  const cam = camAt(t), fb = t >= T.flashIn && t < T.flashOut + .6;
  const dread = t >= T.throw0 && t < T.shiva;
  const base = { t, cam };
  const wo = t >= T.shiva ? { ...base, grey: 1, reveal: T.shiva, revDur: .5, revC: [LX, GY - 300, 1400] } : { ...base, grey: dread ? 1 : 0, reveal: dread ? NEVER : -1e6 };
  E.begin();
  const dayA = fb ? E_(t, T.flashIn, T.flashIn + .6) * (1 - E_(t, T.flashOut - .3, T.flashOut + .5)) : 0;
  plate(fb && dayA > .99 ? P.day : P.dusk, fb && dayA > .99 ? { ...base, grey: 0, reveal: -1e6 } : wo);
  if (fb && dayA > 0 && dayA <= .99) plate(P.day, { ...base, grey: 0, reveal: -1e6, alpha: dayA });
  const flash = fb;
  if (!(fb && dayA > .3)) plate(P.linga, { ...base, grey: 0, reveal: -1e6, M: TR(LX, GY + 12) });
  // Shiva rises out of the linga, with a halo of knife strokes
  if (t >= T.shiva) {
    const u = eo(seg(t, T.shiva, T.shiva + 1.2)), a = E_(t, T.shiva, T.shiva + .6), flip = t >= T.boon ? -1 : 1, sx = (t >= T.boon ? LX + 60 : LX - 10), s = .8 * (.8 + .2 * u), up = GY - 120 + 120 * (1 - u);
    const lf = t >= 51.4 ? 1 - E_(t, 51.4, 52.8) : 1;
    for (let k = 0; k < 60; k++) { const an = k / 60 * Math.PI * 2 + t * .25, r = 300 + 10 * Math.sin(t * 3 + k), cx = sx, cy = GY - 120 - 420; dyn.push({ x: cx + Math.cos(an) * r, y: cy + Math.sin(an) * r, ang: an + Math.PI / 2, len: 110, wid: 26, c: hex(COLS[k % 6]), c2: hex(COLS[(k + 2) % 6]), type: KNIFE, seed: k + 3, hgt: 1, alpha: a * lf }); }
    for (let k = 0; k < 40; k++) { const an = k / 40 * Math.PI * 2 - t * .3, r = 232, cx = sx, cy = GY - 120 - 420; dyn.push({ x: cx + Math.cos(an) * r, y: cy + Math.sin(an) * r, ang: an + Math.PI / 2, len: 80, wid: 16, c: hex(COLS[(k + 3) % 6]), c2: hex('#fff4c0'), type: KNIFE, seed: k + 90, hgt: .8, alpha: a * lf * .9 }); }
    flush({ ...base, grey: 0, run: 0 });
    plate(P.shiva, { ...base, grey: 0, reveal: -1e6, alpha: a * lf, M: mul(TR(sx, up), [s * flip, 0, 0, s, 0, 0]) });
  }
  // diya flames flicker
  for (const x of [LX - 330, LX - 200, LX + 200, LX + 330]) dyn.push({ x, y: GY + 8, ang: -1.57, len: 26 + 5 * Math.sin(t * 9 + x), wid: 14, c: hex('#fff0a0'), c2: hex('#ff9a2a'), type: DAB, seed: Math.floor(t * 8) + x, hgt: .6 });
  flush({ ...base, grey: 0, run: 0 });
  // the boy
  const bp = t < T.boyRun ? 0 : eo(seg(t, T.boyRun, T.boyRun + 1.1)), shake = t > 24 && t < 32.4 ? Math.sin(t * 38) * 1.8 : 0;
  if (fb) { const a = dayA; if (a > 0) plate(P.boyP, { ...base, grey: 0, reveal: -1e6, alpha: a, M: mul(TR(880 + OFFX * 0, GY), SC(1.25)) }); }
  else {
    let bx = LX - 135, pose = P.boyH;
    if (t < T.flashIn) bx = LX - 135; else if (t >= T.boyRun && t < T.boyRun + 1.2) bx = lerp(700 + OFFX, LX - 135, bp);
    if (t >= T.boon) { pose = P.boyP; bx = lerp(LX - 135, 640 + OFFX, ss(seg(t, T.boon + .4, T.boon + 1.6))); }
    if (t >= T.shiva && t < T.boon) bx = LX - 135;
    plate(pose, { ...base, grey: 0, reveal: -1e6, M: mul(TR(bx + shake, GY), SC(1.2)) });
  }
  // number 16 shown beside the hut (screen space, laid in with the knife)
  if (fb) { const a = E_(t, T.num, T.num + .5) * (1 - E_(t, 17.0, 17.8)); if (a > 0) plate(P.num, { t, cam: { x: W / 2, y: H / 2, zoom: 1 }, M: TR(1210, 120), grey: 0, reveal: -1e6, alpha: a, appear: T.num, appDur: 1.0, noUnder: false }); }
  // messengers and rope
  if (t >= T.dutas && t < 26.6) {
    const e = ss(seg(t, T.dutas, T.dutas + .8)), pull = Math.sin((t - T.dutas) * 9) * .5 + .5, fade = 1 - E_(t, 25.8, 26.6);
    [[0, 0], [1, 120]].forEach(([k, off]) => {
      const x0 = 340 + OFFX + off - (1 - e) * 500 + pull * 18 * (k ? -1 : 1);
      plate(P.duta, { ...base, grey: 0, reveal: -1e6, alpha: fade, M: mul(TR(x0, GY), mul(RO(-.05 - pull * .08), SC(1.1))) });
      const hx = x0 + 90, hy = GY - 170, tx = (t < T.boyRun ? LX - 135 : LX - 135) + 30, ty = GY - 150;
      strokePath(dyn, [[hx, hy], [(hx + tx) / 2, (hy + ty) / 2 + 30], [tx, ty]], { wid: 11, c: hex('#ff9a2a'), c2: hex('#c0401a'), type: KNIFE, step: 18, seed: 50 + k, alpha: fade });
    });
    flush({ ...base, grey: 0, run: 0 });
  }
  // Yama on his buffalo
  const yamaX = t < 9.6 ? YX : t < 10.8 ? YX + 900 * ss(seg(t, 9.6, 10.8)) : t < T.yamaBack ? YX + 900 : t < 26.6 ? lerp(YX + 900, YX, eo(seg(t, T.yamaBack, 26.6))) : t < 33.2 ? YX : lerp(YX, YX + 900, ss(seg(t, 33.2, 35.2)));
  const showYama = (t < 10.9 || (t >= T.yamaBack && t < 36.4)) && !fb;
  if (showYama) {
    const ent = t < 3 ? ss(seg(t, .3, 2.4)) : 1, ex = (1 - ent) * 700, hurt = t >= T.shiva ? E_(t, T.shiva, T.shiva + 1.4) : 0;
    const ys = 1.35 * (t < 7 ? 1 + .1 * E_(t, 0, 7) : 1), a = t >= 35 ? 1 - E_(t, 34.6, 36.2) : 1;
    plate(P.yama, { ...base, grey: 0, reveal: -1e6, alpha: a, M: mul(TR(yamaX + ex, GY), mul(RO(-hurt * .12), SC(ys))) });
    const hx = yamaX + ex - 84 * ys, hy = GY - 440 * ys;
    if (t < T.throw0 && (t < 10.9 || t >= T.yamaBack)) plate(P.noose, { ...base, grey: 0, reveal: -1e6, M: mul(TR(hx, hy + 30), mul(RO(Math.sin(t * 2.2) * .35 + .3), SC(.55))) });
    else if (t >= T.throw0 && t < T.throw1) { const u = eo(seg(t, T.throw0, T.throw1)); plate(P.noose, { ...base, grey: 0, reveal: -1e6, M: mul(TR(lerp(hx, LX, u), lerp(hy, GY - 140, u) - Math.sin(Math.PI * u) * 120), mul(RO(u * 7), SC(lerp(.55, 1.3, u), lerp(.55, .75, u)))) }); }
  }
  if (t >= T.throw1 && t < 35) {
    const sn = t >= T.snap ? ss(seg(t, T.snap, T.snap + 1)) : 0;
    plate(P.noose, { ...base, grey: 0, reveal: -1e6, alpha: 1 - sn, M: mul(TR(LX - sn * 60, GY - 140 + sn * 140), mul(RO(-sn * .6), SC(1.6, 1.0))) });
    if (t >= T.snap) plate(P.noose, { ...base, grey: 0, reveal: -1e6, alpha: 1 - sn, M: mul(TR(LX + sn * 70, GY - 140 + sn * 160), mul(RO(sn * .7), SC(1.6, 1.0))) });
  }
  if (t >= 46.4 && t < 51.4) plate(P.yama, { ...base, grey: 0, reveal: -1e6, alpha: 1 - E_(t, 50.6, 51.4), M: mul(TR(lerp(2500, 1560 + OFFX, eo(seg(t, 46.4, 47.6))), GY), mul(RO(-.12 * ss(seg(t, 47.8, 48.8))), SC(1.3))) });
  // plaques laid in with the knife (screen space)
  const c0 = { x: W / 2, y: H / 2, zoom: 1 };
  if (t >= T.kal && t < 42.4) { const a = (1 - E_(t, 41.4, 42.2)); plate(P.kal, { t, cam: c0, M: TR(120, 70), grey: 0, reveal: -1e6, alpha: a, appear: T.kal, appDur: 1.0 }); }
  if (t >= T.boon + .2 && t < 50.4 && tn < 54.8) { const a = (1 - E_(t, 49.6, 50.4)); plate(P.num, { t, cam: c0, M: TR(1230, 80), grey: 0, reveal: -1e6, alpha: a, appear: T.boon + .2, appDur: 1.0 }); }
  const sc0 = { t: tn, cam: c0, grey: 0, reveal: -1e6 };
  if (tn >= 1.4 && tn < 8.9) { const a = 1 - E_(tn, 8.1, 8.9); plate(P.open, { ...sc0, M: mul(TR(496, 24), SC(.8)), alpha: a, appear: 1.4, appDur: 1.2 }); }
  if (tn >= 55.0 && tn < 60.3) { const a = 1 - E_(tn, 59.6, 60.3); plate(P.end2, { ...sc0, M: TR(380, 130), alpha: a, appear: 55.0, appDur: 1.2 }); }
  if (tn >= 60.5 && tn < 67.9) { const a = 1 - E_(tn, 67.2, 67.9); plate(P.cta, { ...sc0, M: TR(380, 130), alpha: a, appear: 60.5, appDur: 1.2 }); }
  if (tn >= 68.0) plate(P.hari, { ...sc0, M: TR(380, 130), appear: 68.0, appDur: 1.0 });
  E.finish({ sat: .74, vig: .25 });
  // captions
  let txt = '', a = 0;
  for (const s of CAPS) if (tn >= s.t0 && tn < s.t1) { txt = s.text; a = Math.min(E_(tn, s.t0, s.t0 + .2), 1 - E_(tn, s.t1 - .25, s.t1)); }
  capEl.textContent = txt; capEl.style.opacity = new URLSearchParams(location.search).get('nosub') ? 0 : a;
  const fade = clamp(1 - E_(tn, DURN - 1.8, DURN - .2)); canvas_fade(fade);
}
function canvas_fade(f) { const c = document.getElementById('c'); c.style.opacity = f; }

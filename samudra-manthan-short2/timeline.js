// Short 2 — एक माला, जिसने तीनों लोकों की श्री छीन ली. One choreography, shared by both styles.
// frame(t) → { items: [{id, M, a, k, b, t0, jit}], cam: [cx, cy, z], mood }
// Times come from the pauses in the user's recording (audio/voice.mp3, 64.5 s).
import { HAND, durvasa, vidyadhari, indra, airavata } from './chars.js';

export const W = 1080, H = 1920, DUR = 65.6, GY = 1300;
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const seg = (t, a, b) => clamp((t - a) / (b - a));
export const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
export const eo = t => 1 - Math.pow(1 - clamp(t), 3);
export const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
// 2D affine matrices, canvas order [a, b, c, d, e, f]
export const mul = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1], A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3], A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
export const T = (x, y) => [1, 0, 0, 1, x, y];
export const R = r => [Math.cos(r), Math.sin(r), -Math.sin(r), Math.cos(r), 0, 0];
export const Sc = (sx, sy = sx) => [sx, 0, 0, sy, 0, 0];
export const ap = (M, [x, y]) => [M[0] * x + M[2] * y + M[4], M[1] * x + M[3] * y + M[5]];
const place = (x, y, s = 1, sx = 1, r = 0) => mul(mul(T(x, y), Sc(sx * s, s)), R(r));

export const CUES = [
  [0.00, 0.96, 'क्या आपको पता है...'], [1.44, 3.02, 'कि समुद्र मंथन की शुरुआत...'], [3.49, 5.29, 'फूलों की एक माला से हुई थी?'],
  [6.14, 7.90, 'विष्णु पुराण के अनुसार,'], [7.90, 9.90, 'एक बार महर्षि दुर्वासा ने'], [9.90, 13.12, 'एक विद्याधरी के हाथ में दिव्य फूलों की माला देखी,'],
  [13.52, 16.35, 'जिसकी सुगंध से पूरा वन महक रहा था।'], [16.96, 18.45, 'ऋषि ने वह माला माँगी,'], [18.73, 21.52, 'और प्रसन्न होकर देवराज इंद्र को भेंट कर दी।'],
  [22.25, 23.25, 'इंद्र ने माला ली...'], [23.54, 26.17, 'और अपने हाथी ऐरावत के मस्तक पर रख दी।'],
  [26.82, 30.44, 'सुगंध से मतवाले ऐरावत ने सूँड़ से माला खींची...'], [30.75, 31.84, 'और धरती पर फेंक दी।'],
  [32.98, 35.12, 'दुर्वासा का क्रोध भड़क उठा —'], [35.66, 36.23, '"हे इंद्र!'], [36.57, 39.78, 'ऐश्वर्य के मद में तुमने मेरे उपहार का अपमान किया है।'],
  [40.25, 40.80, 'जाओ,'], [40.84, 43.42, 'तीनों लोकों में तुम्हारी श्री नष्ट हो जाएगी।"'],
  [44.40, 45.32, 'और वैसा ही हुआ।'], [45.82, 46.85, 'यज्ञ रुक गए,'], [47.18, 48.57, 'वनस्पतियाँ सूख गईं,'], [48.99, 50.87, 'देवताओं का बल क्षीण हो गया...'], [51.25, 52.98, 'और दैत्यों ने उन्हें हरा दिया।'],
  [54.01, 55.64, 'एक माला का अपमान...'], [56.25, 59.04, 'और इसी से शुरू हुई समुद्र मंथन की कथा।'],
  [59.95, 60.90, 'पूरी कथा देखिए —'], [61.33, 62.86, 'समुद्र मंथन के रहस्य।'], [63.44, 64.50, 'जय श्री हरि।'],
];
export const cueAt = t => { for (let i = 0; i < CUES.length; i++) { const [a, b, s] = CUES[i], nx = CUES[i + 1] ? CUES[i + 1][0] : DUR; if (t >= a && t < Math.min(nx, b + .6)) return [s, t - a]; } return null; };

// press on (big → sharp) and lift off (grow, fade)
export function pr(t, t0, t1 = 1e9, din = .5, dout = .6) {
  if (t < t0 || t > t1 + dout) return null;
  if (t < t0 + din) { const u = eo((t - t0) / din); return { a: u, k: 1 + .2 * (1 - u), b: 12 * (1 - u) }; }
  if (t > t1) { const u = ss((t - t1) / dout); return { a: 1 - u, k: 1 + .25 * u, b: 14 * u }; }
  return { a: 1, k: 1, b: 0 };
}
const DV = durvasa(), VD = vidyadhari(), IN = indra(), EL = airavata();

export function frame(t) {
  const items = [];
  const add = (id, M, t0, t1, o = {}) => { const e = pr(t, t0, t1, o.din, o.dout); if (!e) return; items.push({ id, M: mul(M, Sc(e.k)), a: e.a * (o.a ?? 1), b: e.b, t0, jit: o.jit ?? 1 }); };

  // —— 1 · hook ——
  add('hook', place(540, 400, 1), 1.44, 5.95);
  add('garland', place(540, 760, 2.0, 1, .08 * Math.sin(t * 1.3)), .2, 5.95, { din: .7 });

  // —— the forest: 6.1 → 43.6 ——
  add('ground', place(0, GY), 6.0, 43.6, { jit: 0 });
  add('tree1', place(1120, GY + 10, 1.05), 6.14, 43.5);
  add('tree0', place(-60, GY + 10, .95, -1), 6.3, 43.5);

  // Durvasa walks in, stops; his free arm does the acting
  const dx = lerp(-140, 235, ss(seg(t, 7.9, 9.7))), walking = t > 7.9 && t < 9.8;
  const MD = place(dx, GY - (walking ? Math.abs(Math.sin(t * 7)) * 10 : 0), 1.12);
  let armR = walking ? .25 * Math.sin(t * 7) : .12;
  armR = lerp(armR, -1.05, ss(seg(t, 16.96, 17.6)));                 // asks for the garland
  armR = lerp(armR, -.55, ss(seg(t, 18.0, 18.7)));
  armR = lerp(armR, -1.35, ss(seg(t, 19.6, 20.4)));                  // offers it to Indra
  armR = lerp(armR, .1, ss(seg(t, 21.3, 22.0)));
  armR = lerp(armR, -2.7, eo(seg(t, 35.5, 35.9)));                   // "हे इंद्र!"
  armR = lerp(armR, -1.55, ss(seg(t, 36.5, 36.9)));                  // points
  armR = lerp(armR, -2.2, eo(seg(t, 40.7, 40.95)));                  // the curse
  armR = lerp(armR, .1, ss(seg(t, 42.6, 43.4)));
  const MDA = mul(mul(MD, T(...DV.shoulder)), R(armR));
  // anger: flames rise behind the sage
  const anger = ss(seg(t, 33.0, 34.2)) * (1 - ss(seg(t, 43.0, 43.6)));
  if (anger > .01) for (let i = 0; i < 3; i++) add('fire' + ((Math.floor(t * 12) + i) % 2), place(dx - 60 + i * 60, GY - 20, 1.1 + anger * .9 - Math.abs(i - 1) * .3), 33.0, 43.2, { a: anger * .9, din: .8, jit: 0 });
  add('durvasa.body', MD, 7.9, 43.4, { din: .01 }); add('durvasa.arm', MDA, 7.9, 43.4, { din: .01 });
  const dHand = ap(MDA, HAND);

  // the Vidyadhari floats in holding the garland, then rises away
  const vy = 960 + 12 * Math.sin(t * 1.6) - eo(seg(t, 18.2, 19.4)) * 520;
  const MV = place(780, vy, 1.05, -1, -.05);
  add('vidyadhari', MV, 9.9, 18.6, { din: .7 });
  const vHand = ap(MV, VD.hand);

  // Indra rides in on Airavata
  const ex = lerp(1500, 760, ss(seg(t, 18.73, 20.4))), stepping = t > 18.73 && t < 20.5;
  const ME = place(ex, GY - (stepping ? Math.abs(Math.sin(t * 5)) * 8 : 0), 1.25, -1, stepping ? .015 * Math.sin(t * 5) : 0);
  let trR = .05 * Math.sin(t * 1.2);
  trR = lerp(trR, -3.0, ss(seg(t, 26.82, 28.3)));                    // the trunk curls up to the head
  trR = lerp(trR, -1.6, ss(seg(t, 28.5, 30.4)));                     // pulls the garland down
  trR = lerp(trR, -.2, eo(seg(t, 30.75, 31.15)));                    // and flings it
  const MT = mul(mul(ME, T(...EL.trunkBase)), R(trR));
  const seatW = ap(ME, EL.seat);
  const bow = ss(seg(t, 41.0, 41.8)) * .16;
  const MI = place(seatW[0], seatW[1], 1.0, -1, bow);
  let inR = .15;
  inR = lerp(inR, -1.25, ss(seg(t, 20.4, 21.0)));                    // reaches for the garland
  inR = lerp(inR, -2.5, ss(seg(t, 22.25, 22.9)));                    // holds it up
  inR = lerp(inR, -1.1, ss(seg(t, 23.54, 24.3)));                    // places it on Airavata
  inR = lerp(inR, .2, ss(seg(t, 25.2, 25.9)));
  const MIA = mul(mul(MI, T(...IN.shoulder)), R(inR));
  add('airavata.body', ME, 18.73, 43.4, { din: .01 }); add('airavata.trunk', MT, 18.73, 43.4, { din: .01 });
  add('indra.body', MI, 18.73, 43.4, { din: .01 }); add('indra.arm', MIA, 18.73, 43.4, { din: .01 });
  const iHand = ap(MIA, HAND), eHead = ap(ME, EL.headTop), eTip = ap(MT, EL.trunkTip);

  // —— where the garland is ——
  const LAND = [430, GY + 6];
  if (t >= 6.0 && t < 43.5) {
    let g = vHand;
    const mv = (p, a, b, q) => { const u = ss(seg(t, a, b)); return [lerp(p[0], q[0], u), lerp(p[1], q[1], u) - Math.sin(u * Math.PI) * 60]; };
    if (t >= 16.96) g = mv(vHand, 16.96, 17.9, dHand);
    if (t >= 17.9) g = dHand;
    if (t >= 20.5) g = mv(dHand, 20.5, 21.4, iHand);
    if (t >= 21.4) g = iHand;
    if (t >= 23.9) g = mv(iHand, 23.9, 24.9, eHead);
    if (t >= 24.9) g = eHead;
    if (t >= 27.9) g = mv(eHead, 27.9, 28.5, eTip);
    if (t >= 28.5) g = eTip;
    if (t < 30.85 || t > 43.4) add('garland', mul(T(...g), Sc(.9)), 6.0, 43.4, { din: .01 });
    else {   // flung: a parabola to the ground, then it lies there
      const u = seg(t, 30.85, 31.35);
      if (u < 1) add('garland', mul(mul(T(lerp(eTip[0], LAND[0], u), lerp(eTip[1], LAND[1] - 10, u) - Math.sin(u * Math.PI) * 140), R(u * 4)), Sc(.9)), 6, 43.4, { din: .01 });
      else add('garlandL', mul(T(LAND[0], LAND[1] - Math.abs(Math.sin(seg(t, 31.35, 31.75) * Math.PI)) * 18), Sc(.95)), 31.35, 43.4, { din: .01 });
    }
  }
  // the fragrance: petals drifting across the forest
  if (t > 13.5 && t < 17.5) for (let i = 0; i < 12; i++) { const u = seg(t, 13.5 + hash(i) * 1.2, 16.8 + hash(i) * .6); if (u <= 0 || u >= 1) continue; add('petal', place(lerp(vHand[0], 80 + hash(i * 3) * 900, u), lerp(vHand[1], 500 + hash(i * 5) * 700, u) + Math.sin(u * 9 + i) * 30, 1.2, 1, u * 6 + i), 13.5, 17.5, { a: Math.sin(u * Math.PI), din: .01 }); }
  if (t > 31.3 && t < 33.5) for (let i = 0; i < 9; i++) { const u = seg(t, 31.35, 32.9 + hash(i) * .5); if (u >= 1) continue; const a = -Math.PI * (.15 + .7 * hash(i * 9)); add('petal', place(LAND[0] + Math.cos(a) * u * 260, LAND[1] + Math.sin(a) * u * 200 + u * u * 160, 1.1, 1, u * 5), 31.35, 33.4, { a: 1 - u, din: .01 }); }

  // —— 6 · the curse takes hold ——
  add('kund', place(540, GY + 40, 1.1), 44.4, 53.3);
  const fireK = 1 - ss(seg(t, 45.82, 46.4));
  if (fireK > .02) add('fire' + (Math.floor(t * 12) % 2), place(540, GY - 80, 1.0 * fireK + .05), 44.5, 53.3, { jit: 0 });
  for (let i = 0; i < 4; i++) { const st = 46.0 + i * .45; if (t > st && t < st + 3.2) { const u = seg(t, st, st + 3.2); add('smoke' + (i % 2), place(540 + Math.sin(t + i) * 30, GY - 100 - u * 480, .8 + u * .8, 1, Math.sin(t * .8 + i) * .2), st, 53.3, { a: Math.sin(u * Math.PI) * .9, din: .01, jit: 0 }); } }
  const wilt = ss(seg(t, 47.18, 47.7));
  for (const [x, sx] of [[150, 1], [930, -1]]) { add('shrubF', place(x, GY + 20, .95, sx), 44.6, 53.3, { a: 1 - wilt }); if (wilt > 0) add('shrubW', place(x, GY + 20, .95, sx), 47.18, 53.3, { a: wilt, din: .01 }); }
  const weak = ss(seg(t, 48.99, 50.2)), fallen = ss(seg(t, 51.9, 52.5));
  add('deva0', place(345, GY + 20 + weak * 60 + fallen * 80, .92, 1, weak * .32 + fallen * .5), 45.0, 52.5);
  add('deva1', place(735, GY + 20 + weak * 60 + fallen * 80, .92, -1, -(weak * .32 + fallen * .5)), 45.2, 52.5);
  const run = ss(seg(t, 51.25, 51.85));
  add('daitya0', place(lerp(1300, 850, run), GY + 20 - Math.abs(Math.sin(t * 8)) * (1 - run) * 14, .95, -1, -.08), 51.25, 53.3, { din: .2 });
  add('daitya1', place(lerp(1450, 985, run), GY + 20 - Math.abs(Math.sin(t * 8 + 1)) * (1 - run) * 14, .9, -1, -.06), 51.4, 53.3, { din: .2 });

  // —— 7 · one garland… the churning to come ——
  add('garlandL', place(540, 1120, 2.0), 54.01, 56.2, { din: .6 });
  add('sea0', place(0, 1250 + (1 - eo(seg(t, 56.25, 57.0))) * 260), 56.25, 59.4, { jit: 0 });
  add('mandara', place(540, 1270 + (1 - eo(seg(t, 56.6, 57.6))) * 400, .85), 56.6, 59.4, { jit: 0 });
  add('sea1', place(0, 1320 + (1 - eo(seg(t, 56.25, 57.0))) * 300), 56.25, 59.4, { jit: 0 });

  // —— 8 · end card ——
  add('title', place(540, 470, .9), 59.95, 1e9, { din: .6 });
  add('vishnu', place(540, GY + 60, 1.0), 61.4, 1e9, { din: .7 });

  // camera
  let cam = [540, 900, 1.12];
  const push = ss(seg(t, 33.0, 34.8)) * (1 - ss(seg(t, 40.84, 41.3)));
  cam = [lerp(540, 420, push), lerp(900, 930, push), lerp(1.12, 1.32, push)];
  if (t >= 20.6 && t < 31) { const u = ss(seg(t, 22.2, 26.5)) * (1 - ss(seg(t, 30.0, 30.8))); cam = [lerp(540, 600, u), lerp(900, 880, u), lerp(1.12, 1.2, u)]; }
  for (const h of [31.35, 40.84]) if (t >= h && t < h + .45) cam[2] += .1 * (1 - eo((t - h) / .45));
  if (t >= 54 && t < 59.5) { const u = ss(seg(t, 54.0, 58.8)); cam = [540, lerp(1000, 960, u), lerp(1.1, 1.2, u)]; }

  const drain = Math.max(ss(seg(t, 45.82, 46.4)) * .33 + ss(seg(t, 47.18, 47.7)) * .33 + ss(seg(t, 48.99, 49.6)) * .34, 0) * (1 - ss(seg(t, 53.3, 54.0)));
  const flash = t >= 40.84 && t < 41.3 ? 1 - seg(t, 40.84, 41.3) : 0;
  const fade = ss(seg(t, 64.9, 65.6)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, mood: { anger, drain, flash, fade: clamp(fade), hero: t > 59.9 ? 1 : 0 } };
}

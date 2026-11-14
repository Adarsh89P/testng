// Short 8 — विष्णु का मनमोहिनी रूप (voice8.mp3, 55.3 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, seaBack, seaFront, sparkRise, sparkRing, endCard, mul, T, R, ap } from './tlc.js';
import { HAND } from './chars.js';
export const DUR = 56.0, HOOK = [['मनमोहिनी', -52, 108], ['रूप', 66, 110]];
export const THUMB = { t: 34.6, top: ['विष्णु बने', 'मनमोहिनी!'], bottom: 'अमृत का रहस्य' };
export const CUES = splitCues([
  [0, .97, 'क्या आपको पता है...'], [1.42, 4.2, 'कि दैत्यों से अमृत वापस लेने के लिए'], [4.2, 7.07, 'भगवान विष्णु ने एक स्त्री का रूप धारण किया था?'],
  [7.91, 9.28, 'विष्णु पुराण के अनुसार,'], [9.57, 12.41, 'जब माँ लक्ष्मी ने भगवान विष्णु का वरण किया...'], [12.64, 14.29, 'तो दैत्य क्रोधित हो उठे।'], [14.81, 18.23, 'उन्होंने धन्वंतरि के हाथ से अमृत का पात्र छीन लिया।'],
  [20.04, 21.60, 'परिश्रम दोनों ने किया था...'], [22.32, 26.52, 'पर अमृत अगर दैत्यों के पास रह जाता, तो धर्म की रक्षा कौन करता?'],
  [27.49, 31.04, 'तब भगवान विष्णु ने एक मनमोहिनी स्त्री का रूप धारण किया।'], [31.73, 35.00, 'उस रूप पर मोहित होकर दैत्य सुध-बुध खो बैठे...'], [35.49, 38.48, 'और भगवान ने अमृत लेकर देवताओं को दे दिया।'],
  [39.25, 41.69, 'अमृत पीकर देवताओं का तेज लौट आया।'], [42.20, 43.99, 'उन्होंने दैत्यों को पराजित किया...'], [44.23, 46.39, 'और दैत्य पाताल लोक भाग गए।'],
  [47.09, 47.93, 'बल से नहीं...'], [48.38, 50.00, 'बुद्धि से जीता गया अमृत।'], [50.68, 51.69, 'पूरी कथा देखिए —'], [52.12, 53.77, 'समुद्र मंथन के रहस्य।'], [54.31, 55.10, 'जय श्री हरि।']]);
const mv = (t, p, a, b, q) => { const u = ss(seg(t, a, b)); return [lerp(p[0], q[0], u), lerp(p[1], q[1], u) - Math.sin(u * Math.PI) * 80]; };
export function frame(t) {
  const items = [], add = adder(items, t), END = 50.3;
  seaBack(add, t, .1, END);
  // hook: Vishnu becomes Mohini
  add('vishnu', place(540, GY + 120, 1.0), .2, 4.3, { din: .7 });
  add('mohini', place(540, GY + 120, 1.0), 4.4, 7.5, { din: .5 });
  add('hook', place(540, 400), 1.42, 7.5);
  // Lakshmi chooses Vishnu; the daityas rage
  add('vishnu', place(700, GY + 80, .9, -1), 7.91, 14.6); add('lakshmi', place(460, GY + 80, .85), 8.2, 14.6);
  sparkRing(add, t, 9.6, 12.4, 580, GY - 260, 220, 12);
  const sink = ss(seg(t, 44.23, 46.2)), lean = ss(seg(t, 31.73, 33.0)) * (1 - ss(seg(t, 42.2, 43.0)));
  const D0 = place(230 + lean * 40, GY + 40 + sink * 700, .74, 1, -.08 + lean * .2 + sink * .3), D1 = place(110 + lean * 40, GY + 40 + sink * 700, .7, 1, -.06 + lean * .2 + sink * .3);
  add('daitya0', D0, 12.64, 46.4, { din: .4 }); add('daitya1', D1, 12.8, 46.4, { din: .4 });
  if (sink > .02) for (let i = 0; i < 4; i++) add('smoke' + (i % 2), place(120 + i * 60, GY + 40 - sink * 200 - i * 40, .9 + sink * .5, 1, Math.sin(t + i) * .2), 44.3, 46.6, { a: .7 * Math.sin(sink * Math.PI), din: .01 });
  // Dhanvantari and the kalash; the daityas snatch it
  const DH = [880, GY + 80], dS = .72;
  add('dhanvantariE', place(DH[0], DH[1], dS, -1), 14.81, 19.8);
  const pD = [DH[0] - 84 * dS, DH[1] - 318 * dS], pA = ap(D0, [104, -270]);
  // Mohini, the devas
  const MO = [540, GY + 100], mS = .95, pM = [MO[0] + 88 * mS, MO[1] - 330 * mS];
  add('vishnu', place(540, GY + 100, .95), 26.6, 27.4, { din: .4 });
  add('mohini', place(MO[0], MO[1], mS), 27.49, END, { din: .5 });
  const glow = ss(seg(t, 39.25, 40.4));
  const V0 = place(880, GY + 40 - glow * 10, .74, -1, .1 * (1 - glow)), V1 = place(990, GY + 40 - glow * 10, .7, -1, .1 * (1 - glow));
  add('deva0', V0, 20.04, END); add('deva1', V1, 20.2, END);
  const pV = ap(V0, [104, -270]);
  let k = pD;
  if (t >= 16.0) k = mv(t, pD, 16.0, 17.4, pA);
  if (t >= 17.4) k = pA;
  if (t >= 33.4) k = mv(t, pA, 33.4, 35.0, pM);
  if (t >= 35.0) k = pM;
  if (t >= 36.0) k = mv(t, pM, 36.0, 38.0, pV);
  if (t >= 38.0) k = pV;
  add('kalash', place(k[0], k[1] + 40, .8), 14.81, END, { din: .5 });
  for (let i = 0; i < 10; i++) { const st = 31.8 + (i * .29) % 3; if (t < st || t > st + 1.4) continue; const u = (t - st) / 1.4; add('petal', place(lerp(pM[0], 150 + (i % 3) * 60, u), lerp(pM[1] - 100, GY - 300, u), 1.3, 1, u * 6), st, st + 1.2, { a: Math.sin(u * Math.PI), din: .01 }); }
  sparkRise(add, t, 39.2, 41.7, 820, 1040, GY - 60, 380, 14, 4);
  sparkRing(add, t, 47.0, END, MO[0], MO[1] - 340, 220, 12);
  seaFront(add, t, .1, END);
  endCard(add, t, 50.68, 52.12);
  const cam = key(t, [[0, [540, 960, 1.04]], [7.5, [540, 960, 1.04]], [8.2, [540, 1000, 1.0]], [14.6, [540, 1000, 1.0]], [15.6, [560, 1000, 1.06]], [26.5, [560, 1000, 1.06]], [27.6, [540, 980, 1.15]], [31.4, [540, 980, 1.15]], [32.2, [540, 1000, 1.0]], [47.0, [540, 1000, 1.0]], [47.9, [540, 940, 1.12]], [50.3, [540, 940, 1.12]], [50.8, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 55.4, 56.0)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .6 * ss(seg(t, 12.6, 13.6)) * (1 - ss(seg(t, 26.6, 27.6))), drain: 0, flash: clamp(.4 * pulse(t, 4.4) + .5 * pulse(t, 27.49) + .3 * pulse(t, 48.38)), fade: clamp(fade) } };
}

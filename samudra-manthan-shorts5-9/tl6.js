// Short 6 — धन्वंतरि और अमृत कलश (voice6.mp3, 55.3 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, seaBack, seaFront, tableau, sparkRise, sparkRing, endCard, hash } from './tlc.js';
export const DUR = 56.0, HOOK = [['अमृत कलश', -52, 104], ['किसके हाथ?', 66, 104]];
export const THUMB = { t: 24.5, top: ['अमृत कलश लेकर', 'कौन आए?'], bottom: 'भगवान धन्वंतरि' };
export const CUES = splitCues([
  [0, 1.01, 'क्या आपको पता है...'], [1.42, 4.74, 'कि अमृत का कलश लेकर समुद्र से कौन प्रकट हुए थे?'],
  [5.53, 6.84, 'विष्णु पुराण के अनुसार,'], [7.18, 9.39, 'समुद्र मंथन से रत्न निकलते रहे...'], [9.90, 13.51, 'फिर उठा भयंकर विष, जिसे नागों ने ग्रहण किया।'],
  [14.55, 15.40, 'और उसके बाद...'], [15.88, 19.77, 'क्षीरसागर की लहरों के बीच से एक दिव्य पुरुष प्रकट हुए।'],
  [20.32, 23.16, 'श्वेत वस्त्र पहने, तेज से दमकते हुए,'], [23.57, 25.89, 'हाथों में अमृत से भरा कमंडलु लिए —'], [26.49, 28.42, 'ये थे भगवान धन्वंतरि।'],
  [29.01, 33.44, 'उन्हें देखकर देवता, दैत्य और ऋषि — सब आनंद से भर उठे।'], [33.95, 36.88, 'क्योंकि जिस अमृत के लिए यह पूरा मंथन हुआ था...'], [37.21, 39.30, 'वह अब सबकी आँखों के सामने था।'],
  [39.92, 43.27, 'भगवान धन्वंतरि को आयुर्वेद का देवता माना जाता है —'], [43.76, 45.49, 'आरोग्य और जीवन के दाता।'],
  [46.03, 47.40, 'पर अमृत सामने आया...'], [47.64, 49.97, 'तो प्रश्न भी उठा — यह किसे मिलेगा?'],
  [50.57, 51.56, 'पूरी कथा देखिए —'], [51.98, 53.61, 'समुद्र मंथन के रहस्य।'], [54.15, 54.96, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 50.3;
  seaBack(add, t, .1, END);
  add('kalash', place(540, 980, 2.3, 1, .05 * Math.sin(t * 1.3)), .2, 5.3, { din: .7 });
  sparkRing(add, t, .8, 5.2, 540, 830, 230, 12);
  add('hook', place(540, 400), 1.42, 5.3);
  tableau(add, items, t, 5.53, 14.3, 5.6);
  // the poison rises, the Nagas draw it in
  for (let i = 0; i < 6; i++) { const st = 9.9 + i * .3; if (t < st || t > 13.6) continue; const u = seg(t, st, st + 2.4), pull = ss(seg(t, 11.8, 13.4)); add('smoke' + (i % 2), place(lerp(380 + i * 60, [300, 540, 780][i % 3], pull), GY - 100 - u * 500 + pull * 300, (.8 + u * .6) * (1 - pull * .7), 1, Math.sin(t + i) * .2), st, 13.6, { a: Math.sin(Math.min(1, u) * Math.PI) * .85, din: .01 }); }
  [300, 540, 780].forEach((x, k) => add('naga' + k, place(x, GY + 40 + rise(t, 11.4 + k * .12, .7, 300), .8, k === 2 ? -1 : 1), 11.4 + k * .12, 14.0, { din: .4 }));
  // Dhanvantari rises from the waves
  const dAt = [540, GY + 120], dS = 1.05;
  add('dhanvantari', place(dAt[0], dAt[1] + rise(t, 15.9, 1.4, 420), dS), 15.88, END, { din: .8 });
  const kx = dAt[0] + 84 * dS, ky = dAt[1] - 318 * dS;
  sparkRing(add, t, 23.6, 28.4, kx, ky - 40, 120, 10);
  // devas, daityas and a rishi rejoice
  add('daitya0', place(215 + ss(seg(t, 46.0, 48.0)) * 60, GY + 40, .7, 1, -.04 * Math.sin(t * 3)), 29.0, END);
  add('daitya1', place(100 + ss(seg(t, 46.0, 48.0)) * 60, GY + 40, .66, 1), 29.2, END);
  add('deva0', place(880 - ss(seg(t, 46.0, 48.0)) * 60, GY + 40, .7, -1, .04 * Math.sin(t * 3)), 29.4, END);
  add('deva1', place(990 - ss(seg(t, 46.0, 48.0)) * 60, GY + 40, .66, -1), 29.6, END);
  add('durvasa.body', place(330, GY + 60, .6), 30.0, 39.6); add('durvasa.arm', mul(mul(place(330, GY + 60, .6), T(14, -388)), R(-2.3)), 30.0, 39.6);
  sparkRise(add, t, 33.9, 39.3, kx - 120, kx + 120, ky, 300, 14, 3);
  // Ayurveda: healing herbs sprout
  for (const [x, sx, t0] of [[230, 1, 40.0], [850, -1, 40.4], [380, 1, 41.0], [700, -1, 41.4]]) add('shrubF', place(x, GY + 130 + rise(t, t0, .8, 120), .85, sx), t0, 45.8);
  sparkRise(add, t, 43.7, 45.5, 200, 880, GY, 300, 12, 7);
  sparkRing(add, t, 46.0, END, kx, ky - 40, 110 + 20 * Math.sin(t * 6), 8);
  seaFront(add, t, .1, END);
  endCard(add, t, 50.57, 51.98);
  const cam = key(t, [[0, [540, 960, 1.04]], [5.2, [540, 960, 1.04]], [5.9, [540, 980, 1.0]], [14.3, [540, 980, 1.0]], [15.6, [540, 1080, 1.1]], [20.3, [540, 1060, 1.12]], [22.0, [560, 1020, 1.25]], [28.4, [560, 1020, 1.25]], [29.2, [540, 1000, 1.0]], [33.6, [540, 1000, 1.0]], [34.6, [600, 1020, 1.5]], [39.4, [600, 1020, 1.5]], [40.1, [540, 1000, 1.0]], [50.2, [540, 1000, 1.05]], [50.8, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 55.4, 56.0)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .4 * ss(seg(t, 46, 47.6)) * (1 - ss(seg(t, 49.8, 50.4))), drain: .5 * ss(seg(t, 9.9, 11)) * (1 - ss(seg(t, 13.4, 14.4))), flash: clamp(.4 * pulse(t, 15.9) + .3 * pulse(t, 26.49)), fade: clamp(fade) } };
}
import { mul, T, R } from './tlc.js';

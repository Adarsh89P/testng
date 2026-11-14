// Short 5 — क्षीरसागर से निकले दिव्य रत्न (voice5.mp3, 57.2 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, seaBack, seaFront, tableau, sparkRise, sparkRing, endCard } from './tlc.js';
export const DUR = 57.9, HOOK = [['पहला रत्न', -52, 104], ['कौन-सा?', 66, 104]];
export const THUMB = { t: 18.0, top: ['समुद्र मंथन से निकला', 'पहला रत्न!'], bottom: 'कामधेनु · पारिजात · चंद्रमा' };
export const CUES = splitCues([
  [0, .93, 'क्या आपको पता है...'], [1.40, 2.92, 'कि विष्णु पुराण के अनुसार,'], [3.17, 5.98, 'समुद्र मंथन से सबसे पहले क्या निकला था?'],
  [6.73, 10.3, 'जब देवता और दैत्य क्षीरसागर को मथ रहे थे...'], [10.3, 13.86, 'तो समुद्र से एक-एक करके दिव्य रत्न प्रकट होने लगे।'],
  [14.48, 17.50, 'सबसे पहले निकली सुरभि — कामधेनु गाय,'], [17.84, 20.40, 'जो यज्ञ के लिए दूध और घी देती है।'], [20.97, 24.24, 'उसे देखकर देवता और ऋषि आनंद से भर उठे।'],
  [25.68, 27.56, 'फिर प्रकट हुईं वारुणी देवी।'], [28.11, 29.84, 'फिर निकला पारिजात वृक्ष —'], [30.12, 34.15, 'स्वर्ग का वृक्ष, जिसकी सुगंध से सारा संसार महक उठा।'],
  [34.75, 36.31, 'फिर प्रकट हुईं अप्सराएँ —'], [36.78, 38.47, 'अद्भुत सौंदर्य से भरी हुई।'], [38.93, 41.82, 'और फिर उठा शीतल किरणों वाला चंद्रमा...'], [42.19, 45.53, 'जिसे भगवान महादेव ने अपने मस्तक पर धारण कर लिया।'],
  [46.11, 47.10, 'एक-एक रत्न...'], [47.52, 49.39, 'और हर रत्न एक नई कथा।'], [49.90, 52.19, 'पर असली रत्न अभी आना बाकी था।'],
  [52.70, 53.68, 'पूरी कथा देखिए —'], [54.06, 55.67, 'समुद्र मंथन के रहस्य।'], [56.17, 56.94, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 52.4;
  seaBack(add, t, .1, END);
  tableau(add, items, t, .2, 14.1, .2);
  add('hook', place(540, 400), 1.40, 5.9);
  sparkRise(add, t, 10.3, 13.9, 300, 780, GY, 500, 16, 5);
  // each treasure rises from the milk and takes the stage alone
  add('kamadhenu', place(540, GY + 70 + rise(t, 15.4, 1.1), 1.15, -1), 15.4, 25.3, { din: .7 });
  add('durvasa.body', place(170, GY + 60, .66), 20.97, 25.2); add('durvasa.arm', mul2(place(170, GY + 60, .66), 14, -388, -2.3), 20.97, 25.2);
  add('deva0', place(900, GY + 60, .66, -1, .06 * Math.sin(t * 3)), 21.2, 25.2);
  add('varuni', place(540, GY + 90 + rise(t, 25.68, 1.0), .95), 25.68, 27.9, { din: .6 });
  add('tree0', place(540, GY + 80 + rise(t, 28.11, 1.1, 360), 1.0), 28.11, 34.5, { din: .6 });
  for (let i = 0; i < 12; i++) { const u = seg(t, 30.1 + i * .25, 33.9 + i * .1); if (u <= 0 || u >= 1) continue; add('petal', place(lerp(540, 80 + (i * 97) % 920, u), lerp(900, 500 + (i * 151) % 700, u) + Math.sin(u * 9 + i) * 30, 1.3, 1, u * 6), 30.1, 34.4, { a: Math.sin(u * Math.PI), din: .01 }); }
  add('apsara', place(420, GY + 90 + rise(t, 34.75, .9), .82, 1, .06 * Math.sin(t * 3)), 34.75, 38.7, { din: .5 });
  add('apsara2', place(660, GY + 90 + rise(t, 34.95, .9), .82, -1, -.06 * Math.sin(t * 3 + 1)), 34.95, 38.7, { din: .5 });
  // the moon rises, then settles on Mahadev's jata
  const up = ss(seg(t, 38.93, 40.6)), onto = ss(seg(t, 43.0, 44.8));
  add('moon', place(lerp(540, 556, onto), lerp(lerp(GY, 470, up), 846, onto), lerp(1.3, .42, onto), 1, -.3), 38.93, 45.9, { din: .6 });
  add('shiva', place(540, GY + 80, .9), 42.19, 45.9, { din: .7 });
  // all the treasures together, then the promise of a greater one
  const dim = 1 - .6 * ss(seg(t, 49.9, 50.6));
  add('kamadhenu', place(250, GY + 60, .62, -1), 46.11, END, { a: dim });
  add('varuni', place(450, GY + 70, .58), 46.25, END, { a: dim });
  add('apsara', place(640, GY + 70, .52), 46.4, END, { a: dim });
  add('tree0', place(880, GY + 70, .62), 46.55, END, { a: dim });
  add('moon', place(540, 480, .9, 1, -.3), 46.7, END, { a: dim });
  sparkRise(add, t, 47.5, 49.4, 150, 950, GY - 60, 380, 16, 9);
  add('lotusThrone', place(540, GY + 150 + rise(t, 49.9, 1.2, 200), .55), 49.9, END, { din: .6 });
  sparkRing(add, t, 50.5, END, 540, GY + 80, 170, 10);
  seaFront(add, t, .1, END);
  endCard(add, t, 52.70, 54.06);
  const cam = key(t, [[0, [540, 980, 1.0]], [14.0, [540, 980, 1.0]], [15.2, [540, 1100, 1.1]], [45.8, [540, 1080, 1.1]], [46.6, [540, 960, 1.0]], [52.4, [540, 960, 1.0]], [52.9, [540, 960, 1.05]]]);
  if (t >= 42.5 && t < 45.9) { const u = ss(seg(t, 42.5, 43.4)); cam[1] = lerp(cam[1], 980, u); }
  const fade = ss(seg(t, 57.3, 57.9)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: 0, drain: 0, flash: clamp(.3 * pulse(t, 15.4) + .3 * pulse(t, 38.93) + .25 * pulse(t, 49.9)), fade: clamp(fade) } };
}
import { mul, T, R } from './tlc.js';
function mul2(M, sx, sy, r) { return mul(mul(M, T(sx, sy)), R(r)); }

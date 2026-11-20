// Prahlad 6 — पुरोहितों की कृत्या (voice6.mp3, 50.9 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard, palace, hiranya } from './tlc.js';
export const DUR = 51.5, HOOK = [['शत्रु को', -52, 104], ['जीवनदान?', 66, 104]];
export const THUMB = { t: 25.0, top: ['कृत्या का त्रिशूल', 'टूट गया!'], bottom: 'प्रह्लाद — भाग 6' };
export const CUES = splitCues([
  [0, 1.00, 'क्या आपको पता है...'], [1.34, 5.42, 'कि जिन पुरोहितों ने प्रह्लाद को मारने के लिए राक्षसी शक्ति बनाई,'], [5.86, 7.74, 'प्रह्लाद ने उन्हीं को जीवित कर दिया?'],
  [8.58, 9.92, 'विष्णु पुराण के अनुसार,'], [10.24, 13.44, 'हिरण्यकशिपु के पुरोहितों ने पहले प्रह्लाद को समझाया।'], [14.08, 19.28, 'जब वह नहीं माना... तो उन्होंने मंत्रों से एक भयंकर अग्निमयी कृत्या उत्पन्न की।'],
  [20.39, 23.68, 'कृत्या ने त्रिशूल से प्रह्लाद की छाती पर प्रहार किया...'], [24.21, 27.24, 'पर त्रिशूल टुकड़े-टुकड़े होकर धरती पर गिर पड़ा।'], [27.85, 31.32, 'और वह कृत्या लौटी... और उन्हीं पुरोहितों को जलाने लगी।'],
  [32.05, 34.98, 'तब प्रह्लाद दौड़कर उनके पास गया, और प्रार्थना की —'], [35.59, 42.58, '"हे भगवान, यदि मैंने इन्हें कभी शत्रु नहीं माना... तो ये जीवित हो जाएँ।"'],
  [42.90, 47.16, 'और पुरोहित जीवित हो उठे — और प्रह्लाद को आशीर्वाद देने लगे।'], [47.69, 49.21, 'शत्रु के लिए भी करुणा... यही है सच्ची भक्ति।'], [49.77, 50.58, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 49.6, PX = 700;
  add('hook', place(540, 400), 1.34, 8.2);
  add('purohit', place(280, GY + 80, .85), .2, 8.2); add('prahlad', place(760, GY + 80 + rise(t, 5.86, .8, 100), 1.15, -1), 5.86, 8.2);
  sparkRing(add, t, 6.0, 8.2, 760, GY - 230, 140, 10);
  palace(add, t, 8.3, END);
  hiranya(add, t, 200, GY + 60, .8, 1, .1, 8.58, 14.0, { a: .9 });
  // the priests advise, then chant the Kritya into being
  const burn = ss(seg(t, 28.5, 30.0)) * (1 - ss(seg(t, 41.5, 43.0)));
  const pr = (x, d) => place(x, GY + 80, .82, 1, burn * (.12 + .04 * Math.sin(t * 12 + d)));
  add('purohit', pr(300, 0), 10.24, END); add('purohit', pr(470, 1), 10.4, END);
  add('prahlad', place(PX + 60, GY + 80, 1.1, -1), 10.24, 32.0);
  add('kund', place(390, GY + 60, .7), 14.08, 20.3);
  add('fire0', place(390, GY - 20, .6 + .5 * ss(seg(t, 15, 19))), 14.5, 20.3);
  sparkRise(add, t, 15.5, 19.3, 300, 480, GY - 120, 400, 14, 6);
  // Kritya rises in fire and strikes; the trident shatters
  const kx = lerp(420, 560, ss(seg(t, 20.4, 22.8))), back = ss(seg(t, 27.9, 29.5));
  const KX = lerp(kx, 380, back);
  add('kritya', place(KX, GY + 60 + rise(t, 18.6, 1.2, 300), 1.0, 1), 18.6, 31.6);
  add('fire1', place(KX, GY + 20, 1.1 + .1 * Math.sin(t * 9)), 18.6, 31.6, { a: .9 });
  add('trishul', place(KX + 80 + 60 * ss(seg(t, 21.5, 23.2)), GY - 260, 1.0, 1, 1.35), 20.39, 24.3);
  [[-1, 0], [1, 1], [.3, 2], [-.4, 3]].forEach(([d, k]) => { const f = ss(seg(t, 24.3, 25.6)); add('shard', place(PX - 40 + d * 80 * f, GY - 280 + f * 340, 1.2, 1, f * 3 * d), 24.21, 27.6); });
  sparkRing(add, t, 23.3, 25.0, PX - 30, GY - 290, 160, 14);
  for (let i = 0; i < 3; i++) add('fire' + (i % 2), place(310 + i * 90, GY + 40, .5 + .5 * burn), 28.6, 42.5, { a: .9 * (burn > .05 ? 1 : 0) });
  // Prahlad runs to them and prays
  const run = ss(seg(t, 32.1, 34.0));
  add('prahlad', place(lerp(PX + 60, 640, run), GY + 80, 1.1, -1), 32.0, END);
  add('vishnu', place(640, GY - 420, .45, -1), 35.6, 42.8, { a: .55, din: .8 });
  sparkRing(add, t, 40.9, 43.5, 390, GY - 240, 200, 16);
  sparkRise(add, t, 45.7, 49.2, 250, 700, GY - 300, 380, 16, 7);
  endCard(add, t, 49.6, 49.8);
  const cam = key(t, [[0, [540, 960, 1.04]], [8.1, [540, 960, 1.04]], [8.6, [540, 980, 1.0]], [20.2, [540, 980, 1.0]], [23.4, [600, 1000, 1.1]], [27.4, [600, 1000, 1.1]], [28.2, [540, 980, 1.0]], [49.5, [540, 980, 1.0]], [49.8, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 50.9, 51.5)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .5 * ss(seg(t, 14.5, 16)) * (1 - ss(seg(t, 31.5, 32.5))), drain: 0, flash: clamp(.55 * pulse(t, 24.21) + .4 * pulse(t, 42.9)), fade: clamp(fade) } };
}

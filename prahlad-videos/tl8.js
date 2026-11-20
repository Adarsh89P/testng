// Prahlad 8 — दैत्य बालकों को उपदेश (voice8.mp3, 45.2 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard } from './tlc.js';
export const DUR = 45.8, HOOK = [['दैत्यों के बच्चे', -52, 92], ['और भक्ति?', 66, 104]];
export const THUMB = { t: 38.0, top: ['कौन शत्रु?', 'कौन पराया?'], bottom: 'प्रह्लाद — भाग 8' };
export const CUES = splitCues([
  [0, .96, 'क्या आपको पता है...'], [1.35, 5.81, 'कि छोटे से प्रह्लाद ने दैत्यों के बच्चों को ही विष्णु-भक्ति सिखा दी थी?'],
  [6.57, 7.93, 'विष्णु पुराण के अनुसार,'], [8.24, 14.64, 'गुरु के आश्रम में जब गुरु बाहर जाते... तो प्रह्लाद अपने साथी दैत्य बालकों को बुलाकर समझाता।'],
  [15.35, 16.95, 'वह कहता — "मित्रो,'], [17.44, 19.66, 'बचपन, यौवन, बुढ़ापा —'], [20.30, 21.92, 'यह शरीर तो बदलता रहता है।'], [22.43, 24.39, 'सुख के पीछे भी दुःख छिपा है।'],
  [24.94, 28.96, 'पर जो भगवान विष्णु सबके भीतर बसते हैं — वे कभी नहीं बदलते।"'], [29.61, 31.68, 'और फिर उसने सबसे बड़ी बात कही —'],
  [32.19, 33.64, '"किसी से द्वेष मत करो।'], [34.07, 36.25, 'जब वही भगवान सब प्राणियों में हैं...'], [36.62, 38.55, 'तो कौन शत्रु? कौन पराया?"'],
  [39.23, 43.58, 'दैत्य कुल में जन्मे बालक... और सबके लिए मित्रता का संदेश।'], [44.10, 45.17, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 44.0, PX = 540;
  add('hook', place(540, 400), 1.35, 6.4);
  add('ground', place(0, GY), 0, END);
  add('tree0', place(120, GY + 40, .9), 0, END); add('tree1', place(980, GY + 40, .9, -1), 0, END);
  add('prahlad', place(PX, GY + 80, 1.1), .2, 17.3);
  const B = [[230, 'boy0', 1], [360, 'boy1', 1], [740, 'boy0', -1], [860, 'boy1', -1]];
  B.forEach(([x, id, s], i) => add(id, place(x, GY + 90, .9, s), 1.6 + i * .2, 17.3));
  add('purohit', place(lerp(300, -200, ss(seg(t, 8.4, 11.0))), GY + 80, .8, -1), 6.57, 11.0);
  sparkRing(add, t, 11.5, 14.6, PX, GY - 250, 160, 10);
  // the stages of life
  [[230, 'boy0', .75, 17.44], [540, 'deva0', .7, 18.4], [850, 'purohit', .8, 19.2]].forEach(([x, id, s, t0]) => add(id, place(x, GY + 80, s), t0, 24.6));
  add('cloud', place(540, GY - 820, .8), 22.43, 24.6, { a: .6 });
  // the One within all does not change
  add('prahlad', place(PX, GY + 80, 1.2), 24.6, END);
  add('vishnu', place(PX, GY - 440, .5), 24.94, 29.4, { a: .55, din: .8 });
  sparkRing(add, t, 24.94, 29.0, PX, GY - 260, 180, 14);
  // no enmity: the boys draw close
  const near = ss(seg(t, 32.2, 34.0));
  B.forEach(([x, id, s], i) => add(id, place(lerp(x, x + (PX - x) * .32, near), GY + 90, .9, s), 29.6, END));
  for (let i = 0; i < 5; i++) { const x = 200 + i * 170; sparkRing(add, t, 34.1 + i * .2, 38.6, x, GY - 140, 60, 6); }
  add('vishnu', place(PX, GY - 460, .42), 34.07, 38.8, { a: .4, din: .9 });
  sparkRise(add, t, 39.2, 43.6, 180, 900, GY - 200, 380, 20, 8);
  endCard(add, t, 44.0, 44.2);
  const cam = key(t, [[0, [540, 980, 1.0]], [17.0, [540, 980, 1.0]], [24.5, [540, 1000, .98]], [25.2, [540, 1040, 1.12]], [29.4, [540, 1040, 1.12]], [30.2, [540, 980, 1.0]], [43.9, [540, 980, 1.0]], [44.2, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 45.2, 45.8)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: 0, drain: .25 * ss(seg(t, 22.4, 23)) * (1 - ss(seg(t, 24.4, 25))), flash: clamp(.35 * pulse(t, 24.94) + .35 * pulse(t, 39.23)), fade: clamp(fade) } };
}

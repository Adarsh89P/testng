// Prahlad 10 — प्रह्लाद का वरदान (voice10.mp3, 53.6 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard, palace, hiranya, shake } from './tlc.js';
export const DUR = 54.2, HOOK = [['पिता के लिए', -52, 100], ['क्या माँगा?', 66, 104]];
export const THUMB = { t: 27.5, top: ['पिता के लिए', 'क्षमा माँगी!'], bottom: 'प्रह्लाद — भाग 10 (अंतिम)' };
export const CUES = splitCues([
  [0, .96, 'क्या आपको पता है...'], [1.40, 5.71, 'कि भगवान से वर माँगते समय प्रह्लाद ने अपने पिता के लिए क्या माँगा?'],
  [6.63, 10.37, 'विष्णु पुराण के अनुसार, भगवान विष्णु ने प्रसन्न होकर कहा —'], [10.96, 12.38, '"प्रह्लाद, वर माँगो।"'],
  [13.53, 15.47, 'प्रह्लाद ने पहला वर माँगा —'], [16.09, 22.07, '"हे प्रभु, मैं हज़ारों जन्म भी लूँ... तो हर जन्म में मेरी भक्ति आप में अटल रहे।"'],
  [23.04, 23.83, 'और दूसरा वर —'], [24.42, 28.57, '"मेरे पिता ने मुझसे जो द्वेष किया... उस पाप से वे मुक्त हो जाएँ।"'],
  [29.52, 34.89, 'जिस पिता ने उसे बार-बार मारने का प्रयास किया... उसी के लिए प्रह्लाद ने क्षमा माँगी।'],
  [35.67, 39.79, 'भगवान ने दोनों वर दिए, और कहा कि वह मुक्ति को भी प्राप्त होगा।'],
  [40.50, 46.75, 'बाद में भगवान ने नरसिंह रूप में हिरण्यकशिपु का अंत किया, और प्रह्लाद दैत्यों का राजा बना।'],
  [47.37, 52.00, 'यही है प्रह्लाद का रहस्य — अटूट भक्ति, और किसी से द्वेष नहीं।'], [52.55, 53.32, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 52.4;
  add('hook', place(540, 400), 1.40, 6.4);
  add('prahlad', place(700, GY + 80, 1.1, -1), .2, 6.4); add('hiranya', place(300, GY + 60, .9), 2.6, 6.4, { a: .55 });
  add('ground', place(0, GY), 0, 40.4);
  // Vishnu and Prahlad
  add('vishnu', place(330, GY + 60, 1.0), 6.63, 40.4, { din: .9 });
  add('prahlad', place(760, GY + 80, 1.15, -1), 6.63, 40.4);
  sparkRing(add, t, 10.96, 12.6, 330, GY - 460, 220, 14);
  // boon one: devotion in every birth
  for (let i = 0; i < 7; i++) add('lotusThrone', place(120 + i * 140, GY - 760 - 60 * Math.sin(i * 1.3), .3), 18.99 + i * .3, 22.6, { a: .8 });
  sparkRing(add, t, 16.1, 22.2, 760, GY - 240, 150, 12);
  // boon two: for his father
  add('hiranya', place(560, GY - 360, .55), 24.42, 34.9, { a: .5, din: 1.0 });
  sparkRing(add, t, 26.8, 34.9, 560, GY - 620, 160, 14);
  sparkRise(add, t, 29.5, 34.9, 440, 680, GY - 450, 420, 14, 9);
  sparkRing(add, t, 35.67, 39.8, 760, GY - 240, 220, 18);
  // Narasimha from the pillar; Prahlad crowned king
  palace(add, t, 40.4, 47.3);
  add('pillar', place(540, GY + 30, 1.1), 40.5, 42.0);
  add('narasimha', place(540, GY + 60 + rise(t, 41.6, .7, 160), 1.05, 1, shake(t, 41.6, 1.0, .04)), 41.6, 44.6);
  sparkRing(add, t, 41.6, 43.5, 540, GY - 460, 260, 18);
  add('throne', place(540, GY + 60, .95), 44.4, 47.3);
  add('prahlad', place(540, GY + 60, 1.1), 44.6, 47.3, { din: .6 });
  add('daitya0', place(220, GY + 70, .7, 1), 45.0, 47.3); add('daitya1', place(860, GY + 70, .7, -1), 45.2, 47.3);
  // the secret: devotion, and no hatred
  add('ground', place(0, GY), 47.3, END);
  add('vishnu', place(330, GY + 60, 1.0), 47.37, END);
  add('prahlad', place(760, GY + 80, 1.15, -1), 47.37, END);
  sparkRise(add, t, 49.5, 52.2, 200, 900, GY - 200, 400, 16, 10);
  endCard(add, t, 52.4, 52.6);
  const cam = key(t, [[0, [540, 960, 1.04]], [6.3, [540, 960, 1.04]], [6.9, [540, 980, 1.0]], [40.3, [540, 980, 1.0]], [41.4, [540, 1000, 1.08]], [44.4, [540, 1000, 1.08]], [45.0, [540, 980, 1.0]], [52.3, [540, 980, 1.0]], [52.6, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 53.6, 54.2)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .6 * ss(seg(t, 41.4, 41.8)) * (1 - ss(seg(t, 43.8, 44.6))), drain: 0, flash: clamp(.4 * pulse(t, 10.96) + .7 * pulse(t, 41.6) + .3 * pulse(t, 44.6)), fade: clamp(fade) } };
}

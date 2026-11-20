// Prahlad 7 — विष, ऊँचाई और माया (voice7.mp3, 47.2 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard, palace, hiranya, hash } from './tlc.js';
export const DUR = 47.7, HOOK = [['किसने', -52, 110], ['थामा?', 66, 110]];
export const THUMB = { t: 26.0, top: ['धरती माता ने', 'थाम लिया!'], bottom: 'प्रह्लाद — भाग 7' };
export const CUES = splitCues([
  [0, .97, 'क्या आपको पता है...'], [1.40, 5.49, 'कि प्रह्लाद को महल की चोटी से फेंका गया, तो उसे किसने थामा?'],
  [6.24, 10.36, 'विष्णु पुराण के अनुसार, हिरण्यकशिपु ने रसोइयों को आदेश दिया —'], [10.81, 12.52, '"इसके भोजन में विष मिला दो।"'],
  [13.09, 15.97, 'पर प्रह्लाद ने भगवान का नाम लेकर भोजन किया...'], [16.33, 18.71, 'और वह विष भी बिना हानि के पच गया।'],
  [19.84, 23.39, 'फिर उसे महल की सबसे ऊँची छत से नीचे फेंक दिया गया।'], [23.99, 27.90, 'पर धरती माता ने स्वयं उस बालक को अपनी गोद में थाम लिया।'],
  [28.67, 32.13, 'तब मायावी शंबरासुर ने अपनी हज़ारों मायाएँ फैलाईं।'], [32.61, 38.05, 'पर भगवान का सुदर्शन चक्र प्रकट हुआ... और एक-एक करके सारी मायाएँ नष्ट हो गईं।'],
  [38.54, 41.03, 'और जब वायु को उसे सुखा देने भेजा गया...'], [41.40, 45.40, 'तो उसके हृदय में बसे भगवान ने उस वायु को भी शांत कर दिया।'], [46.01, 46.82, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 45.9, PX = 540;
  add('pillar', place(540, GY + 30, 1.0), .2, 6.0);
  add('prahlad', place(560, GY - 1000 + 900 * ss(seg(t, 2.0, 4.0)), .8, 1, -.6 * (1 - ss(seg(t, 2, 4)))), 1.4, 6.0);
  add('bhudevi', place(560, GY + 90, .9), 4.4, 6.0, { a: .8 });
  add('hook', place(540, 400), 1.40, 6.0);
  palace(add, t, 6.0, 28.4);
  hiranya(add, t, 220, GY + 60, .9, 1, lerp(.1, -1.6, ss(seg(t, 10.8, 11.3))), 6.24, 13.0);
  add('daitya0', place(820, GY + 70, .7, -1), 7.5, 13.0);
  add('bowl', place(760, GY - 120, 1.0), 10.81, 13.0);
  // the poisoned meal
  add('prahlad', place(PX, GY + 80, 1.15), 13.0, 19.4);
  add('bowl', place(PX + 90, GY - 230, .8), 13.09, 16.4);
  sparkRing(add, t, 13.6, 18.6, PX, GY - 250, 160, 12);
  // thrown from the highest roof; Earth catches him
  const fall = ss(seg(t, 21.0, 24.4));
  add('pillar', place(540, GY + 30, 1.25), 19.84, 28.4);
  add('prahlad', place(560, lerp(GY - 1150, GY - 80, fall), .85, 1, lerp(0, 1.6, fall)), 19.84, 24.6);
  add('bhudevi', place(540, GY + 90 + rise(t, 23.4, 1.0, 400), 1.05), 23.4, 28.4, { din: .9 });
  add('prahlad', place(680, GY - 330, .62, 1, -1.45), 24.4, 28.4);
  sparkRing(add, t, 24.0, 27.6, 560, GY - 260, 190, 14);
  // Shambara's illusions; the Sudarshan chakra cuts them down
  add('ground', place(0, GY), 28.4, END);
  add('prahlad', place(PX, GY + 80, 1.1), 28.5, END);
  add('shambara', place(220, GY + 80, .95), 28.67, 38.2);
  for (let i = 0; i < 6; i++) { const cut = 33.6 + i * .7, x = 120 + (i % 3) * 400 + (i > 2 ? 160 : 0), y = GY - 420 - (i > 2 ? 250 : 0); add('smoke' + (i % 2), place(x, y, 1.0 + .2 * Math.sin(t + i)), 29.0 + i * .25, cut, { a: .85 }); add('shambara', place(x, y + 300, .5, i % 2 ? -1 : 1), 29.4 + i * .25, cut, { a: .45 }); sparkRing(add, t, cut, cut + .5, x, y + 100, 90, 6); }
  const cx = lerp(PX, 900, ss(seg(t, 33.0, 37.6))), cy = GY - 600 + 200 * Math.sin((t - 32.6) * 2.2);
  add('chakra', place(cx, cy, 1.4, 1, t * 9), 32.61, 38.2, { din: .5 });
  // the wind is calmed
  for (let i = 0; i < 4; i++) { const calm = ss(seg(t, 42.0, 44.0)); add('cloud', place(-200 + ((t - 38.5) * 260 * (1 - calm) + i * 330) % 1500, GY - 700 + i * 120, .7), 38.54, 44.5, { a: .7 * (1 - calm) }); }
  add('vishnu', place(PX, GY - 420, .45), 41.40, 45.6, { a: .55, din: .8 });
  sparkRing(add, t, 41.4, 45.4, PX, GY - 240, 120, 12);
  endCard(add, t, 45.9, 46.1);
  const cam = key(t, [[0, [540, 960, 1.04]], [5.9, [540, 960, 1.04]], [6.4, [540, 980, 1.0]], [19.6, [540, 980, 1.0]], [20.4, [540, 760, 1.05]], [23.6, [540, 1000, 1.0]], [28.3, [540, 980, 1.0]], [45.8, [540, 980, 1.0]], [46.1, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 47.1, 47.7)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .5 * ss(seg(t, 10.7, 11.4)) * (1 - ss(seg(t, 13, 14))) + .4 * ss(seg(t, 28.6, 29.5)) * (1 - ss(seg(t, 36, 38))), drain: .3 * ss(seg(t, 38.5, 39.5)) * (1 - ss(seg(t, 42, 43.5))), flash: clamp(.4 * pulse(t, 24.0) + .45 * pulse(t, 32.61)), fade: clamp(fade) } };
}

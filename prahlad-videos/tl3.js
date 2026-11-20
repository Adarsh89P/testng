// Prahlad 3 — शस्त्र और सर्प (voice3.mp3, 47.5 s)
import { mul, T, GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard, palace, hiranya, hash } from './tlc.js';
export const DUR = 48.1, HOOK = [['पहला', -52, 110], ['आदेश', 66, 110]];
export const THUMB = { t: 33.0, top: ['सर्पों के दाँत', 'टूट गए!'], bottom: 'प्रह्लाद — भाग 3' };
export const CUES = splitCues([
  [0, .96, 'क्या आपको पता है...'], [1.43, 6.10, 'कि हिरण्यकशिपु ने अपने ही पुत्र को मारने का पहला आदेश किसे दिया था?'],
  [6.93, 8.24, 'विष्णु पुराण के अनुसार,'], [8.49, 11.39, 'जब प्रह्लाद बार-बार विष्णु का नाम लेता रहा...'], [11.82, 14.37, 'तो दैत्यराज ने अपने दैत्यों को आज्ञा दी —'], [14.76, 15.65, '"इसे मार डालो!"'],
  [16.61, 19.95, 'सैकड़ों दैत्य शस्त्र लेकर उस बालक पर टूट पड़े।'], [20.56, 25.22, 'पर प्रह्लाद शांत खड़ा रहा, मन में श्रीहरि का स्मरण करता हुआ...'], [25.69, 28.46, 'और एक भी शस्त्र उसे चोट न पहुँचा सका।'],
  [29.07, 30.90, 'तब बुलाए गए विषैले सर्प।'], [31.33, 33.43, 'उन्होंने बालक को चारों ओर से डसा...'], [33.90, 37.33, 'पर उनके दाँत टूट गए, और प्रह्लाद को कुछ नहीं हुआ।'],
  [37.95, 42.61, 'जिसके हृदय में स्वयं विष्णु बसते हों... उसे कौन-सा शस्त्र छू सकता है?'], [43.51, 45.87, 'अगले भाग में — दिशाओं के हाथी।'], [46.43, 47.20, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 46.3;
  add('hook', place(540, 400), 1.43, 6.8);
  hiranya(add, t, 320, GY + 80, 1.0, 1, -1.5, .2, 6.8);
  add('prahlad', place(800, GY + 80, 1.1, -1), 1.0, 6.8);
  palace(add, t, 6.8, END);
  const PX = 560;
  add('prahlad', place(PX, GY + 80, 1.2, -1), 7.0, END);
  hiranya(add, t, 200, GY + 60, .9, 1, lerp(.1, -1.6, eo2(seg(t, 14.6, 15.0))), 8.49, 16.4);
  // the daityas charge with weapons; nothing touches him
  const charge = ss(seg(t, 16.6, 18.6)), recoil = ss(seg(t, 26.0, 28.3));
  const strike = t > 20.5 && t < 26 ? Math.max(0, Math.sin((t - 20.5) * 5)) * 30 : 0;
  [[-1, 'daitya0', 0], [-1, 'daitya1', 1], [1, 'daitya0', 2], [1, 'daitya1', 3]].forEach(([side, id, k]) => {
    const x0 = PX + side * (520 + (k % 2) * 120), x1 = PX + side * (170 + (k % 2) * 110) - side * strike;
    add(id, place(lerp(lerp(x0, x1, charge), x0, recoil), GY + 70, .78 - (k % 2) * .06, side < 0 ? 1 : -1, side * -.08), 16.61, 28.9);
  });
  for (let i = 0; i < 8; i++) { const st = 20.6 + i * .6; sparkRing(add, t, st, st + .4, PX + (i % 2 ? 90 : -90), GY - 220 + (i % 3) * 30, 50, 5); }
  // the serpents strike; their fangs break
  [[-260, 0], [260, 1], [-130, 2], [130, 0]].forEach(([dx, v], k) => { const t0 = 29.07 + k * .15, sink = ss(seg(t, 35.6, 37.0)), lunge = t > 31.3 && t < 33.9 ? 30 * Math.sin((t - 31.3) * 6) : 0; add('naga' + v, place(PX + dx - Math.sign(dx) * lunge, GY + 120 + rise(t, t0, .7, 300) + sink * 400, .8, dx > 0 ? -1 : 1), t0, 37.0); });
  sparkRing(add, t, 33.9, 35.4, PX, GY - 200, 200, 14);
  // the One in his heart
  add('vishnu', place(PX, GY - 380, .5), 37.95, 42.8, { a: .55, din: .8 });
  sparkRing(add, t, 37.95, 42.6, PX, GY - 240, 100, 10);
  add('airavata.body', place(900, GY + 100, .7, -1), 43.51, 46.2); add('airavata.trunk', mul(place(900, GY + 100, .7, -1), T(266, -212)), 43.51, 46.2);
  endCard(add, t, 46.2, 46.4);
  const cam = key(t, [[0, [540, 960, 1.04]], [6.7, [540, 960, 1.04]], [7.3, [540, 980, 1.0]], [16.4, [540, 980, 1.0]], [20.5, [560, 1020, 1.1]], [28.5, [560, 1020, 1.1]], [29.4, [560, 1040, 1.15]], [37.5, [560, 1040, 1.15]], [38.2, [540, 980, 1.0]], [46.2, [540, 980, 1.0]], [46.5, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 47.5, 48.1)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .6 * ss(seg(t, 14.6, 15.4)) * (1 - ss(seg(t, 27.8, 28.8))), drain: 0, flash: clamp(.4 * pulse(t, 33.9) + .3 * pulse(t, 37.95)), fade: clamp(fade) } };
}
function eo2(u) { return 1 - Math.pow(1 - u, 3); }

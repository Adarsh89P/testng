// Short 9 — इंद्र की स्तुति और माँ लक्ष्मी का वरदान (voice9.mp3, 50.4 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, seaBack, seaFront, sparkRise, sparkRing, endCard, mul, T, R } from './tlc.js';
import { indra } from './chars.js';
export const DUR = 51.0, HOOK = [['माँ लक्ष्मी का', -52, 100], ['वरदान', 66, 110]];
export const THUMB = { t: 36.6, top: ['माँ लक्ष्मी के', '2 वरदान'], bottom: 'समुद्र मंथन — अंतिम भाग' };
export const CUES = splitCues([
  [0, .99, 'क्या आपको पता है...'], [1.44, 6.04, 'कि समुद्र मंथन की कथा के अंत में माँ लक्ष्मी ने कौन-सा वरदान दिया था?'],
  [7.03, 8.41, 'विष्णु पुराण के अनुसार,'], [8.65, 11.33, 'जब देवताओं ने दैत्यों को पराजित कर दिया...'], [11.73, 14.44, 'तो इंद्र फिर से स्वर्ग के सिंहासन पर बैठे।'], [14.98, 18.38, 'और उन्होंने विनम्र होकर माँ लक्ष्मी की स्तुति की।'],
  [19.66, 21.22, 'प्रसन्न होकर माँ ने कहा —'], [21.74, 22.37, '"वर माँगो।"'], [23.09, 24.48, 'इंद्र ने दो वर माँगे।'],
  [25.03, 25.40, 'पहला —'], [25.96, 28.98, '"हे माँ, आप तीनों लोकों को कभी न छोड़ें।"'], [29.58, 30.04, 'दूसरा —'], [30.58, 35.05, '"जो भी इस स्तुति से आपका स्मरण करे, आप उससे कभी विमुख न हों।"'],
  [35.83, 37.62, 'माँ लक्ष्मी ने दोनों वर दे दिए।'], [38.18, 40.83, 'एक माला के अपमान से श्री चली गई थी...'], [41.29, 45.10, 'और विनम्रता से शरण में जाने पर, वह सदा के लिए लौट आई।'],
  [45.60, 48.74, 'यही है समुद्र मंथन का सबसे बड़ा रहस्य।'], [49.28, 50.11, 'जय श्री हरि।']]);
const IN = indra();
export function frame(t) {
  const items = [], add = adder(items, t), END = 45.4;
  // hook: Lakshmi on her lotus
  add('lotusThrone', place(540, GY + 140, .9), .2, 6.8, { din: .7 });
  add('lakshmi', place(540, GY + 20, .95), .4, 6.8, { din: .7 });
  sparkRing(add, t, 1.0, 6.8, 540, GY - 330, 230, 12);
  add('hook', place(540, 400), 1.44, 6.8);
  // svarga: clouds; the devas victorious, the daityas gone
  add('cloud', place(220, 560, 1.0), 7.0, END); add('cloud', place(880, 640, .9), 7.2, END); add('cloud', place(560, 330, .7), 7.4, END);
  const flee = ss(seg(t, 8.65, 10.8));
  add('daitya0', place(160, GY + 60 + flee * 700, .7, 1, .3 * flee), 7.03, 11.0); add('daitya1', place(60, GY + 60 + flee * 700, .66, 1, .3 * flee), 7.03, 11.0);
  add('deva0', place(720, GY + 60, .66, -1), 7.03, 11.6); add('deva1', place(860, GY + 60, .62, -1), 7.2, 11.6);
  // Indra on his throne, praising Lakshmi
  const TH = [360, GY + 80], tS = .95, bow = ss(seg(t, 15.0, 15.8)) * .14 * (1 - ss(seg(t, 22.6, 23.2)));
  add('throne', place(TH[0], TH[1], tS), 11.73, END);
  const seat = [TH[0] + 10, TH[1] - 60 * tS], MI = place(seat[0], seat[1], 1.0, 1, bow);
  let armR = .15; armR = lerp(armR, -.9, ss(seg(t, 15.0, 15.8))); armR = lerp(armR, -1.9, ss(seg(t, 23.1, 23.8))); armR = lerp(armR, -.9, ss(seg(t, 35.8, 36.6)));
  add('indra.body', MI, 11.73, END); add('indra.arm', mul(mul(MI, T(...IN.shoulder)), R(armR)), 11.73, END);
  const LK = [800, GY + 40];
  add('lotusThrone', place(LK[0], LK[1] + 90, .6), 14.98, END, { din: .7 });
  add('lakshmi', place(LK[0], LK[1], .78, -1), 15.1, END, { din: .7 });
  sparkRing(add, t, 19.66, 22.6, LK[0], LK[1] - 300, 180, 12);
  // boon 1: never leave the three worlds — a burst of light in sky, earth and below
  [[540, 380, 25.96], [540, 900, 26.8], [540, 1560, 27.6]].forEach(([x, y, t0]) => sparkRing(add, t, t0, 29.2, x, y, 140, 10));
  // boon 2: whoever praises her with this hymn
  add('pothi', place(540, 560, .85), 30.58, 35.6, { din: .6 });
  sparkRise(add, t, 31.0, 35.0, 300, 780, 700, 300, 14, 2);
  // the boons granted: a shower of gold
  for (let i = 0; i < 18; i++) { const st = 35.9 + (i * .17) % 1.6; if (t < st || t > st + 1.6) continue; const u = (t - st) / 1.6; add('spark', place(LK[0] - 60 + (i * 37) % 160, LK[1] - 380 + u * 420, 1.1, 1, t * 3 + i), st, st + 1.4, { a: Math.sin(u * Math.PI), din: .1 }); }
  // the garland: once insulted, now restored
  const rest = ss(seg(t, 41.29, 43.0));
  add('garlandL', place(540, GY + 240 - rest * 120, 1.5), 38.18, END, { din: .6 });
  sparkRing(add, t, 43.0, END, 540, GY + 150, 160, 10);
  // the secret: Vishnu and Lakshmi together
  endCard(add, t, 45.60, 45.9, true);
  const cam = key(t, [[0, [540, 960, 1.04]], [6.8, [540, 960, 1.04]], [7.5, [540, 960, 1.0]], [14.6, [540, 960, 1.0]], [15.6, [600, 1000, 1.08]], [24.6, [600, 1000, 1.08]], [25.4, [540, 960, 1.0]], [45.4, [540, 960, 1.0]], [45.9, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 50.4, 51.0)) + (1 - ss(seg(t, 0, .25)));
  const drain = .7 * ss(seg(t, 38.18, 39.0)) * (1 - ss(seg(t, 41.29, 42.4)));
  return { items, cam, lamps: [], mood: { anger: 0, drain, flash: clamp(.35 * pulse(t, 19.66) + .3 * pulse(t, 35.83) + .45 * pulse(t, 43.0)), fade: clamp(fade) } };
}

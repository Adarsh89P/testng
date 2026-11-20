// Prahlad 5 — अग्नि परीक्षा, होलिका कहाँ? (voice5.mp3, 48.9 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard, palace, hiranya, hash } from './tlc.js';
export const DUR = 49.5, HOOK = [['होलिका', -52, 110], ['कहाँ?', 66, 110]];
export const THUMB = { t: 31.0, top: ['अग्नि बनी', 'शीतल कमल!'], bottom: 'प्रह्लाद — भाग 5' };
export const CUES = splitCues([
  [0, .92, 'क्या आपको पता है...'], [1.29, 6.39, 'कि विष्णु पुराण में प्रह्लाद को जलाने की कथा में होलिका का नाम ही नहीं आता?'],
  [7.34, 10.03, 'विष्णु पुराण के अनुसार, हाथी हार गए...'], [10.56, 15.48, 'तो दैत्यराज ने आदेश दिया — "लकड़ियों का पहाड़ बनाओ, और इसे अग्नि में डाल दो!"'],
  [17.25, 22.34, 'दैत्यों ने प्रह्लाद को लकड़ियों के बीच रखा, और वायु से अग्नि को प्रचंड कर दिया।'], [22.86, 24.56, 'ज्वालाएँ आकाश तक उठीं...'],
  [25.17, 27.16, 'पर प्रह्लाद बोला — "पिताजी,'], [27.54, 33.10, 'यह अग्नि मुझे ऐसी लग रही है... जैसे चारों ओर शीतल कमल की पंखुड़ियाँ बिछी हों।"'],
  [34.10, 38.25, 'होलिका की प्रसिद्ध कथा बाद के ग्रंथों और लोक-परंपरा में मिलती है।'], [38.71, 43.12, 'पर विष्णु पुराण में — स्वयं अग्नि ही विष्णु-भक्त को नहीं जला सकी।'],
  [43.92, 47.32, 'एक ही कथा... अलग-अलग ग्रंथों में अलग-अलग रूप।'], [47.84, 48.65, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 47.5, PX = 540;
  add('hook', place(540, 400), 1.29, 7.0);
  add('pothi', place(540, GY - 60, .9), .3, 7.0);
  add('fire0', place(540, GY + 60, .8), 3.0, 7.0, { a: .8 });
  palace(add, t, 7.0, 34.0);
  hiranya(add, t, 240, GY + 60, .95, 1, lerp(.1, -1.8, ss(seg(t, 10.6, 11.2))), 7.34, 16.9);
  add('prahlad', place(780, GY + 80, 1.0, -1), 7.34, 16.9);
  add('daitya0', place(900, GY + 70, .7, -1), 9.0, 10.3);
  // the pyre; fire roars; the boy sits calm
  add('woodpile', place(PX, GY + 70, 1.1), 17.25, 34.0, { din: .8 });
  add('prahlad', place(PX, GY - 60, .95), 17.6, 34.0);
  add('daitya0', place(200, GY + 70, .75, 1), 17.25, 22.6); add('daitya1', place(880, GY + 70, .75, -1), 17.25, 22.6);
  const grow = ss(seg(t, 20.0, 24.5)), cool = ss(seg(t, 27.6, 31.0));
  for (let i = 0; i < 6; i++) { const x = PX + (i - 2.5) * 95, s = (.6 + .5 * grow + .1 * Math.sin(t * 9 + i)) * (1 - cool); if (s > .05) add('fire' + (i % 2), place(x, GY - 10 - 40 * (i % 2), s), 19.8 + i * .12, 34.0, { a: .95 }); }
  sparkRise(add, t, 20.1, 27.6, 380, 700, GY - 200, 600, 22, 5);
  add('lotusThrone', place(PX, GY - 20, .85), 28.6, 34.0, { a: cool });
  for (let i = 0; i < 16; i++) { const a = i / 16 * 6.283, r = 210 + 40 * Math.sin(i * 2.1); add('petal', place(PX + Math.cos(a) * r, GY - 160 + Math.sin(a) * r * .6, 1.8, 1, t * .3 + i), 29.0 + i * .1, 34.0); }
  add('vishnu', place(PX, GY - 520, .42), 29.8, 33.8, { a: .5, din: .9 });
  // texts compared
  add('ground', place(0, GY), 34.0, END);
  add('pothiL', place(540, GY - 700, 1.4), 34.10, 43.4);
  add('pothiV', place(540, GY - 380, 1.4), 38.71, 43.4);
  add('prahlad', place(540, GY + 80, .95), 40.31, 43.4);
  sparkRing(add, t, 40.31, 43.1, 540, GY - 200, 130, 10);
  add('pothiV', place(540, GY - 720, 1.3), 43.92, END); add('pothiL', place(540, GY - 470, 1.3), 44.3, END); add('pothi', place(540, GY - 220, 1.3), 44.7, END);
  endCard(add, t, 47.5, 47.7);
  const cam = key(t, [[0, [540, 960, 1.04]], [6.8, [540, 960, 1.04]], [7.4, [540, 980, 1.0]], [16.9, [540, 980, 1.0]], [22.5, [540, 1000, 1.06]], [33.6, [540, 1000, 1.06]], [34.2, [540, 980, 1.0]], [47.4, [540, 980, 1.0]], [47.7, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 48.9, 49.5)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .55 * ss(seg(t, 10.5, 11.3)) * (1 - ss(seg(t, 26.5, 28))), drain: 0, flash: clamp(.45 * pulse(t, 28.0) + .3 * pulse(t, 40.31)), fade: clamp(fade) } };
}

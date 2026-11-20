// Prahlad 9 — समुद्र की गहराई में (voice9.mp3, 50.7 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard, palace, hiranya } from './tlc.js';
export const DUR = 51.3, HOOK = [['समुद्र में', -52, 104], ['बंदी?', 66, 110]];
export const THUMB = { t: 44.0, top: ['समुद्र से निकले', 'भगवान विष्णु!'], bottom: 'प्रह्लाद — भाग 9' };
export const CUES = splitCues([
  [0, .94, 'क्या आपको पता है...'], [1.36, 6.97, 'कि प्रह्लाद को नागपाश में बाँधकर समुद्र में डाला गया, और ऊपर पर्वत रख दिए गए थे?'],
  [7.59, 10.56, 'विष्णु पुराण के अनुसार, सारे उपाय विफल हुए...'], [11.12, 13.44, 'तो हिरण्यकशिपु ने अंतिम आदेश दिया।'], [13.99, 16.40, 'प्रह्लाद को नागों के पाश से बाँधा गया,'],
  [16.77, 21.83, 'समुद्र में फेंका गया... और उसके ऊपर हज़ारों योजन ऊँचे पर्वत रख दिए गए।'],
  [22.75, 27.89, 'समुद्र की गहराई में, अंधकार में... प्रह्लाद ने भगवान की स्तुति की।'], [28.47, 32.93, 'वह इतना ध्यान-मग्न हुआ कि स्वयं को भगवान से अलग ही न समझ सका।'],
  [33.45, 35.95, 'और उसी क्षण — नागपाश टूट गए।'], [36.35, 39.07, 'समुद्र में उथल-पुथल मची, पर्वत हट गए...'], [39.45, 41.01, 'और प्रह्लाद ऊपर उठ आया।'],
  [41.57, 45.58, 'तब पीतांबर धारी भगवान विष्णु स्वयं उसके सामने प्रकट हुए।'], [46.14, 48.99, 'अगले भाग में — प्रह्लाद ने क्या वरदान माँगा?'], [49.52, 50.39, 'जय श्री हरि।']]);
export function frame(t) {
  const items = [], add = adder(items, t), END = 49.4, PX = 540;
  add('hook', place(540, 400), 1.36, 7.4);
  add('ocean0', place(0, GY - 10), .2, 7.4); add('mountain', place(540, GY - 30, 1.0), 4.8, 7.4);
  add('ocean1', place(0, GY + 120), .2, 7.4);
  palace(add, t, 7.4, 16.6);
  hiranya(add, t, 230, GY + 60, .95, 1, lerp(.1, -1.7, ss(seg(t, 11.1, 11.6))), 7.59, 16.6);
  add('prahlad', place(780, GY + 80, 1.0, -1), 7.59, 16.6);
  add('wrap', place(780, GY - 120, .4, 1, -.1), 13.99, 16.6); add('wrap', place(780, GY - 200, .4, 1, .1), 14.3, 16.6);
  // thrown into the sea; mountains piled on the surface
  const sink = ss(seg(t, 16.9, 19.0)), SY = GY - 260;
  add('ocean0', place(0, SY), 16.6, 22.4);
  const py = lerp(SY - 700, SY + 500, sink);
  add('prahlad', place(PX, py, .8, 1, -.4 * sink), 16.77, 22.4); add('wrap', place(PX, py - 140, .35, 1, -.1), 16.77, 22.4); add('wrap', place(PX, py - 210, .35, 1, .1), 16.77, 22.4);
  for (let i = 0; i < 3; i++) { const d = ss(seg(t, 19.0 + i * .5, 20.2 + i * .5)); add('mountain', place(250 + i * 290, lerp(SY - 1300, SY + 20, d), .9), 18.8 + i * .5, 22.4); }
  add('ocean1', place(0, SY + 130), 16.6, 22.4);
  // in the dark depths: stillness and stuti (the surface and mountains far above)
  const lift = ss(seg(t, 36.4, 38.6)), sh = t > 36.35 && t < 39.5 ? 18 * Math.sin(t * 22) : 0;
  add('ocean0', place(-300 + sh, 330, 2.4), 22.4, 39.6);
  for (let i = 0; i < 3; i++) add('mountain', place(250 + i * 290 + lift * (i - 1) * 600, 350 - lift * 700, .9), 22.4, 39.2);
  const bound = 34.69, up = ss(seg(t, 39.45, 41.0));
  add('prahlad', place(PX, GY - 100 + 12 * Math.sin(t * 1.5) - up * 900, 1.2), 22.4, 41.0);
  add('wrap', place(PX, GY - 260, .38, 1, -.1), 22.4, bound + .2, { dout: .25 }); add('wrap', place(PX, GY - 330, .38, 1, .1), 22.4, bound + .2, { dout: .25 });
  sparkRing(add, t, 25.88, 33.4, PX, GY - 380, 150, 12);
  add('vishnu', place(PX, GY - 560, .5), 28.47, 33.4, { a: .45, din: 1.2 });
  sparkRing(add, t, 34.69, 36.4, PX, GY - 330, 240, 18);
  // risen: on the sea, before Vishnu
  add('ocean0', place(0, GY - 10 + 20 * Math.sin(t * 3)), 40.6, END);
  add('prahlad', place(PX + 150, GY + 70, 1.1, -1), 40.6, END, { din: .5 });
  add('vishnu', place(360, GY + 60, .95), 41.57, END, { din: .9 });
  add('ocean1', place(0, GY + 130 - 20 * Math.sin(t * 3)), 40.6, END);
  sparkRing(add, t, 41.6, 45.6, 360, GY - 420, 230, 16);
  add('lotusThrone', place(540, GY - 760, .6), 46.14, 49.0, { a: .8 });
  endCard(add, t, 49.4, 49.6);
  const cam = key(t, [[0, [540, 960, 1.04]], [7.3, [540, 960, 1.04]], [7.8, [540, 980, 1.0]], [21.8, [540, 980, 1.0]], [22.6, [540, 980, 1.0]], [33.0, [540, 1000, 1.06]], [36.4, [540, 980, 1.0]], [49.3, [540, 980, 1.0]], [49.6, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 50.7, 51.3)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .5 * ss(seg(t, 11, 12)) * (1 - ss(seg(t, 21.5, 22.5))), drain: .7 * ss(seg(t, 21.8, 23.0)) * (1 - ss(seg(t, 34.4, 35.4))), flash: clamp(.55 * pulse(t, 34.69) + .45 * pulse(t, 41.57)), fade: clamp(fade) } };
}

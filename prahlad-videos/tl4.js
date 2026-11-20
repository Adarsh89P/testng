// Prahlad 4 — दिशाओं के हाथी (voice4.mp3, 47.3 s)
import { mul, T, R, GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, sparkRise, sparkRing, endCard, palace, hiranya, shake } from './tlc.js';
export const DUR = 47.9, HOOK = [['दिग्गज बनाम', -52, 100], ['बालक', 66, 116]];
export const THUMB = { t: 31.2, top: ['हाथियों के दाँत', 'टूट गए!'], bottom: 'प्रह्लाद — भाग 4' };
export const CUES = splitCues([
  [0, .94, 'क्या आपको पता है...'], [1.35, 5.35, 'कि प्रह्लाद को कुचलने के लिए दिशाओं के महान हाथी बुलाए गए थे?'],
  [5.91, 9.28, 'विष्णु पुराण के अनुसार, शस्त्र और सर्प हार गए...'], [9.76, 11.45, 'तो हिरण्यकशिपु ने आदेश दिया —'], [11.97, 15.93, '"दिशाओं के दिग्गजों को बुलाओ! वे इसे अपने दाँतों से कुचल दें।"'],
  [17.64, 19.56, 'पर्वत जैसे विशाल हाथी आए।'], [19.98, 24.51, 'उन्होंने छोटे से बालक को धरती पर गिराया, और अपने दाँतों से दबाने लगे।'],
  [25.02, 29.05, 'पर प्रह्लाद ने आँखें बंद कीं... और भगवान गोविंद का स्मरण किया।'], [29.52, 32.19, 'और फिर — उन हाथियों के दाँत ही टूट गए।'],
  [32.73, 36.50, 'प्रह्लाद ने पिता से कहा — "पिताजी, यह मेरा बल नहीं है।'], [36.88, 40.37, 'यह उन जनार्दन का प्रभाव है, जिनका मैं स्मरण करता हूँ।"'],
  [40.97, 42.70, 'बल टूटा... भक्ति नहीं।'], [43.31, 45.59, 'अगले भाग में — अग्नि की परीक्षा।'], [46.09, 46.98, 'जय श्री हरि।']]);
const ele = (add, M, t0, t1, rot = 0, o) => { add('airavata.body', M, t0, t1, o); add('airavata.trunk', mul(mul(M, T(266, -212)), R(rot)), t0, t1, o); };
export function frame(t) {
  const items = [], add = adder(items, t), END = 45.9, PX = 540;
  add('hook', place(540, 400), 1.35, 5.8);
  ele(add, place(250, GY + 90, .8), .2, 5.8, .1 * Math.sin(t * 2)); ele(add, place(830, GY + 90, .8, -1), .2, 5.8, .1 * Math.sin(t * 2 + 1));
  add('prahlad', place(PX, GY + 80, 1.0), .5, 5.8);
  palace(add, t, 5.8, END);
  hiranya(add, t, 260, GY + 60, .95, 1, lerp(.1, -1.7, ss(seg(t, 11.9, 12.4))), 5.91, 17.4, { r: shake(t, 11.97, 1.2, .05) });
  add('prahlad', place(780, GY + 80, 1.0, -1), 5.91, 17.4);
  // the elephants of the quarters arrive; the boy is thrown down
  const come = ss(seg(t, 17.6, 19.6)), down = ss(seg(t, 20.2, 21.0)), press = t > 21 && t < 29.5 ? 18 * Math.sin((t - 21) * 4) : 0;
  const recoil = ss(seg(t, 30.4, 32.0));
  const ex = (side) => PX + side * (lerp(700, 300, come) - (t > 21 ? press : 0) + recoil * 160);
  const tr = t < 30.4 ? .25 + .1 * Math.sin(t * 4) : -.6 * recoil;
  ele(add, place(ex(-1), GY + 90 + rise(t, 17.6, .8, 60), 1.05, 1, -.05 + .1 * recoil), 17.64, 33.5, tr);
  ele(add, place(ex(1), GY + 90 + rise(t, 17.8, .8, 60), 1.05, -1, .05 - .1 * recoil), 17.64, 33.5, tr);
  add('prahlad', place(PX + 120 * down, GY + 80, 1.0, 1, lerp(0, -1.5, down)), 17.64, 32.6);
  sparkRing(add, t, 25.0, 29.4, PX + 200, GY - 60, 120, 12);
  add('vishnu', place(PX, GY - 520, .45), 27.1, 32.4, { a: .55, din: .8 });
  // tusks snap and fall
  [[-1, 0], [1, 1]].forEach(([s, k]) => { const f = ss(seg(t, 30.4, 31.6)); add('tusk', place(PX + s * (300 + f * 60), GY - 140 + f * 200, .9, -s, s * f * 2.4), 30.37, 33.5); });
  sparkRing(add, t, 30.37, 32.0, PX, GY - 120, 260, 16);
  // son speaks to father
  hiranya(add, t, 250, GY + 60, .95, 1, .1, 32.6, END);
  add('prahlad', place(760, GY + 80, 1.15, -1), 32.6, END);
  add('vishnu', place(760, GY - 400, .45, -1), 36.88, 40.6, { a: .55, din: .8 });
  sparkRise(add, t, 40.97, 42.9, 650, 870, GY - 200, 300, 12, 4);
  add('fire0', place(820, GY + 40, 1.0), 43.31, 45.9, { a: .9 });
  endCard(add, t, 45.9, 46.1);
  const cam = key(t, [[0, [540, 960, 1.04]], [5.6, [540, 960, 1.04]], [6.2, [540, 980, 1.0]], [17.3, [540, 980, 1.0]], [19.6, [540, 1000, .98]], [24.5, [540, 1060, 1.12]], [30.2, [540, 1060, 1.12]], [30.6, [540, 1040, 1.06]], [32.4, [540, 980, 1.0]], [45.8, [540, 980, 1.0]], [46.1, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 47.3, 47.9)) + (1 - ss(seg(t, 0, .25)));
  return { items, cam, lamps: [], mood: { anger: .6 * ss(seg(t, 11.8, 12.6)) * (1 - ss(seg(t, 29.2, 30.2))), drain: .25 * ss(seg(t, 20, 21)) * (1 - ss(seg(t, 25, 26))), flash: clamp(.55 * pulse(t, 30.37) + .3 * pulse(t, 40.97)), fade: clamp(fade) } };
}

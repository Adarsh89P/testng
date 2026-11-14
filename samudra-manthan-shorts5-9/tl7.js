// Short 7 — माँ लक्ष्मी का प्राकट्य (voice7.mp3, 59.6 s)
import { GY, lerp, seg, ss, clamp, place, pulse, adder, key, rise, splitCues, seaBack, seaFront, sparkRise, sparkRing, endCard, mul, T, R, ap } from './tlc.js';
import { airavata } from './chars.js';
export const DUR = 60.2, HOOK = [['सबसे महान', -52, 104], ['रत्न', 66, 110]];
export const THUMB = { t: 33.0, top: ['समुद्र मंथन का', 'सबसे महान रत्न'], bottom: 'माँ लक्ष्मी का प्राकट्य' };
export const CUES = splitCues([
  [0, .98, 'क्या आपको पता है...'], [1.49, 4.79, 'कि समुद्र मंथन से जो सबसे महान रत्न निकला,'], [5.17, 6.64, 'वह स्वयं माँ लक्ष्मी थीं?'],
  [7.35, 8.74, 'विष्णु पुराण के अनुसार,'], [9.14, 9.99, 'अमृत के बाद...'], [10.36, 13.24, 'क्षीरसागर से खिले हुए कमल पर विराजमान,'], [13.67, 17.44, 'हाथों में कमल लिए, अपूर्व सौंदर्य से दमकती हुई —'], [17.87, 19.21, 'देवी श्री प्रकट हुईं।'],
  [20.89, 23.57, 'महर्षियों ने श्रीसूक्त से उनकी स्तुति की।'], [24.06, 27.15, 'गंधर्व गाने लगे, अप्सराएँ नाचने लगीं।'], [27.63, 30.50, 'गंगा आदि नदियाँ स्नान के लिए जल लेकर आईं,'],
  [30.73, 35.06, 'और दिशाओं के दिग्गजों ने सोने के कलशों से उनका अभिषेक किया।'], [35.72, 39.53, 'क्षीरसागर ने उन्हें कभी न मुरझाने वाले कमलों की माला दी,'], [39.93, 42.34, 'और विश्वकर्मा ने दिव्य आभूषण।'],
  [42.96, 45.28, 'और फिर, सबके देखते-देखते...'], [45.70, 49.78, 'माँ लक्ष्मी ने भगवान विष्णु के वक्षस्थल पर अपना स्थान लिया।'], [50.41, 53.17, 'जो श्री एक माला के अपमान से चली गई थी...'], [53.63, 54.42, 'वही लौट आई।'],
  [55.16, 56.16, 'पूरी कथा देखिए —'], [56.56, 58.15, 'समुद्र मंथन के रहस्य।'], [58.67, 59.40, 'जय श्री हरि।']]);
const EL = airavata();
export function frame(t) {
  const items = [], add = adder(items, t), END = 54.9;
  seaBack(add, t, .1, END);
  add('hook', place(540, 400), 1.49, 6.9);
  add('lotusThrone', place(540, 1180, .75), .2, 6.9, { din: .7 });
  sparkRing(add, t, 1.0, 6.9, 540, 1080, 200, 10);
  add('lakshmi', place(540, 1100, .62), 5.17, 6.9, { din: .4, a: .9 });
  // the lotus rises from the milk, and the goddess appears upon it
  const toV = ss(seg(t, 45.7, 48.8)), lx = lerp(540, 640, toV);
  add('lotusThrone', place(lx, GY + 70 + rise(t, 10.36, 1.4, 380), 1.0), 10.36, 50.2, { din: .8 });
  const LK = [lx, GY - 60];
  add('lakshmi', place(LK[0], LK[1], .95), 17.87, 50.2, { din: .7 });
  sparkRing(add, t, 13.7, 17.5, 540, GY - 120, 200, 10);
  // maharshis praise her with the Shri Sukta
  for (const [x, sx] of [[170, 1], [910, -1]]) { const M = place(x, GY + 80, .62, sx); add('durvasa.body', M, 20.89, 23.9); add('durvasa.arm', mul(mul(M, T(14, -388)), R(-2.4)), 20.89, 23.9); }
  // gandharvas sing, apsaras dance
  add('deva0', place(300, GY + 60, .55), 24.06, 27.5); add('deva1', place(780, GY + 60, .55, -1), 24.2, 27.5);
  add('apsara', place(150, GY + 80, .58, 1, .07 * Math.sin(t * 3)), 24.4, 27.5); add('apsara2', place(930, GY + 80, .58, -1, -.07 * Math.sin(t * 3)), 24.6, 27.5);
  // the Ganga and the rivers bring water
  add('river', place(250, 260, 1.0, 1, -.42), 27.63, 30.6, { din: .8 });
  // the elephants of the quarters pour from golden vessels
  for (const [x, sx] of [[140, 1], [940, -1]]) {
    const ME = place(x, GY + 120, .55, sx), MT = mul(mul(ME, T(...EL.trunkBase)), R(-2.5 + .08 * Math.sin(t * 2))), tip = ap(MT, EL.trunkTip);
    add('airavata.body', ME, 30.73, 35.3); add('airavata.trunk', MT, 30.73, 35.3);
    add('kalash', place(tip[0], tip[1] - 20, .7, 1, sx * 1.1), 31.0, 35.3);
    const ang = Math.atan2(LK[1] - 420 - tip[1], LK[0] - tip[0]) - Math.PI / 2;
    add('stream', place(tip[0] + sx * 30, tip[1], 1.2, 1, ang), 31.6, 35.3, { din: .4 });
  }
  // the ocean's garland of unfading lotuses, then Vishwakarma's ornaments
  const gU = ss(seg(t, 36.0, 38.6)), neck = [LK[0] + 6, LK[1] - 380];
  add('garland', place(lerp(540, neck[0], gU), lerp(GY + 200, neck[1], gU), lerp(1.2, .75, gU)), 35.72, 50.2, { din: .6 });
  sparkRing(add, t, 39.9, 42.4, LK[0], LK[1] - 330, 170, 14);
  // she goes to Vishnu
  add('vishnu', place(820, GY + 80, .92, -1), 43.0, END, { din: .7 });
  add('lakshmi', place(660, GY + 70, .88), 50.2, END, { din: .01 });
  sparkRing(add, t, 48.6, 50.4, 720, GY - 300, 240, 14);
  // the garland's insult… and Shri returns
  const back = ss(seg(t, 53.63, 54.2));
  add('garlandL', place(540, GY + 220 - back * 60, 1.4), 50.41, END, { din: .6 });
  sparkRing(add, t, 53.63, END, 540, GY + 170, 150, 10);
  seaFront(add, t, .1, END);
  endCard(add, t, 55.16, 56.56, true);
  const cam = key(t, [[0, [540, 960, 1.04]], [6.8, [540, 960, 1.04]], [7.6, [540, 1000, 1.0]], [17.5, [540, 980, 1.06]], [19.2, [540, 900, 1.15]], [20.8, [540, 940, 1.0]], [42.7, [540, 940, 1.0]], [45.0, [640, 960, 1.05]], [50.2, [700, 940, 1.1]], [50.6, [540, 1000, 1.0]], [54.9, [540, 1000, 1.0]], [55.4, [540, 960, 1.05]]]);
  const fade = ss(seg(t, 59.6, 60.2)) + (1 - ss(seg(t, 0, .25)));
  const drain = .7 * ss(seg(t, 50.41, 51.2)) * (1 - ss(seg(t, 53.63, 54.3)));
  return { items, cam, lamps: [], mood: { anger: 0, drain, flash: clamp(.45 * pulse(t, 17.87) + .3 * pulse(t, 48.8) + .4 * pulse(t, 53.63)), fade: clamp(fade) } };
}

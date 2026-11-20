// Prahlad series characters (same shape language as chars.js).
import { S, P, L, E, C, B, X, curve, face, hairBack, crownTall, earring, neck, PI } from './chars.js';

// —— Hiranyakashipu: the daitya king. Dark skin, fierce solid face, spiked gold crown, crimson and gold. Origin at the feet ——
export function hiranyakashipu() {
  const N = [8, -420], k = 1.6, sh = [];
  sh.push({ p: B([[-12, -396], [-40, -320], [-46, -250]], 26, 20), c: 'skinD' }); sh.push({ p: C(-46, -244, 13), c: 'skinD' });
  sh.push({ p: B([[-46, -250], [-50, -60]], 10, 10), c: 'wood' }); sh.push({ p: E(-48, -272, 26, 34), c: 'gold', pat: { t: 'scales' } });   // mace
  sh.push({ p: B([[-10, -250], [-40, -130], [-46, -8]], 38, 28), c: 'crim' }); sh.push({ p: B([[14, -250], [30, -130], [46, -8]], 38, 28), c: 'crim' });
  for (const x of [-46, 46]) sh.push({ p: S([[x - 18, -14], [x + 28, -14], [x + 32, 4], [x - 20, 6]]), c: 'gold' });
  sh.push({ p: P([[-52, -300], [52, -300], [62, -220], [72, -120], [40, -110], [10, -118], [-22, -108], [-54, -118], [-72, -124], [-62, -220]]), c: 'red', pat: { t: 'lattice', s: 12 } });
  sh.push({ p: S([[-44, -300], [-52, -356], [-42, -410], [0, -426], [40, -412], [52, -356], [44, -300]]), c: 'jade', pat: { t: 'scalesOpen' } });
  sh.push({ p: S([[-38, -410], [0, -426], [38, -412], [32, -384], [0, -374], [-30, -386]]), c: 'gold', pat: { t: 'lattice', s: 7 } });
  sh.push({ p: B([[-46, -306], [48, -306]], 18, 18, false), c: 'gold', pat: { t: 'coin' } });
  sh.push(neck(N, k, 'skinD')); sh.push(hairBack(N, k, 'ink', 20));
  sh.push(...face(N, k, { solid: true, skin: 'skinD', fierce: true }));
  sh.push({ p: X(N, k, L([[24, -25], [12, -28], [2, -22]])), c: 'ink', line: 2.6 });   // moustache
  sh.push({ p: X(N, k, P([[18, -16], [22, -9], [15, -12]])), c: 'ivory', ink: 0 });
  sh.push({ p: X(N, k, P([[-28, -62], [20, -64], [22, -84], [12, -76], [8, -112], [0, -86], [-6, -124], [-12, -88], [-20, -110], [-22, -80], [-32, -88]])), c: 'gold', pat: { t: 'lattice', s: 6 } });
  sh.push({ p: X(N, k, C(-4, -74, 4)), c: 'red', ink: 1 }); sh.push(earring(N, k));
  const arm = { box: [-34, -34, 80, 220], shapes: [
    { p: B([[0, 0], [10, 96]], 30, 24), c: 'jade' }, { p: B([[10, 96], [36, 176]], 24, 18), c: 'skinD' },
    { p: E(32, 156, 13, 7, 1.2), c: 'gold', pat: { t: 'coin' } }, { p: S([[24, 168], [48, 170], [56, 188], [44, 198], [26, 192]]), c: 'skinD' }] };
  return { body: { box: [-130, -680, 140, 20], shapes: sh }, arm, shoulder: [16, -404] };
}
// —— Prahlad: a child devotee. Open face, shikha, tilak, yellow dhoti, hands joined. Origin at the feet ——
export function prahlad() {
  const N = [6, -268], k = 1.35, sh = [];
  sh.push({ p: B([[-6, -150], [-20, -70], [-24, -6]], 24, 17), c: 'skin' }); sh.push({ p: B([[8, -150], [18, -70], [26, -6]], 24, 17), c: 'skin' });
  for (const x of [-24, 26]) sh.push({ p: S([[x - 11, -9], [x + 18, -9], [x + 21, 3], [x - 12, 5]]), c: 'skin' });
  sh.push({ p: P([[-34, -196], [34, -196], [42, -140], [48, -84], [22, -76], [4, -82], [-16, -74], [-38, -82], [-48, -86], [-42, -140]]), c: 'gold', pat: { t: 'folds' } });
  sh.push({ p: S([[-26, -196], [-30, -230], [-24, -262], [0, -272], [22, -262], [30, -230], [26, -196]]), c: 'skin' });
  sh.push({ p: B([[-24, -262], [4, -228], [28, -198]], 18, 18, false), c: 'saffron', pat: { t: 'folds' } });
  sh.push({ beads: curve([[-10, -268], [6, -246], [20, -262]]), r: 3, c: 'rudraksha' });
  // hands joined in namaskar before the chest
  sh.push({ p: B([[16, -252], [36, -228], [44, -238]], 15, 12), c: 'skin' });
  sh.push({ p: S([[38, -232], [52, -262], [58, -258], [50, -226]]), c: 'skin' });
  sh.push(neck(N, k, 'skin'));
  sh.push({ p: X(N, k, S([[-2, -64], [-16, -68], [-28, -60], [-32, -40], [-30, -20], [-20, -10], [-9, -26], [-5, -40], [-6, -56]])), c: 'ink', pat: { t: 'slits', n: 4 } });
  sh.push({ p: X(N, k, B([[-14, -68], [-26, -80], [-34, -74]], 6, 3)), c: 'ink' });   // shikha
  sh.push(...face(N, k, { skin: 'skin' }));
  sh.push({ p: X(N, k, L([[12, -62], [12, -54]])), c: 'red', line: 2 });
  sh.push({ p: X(N, k, L([[9, -62], [10, -56]])), c: 'ashMark', line: 1.4 }); sh.push({ p: X(N, k, L([[15, -62], [14.5, -56]])), c: 'ashMark', line: 1.4 });
  return { body: { box: [-80, -400, 90, 16], shapes: sh } };
}
export function pillar() {
  return { box: [-80, -1040, 80, 20], shapes: [
    { p: P([[-70, 0], [70, 0], [60, -40], [-60, -40]]), c: 'gold2', pat: { t: 'coin' } },
    { p: P([[-44, -40], [44, -40], [38, -940], [-38, -940]]), c: 'red', pat: { t: 'rings' } },
    { p: P([[-74, -940], [74, -940], [60, -1000], [-60, -1000]]), c: 'gold', pat: { t: 'lattice', s: 10 } },
    { p: c => c.roundRect(-80, -1036, 160, 36, 8), c: 'gold2', pat: { t: 'beads' } }] };
}
export function woodpile() {
  const sh = [];
  for (let r = 0; r < 5; r++) for (let i = 0; i < 6 - r; i++) { const x = -150 + r * 30 + i * 60, y = -20 - r * 34; sh.push({ p: E(x, y, 34, 17), c: r % 2 ? 'wood' : 'brown', pat: { t: 'bark' } }); }
  return { box: [-200, -200, 200, 20], shapes: sh };
}
export function tusk() { return { box: [-60, -20, 60, 20], shapes: [{ p: B([[-50, 6], [0, -6], [50, 2]], 18, 4), c: 'ivory' }] }; }

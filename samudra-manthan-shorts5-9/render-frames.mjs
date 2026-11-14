// Resumable frame renderer: node frames.mjs <demo> <outDir> <a> <b> [--q 'k=v'] [--size WxH] [--fps 24]
// Renders frames [a, b) as JPEGs, skipping any that already exist.
import fs from 'fs'; import path from 'path';
import { openDemo, closeServer } from '/root/lemo-opuscar/core/render/page.mjs';
const [dir, outDir, A, B] = process.argv.slice(2), args = process.argv.slice(6);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [w, h] = opt('--size', '1080x1920').split('x').map(Number), FPS = +opt('--fps', 24), q = opt('--q', '');
fs.mkdirSync(outDir, { recursive: true });
const todo = []; for (let f = +A; f < +B; f++) if (!fs.existsSync(path.join(outDir, `f_${String(f).padStart(5, '0')}.jpg`))) todo.push(f);
console.log(`${todo.length} frames to render in [${A}, ${B})`);
if (todo.length) {
  const { browser, page } = await openDemo(dir, { w, h, q }); const t0 = Date.now();
  for (const [i, f] of todo.entries()) {
    await page.evaluate(t => window.render(t), f / FPS);
    const p = path.join(outDir, `f_${String(f).padStart(5, '0')}.jpg`);
    fs.writeFileSync(p + '.tmp', await page.screenshot({ type: 'jpeg', quality: 93 })); fs.renameSync(p + '.tmp', p);
    if (i % 20 === 0) console.log(`frame ${f}  ${i + 1}/${todo.length}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  await browser.close();
}
closeServer(); console.log('done');

/* Homepage: HD interactive sky + page chrome.
   The sky follows the visitor's local time. Drag the sun (day) or moon (night)
   along its arc to change the hour; the whole page follows into light or dark.
   Click the lighthouse to light it. Everything is drawn on one canvas. */
(() => {
  const root = document.documentElement;
  const cv = document.getElementById('sky'), ctx = cv.getContext('2d');
  const scene = document.getElementById('scene');
  const dn = document.getElementById('dn'), clock = document.getElementById('clock'), when = document.getElementById('when');
  const dragNote = document.getElementById('dragNote'), clickNote = document.getElementById('clickNote');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------------------------------------------------------------- state
  let hour, live = true, dragging = false, W = 0, H = 0, dpr = 1, raf = 0, visible = true;
  let lastT = performance.now(), time = 0, dragged = false, lampOn = false, lampFlash = 0;
  const nowHour = () => { const d = new Date(); return d.getHours() + d.getMinutes() / 60; };
  hour = nowHour();

  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const lerp = (a, b, k) => a + (b - a) * k;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const smooth = k => k * k * (3 - 2 * k);
  const mix = (c1, c2, k) => [lerp(c1[0], c2[0], k), lerp(c1[1], c2[1], k), lerp(c1[2], c2[2], k)];
  const rgba = (c, a = 1) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
  const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];

  const isDay = h => h >= 6 && h < 18;
  const arcT = h => isDay(h) ? (h - 6) / 12 : ((h - 18 + 24) % 24) / 12;
  const horizon = () => Math.round(H * .6);

  // ---------------------------------------------------------------- palette keyframes (by hour)
  // sky top / mid / horizon, sea near / far, cloud lit / shade, hill far / near, star alpha
  const K = [
    [0,    '#050817', '#0b1230', '#1a2550', '#0a1124', '#060a18', '#4a5683', '#1c2444', '#18213b', '#0f1729', 1],
    [4.8,  '#060a1c', '#0e1636', '#22305e', '#0b1328', '#070b1a', '#4f5b8a', '#1e2747', '#1a243f', '#10182b', 1],
    [5.7,  '#1b2350', '#4a4f86', '#d98a7a', '#2a3360', '#141b3a', '#c99aa0', '#4a4e7a', '#3b3f5e', '#262a45', .35],
    [6.4,  '#3d6fb4', '#8aa6d6', '#ffc48c', '#4f79a8', '#2c4f7c', '#ffe3cc', '#b49aa8', '#6f8a7a', '#4f6e57', 0],
    [8,    '#2f7fd0', '#79b6ea', '#cfe8f7', '#3a8cc6', '#2468a0', '#ffffff', '#c6d4e6', '#6f9a7c', '#4f8a5d', 0],
    [12,   '#2a83d6', '#6cb5ec', '#c5e6f7', '#3891c9', '#1f6aa3', '#ffffff', '#cdd9e8', '#78a684', '#56925f', 0],
    [16,   '#3279c4', '#7db3e2', '#d6e9f4', '#3c88bd', '#236399', '#fffaf2', '#cfd5e2', '#7a9e80', '#5a8a5c', 0],
    [17.3, '#4b6fb0', '#a7a9d0', '#ffc78f', '#4d77a6', '#2c5384', '#ffe2c2', '#c49d9c', '#7c8a6c', '#5c6f4f', 0],
    [18.1, '#2d3a78', '#8a6a9a', '#ff9a6b', '#3d4f82', '#202c5a', '#ffb98f', '#7d6286', '#4c4e5e', '#33384a', .15],
    [19,   '#121a42', '#2e3270', '#6e4f86', '#18214a', '#0e1530', '#7a6c9c', '#2c2f5a', '#262c48', '#181e33', .7],
    [20.5, '#070b1f', '#0e1638', '#1f2b58', '#0b1328', '#070b1a', '#4a5683', '#1c2444', '#18213b', '#0f1729', 1],
    [24,   '#050817', '#0b1230', '#1a2550', '#0a1124', '#060a18', '#4a5683', '#1c2444', '#18213b', '#0f1729', 1],
  ].map(r => [r[0], ...r.slice(1, 10).map(hex), r[10]]);
  function palette(h) {
    let i = 0; while (i < K.length - 2 && K[i + 1][0] <= h) i++;
    const a = K[i], b = K[i + 1], k = smooth(clamp((h - a[0]) / (b[0] - a[0]), 0, 1));
    const c = j => mix(a[j], b[j], k);
    return {top: c(1), mid: c(2), low: c(3), seaN: c(4), seaF: c(5), cLit: c(6), cShade: c(7), hillF: c(8), hillN: c(9),
      stars: lerp(a[10], b[10], k), night: !isDay(h), e: Math.sin(Math.PI * arcT(h))};
  }

  // ---------------------------------------------------------------- body position
  function bodyPos(h) {
    const t = arcT(h), top = Math.max(42, H * .1), base = horizon() + 8;
    return {x: W * (.07 + .86 * t), y: base - Math.sin(Math.PI * t) * (base - top), t};
  }

  // ---------------------------------------------------------------- scene objects
  const stars = Array.from({length: 420}, () => ({x: rnd(), y: Math.pow(rnd(), 1.25) * .95, r: rnd() < .06 ? 1.1 + rnd() * .9 : .35 + rnd() * .7,
    p: rnd() * 6.28, s: .6 + rnd() * 2.2, c: rnd() < .12 ? [255, 214, 170] : rnd() < .2 ? [190, 210, 255] : [255, 255, 255]}));
  const planets = [{x: .3, y: .09, r: 1.9, c: [255, 232, 190]}, {x: .86, y: .16, r: 1.6, c: [255, 170, 120]}];
  const clouds = Array.from({length: 7}, (_, i) => ({x: i / 7 * 1.3 + rnd() * .08, y: [.1, .26, .16, .34, .12, .3, .2][i], s: .45 + rnd() * .55,
    v: .006 + rnd() * .01, seed: 100 + i * 37, a: .78 + rnd() * .22, far: i % 3 === 0}));
  const fireflies = Array.from({length: 46}, () => ({side: rnd() < .62 ? 0 : 1, u: rnd(), v: rnd(), p: rnd() * 6.28, s: .4 + rnd() * .9}));
  const shimmer = Array.from({length: 150}, () => ({u: rnd(), v: Math.pow(rnd(), 1.6), w: .01 + rnd() * .05, p: rnd() * 6.28}));
  const boats = [{x: .62, s: 1, p: 0}, {x: .7, s: .65, p: 2}, {x: .42, s: .5, p: 4}];
  const birds = Array.from({length: 6}, (_, i) => ({dx: i * 14 - 30 + rnd() * 8, dy: (i % 3) * 7 + rnd() * 4, p: rnd() * 6}));
  let flockX = -0.1;
  const sats = [{x: rnd(), y: .12, v: .006, p: 0}, {x: rnd(), y: .22, v: -.004, p: 1.7}];
  let plane = null, nextPlane = 4, shooting = [], nextShoot = 2;

  // ---------------------------------------------------------------- sprite caches
  const cloudCache = new Map();
  function cloudSprite(c, lit, shade) {
    const key = c.seed + ':' + lit.map(v => v >> 3).join() + shade.map(v => v >> 3).join();
    if (cloudCache.has(key)) return cloudCache.get(key);
    if (cloudCache.size > 260) cloudCache.clear();
    const w = 460, h = 210, sc = dpr, base = h * .8;
    let s2 = c.seed; const r2 = () => (s2 = (s2 * 16807) % 2147483647) / 2147483647;
    const puffs = [], n = 16 + (c.seed % 7);
    for (let i = 0; i < n; i++) {
      const t = (i + .5) / n, lift = Math.sin(Math.PI * t) * (.5 + r2() * .5);
      const r = h * (.1 + .17 * lift + r2() * .06);
      puffs.push([w * (.1 + .8 * t) + (r2() - .5) * 24, base - r * .55 - lift * h * .3, r]);
    }
    // 1. one solid silhouette (union of puffs, so no seams between them)
    const a = document.createElement('canvas'); a.width = w * sc; a.height = h * sc;
    const g = a.getContext('2d'); g.scale(sc, sc);
    g.fillStyle = '#fff'; g.beginPath();
    for (const [x, y, r] of puffs) { g.moveTo(x + r, y); g.arc(x, y, r, 0, 7); }
    g.rect(w * .1, base - h * .12, w * .8, h * .12); g.fill('nonzero');
    // 2. shade it: lit from above, darker and flatter underneath
    g.globalCompositeOperation = 'source-atop';
    let gr = g.createLinearGradient(0, base - h * .62, 0, base);
    gr.addColorStop(0, rgba(mix(lit, [255, 255, 255], .3))); gr.addColorStop(.45, rgba(lit)); gr.addColorStop(1, rgba(shade));
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    // 3. soft highlights on the upper-left of the bigger puffs for volume
    for (const [x, y, r] of puffs) {
      if (r < h * .17) continue;
      gr = g.createRadialGradient(x - r * .3, y - r * .4, 0, x - r * .3, y - r * .4, r * .9);
      gr.addColorStop(0, rgba(mix(lit, [255, 255, 255], .5), .55)); gr.addColorStop(1, rgba(lit, 0));
      g.fillStyle = gr; g.fillRect(x - r * 1.3, y - r * 1.4, r * 2.2, r * 2.2);
    }
    // 4. a faint inner shadow line between puff rows, then trim the base
    g.globalCompositeOperation = 'destination-out';
    gr = g.createLinearGradient(0, base - 6, 0, base + 8);
    gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,1)');
    g.fillStyle = gr; g.fillRect(0, base - 6, w, h);
    // 5. soften the whole thing
    const b = document.createElement('canvas'); b.width = a.width; b.height = a.height;
    const gb = b.getContext('2d'); gb.filter = `blur(${2.2 * sc}px)`; gb.drawImage(a, 0, 0);
    gb.filter = 'none'; gb.globalAlpha = .55; gb.drawImage(a, 0, 0);
    const out = {img: b, w, h};
    cloudCache.set(key, out); return out;
  }

  let grain = null;
  function makeGrain() {
    const n = document.createElement('canvas'); n.width = n.height = 160;
    const g = n.getContext('2d'), d = g.createImageData(160, 160);
    for (let i = 0; i < d.data.length; i += 4) { const v = Math.random() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 22; }
    g.putImageData(d, 0, 0); grain = ctx.createPattern(n, 'repeat');
  }

  let milky = null;
  function makeMilky() {
    const m = document.createElement('canvas'); m.width = 900; m.height = 260;
    const g = m.getContext('2d');
    for (let i = 0; i < 900; i++) {
      const t = Math.random(), x = t * 900, y = 130 + Math.sin(t * 3.1) * 40 + (Math.random() - .5) * 90 * Math.random();
      const r = 6 + Math.random() * 26, gr = g.createRadialGradient(x, y, 0, x, y, r);
      const tint = Math.random() < .3 ? '200,180,255' : '170,195,255';
      gr.addColorStop(0, `rgba(${tint},.05)`); gr.addColorStop(1, `rgba(${tint},0)`);
      g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2);
    }
    for (let i = 0; i < 700; i++) { g.fillStyle = `rgba(255,255,255,${Math.random() * .5})`; g.fillRect(Math.random() * 900, 130 + (Math.random() - .5) * 120 * Math.random(), .8, .8); }
    milky = m;
  }

  // ---------------------------------------------------------------- terrain
  const leftHill = x => { const k = x / (W * .36); return horizon() - H * .2 * Math.max(0, Math.cos(k * 1.35)) * (1 - k * .25); };
  function drawLand(p) {
    const hz = horizon();
    // far range on the right
    ctx.fillStyle = rgba(mix(p.hillF, p.low, .45));
    ctx.beginPath(); ctx.moveTo(W * .55, hz + 1);
    ctx.bezierCurveTo(W * .64, hz - H * .05, W * .7, hz - H * .11, W * .78, hz - H * .1);
    ctx.bezierCurveTo(W * .86, hz - H * .09, W * .93, hz - H * .15, W * 1.02, hz - H * .12); ctx.lineTo(W * 1.02, hz + 1); ctx.fill();
    // right island, lit from the body side
    const b = bodyPos(hour);
    let gr = ctx.createLinearGradient(W * .74, 0, W, 0);
    const lit = mix(p.hillN, p.cLit, p.night ? .08 : .18);
    gr.addColorStop(b.x > W * .8 ? 1 : 0, rgba(lit)); gr.addColorStop(b.x > W * .8 ? 0 : 1, rgba(mix(p.hillN, [0, 0, 0], .2)));
    ctx.fillStyle = gr; ctx.beginPath(); ctx.moveTo(W * .72, hz + 1);
    ctx.bezierCurveTo(W * .79, hz - H * .03, W * .84, hz - H * .085, W * .9, hz - H * .08);
    ctx.bezierCurveTo(W * .95, hz - H * .075, W * .99, hz - H * .04, W * 1.02, hz - H * .03); ctx.lineTo(W * 1.02, hz + 1); ctx.fill();
    // left headland with grass gradient
    gr = ctx.createLinearGradient(0, hz - H * .22, 0, hz + 4);
    gr.addColorStop(0, rgba(mix(p.hillN, p.cLit, p.night ? .06 : .16))); gr.addColorStop(1, rgba(mix(p.hillN, [0, 0, 0], .25)));
    ctx.fillStyle = gr; ctx.beginPath(); ctx.moveTo(-2, hz + 2);
    for (let x = -2; x <= W * .4; x += 6) ctx.lineTo(x, leftHill(x));
    ctx.lineTo(W * .4, hz + 2); ctx.fill();
    // rocks along the shore
    ctx.fillStyle = rgba(mix(p.hillN, [0, 0, 0], .35));
    for (let i = 0; i < 9; i++) { const x = W * (.29 + i * .012), y = hz + 2 + (i % 3) * 2; ctx.beginPath(); ctx.ellipse(x, y, 5 + (i % 4) * 2, 2.2, 0, 0, 7); ctx.fill(); }
    // trees on the headland
    for (let i = 0; i < 7; i++) {
      const x = W * (.015 + i * .028), y = leftHill(x) + 2, r = 7 + (i % 3) * 3;
      ctx.fillStyle = rgba(mix(p.hillN, [0, 0, 0], .45)); ctx.fillRect(x - 1, y - r * .6, 2, r * .7);
      ctx.fillStyle = rgba(mix(mix(p.hillN, [30, 70, 40], p.night ? .1 : .35), [0, 0, 0], .18));
      ctx.beginPath(); ctx.arc(x, y - r * 1.1, r, 0, 7); ctx.arc(x + r * .5, y - r * .8, r * .7, 0, 7); ctx.fill();
    }
  }

  function lighthouse(p) {
    const x = W * .135, y = leftHill(W * .135) + 3, s = clamp(H / 520, .75, 1.25);
    const wall = p.night ? [196, 204, 222] : mix([246, 242, 234], p.cLit, .2);
    ctx.fillStyle = rgba(wall); ctx.beginPath();
    ctx.moveTo(x - 8 * s, y); ctx.lineTo(x - 5 * s, y - 42 * s); ctx.lineTo(x + 5 * s, y - 42 * s); ctx.lineTo(x + 8 * s, y); ctx.fill();
    ctx.fillStyle = '#C2412D'; ctx.fillRect(x - 7.2 * s, y - 14 * s, 14.4 * s, 6 * s); ctx.fillRect(x - 6 * s, y - 30 * s, 12 * s, 5 * s);
    ctx.fillStyle = rgba(mix(wall, [0, 0, 0], .55)); ctx.fillRect(x - 6.5 * s, y - 50 * s, 13 * s, 8 * s);
    ctx.fillStyle = '#C2412D'; ctx.beginPath(); ctx.moveTo(x - 7.5 * s, y - 50 * s); ctx.lineTo(x, y - 57 * s); ctx.lineTo(x + 7.5 * s, y - 50 * s); ctx.fill();
    const on = p.night || lampOn || p.e < .12;
    const lampY = y - 46 * s;
    if (on) {
      const fl = 1 + lampFlash * 2;
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      let g = ctx.createRadialGradient(x, lampY, 0, x, lampY, 26 * s * fl);
      g.addColorStop(0, 'rgba(255,236,170,.9)'); g.addColorStop(1, 'rgba(255,236,170,0)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, lampY, 26 * s * fl, 0, 7); ctx.fill();
      // rotating beam: its visible length follows the cosine of the lamp's rotation
      const rot = time * (lampOn ? 1.6 : .9), dir = Math.cos(rot), len = W * .55 * Math.abs(dir) * (p.night ? 1 : .6);
      if (len > 4) {
        const ex = x + Math.sign(dir) * len;
        g = ctx.createLinearGradient(x, 0, ex, 0);
        g.addColorStop(0, `rgba(255,238,180,${.32 * fl})`); g.addColorStop(1, 'rgba(255,238,180,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x, lampY - 2); ctx.lineTo(ex, lampY - 30 * s); ctx.lineTo(ex, lampY + 26 * s); ctx.lineTo(x, lampY + 2); ctx.fill();
      }
      ctx.restore();
      ctx.fillStyle = '#fff6d6'; ctx.fillRect(x - 3 * s, lampY - 3 * s, 6 * s, 5 * s);
    } else { ctx.fillStyle = 'rgba(40,50,70,.55)'; ctx.fillRect(x - 3 * s, lampY - 3 * s, 6 * s, 5 * s); }
    // a lit cottage window beside it at night
    const cx = W * .07, cy = leftHill(cx) + 2;
    ctx.fillStyle = rgba(mix(wall, [0, 0, 0], .25)); ctx.fillRect(cx - 9 * s, cy - 12 * s, 18 * s, 12 * s);
    ctx.fillStyle = '#8d3b2c'; ctx.beginPath(); ctx.moveTo(cx - 11 * s, cy - 12 * s); ctx.lineTo(cx, cy - 20 * s); ctx.lineTo(cx + 11 * s, cy - 12 * s); ctx.fill();
    ctx.fillStyle = p.night ? '#ffd98a' : 'rgba(40,50,70,.5)'; ctx.fillRect(cx - 3 * s, cy - 9 * s, 5 * s, 5 * s);
    return {x, y: y - 28 * s, r: 34 * s};
  }

  // ---------------------------------------------------------------- frame
  function draw(now) {
    const dt = Math.min(.05, (now - lastT) / 1000); lastT = now; if (!reduce) time += dt;
    const p = palette(hour), hz = horizon(), b = bodyPos(hour);
    ctx.clearRect(0, 0, W, H);

    // sky
    let g = ctx.createLinearGradient(0, 0, 0, hz);
    g.addColorStop(0, rgba(p.top)); g.addColorStop(.6, rgba(p.mid)); g.addColorStop(1, rgba(p.low));
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, hz + 1);

    // stars, milky way, planets
    if (p.stars > .01) {
      ctx.globalAlpha = p.stars * .7; ctx.save(); ctx.translate(W * .5, hz * .42); ctx.rotate(-.28);
      ctx.drawImage(milky, -W * .75, -hz * .35, W * 1.5, hz * .7); ctx.restore(); ctx.globalAlpha = 1;
      for (const s of stars) {
        const a = p.stars * (.45 + .55 * Math.sin(time * s.s + s.p)) * (1 - s.y * .35);
        if (a <= .02) continue;
        ctx.fillStyle = rgba(s.c, a); ctx.beginPath(); ctx.arc(s.x * W, s.y * hz, s.r, 0, 7); ctx.fill();
        if (s.r > 1.2) { ctx.fillStyle = rgba(s.c, a * .18); ctx.beginPath(); ctx.arc(s.x * W, s.y * hz, s.r * 3, 0, 7); ctx.fill(); }
      }
      for (const pl of planets) {
        const x = pl.x * W, y = pl.y * hz; g = ctx.createRadialGradient(x, y, 0, x, y, 10);
        g.addColorStop(0, rgba(pl.c, p.stars)); g.addColorStop(.25, rgba(pl.c, p.stars * .35)); g.addColorStop(1, rgba(pl.c, 0));
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, 10, 0, 7); ctx.fill();
      }
      // shooting stars
      if (p.night && !reduce) {
        nextShoot -= dt;
        if (nextShoot < 0) { nextShoot = 2.5 + Math.random() * 5; shooting.push({x: Math.random() * W, y: Math.random() * hz * .45, a: .5 + Math.random() * .5, t: 0, d: Math.random() < .5 ? -1 : 1}); }
        shooting = shooting.filter(s => (s.t += dt) < .9);
        for (const s of shooting) {
          const k = s.t / .9, x = s.x + s.d * k * 260, y = s.y + k * 120, tl = 70;
          g = ctx.createLinearGradient(x, y, x - s.d * tl, y - tl * .46);
          g.addColorStop(0, `rgba(255,255,255,${(1 - k) * s.a})`); g.addColorStop(1, 'rgba(255,255,255,0)');
          ctx.strokeStyle = g; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - s.d * tl, y - tl * .46); ctx.stroke();
        }
      }
    }

    // satellites
    if (p.stars > .5) for (const s of sats) {
      s.x = (s.x + s.v * dt + 1) % 1; const x = s.x * W, y = s.y * hz, on = Math.sin(time * 3 + s.p) > .6;
      ctx.fillStyle = `rgba(220,230,255,${on ? .95 : .45})`; ctx.fillRect(x - 1, y - 1, 2.2, 2.2);
      ctx.fillStyle = 'rgba(120,150,220,.6)'; ctx.fillRect(x - 6, y - .5, 4, 1.4); ctx.fillRect(x + 3, y - .5, 4, 1.4);
    }

    // body glow + body
    const glowR = p.night ? 170 : 230 + (1 - p.e) * 220;
    g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, glowR);
    if (p.night) { g.addColorStop(0, 'rgba(210,222,255,.32)'); g.addColorStop(.35, 'rgba(160,180,240,.12)'); g.addColorStop(1, 'rgba(160,180,240,0)'); }
    else { const w = mix([255, 170, 110], [255, 246, 220], smooth(clamp(p.e / .5, 0, 1))); g.addColorStop(0, rgba(w, .85)); g.addColorStop(.18, rgba(w, .4)); g.addColorStop(1, rgba(w, 0)); }
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, hz);
    // plane with blinking lights and a fading contrail
    if (!reduce) {
      nextPlane -= dt;
      if (!plane && nextPlane < 0) { const d = Math.random() < .5 ? 1 : -1; plane = {x: d > 0 ? -40 : W + 40, y: hz * (.1 + Math.random() * .2), d, v: 38 + Math.random() * 22, trail: []}; }
      if (plane) {
        plane.x += plane.d * plane.v * dt; plane.trail.push([plane.x, plane.y, time]);
        plane.trail = plane.trail.filter(t => time - t[2] < 7);
        ctx.lineCap = 'round';
        for (let i = 1; i < plane.trail.length; i++) {
          const [x0, y0, t0] = plane.trail[i - 1], [x1, y1] = plane.trail[i], age = (time - t0) / 7;
          ctx.strokeStyle = p.night ? `rgba(200,210,240,${(1 - age) * .22})` : `rgba(255,255,255,${(1 - age) * .75})`;
          ctx.lineWidth = 1.2 + age * 3; ctx.beginPath(); ctx.moveTo(x0 - plane.d * 10, y0); ctx.lineTo(x1 - plane.d * 10, y1); ctx.stroke();
        }
        const x = plane.x, y = plane.y;
        ctx.fillStyle = p.night ? 'rgba(170,180,205,.9)' : 'rgba(235,238,245,.95)';
        ctx.beginPath(); ctx.ellipse(x, y, 9, 1.8, 0, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.moveTo(x - 1, y); ctx.lineTo(x - plane.d * 4, y + 5); ctx.lineTo(x + plane.d * 2, y); ctx.fill();
        ctx.beginPath(); ctx.moveTo(x - plane.d * 8, y); ctx.lineTo(x - plane.d * 10, y - 4); ctx.lineTo(x - plane.d * 6, y); ctx.fill();
        if (Math.sin(time * 7) > .3) { ctx.fillStyle = '#ff4d4d'; ctx.fillRect(x - plane.d * 2, y + 4, 2, 2); ctx.fillStyle = '#fff'; ctx.fillRect(x - plane.d * 10, y - 4, 2, 2); }
        if (plane.x < -60 || plane.x > W + 60) { plane = null; nextPlane = 10 + Math.random() * 14; }
      }
    }

    // clouds (pass in front of the sun and moon)
    for (const c of clouds) {
      const sp = cloudSprite(c, p.cLit, p.cShade);
      const scale = c.s * clamp(W / 1300, .55, 1.2) * (c.far ? .7 : 1);
      const x = (((c.x + (reduce ? 0 : time * c.v * .06)) % 1.35) - .2) * W, y = c.y * hz;
      ctx.globalAlpha = c.a * (p.night ? .75 : 1) * (c.far ? .7 : 1);
      ctx.drawImage(sp.img, x, y - sp.h * scale * .55, sp.w * scale, sp.h * scale);
    }
    ctx.globalAlpha = 1;

    // the sun / moon sits in front of the clouds so it is always grabbable
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, hz); ctx.clip();
    if (p.night) {
      const r = 17;
      ctx.shadowColor = 'rgba(225,232,255,.95)'; ctx.shadowBlur = 30;
      g = ctx.createRadialGradient(b.x - 5, b.y - 5, 2, b.x, b.y, r);
      g.addColorStop(0, '#ffffff'); g.addColorStop(.7, '#eef1f8'); g.addColorStop(1, '#cfd6e6');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(b.x, b.y, r, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
      ctx.fillStyle = 'rgba(150,160,185,.28)';
      [[-5, -4, 4], [5, 3, 3.2], [-1, 7, 2.4], [7, -6, 2], [-8, 4, 1.6]].forEach(([dx, dy, rr]) => { ctx.beginPath(); ctx.arc(b.x + dx, b.y + dy, rr, 0, 7); ctx.fill(); });
    } else {
      const sc = mix([255, 158, 92], [255, 252, 236], smooth(clamp(p.e / .45, 0, 1)));
      ctx.shadowColor = rgba(sc); ctx.shadowBlur = 50; ctx.fillStyle = rgba(sc);
      ctx.beginPath(); ctx.arc(b.x, b.y, 22, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let i = 0; i < 16; i++) {
        const a = i / 16 * 6.283 + time * .05, l = 80 + (i % 3) * 40;
        g = ctx.createLinearGradient(b.x, b.y, b.x + Math.cos(a) * l, b.y + Math.sin(a) * l);
        g.addColorStop(0, `rgba(255,250,225,${.18 * p.e + .05})`); g.addColorStop(1, 'rgba(255,250,225,0)');
        ctx.strokeStyle = g; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(b.x, b.y); ctx.lineTo(b.x + Math.cos(a) * l, b.y + Math.sin(a) * l); ctx.stroke();
      }
      ctx.restore();
    }
    ctx.restore();

    // birds by day
    if (!p.night && p.e > .15) {
      flockX += dt * .012; if (flockX > 1.2) flockX = -.15;
      ctx.strokeStyle = 'rgba(28,36,52,.6)'; ctx.lineWidth = 1.3;
      for (const bd of birds) {
        const x = flockX * W + bd.dx, y = hz * .2 + bd.dy + Math.sin(time * .6 + bd.p) * 3, f = Math.sin(time * 7 + bd.p) * 2.4, s = 5;
        ctx.beginPath(); ctx.moveTo(x - s, y - f); ctx.quadraticCurveTo(x - s / 2, y - s / 2, x, y); ctx.quadraticCurveTo(x + s / 2, y - s / 2, x + s, y - f); ctx.stroke();
      }
    }

    // horizon haze
    g = ctx.createLinearGradient(0, hz - H * .12, 0, hz);
    g.addColorStop(0, rgba(p.low, 0)); g.addColorStop(1, rgba(p.low, .55));
    ctx.fillStyle = g; ctx.fillRect(0, hz - H * .12, W, H * .12);

    drawLand(p);

    // sea
    g = ctx.createLinearGradient(0, hz, 0, H);
    g.addColorStop(0, rgba(p.seaF)); g.addColorStop(1, rgba(p.seaN));
    ctx.fillStyle = g; ctx.fillRect(0, hz, W, H - hz);
    ctx.fillStyle = rgba(mix(p.low, [255, 255, 255], .35), .5); ctx.fillRect(0, hz, W, 1);
    // sky reflected on the water, faint
    g = ctx.createLinearGradient(0, hz, 0, hz + (H - hz) * .5);
    g.addColorStop(0, rgba(p.low, .35)); g.addColorStop(1, rgba(p.low, 0));
    ctx.fillStyle = g; ctx.fillRect(0, hz, W, (H - hz) * .5);

    // long broken reflection of the sun / moon
    if (b.y < hz + 6) {
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      const rc = p.night ? [215, 225, 255] : mix([255, 170, 110], [255, 246, 220], smooth(clamp(p.e / .5, 0, 1)));
      const rows = 46, depth = H - hz;
      for (let i = 0; i < rows; i++) {
        const k = i / rows, y = hz + 2 + Math.pow(k, 1.5) * depth;
        const w = (8 + k * 70) * (.55 + .45 * Math.sin(time * 1.7 + i * 2.1)) * (p.night ? .8 : 1.2);
        const off = Math.sin(time * 1.1 + i * 1.3) * (4 + k * 10);
        ctx.fillStyle = rgba(rc, (p.night ? .5 : .6) * (1 - k * .75));
        ctx.fillRect(b.x - w / 2 + off, y, w, 1 + k * 1.4);
        if (i % 3 === 0) ctx.fillRect(b.x + off * 2.2 + w * .7, y + 1, w * .3, 1);
      }
      ctx.restore();
    }
    // shimmer streaks across the whole sea
    for (const s of shimmer) {
      const y = hz + 3 + s.v * (H - hz), a = .08 + .1 * Math.sin(time * 1.4 + s.p);
      if (a <= 0) continue;
      const x = ((s.u + time * .004 * (1 + s.v)) % 1) * W;
      ctx.fillStyle = p.night ? `rgba(160,180,230,${a * .7})` : `rgba(255,255,255,${a * 1.4})`;
      ctx.fillRect(x, y, s.w * W * (.4 + s.v), 1);
    }
    // boats
    for (const bt of boats) {
      const x = bt.x * W + (reduce ? 0 : Math.sin(time * .12 + bt.p) * 18), y = hz + 6 * bt.s + Math.sin(time * 1.1 + bt.p) * .9, s = bt.s * 10;
      ctx.fillStyle = p.night ? 'rgba(196,206,230,.65)' : 'rgba(255,255,255,.96)';
      ctx.beginPath(); ctx.moveTo(x, y - s * 2.3); ctx.lineTo(x, y - 1); ctx.lineTo(x + s * 1.25, y - 1); ctx.fill();
      ctx.fillStyle = p.night ? 'rgba(230,180,160,.5)' : 'rgba(230,236,244,.9)';
      ctx.beginPath(); ctx.moveTo(x - 1, y - s * 1.8); ctx.lineTo(x - 1, y - 1); ctx.lineTo(x - s * .8, y - 1); ctx.fill();
      ctx.fillStyle = p.night ? 'rgba(14,20,40,.95)' : 'rgba(40,50,70,.9)';
      ctx.beginPath(); ctx.moveTo(x - s * .9, y); ctx.lineTo(x + s * 1.5, y); ctx.lineTo(x + s * 1.1, y + s * .45); ctx.lineTo(x - s * .6, y + s * .45); ctx.fill();
      if (p.night) { ctx.fillStyle = 'rgba(255,214,140,.9)'; ctx.fillRect(x + s * .2, y - 1.5, 1.6, 1.6); }
      ctx.fillStyle = p.night ? 'rgba(200,210,240,.12)' : 'rgba(255,255,255,.25)'; ctx.fillRect(x - s, y + s * .6, s * 2.6, 1);
    }

    const lh = lighthouse(p); lighthouseHit = lh;

    // fireflies at night
    if (p.stars > .3) {
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (const f of fireflies) {
        let x, y;
        if (f.side === 0) { x = W * (.01 + f.u * .32); y = lerp(leftHill(x) + 6, hz - 2, f.v) ; }
        else { x = W * (.76 + f.u * .24); y = hz - H * .06 * f.v; }
        x += Math.sin(time * f.s + f.p) * 6; y += Math.cos(time * f.s * .8 + f.p) * 4;
        const a = p.stars * (.35 + .65 * Math.max(0, Math.sin(time * (1 + f.s) + f.p)));
        g = ctx.createRadialGradient(x, y, 0, x, y, 6);
        g.addColorStop(0, `rgba(226,255,150,${a})`); g.addColorStop(1, 'rgba(226,255,150,0)');
        ctx.fillStyle = g; ctx.fillRect(x - 6, y - 6, 12, 12);
      }
      ctx.restore();
    }
    lampFlash = Math.max(0, lampFlash - dt * 1.5);

    // film grain for a painted, HD finish
    ctx.save(); ctx.globalCompositeOperation = 'overlay'; ctx.fillStyle = grain; ctx.fillRect(0, 0, W, H); ctx.restore();

    // handwritten hints follow their targets
    if (dragNote) {
      const flip = b.x > W - 150;
      dragNote.classList.toggle('flip', flip);
      dragNote.style.transform = `translate(${Math.round(flip ? b.x - 118 : b.x + 22)}px, ${Math.round(Math.max(6, b.y - 40))}px)`;
    }
    if (clickNote) clickNote.style.transform = `translate(${Math.round(lh.x + 18)}px, ${Math.round(lh.y - 48)}px)`;
    root.style.setProperty('--pool', p.night ? '120,140,230' : `${mix([255, 170, 110], [255, 236, 200], p.e).map(v => v | 0)}`);

    if (!reduce || dragging) raf = requestAnimationFrame(draw);
  }
  let lighthouseHit = {x: -999, y: -999, r: 0};

  function start() { cancelAnimationFrame(raf); lastT = performance.now(); raf = requestAnimationFrame(draw); }
  function resize() {
    dpr = Math.min(2.5, window.devicePixelRatio || 1);
    W = scene.clientWidth; H = scene.clientHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cloudCache.clear(); makeGrain(); if (!milky) makeMilky();
    start();
  }

  // ---------------------------------------------------------------- UI sync
  function fmt(h) {
    const hh = Math.floor(h) % 24, mm = Math.floor((h % 1) * 60), ap = hh < 12 ? 'am' : 'pm';
    return `${(hh % 12) || 12}:${String(mm).padStart(2, '0')} ${ap}`;
  }
  function sync() {
    const day = isDay(hour);
    dn.setAttribute('aria-checked', day);
    dn.setAttribute('aria-label', day ? 'Day. Switch to night' : 'Night. Switch to day');
    root.dataset.theme = day ? 'light' : 'dark';
    clock.textContent = fmt(hour);
    when.classList.toggle('manual', !live);
    document.getElementById('whenTxt').textContent = live ? '· your local sky' : '· drag to change';
    scene.setAttribute('aria-label', `Interactive sky showing ${fmt(hour)}. Drag the ${day ? 'sun' : 'moon'}, or use the arrow keys, to change the time of day.`);
    document.querySelector('meta[name=theme-color]')?.setAttribute('content', day ? '#ffffff' : '#0E0F11');
    if (reduce) start();
  }

  // ---------------------------------------------------------------- interaction
  const local = e => { const r = scene.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  function hourFromX(x) {
    const t = clamp((x / W - .07) / .86, 0, 1);
    return isDay(hour) ? 6 + t * 11.99 : (18 + t * 11.99) % 24;
  }
  scene.addEventListener('pointerdown', e => {
    const [x, y] = local(e), b = bodyPos(hour);
    if (Math.hypot(x - lighthouseHit.x, y - lighthouseHit.y) < lighthouseHit.r) {
      lampOn = !lampOn; lampFlash = 1; clickNote?.classList.add('gone'); start(); return;
    }
    if (Math.hypot(x - b.x, y - b.y) > 60) return;
    dragging = true; live = false; scene.setPointerCapture(e.pointerId); scene.style.cursor = 'grabbing';
    if (!dragged) { dragged = true; dragNote?.classList.add('gone'); setTimeout(() => clickNote?.classList.add('show'), 600); setTimeout(() => clickNote?.classList.add('gone'), 9000); }
    e.preventDefault(); start();
  });
  scene.addEventListener('pointermove', e => {
    const [x, y] = local(e);
    if (!dragging) {
      const b = bodyPos(hour);
      scene.style.cursor = Math.hypot(x - b.x, y - b.y) < 60 ? 'grab' : Math.hypot(x - lighthouseHit.x, y - lighthouseHit.y) < lighthouseHit.r ? 'pointer' : '';
      return;
    }
    hour = hourFromX(x); sync();
  });
  const end = () => { dragging = false; scene.style.cursor = ''; };
  scene.addEventListener('pointerup', end); scene.addEventListener('pointercancel', end);

  scene.tabIndex = 0;
  scene.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { lampOn = !lampOn; lampFlash = 1; e.preventDefault(); start(); return; }
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault(); live = false; dragNote?.classList.add('gone');
    const t = clamp(arcT(hour) + (e.key === 'ArrowRight' ? 1 : -1) / 48, 0, .999);
    hour = isDay(hour) ? 6 + t * 12 : (18 + t * 12) % 24; sync();
  });

  dn.addEventListener('click', () => {
    live = false;
    hour = isDay(hour) ? 21.5 : 10.5;
    sync();
    try { localStorage.setItem('rk-theme', isDay(hour) ? 'light' : 'dark'); } catch (e) {}
  });
  document.getElementById('reset').addEventListener('click', () => { live = true; hour = nowHour(); sync(); });
  setInterval(() => { if (live) { hour = nowHour(); sync(); } }, 30000);

  new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) start(); else cancelAnimationFrame(raf); }).observe(scene);
  addEventListener('resize', resize);
  setTimeout(() => { if (!dragged) dragNote?.classList.add('gone'); }, 14000);

  // ---------------------------------------------------------------- rest of the page
  const tr = document.getElementById('track');
  [...tr.children].forEach(n => { const c = n.cloneNode(true); c.setAttribute('aria-hidden', 'true'); tr.appendChild(c); });

  const links = [...document.querySelectorAll('.nav a[href^="#"]')];
  const secs = links.map(a => document.querySelector(a.getAttribute('href')));
  addEventListener('scroll', () => {
    let i = 0; secs.forEach((s, k) => { if (s && s.getBoundingClientRect().top < innerHeight * .5) i = k; });
    links.forEach((a, k) => a.classList.toggle('on', k === i));
  }, {passive: true});

  const q = new URLSearchParams(location.search).get('t');
  if (q !== null && !isNaN(+q)) { hour = +q % 24; live = false; }
  resize(); sync();
})();

(() => {
  const root = document.documentElement;
  const cv = document.getElementById('sky'), ctx = cv.getContext('2d');
  const scene = document.getElementById('scene');
  const dn = document.getElementById('dn'), clock = document.getElementById('clock'), when = document.getElementById('when'), hint = document.getElementById('hint');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // hour: 0..24. Day arc 6→18 for the sun, night arc 18→6 for the moon.
  let hour, live = true, dragging = false, W = 0, H = 0, dpr = 1, t0 = performance.now();
  const nowHour = () => { const d = new Date(); return d.getHours() + d.getMinutes() / 60; };
  hour = nowHour();

  // deterministic pseudo-random
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const stars = Array.from({length: 140}, () => ({x: rnd(), y: rnd() * .62, r: rnd() * 1.3 + .3, p: rnd() * 6.28}));
  const clouds = Array.from({length: 7}, (_, i) => ({x: i / 7 * 1.3 + rnd() * .08, y: .08 + rnd() * .3, s: .6 + rnd() * .8, v: .004 + rnd() * .006, n: 4 + (i % 3)}));
  const birds = Array.from({length: 5}, () => ({x: .55 + rnd() * .2, y: .14 + rnd() * .1, s: 4 + rnd() * 4, p: rnd() * 6}));
  const boats = [{x: .63, s: 1}, {x: .71, s: .7}];

  const lerp = (a, b, k) => a + (b - a) * k;
  const mix = (c1, c2, k) => c1.map((v, i) => Math.round(lerp(v, c2[i], k)));
  const rgb = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const smooth = k => k * k * (3 - 2 * k);

  const isDay = h => h >= 6 && h < 18;
  // position along arc: 0 at rising edge, 1 at setting edge
  const arcT = h => isDay(h) ? (h - 6) / 12 : ((h - 18 + 24) % 24) / 12;
  const horizon = () => H * .64;
  function bodyPos(h) {
    const t = arcT(h), cx = W * (.08 + .84 * t), top = Math.max(46, H * .12), base = horizon() + 10;
    return {x: cx, y: base - Math.sin(Math.PI * t) * (base - top), t};
  }

  // palettes
  const P = {
    noonTop: [42,131,214], noonBot: [197,230,247],
    goldTop: [92,120,190], goldBot: [252,196,140],
    nightTop: [6,9,22], nightBot: [30,44,82],
    seaNoon: [43,134,192], seaNoon2: [127,207,214], seaGold: [70,92,140], seaGold2: [236,170,130], seaNight: [8,16,36], seaNight2: [24,38,70],
  };
  function palette(h) {
    if (isDay(h)) {
      const e = Math.sin(Math.PI * arcT(h));           // elevation 0..1
      const k = smooth(clamp(e / .45, 0, 1));          // 0 = golden hour, 1 = high sun
      return {top: mix(P.goldTop, P.noonTop, k), bot: mix(P.goldBot, P.noonBot, k), sea: mix(P.seaGold, P.seaNoon, k), sea2: mix(P.seaGold2, P.seaNoon2, k), night: 0, e, k};
    }
    const e = Math.sin(Math.PI * arcT(h));
    const k = smooth(clamp(e / .3, 0, 1));             // dusk → deep night
    return {top: mix([40,50,100], P.nightTop, k), bot: mix([120,90,120], P.nightBot, k), sea: mix([30,36,70], P.seaNight, k), sea2: mix([70,60,90], P.seaNight2, k), night: 1, e, k};
  }

  function hill(x0, x1, peak, col, side) {
    const hz = horizon();
    ctx.beginPath(); ctx.moveTo(x0, hz + 2);
    ctx.bezierCurveTo(lerp(x0, x1, .25), hz - peak * 1.1, lerp(x0, x1, .55), hz - peak, x1, hz + 2);
    ctx.closePath(); ctx.fillStyle = col; ctx.fill();
  }

  function cloud(cx, cy, s, n, col) {
    ctx.fillStyle = col; ctx.beginPath();
    for (let i = 0; i < n; i++) {
      const ox = (i - (n - 1) / 2) * 26 * s, oy = -Math.sin((i / (n - 1)) * Math.PI) * 14 * s;
      ctx.moveTo(cx + ox + 30 * s, cy + oy); ctx.ellipse(cx + ox, cy + oy, 30 * s, 18 * s, 0, 0, Math.PI * 2);
    }
    ctx.moveTo(cx + n * 15 * s, cy + 6 * s); ctx.ellipse(cx, cy + 6 * s, n * 15 * s, 9 * s, 0, 0, Math.PI * 2);
    ctx.fill('nonzero');
  }

  function draw(now) {
    const time = (now - t0) / 1000;
    const pal = palette(hour), hz = horizon(), b = bodyPos(hour);

    // sky
    let g = ctx.createLinearGradient(0, 0, 0, hz);
    g.addColorStop(0, rgb(pal.top)); g.addColorStop(1, rgb(pal.bot));
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, hz + 1);

    // stars
    if (pal.night) {
      for (const s of stars) {
        const a = pal.k * (.55 + .45 * Math.sin(time * 1.6 + s.p));
        ctx.fillStyle = `rgba(255,255,255,${a})`;
        ctx.beginPath(); ctx.arc(s.x * W, s.y * hz, s.r, 0, 7); ctx.fill();
      }
    }

    // glow around body
    const glowR = pal.night ? 150 : 260 + (1 - pal.k) * 180;
    g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, glowR);
    if (pal.night) { g.addColorStop(0, 'rgba(220,230,255,.35)'); g.addColorStop(1, 'rgba(220,230,255,0)'); }
    else { g.addColorStop(0, `rgba(255,250,220,${.9})`); g.addColorStop(.25, `rgba(255,${Math.round(lerp(170,235,pal.k))},${Math.round(lerp(110,190,pal.k))},.45)`); g.addColorStop(1, 'rgba(255,220,180,0)'); }
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, hz);

    // clouds
    const cloudCol = pal.night ? `rgba(150,165,205,${.12 + .2 * (1 - pal.k)})` : rgb(mix([255,214,190], [255,255,255], pal.k), .92);
    for (const c of clouds) {
      const x = ((c.x + (reduce ? 0 : time * c.v * .1)) % 1.3) - .15;
      cloud(x * W, c.y * hz, c.s * Math.min(1, W / 1100), c.n, cloudCol);
    }

    // body
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, hz); ctx.clip();
    if (pal.night) {
      ctx.fillStyle = '#F2F4FA'; ctx.shadowColor = 'rgba(220,230,255,.9)'; ctx.shadowBlur = 24;
      ctx.beginPath(); ctx.arc(b.x, b.y, 22, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
      ctx.fillStyle = 'rgba(170,180,200,.35)';
      [[-7,-5,5],[6,4,4],[-2,9,3],[8,-8,2.5]].forEach(([dx,dy,r]) => { ctx.beginPath(); ctx.arc(b.x+dx, b.y+dy, r, 0, 7); ctx.fill(); });
    } else {
      const sc = mix([255,170,90], [255,251,232], pal.k);
      ctx.fillStyle = rgb(sc); ctx.shadowColor = rgb(sc); ctx.shadowBlur = 40;
      ctx.beginPath(); ctx.arc(b.x, b.y, 26, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
      // rays
      ctx.strokeStyle = `rgba(255,255,240,${.25 * pal.k})`; ctx.lineWidth = 2;
      for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283 + time * .08; ctx.beginPath(); ctx.moveTo(b.x + Math.cos(a) * 38, b.y + Math.sin(a) * 38); ctx.lineTo(b.x + Math.cos(a) * 64, b.y + Math.sin(a) * 64); ctx.stroke(); }
    }
    ctx.restore();

    // birds (day)
    if (!pal.night) {
      ctx.strokeStyle = `rgba(30,40,60,${.55 * pal.k + .2})`; ctx.lineWidth = 1.4;
      for (const bd of birds) {
        const x = bd.x * W + (reduce ? 0 : Math.sin(time * .2 + bd.p) * 20), y = bd.y * hz + Math.sin(time * .5 + bd.p) * 4, f = Math.sin(time * 6 + bd.p) * 2;
        ctx.beginPath(); ctx.moveTo(x - bd.s, y - f); ctx.quadraticCurveTo(x - bd.s / 2, y - bd.s / 2, x, y); ctx.quadraticCurveTo(x + bd.s / 2, y - bd.s / 2, x + bd.s, y - f); ctx.stroke();
      }
    }

    // hills
    const hillFar = pal.night ? rgb(mix([40,52,80],[16,24,44],pal.k)) : rgb(mix([150,120,110],[118,170,140],pal.k));
    const hillNear = pal.night ? rgb(mix([30,40,62],[10,16,30],pal.k)) : rgb(mix([110,100,80],[86,150,92],pal.k));
    hill(W * .62, W * 1.05, H * .13, hillFar);
    hill(W * .78, W * 1.12, H * .09, hillNear);
    hill(-W * .08, W * .3, H * .17, hillFar);
    hill(-W * .1, W * .2, H * .11, hillNear);
    // lighthouse on left headland
    const lx = W * .12, ly = horizon() - H * .135;
    ctx.fillStyle = pal.night ? '#c9cfdb' : '#F4F1EA'; ctx.beginPath(); ctx.moveTo(lx - 7, ly + 2); ctx.lineTo(lx - 4.5, ly - 34); ctx.lineTo(lx + 4.5, ly - 34); ctx.lineTo(lx + 7, ly + 2); ctx.fill();
    ctx.fillStyle = '#C2412D'; ctx.fillRect(lx - 6, ly - 18, 12, 6); ctx.fillRect(lx - 5.5, ly - 40, 11, 6);
    if (pal.night || pal.k < .35) {
      const beam = Math.sin(time * .9);
      ctx.fillStyle = 'rgba(255,240,180,.95)'; ctx.beginPath(); ctx.arc(lx, ly - 37, 3, 0, 7); ctx.fill();
      const bx = lx + beam * W * .35, bg = ctx.createLinearGradient(lx, 0, bx, 0);
      bg.addColorStop(0, 'rgba(255,240,180,.35)'); bg.addColorStop(1, 'rgba(255,240,180,0)');
      ctx.fillStyle = bg; ctx.beginPath(); ctx.moveTo(lx, ly - 37); ctx.lineTo(bx, ly - 37 - 18); ctx.lineTo(bx, ly - 37 + 18); ctx.fill();
    }

    // sea
    g = ctx.createLinearGradient(0, hz, 0, H);
    g.addColorStop(0, rgb(pal.sea)); g.addColorStop(.55, rgb(pal.sea2)); g.addColorStop(1, rgb(pal.sea2));
    ctx.fillStyle = g; ctx.fillRect(0, hz, W, H - hz);
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(0, hz, W, 1);

    // reflection column
    const refl = pal.night ? 'rgba(230,236,255,' : `rgba(255,${Math.round(lerp(200,250,pal.k))},${Math.round(lerp(150,220,pal.k))},`;
    const vis = b.y < hz + 6 ? 1 : 0;
    for (let i = 0; i < 26 && vis; i++) {
      const yy = hz + 4 + i * i * .55, w = (12 + i * 3.2) * (1 + .35 * Math.sin(time * 2 + i));
      if (yy > H) break;
      ctx.fillStyle = refl + (.55 - i * .018) + ')';
      ctx.fillRect(b.x - w / 2 + Math.sin(time * 1.3 + i * 1.7) * 6, yy, w, 1.6 + i * .05);
    }
    // ripples
    ctx.strokeStyle = 'rgba(255,255,255,.12)'; ctx.lineWidth = 1;
    for (let i = 0; i < 18; i++) {
      const yy = hz + 10 + (i * 37 % (H - hz)), xx = ((i * 191 + time * 8) % (W + 80)) - 40;
      ctx.beginPath(); ctx.moveTo(xx, yy); ctx.lineTo(xx + 24 + (i % 4) * 8, yy); ctx.stroke();
    }
    // boats
    for (const bt of boats) {
      const x = bt.x * W + (reduce ? 0 : Math.sin(time * .15 + bt.x * 9) * 14), y = hz + 8 * bt.s + Math.sin(time * 1.2 + bt.x * 5) * .8, s = bt.s * 10;
      ctx.fillStyle = pal.night ? 'rgba(200,210,230,.6)' : 'rgba(255,255,255,.95)';
      ctx.beginPath(); ctx.moveTo(x, y - s * 2.2); ctx.lineTo(x, y - 1); ctx.lineTo(x + s * 1.2, y - 1); ctx.fill();
      ctx.fillStyle = pal.night ? 'rgba(20,28,50,.9)' : 'rgba(40,50,70,.85)';
      ctx.beginPath(); ctx.moveTo(x - s * .9, y); ctx.lineTo(x + s * 1.5, y); ctx.lineTo(x + s * 1.1, y + s * .45); ctx.lineTo(x - s * .6, y + s * .45); ctx.fill();
    }

    if (!reduce || dragging) raf = requestAnimationFrame(draw);
  }

  let raf = 0, visible = true;
  function start() { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); }
  function resize() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = scene.clientWidth; H = scene.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    start();
  }

  // ---------- UI sync ----------
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
    hint.textContent = day ? '☀︎ Drag the sun' : '☾ Drag the moon';
    document.querySelector('meta[name=theme-color]')?.setAttribute('content', day ? '#ffffff' : '#0E0F11');
    if (reduce) start();
  }

  // ---------- drag ----------
  function hourFromX(x) {
    const t = clamp((x / W - .08) / .84, 0, 1);
    return isDay(hour) ? 6 + t * 12 : (18 + t * 12) % 24;
  }
  scene.addEventListener('pointerdown', e => {
    const r = scene.getBoundingClientRect(), b = bodyPos(hour);
    const x = e.clientX - r.left, y = e.clientY - r.top;
    if (Math.hypot(x - b.x, y - b.y) > 70) return;
    dragging = true; live = false; scene.setPointerCapture(e.pointerId); scene.style.cursor = 'grabbing';
    hint.classList.add('gone'); e.preventDefault(); start();
  });
  scene.addEventListener('pointermove', e => {
    const r = scene.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
    if (!dragging) { const b = bodyPos(hour); scene.style.cursor = Math.hypot(x - b.x, y - b.y) < 70 ? 'grab' : ''; return; }
    hour = hourFromX(x); sync();
  });
  const end = () => { dragging = false; scene.style.cursor = ''; };
  scene.addEventListener('pointerup', end); scene.addEventListener('pointercancel', end);

  // keyboard: arrows move the sun when the scene is focused
  scene.tabIndex = 0;
  scene.addEventListener('keydown', e => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault(); live = false;
    const t = clamp(arcT(hour) + (e.key === 'ArrowRight' ? 1 : -1) / 48, 0, .999);
    hour = isDay(hour) ? 6 + t * 12 : (18 + t * 12) % 24; sync();
  });

  dn.addEventListener('click', () => {
    live = false;
    hour = isDay(hour) ? 21 : 10.5;   // jump to a nice night / morning
    sync();
    try { localStorage.setItem('rk-theme', isDay(hour) ? 'light' : 'dark'); } catch (e) {}
  });
  document.getElementById('reset').addEventListener('click', () => { live = true; hour = nowHour(); sync(); });
  setInterval(() => { if (live) { hour = nowHour(); sync(); } }, 30000);

  new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) start(); else cancelAnimationFrame(raf); }).observe(scene);
  addEventListener('resize', resize);
  setTimeout(() => hint.classList.add('gone'), 6000);

  // duplicate gallery for seamless marquee
  const tr = document.getElementById('track');
  [...tr.children].forEach(n => { const c = n.cloneNode(true); c.setAttribute('aria-hidden', 'true'); tr.appendChild(c); });

  // active nav
  const links = [...document.querySelectorAll('.nav a[href^="#"]')];
  const secs = links.map(a => document.querySelector(a.getAttribute('href')));
  addEventListener('scroll', () => {
    let i = 0; secs.forEach((s, k) => { if (s && s.getBoundingClientRect().top < innerHeight * .5) i = k; });
    links.forEach((a, k) => a.classList.toggle('on', k === i));
  }, {passive: true});

  // honour ?t=21 for previews
  const q = new URLSearchParams(location.search).get('t');
  if (q !== null && !isNaN(+q)) { hour = +q % 24; live = false; }
  resize(); sync();
})();

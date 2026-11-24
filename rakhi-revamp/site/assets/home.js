/* Homepage: real-photo Spiti hero + page chrome.
   A real photo of Key Monastery with the Langza Buddha, graded live for the hour of the
   visitor's local sky. Drag the sun (day) or moon (night) across the real skyline to change
   the hour; the whole page follows into light or dark. Click the Buddha to light butter lamps. */
(() => {
  const root = document.documentElement;
  const scene = document.getElementById('scene'), photo = document.getElementById('photo'), bud = document.getElementById('buddha');
  const cv = document.getElementById('sky'), ctx = cv.getContext('2d');
  const gGold = document.getElementById('gradeGold'), gNight = document.getElementById('gradeNight'), lamps = document.getElementById('lamps');
  const dn = document.getElementById('dn'), clock = document.getElementById('clock'), when = document.getElementById('when');
  const dragNote = document.getElementById('dragNote'), clickNote = document.getElementById('clickNote');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  let hour, live = true, dragging = false, W = 0, H = 0, dpr = 1, raf = 0, visible = true, dragged = false, lampOn = false, time = 0, last = performance.now();
  const nowHour = () => { const d = new Date(); return d.getHours() + d.getMinutes() / 60; };
  hour = nowHour();
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const smooth = (a, b, v) => { const k = clamp((v - a) / (b - a), 0, 1); return k * k * (3 - 2 * k); };
  const isDay = h => h >= 6 && h < 18;
  const arcT = h => isDay(h) ? (h - 6) / 12 : ((h - 18 + 24) % 24) / 12;

  // how dark (0 day .. 1 night) and how golden (sunrise / sunset) the hour is
  const nightAmt = h => Math.max(1 - smooth(5.2, 6.5, h), smooth(17.6, 18.9, h));
  const goldAmt = h => Math.max(Math.exp(-((h - 17.3) ** 2) / .7), Math.exp(-((h - 6.7) ** 2) / .7)) * (1 - nightAmt(h));

  // photo framing (object-fit: cover) — shared with the sky mask so they line up
  let posX = .62, posY = .42;
  const mask = new Image(); mask.src = 'assets/sky-mask.png'; mask.onload = () => draw();
  const IMG_W = 1200, IMG_H = 800;
  function cover() { const s = Math.max(W / IMG_W, H / IMG_H), dw = IMG_W * s, dh = IMG_H * s; return [(W - dw) * posX, (H - dh) * posY, dw, dh]; }

  // the sun / moon path: rises behind the left ridge, sets behind the right one
  function bodyPos(h) { const t = arcT(h); return {x: W * (.08 + .84 * t), y: H * .56 - Math.sin(Math.PI * t) * H * .48, t}; }

  let seed = 13; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const stars = Array.from({length: 520}, () => ({x: rnd(), y: rnd() * .62, r: rnd() < .05 ? 1.3 + rnd() : .3 + rnd() * .65, p: rnd() * 6.28, s: .6 + rnd() * 2}));
  let milky = null;
  function makeMilky() {
    milky = document.createElement('canvas'); milky.width = 900; milky.height = 260; const g = milky.getContext('2d');
    for (let i = 0; i < 700; i++) { const u = Math.random() * 900, v = 130 + (Math.random() - .5) * 110 * Math.random(), R = 8 + Math.random() * 30;
      const gr = g.createRadialGradient(u, v, 0, u, v, R); gr.addColorStop(0, 'rgba(190,200,255,.06)'); gr.addColorStop(1, 'rgba(190,200,255,0)'); g.fillStyle = gr; g.fillRect(u - R, v - R, 2 * R, 2 * R); }
  }

  function grade() {
    const n = nightAmt(hour), g = goldAmt(hour);
    const f = `brightness(${(1 - .2 * g - .64 * n).toFixed(3)}) contrast(${(1 + .1 * g + .14 * n).toFixed(3)}) saturate(${(1 + .32 * g - .45 * n).toFixed(3)}) sepia(${(.42 * g).toFixed(3)}) hue-rotate(${(8 * n).toFixed(1)}deg)`;
    photo.style.filter = f;
    bud.style.filter = f + ` saturate(${(.8 + .2 * n).toFixed(2)}) contrast(.93) drop-shadow(10px 14px 18px rgba(0,0,0,.3))`;
    gGold.style.opacity = g.toFixed(3); gNight.style.opacity = n.toFixed(3);
    lamps.style.opacity = Math.max(lampOn ? 1 : 0, n * .85).toFixed(2);
    root.style.setProperty('--pool', n > .5 ? '120,140,230' : g > .3 ? '255,170,110' : '255,236,200');
  }

  function draw(now = performance.now()) {
    const dt = Math.min(.05, (now - last) / 1000); last = now; if (!reduce) time += dt;
    const n = nightAmt(hour), g = goldAmt(hour), b = bodyPos(hour);
    ctx.clearRect(0, 0, W, H);
    // stars + milky way
    if (n > .02) {
      ctx.globalAlpha = n * .9; ctx.save(); ctx.translate(W * .5, H * .22); ctx.rotate(-.42); ctx.drawImage(milky, -W * .7, -H * .22, W * 1.4, H * .44); ctx.restore();
      for (const s of stars) { const a = n * (.4 + .6 * Math.sin(time * s.s + s.p) ** 2); ctx.globalAlpha = a; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(s.x * W, s.y * H, s.r, 0, 7); ctx.fill(); }
      ctx.globalAlpha = 1;
    }
    // glow + body
    const night = !isDay(hour);
    const col = night ? '225,232,255' : g > .25 ? '255,186,120' : '255,247,225';
    let gr = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, night ? 170 : W * .42);
    gr.addColorStop(0, `rgba(${col},${night ? .3 : .75})`); gr.addColorStop(night ? .3 : .08, `rgba(${col},${night ? .1 : .32})`); gr.addColorStop(1, `rgba(${col},0)`);
    ctx.fillStyle = gr; ctx.fillRect(0, 0, W, H);
    ctx.shadowColor = `rgb(${col})`; ctx.shadowBlur = night ? 26 : 42; ctx.fillStyle = night ? '#f4f6fb' : `rgb(${col})`;
    ctx.beginPath(); ctx.arc(b.x, b.y, night ? 14 : 18, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
    if (night) { ctx.fillStyle = 'rgba(150,160,185,.28)'; [[-4, -3, 3.4], [4, 3, 2.6], [-1, 6, 2]].forEach(([a, c, r]) => { ctx.beginPath(); ctx.arc(b.x + a, b.y + c, r, 0, 7); ctx.fill(); }); }
    // keep everything inside the real sky
    if (mask.complete && mask.naturalWidth) { const [x, y, w, h] = cover(); ctx.globalCompositeOperation = 'destination-in'; ctx.drawImage(mask, x, y, w, h); ctx.globalCompositeOperation = 'source-over'; }
    // hints follow their targets
    if (dragNote) { const flip = b.x > W - 150; dragNote.classList.toggle('flip', flip);
      dragNote.style.transform = `translate(${Math.round(flip ? b.x - 118 : b.x + 22)}px, ${Math.round(Math.max(6, b.y - 40))}px)`; }
    if (clickNote) { const r = bud.getBoundingClientRect(), sr = scene.getBoundingClientRect();
      clickNote.style.transform = `translate(${Math.round(r.right - sr.left - 10)}px, ${Math.round(r.top - sr.top + 10)}px)`; }
    if (visible && !reduce && n > .02) raf = requestAnimationFrame(draw);
  }
  function start() { cancelAnimationFrame(raf); last = performance.now(); raf = requestAnimationFrame(draw); }
  function resize() {
    dpr = Math.min(2, window.devicePixelRatio || 1); W = scene.clientWidth; H = scene.clientHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    posX = W / H < .9 ? .74 : .62; photo.style.objectPosition = `${posX * 100}% ${posY * 100}%`;
    if (!milky) makeMilky(); start();
  }

  // ---------------------------------------------------------------- UI sync
  function fmt(h) { const hh = Math.floor(h) % 24, mm = Math.floor((h % 1) * 60), ap = hh < 12 ? 'am' : 'pm'; return `${(hh % 12) || 12}:${String(mm).padStart(2, '0')} ${ap}`; }
  function sync() {
    const day = isDay(hour);
    dn.setAttribute('aria-checked', day); dn.setAttribute('aria-label', day ? 'Day. Switch to night' : 'Night. Switch to day');
    root.dataset.theme = day ? 'light' : 'dark';
    clock.textContent = fmt(hour); when.classList.toggle('manual', !live);
    document.getElementById('whenTxt').textContent = live ? '· your local sky' : '· drag to change';
    scene.setAttribute('aria-label', `Key Monastery in Spiti at ${fmt(hour)}. Drag the ${day ? 'sun' : 'moon'}, or use the arrow keys, to change the time of day.`);
    document.querySelector('meta[name=theme-color]')?.setAttribute('content', day ? '#ffffff' : '#0E0F11');
    grade(); start();
  }

  // ---------------------------------------------------------------- interaction
  const local = e => { const r = scene.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  const onBuddha = e => { const r = bud.getBoundingClientRect(); return e.clientX > r.left + r.width * .2 && e.clientX < r.right - r.width * .2 && e.clientY > r.top && e.clientY < r.bottom; };
  function hourFromX(x) { const t = clamp((x / W - .08) / .84, 0, .999); return isDay(hour) ? 6 + t * 12 : (18 + t * 12) % 24; }
  function toggleLamps() { lampOn = !lampOn; bud.classList.add('blessed'); setTimeout(() => bud.classList.remove('blessed'), 900); clickNote?.classList.add('gone'); grade(); }
  scene.addEventListener('pointerdown', e => {
    if (onBuddha(e)) { toggleLamps(); return; }
    const [x, y] = local(e), b = bodyPos(hour);
    if (Math.hypot(x - b.x, y - b.y) > 60) return;
    dragging = true; live = false; scene.setPointerCapture(e.pointerId); scene.style.cursor = 'grabbing';
    if (!dragged) { dragged = true; dragNote?.classList.add('gone'); setTimeout(() => clickNote?.classList.add('show'), 600); setTimeout(() => clickNote?.classList.add('gone'), 9000); }
    e.preventDefault();
  });
  scene.addEventListener('pointermove', e => {
    if (!dragging) { const [x, y] = local(e), b = bodyPos(hour); scene.style.cursor = Math.hypot(x - b.x, y - b.y) < 60 ? 'grab' : onBuddha(e) ? 'pointer' : ''; return; }
    hour = hourFromX(local(e)[0]); sync();
  });
  const end = () => { dragging = false; scene.style.cursor = ''; };
  scene.addEventListener('pointerup', end); scene.addEventListener('pointercancel', end);
  scene.tabIndex = 0;
  scene.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleLamps(); return; }
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault(); live = false; dragNote?.classList.add('gone');
    const t = clamp(arcT(hour) + (e.key === 'ArrowRight' ? 1 : -1) / 48, 0, .999);
    hour = isDay(hour) ? 6 + t * 12 : (18 + t * 12) % 24; sync();
  });
  dn.addEventListener('click', () => { live = false; hour = isDay(hour) ? 21.5 : 10.5; sync(); try { localStorage.setItem('rk-theme', isDay(hour) ? 'light' : 'dark'); } catch (e) {} });
  document.getElementById('reset').addEventListener('click', () => { live = true; hour = nowHour(); sync(); });
  setInterval(() => { if (live) { hour = nowHour(); sync(); } }, 30000);
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) start(); else cancelAnimationFrame(raf); }).observe(scene);
  addEventListener('resize', resize);
  bud.addEventListener('load', () => draw());
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

  // ---------------------------------------------------------------- projects: filters
  const projs = [...document.querySelectorAll('.proj')], status = document.getElementById('filterStatus');
  document.querySelectorAll('.filters button').forEach(btn => btn.addEventListener('click', () => {
    const f = btn.dataset.f;
    document.querySelectorAll('.filters button').forEach(b => { const on = b === btn; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); });
    let n = 0;
    projs.forEach(pr => { const show = f === 'all' || pr.dataset.cat === f; pr.classList.toggle('hide', !show); if (show) { n++; pr.classList.remove('in'); requestAnimationFrame(() => pr.classList.add('in')); } });
    if (status) status.textContent = `Showing ${n} project${n === 1 ? '' : 's'}`;
  }));

  // ---------------------------------------------------------------- projects: tilt, parallax, cursor bubble
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (fine && !reduce) {
    const bubble = document.createElement('div'); bubble.className = 'cursor'; bubble.setAttribute('aria-hidden', 'true'); document.body.appendChild(bubble);
    let bx = 0, by = 0, tx = 0, ty = 0, bubbleRaf = 0;
    const follow = () => { bx += (tx - bx) * .22; by += (ty - by) * .22; bubble.style.left = bx + 'px'; bubble.style.top = by + 'px';
      if (Math.abs(tx - bx) + Math.abs(ty - by) > .5) bubbleRaf = requestAnimationFrame(follow); else bubbleRaf = 0; };
    projs.forEach(pr => {
      const media = pr.querySelector('[data-tilt]'), img = media.querySelector('.stage') || media.querySelector('img');
      const layers = [...media.querySelectorAll('.layer')];
      layers.forEach(l => l.style.setProperty('--d', l.dataset.depth || 1));
      pr.addEventListener('pointerenter', e => {
        bubble.innerHTML = pr.querySelector('.proj-cta').innerHTML; bubble.classList.add('on');
        bx = tx = e.clientX; by = ty = e.clientY; follow();
      });
      pr.addEventListener('pointermove', e => {
        tx = e.clientX; ty = e.clientY; if (!bubbleRaf) bubbleRaf = requestAnimationFrame(follow);
        const r = media.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width - .5, ny = (e.clientY - r.top) / r.height - .5;
        img.style.setProperty('--ry', (nx * 7).toFixed(2) + 'deg'); img.style.setProperty('--rx', (-ny * 6).toFixed(2) + 'deg');
        layers.forEach(l => { l.style.setProperty('--px', (nx * -14).toFixed(1)); l.style.setProperty('--py', (ny * -10).toFixed(1)); });
      });
      pr.addEventListener('pointerleave', () => {
        bubble.classList.remove('on');
        img.style.setProperty('--rx', '0deg'); img.style.setProperty('--ry', '0deg');
        layers.forEach(l => { l.style.setProperty('--px', 0); l.style.setProperty('--py', 0); });
      });
    });
  }

  // ---------------------------------------------------------------- experience: timeline bars, tabs, durations
  const now = new Date(), nowY = now.getFullYear() + now.getMonth() / 12, Y0 = 2020, SPAN = 7;
  document.querySelectorAll('.bar').forEach(bar => {
    const from = +bar.dataset.from, to = bar.dataset.to === 'now' ? nowY : +bar.dataset.to;
    bar.style.setProperty('--l', ((from - Y0) / SPAN * 100).toFixed(2) + '%');
    bar.style.setProperty('--w', ((to - from) / SPAN * 100).toFixed(2) + '%');
    if (bar.dataset.to === 'now') bar.classList.add('live');
  });
  const ym = v => { const [y, m] = v.split('-').map(Number); return y * 12 + (m - 1); };
  document.querySelectorAll('.dur').forEach(d => {
    const a = ym(d.dataset.from), b = d.dataset.to === 'now' ? now.getFullYear() * 12 + now.getMonth() : ym(d.dataset.to);
    const m = Math.max(1, b - a), y = Math.floor(m / 12), r = m % 12;
    d.textContent = [y ? `${y} yr${y > 1 ? 's' : ''}` : '', r ? `${r} mo${r > 1 ? 's' : ''}` : ''].filter(Boolean).join(' ');
  });
  const tabs = [...document.querySelectorAll('.lanes [role=tab]')];
  const select = (t, focus) => {
    tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
    if (focus) t.focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', e => {
      const k = {ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1}[e.key];
      if (k) { e.preventDefault(); select(tabs[(i + k + tabs.length) % tabs.length], true); }
      if (e.key === 'Home') { e.preventDefault(); select(tabs[0], true); }
      if (e.key === 'End') { e.preventDefault(); select(tabs[tabs.length - 1], true); }
    });
  });

  // ---------------------------------------------------------------- reveal on scroll + count-up stats
  const countUp = el => {
    const end = +el.dataset.count; if (reduce) { el.textContent = end; return; }
    const t0 = performance.now(), step = t => { const k = Math.min(1, (t - t0) / 900); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); };
    el.textContent = 0; requestAnimationFrame(step);
  };
  const toReveal = [...document.querySelectorAll('.reveal')];
  document.querySelectorAll('.projects .proj').forEach((el, i) => el.style.setProperty('--delay', (i % 2 ? .12 : 0) + 's'));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in'); io.unobserve(e.target);
      e.target.querySelectorAll('[data-count]').forEach(countUp);
    }), {rootMargin: '0px 0px -10% 0px'});
    toReveal.forEach(el => io.observe(el));
  } else toReveal.forEach(el => el.classList.add('in'));

  const q = new URLSearchParams(location.search).get('t');
  if (q !== null && !isNaN(+q)) { hour = +q % 24; live = false; }
  resize(); sync();
})();

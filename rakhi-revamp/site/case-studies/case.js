(() => {
  const root = document.documentElement;
  root.classList.add('js');

  // ---- theme: saved choice, else the visitor's local time (same rule as the homepage sky)
  const dn = document.getElementById('dn');
  let saved = null;
  try { saved = localStorage.getItem('rk-theme'); } catch (e) {}
  const h = new Date().getHours();
  const apply = t => {
    root.dataset.theme = t;
    dn.setAttribute('aria-checked', t === 'light');
    dn.setAttribute('aria-label', t === 'light' ? 'Day. Switch to night' : 'Night. Switch to day');
  };
  apply(saved || (h >= 6 && h < 18 ? 'light' : 'dark'));
  dn.addEventListener('click', () => {
    const t = root.dataset.theme === 'light' ? 'dark' : 'light';
    apply(t);
    try { localStorage.setItem('rk-theme', t); } catch (e) {}
  });

  // ---- mobile drawer
  const side = document.getElementById('side'), tog = document.getElementById('tocBtn'), scrim = document.querySelector('.scrim');
  const setOpen = o => { side.classList.toggle('open', o); tog && tog.setAttribute('aria-expanded', o); };
  tog && tog.addEventListener('click', () => setOpen(!side.classList.contains('open')));
  scrim && scrim.addEventListener('click', () => setOpen(false));
  side.querySelectorAll('.toc a').forEach(a => a.addEventListener('click', () => setOpen(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });

  // ---- active section + progress
  const links = [...document.querySelectorAll('.toc a')];
  const secs = links.map(a => document.getElementById(a.hash.slice(1)));
  const bar = document.querySelector('.progress');
  const onScroll = () => {
    let i = 0;
    secs.forEach((s, k) => { if (s && s.getBoundingClientRect().top < innerHeight * .35) i = k; });
    links.forEach((a, k) => { a.classList.toggle('on', k === i); if (k === i) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = (max > 0 ? scrollY / max * 100 : 0) + '%';
  };
  addEventListener('scroll', onScroll, {passive: true}); onScroll();

  // ---- generic tab sets (process stepper + screen gallery)
  document.querySelectorAll('[data-tabs]').forEach(set => {
    const tabs = [...set.querySelectorAll('[role=tab]')], meter = set.querySelector('.step-meter span');
    const pick = (t, focus) => {
      tabs.forEach((x, i) => {
        const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
        if (on && meter) meter.style.setProperty('--p', ((i + 1) / tabs.length * 100) + '%');
      });
      if (focus) t.focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => pick(t));
      t.addEventListener('keydown', e => {
        const k = {ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1}[e.key];
        if (k) { e.preventDefault(); pick(tabs[(i + k + tabs.length) % tabs.length], true); }
        if (e.key === 'Home') { e.preventDefault(); pick(tabs[0], true); }
        if (e.key === 'End') { e.preventDefault(); pick(tabs[tabs.length - 1], true); }
      });
    });
    if (tabs.length) pick(tabs.find(t => t.getAttribute('aria-selected') === 'true') || tabs[0]);
  });

  // ---- insight -> decision flip cards
  document.querySelectorAll('.flip-btn').forEach(b => {
    const front = b.querySelector('.front'), back = b.querySelector('.back');
    const set = open => { b.setAttribute('aria-expanded', open); front.setAttribute('aria-hidden', open); back.setAttribute('aria-hidden', !open); };
    set(false);
    b.addEventListener('click', () => set(b.getAttribute('aria-expanded') !== 'true'));
  });

  // ---- zoomable screens in a lightbox
  const zooms = [...document.querySelectorAll('.zoom')], lb = document.getElementById('lightbox');
  if (lb && zooms.length) {
    const img = lb.querySelector('img'), cap = lb.querySelector('p');
    let cur = 0, opener = null;
    const show = i => { cur = (i + zooms.length) % zooms.length; const z = zooms[cur], src = z.querySelector('img');
      img.src = z.dataset.full || src.currentSrc || src.src; img.alt = src.alt; cap.textContent = src.alt; };
    zooms.forEach((z, i) => z.addEventListener('click', () => { opener = z; show(i); lb.showModal(); }));
    lb.querySelector('.lb-close').addEventListener('click', () => lb.close());
    lb.querySelector('.lb-prev').addEventListener('click', () => show(cur - 1));
    lb.querySelector('.lb-next').addEventListener('click', () => show(cur + 1));
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', e => { if (e.key === 'ArrowRight') show(cur + 1); if (e.key === 'ArrowLeft') show(cur - 1); });
    lb.addEventListener('close', () => opener && opener.focus());
    if (zooms.length < 2) lb.querySelectorAll('.lb-prev,.lb-next').forEach(b => b.hidden = true);
  }

  // ---- reveal on scroll
  const items = document.querySelectorAll('.cs-reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(n => n.classList.add('in')); return; }
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), {rootMargin: '0px 0px -8% 0px'});
  items.forEach(n => io.observe(n));
})();

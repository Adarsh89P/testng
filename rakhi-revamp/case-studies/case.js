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

  // ---- reveal on scroll
  const items = document.querySelectorAll('.cs-reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(n => n.classList.add('in')); return; }
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), {rootMargin: '0px 0px -8% 0px'});
  items.forEach(n => io.observe(n));
})();

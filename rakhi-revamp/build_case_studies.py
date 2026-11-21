import re, html, os, shutil, sys
SRC = sys.argv[1]; OUT = sys.argv[2]
PAGES = ['healthcare_case_study.html','yoga_case_study.html','malta_taxi_case_study.html','banking_case_study.html']
LINKEDIN = 'https://www.linkedin.com/in/rakhi-das-183381158/'
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
BACK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 8H3M7 4L3 8l4 4"/></svg>'
LIST = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M3 4h10M3 8h10M3 12h6"/></svg>'

HC_HERO = '''<figure class="cs-hero-figure cs-reveal"><div class="stack" role="img" aria-label="The healthcare product suite: the bookings dashboard in a browser, with the patient app on a phone in front">
  <div class="browser"><div class="bar"><i></i><i></i><i></i><span>clinic.dashboard / bookings</span></div>
  <img src="../public/Healthcare/banner/dash.png" alt="" width="1700" height="816" fetchpriority="high" decoding="async"></div>
  <picture><source srcset="../public/Healthcare/banner/phone-app.webp" type="image/webp"><img class="float" src="../public/Healthcare/banner/phone-app.png" alt="" width="319" height="658" decoding="async"></picture>
</div></figure>'''

def text(x): return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', x)).split())

def cut_block(s, start_idx):
    """return end index of the element starting at start_idx (balanced on its tag name)"""
    tag = re.match(r'<(\w+)', s[start_idx:]).group(1)
    depth = 0
    for m in re.finditer(r'<(/?)%s\b[^>]*>' % tag, s[start_idx:]):
        depth += -1 if m.group(1) else 1
        if depth == 0: return start_idx + m.end()
    raise ValueError('unbalanced')

assets = set(); report = []
for name in PAGES:
    s = open(os.path.join(SRC, 'case-studies', name), encoding='utf-8').read()
    title = text(re.search(r'<title>([\s\S]*?)</title>', s).group(1))
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = desc.group(1) if desc else ''
    proj = text(re.search(r'class="cs-nav-title">([\s\S]*?)</span>', s).group(1))
    kicker = text(re.search(r'class="cs-kicker[^"]*">([\s\S]*?)</p>', s).group(1))
    drawer = re.search(r'<div class="cs-drawer"[\s\S]*?</ol>', s).group(0)
    toc = re.findall(r'<a href="#([^"]+)">([\s\S]*?)</a>', drawer)

    main = s[s.index('<main'):s.index('</main>') + 7]
    main = re.sub(r'<!--[\s\S]*?-->', '', main)
    # drop the author's private TODO notes
    n0 = len(re.findall(r'class="cs-pending', main))
    while 'class="cs-pending' in main:
        i = main.index('class="cs-pending'); i = main.rindex('<div', 0, i)
        main = main[:i] + main[cut_block(main, i):]
    # healthcare layered hero -> composed figure
    if 'class="hero-stage' in main:
        i = main.index('<figure class="cs-hero-figure'); main = main[:i] + HC_HERO + main[cut_block(main, i):]
    main = main.replace('../index.html#works', '../index.html#work')
    main = main.replace('<figure class="cs-hero-figure">', '<figure class="cs-hero-figure cs-reveal">')
    # sections left with only a heading after removing notes
    empty = []
    for m in re.finditer(r'<section[^>]*id="([^"]+)"[\s\S]*?</section>', main):
        body = re.sub(r'<p class="cs-sec-label[\s\S]*?</p>|<h2[\s\S]*?</h2>|<p class="cs-lead[\s\S]*?</p>', '', m.group(0))
        if len(text(body)) < 20 and '<img' not in body: empty.append(m.group(1))
    for sid in empty:
        i = main.index(f'id="{sid}"'); i = main.rindex('<section', 0, i)
        main = main[:i] + main[cut_block(main, i):]
        toc = [t for t in toc if t[0] != sid]
    cnt = iter(range(1, 100))
    main = re.sub(r'(class="cs-sec-label[^"]*">)\s*\d\d —', lambda m: f'{m.group(1)}{next(cnt):02d} —', main)
    report.append(f'{name}: removed {n0} TODO notes; removed empty sections {empty}')

    for p in re.findall(r'(?:src|srcset)="(\.\./public/[^"\s]+)', main): assets.add(p)

    toc_html = '\n'.join(f'<a href="#{sid}"><i>{k:02d}</i>{text(lbl)}</a>' for k, (sid, lbl) in enumerate(toc, 1))
    idx = PAGES.index(name); nxt = PAGES[(idx + 1) % len(PAGES)]
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%2310141B'/%3E%3Ctext x='32' y='45' font-family='Georgia,serif' font-size='40' fill='%23fff' text-anchor='middle'%3ER%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="case.css">
<script>try{{var t=localStorage.getItem('rk-theme');var h=new Date().getHours();document.documentElement.dataset.theme=t||(h>=6&&h<18?'light':'dark')}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<span class="progress" aria-hidden="true"></span>

<aside class="side" id="side" aria-label="Case study sections">
  <a class="home" href="../index.html#work">{BACK} Home</a>
  <p class="side-title">{html.escape(proj)}</p>
  <p class="side-sub">{html.escape(kicker)}</p>
  <nav class="toc">
{toc_html}
  </nav>
  <div class="side-foot">
    <a href="{nxt}">Next case study →</a>
    <a href="mailto:dasrakhi303@gmail.com">dasrakhi303@gmail.com</a>
  </div>
</aside>
<div class="scrim" aria-hidden="true"></div>

<div class="mnav glass"><a href="../index.html#work">{BACK} Home</a><button type="button" id="tocBtn" aria-expanded="false" aria-controls="side">{LIST} Sections</button></div>
<div class="topbar"><div class="dn-wrap glass"><button class="dn" id="dn" role="switch" aria-checked="true" aria-label="Day. Switch to night"><span class="stars"></span><span class="knob"></span></button></div></div>

{main}

<footer class="foot">
  <div class="cs-shell foot-in">
    <div><h2>let’s <em>talk</em></h2><p>Open to full-time product design roles. Happy to walk through this project, or any of the others.</p></div>
    <div class="acts">
      <a class="btn btn-primary" href="mailto:dasrakhi303@gmail.com">dasrakhi303@gmail.com {ARROW}</a>
      <a class="btn btn-outline" href="../assets/Rakhi_Das_UIUX_Designer_Resume.pdf" download>Download résumé</a>
    </div>
  </div>
  <div class="cs-shell foot-line"><span>© 2026 Rakhi Das</span><span><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a><a href="https://www.behance.net/rakhidas1" target="_blank" rel="noopener">Behance ↗</a></span></div>
</footer>
<script src="case.js"></script>
</body>
</html>
'''
    open(os.path.join(OUT, 'case-studies', name), 'w', encoding='utf-8').write(out)

missing = []
for p in sorted(assets):
    rel = html.unescape(p[3:]).replace('%20', ' ')
    src = os.path.join(SRC, rel); dst = os.path.join(OUT, rel)
    if not os.path.exists(src): missing.append(rel); continue
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
print('\n'.join(report)); print('assets', len(assets), 'missing', missing)

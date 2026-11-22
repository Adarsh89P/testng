"""Build the four case-study pages from one template.

Edit the CONTENT below and run:  python3 rakhi-revamp/tools/build_case_studies.py
Pages are written to rakhi-revamp/site/case-studies/. Keep copy short: each page
is meant to be read in about three minutes.
"""
import html, os, re
from urllib.parse import quote

SITE = os.path.join(os.path.dirname(__file__), '..', 'site')
OUT = os.path.join(SITE, 'case-studies')
BASE = 'https://rakhidas25.github.io/rakhi-das-portfolio/'
LINKEDIN = 'https://www.linkedin.com/in/rakhi-das-183381158/'
ORDER = ['healthcare', 'yoga', 'malta_taxi', 'banking']

# ----------------------------------------------------------------------------- content
CONTENT = {
'healthcare': dict(
  short='Healthcare platform', kicker='Healthcare · Product design',
  title='One connected system for <em>faster, simpler</em> diagnostics.',
  sub='A diagnostic platform that puts patients, front-desk staff, admins and home-collection teams on one shared record, across five products.',
  facts=[('Role', 'Sole UI/UX designer'), ('Timeline', 'Mar – Jul 2025'), ('Platform', 'Web + mobile · 5 products'), ('I did', 'Research · UX · UI · Prototyping')],
  hero='stack',
  glance=[('Problem', 'Booking, tracking and reporting a test was split across tools that didn’t talk to each other.'),
          ('Users', 'Patients, front-desk executives, administrators, phlebotomists and home collectors.'),
          ('Solution', 'Five interfaces sharing one record, one status vocabulary and one component set.'),
          ('Outcome', 'Less manual re-entry, and a test patients can follow from booking to report.')],
  problem='Patients couldn’t see what happened after booking, so they phoned the desk. Internally, the same journey was stitched together by hand across front desk, admin and home collection — which is where the delays and errors came from.',
  pains=['Fragmented information', 'Manual handoffs between roles', 'No visibility of a test’s status'],
  process=[('Discover', 'Contextual inquiry with the teams running the service, research across all five roles, and a map of the existing workflow.'),
           ('Define', 'Findings documented and the user journey prioritised, so the MVP had a defensible scope rather than a wish list.'),
           ('Ideate', 'Directions explored in low fidelity first, then high-fidelity prototypes once the structure was agreed.'),
           ('Validate & ship', 'Feasibility tested with the teams who would run it, then release and monitoring.')],
  insights=[('Patients weren’t confused by the booking form — they were confused by the silence after it.', 'Made status the spine of the patient app: every test carries one visible state from booking to report, and the report lives in the same place.'),
            ('The front desk was absorbing the system’s complexity by re-keying the same details.', 'One quick registration path, with tests and appointments on a single screen so the desk stops switching systems.'),
            ('Every role could see its own step, and no role could see the operation.', 'One connected system: admins get a single control surface, collectors get assigned tasks and a route, all on the records the desk uses.')],
  screens=[('Patient app', 'Booking a test and following it to the report, without phoning anyone.', 'Healthcare/app1.png', 'Patient app home with test search, quick actions and upcoming appointments, beside the doctor listing',
            ['Search and quick actions sit above the fold.', 'Upcoming appointments are on the home screen, so status needs no navigation.', 'Date and slot are one step, sized for one-handed use.']),
           ('Front desk', 'Registering a patient and managing their tests from one screen.', 'Healthcare/Frame 1000005296.png', 'Front-desk portal with patient records next to booking and test management',
            ['Patient record and booking actions share one view — no context switch.', 'A dense table, because scanning beats scrolling in an all-day tool.']),
           ('Admin', 'One place to run staff, reports, users and operations.', 'Healthcare/Frame 1000005302.png', 'Admin dashboard with control over users, reports and analytics',
            ['Overview metrics lead, so the state of the operation is read first.', 'Charts sit beside the records they summarise.']),
           ('Home collector', 'Knowing what to collect, where and in what order — in the field.', 'Healthcare/Frame 1000005307.png', 'Home collector app with assigned tasks and an optimised collection route',
            ['Each task carries its own visit details.', 'The visit order is given, not worked out by the collector.', 'Status updates flow back to the desk and admin.']),
           ('Website', 'Finding a test, booking it, and trusting the clinic.', 'Healthcare/Frame 1000005311.png', 'Clinic website with a direct path to test discovery and booking',
            ['Test discovery and booking is the primary path.', 'Same components and colours as the internal tools, so the brand holds end to end.'])],
  features=[],
  outcome_title='A unified diagnostic ecosystem.',
  outcomes=[('01', 'One connected system serving all five kinds of user.'), ('02', 'Less manual work, and fewer errors from re-entering data.'),
            ('03', 'A test patients can follow from booking to report.'), ('04', 'A design system that scales across web and mobile.')],
  stats=False, outcome_note='',
  learned=('Reducing complexity isn’t about removing information — it’s about delivering the right information, at the right time, to the right person.',
           'The hardest part was resisting the urge to draw screens before the workflow underneath them was settled.'),
),
'yoga': dict(
  short='YogaEase', kicker='Wellness · Product design',
  title='Five wellness apps, <em>folded into one</em>.',
  sub='YogaEase brings guided practice, mindfulness, recipes and a store into one routine behind a single account.',
  facts=[('Role', 'Associate UI/UX designer, with a Team Lead'), ('Timeline', '2023 · 80+ hours'), ('Platform', 'Mobile app · 40+ screens'), ('I did', 'Research · IA · UI · Prototyping')],
  hero=('Yoga/hero.jpg', 'YogaEase banner: a practitioner in a low lunge on a black-sand beach under a clear sky'),
  glance=[('Problem', 'Practice, meditation, recipes and shopping lived in five separate apps.'),
          ('Users', 'Yoga enthusiasts, from first-timers to regular practitioners.'),
          ('Solution', 'One app with five connected areas and a single wellness dashboard.'),
          ('Outcome', '40+ screens delivered to handoff in about 80 hours.')],
  problem='Eight user interviews surfaced the same four pain points again and again.',
  pains=['Not enough time', 'No sense of progress', 'Practice and nutrition lived apart', 'Hard to start as a beginner'],
  process=[('Discover', 'Client goals, idea validation and eight user interviews.'),
           ('Structure', 'Affinity mapping, a persona, and one site map across mindfulness, yoga, home, shop and recipes.'),
           ('Design', 'Wireframes into 40+ final screens on a calm, consistent design system.'),
           ('Deliver', 'Prototyping, review and handoff.')],
  insights=[('People practise for very different reasons — fitness, calm, flexibility.', 'A wellness dashboard that tracks yoga, sleep, mood, water and steps together, so the app flexes to each goal.'),
            ('Discovery is hard: users want a curated selection, not a bigger catalogue.', 'A beginner path — graded series and a curated library — so a first session is easy to find.'),
            ('Nutrition belongs next to practice; community and mindfulness keep people coming back.', 'Recipes sit in the tab bar beside the practice, not buried in a submenu.')],
  screens=[('Overview', 'Welcome, recipes and the session library.', 'Yoga/final-trio.jpg', 'Three YogaEase screens: the welcome screen, a recipe feed and a session library',
            ['Five areas behind one account.', 'One calm visual system across all of them.']),
           ('Home dashboard', 'Progress you can see at a glance.', 'Yoga/home-screen.jpg', 'Home screen annotated with its three parts, beside the tracker list and water-consumption detail',
            ['Yoga, sleep, mood, water and steps tracked in one place.', 'Short on-demand sessions next to the live timetable.']),
           ('First run', 'Showing the value before asking for an account.', 'Yoga/onboarding.jpg', 'Onboarding: four intro screens, create-account and log-in forms, and the verification screen',
            ['Four intro screens show what the app offers first.', 'Then social sign-in and a verification code.']),
           ('Feed & workshops', 'A personalised home feed and upcoming workshops.', 'Yoga/overview-phones.jpg', 'Upcoming workshops list and the personalised home feed with a mood check-in',
            ['A mood check-in personalises the feed.', 'Live workshops sit beside on-demand content.'])],
  features=[],
  outcome_title='Five products, one wellness routine.',
  outcomes=[('40+', 'Screens designed across the full journey.'), ('80+', 'Hours from first interview to handoff.'),
            ('8', 'Users interviewed in qualitative research.'), ('5', 'Connected product areas under one IA.')],
  stats=True, outcome_note='Delivered to handoff — no post-launch analytics were collected, and none are claimed.',
  learned=('What was five apps to juggle ended as one flow behind a single account.',
           'I worked under the guidance of an experienced Team Lead to bring the app to life.'),
),
'malta_taxi': dict(
  short='Malta Taxi', kicker='Mobility · Product design',
  title='Booking a ride in a place <em>you don’t know</em>.',
  sub='A taxi app for Malta, where most riders are tourists: the fare before you commit, the car on a live map, and a flow short enough to finish on the kerb.',
  facts=[('Role', 'UI/UX designer'), ('Timeline', 'Jan – Jul 2024'), ('Platform', 'iOS & Android'), ('Deliverable', 'Mobile app design')],
  hero=('MaltaTaxi/malta-devices.png', 'Two iPhones showing the Malta Taxi onboarding screen and the location permission screen'),
  glance=[('Problem', 'Tourists couldn’t book a reliable taxi quickly — no clear price and no tracking.'),
          ('Users', 'Riders in Malta, most of them first-time visitors.'),
          ('Solution', 'One booking sequence: location, live map, fare-first booking and tours.'),
          ('Outcome', 'A complete iOS and Android app design, from onboarding to tour exploration.')],
  problem='No clear pricing, no real-time tracking and a slow booking flow aren’t three separate complaints. Together they make one broken first ride — so the fix had to be one sequence, not three features bolted on.',
  pains=['No clear pricing', 'No real-time tracking', 'A slow booking flow'],
  process=[('Rider needs', 'Five needs from the brief that every screen was held against: quick booking, clear pricing, tracking, easy navigation and guidance.'),
           ('Sequence', 'The journey ordered by when a rider meets each doubt, not listed by feature.'),
           ('Design', 'Onboarding, live map, destination search and booking, and tour exploration.'),
           ('Deliver', 'A mobile app design for iOS and Android.')],
  insights=[('Not knowing the price is what makes the wait feel risky.', 'The fare is shown while the ride is still cancellable, not after. Trust is decided in that gap.'),
            ('Not seeing the car makes the price feel like a gamble.', 'A live map of nearby taxis, so the wait is something you can watch rather than endure.'),
            ('Tourists can’t spell the street they want.', 'Destination search built for unfamiliar places, treating the tourist case as the default.')],
  screens=[('Onboarding & location', 'Two screens that make the app useful the moment onboarding ends.', 'MaltaTaxi/malta-devices.png', 'Malta Taxi onboarding screen and the location permission screen',
            ['Onboarding states the promise and offers one action.', 'Location is asked for once, with the reason attached — not as a bare system prompt.'])],
  features=[('Quick onboarding', 'Location set up front, so no later screen stops to ask.'), ('Live map', 'Nearby taxis answer “is one actually coming?”.'),
            ('Fare-first booking', 'Search and a confirmation that shows the price while cancelling is free.'), ('Tour exploration', 'Places to go for travellers, not just a field to fill.')],
  outcome_title='A complete booking app for iOS and Android.',
  outcomes=[('01', 'Onboarding and location setup that makes the first screen useful.'), ('02', 'A live map of nearby taxis, so the wait can be watched.'),
            ('03', 'Destination search and booking with the fare shown before confirming.'), ('04', 'Tour exploration for travellers.')],
  stats=False, outcome_note='', learned=None,
),
'banking': dict(
  short='QIIB banking', kicker='Fintech · Product design',
  title='Banking onboarding in <em>three screens</em>.',
  sub='A skippable three-screen onboarding into QIIB’s mobile banking app, opening onto accounts, partner services, an ATM locator and a live currency converter.',
  facts=[('Client', 'QIIB · via Sundew Solutions'), ('Timeline', 'Nov 2025'), ('Platform', 'Mobile app'), ('I did', 'Research · UX/UI · Design system')],
  hero=('MobileBanking/qiib-devices.png', 'Two iPhones showing the QIIB currency converter with a live USD to QAR rate, and the home screen'),
  glance=[('Problem', 'QIIB needed its mobile banking redefined for speed, security and simplicity.'),
          ('Users', 'QIIB customers in Qatar — new ones, and existing ones reinstalling the app.'),
          ('Solution', 'A three-step onboarding with a way out at every step, into four destinations.'),
          ('Outcome', 'Onboarding, home and a live converter, built on one shared design system.')],
  problem='Qatar International Islamic Bank needed its mobile banking app redefined for speed, security and simplicity — delivered at Sundew Solutions.',
  pains=[],
  process=[('Research', 'Discovery, benchmarking and user flows.'),
           ('Design', 'Wireframes, a design system and the final UI.'),
           ('Deliver', 'Prototyping and handoff.')],
  insights=[('An existing customer reinstalling the app shouldn’t have to read an introduction to it.', 'The first screen names the bank and the country, asks for nothing, and offers Skip immediately.'),
            ('People should see where the app will take them before they arrive.', 'The second screen introduces accounts, the ATM locator and partner services — three of the four tabs they land on. Skip becomes Back.'),
            ('Onboarding should end on doing, not seeing.', 'The last screen is about sending, paying and completing — the closest of the three to the home screen that follows.')],
  screens=[('Home & converter', 'The two screens a customer lands on after onboarding.', 'MobileBanking/qiib-devices.png', 'QIIB currency converter and home screen side by side',
            ['Home leads with balance and card, then Request and Transfer.', 'Credits and debits differ by arrow direction as well as sign.', 'A live USD–QAR rate with trend and last-updated time.']),
           ('Home in use', 'The home screen in a customer’s hand.', 'Banking/bankingOnboarding.png', 'The QIIB app home screen held in a hand',
            ['Balance, card and recent transactions on one screen.', 'Four destinations in the tab bar: Home, Partners, Locate, Converter.'])],
  features=[],
  outcome_title='What shipped.',
  outcomes=[('01', 'A three-screen onboarding with Skip or Back at every step.'), ('02', 'Four destinations behind it: Home, Partners, Locate and Converter.'),
            ('03', 'A live currency converter with rate trend and last-updated time.'), ('04', 'All of it designed on one shared design system.')],
  stats=False, outcome_note='', learned=None,
),
}

# ----------------------------------------------------------------------------- helpers
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
BACK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 8H3M7 4L3 8l4 4"/></svg>'
LIST = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M3 4h10M3 8h10M3 12h6"/></svg>'
X = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"/></svg>'
L = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>'
R = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>'
FLIP = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 8a5.5 5.5 0 0 1 9.4-3.9M13.5 8a5.5 5.5 0 0 1-9.4 3.9M12 1.8v2.6H9.4M4 14.2v-2.6h2.6"/></svg>'
SECTIONS = [('glance', 'At a glance'), ('problem', 'The problem'), ('process', 'Process'), ('insights', 'Insights → decisions'), ('solution', 'The solution'), ('outcome', 'Outcome')]

def img_size(rel):
    from PIL import Image
    with Image.open(os.path.join(SITE, 'public', rel)) as im: return im.size

def picture(rel, alt, cls='', lazy=True, eager=False):
    w, h = img_size(rel); src = '../public/' + quote(rel)
    webp = os.path.splitext(rel)[0] + '.webp'
    load = '' if eager else ' loading="lazy"'
    pr = ' fetchpriority="high"' if eager else ''
    tag = f'<img{" class=" + chr(34) + cls + chr(34) if cls else ""} src="{src}" alt="{html.escape(alt)}" width="{w}" height="{h}"{load}{pr} decoding="async">'
    if os.path.exists(os.path.join(SITE, 'public', webp)):
        return f'<picture><source srcset="../public/{quote(webp)}" type="image/webp">{tag}</picture>'
    return tag

def label(i, name): return f'<p class="cs-sec-label">{i:02d} — {name}</p>'

def render(key):
    c = CONTENT[key]; i = ORDER.index(key); nxt = ORDER[(i + 1) % len(ORDER)]; n = CONTENT[nxt]
    plain_title = re.sub('<[^>]+>', '', c['title'])
    # hero
    if c['hero'] == 'stack':
        hero = ('<figure class="cs-hero-figure cs-reveal"><div class="stack" role="img" aria-label="The healthcare product suite: the bookings dashboard in a browser, with the patient app on a phone in front">'
                '<div class="browser"><div class="bar"><i></i><i></i><i></i><span>clinic.dashboard / bookings</span></div>'
                f'{picture("Healthcare/banner/dash.png", "", eager=True)}</div>'
                f'{picture("Healthcare/banner/phone-app.png", "", cls="float")}</div></figure>')
    else:
        hero = f'<figure class="cs-hero-figure cs-reveal">{picture(c["hero"][0], c["hero"][1], eager=True)}</figure>'
    facts = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in c['facts'])
    glance = ''.join(f'<div><dt><i>{j+1}</i>{k}</dt><dd>{v}</dd></div>' for j, (k, v) in enumerate(c['glance']))
    pains = ('<ul class="pains">' + ''.join(f'<li><b>{j+1:02d}</b>{p}</li>' for j, p in enumerate(c['pains'])) + '</ul>') if c['pains'] else ''
    steps = c['process']
    step_tabs = ''.join(f'<button role="tab" id="st-{j}" aria-controls="sp-{j}" aria-selected="{"true" if j == 0 else "false"}"{"" if j == 0 else " tabindex=" + chr(34) + "-1" + chr(34)}><i>STEP {j+1:02d}</i><b>{t}</b></button>' for j, (t, _) in enumerate(steps))
    step_panels = ''.join(f'<p class="step-panel" role="tabpanel" id="sp-{j}" aria-labelledby="st-{j}"{"" if j == 0 else " hidden"}>{d}</p>' for j, (_, d) in enumerate(steps))
    flips = ''.join(f'''<div class="flip"><button class="flip-btn" type="button" aria-expanded="false">
        <span class="face front"><small>Insight {j+1:02d}</small><p>{a}</p><em>What I designed {ARROW}</em></span>
        <span class="face back"><small>Design decision</small><p>{b}</p><em>{FLIP} Back to the insight</em></span></button></div>''' for j, (a, b) in enumerate(c['insights']))
    scr = c['screens']
    g_tabs = ''.join(f'<button role="tab" id="gt-{j}" aria-controls="gp-{j}" aria-selected="{"true" if j == 0 else "false"}"{"" if j == 0 else " tabindex=" + chr(34) + "-1" + chr(34)}><i>{j+1:02d}</i>{t}</button>' for j, (t, *_ ) in enumerate(scr)) if len(scr) > 1 else ''
    g_panels = ''
    for j, (t, sub, rel, alt, calls) in enumerate(scr):
        role = f' role="tabpanel" id="gp-{j}" aria-labelledby="gt-{j}"' if len(scr) > 1 else ''
        g_panels += (f'<div class="g-panel"{role}{"" if j == 0 else " hidden"}>'
                     f'<button class="zoom" type="button" data-full="../public/{quote(rel)}" aria-label="Enlarge: {html.escape(alt)}">{picture(rel, alt)}</button>'
                     f'<div><h3>{t}</h3><p class="g-sub">{sub}</p><ol class="callouts">' + ''.join(f'<li>{x}</li>' for x in calls) + '</ol></div></div>')
    gallery = (f'<div class="gallery"{" data-tabs" if len(scr) > 1 else ""}>' + (f'<div class="g-tabs" role="tablist" aria-label="Screens">{g_tabs}</div>' if g_tabs else '') + g_panels + '</div>')
    feats = (f'<ul class="features" style="--n:{len(c["features"])}">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in c['features']) + '</ul>') if c['features'] else ''
    outs = ''.join(f'<li><span>{a}</span><p>{b}</p></li>' for a, b in c['outcomes'])
    note = f'<p class="cs-outcome-note">{c["outcome_note"]}</p>' if c['outcome_note'] else ''
    learned = (f'<div class="learned cs-reveal"><p class="cs-sec-label">What I learned</p><div><blockquote>{c["learned"][0]}</blockquote>'
               f'<p>{c["learned"][1]}</p></div></div>') if c['learned'] else ''
    main = f'''<main id="main" class="cs-page">
  <header class="cs-shell cs-hero">
    <p class="cs-kicker cs-reveal">{c["kicker"]}</p>
    <h1 class="cs-hero-title cs-reveal">{c["title"].replace("<em>", '<span class="cs-em">').replace("</em>", "</span>")}</h1>
    <p class="cs-hero-sub cs-reveal">{c["sub"]}</p>
    <dl class="cs-meta cs-reveal">{facts}</dl>
    <div class="cs-hero-actions cs-reveal"><a class="btn btn-primary" href="#solution">See the screens {ARROW}</a><span class="read">{{READ}} min read</span></div>
    {hero}
  </header>

  <section class="cs-sec cs-shell" id="glance" aria-labelledby="h-glance">
    <div class="cs-reveal">{label(1, "At a glance")}<h2 class="cs-h2" id="h-glance">The project in thirty seconds.</h2></div>
    <dl class="glance cs-reveal">{glance}</dl>
  </section>

  <section class="cs-sec cs-shell" id="problem" aria-labelledby="h-problem">
    <div class="cs-reveal">{label(2, "The problem")}<h2 class="cs-h2" id="h-problem">What was getting in the way.</h2><p class="intro-p">{c["problem"]}</p></div>
    <div class="cs-reveal">{pains}</div>
  </section>

  <section class="cs-sec cs-shell" id="process" aria-labelledby="h-process">
    <div class="cs-reveal">{label(3, "Process")}<h2 class="cs-h2" id="h-process">How the work ran.</h2></div>
    <div class="stepper cs-reveal" data-tabs style="--n:{len(steps)}">
      <div class="step-tabs" role="tablist" aria-label="Process steps">{step_tabs}</div>
      <div class="step-meter" aria-hidden="true"><span></span></div>
      {step_panels}
    </div>
  </section>

  <section class="cs-sec cs-shell" id="insights" aria-labelledby="h-insights">
    <div class="cs-reveal">{label(4, "Insights → decisions")}<h2 class="cs-h2" id="h-insights">What I learned, and what it changed.</h2></div>
    <div class="flips cs-reveal">{flips}</div>
    <p class="flip-hint cs-reveal">Tap a card to see the design decision.</p>
  </section>

  <section class="cs-sec cs-shell" id="solution" aria-labelledby="h-solution">
    <div class="cs-reveal">{label(5, "The solution")}<h2 class="cs-h2" id="h-solution">The key screens.</h2></div>
    <div class="cs-reveal">{gallery}</div>
    <div class="cs-reveal">{feats}</div>
  </section>

  <section class="cs-sec cs-shell" id="outcome" aria-labelledby="h-outcome">
    <div class="cs-outcome cs-reveal">{label(6, "Outcome")}<h2 id="h-outcome">{c["outcome_title"]}</h2>
      <ol class="cs-outcome-list{" is-stats" if c["stats"] else ""}">{outs}</ol>{note}</div>
    {learned}
    <a class="next cs-reveal" href="{nxt}_case_study.html">
      <div><small>Next case study</small><b>{n["title"].replace("<em>", "").replace("</em>", "")}</b><span class="go">Read {n["short"]} {ARROW}</span></div>
      <img src="../assets/og-{nxt}.jpg" alt="" width="1200" height="630" loading="lazy">
    </a>
  </section>
</main>'''
    words = len(html.unescape(re.sub(r'<[^>]+>', ' ', main)).split())
    main = main.replace('{READ}', str(max(1, round(words / 200))))
    toc = '\n'.join(f'<a href="#{sid}"><i>{j+1:02d}</i>{name}</a>' for j, (sid, name) in enumerate(SECTIONS))
    desc = re.sub('<[^>]+>', '', c['sub'])
    url = f'{BASE}case-studies/{key}_case_study.html'
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{c["short"]} · Case study · Rakhi Das</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%2310141B'/%3E%3Ctext x='32' y='45' font-family='Georgia,serif' font-size='40' fill='%23fff' text-anchor='middle'%3ER%3C/text%3E%3C/svg%3E">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{url}">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Rakhi Das">
<meta property="og:title" content="{html.escape(plain_title)} — {c["short"]} case study">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/og-{key}.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="case.css">
<script>try{{var t=localStorage.getItem('rk-theme');var h=new Date().getHours();document.documentElement.dataset.theme=t||(h>=6&&h<18?'light':'dark')}}catch(e){{}}document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<span class="progress" aria-hidden="true"></span>

<aside class="side" id="side" aria-label="Case study sections">
  <a class="home" href="../index.html#work">{BACK} Home</a>
  <p class="side-title">{c["short"]}</p>
  <p class="side-sub">{c["kicker"]}</p>
  <nav class="toc">
{toc}
  </nav>
  <div class="side-foot">
    <a href="{nxt}_case_study.html">Next: {n["short"]} →</a>
    <a href="mailto:dasrakhi303@gmail.com">dasrakhi303@gmail.com</a>
  </div>
</aside>
<div class="scrim" aria-hidden="true"></div>

<div class="mnav glass" role="region" aria-label="Page navigation"><a href="../index.html#work">{BACK} Home</a><button type="button" id="tocBtn" aria-expanded="false" aria-controls="side">{LIST} Sections</button></div>
<div class="topbar" role="region" aria-label="Display settings"><div class="dn-wrap glass"><button class="dn" id="dn" role="switch" aria-checked="true" aria-label="Day. Switch to night"><span class="stars"></span><span class="knob"></span></button></div></div>

{main}

<dialog class="lightbox" id="lightbox" aria-label="Enlarged screen">
  <img src="" alt="">
  <p></p>
  <button class="lb-btn lb-close" type="button" aria-label="Close">{X}</button>
  <button class="lb-btn lb-prev" type="button" aria-label="Previous screen">{L}</button>
  <button class="lb-btn lb-next" type="button" aria-label="Next screen">{R}</button>
</dialog>

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
    with open(os.path.join(OUT, f'{key}_case_study.html'), 'w', encoding='utf-8') as f: f.write(page)
    return words

if __name__ == '__main__':
    for k in ORDER: print(f'{k}: {render(k)} words')

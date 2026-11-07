const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const font='@font-face{font-family:D;src:url(file:///home/user/testng/channel/brand/noto-serif-devanagari-devanagari-700-normal.woff2);font-weight:700}@font-face{font-family:B;src:url(file:///home/user/testng/channel/brand/noto-serif-bengali-bengali-700-normal.woff2);font-weight:700}';
const p=await b.newPage({viewport:{width:800,height:800}});
await p.setContent(`<meta charset=utf-8><style>${font}body{margin:0}</style><svg width="800" height="800" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="g" cx=".5" cy=".38" r=".78"><stop offset="0" stop-color="#e8774a"/><stop offset=".45" stop-color="#a23f6e"/><stop offset="1" stop-color="#1f1245"/></radialGradient>
<radialGradient id="h"><stop offset="0" stop-color="#ffe9b8" stop-opacity=".7"/><stop offset="1" stop-color="#ffe9b8" stop-opacity="0"/></radialGradient>
<linearGradient id="k" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset="1" stop-color="#c98a2b"/></linearGradient></defs>
<rect width="800" height="800" fill="url(#g)"/><circle cx="400" cy="400" r="335" fill="none" stroke="#f6c66a" stroke-width="12"/>
<circle cx="400" cy="300" r="190" fill="url(#h)"/>
<g fill="#ffe9b8" opacity=".95"><path d="M400 120 q-28 55 0 105 q28 -50 0 -105z"/><path d="M360 135 q-22 45 10 90 q10 -45 -10 -90z" opacity=".8"/><path d="M440 135 q22 45 -10 90 q-10 -45 10 -90z" opacity=".8"/></g>
<g fill="url(#k)"><path d="M300 270 h200 q10 0 8 12 l-8 30 q70 50 66 130 q-8 100 -166 100 q-158 0 -166 -100 q-4 -80 66 -130 l-8 -30 q-2 -12 8 -12z" transform="translate(0,-10)"/>
<ellipse cx="400" cy="262" rx="108" ry="16"/><rect x="340" y="510" width="120" height="28" rx="12"/><rect x="310" y="535" width="180" height="22" rx="10"/></g>
<path d="M330 330 q70 -30 140 0" stroke="#7a3f1a" stroke-width="6" fill="none" opacity=".5"/>
<text x="400" y="640" text-anchor="middle" font-family="D" font-weight="700" font-size="82" fill="#fff1cf">अमृत कथा</text>
<text x="400" y="705" text-anchor="middle" font-family="B" font-weight="700" font-size="50" fill="#f6c66a">অমৃত কথা</text></svg>`);
await p.waitForTimeout(700);await p.screenshot({path:'logo_amrit.png'});await b.close()})()

const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:2560,height:1440}});
const pot=`<svg width="300" height="420" viewBox="260 100 280 480" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="k" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset="1" stop-color="#d49a35"/></linearGradient></defs>
<g fill="#ffe9b8"><path d="M400 120 q-28 55 0 105 q28 -50 0 -105z"/><path d="M360 135 q-22 45 10 90 q10 -45 -10 -90z" opacity=".85"/><path d="M440 135 q22 45 -10 90 q-10 -45 10 -90z" opacity=".85"/></g>
<g fill="url(#k)"><path d="M300 270 h200 q10 0 8 12 l-8 30 q70 50 66 130 q-8 100 -166 100 q-158 0 -166 -100 q-4 -80 66 -130 l-8 -30 q-2 -12 8 -12z" transform="translate(0,-10)"/><ellipse cx="400" cy="262" rx="108" ry="16"/><rect x="340" y="510" width="120" height="28" rx="12"/><rect x="310" y="535" width="180" height="22" rx="10"/></g></svg>`;
await p.setContent(`<meta charset=utf-8><style>
@font-face{font-family:D;src:url(file:///home/user/testng/channel/brand/noto-serif-devanagari-devanagari-700-normal.woff2);font-weight:700}
@font-face{font-family:B;src:url(file:///home/user/testng/channel/brand/noto-serif-bengali-bengali-700-normal.woff2);font-weight:700}
body{margin:0;width:2560px;height:1440px;position:relative;overflow:hidden;background:linear-gradient(#1f1245 0%,#4a2468 38%,#a23f6e 68%,#e8774a 100%)}
.glow{position:absolute;left:480px;top:300px;width:1600px;height:900px;background:radial-gradient(ellipse,#ffe9b844,transparent 65%)}
.m{position:absolute;left:0;bottom:0;width:100%;height:300px;background:#150b30;clip-path:polygon(0 55%,10% 25%,22% 50%,36% 10%,50% 45%,64% 5%,78% 40%,90% 15%,100% 50%,100% 100%,0 100%)}
.m2{position:absolute;left:0;bottom:0;width:100%;height:190px;background:#0e0722;clip-path:polygon(0 60%,18% 30%,34% 55%,52% 20%,70% 55%,86% 25%,100% 55%,100% 100%,0 100%)}
.wrap{position:absolute;left:507px;top:508px;width:1546px;height:423px;display:flex;align-items:center;justify-content:center;gap:60px}
.pot{flex:none;height:423px;display:flex;align-items:center}
.tx{display:flex;flex-direction:column;justify-content:center;font-weight:700}
.h{font-family:D;font-size:190px;color:#fff1cf;line-height:1.05;text-shadow:0 6px 30px #0009}
.bn{font-family:B;font-size:84px;color:#f6c66a;line-height:1.1}
.en{font-family:Georgia,serif;font-size:50px;color:#ffe9b8;letter-spacing:6px;margin-top:14px;font-weight:400;opacity:.95}
.st{position:absolute;border-radius:50%;background:#ffe9b8}
</style><div class=glow></div>
<div class=st style="left:300px;top:200px;width:6px;height:6px"></div><div class=st style="left:2200px;top:260px;width:8px;height:8px"></div><div class=st style="left:1700px;top:140px;width:5px;height:5px"></div><div class=st style="left:900px;top:120px;width:6px;height:6px"></div><div class=st style="left:2350px;top:520px;width:5px;height:5px"></div><div class=st style="left:180px;top:560px;width:7px;height:7px"></div>
<div class=m></div><div class=m2></div>
<div class=wrap><div class=pot>${pot}</div><div class=tx><div class=h>अमृत कथा</div><div class=bn>অমৃত কথা</div><div class=en>SHIVA · RAMAYANA · VEDAS</div></div></div>`);
await p.waitForTimeout(800);await p.screenshot({path:'banner_amrit.png'});await b.close()})()

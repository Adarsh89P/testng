const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const font='@font-face{font-family:D;src:url(file:///home/user/testng/channel/brand/noto-serif-devanagari-devanagari-700-normal.woff2);font-weight:700}';
const p=await b.newPage({viewport:{width:800,height:800}});
await p.setContent(`<meta charset=utf-8><style>${font}body{margin:0}</style><svg width="800" height="800" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="g" cx=".5" cy=".42" r=".75"><stop offset="0" stop-color="#e8774a"/><stop offset=".45" stop-color="#a23f6e"/><stop offset="1" stop-color="#1f1245"/></radialGradient>
<radialGradient id="h"><stop offset="0" stop-color="#ffe9b8" stop-opacity=".55"/><stop offset="1" stop-color="#ffe9b8" stop-opacity="0"/></radialGradient></defs>
<rect width="800" height="800" fill="url(#g)"/><circle cx="400" cy="400" r="330" fill="none" stroke="#f6c66a" stroke-width="12"/>
<circle cx="400" cy="400" r="290" fill="none" stroke="#f6c66a" stroke-width="3" opacity=".6"/>
<circle cx="400" cy="390" r="230" fill="url(#h)"/>
<text x="400" y="500" text-anchor="middle" font-family="D" font-weight="700" font-size="360" fill="#fff1cf">ॐ</text>
<path d="M330 640 q70 50 140 0" stroke="#f6c66a" stroke-width="10" fill="none" opacity=".8"/></svg>`);
await p.waitForTimeout(600);await p.screenshot({path:'logo_common.png'});
await p.setViewportSize({width:2560,height:1440});
await p.setContent(`<meta charset=utf-8><style>${font}body{margin:0;width:2560px;height:1440px;background:linear-gradient(#2a1658,#a23f6e 60%,#e8774a);font-family:D;position:relative;overflow:hidden}
.t{position:absolute;width:100%;text-align:center;top:500px;color:#ffe9b8;font-size:230px;text-shadow:0 6px 30px #000a}.s{position:absolute;width:100%;text-align:center;top:800px;color:#f6c66a;font-size:78px}
.m{position:absolute;left:0;bottom:0;width:100%;height:260px;background:#1a0f3a;clip-path:polygon(0 60%,15% 20%,30% 55%,50% 0,70% 50%,85% 15%,100% 55%,100% 100%,0 100%)}</style>
<div class=t>सनातन गाथा</div><div class=s>शिव · राम · वेद — सनातन की कथाएँ</div><div class=m></div>`);
await p.waitForTimeout(600);await p.screenshot({path:'banner_common.png'});await b.close()})()

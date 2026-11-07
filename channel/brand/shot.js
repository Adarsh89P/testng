const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:800,height:800}});
await p.goto('file://'+process.cwd()+'/brand.html');await p.waitForTimeout(500);await p.screenshot({path:'logo.png'});
await p.setViewportSize({width:2560,height:1440});
await p.setContent(`<meta charset=utf-8><style>@font-face{font-family:D;src:url(file://${process.cwd()}/noto-serif-devanagari-devanagari-700-normal.woff2)}body{margin:0;width:2560px;height:1440px;background:linear-gradient(#2a1658,#a23f6e 60%,#e8774a);font-family:D;position:relative;overflow:hidden}
.t{position:absolute;left:0;width:100%;text-align:center;top:520px;color:#ffe9b8;font-size:230px;text-shadow:0 6px 30px #000a}.s{position:absolute;width:100%;text-align:center;top:800px;color:#f6c66a;font-size:78px}
.m{position:absolute;left:0;bottom:0;width:100%;height:260px;background:#1a0f3a;clip-path:polygon(0 60%,15% 20%,30% 55%,50% 0,70% 50%,85% 15%,100% 55%,100% 100%,0 100%)}</style>
<div class=t>पुराण छाया</div><div class=s>शिव के 108 नाम · हर नाम, एक कथा</div><div class=m></div>`);
await p.waitForTimeout(500);await p.screenshot({path:'banner.png'});await b.close()})()

const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const html=(s)=>`<meta charset=utf-8><style>@font-face{font-family:D;src:url(file:///home/user/testng/channel/brand/noto-serif-devanagari-devanagari-700-normal.woff2);font-weight:700}
html,body{margin:0;background:transparent}div{width:${s}px;height:${s}px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:D;font-weight:700;line-height:1.05;color:#ffe9b8;text-shadow:0 0 ${s*.03}px #1a0f3a,0 ${s*.012}px ${s*.04}px #1a0f3a,0 0 ${s*.08}px #1a0f3acc}
span{font-size:${s*.40}px}span+span{color:#f6c66a}</style><div><span>अमृत</span><span>कथा</span></div>`;
for(const s of [300,150]){const p=await b.newPage({viewport:{width:s,height:s}});await p.setContent(html(s));await p.waitForTimeout(500);await p.screenshot({path:'watermark_text_'+s+'.png',omitBackground:true});}
await b.close()})()

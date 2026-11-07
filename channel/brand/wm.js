const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const svg=`<svg width="300" height="300" viewBox="260 100 280 480" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="k" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset="1" stop-color="#d49a35"/></linearGradient><filter id="s"><feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#1a0f3a" flood-opacity=".85"/></filter></defs>
<g filter="url(#s)"><g fill="#ffe9b8"><path d="M400 120 q-28 55 0 105 q28 -50 0 -105z"/><path d="M360 135 q-22 45 10 90 q10 -45 -10 -90z" opacity=".85"/><path d="M440 135 q22 45 -10 90 q-10 -45 10 -90z" opacity=".85"/></g>
<g fill="url(#k)"><path d="M300 270 h200 q10 0 8 12 l-8 30 q70 50 66 130 q-8 100 -166 100 q-158 0 -166 -100 q-4 -80 66 -130 l-8 -30 q-2 -12 8 -12z" transform="translate(0,-10)"/><ellipse cx="400" cy="262" rx="108" ry="16"/><rect x="340" y="510" width="120" height="28" rx="12"/><rect x="310" y="535" width="180" height="22" rx="10"/></g></g></svg>`;
const p=await b.newPage({viewport:{width:300,height:300}});
await p.setContent('<body style="margin:0;background:transparent">'+svg);
await p.screenshot({path:'watermark_300.png',omitBackground:true});
await p.setViewportSize({width:150,height:150});await p.setContent('<body style="margin:0;background:transparent">'+svg.replace(/300/g,'150'));
await p.screenshot({path:'watermark_150.png',omitBackground:true});
await p.setViewportSize({width:700,height:260});
await p.setContent('<body style="margin:0;display:flex"><div style="background:#fff;width:350px;height:260px;display:flex;align-items:center;justify-content:center"><img src="file://'+process.cwd()+'/watermark_150.png"></div><div style="background:#a23f6e;width:350px;height:260px;display:flex;align-items:center;justify-content:center"><img src="file://'+process.cwd()+'/watermark_150.png"></div>');
await p.waitForTimeout(300);await p.screenshot({path:'/tmp/wm_test.png'});await b.close()})()

const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:800,height:800}});
await p.goto('file://'+process.cwd()+'/logo.html');await p.screenshot({path:'logo.png'});await b.close()})()

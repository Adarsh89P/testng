const {chromium}=require('playwright');const fs=require('fs'),cp=require('child_process');
const [,, name, srt, src, out]=process.argv;
const T=t=>{const m=t.match(/(\d+):(\d+):(\d+),(\d+)/);return +m[1]*3600+ +m[2]*60+ +m[3]+ +m[4]/1000};
const cues=fs.readFileSync(srt,'utf8').trim().split(/\n\s*\n/).map(b=>{const l=b.split('\n');const [a,c]=l[1].split(' --> ');return {a:T(a),b:T(c),t:l.slice(2).join(' ')}});
const topname=(cues[0].t.match(/:\s*(.+?)[,।.]?$/)||[])[1]||name;
const font='@font-face{font-family:D;src:url(file:///home/user/testng/shorts/noto-serif-devanagari-devanagari-700-normal.woff2);font-weight:700}';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:360}});
fs.mkdirSync('/tmp/cap_'+name,{recursive:true});
for(let i=0;i<cues.length;i++){await p.setContent(`<meta charset=utf-8><style>${font}body{margin:0;background:transparent;width:1000px;height:360px;display:flex;align-items:center;justify-content:center}
div{font-family:D;font-weight:700;font-size:62px;line-height:1.35;color:#fff;text-align:center;padding:22px 36px;background:#1a0f3acc;border-radius:28px;max-width:940px;text-shadow:0 2px 8px #000a}</style><div>${cues[i].t}</div>`);
await p.waitForTimeout(150);await p.screenshot({path:'/tmp/cap_'+name+'/c'+i+'.png',omitBackground:true})}
const q=await b.newPage({viewport:{width:1080,height:330}});
await q.setContent(`<meta charset=utf-8><style>${font}body{margin:0;background:transparent;width:1080px;height:330px;font-family:D;font-weight:700;text-align:center;text-shadow:0 4px 20px #000a}
.a{font-size:50px;color:#f6c66a;padding-top:60px}.b{font-size:130px;color:#fff1cf;line-height:1.15}</style><div class=a>शिव के 108 नामों में से</div><div class=b>${topname}</div>`);
await q.waitForTimeout(200);await q.screenshot({path:'/tmp/cap_'+name+'/top.png',omitBackground:true});await b.close();
let inp='-i '+src+' -i /tmp/cap_'+name+'/top.png',fc='[0:v]split[a][f];[a]scale=-2:1920,crop=1080:1920,boxblur=40:6,eq=brightness=-0.18[bg];[f]crop=1920:880:0:0,scale=1080:-2[fg];[bg][fg]overlay=0:580[v0];[v0][1:v]overlay=0:150[v1]';
let last='v1';cues.forEach((c,i)=>{inp+=' -i /tmp/cap_'+name+'/c'+i+'.png';fc+=`;[${last}][${i+2}:v]overlay=40:1160:enable='between(t,${c.a},${c.b})'[o${i}]`;last='o'+i});
const cmd=`ffmpeg -y -loglevel error ${inp} -filter_complex "${fc}" -map "[${last}]" -map 0:a -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p -r 24 -c:a copy -movflags +faststart ${out}`;
fs.writeFileSync('/tmp/cmd_'+name+'.sh',cmd);console.log(cues.length,'cues; top =',topname)})()

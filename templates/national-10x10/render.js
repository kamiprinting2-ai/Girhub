// node templates/national-10x10/render.js : 106mm (10x10 cm + 3mm bleed) PDF + 600 dpi PNGs (with bleed, and trimmed 10x10)
const {chromium}=require('playwright');const path=require('path');
(async()=>{const d=__dirname,src='file://'+path.join(d,'design.html');const b=await chromium.launch();
 const p=await b.newPage();await p.goto(src,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 await p.pdf({path:path.join(d,'اليوم-الوطني-10x10-مع-نزيف-106مم.pdf'),width:'106mm',height:'106mm',printBackground:true});
 const W=Math.round(106/25.4*96);const q=await b.newPage({viewport:{width:W,height:W},deviceScaleFactor:600/96});
 await q.goto(src,{waitUntil:'networkidle'});await q.evaluate(()=>document.fonts.ready);await q.waitForTimeout(500);
 await q.screenshot({path:path.join(d,'full.png'),clip:{x:0,y:0,width:W,height:W}});await b.close();})();

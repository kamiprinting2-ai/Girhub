// node brand/colors/reds/render_reds.js : A4 PDF + 300 dpi PNG of the red shades chart
const {chromium}=require('playwright');const path=require('path');
(async()=>{const d=__dirname,src='file://'+path.join(d,'reds.html');const b=await chromium.launch();
 const p=await b.newPage();await p.goto(src);await p.waitForTimeout(2500);
 await p.pdf({path:path.join(d,'درجات-الأحمر-A4.pdf'),width:'210mm',height:'297mm',printBackground:true});
 const W=Math.round(210/25.4*96),H=Math.round(297/25.4*96);
 const q=await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:300/96});await q.goto(src);await q.waitForTimeout(2500);
 await q.screenshot({path:path.join(d,'درجات-الأحمر.png'),clip:{x:0,y:0,width:W,height:H}});await b.close();})();

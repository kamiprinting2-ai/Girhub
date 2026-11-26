// Renders panels_brand_20x25.html: print PDF (200x250 mm, 3 pages) + one 300 dpi PNG per board.
// node brand/shop-boards/src/render_20x25.js  (run from repo root)
const {chromium}=require('playwright');const path=require('path');
(async()=>{
 const src=path.resolve(__dirname,'panels_brand_20x25.html');const out=path.resolve(__dirname,'..');
 const b=await chromium.launch();
 const p=await b.newPage();await p.goto('file://'+src);await p.waitForTimeout(2500);
 await p.pdf({path:out+'/لوحات-كامي-20x25.pdf',width:'200mm',height:'250mm',printBackground:true,preferCSSPageSize:true});
 const W=Math.round(200/25.4*96),H=Math.round(250/25.4*96),k=300/96;
 for(const i of [1,2,3]){const q=await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:k});
  await q.goto('file://'+src+'?p='+i);await q.waitForTimeout(2500);
  await q.screenshot({path:out+'/0'+i+'.png',clip:{x:0,y:0,width:W,height:H}});await q.close();}
 await b.close();})();

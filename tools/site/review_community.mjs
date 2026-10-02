// Review the published static routes and the new community task at phone and desktop widths.
// Network-dependent responder checks retain their own archived results; this run is explicitly offline.
import { chromium } from 'playwright-core';
import fs from 'fs';import path from 'path';import http from 'http';
const root=path.resolve(new URL('../..',import.meta.url).pathname);
const docs=path.join(root,'docs');const out=path.join(root,'research/v13/evidence/v136');
fs.mkdirSync(out,{recursive:true});
const server=http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  let file=path.join(docs,pathname.replace(/^\/esa_poster\//,''));
  if(fs.existsSync(file)&&fs.statSync(file).isDirectory()) file=path.join(file,'index.html');
  if(!file.startsWith(docs)||!fs.existsSync(file)){res.writeHead(404);res.end();return;}
  const mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json'};
  res.setHeader('content-type',mime[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}/esa_poster/`;
const browser=await chromium.launch({executablePath:process.env.PW_CHROMIUM||'/root/.cache/ms-playwright/chromium_headless_shell-1194/chrome-linux/headless_shell',args:['--no-sandbox']});
const result={checked_utc:new Date().toISOString(),scope:'Static local routes; external requests blocked. No live responder success is inferred.',routes:[],failures:[],community:{},demo:{}};
try{
 for(const width of [390,1440]){
  const ctx=await browser.newContext({viewport:{width,height:width===390?844:1000},permissions:['clipboard-read','clipboard-write']});
  const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  let external=[];
  await page.route('**/*',route=>{if(route.request().url().startsWith(base))return route.continue();external.push(route.request().url());return route.abort();});
  for(const route of ['', 'demo/', 'r/', 't/', 'test/', 'methods/', 'use/', 'questions/']){
   external=[];
   const resp=await page.goto(base+route,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
   const layout=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,title:document.title,images:[...document.images].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0}))}));
   const pass=resp.status()===200&&layout.scroll<=width+1&&layout.images.every(i=>i.ok)&&errors.length===0;
   result.routes.push({route:route||'/',width,http_status:resp.status(),...layout,pass});if(!pass)result.failures.push({route,width,errors:[...errors],layout});
   if(route==='demo/'){
    await page.waitForFunction(()=>window.__TOUR__?.complete&&window.__RESULT__,{},{timeout:20000});
    const run=await page.evaluate(()=>({tour:window.__TOUR__,receiver:window.__RESULT__}));
    const ok=run.tour.seconds<=20&&run.tour.sequence.length===6&&run.tour.sequence[4].verdict==='REFUSED'&&run.tour.sequence[5].verdict==='ACCEPTED'&&external.length===0;
    result.demo[width]={...run,external_requests:external,pass:ok};if(!ok)result.failures.push({demo:width,...run,external});
    await page.screenshot({path:path.join(out,`demo_${width}.png`),fullPage:false});
   }
   if(route==='use/'){
    const cards=await page.locator('.setup h3').allTextContents();
    if(cards.join('|')!=='ChatGPT|Claude|Visual Studio Code|Dify|Salesforce MuleSoft')result.failures.push('Missing primary community route');
    await page.locator('#copy-handoff').click();
    const copied=await page.evaluate(()=>navigator.clipboard.readText());const prompt=await page.locator('#handoff').inputValue();
    if(copied!==prompt||!copied.includes('emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa')) result.failures.push('Clipboard did not preserve exact token');
    const urls=await page.locator('.setup a').evaluateAll(els=>els.map(e=>({text:e.textContent,url:e.href})));
    result.community[width]={cards,copy_matches:copied===prompt,links:urls};
    await page.screenshot({path:path.join(out,`community_${width}.png`),fullPage:width===390});
    await page.getByRole('link',{name:'Methods and reproduction',exact:true}).click();
    if(!(await page.locator('h1').innerText()).includes('Methods'))result.failures.push('Community-to-methods link failed');
   }
  }
  if(width===390){
   await page.emulateMedia({reducedMotion:'reduce'});
   await page.goto(base+'demo/');await page.waitForFunction(()=>window.__TOUR__?.complete);
   result.demo.reduced_motion=await page.evaluate(()=>window.__TOUR__);
   if(result.demo.reduced_motion.seconds>1)result.failures.push('Reduced-motion tour did not finish immediately');
   const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
   const np=await nojs.newPage();await np.goto(base+'demo/');
   const fallback=await np.locator('noscript').innerText();
   result.demo.no_javascript_fallback=fallback.includes('JavaScript is off')&&fallback.includes('L0 refused')&&fallback.includes('ACCEPTED, checked');
   if(!result.demo.no_javascript_fallback)result.failures.push('No-script evidence fallback missing');
   await nojs.close();
  }
  await ctx.close();
 }
}finally{await browser.close();await new Promise(r=>server.close(r));}
fs.writeFileSync(path.join(out,'site_review.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({routes:result.routes.length,passed:result.routes.filter(r=>r.pass).length,demo_seconds:[result.demo[390]?.tour.seconds,result.demo[1440]?.tour.seconds],failures:result.failures},null,2));
if(result.failures.length) process.exitCode=1;

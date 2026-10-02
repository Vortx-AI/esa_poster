// Headless phone test of docs/: serve it with python -m http.server under /esa_poster/ (as GitHub Pages will),
// open every page in Chromium at 390 x 844 (DPR 2, touch, Android UA), and assert:
//   - the demo's verdicts, in ladder words, live and offline, within 20 s; the no-JS summary;
//   - TRY A TOKEN re-hashes the real token in the browser, and refuses a wrong cell (L1) and a changed name (L0);
//   - no page issues a POST (or any non-GET) to emem.dev: every such request is aborted and fails the test;
//   - no horizontal scroll at 390 px; no page error; the six QR SVGs, rendered by Chromium, decode to their payloads.
// Screenshots go to docs/assets/screens/, results to docs/assets/screens/results.json.
//   node tools/site/test_site.mjs [docs_dir]
// Chromium: /opt/pw-browsers (playwright-core). Behind a TLS-re-terminating proxy, set HTTPS_PROXY; the proxy CA's SPKI is read from
// /root/.ccr/agent-proxy-ca.crt (or PW_SPKI=<b64,b64>) and passed as --ignore-certificate-errors-spki-list.
import { chromium } from 'playwright-core';
import fs from 'fs'; import os from 'os'; import path from 'path'; import net from 'net'; import crypto from 'crypto';
import { spawn, execFileSync } from 'child_process';

const here = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(here, '../..');
const DOCS = path.resolve(process.argv[2] || path.join(ROOT, 'docs'));
const SHOTS = path.join(DOCS, 'assets/screens'); fs.mkdirSync(SHOTS, { recursive: true });
const EXP = JSON.parse(fs.readFileSync(path.join(DOCS, 'demo/expected.json'), 'utf8'));
const QRM = JSON.parse(fs.readFileSync(path.join(ROOT, 'poster/fig/v13/qr_manifest.json'), 'utf8'));
const CHROME = process.env.PW_CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

function spkiList() {
  if (process.env.PW_SPKI) return process.env.PW_SPKI;
  const f = '/root/.ccr/agent-proxy-ca.crt'; if (!fs.existsSync(f)) return '';
  const pems = fs.readFileSync(f, 'utf8').match(/-----BEGIN CERTIFICATE-----[\s\S]+?-----END CERTIFICATE-----/g) || [];
  return pems.map((p) => crypto.createHash('sha256').update(new crypto.X509Certificate(p).publicKey.export({ type: 'spki', format: 'der' })).digest('base64')).join(',');
}
const freePort = () => new Promise((res) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });

// ---- serve docs/ at /esa_poster/
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'emem-site-')); fs.symlinkSync(DOCS, path.join(tmp, 'esa_poster'));
const port = await freePort();
const srv = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', tmp], { stdio: 'ignore' });
const BASE = `http://127.0.0.1:${port}/esa_poster/`;
for (let i = 0; i < 50; i++) { try { const r = await fetch(BASE); if (r.ok) break; } catch {} await new Promise((r) => setTimeout(r, 100)); }

const spki = spkiList();
const browser = await chromium.launch({ executablePath: CHROME, proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY, bypass: '127.0.0.1,localhost' } : undefined,
  args: spki ? ['--ignore-certificate-errors-spki-list=' + spki] : [] });
const PHONE = { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
  userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36', locale: 'en-GB', timezoneId: 'Europe/Berlin' };

const results = { started_utc: new Date().toISOString(), base: BASE, viewport: '390x844 DPR 2', pages: {}, blocked_writes: [], requests_external: [], failures: [] };
const check = (ok, what) => { if (!ok) results.failures.push(what); return ok; };

async function newPage(opts = {}) {
  const ctx = await browser.newContext({ ...PHONE, ...opts.ctx });
  const page = await ctx.newPage(); const log = []; const reqs = [];
  await page.route('**/*', async (route) => {
    const r = route.request(), u = r.url(), m = r.method();
    if (!u.startsWith('http://127.0.0.1')) reqs.push(`${m} ${u.slice(0, 140)}`);
    if (/^https?:\/\/([a-z0-9-]+\.)*emem\.dev\//.test(u) && m !== 'GET' && !(m === 'OPTIONS')) { results.blocked_writes.push(`${m} ${u} (${opts.name})`); return route.abort('blockedbyclient'); }
    if (opts.offline && !u.startsWith('http://127.0.0.1')) return route.abort('internetdisconnected');
    return route.continue();
  });
  page.on('pageerror', (e) => log.push('pageerror: ' + e.message.slice(0, 200)));
  page.on('console', (m) => { if (m.type() === 'error') log.push('console: ' + m.text().slice(0, 200)); });
  if (opts.throttle) { const cdp = await ctx.newCDPSession(page); await cdp.send('Network.enable'); await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 4e6 / 8, uploadThroughput: 1e6 / 8 }); }
  return { ctx, page, log, reqs };
}
async function layout(page) { return page.evaluate(() => ({ scrollW: document.documentElement.scrollWidth, innerW: innerWidth, title: document.title, h1: (document.querySelector('h1') || {}).textContent || '' })); }

async function simplePage(name, rel, fn) {
  const { ctx, page, log, reqs } = await newPage({ name });
  const t0 = Date.now(); const resp = await page.goto(BASE + rel, { waitUntil: 'load' }); const ms = Date.now() - t0;
  await page.waitForTimeout(400);
  const L = await layout(page); const extra = fn ? await fn(page) : {};
  await page.screenshot({ path: path.join(SHOTS, `${name}.png`) });
  results.pages[name] = { url: rel, status: resp.status(), load_ms: ms, ...L, errors: log, external_requests: reqs, ...extra };
  check(resp.status() === 200, `${name}: HTTP ${resp.status()}`); check(L.scrollW <= 390, `${name}: horizontal scroll (${L.scrollW} px)`);
  check(!log.some((l) => l.startsWith('pageerror')), `${name}: page error ${log.join('; ')}`);
  await ctx.close();
}

// ---- landing
await simplePage('landing', '', async (page) => {
  const ctas = await page.$$eval('a.cta', (as) => as.map((a) => [a.querySelector('b').textContent.replace(' →', ''), a.getAttribute('href')]));
  const want = [['VIEW THE DEMO', './demo/'], ['TRY A TOKEN', './t/'], ['INSPECT THE RECORD', './r/'], ['RE-RUN THE TEST', './test/'], ['READ THE METHODS', './methods/'], ['DISCOVER INTEGRATIONS', './use/']];
  check(JSON.stringify(ctas) === JSON.stringify(want), 'landing: the six CTAs differ: ' + JSON.stringify(ctas));
  const h1 = await page.textContent('h1'); check(h1 === 'Agents hand each other evidence references, not paraphrases.', 'landing: hero sentence');
  return { ctas };
});

// ---- the demo, live
async function demo(name, q, opts = {}) {
  const { ctx, page, log, reqs } = await newPage({ name, ...opts });
  const t0 = Date.now(); await page.goto(BASE + 'demo/' + q, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => !!window.__RESULT__, null, { timeout: 40000 }).catch(() => {});
  const wall = (Date.now() - t0) / 1000;
  const R = await page.evaluate(() => window.__RESULT__ || null);
  const board = await page.evaluate(() => { const b = document.querySelector('#board').getBoundingClientRect(); return { top: b.top, bottom: b.bottom, pills: [...document.querySelectorAll('#board .pill')].map((p) => p.innerText.replace(/\n/g, ' ')) }; });
  await page.screenshot({ path: path.join(SHOTS, `${name}.png`) });
  if (name === 'demo_live') await page.screenshot({ path: path.join(SHOTS, `${name}_full.png`), fullPage: true });
  const L = await layout(page);
  const r = { url: 'demo/' + q, wall_s: wall, page_s: R && R.seconds, board, lines: R && R.lines, l3: R && R.l3, south: R && R.south, live: R && R.live, ...L, errors: log, external_requests: reqs };
  results.pages[name] = r;
  if (!check(!!R, `${name}: demo never finished`)) { await ctx.close(); return r; }
  for (const id of ['prose', 'M3', 'M4', 'M8', 'G0']) {
    const got = R.lines.find((x) => x.id === id), want = EXP.results[id];
    check(got && got.line === want.line, `${name}: ${id} verdict "${got && got.line}" != "${want.line}"`);
  }
  check(R.lines.find((x) => x.id === 'M3').line.startsWith('L0 refused'), `${name}: M3 not refused at L0`);
  check(R.lines.find((x) => x.id === 'M4').line.startsWith('L1 refused'), `${name}: M4 not refused at L1`);
  check(R.lines.find((x) => x.id === 'M8').line.startsWith('L0 refused'), `${name}: M8 not refused at L0`);
  check(R.lines.find((x) => x.id === 'G0').line.startsWith('ACCEPTED, checked at L0, L1, L2'), `${name}: G0 not accepted`);
  check(R.south === '0.3016', `${name}: south pixel ${R.south}`);
  check(R.seconds <= 20, `${name}: took ${R.seconds} s (> 20 s)`);
  check(board.bottom <= 844, `${name}: verdict board ends at ${board.bottom} px, below the fold`);
  check(L.scrollW <= 390, `${name}: horizontal scroll (${L.scrollW} px)`);
  if (opts.offline) {
    check(/^L3 not re-read/.test(R.l3), `${name}: offline L3 line "${R.l3}"`);
    check(reqs.length === 0 || reqs.every((u) => /^GET /.test(u)), `${name}: offline made requests`);
  } else {
    check(/^L3 re-read/.test(R.l3), `${name}: L3 "${R.l3}"`);
    check(R.live.facts && R.live.facts.genuine === 200 && R.live.facts.same === true && R.live.facts.forged === 404, `${name}: live facts ${JSON.stringify(R.live.facts)}`);
    check(R.live.src && R.live.src.B08 === 3502 && R.live.src.B04 === 1900 && R.live.src.b3.every(Boolean), `${name}: live source ${JSON.stringify(R.live.src)}`);
  }
  await ctx.close(); return r;
}
await demo('demo_live', '');
await demo('demo_fast', '?fast');
await demo('demo_throttled_4g', '', { throttle: true });
await demo('demo_offline', '?offline', { offline: true });

// ---- the demo without JavaScript: the static summary
{
  const { ctx, page, log, reqs } = await newPage({ name: 'demo_nojs', ctx: { javaScriptEnabled: false } });
  await page.goto(BASE + 'demo/', { waitUntil: 'load' });
  const txt = await page.evaluate(() => document.body.innerText);
  await page.screenshot({ path: path.join(SHOTS, 'demo_nojs.png') });
  const ok = ['prose', 'M3', 'M4', 'M8', 'G0'].every((id) => txt.includes(EXP.results[id].line)) && txt.includes('transcript.txt');
  check(ok, 'demo_nojs: the static summary is missing a verdict');
  results.pages.demo_nojs = { url: 'demo/ (JavaScript off)', summary_has_all_verdicts: ok, errors: log, external_requests: reqs, ...(await layout(page)) };
  await ctx.close();
}
{ const r = await fetch(BASE + 'demo/transcript.txt'); const t = await r.text(); check(r.ok && ['M3', 'M4', 'M8', 'G0'].every((id) => t.includes(EXP.results[id].line)), 'transcript.txt lacks a verdict'); results.pages.transcript = { status: r.status, bytes: t.length }; }

// ---- TRY A TOKEN
{
  const { ctx, page, log, reqs } = await newPage({ name: 't' });
  const t0 = Date.now(); await page.goto(BASE + 't/', { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.__TRESULT__ && window.__TRESULT__.state !== undefined, null, { timeout: 30000 }).catch(() => {});
  const real = await page.evaluate(() => window.__TRESULT__ || null); const ms = Date.now() - t0;
  await page.screenshot({ path: path.join(SHOTS, 't.png') }); await page.screenshot({ path: path.join(SHOTS, 't_full.png'), fullPage: true });
  const L = await layout(page);
  check(real && real.state === 'ok' && real.name === EXP.token.split(':').pop() && real.value === 0.4708994708994709 && real.cell === 'defi.zb572.xoso.zb1ec' && real.bytes === 1115, 't: the real token did not re-hash and bind: ' + JSON.stringify(real));
  const runEx = async (k) => { await page.evaluate(() => { window.__TRESULT__ = undefined; }); await page.click(`[data-ex="${k}"]`); await page.waitForFunction(() => window.__TRESULT__ && window.__TRESULT__.state, null, { timeout: 30000 }).catch(() => {}); return page.evaluate(() => window.__TRESULT__ || null); };
  const m4 = await runEx('m4'); await page.screenshot({ path: path.join(SHOTS, 't_m4.png') });
  const m7 = await runEx('m7');
  check(m4 && m4.state === 'no' && m4.line.startsWith('L1 refused'), 't: M4 not refused at L1: ' + JSON.stringify(m4));
  check(m7 && m7.state === 'no' && m7.line.startsWith('L0 refused'), 't: M7 not refused at L0: ' + JSON.stringify(m7));
  check(L.scrollW <= 390, `t: horizontal scroll (${L.scrollW} px)`);
  check(!log.some((l) => l.startsWith('pageerror')), 't: page error ' + log.join('; '));
  results.pages.t = { url: 't/', ms_to_result: ms, real, m4: m4 && m4.line, m7: m7 && m7.line, ...L, errors: log, external_requests: reqs };
  await ctx.close();
}

// ---- the other pages
await simplePage('record', 'r/', async (page) => {
  const t = await page.evaluate(() => document.body.innerText);
  check(t.includes('BOARD TRACK') && t.includes('no hash') && t.includes('No signature of its own') && t.includes('oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa'), 'record: a required statement is missing');
  return { rows: await page.$$eval('tbody tr', (r) => r.length) };
});
await simplePage('test', 'test/', async (page) => { const t = await page.evaluate(() => document.body.innerText); check(t.includes('mutation_suite.py') && t.includes('research/repro/v13/r5') && t.includes('trace_fact.py') && t.includes('verify_bundle.py'), 'test: a command is missing'); return {}; });
await simplePage('methods', 'methods/', async (page) => { const t = await page.evaluate(() => document.body.innerText); check(['L0', 'L5', '20261019', 'Wilson', 'T1'].every((k) => t.includes(k)), 'methods: a section is missing'); return { refs: await page.$$eval('#refs ~ ol li', (l) => l.length) }; });
await simplePage('use', 'use/', async (page) => { const chips = await page.$$eval('.int .chip', (c) => c.map((x) => x.textContent)); check(chips.length >= 30, 'use: too few integration rows'); return { rows: chips.length, statuses: [...new Set(chips)] }; });

// ---- the six QR SVGs, rendered by Chromium, decoded by OpenCV
{
  const ctx = await browser.newContext({ viewport: { width: 600, height: 600 }, deviceScaleFactor: 1 }); const page = await ctx.newPage(); const qr = [];
  for (const q of QRM) {
    const svg = fs.readFileSync(path.join(ROOT, 'poster/fig/v13', `qr_${q.slug}.svg`), 'utf8');
    await page.setContent(`<body style="margin:0;background:#fff"><img id="q" style="width:410px;height:410px;display:block" src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}"></body>`);
    const f = path.join(tmp, `qr_${q.slug}.png`); await (await page.$('#q')).screenshot({ path: f });
    let got = ''; try { got = execFileSync('python3', ['-c', 'import cv2,sys; s,_,_=cv2.QRCodeDetector().detectAndDecode(cv2.imread(sys.argv[1],0)); print(s)', f]).toString().trim(); } catch (e) { got = 'decode error'; }
    qr.push({ slug: q.slug, payload: q.payload, chromium_render_decoded: got, ok: got === q.payload }); check(got === q.payload, `qr_${q.slug}: Chromium render decodes to "${got}"`);
  }
  results.qr = qr; await ctx.close();
}

check(results.blocked_writes.length === 0, 'a page tried to write to emem.dev: ' + results.blocked_writes.join('; '));
results.posts_to_emem = results.blocked_writes.length;
results.finished_utc = new Date().toISOString();
await browser.close(); srv.kill(); fs.rmSync(tmp, { recursive: true, force: true });
fs.writeFileSync(path.join(SHOTS, 'results.json'), JSON.stringify(results, null, 1) + '\n');
const summary = Object.fromEntries(Object.entries(results.pages).map(([k, v]) => [k, v.page_s !== undefined ? `${v.page_s && v.page_s.toFixed(2)} s` : v.load_ms !== undefined ? `${v.load_ms} ms` : v.ms_to_result !== undefined ? `${v.ms_to_result} ms` : 'ok']));
console.log(JSON.stringify({ summary, demo_lines: (results.pages.demo_live.lines || []).map((l) => `${l.id}: ${l.line}`), l3: results.pages.demo_live.l3, t: results.pages.t && results.pages.t.real && results.pages.t.real.line, posts_to_emem: results.posts_to_emem, qr: results.qr.map((q) => `${q.slug} ${q.ok}`), failures: results.failures }, null, 1));
if (results.failures.length) { console.error('SITE TEST FAIL:\n  ' + results.failures.join('\n  ')); process.exit(1); }
console.log('site test OK');

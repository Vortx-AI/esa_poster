// The browser side of the receiver demo. Data arrive inline (window.__DEMO__), verdicts come from verify.mjs.
import { blake3 } from '@noble/hashes/blake3';
import { ed25519 } from '@noble/curves/ed25519';
import * as V from './verify.mjs';

const D = window.__DEMO__;
const $ = (s) => document.querySelector(s);
const mk = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
const b64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
const q = new URLSearchParams(location.search);
const FAST = q.has('fast') || matchMedia('(prefers-reduced-motion: reduce)').matches;
const OFFLINE = q.has('offline');
const STEP = FAST ? 0 : 1500;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const T0 = performance.now(); const el = () => ((performance.now() - T0) / 1000).toFixed(1) + ' s';
const say = (t) => { $('#live').textContent = t; };
const edVerify = (sig, msg, pk) => { try { return ed25519.verify(sig, msg, pk); } catch { return false; } };

const bundleBytes = b64(D.bundle_b64);
const bundle = V.cbor(bundleBytes);
const receive = V.makeReceiver({ blake3, edVerify, bundle });
const tok = V.parseToken(bundle.token);
const fact = V.factsRaw(V.bytesOf(bundle.entry)).find((x) => V.b32e(blake3(x)) === tok.cid);
const M = V.mutations(fact, bundle.token);
const rec = V.cbor(fact);

// self-test before anything is reported (a broken hash library must not call a genuine record forged)
const emptyHex = V.hex(blake3(new Uint8Array(0)));
if (emptyHex !== 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262') { say('self-test failed: this browser\'s BLAKE3 is wrong, so this page checks nothing'); throw new Error('blake3 self-test'); }

// ---------------------------------------------------------------- the handoffs (R1 names)
const otherTok = `emem:fact:${M.otherCell}:${tok.cid}`;
const m8cid = V.b32e(blake3(M.m8));
const H = [
  { id: 'prose', tag: 'prose', title: 'A paraphrase', sub: 'evidence relayed as a sentence',
    got: '“NDVI is about 0.47 at the Keylong field, late September.”', h: { kind: 'prose' } },
  { id: 'm3', tag: 'M3', title: 'One byte changed in transit', sub: 'value moved by one ULP: 0.4708994708994709 → 0.47089947089947093; token kept',
    got: `byte ${M.off + 7} of the record: 0x${fact[M.off + 7].toString(16)} → 0x${M.m3[M.off + 7].toString(16)}`, h: { kind: 'ref', token: bundle.token, bytes: M.m3 } },
  { id: 'm4', tag: 'M4', title: 'The right record, cited for another place', sub: 'token cell swapped to a Bengaluru cell',
    got: otherTok, h: { kind: 'ref', token: otherTok, bytes: fact } },
  { id: 'm8', tag: 'M8', title: 'Value forged to 0.45 and re-hashed', sub: 'a self-consistent token for a record nobody signed',
    got: `emem:fact:${tok.cell}:${m8cid}`, h: { kind: 'ref', token: `emem:fact:${tok.cell}:${m8cid}`, bytes: M.m8 } },
  { id: 'g0', tag: 'G0', title: 'The genuine handoff', sub: 'token and bytes as signed',
    got: bundle.token, h: { kind: 'ref', token: bundle.token, bytes: fact } },
];

// ---------------------------------------------------------------- static parts
$('#tok').textContent = bundle.token;
$('#nbytes').textContent = fact.length.toLocaleString('en');
$('#val').textContent = rec.value.toFixed(4);
$('#obs').textContent = rec.sources[0].captured_at.replace(/\.\d+Z$/, 'Z').replace('T', ' ');
$('#rawhex').textContent = V.hex(fact).replace(/(.{64})/g, '$1\n');
$('#rawjson').textContent = JSON.stringify(rec, (k, v) => (k === 'signer' ? V.b32e(V.bytesOf(v)) : v), 1);

const board = $('#board');
const rows = H.map((x) => {
  const pill = mk('li', 'pill wait'); pill.append(mk('b', '', x.tag), mk('span', '', '…')); board.append(pill);
  const card = mk('section', 'card wait'); card.id = 'c-' + x.id;
  const hd = mk('header'); hd.append(mk('span', 'tag', x.tag), mk('h3', '', x.title)); card.append(hd);
  card.append(mk('p', 'sub', x.sub));
  const got = mk('p', 'got'); got.append(mk('span', 'k', 'B receives '), mk('code', '', x.got)); card.append(got);
  const ol = mk('ol', 'steps'); card.append(ol);
  const v = mk('p', 'verdict', 'waiting'); card.append(v);
  $('#cards').append(card);
  return { x, pill, card, ol, v };
});

const p3pill = mk('li', 'pill wait'); p3pill.append(mk('b', '', 'L3 pixel'), mk('span', '', '…')); board.append(p3pill);
async function play(r) {
  const res = receive(r.x.h);
  r.card.classList.remove('wait');
  for (const s of res.steps) {
    const li = mk('li', s.ok === null ? 'na' : s.ok ? 'ok' : 'no');
    li.append(mk('i', '', s.ok === null ? '·' : s.ok ? '✓' : '✕'), mk('span', 'ly', s.layer === 'none' ? '' : s.layer), mk('span', '', s.text));
    r.ol.append(li); if (!FAST) await sleep(180);
  }
  const cls = res.verdict === 'REFUSED' ? 'no' : res.checked ? 'ok' : 'warn';
  const word = res.verdict === 'REFUSED' ? res.layer + ' refused' : res.checked ? 'ACCEPTED, checked' : 'ACCEPTED, unchecked';
  r.v.textContent = V.verdictLine(res); r.res = res; r.v.className = 'verdict ' + cls; r.card.classList.add(cls);
  r.pill.className = 'pill ' + cls; r.pill.lastChild.textContent = res.verdict === 'REFUSED' ? res.layer + ' refused' : res.checked ? 'accepted' : 'unchecked';
  say(`${r.x.tag}: ${word}`);
  return res;
}

// ---------------------------------------------------------------- live confirmations (optional; verdicts never depend on them)
const live = {};
async function liveFacts() {
  if (OFFLINE) return null;
  try {
    const g = await fetch(`https://emem.dev/v1/facts/${tok.cid}`, { headers: { accept: 'application/cbor' } });
    const gb = new Uint8Array(await g.arrayBuffer());
    const f = await fetch(`https://emem.dev/v1/facts/${m8cid}`, { headers: { accept: 'application/cbor' } });
    return { genuine: g.status, same: V.eq(gb, fact), forged: f.status };
  } catch (e) { return { err: String(e.message || e) }; }
}
async function liveSource() {
  if (OFFLINE) return null;
  try {
    const sas = await (await fetch('https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel2l2a01/sentinel2-l2')).json();
    const fetchRange = async (u, a, b) => { const r = await fetch(u + '?' + sas.token, { headers: { range: `bytes=${a}-${b}` } }); if (r.status !== 206) throw new Error('source answered ' + r.status); return new Uint8Array(await r.arrayBuffer()); };
    const inflate = async (u) => new Uint8Array(await new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('deflate'))).arrayBuffer());
    const up = bundle.upstream; const out = {};
    for (const u of up) { const band = /_(B0[48])_/.exec(u.url)[1];
      out[band] = await V.rereadPixel({ url: u.url, col: u.col, row: u.row, fetchRange, inflate, H: blake3, expectTileB3: V.hex(V.bytesOf(u.tile_blake3)) }); }
    return out;
  } catch (e) { return { err: String(e.message || e) }; }
}

function drawGrid(b08, b04, off, from) {
  const g = $('#grid'); g.replaceChildren();
  for (let r = 0; r < 5; r++) for (let c = 0; c < 5; c++) {
    const v = V.ndvi(b08[r][c], b04[r][c], off), cell = mk('div', 'px');
    const t = Math.max(0, Math.min(1, (v - 0.0) / 0.7)); cell.style.setProperty('--t', t.toFixed(3));
    cell.append(mk('span', '', v.toFixed(3)));
    if (r === 2 && c === 2) cell.classList.add('named'); if (r === 3 && c === 2) cell.classList.add('south');
    g.append(cell);
  }
  $('#gridfrom').textContent = from;
}

(async function main() {
  const pFacts = liveFacts(), pSrc = liveSource();
  say('running: five handoffs, then the source');
  for (const r of rows) { await play(r); if (!FAST) await sleep(STEP); }
  // archive confirmation
  const lf = await pFacts;
  $('#archive').textContent = !lf ? 'skipped (offline mode)' : lf.err ? 'emem.dev not reachable from here (' + lf.err + '); the verdicts above used only the embedded bytes'
    : `live: GET emem.dev/v1/facts/${tok.cid.slice(0, 8)}… → ${lf.genuine}, ${lf.same ? 'byte-identical to the embedded copy' : 'DIFFERENT from the embedded copy'}; the forged name ${m8cid.slice(0, 8)}… → ${lf.forged}`;
  // L3: source re-read
  const p3 = $('#l3');
  p3.classList.remove('wait');
  const wDN = D.window_oj5; // committed 5x5 DN window (research/repro/data/v8/pixel_windows.json), the offline fallback
  drawGrid(wDN.B08, wDN.B04, wDN.offset, 'committed copy of the 5 × 5 window (research/repro/data/v8/pixel_windows.json)');
  const src = await Promise.race([pSrc, sleep(FAST ? 60000 : 9000).then(() => ({ err: 'the source took longer than 9 s' }))]);
  const L = $('#l3steps'); L.replaceChildren();
  const add = (ok, text) => { const li = mk('li', ok === null ? 'na' : ok ? 'ok' : 'no'); li.append(mk('i', '', ok === null ? '·' : ok ? '✓' : '✕'), mk('span', 'ly', 'L3'), mk('span', '', text)); L.append(li); };
  if (!src || src.err) {
    add(null, src ? 'live re-read not available: ' + src.err : 'live re-read skipped (offline mode)');
    add(null, `the committed window gives B08 ${wDN.B08[2][2]}, B04 ${wDN.B04[2][2]} at the named pixel, the DNs the record signed`);
    $('#l3verdict').textContent = 'L3 not re-read on this device: the committed copy is shown'; $('#l3verdict').className = 'verdict warn';
    p3pill.className = 'pill warn'; p3pill.lastChild.textContent = 'not re-read'; p3.classList.add('warn');
  } else {
    const a = src.B08, b = src.B04, dn = (rec.derivation.args || [])[5];
    add(a.tile_matches_trace && b.tile_matches_trace, `read the two named files from Planetary Computer: tile ${a.tile_index} of each (${(a.tile_length + b.tile_length).toLocaleString('en')} B); their BLAKE3 equals the hashes taken on 30 Sep`);
    add(a.dn === dn[0] && b.dn === dn[1], `pixel (col ${bundle.upstream[0].col}, row ${bundle.upstream[0].row}): B08 ${a.dn}, B04 ${b.dn}; the record signed ${dn[0]}, ${dn[1]}`);
    const v = V.ndvi(a.dn, b.dn, (rec.derivation.args || [])[12]);
    add(v === rec.value, `NDVI from the re-read pixel: ${v} ${v === rec.value ? '= the signed value, bit for bit' : '≠ the signed value'}`);
    drawGrid(a.win, b.win, (rec.derivation.args || [])[12], 'live: re-read from the source by this browser just now');
    const ok = a.dn === dn[0] && b.dn === dn[1] && v === rec.value;
    $('#l3verdict').textContent = ok ? 'L3 re-read: the named pixel of the named files gives the signed value, bit for bit.' : 'L3 refused: the named pixel does not give the signed value.'; $('#l3verdict').className = 'verdict ' + (ok ? 'ok' : 'no');
    p3pill.className = 'pill ' + (ok ? 'ok' : 'no'); p3pill.lastChild.textContent = ok ? 're-read, matches' : 'MISMATCH'; p3.classList.add(ok ? 'ok' : 'no'); say('L3: ' + $('#l3verdict').textContent);
    live.src = src;
  }
  const sx = V.ndvi(wDN.B08[3][2], wDN.B04[3][2], wDN.offset);
  $('#south').textContent = sx.toFixed(4);
  $('#bnd').classList.remove('wait');
  $('#done').textContent = `done in ${el()}${OFFLINE ? ' (offline)' : ''}`;
  say('done: one paraphrase accepted unchecked; M3 refused at L0, M4 at L1, M8 at L0; the genuine record accepted at L0 to L2; ' + (src && !src.err ? 'its pixel re-read at L3' : 'L3 not re-read'));
  window.__RESULT__ = { verdicts: rows.map((r) => r.pill.className).concat([p3pill.className]), lines: rows.map((r) => ({ id: r.x.tag, line: V.verdictLine(r.res), layer: r.res.layer || null, verdict: r.res.verdict, checked: !!r.res.checked })), l3: $('#l3verdict').textContent, south: $('#south').textContent, seconds: (performance.now() - T0) / 1000, live: { facts: lf, src: src && !src.err ? { B08: src.B08.dn, B04: src.B04.dn, b3: [src.B08.tile_matches_trace, src.B04.tile_matches_trace] } : src } };
})();

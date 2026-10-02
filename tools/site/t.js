// TRY A TOKEN: resolve one emem:fact token with a single GET, re-hash the bytes, decode them, bind the cell.
// Read-only: the only request is GET https://emem.dev/v1/facts/<cid> (Accept: application/cbor). Nothing is written.
import { blake3 } from '@noble/hashes/blake3';
import * as V from './verify.mjs';

const $ = (s) => document.querySelector(s);
const mk = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
const REAL = window.__T__.token;
const box = $('#tok'), out = $('#out'), steps = $('#steps'), verdict = $('#verdict'), fields = $('#fields');
if (V.hex(blake3(new Uint8Array(0))) !== 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262') {
  verdict.textContent = 'Self-test failed: this browser computes BLAKE3 wrongly, so this page checks nothing.'; throw new Error('blake3 self-test');
}

function add(layer, ok, text) {
  const li = mk('li', ok === null ? 'na' : ok ? 'ok' : 'no');
  li.append(mk('i', '', ok === null ? '·' : ok ? '✓' : '✕'), mk('span', 'ly', layer), mk('span', '', text)); steps.append(li);
}
function show(v) {
  if (v instanceof Uint8Array) return `${v.length} bytes: ${V.hex(v).slice(0, 32)}${v.length > 16 ? '…' : ''}`;
  if (Array.isArray(v) && v.length === 32 && v.every((x) => Number.isInteger(x) && x >= 0 && x < 256)) return V.b32e(Uint8Array.from(v)) + ' (32-byte key)';
  if (typeof v === 'object' && v !== null) { const s = JSON.stringify(v); return s.length > 600 ? s.slice(0, 600) + '…' : s; }
  return String(v);
}
function row(k, v) { const tr = mk('tr'); tr.append(mk('th', '', k), mk('td', '', v)); fields.append(tr); }
function done(state, line, extra) {
  verdict.textContent = line; verdict.className = 'verdict ' + state;
  window.__TRESULT__ = { state, line, ...extra };
  $('#status').textContent = line;
}

async function check(token) {
  steps.replaceChildren(); fields.replaceChildren(); out.hidden = false; verdict.className = 'verdict'; verdict.textContent = 'checking…';
  const t0 = performance.now();
  const q = encodeURIComponent(token.trim());
  $('#verifylink').href = 'https://emem.dev/verify?q=' + q;
  history.replaceState(null, '', '?q=' + q);
  const t = V.parseToken(token);
  if (!t) { add('L0', false, 'this is not an emem:fact token (emem:fact:<cell>:<52-character name>)'); return done('no', 'L0 refused: not an emem:fact token', { token }); }
  add('L0', null, `asking emem.dev for the bytes named ${t.cid.slice(0, 8)}… (GET /v1/facts/${t.cid.slice(0, 8)}…, CBOR)`);
  $('#rawlink').href = `https://emem.dev/v1/facts/${t.cid}`; $('#rawlink').textContent = `emem.dev/v1/facts/${t.cid.slice(0, 8)}…`;
  let res, bytes;
  try { res = await fetch(`https://emem.dev/v1/facts/${t.cid}`, { headers: { accept: 'application/cbor' } }); bytes = new Uint8Array(await res.arrayBuffer()); }
  catch (e) { add('L0', null, 'emem.dev could not be reached from this browser: ' + (e.message || e)); return done('warn', 'Not checked: emem.dev is not reachable from here', { token }); }
  if (res.status === 404) { add('L0', false, 'emem.dev holds no record with this name (HTTP 404)'); return done('no', 'L0 refused: no record has this name', { token, status: 404 }); }
  if (res.status !== 200) { add('L0', null, `emem.dev answered HTTP ${res.status}`); return done('warn', `Not checked: emem.dev answered HTTP ${res.status}`, { token, status: res.status }); }
  const name = V.b32e(blake3(bytes));
  const hashOk = name === t.cid;
  add('L0', hashOk, hashOk ? `your browser re-hashed the ${bytes.length.toLocaleString('en')} bytes with BLAKE3-256: they hash to the name in the token` : `the ${bytes.length.toLocaleString('en')} bytes hash to ${name.slice(0, 8)}…, not to ${t.cid.slice(0, 8)}…`);
  if (!hashOk) return done('no', 'L0 refused: the bytes do not hash to the name', { token, name });
  let rec; try { rec = V.cbor(bytes); } catch { add('L0', false, 'the bytes are not a CBOR record'); return done('no', 'L0 refused: the bytes are not a CBOR record', { token }); }
  for (const [k, v] of Object.entries(rec)) {
    if (k === 'tslot' && typeof v === 'number') row(k, `${v} (UTC day ${V.tslotDate(v)})`);
    else if (k === 'sources' && Array.isArray(v)) v.forEach((s, i) => { for (const [sk, sv] of Object.entries(s)) row(`sources[${i}].${sk}`, show(sv)); });
    else if (k === 'derivation' && v && typeof v === 'object') { row('derivation.fn_key', show(v.fn_key)); if (v.args) row('derivation.args', show(v.args)); }
    else row(k, show(v));
  }
  const cellOk = rec.cell === t.cell;
  add('L1', cellOk, cellOk ? `the record's own cell is the token's cell (${rec.cell})` : `the token says ${t.cell}; the record says ${rec.cell}`);
  if (!cellOk) return done('no', 'L1 refused: the record is about another cell than the token names', { token, record_cell: rec.cell });
  const src = (rec.sources || [])[0] || {};
  const hasHash = !!(src.hash || src.cid);
  add('L3', null, hasHash ? 'the record carries a hash or cid for its source; this page does not fetch the source' : 'the record names its source by URL or id and carries no hash of it; checking the source means re-reading it (VIEW THE DEMO does that for the Keylong record)');
  add('L0', null, 'not checked on this page: the batch attestation signature and the log entry. The record has no signature of its own; INSPECT THE RECORD and VIEW THE DEMO show both for the Keylong record');
  const ms = Math.round(performance.now() - t0);
  $('#summary').textContent = `${rec.band || ''} · ${typeof rec.value === 'number' ? rec.value : show(rec.value)} · cell ${rec.cell} · tslot ${rec.tslot} (${typeof rec.tslot === 'number' ? V.tslotDate(rec.tslot) : '?'})` + (src.captured_at ? ` · captured ${src.captured_at}` : '') + (src.scheme ? ` · source ${src.scheme}` : '');
  return done('ok', 'ACCEPTED at L0 (re-hashed) and L1 (cell bound); signature, log, recompute and source not checked here', { token, ms, value: rec.value, band: rec.band, cell: rec.cell, tslot: rec.tslot, captured_at: src.captured_at, scheme: src.scheme, name, bytes: bytes.length });
}

const p = new URLSearchParams(location.search);
box.value = (p.get('q') || REAL).trim();
$('#go').addEventListener('click', () => check(box.value));
for (const b of document.querySelectorAll('[data-ex]')) b.addEventListener('click', () => { box.value = window.__T__.examples[b.dataset.ex]; check(box.value); });
check(box.value);

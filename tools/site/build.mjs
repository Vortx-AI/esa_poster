// Build the receiver demo: docs/demo/index.html (one self-contained page) and docs/demo/transcript.txt (the text
// fallback), from committed data only. The same receiver code (verify.mjs) runs here and in the browser.
//   node tools/site/build.mjs [repo_root] [out_dir]
import fs from 'fs'; import path from 'path'; import crypto from 'crypto';
import * as esbuild from 'esbuild';
import { blake3 } from '@noble/hashes/blake3';
import { ed25519 } from '@noble/curves/ed25519';
import * as V from './verify.mjs';

const here = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(process.argv[2] || path.join(here, '../..'));
const out = path.resolve(process.argv[3] || path.join(ROOT, 'docs/demo'));
fs.mkdirSync(out, { recursive: true });
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const bundlePath = path.join(ROOT, 'research/repro/v8/proof_bundle_ndvi.cbor');
const bundleBytes = new Uint8Array(fs.readFileSync(bundlePath));
const sha = crypto.createHash('sha256').update(bundleBytes).digest('hex');
const win = JSON.parse(fs.readFileSync(path.join(ROOT, 'research/repro/data/v8/pixel_windows.json'), 'utf8'));
const wkey = Object.keys(win).find((k) => k.startsWith('oj5cecci')); const w = win[wkey];
const prev = JSON.parse(fs.readFileSync(path.join(ROOT, 'research/repro/data/v8/prevalence_summary.json'), 'utf8')).pre;
const img = fs.readFileSync(path.join(here, 'keylong_tc_192.webp')).toString('base64');

// ---- the same receiver, run here: writes the transcript and fails the build on any unexpected verdict
const bundle = V.cbor(bundleBytes);
const edVerify = (s, m, p) => { try { return ed25519.verify(s, m, p); } catch { return false; } };
const receive = V.makeReceiver({ blake3, edVerify, bundle });
if (V.hex(blake3(new Uint8Array(0))) !== 'af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262') throw new Error('BLAKE3 self-test failed');
const tok = V.parseToken(bundle.token);
const fact = V.factsRaw(V.bytesOf(bundle.entry)).find((x) => V.b32e(blake3(x)) === tok.cid);
const M = V.mutations(fact, bundle.token), rec = V.cbor(fact), m8cid = V.b32e(blake3(M.m8));
const cases = [
  ['prose', 'A paraphrase', '"NDVI is about 0.47 at the Keylong field, late September."', { kind: 'prose' }, ['ACCEPTED', false, null]],
  ['M3', 'One byte changed in transit (value +1 ULP, token kept)', `byte ${M.off + 7}: 0x${fact[M.off + 7].toString(16)} -> 0x${M.m3[M.off + 7].toString(16)} (value 0.4708994708994709 -> 0.47089947089947093)`, { kind: 'ref', token: bundle.token, bytes: M.m3 }, ['REFUSED', undefined, 'L0']],
  ['M4', 'The right record, cited for another place', `emem:fact:${M.otherCell}:${tok.cid}`, { kind: 'ref', token: `emem:fact:${M.otherCell}:${tok.cid}`, bytes: fact }, ['REFUSED', undefined, 'L1']],
  ['M8', 'Value forged to 0.45 and re-hashed', `emem:fact:${tok.cell}:${m8cid}`, { kind: 'ref', token: `emem:fact:${tok.cell}:${m8cid}`, bytes: M.m8 }, ['REFUSED', undefined, 'L0']],
  ['G0', 'The genuine handoff', bundle.token, { kind: 'ref', token: bundle.token, bytes: fact }, ['ACCEPTED', true, 'L0, L1, L2']],
];
const n = (dn) => V.ndvi(dn[0], dn[1], w.offset);
const south = n([w.B08[3][2], w.B04[3][2]]), named = n([w.B08[2][2], w.B04[2][2]]);
if (named !== rec.value) throw new Error('committed window does not give the signed value');

const L = [], S = [], results = {};
L.push('EMEM receiver demo: text version (deterministic; written by tools/site/build.mjs from committed data with the page\'s own receiver code)');
L.push(`Observation: NDVI ${rec.value} at cell ${rec.cell} (near Keylong, Lahaul, India), Sentinel-2A L2A B08/B04, captured ${rec.sources[0].captured_at}, signed ${rec.signed_at}.`);
L.push(`Agent A hands over: ${bundle.token}`);
L.push(`It names ${fact.length} bytes of CBOR by their BLAKE3-256 hash. Receiver: Agent B, using BLAKE3, Ed25519 and CBOR only; pinned key ${V.PINNED_KEY_B32}.`);
L.push('Ladder: L0 record integrity (hash, attestation signature, log), L1 observation identity, L2 derivation, L3 source re-read, L4 entity, L5 truth and decision.');
L.push('');
for (const [id, title, got, h, [ev, ec, el]] of cases) {
  const r = receive(h);
  if (r.verdict !== ev || (ec !== undefined && !!r.checked !== ec) || (r.layer || null) !== el) throw new Error(`${id}: expected ${ev}/${el}, got ${r.verdict}/${r.layer}`);
  results[id] = { verdict: r.verdict, checked: !!r.checked, layer: r.layer || null, line: V.verdictLine(r) };
  L.push(`${id}. ${title}`); L.push(`   B receives: ${got}`);
  for (const s of r.steps) L.push(`   [${s.ok === null ? ' -- ' : s.ok ? 'pass' : 'FAIL'}] ${s.layer === 'none' ? '  ' : s.layer} ${s.text}`);
  L.push(`   => ${V.verdictLine(r)}`); L.push('');
  S.push(`<li><b>${esc(id)}</b> ${esc(title)}: <b>${esc(V.verdictLine(r))}</b></li>`);
}
L.push('L3. Re-read the named pixel (live in the browser; the committed copy is below)');
L.push(`   files: ${bundle.upstream.map((u) => u.url.split('/').pop()).join(', ')}; pixel col ${bundle.upstream[0].col}, row ${bundle.upstream[0].row}`);
L.push('   the record names these files by URL and carries no hash of them, so L3 is a re-read, not a hash check');
L.push(`   named pixel: B08 ${w.B08[2][2]}, B04 ${w.B04[2][2]}, offset ${w.offset} -> NDVI ${named} (signed value ${rec.value}; equal bit for bit)`);
L.push(`   pixel 10 m south: B08 ${w.B08[3][2]}, B04 ${w.B04[3][2]} -> NDVI ${south}. Before 28 Sep 2026 emem's reader took this pixel; ${prev.matches_round_not_floor} of ${prev.n} sampled earlier records carried such values. Signatures cannot see it; only the re-read can.`);
L.push('');
L.push('Not checkable here: L4 whether this cell is the field Agent A meant (out of scope); L5 whether the sensor and a decision taken on the value are right (inherited from product validation, or out of scope).');
L.push('A signature fixes the bytes. It does not make the measurement true.');
L.push(''); L.push(`Embedded data: research/repro/v8/proof_bundle_ndvi.cbor (${bundleBytes.length} B, sha256 ${sha}); research/repro/data/v8/pixel_windows.json ["${wkey}"].`);
fs.writeFileSync(path.join(out, 'transcript.txt'), L.join('\n') + '\n');
S.push(`<li><b>L3</b> the committed 5 × 5 window gives B08 ${w.B08[2][2]}, B04 ${w.B04[2][2]} at the named pixel, NDVI ${named}, equal to the signed value; the pixel 10 m south gives ${south.toFixed(4)}. A browser with JavaScript re-reads it live.</li>`);
const STATIC = `<ul>${S.join('')}</ul><p>L4 (is this the field A meant) and L5 (is the sensor right, is the decision right) are not checkable from the record.</p>`;

// ---- the page
const js = await esbuild.build({ entryPoints: [path.join(here, 'page.js')], bundle: true, minify: true, format: 'iife', target: ['es2020', 'safari15'], write: false, legalComments: 'none' });
const DATA = JSON.stringify({ bundle_b64: Buffer.from(bundleBytes).toString('base64'), window_oj5: { B08: w.B08, B04: w.B04, offset: w.offset } });
const html = fs.readFileSync(path.join(here, 'template.html'), 'utf8')
  .replace('{{IMG}}', 'data:image/webp;base64,' + img).replace('{{DATA}}', () => DATA)
  .replace('{{BUNDLE_JS}}', () => js.outputFiles[0].text.replace(/<\/script/g, '<\\/script'))
  .replace('{{STATIC}}', () => STATIC).replace('{{TOKEN}}', bundle.token).replaceAll('{{NBYTES}}', fact.length.toLocaleString('en'))
  .replace('{{SOUTH}}', south.toFixed(4)).replace('{{PREV_N}}', String(prev.n)).replace('{{PREV_K}}', String(prev.matches_round_not_floor))
  .replace('{{BUNDLE_LEN}}', bundleBytes.length.toLocaleString('en')).replace('{{BUNDLE_SHA}}', sha);
if (/\{\{[A-Z_]+\}\}/.test(html)) throw new Error('unfilled placeholder: ' + html.match(/\{\{[A-Z_]+\}\}/)[0]);
fs.writeFileSync(path.join(out, 'index.html'), html);
fs.writeFileSync(path.join(out, 'expected.json'), JSON.stringify({ token: bundle.token, results, south, named, m8cid, m3cid: V.b32e(blake3(M.m3)) }, null, 1) + '\n');
const h = (f) => crypto.createHash('sha256').update(fs.readFileSync(path.join(out, f))).digest('hex');
console.log(JSON.stringify({ demo: path.relative(ROOT, out), index_bytes: Buffer.byteLength(html), js_bytes: js.outputFiles[0].text.length, verdicts: Object.fromEntries(Object.entries(results).map(([k, v]) => [k, v.line])), transcript_sha256: h('transcript.txt') }));

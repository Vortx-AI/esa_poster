// The rest of the poster's Pages site: landing, TRY A TOKEN, INSPECT THE RECORD, RE-RUN THE TEST, READ THE METHODS,
// DISCOVER INTEGRATIONS. Every number is read from a committed file at build time; nothing is typed by hand twice.
//   node tools/site/site.mjs [repo_root] [docs_dir]
import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process';
import * as esbuild from 'esbuild';
import { blake3 } from '@noble/hashes/blake3';
import * as V from './verify.mjs';

const here = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(process.argv[2] || path.join(here, '../..'));
const out = path.resolve(process.argv[3] || path.join(ROOT, 'docs'));
const rd = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');
const rj = (p) => JSON.parse(rd(p));
const w = (p, s) => { fs.mkdirSync(path.dirname(path.join(out, p)), { recursive: true }); fs.writeFileSync(path.join(out, p), s); };
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const GH = 'https://github.com/Vortx-AI/esa_poster';
const tree = (p) => `${GH}/tree/main/${p}`, blob = (p) => `${GH}/blob/main/${p}`;
const src = (p, label) => `<a href="${blob(p)}"><code>${esc(label || p)}</code></a>`;
// date a committed file was last committed (UTC), so every number carries the date of its file
const gitDate = (p) => { try { return execFileSync('git', ['-C', ROOT, 'log', '-1', '--date=format-local:%Y-%m-%d', '--format=%cd', '--', p], { env: { ...process.env, TZ: 'UTC' } }).toString().trim() || 'uncommitted'; } catch { return 'uncommitted'; } };
const fmt = (x, d = 1) => Number(x).toLocaleString('en', { minimumFractionDigits: d, maximumFractionDigits: d });
const int = (x) => Number(x).toLocaleString('en');
const pct = (x, d = 1) => fmt(100 * x, d) + ' %';

// ------------------------------------------------------------------ the evidence these pages print
const bundleBytes = new Uint8Array(fs.readFileSync(path.join(ROOT, 'research/repro/v8/proof_bundle_ndvi.cbor')));
const bundle = V.cbor(bundleBytes);
const tok = V.parseToken(bundle.token), entry = V.bytesOf(bundle.entry), att = V.cbor(entry);
const fact = V.factsRaw(entry).find((x) => V.b32e(blake3(x)) === tok.cid), rec = V.cbor(fact);
const S = bundle.sth, W = bundle.witness, a = rec.derivation.args, s0 = rec.sources[0];
const TOKEN = bundle.token, CID = tok.cid;
const VERIFY_URL = 'https://emem.dev/verify?q=' + encodeURIComponent(TOKEN);
const win = rj('research/repro/data/v8/pixel_windows.json'); const wk = Object.keys(win).find((k) => k.startsWith('oj5cecci')); const pw = win[wk];
const SOUTH = V.ndvi(pw.B08[3][2], pw.B04[3][2], pw.offset);
const PREV_FILE = 'research/v13/evidence/g1_pixel_audit/prevalence_summary.json', PREV = rj(PREV_FILE);
const R1_FILE = 'research/repro/v11/out/mutation_matrix.json', R1 = rj(R1_FILE);
const COST_FILE = 'research/v13/cost_measurements.json', COST = rj(COST_FILE);
const ECO_FILE = 'research/v13/ecosystem_manifest.json', ECO = rj(ECO_FILE);
const XRT_FILE = 'research/repro/data/v8/crossruntime_table.json';
const XRT = fs.existsSync(path.join(ROOT, XRT_FILE)) ? rj(XRT_FILE) : null;
const R5_FILE = 'research/repro/v13/r5/results.json';
const R5 = fs.existsSync(path.join(ROOT, R5_FILE)) ? rj(R5_FILE) : null;   // final R5 results, when committed
const R5_FINAL = !!(R5 && R5.final === true);
const kn = (o) => `${o.k}/${o.n}`;
const knp = (o, w) => `${o.k}/${o.n} (${pct(o.k / o.n)}, ${pct(w[0])} to ${pct(w[1])})`;
const FORMAL_FILE = 'research/v13/evidence/formalism/test_results.json';
const FORMAL = rj(FORMAL_FILE);
const BUILT = new Date().toISOString().slice(0, 10);

// ------------------------------------------------------------------ layout
const page = (dir, title, desc, crumb, body, { csp = '', head = '' } = {}) => {
  const up = dir ? '../' : './';
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
${csp ? `<meta http-equiv="Content-Security-Policy" content="${csp}">\n` : ''}<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="stylesheet" href="${up}assets/site.css">
${head}</head>
<body>
<main>
<nav class="top" aria-label="site">${dir ? `<a href="../">EMEM poster</a><span>·</span><span>${esc(crumb)}</span>` : '<span>EMEM poster · Agentic AI for EO, Berlin, 19 Oct 2026</span>'}</nav>
${body}
<footer>
<p>Jaya Kumari, Avijeet Singh · Vortx AI · Poster Session 1, Agentic AI for Earth Observation (ESA Φ-lab and BIFOLD), Berlin, 19 Oct 2026.</p>
<p>These pages are static files built from the poster repository on ${BUILT} by <a href="${tree('tools/site')}">tools/site</a>. No account, no key, no tracking. They never write to emem.dev.</p>
</footer>
</main>
</body>
</html>
`;
};
const table = (head, rows, cls = '') => `<div class="tw"><table class="${cls}${head.length >= 4 ? ' wide' : ''}"><thead><tr>${head.map((h) => `<th${h.startsWith('#') ? ' class="n"' : ''}>${esc(h.replace(/^#/, ''))}</th>`).join('')}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((c, i) => (i === 0 ? `<th>${c}</th>` : `<td${/^[\d.,\s%µmsBMk/−-]+$/.test(String(c).replace(/<[^>]+>/g, '')) && String(c).length < 24 ? ' class="n"' : ''}>${c}</td>`)).join('')}</tr>`).join('')}</tbody></table></div>`;

// ------------------------------------------------------------------ landing
const CTAS = [
  ['TRY IT', 'demo/', 'Become Agent B in your browser. Resolve a real observation and run its checks. No sign-in.', true],
  ['INSPECT', 'r/', `Open the ${int(fact.length)}-byte observation record, its source references and batch attestation.`],
  ['CONNECT', 'use/', 'Use ChatGPT, Claude, Visual Studio Code, Dify or Salesforce MuleSoft. Copy a token and try a handoff.'],
  ['REPRODUCE', 'methods/', 'Read the methods, run the experiments and explore the recovered demonstrations.'],
];
w('index.html', page('', 'EMEM at Agentic AI for EO 2026', 'An Earth observation that survives an agent handoff. Try it, inspect the record, reproduce the experiments.', '', `
<h1>An Earth observation that survives an agent handoff.</h1>
<p class="lead">EMEM gives an observation a lookup identity and a content-addressed record. Agent A passes a compact reference; Agent B resolves the same record and checks it before continuing. Earth data stays upstream while its reference enters the reasoning.</p>
<p><a class="btn" href="${GH}/raw/refs/heads/main/poster/emem-poster-A0.pdf">Download the A0 poster</a> · <a href="${blob('poster/emem-poster-preview.png')}">View the poster</a></p>
${CTAS.map(([k, u, d, hero]) => `<a class="cta${hero ? ' hero' : ''}" href="./${u}"><b>${k} →</b><span>${esc(d)}</span></a>`).join('\n')}
<p class="note"><a href="./t/">Resolve your own token</a> · <a href="./use/">Find an integration</a> · <a href="./test/">Run the tests</a></p>
<p class="note">Source and evidence: <a href="${GH}">github.com/Vortx-AI/esa_poster</a>.</p>`));

// ------------------------------------------------------------------ TRY A TOKEN
const tjs = await esbuild.build({ entryPoints: [path.join(here, 't.js')], bundle: true, minify: true, format: 'iife', target: ['es2020', 'safari15'], write: false, legalComments: 'none' });
const examples = { real: TOKEN, m4: `emem:fact:defi.zb493.xuqA.zcb5f:${CID}`, m7: `emem:fact:${tok.cell}:${(CID[0] === 'o' ? 'p' : 'o') + CID.slice(1)}` };
w('t/index.html', page('t', 'TRY A TOKEN · EMEM', 'Resolve an emem:fact token with one GET, re-hash its bytes in your browser and check its cell.', 'try a token', `
<h1>Try a token</h1>
<p class="lead">An <code>emem:fact</code> token names one record by the BLAKE3-256 hash of its bytes, and says which cell it is about. Your browser asks emem.dev for those bytes with one GET, hashes them itself, decodes them and compares the cell. Nothing is written.</p>
<label for="tok" class="note">Token (the Keylong NDVI record from the poster is filled in):</label>
<textarea id="tok" rows="3" spellcheck="false" autocapitalize="off" autocomplete="off" style="width:100%;font:13px/1.4 var(--mono);padding:8px;border:1.5px solid var(--ink2);border-radius:8px;background:var(--card);color:var(--ink);margin:4px 0 8px">${esc(TOKEN)}</textarea>
<p><button id="go" type="button" class="btn">CHECK THIS TOKEN</button></p>
<p class="note">Or try: <button type="button" class="ex" data-ex="real">the real token</button> <button type="button" class="ex" data-ex="m4">same name, another cell (M4)</button> <button type="button" class="ex" data-ex="m7">one character changed (M7)</button></p>
<p id="status" role="status" aria-live="polite" class="sr"></p>
<section id="out" class="box" hidden>
<p class="verdict" id="verdict"></p>
<p id="summary" style="font:600 14px/1.4 var(--mono)"></p>
<ol class="steps" id="steps"></ol>
<h3>The record, decoded</h3>
<div class="tw"><table class="kv"><tbody id="fields"></tbody></table></div>
<p class="note">Raw bytes: <a id="rawlink" href="https://emem.dev/v1/facts/${CID}">emem.dev/v1/facts/${CID.slice(0, 8)}…</a> (send <code>Accept: application/cbor</code> for the CBOR).</p>
</section>
<h2>What this page checks, and what it does not</h2>
<ul>
<li><b>L0 hash:</b> the bytes emem.dev returns hash to the name in the token. A changed byte gives another name.</li>
<li><b>L1 cell:</b> the record's own cell equals the cell in the token. The right record cited for another place is refused.</li>
<li><b>Not here:</b> the record carries no signature of its own. The operator signs a Merkle root over BLAKE3 hashes of a batch of records, and the batch sits in a public log. <a href="../demo/">VIEW THE DEMO</a> checks both for the Keylong record. The source is named, not hashed, so checking it means re-reading it (L3, also in the demo).</li>
</ul>
<p>The same token on emem.dev's own checker, which also verifies the server's signed resolve receipt: <a id="verifylink" href="${esc(VERIFY_URL)}">emem.dev/verify?q=&lt;token&gt;</a>. On a phone its result starts below the first screen.</p>
<noscript><p class="box">This page needs JavaScript to fetch and hash the bytes. Without it, open <a href="${esc(VERIFY_URL)}">emem.dev/verify</a> with the token, or read the record field by field on <a href="../r/">INSPECT THE RECORD</a>.</p></noscript>
<script>window.__T__=${JSON.stringify({ token: TOKEN, examples })};</script>
<script>${tjs.outputFiles[0].text.replace(/<\/script/g, '<\\/script')}</script>`, {
  csp: "default-src 'none'; script-src 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src https://emem.dev; base-uri 'none'; form-action 'none'",
  head: `<style>
.btn,.ex{font:700 14px/1 var(--mono);letter-spacing:.04em;border:1.5px solid var(--blue);background:var(--blue);color:#fff;border-radius:8px;padding:11px 14px;cursor:pointer}
.ex{font-weight:600;font-size:12.5px;background:var(--card);color:var(--blue);padding:7px 9px;margin:3px 2px}
.steps{list-style:none;padding:0;margin:8px 0;display:grid;gap:5px;font-size:14px}
.steps li{display:grid;grid-template-columns:16px 26px 1fr;gap:4px;align-items:baseline}
.steps i{font-style:normal;font-weight:700}.steps .ly{font:600 11px/1 var(--mono);color:var(--mute)}
.steps .ok i{color:var(--blue)}.steps .no i,.steps .no span:last-child{color:var(--red)}.steps .na i{color:var(--mute)}
.verdict{font-weight:700;font-size:16px;margin:0 0 6px}.verdict.ok{color:var(--blue)}.verdict.no{color:var(--red)}.verdict.warn{color:var(--amber-ink)}
</style>
` }));

// ------------------------------------------------------------------ INSPECT THE RECORD
const b32 = (u) => V.b32e(V.bytesOf(u));
const Y = '<span class="yes">yes</span>', N = '<span class="no">no</span>';
const argLabels = ['latitude of the cell node', 'longitude of the cell node', 'Sentinel-2 scene id', 'EPSG code of the asset', 'formula note', 'DNs read [B08, B04]', 'scene cloud cover, %', 'maximum cloud cover allowed, %', 'look-back window, days', 'SCL class at the pixel', 'scenes tried', 'STAC catalogue searched', 'BOA offset'];
const argLayer = ['L1, L3', 'L1, L3', 'L3', 'L3', 'L2', 'L2, L3', 'L3', 'L3', 'L3', 'L3', 'L3', 'L3', 'L2, L3'];
const files = s0.id.split(' ; ');
const fieldRows = [
  ['kind', `<code>${esc(rec.kind)}</code>`, Y, N, 'L0'],
  ['cell', `<code>${rec.cell}</code> (node ${a[0].toFixed(5)}° N, ${a[1].toFixed(5)}° E, near Keylong, Lahaul, India)`, Y, N, 'L1'],
  ['band', `<code>${rec.band}</code>`, Y, N, 'L1'],
  ['tslot', `${rec.tslot} (UTC day ${V.tslotDate(rec.tslot)})`, Y, N, 'L1'],
  ['value', `<b>${rec.value}</b> (IEEE-754 double)`, Y, N, 'L0, L2'],
  ['confidence', `${rec.confidence.toFixed(2)} (single-precision float)`, Y, N, 'L2'],
  ['sources[0].scheme', `<code>${s0.scheme}</code>`, Y, N, 'L3'],
  ['sources[0].id', files.map((f) => `<code>${esc(f.split('/').pop())}</code>`).join('<br>') + `<br><span class="note">two Planetary Computer COG URLs, named in full; <b>no hash of either file</b></span>`, Y, '<span class="no">no: named by URL only</span>', 'L3'],
  ['sources[0].captured_at', s0.captured_at, Y, N, 'L1, L3'],
  ['derivation.fn_key', `<code>${rec.derivation.fn_key}</code>`, Y, N, 'L2'],
  ...a.map((v, i) => [`derivation.args[${i}]`, `${esc(argLabels[i] || 'argument')}: <code>${esc(Array.isArray(v) ? '[' + v.join(', ') + ']' : v)}</code>`, Y, N, argLayer[i] || '']),
  ['privacy_class', `<code>${rec.privacy_class}</code>`, Y, N, 'none'],
  ['schema_cid', `<code>${rec.schema_cid}</code>`, Y, N, 'L0'],
  ['signer', `<code>${b32(rec.signer)}</code> (emem.dev's key; a field, not a signature)`, Y, N, 'L0'],
  ['signed_at', rec.signed_at, Y, N, 'L1, L3'],
];
const absentRows = [
  ['unit', 'absent'], ['uncertainty', 'absent'], ['sources[0].hash', 'absent: the server never fills it'], ['sources[0].cid', 'absent'],
  ['reader stamp (cog-pixel-floor@2)', 'absent: signed after the pixel fix of 28 Sep 2026 04:09Z, before the stamp was added'],
];
const attRows = [
  ['facts', `a batch of ${att.facts.length} record; its leaf is BLAKE3 of the ${int(fact.length)} bytes above`, 'via batch_root'],
  ['batch_root', `<code>${b32(att.batch_root)}</code> (Merkle root over the sorted BLAKE3 leaves)`, Y],
  ['registry_cid', `<code>${att.registry_cid}</code>`, Y],
  ['schema_cid', `<code>${att.schema_cid}</code>`, Y],
  ['attester', `<code>${b32(att.attester)}</code> (the verifying key)`, 'the key that verifies'],
  ['signature', `Ed25519, ${V.bytesOf(att.signature).length} bytes, over BLAKE3(PreimageV1("attestation"){1: batch_root, 2: registry_cid, 3: schema_cid})`, 'is the signature'],
  ['attested_at', att.attested_at, '<span class="no">no</span> (bound only by the log entry hash)'],
  ['attester_key_epoch', String(att.attester_key_epoch), N],
  ['preimage_version', String(att.preimage_version), 'selects the rule'],
];
const logRows = [
  ['log entry', `${int(bundle.leaf_index)} (leaf = BLAKE3(0x00 ‖ BLAKE3(attestation entry)), entry ${int(entry.length)} B)`, `<a href="https://emem.dev/v1/log/entries?start=${bundle.leaf_index}&end=${bundle.leaf_index + 1}">GET the entry</a>`],
  ['signed tree head', `${int(S.tree_size)} entries, signed ${S.signed_at} by <code>${b32(S.pubkey).slice(0, 8)}…</code>; inclusion path of ${S.inclusion_path.length} hashes`, `<a href="https://emem.dev/v1/log/inclusion?leaf_index=${bundle.leaf_index}&tree_size=${S.tree_size}">GET the inclusion proof</a>`],
  ['witness', `key <code>${b32(W.pubkey).slice(0, 12)}…</code> co-signed head ${int(W.tree_size)}; consistency proof of ${W.consistency_to_sth.length} hashes to the head above`, `<a href="https://emem.dev/v1/log/consistency?first=${W.tree_size}&second=${S.tree_size}">GET the consistency proof</a>`],
  ['current head', 'the log keeps growing; pin a head and ask for consistency later', '<a href="https://emem.dev/v1/log/sth">GET /v1/log/sth</a>'],
];
w('r/index.html', page('r', 'INSPECT THE RECORD · EMEM', `The ${fact.length}-byte record behind the EMEM poster's main example, field by field.`, 'inspect the record', `
<h1>The record Agent A handed over</h1>
<p class="lead">One observation: NDVI ${rec.value.toFixed(4)} at one 10 m cell near Keylong on ${V.tslotDate(rec.tslot)}, from a Sentinel-2A L2A scene. Below is every field of its ${int(fact.length)} bytes, read by the build from <code>research/repro/v8/proof_bundle_ndvi.cbor</code>.</p>
<div class="box">
<p><b>The token:</b> <code>${TOKEN}</code></p>
<p><b>Its name:</b> <code>${CID}</code> = base32(BLAKE3-256(the ${int(fact.length)} bytes)). The name binds every field below. It names this record, not the satellite file.</p>
<p><b>No signature of its own.</b> The record carries the signer's key as a field. The signature is on the batch: the operator signs a Merkle root over BLAKE3(record) leaves, and the batch is a log entry.</p>
<p><b>Source named, not hashed.</b> <code>sources[0]</code> names the two COG files by URL and carries no hash of them. So L3 is a re-read of the named pixel, not a hash check.</p>
</div>
<h2>1 · The record (${int(fact.length)} bytes, CBOR)</h2>
${table(['field', 'value in this record', 'bound by the name', 'binds the source file\'s bytes', 'ladder layer'], fieldRows)}
<p class="note">Not in the record: ${absentRows.map(([k, v]) => `<code>${esc(k)}</code> (${esc(v)})`).join('; ')}. The provenance class is declared per band in the bands manifest, not in the record. The request (the asked date, the question) is not stored.</p>
<h2>2 · The batch attestation (what is signed)</h2>
${table(['field', 'value', 'in the signed preimage'], attRows)}
<p class="note">Every field of the record is signed transitively: its hash is a leaf under <code>batch_root</code>. The pinned key is published under emem.dev in DNS TXT <code>_emem-node.emem.dev</code>, <code>did.json</code> and <code>jwks.json</code>; all are controlled by the operator of emem.dev.</p>
<h2>3 · The public log</h2>
${table(['object', 'value', 'read-only link'], logRows)}
<p class="note">These are the proofs the demo checks offline from the committed bundle (signed ${S.signed_at}). The links fetch fresh copies from emem.dev with GET. One organisation runs both the log and its only independent-tier witness today.</p>
<div class="slot" id="board-track">
<p><b>ARCHIVED BOARD TRACK</b></p>
<p>The earlier PDF at commit e66c3ba is a step of a signed emem track: 21 steps, every record the board rests on in panel order, then the print file (PDF at commit e66c3ba) as a pointer note. ememdemo re-checks all 21 in the browser and recomputes the chain to its head <code>ct2yz27kkkrh64emgdzs7bybgy</code>; the track is log entry 2,591,968.</p>
<p><a href="https://vortx-ai.github.io/ememdemo/?s=https%3A%2F%2Femem.dev%2Fmemories%2Fby_attester%2Fnjedkglt%2Fhepwyxdhiwckwi7qahkuvya2b4.md">Open the archived board track in ememdemo</a> · <a href="https://emem.dev/memories/by_attester/njedkglt/hepwyxdhiwckwi7qahkuvya2b4.md">the track note</a> · <a href="https://emem.dev/memories/by_attester/njedkglt/7jr4zw2tq7slvbsyzbyxxzwwii.md">the print's pointer note</a>. Signed by the poster key njedkglt; composer: <code>research/repro/v13/track/make_track_v13.py</code>.</p>
<p class="note">This track identifies that archived PDF. The current poster has new bytes; its file hash and build report are published in the repository. The archived signature does not attest the revised PDF.</p>
</div>
<h2>Check it yourself</h2>
<ul>
<li><a href="../demo/">VIEW THE DEMO</a>: your browser re-hashes these bytes, checks the attestation and the log, recomputes NDVI and re-reads the pixel.</li>
<li><a href="../t/">TRY A TOKEN</a>: one GET, one re-hash, one cell comparison. Or emem.dev's own checker: <a href="${esc(VERIFY_URL)}">emem.dev/verify</a>.</li>
<li>The raw bytes: <a href="https://emem.dev/v1/facts/${CID}">emem.dev/v1/facts/${CID.slice(0, 8)}…</a> (send <code>Accept: application/cbor</code>). <code>b3sum</code> of them, in base32, is the name above.</li>
<li>Offline, with no network: <a href="../test/#bundle">verify_bundle.py</a> runs the same nine checks in Python.</li>
</ul>
<h2>The ${int(fact.length)} bytes (hex)</h2>
<pre>${V.hex(fact).replace(/(.{64})/g, '$1\n')}</pre>
<p>A signature fixes these bytes. It does not make the measurement true. Whether the cell is the field you meant (L4), and whether the sensor and a decision taken on the value are right (L5), are outside what this record can show.</p>`));

// ------------------------------------------------------------------ RE-RUN THE TEST
const m2 = COST.m2_offline_verification, m3 = COST.m3_trace_read_only;
const r1s = R1.summary, r1levels = R1.meta.levels.map((l) => l.id);
w('test/index.html', page('test', 'RE-RUN THE TEST · EMEM', 'Exact commands to re-run every experiment on the EMEM poster.', 're-run the test', `
<h1>Re-run the test</h1>
<p class="lead">Every result on the poster comes from a script in the repository. Clone it once:</p>
<pre><code>git clone ${GH}
cd esa_poster
pip install blake3 cbor2 pynacl</code></pre>

<h2 id="r1">R1 · The mutation suite (offline, deterministic)</h2>
<pre><code>python research/repro/v11/mutation_suite.py</code></pre>
<p>${R1.meta.mutations.length - 1} corruptions and one control, at ${r1levels.length} verification depths (${r1levels[0]} prose to ${r1levels[r1levels.length - 1]} source re-read), on the real Keylong record. Rule: ${esc(R1.meta.rule)}. No network; the whole suite took ${R1.meta.suite_seconds} s in the committed run (${gitDate(R1_FILE)}). It rewrites <code>research/repro/v11/out/</code>; compare with the committed copy:</p>
${table(['depth', ...r1levels], [['acted on corrupted evidence', ...r1levels.map((l) => `${r1s[l].false_accepts}/${r1s[l].applicable}`)]])}
<p class="note">Source: ${src(R1_FILE)} and <a href="${blob('research/repro/v11/out/summary.md')}">summary.md</a>. Folder: <a href="${tree('research/repro/v11')}">research/repro/v11</a>.</p>

<h2 id="r5">R5 · Agent-to-agent handoff with language-model receivers</h2>
<p>R5 puts language-model receivers in Agent B's seat and hands them the same corruptions in seven representations, from prose to an EMEM token behind a fail-closed resolver. The design is on <a href="../methods/#r5">READ THE METHODS</a>.</p>
${R5_FINAL ? `<pre><code>python research/repro/v13/r5/analyze.py     # re-scores trials.jsonl and rewrites results.json and results.md</code></pre>
<p>${int(R5.n_trials_scored)} scored trials (${int(R5.n_pilot)} pilot trials and ${int(R5.n_excluded)} rows with no model output are excluded by the rules in the pre-registration), ${R5.dates.first_trial_utc.slice(0, 10)} ${R5.dates.first_trial_utc.slice(11, 16)} to ${R5.dates.last_trial_utc.slice(11, 16)} UTC. Pre-registration BLAKE3 <code>${R5.prereg_blake3.slice(0, 16)}…</code>, hashed at ${R5.dates.prereg_hashed_utc.slice(11, 16)} UTC before trial 1. Receivers: three Claude models (pooled) and one open-weight 7B model (apart); the model identifiers are in <a href="${blob('research/repro/v13/r5/results.md')}">results.md</a>.</p>
${table(['false acceptance, 3 Claude models pooled', 'A prose', 'B JSON', 'C retrieved text', 'D opaque id', 'E0 token, no instruction', 'E token, instructed check', 'E+ token, fail-closed'],
  [['agents (k/n)', ...['A', 'B', 'C', 'D', 'E0', 'E', 'E+'].map((c) => kn(R5.primary[c].pooled_claude.false_accept))],
   ['deterministic ceiling', ...['A', 'B', 'C', 'D', 'E0', 'E', 'E+'].map((c) => kn(R5.primary[c].ceiling.false_accept))]])}
<p class="note">Re-running the agents themselves costs money and time (USD ${fmt(R5.total_cost_usd_all_blocks, 2)} for every block including the pilot and re-runs): <code>run_claude.py</code> and <code>run_open.py</code> in <a href="${tree('research/repro/v13/r5')}">research/repro/v13/r5/</a> take the plan files there; <code>relay_server.py</code> is the adversary; every tool call is in <code>raw/</code>. Source: ${src(R5_FILE)} (${gitDate(R5_FILE)}).</p>` : `<p class="slot"><b>R5 RESULTS</b><br>R5 is being run now. Its pre-registration, scripts, raw trials and the one command to re-run them will appear in <a href="${tree('research/repro/v13/r5')}">research/repro/v13/r5/</a>. Until they are committed on <code>main</code>, that link shows "not found".</p>`}

<h2 id="trace">The 15-link trace (live)</h2>
<pre><code>python research/repro/v8/trace_fact.py --out=/tmp/trace</code></pre>
<p>Walks the Keylong token from the token to the pixel and the signer's domain: resolve, re-hash, cell binding, recompute, STAC metadata, the COG pixel, the SCL class, the byte-range witness, receipts, the log entry, inclusion, consistency and the key's publication (links 1 to 15, plus 9b and 9c). It took ${COST['m3_trace_read_only']['committed_2026-09-30_full_trace_s']} s in the committed run of 30 Sep 2026. A read-only variant took a median ${fmt(m3.keylong_ndvi.wall_s.median)} s over ${m3.keylong_ndvi.wall_s.n} runs on 1 Oct 2026 (${COST.measured_on}).</p>
<p class="note"><b>It calls live services.</b> Besides GETs, it sends POST <code>/v1/memory_token/resolve</code>, <code>/v1/range_hash</code> and <code>/v1/recall</code> to emem.dev; the last two sign and store records there. Add <code>--no-pixel</code> or <code>--no-log</code> to skip the slow links. Committed output: <a href="${blob('research/repro/v8/trace_fact_output.txt')}">trace_fact_output.txt</a>.</p>

<h2 id="bundle">The offline proof bundle (no network)</h2>
<pre><code>python research/repro/v8/verify_bundle.py research/repro/v8/proof_bundle_ndvi.cbor</code></pre>
<p>Nine checks on the ${int(bundleBytes.length)}-byte bundle: the record's hash, the batch root and its Ed25519 signature under the pinned key, the log leaf, inclusion under the signed head, the head's signature, the witness signature, its inclusion and its consistency with the head. Median ${fmt(m2.process_wall_unshare_rn_ms.median)} ms as a fresh process with networking removed (<code>unshare -rn</code>, n = ${m2.process_wall_unshare_rn_ms.n}, ${COST.measured_on}), of which ${fmt(m2.baseline_interpreter_plus_imports_ms.median)} ms is Python start-up.</p>

<h2 id="site">These pages</h2>
<pre><code>npm ci --prefix tools/site
python poster/build_site.py          # rebuild docs/ and the six QR codes
python poster/build_site.py --test   # plus the headless phone test</code></pre>
<p class="note">The demo's receiver runs in Node at build time and writes <a href="../demo/transcript.txt">transcript.txt</a>; the build fails if any verdict changes. Source: <a href="${tree('tools/site')}">tools/site</a>.</p>`));

// ------------------------------------------------------------------ READ THE METHODS
const st = (o) => `${o.n}`;
const iqr = (o, d) => (o.q1 !== undefined ? `${fmt(o.q1, d)} to ${fmt(o.q3, d)}` : '');
const P = m2.primitives_us, m1 = COST.m1_resolve_fact_https, m4 = COST.m4_source_reread, m5 = COST.m5_tokens.items, m6 = COST.m6_storage;
const costRows = [
  ['BLAKE3 of the 1,115 B record', st(P.blake3_fact_1115B), fmt(P.blake3_fact_1115B.median, 2), iqr(P.blake3_fact_1115B, 2), 'µs'],
  ['CBOR decode of the record (cbor2)', st(P.cbor2_loads_fact_1115B), fmt(P.cbor2_loads_fact_1115B.median), iqr(P.cbor2_loads_fact_1115B), 'µs'],
  ['one Ed25519 verify (pynacl)', st(P.ed25519_verify_pynacl), fmt(P.ed25519_verify_pynacl.median), iqr(P.ed25519_verify_pynacl), 'µs'],
  ['20-hash Merkle inclusion fold', st(P.inclusion_fold_20_hashes), fmt(P.inclusion_fold_20_hashes.median), iqr(P.inclusion_fold_20_hashes), 'µs'],
  ['every offline check, one decision (R1 level I)', st(m2.mutation_suite_ms_per_decision_by_level.I), fmt(m2.mutation_suite_ms_per_decision_by_level.I.median, 3), iqr(m2.mutation_suite_ms_per_decision_by_level.I, 3), 'ms'],
  ['verify_bundle.py, 9 checks, as a fresh process', st(m2.process_wall_unshare_rn_ms), fmt(m2.process_wall_unshare_rn_ms.median), iqr(m2.process_wall_unshare_rn_ms), 'ms'],
  ['GET /v1/facts/&lt;cid&gt; (CBOR), new connection', st(m1.cold_cbor_new_connection_ms), fmt(m1.cold_cbor_new_connection_ms.median), iqr(m1.cold_cbor_new_connection_ms), 'ms'],
  ['same, reused connection', st(m1.warm_cbor_reused_connection_ms), fmt(m1.warm_cbor_reused_connection_ms.median), iqr(m1.warm_cbor_reused_connection_ms), 'ms'],
  ['Planetary Computer SAS token GET', st(m4.sas_token_ms), int(Math.round(m4.sas_token_ms.median)), iqr(m4.sas_token_ms, 0), 'ms'],
  [`B08 tile #413 range read (${int(m4.b08_tile_bytes[0])} B)`, st(m4.b08_tile413_ms), int(Math.round(m4.b08_tile413_ms.median)), iqr(m4.b08_tile413_ms, 0), 'ms'],
  [`B04 tile #413 range read (${int(m4.b04_tile_bytes[0])} B)`, st(m4.b04_tile413_ms), int(Math.round(m4.b04_tile413_ms.median)), iqr(m4.b04_tile413_ms, 0), 'ms'],
  ['15-link trace, read-only variant', st(m3.keylong_ndvi.wall_s), fmt(m3.keylong_ndvi.wall_s.median), iqr(m3.keylong_ndvi.wall_s), 's'],
  ['one emem:fact token (cl100k_base)', '1', String(m5.fact_token.cl100k), '', 'tokens'],
  ['the value it names, 16 digits (cl100k_base)', '1', String(m5.value_16_digits.cl100k), '', 'tokens'],
  ['the fact as JSON (cl100k_base)', '1', String(m5.fact_json_as_served.cl100k), '', 'tokens'],
  ['fact records at the Keylong cell (CBOR)', st(m6.facts.bytes_all), int(m6.facts.bytes_all.median), iqr(m6.facts.bytes_all, 0), 'B'],
  ['offline proof bundle', '1', int(m6.proof_bundle_committed_bytes), '', 'B'],
];
const ladder = [
  ['L0 record integrity', 'Are these the exact bytes the pinned key attested and logged?', 'resolve, re-hash, attestation signature and batch root, log inclusion and consistency', 'CHECKABLE', 'M1, M2, M3, M7, M8 to M13, M16'],
  ['L1 observation identity', 'Does the record describe the cell, band and time I asked about?', 'record fields against the token and the question', 'CHECKABLE (declared fields)', 'M4, M5, M6'],
  ['L2 derivation', 'Does the value follow from the recorded inputs by the named function?', 'recompute from fn_key and args, compare IEEE-754 bits', 'RECOMPUTABLE where the inputs are in the record, else INHERITED', 'M14'],
  ['L3 source', 'Do the recorded inputs equal the named upstream file at the named pixel?', 're-read the pixel; catalogue metadata; byte-range witness', 'PARTIAL: no upstream hash is bound', 'M15 (only the re-read catches it)'],
  ['L4 entity', 'Is this cell the thing the sender meant?', 'none', 'OUT OF SCOPE', 'M17 accepted at every depth'],
  ['L5 truth, decision', 'Is the value right about the world, and is acting on it right?', 'none', 'OUT OF SCOPE (decision); INHERITED (product accuracy)', 'none'],
];
const threats = [
  ['T0 lossy channel', 'paraphrase, round, compact, truncate', 'L0 (resolve the token)'],
  ['T1 relay or forger without the pinned key', 'changes values, cells, dates, sources and references; replays old records; re-encodes and re-hashes; signs with its own key', 'L0, L1 (an entity swap, M17, is never caught)'],
  ['T2 the trusted signer errs or equivocates', 'wrong arithmetic, a wrong pixel, a wrong convention, a second version for one client', 'L2, L3, and the log if heads are shared'],
  ['T3 compromised signing key', 'signs anything', 'out of scope; for open data L2 and L3 still expose false values'],
  ['T4 upstream producer or mirror', 'wrong calibration, reprocessing under one name, mutable paths', 'L3 partly, and only against the archive'],
  ['T5 entity and semantics', 'the right record of the wrong thing', 'out of scope'],
  ['T6 receiver failure', 'a verifier bug, a model that skips the check, a tool that fails open', 'outside the protocol; independent verifier code and fail-closed tools'],
];
const prior = [
  ['STAC 1.1.0 / STAC API 1.0.0', 'What data exists, and where?', 'an asset (file) in an Item', 'the record names the STAC asset; it could copy <code>file:checksum</code> into its source hash'],
  ['openEO API 1.3.0', 'Compute this on that data.', 'a process graph or batch job', 'a process graph can be the recipe the record names'],
  ['W3C PROV-O / PROV-DM (2013)', 'How was this made?', 'entity, activity, agent', 'the derivation fields map to PROV terms'],
  ['C2PA 2.4', 'Who made or edited this file?', 'a media asset and its manifest', 'a rendered map could carry a manifest with the fact name (planned, not built)'],
  ['CDSE Traceability', 'Is this product the one ESA published?', 'a product zip', 'an upstream identity the record could name (not done today)'],
  ['RAG (Lewis et al. 2020)', 'Which context is relevant?', 'a text chunk', 'retrieval can return tokens instead of paraphrases'],
  ['MCP (2026-07-28)', 'How does an agent call a tool?', 'a tool call', 'EMEM is an MCP server; its token is a checkable handle'],
  ['A2A 1.0', 'Who is this agent?', 'an Agent Card, a task artifact', 'tokens travel inside artifact parts'],
  ['GeoGuard (2026)', 'Is this claim supported?', 'an atomic claim in text', 'its tools could return EMEM facts, so the evidence is re-checkable'],
  ['Sigstore, in-toto, SLSA 1.2', 'Who built and signed this artifact?', 'a software artifact digest', 'the same pattern, applied to observations'],
  ['RFC 6962 / 9162; SCITT RFC 9943', 'Was this logged, append-only?', 'a log entry', 'the EMEM log is RFC 6962-style with BLAKE3'],
  ['IPFS CID / multiformats', 'Which bytes?', 'bytes', 'EMEM exposes a CIDv1 with a BLAKE3 multihash'],
  ['FAIR, DOI, RDA data citation', 'How do I cite data reproducibly?', 'a dataset or a query subset', 'subset citation applied to one observation, checked by signature'],
];
const refs = [
  ['BLAKE3 specification', 'https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf'],
  ['RFC 8032, Edwards-Curve Digital Signature Algorithm (Ed25519)', 'https://www.rfc-editor.org/rfc/rfc8032'],
  ['RFC 8949, Concise Binary Object Representation (CBOR)', 'https://www.rfc-editor.org/rfc/rfc8949'],
  ['RFC 6962, Certificate Transparency', 'https://www.rfc-editor.org/rfc/rfc6962'],
  ['RFC 9162, Certificate Transparency Version 2.0', 'https://www.rfc-editor.org/rfc/rfc9162'],
  ['RFC 9943, SCITT architecture', 'https://www.rfc-editor.org/rfc/rfc9943'],
  ['STAC specification', 'https://github.com/radiantearth/stac-spec'],
  ['STAC file extension (file:checksum)', 'https://github.com/stac-extensions/file'],
  ['openEO API', 'https://github.com/Open-EO/openeo-api'],
  ['W3C PROV-DM', 'https://www.w3.org/TR/prov-dm/'],
  ['C2PA specification 2.4', 'https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html'],
  ['CDSE Traceability service', 'https://documentation.dataspace.copernicus.eu/APIs/Traceability.html'],
  ['Lewis et al. 2020, Retrieval-augmented generation for knowledge-intensive NLP tasks', 'https://arxiv.org/abs/2005.11401'],
  ['Model Context Protocol, specification versioning', 'https://modelcontextprotocol.io/specification/versioning'],
  ['A2A protocol specification', 'https://a2a-protocol.org/latest/specification/'],
  ['GeoGuard', 'https://github.com/NASA-IMPACT/geoguard'],
  ['Sigstore overview', 'https://docs.sigstore.dev/about/overview/'],
  ['in-toto attestation statement v1', 'https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md'],
  ['SLSA specification', 'https://slsa.dev/spec/'],
  ['multiformats CID', 'https://github.com/multiformats/cid'],
  ['Wilson 1927, Probable inference, the law of succession, and statistical inference (JASA 22:209)', 'https://doi.org/10.1080/01621459.1927.10502953'],
  ['emem source (Apache-2.0)', 'https://github.com/Vortx-AI/emem'],
  ['Sentinel-2 L2A on Planetary Computer', 'https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a'],
];
const pre = PREV.pre, post = PREV.post;
w('methods/index.html', page('methods', 'READ THE METHODS · EMEM', 'Methods behind the EMEM poster: the record, the verification ladder, the threat model, the experiments, the M15 sample, costs and references.', 'read the methods', `
<h1>Methods</h1>
<p class="lead">How the poster's claims were produced, and where each stops. Every number here is read by the build from the file named beside it; the date is the file's measurement or commit date (UTC).</p>
<p><a class="btn" href="../test/">Run the experiments</a> · <a href="../use/">Find an integration</a> · <a href="../t/">Resolve a token</a></p>
<h2>The complete system</h2>
<p>Observe → locate → record → hand off → resolve → check → continue. The lookup identity is cell, product and observation time. The content address identifies the exact canonical record. An <code>emem:fact:&lt;cell64&gt;:&lt;fact_cid&gt;</code> reference carries the cell and content address; the product and time are fields inside the record.</p>
<p>The two-process handoff in ${src(XRT_FILE)} passes the reference on stdout to a second program, which re-hashes the record, checks the receipt and recomputes NDVI. This is a measured program-to-program handoff, not a ChatGPT-to-Claude conversation.</p>
<p>Detailed figures: <a href="${blob('poster/fig/v13/f8_ladder_detail.svg')}">verification layers and measured coverage</a> · <a href="${blob('poster/fig/v13/f14_token_family.svg')}">token grammars and hash rules</a> · <a href="${blob('poster/fig/v13/f15_sat042.svg')}">SAT-042 reference harness</a>.</p>
<p>SAT-042 is a deterministic test harness, with no spacecraft enrolled. Its admission gate binds the output value digest. Code, model and run fields in the trace do not make that gate a full binding of those identities. The observation handoff does not depend on this extension.</p>
<h2 id="formalism">Drift, memory and the tests behind them</h2>
<pre><code>Δz = Δ_env + Δ_sensor + Δ_geo + Δ_encoder + ε
For finite output x and anchor a:
  d = |x − a|
  finite σ &gt; 0: r = d/(3σ); s = r/(1+r)
  invalid σ:    s = 0 if d = 0, otherwise 1
M = (O*, E*)            O = (a, b, t, v, u, p, s)
E = (subject, predicate, object, valid_from, valid_to)
Cτ = TxAsOf(O*, a, b, τ)
latest-as-of recall = max_(t,cid) {O in Cτ : t ≤ t*}</code></pre>
<p><b>Drift:</b> the reference can change during a handoff while the world stands still; a readout at a stable address can also change between visits. The decomposition names world, instrument, alignment, encoder and noise. The implemented attribution ledger associates per-term evidence with a signed receipt; its numeric split is null. The drift-anchor score is a separate disagreement measure. At 3σ it reaches 0.50 (tension); at 9σ it reaches 0.75 (contradicted). Invalid uncertainty includes zero, negative and non-finite σ; it requires exact agreement. The code variable z is renamed r to avoid confusing it with the readout in the decomposition.</p>
<p><b>Observation:</b> a is the cell, b the typed band, t the valid time, v the value, u the uncertainty, p the provenance (source references, recipe and signing time), and s the associated attestation. This is a conceptual model, not a wire schema: the tested fact record has no individual signature field. Its CID hashes the canonical record bytes; a batch attestation covers the address, and a read receipt separately binds the response. Missing source hashes or uncertainty do not appear merely because the conceptual model names them.</p>
<p><b>Two clocks:</b> TxAsOf resolves the versions known at signing-time bound τ per cell, band and valid-time slot. In latest-as-of mode, with no exact tslot, recall then selects the latest qualifying valid time ≤ t*, with lexicographic CID order breaking ties; an empty candidate set returns no observation. Exact-slot, unbounded and provenance-filtered reads have their own semantics. The Bengaluru example returns 918.0 m at a 15 June signing-time bound and 915.07 m after a provider change. Both records remain citable. Temporal storage and event sourcing are established techniques; the agent-handoff implication is a portable reference to the exact historically cited record, with receiver-side checks. This does not demonstrate physical ground movement.</p>
<p><b>Memory operations:</b> recall and diff recover states and compare visits; merge creates a citable set, not an averaged measurement; trace follows versioned recipes and cited inputs; competing retains contradictory evidence; evolve appends and supersedes; ensure reuses or materialises a missing single-hop read; valid assesses product-dependent staleness. Multi-hop planning and causal removal/recomputation remain open. Complete recovery and source notes: ${src('research/v13/22_RECOVERED_DESIGN_AND_FORMALISM.md')}.</p>
<p>Model-output records preserve the metadata actually present. The archived Prithvi vector has 1,024 values and a checkpoint digest inside the hashed record. TESSERA has 128 values and a product-year path, with no checkpoint digest. These encoder bands are retired on the deployment; the poster shows retained records, not current inference. Evidence: ${src('research/v13/evidence/critic/cell.json')}.</p>
<p><b>Fresh upstream tests:</b> ${FORMAL.passed} passed, ${FORMAL.failed} failed, ${FORMAL.skipped} skipped on ${FORMAL.date}, at emem <code>${FORMAL.commit.slice(0,7)}</code>. These are the existing SDK offline receipt and benchmark canonical-encoding tests, run without changes. They accept a genuine receipt and reject changed addresses, request ids, clocks, primitives and Merkle proofs; canonical vectors exercise floats, booleans and CID changes. Results: ${src(FORMAL_FILE)}, ${src('research/v13/evidence/formalism/offline_tests.txt')}. Exact source files, hashes and commit links: ${src('research/v13/evidence/formalism/sources.json')}.</p>
<p><b>Archived Rust tests:</b> the 30 September emem-trace run at <code>04b40c5</code> has 22 passed and one deliberately ignored timing test. It includes drift thresholds, missing uncertainty, trace chaining, output binding and signature rejection. The separately filtered storage run has 23 passed. These are retained results, not fresh executions here: ${src('research/repro/v12/trace/emem_trace_tests.txt')}. The temporal tests at the current pinned commit exercise both time bounds, their intersection, empty results and historical reads. Their source was inspected; Rust is not installed in this build environment, so no new Rust result is claimed.</p>
<p><b>Next experiments:</b> use controlled scene, pixel and encoder changes to test numeric attribution, wire device outputs to recalled Earth anchors, and repeat checked handoffs between separately operated agent hosts. The current two-process result does not establish a cross-host agent conversation. Restoration decisions and remaining scope: ${src('research/v13/16_FORMALISM_AND_TEST_AUDIT.md')}.</p>
<h2>Research questions behind the experiments</h2>
<p>Can a receiver detect altered evidence without trusting the sender? Which changes become visible at each verification depth? How do prose, JSON, retrieval, an opaque id and a checked reference compare? What remains inherited when the cited record is intact? The experiments below separate these questions from the poster's explanatory flow.</p>

<p class="note">Contents: <a href="#record">record</a> · <a href="#ladder">ladder</a> · <a href="#threat">threat model</a> · <a href="#r1">R1</a> · <a href="#r5">R5</a> · <a href="#m15">M15 sample</a> · <a href="#demo">demo</a> · <a href="#cost">cost</a> · <a href="#prior">prior art</a> · <a href="#refs">references</a></p>

<h2 id="record">1 · The record and its content address</h2>
<p>An EMEM fact is one observation record: cell, band, UTC day (tslot), value, confidence, sources (scheme, id or URL, capture time), derivation (function key and arguments such as scene id, EPSG code, DNs, BOA offset and catalogue), privacy class, schema cid, signer and signing time. It is encoded as CBOR. Its name is</p>
<pre><code>fact_cid = base32(BLAKE3-256(record bytes))     52 characters</code></pre>
<p>A token adds the cell: <code>emem:fact:&lt;cell&gt;:&lt;fact_cid&gt;</code>. The record has no signature of its own. The operator's key signs <code>PreimageV1("attestation"){batch_root, registry_cid, schema_cid}</code>, where <code>batch_root</code> is a Merkle root over the BLAKE3 hashes of a batch of records, and the attestation is an entry in an RFC 6962-style log. The record names its upstream file by scene id and URL and binds none of its bytes, so a receiver checks the source by re-reading it. Field by field: <a href="../r/">INSPECT THE RECORD</a>.</p>
<p class="note">A receiver must hash the bytes it received. Decoding and re-encoding with a generic CBOR library gives other bytes and would refuse every genuine record (report 09, §3.2).</p>

<h2 id="ladder">2 · The verification ladder</h2>
<p>"Verified" is never used alone. Each check names its layer.</p>
${table(['layer', 'question', 'check', 'status', 'R1 first refusal'], ladder)}
<p class="note">Status words: CHECKABLE (decided offline with stock libraries), RECOMPUTABLE (re-executed or re-read and compared bit for bit), INHERITED (rests on the signer or the producer), PARTIAL, OUT OF SCOPE. Source: ${src('research/v13/10_ladder_threat_invention.md')} §3 (${gitDate('research/v13/10_ladder_threat_invention.md')}).</p>

<h2 id="threat">3 · Threat model</h2>
${table(['party', 'can do', 'stopped at'], threats)}
<p>Out of scope: a compromised signer, an incorrect sensor or product, substitution where the archive is not open or not immutable, entity mistakes, decision correctness, availability, and completeness of the log.</p>
<p>Trust is one organisation deep today. emem.dev and its only independent-tier witness (geo.qa) are both run by Vortx AI; <code>/v1/log/witnesses</code> reported <code>independent_operator_count: 1</code> and <code>head_is_independently_witnessed: false</code> on 2026-10-01 at 01:02Z. The key is bound to the domain by Web PKI and DNS without DNSSEC.</p>

<h2 id="r1">4 · R1, the mutation suite</h2>
<p>One real record (the Keylong NDVI record above), its attestation, signed tree head, inclusion path and witness, and the 5 × 5 DN windows re-read from the public COGs. Question: NDVI at cell <code>${R1.meta.question.cell}</code>, tslot ${R1.meta.question.tslot}. Rule: ${esc(R1.meta.rule)}. ${R1.meta.mutations.length - 2} in-scope corruptions (M1 to M16), one control (G0) and one out-of-scope entity case (M17), each at nine depths: A prose, B structured record, C opaque id, D + re-hash, E + cell, band and tslot binding, F + Ed25519 under the pinned key, G + log inclusion, H + recompute, I + source re-read. Signer errors (T2) use a TEST key derived from a public string; nothing is signed with emem's key.</p>
${table(['depth', ...r1levels], [['acted on corrupted evidence', ...r1levels.map((l) => `${r1s[l].false_accepts}/${r1s[l].applicable}`)]])}
<p class="note">The control is never refused. One full level-I check took ${R1.meta.full_verification_ms} ms offline. The verifier is code, not a model, and "0 of 16" is a property of this suite: three signer errors outside it (an offset recorded as 0, a relabelled same-day scene, a wrong unit) pass every check D to I (report 10, §3.4). Source: ${src(R1_FILE)} (${gitDate(R1_FILE)}).</p>

<h2 id="r5">5 · R5, agent-to-agent handoff</h2>
<p>A receiving agent B makes one threshold decision from evidence handed over by agent A. Between them an adversary applies one of 24 enumerated corruptions (R1's ids plus new ones tied to real incidents). Each is rendered in seven representations: A prose, B structured JSON, C retrieved context, D opaque id, E0 EMEM token with tools and no instruction, E token with an instructed check, E+ token behind a fail-closed resolver. The primary endpoint is false acceptance: B acts on corrupted evidence. Secondary endpoints include false refusal of the genuine record, whether the check was run and bound to B's own question, and cost. Intervals are Wilson 95 %, with a cluster bootstrap over items. Receivers are language models from two families, one through an MCP client and one local; the exact models and versions are in the pre-registration.</p>
${R5_FINAL ? `<h3>Results (final, ${R5.dates.analysed_utc.slice(0, 10)})</h3>
<p>Primary endpoint, three Claude models pooled over the primary items, with Wilson 95 % intervals: prose ${knp(R5.primary.A.pooled_claude.false_accept, R5.primary.A.pooled_claude.wilson95)}; JSON ${knp(R5.primary.B.pooled_claude.false_accept, R5.primary.B.pooled_claude.wilson95)}; retrieved text ${knp(R5.primary.C.pooled_claude.false_accept, R5.primary.C.pooled_claude.wilson95)}; opaque id ${knp(R5.primary.D.pooled_claude.false_accept, R5.primary.D.pooled_claude.wilson95)}; EMEM token with the tool and no instruction ${knp(R5.primary.E0.pooled_claude.false_accept, R5.primary.E0.pooled_claude.wilson95)}; token with an instructed check ${knp(R5.primary.E.pooled_claude.false_accept, R5.primary.E.pooled_claude.wilson95)}; token behind a fail-closed resolver ${knp(R5.primary['E+'].pooled_claude.false_accept, R5.primary['E+'].pooled_claude.wilson95)}. The deterministic verifier on the same items: ${['A', 'B', 'C', 'D', 'E0', 'E', 'E+'].map((c) => kn(R5.primary[c].ceiling.false_accept)).join(', ')}. Within each Claude model, E below A, B, C and D each by a one-sided Fisher exact test with Holm correction (every adjusted p below 0.01; table in results.md).</p>
<p>The open-weight 7B model, one replicate, conditions A, B, E and E+: ${['A', 'B', 'E', 'E+'].map((c) => `${c} ${kn(R5.open_models['qwen2.5-7b-instruct-q4_k_m'][c].false_accept)}`).join(', ')}. A token protects a receiver that calls the check, binds it to its own question and obeys a refusal; this one dropped the token's prefix and acted on refusals.</p>
<p>Live block (emem MCP, real records): with no instruction agents acted on corrupted evidence in ${kn(R5.block2_pooled.L0.fa_inscope)} in-scope trials, instructed to resolve and bind ${kn(R5.block2_pooled.L1.fa_inscope)}, with our source re-read ${kn(R5.block2_pooled.L2.fa_inscope)}; the real pre-fix record (the wrong pixel, panel 6 of the board) passed 4/4, 2/4 and 0/4 (one-sided Fisher p = 0.214). Controls were correct ${kn(R5.block2_pooled.L0.control_correct)}, ${kn(R5.block2_pooled.L1.control_correct)} and ${kn(R5.block2_pooled.L2.control_correct)}: the instructed receiver refused a genuine record twice because the live resolve body carries no scene date.</p>
<p class="note">Deviations and adverse results, in full in results.md sections 9 and 10: ${int(R5.n_excluded)} trial rows returned a CLI rate-limit message and no model output (06:31 to 06:40 UTC); they are marked excluded and every affected trial was re-run after the limit reset. Replicates per Claude model followed the pre-registered cost rule (${Object.values(R5.cells.A.M1.per_model).map((v) => v.n).join(', ')} runs per model, ${Object.values(R5.cells.A.M1.per_model).reduce((t, v) => t + v.n, 0)} per cell). The second model family is one open model; three further open models were downloaded but not run. A value the receiver recomputed from the record's own DNs is credited (scoring addendum 1, hashed before the Claude blocks; the original rule is a sensitivity row). JSON and the opaque id caught about half the corruptions by reading the fields they carry. The thresholds are constructed next to the genuine values; two records, two places, three bands; the three pooled models share a vendor; relay, verifier, corpus and scorer were written by the same team. Pre-registration: ${src('research/repro/v13/r5/prereg.md')} (BLAKE3 <code>${R5.prereg_blake3.slice(0, 16)}…</code>). Results: ${src('research/repro/v13/r5/results.md')}, ${src(R5_FILE)} (${gitDate(R5_FILE)}), ${src('research/repro/v13/r5/trials.jsonl')}.</p>` : `<p class="slot"><b>R5 STATUS</b><br>Running now. Results, pre-registration and scripts will appear in <a href="${tree('research/repro/v13/r5')}">research/repro/v13/r5/</a>. No R5 number is printed until then. Design: ${src('research/v13/02_experiment_design.md')}.</p>`}

<h2 id="m15">6 · M15, the right record and the wrong pixel</h2>
<p>Before 2026-09-28 04:09:26Z emem's COG reader rounded the fractional pixel position; GDAL takes the floor. For each sampled record the audit re-reads both candidate pixels from the named files and asks which one the signed DNs match.</p>
<ul>
<li>Sampling: <a href="${blob('research/v13/evidence/g1_pixel_audit/prevalence.py')}"><code>prevalence.py</code></a>, <code>random.Random(20261019)</code>, one record per cell, from the Sentinel-2 point facts cited in <code>emem.dev/channel.json</code>.</li>
<li>Pre-fix sample: n = ${pre.n} records over ${pre.cells} cells and ${pre.scenes} scenes, ${Object.keys(pre.bands).length} bands, providers ${Object.entries(pre.providers).map(([k, v]) => `${k} ${v}`).join(', ')}, signed ${pre.signed_at_range[0].slice(0, 10)} to ${pre.signed_at_range[1].slice(0, 10)}.</li>
<li>Result: <b>${pre.matches_round_not_floor} of ${pre.n}</b> match the rounded pixel and not the floor pixel; ${pre.floor_equals_round_pixel} have equal DNs under both rules; ${pre.matches_floor_not_round} match only the floor. Wilson 95 %: ${pct(pre.frac_round_wilson95[1])} to ${pct(pre.frac_round_wilson95[2])}.</li>
<li>After the fix: ${post.matches_round_not_floor} of ${post.n} (Wilson upper bound ${pct(post.frac_round_wilson95[2])}), ${post.matches_floor_not_round} match only the floor. All post-fix records come from one provider, so the comparison is provider-confounded.</li>
<li>For the Keylong cell the rounded pixel is the one 10 m south: NDVI ${SOUTH.toFixed(4)} instead of ${rec.value.toFixed(4)}.</li>
</ul>
<p class="note">Every check at L0 to L2 accepts such a record. Only the L3 re-read catches it. Source: ${src(PREV_FILE)} (${gitDate(PREV_FILE)}), same values as <code>research/repro/data/v8/prevalence_summary.json</code>.</p>

<h2 id="demo">7 · What the demo shows, and what it does not</h2>
<ul>
<li>It is a scripted harness written by the authors. The receiver is code, not a language model. The mutations are authored and named as in R1. The record, its signature, its log proofs and the source pixels are real.</li>
<li>It covers one record, one cell and one band. It is not the 16-mutation suite.</li>
<li>M8 is refused because the page holds the signed batch for this observation. A real receiver would look the forged name up and get a 404; the optional live mode checks that response.</li>
<li>The L3 tile hashes it compares come from the poster team's trace of 30 Sep 2026, not from the signer: the record carries no source hash.</li>
</ul>

<h2 id="cost">8 · Cost</h2>
${table(['operation', '#n', '#median', 'IQR', 'unit'], costRows)}
<p class="note">Measured ${esc(COST.measured_on)} on ${esc(COST.environment.client_host)}. Network rows pass through a TLS-re-terminating egress proxy, so a phone will differ. Source: ${src(COST_FILE)}; method: ${src('research/v13/08_cost_overhead.md')}.</p>

<h2 id="prior">9 · Prior art: what each layer answers</h2>
<p><a href="../questions/">Short reviewer answers with evidence</a></p>
<p>Adjacent systems find files, run workflows, record lineage, sign files, retrieve context, carry calls and judge claims. EMEM names the one observation an agent cited and lets the next agent re-check it. It relies on those layers and replaces none.</p>
${table(['system', 'question it answers', 'unit it identifies', 'where EMEM sits'], prior)}
<p class="note">Source: ${src('research/v13/04_prior_art_and_field.md')} §1.3 (versions as checked on 2026-10-01).</p>

<h2 id="recovered">Recovered demonstrations from earlier posters</h2>
<p>These archived experiments add breadth to the focused handoff test on the A0 poster. Their original evidence and dates stay attached.</p>
<h3>Two seasons at one field</h3>
<p>Keylong, India: 141 Sentinel-2 NDVI records from January 2025 to September 2026. The records name the scene and observation time, so a later agent can recover the measurement used in a seasonal comparison. ${src('research/repro/v12/data/case_keylong_ndvi.json', 'Evidence')}.</p>
<img class="recovered" src="../assets/recovered_keylong.svg" alt="Archived v12 Keylong seasonal NDVI series, with scene and source context">
<h3>A reproducible forest-loss screen</h3>
<p>Rondônia, Brazil: 100 sampled point cells and 600 facts, read on 30 September 2026. The screen combines forest status and loss year; it is a sampled evidence workflow, not a determination of legal compliance. The source-pixel audit in the main methods shows why the reading rule still matters.</p>
<img class="recovered" src="../assets/recovered_rondonia.svg" alt="Archived v12 Rondônia forest and loss-year evidence over sampled cells">
<p>${src('research/should_do/19_V12_CLAIMS_MAP.md', 'Original v12 claim and evidence map')} · ${src('research/repro/v12/data/case_rondonia_eudr.json', 'Rondônia example records')}.</p>
<h3>Execution evidence: SAT-042</h3>
<p>A scripted reference-harness run, not a spacecraft. The trace binds recorded steps and outputs; the drift anchor scores disagreement. Hardware enrolment and live device-to-anchor wiring remain separate work.</p>
<img class="recovered" src="../assets/recovered_sat042.svg" alt="Archived SAT-042 scripted execution trace and its checks">
<p>${src('research/repro/v12/trace/trace_truth.md', 'Trace evidence and scope')}.</p>
<h3>Bundles, state checkpoints and absence</h3>
<p>The eight-record bundle, four reproduced state hashes and Berlin coverage absences are restored to the poster face. ${src('research/v13/18_RECOVERED_CONTRIBUTIONS_AND_COMMUNITY.md', 'Version-by-version recovery map')} · ${src('research/v13/evidence/community/recovery_checks.json', 'Fresh offline checks')}.</p>
<style>.recovered{display:block;max-width:100%;height:auto;margin:18px 0;border:1px solid var(--rule)}</style>
<h2 id="refs">10 · References</h2>
<ol>${refs.map(([t, u]) => `<li>${esc(t)}. <a href="${esc(u)}">${esc(u.replace(/^https:\/\//, ''))}</a></li>`).join('')}</ol>`));

// ------------------------------------------------------------------ DISCOVER INTEGRATIONS (generated from the manifest)
const GROUPS = [
  ['Agent hosts', ['agent host']],
  ['Interoperability', ['protocol', 'protocol surface']],
  ['Discovery', ['registry', 'directory', 'mirror', 'landing page']],
  ['Developer', ['sdk', 'self-host', 'source']],
  ['Frameworks', ['framework example']],
  ['Workflow templates', ['workflow']],
];
const roles = new Set(GROUPS.flatMap(([, r]) => r));
for (const r of ECO) if (!roles.has(r.role)) throw new Error('ecosystem row with an unmapped role: ' + r.id + ' ' + r.role);
const STATUS = ['LIVE', 'PROTOCOL', 'REGISTRY', 'EXAMPLE', 'EXPERIMENTAL', 'ROADMAP', 'NOT FOUND'];
for (const r of ECO) if (!STATUS.includes(r.status)) throw new Error('unknown status ' + r.status + ' in ' + r.id);
const GHMARK = '<svg class="mark" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>';
const allowed = (r) => r.print && r.print.allowed === true;
const how = (r) => { const t = (r.print && r.print.text) || ''; const i = t.indexOf(': '); return t && !t.startsWith('(') && i > 0 ? t.slice(i + 2) : ''; };
const item = (r) => {
  const mark = r.id === 'github-repo' ? GHMARK : '';
  const line = how(r);
  const board = ''; // Print placement is an editorial decision, not a user-facing capability.
  return `<li class="int" id="${esc(r.id)}">
<p><span class="chip ${r.status.replace(' ', '')}">${esc(r.status)}</span> <b>${mark}${esc(r.platform)}</b></p>
${line ? `<pre><code>${esc(line)}</code></pre>` : ''}<p class="note"><a href="${esc(r.url)}">${esc(r.url.replace(/^https:\/\//, '').slice(0, 90))}${r.url.length > 98 ? '…' : ''}</a></p>
<p>${esc(r.user_can)}.</p>
<p class="note">Evidence: ${esc(r.evidence_level)}. Checked ${esc(r.verified_utc)}. ${esc(board)}.</p>
${r.caveats && r.caveats.length ? `<details><summary>Caveats (${r.caveats.length})</summary><ul>${r.caveats.map((c) => `<li>${esc(c)}</li>`).join('')}</ul></details>` : ''}
</li>`;
};
const counts = Object.fromEntries(STATUS.map((s) => [s, ECO.filter((r) => r.status === s).length]));
let xrt = '';
if (XRT && XRT.summary) {
  const sm = XRT.summary.ndvi_keylong || Object.values(XRT.summary)[0];
  if (sm && sm.paths_run !== undefined) xrt = `<h2>Same token, many runtimes</h2><p>The Keylong token resolved through ${sm.paths_run} client paths (REST, raw MCP, A2A, two SDKs, framework adapters, the official MCP SDKs and an independent blake3 and cbor2 reader): ${sm.paths_ok} of ${sm.paths_run} succeeded, with ${[].concat(sm.distinct_fact_cids).length} distinct record name and ${[].concat(sm.distinct_values).length} distinct value, run ${String(XRT.generated_utc || '').slice(0, 16).replace('T', ' ')} UTC. Model-in-the-loop handoffs between two agent hosts are not shown here. Source: ${src(XRT_FILE)}.</p>` + table(['Client path', 'Time (ms)', 'Record re-hashed', 'Receipt signature checked'], XRT.rows.ndvi_keylong.map(r => [esc(r.path === 'A->B_isolated_processes' ? 'A to B, isolated processes (one run)' : r.path.replace(/^[0-9][a-z]?_/, '').replaceAll('_', ' ')), String(r.ms_median ?? r.ms), r.rehash_ok ? 'yes' : 'no', r.receipt_sig_ok ? 'yes' : 'not checked here']));
}
const platform = (id) => ECO.find((r) => r.id === id);
const link = (id, label) => `<a href="${esc(platform(id).url)}">${esc(label || platform(id).platform)}</a>`;
const prompt = `Resolve this emem token. Return its exact value_verbatim, band, cell, observation date and source references. Check the record hash and receipt using the available verifier; say which checks actually ran. Keep the token unchanged for the next agent.

${TOKEN}`;
const connectCards = [
  ['ChatGPT', `${link('chatgpt', 'Open the emem plugin')} and enable it. Mention <b>@emem</b>, then paste the example below.`, 'The connected plugin exposes emem_memory_token_resolve.'],
  ['Claude', `Add the MCP server in Claude.ai, or install the Claude Code plugin with its procedures. ${link('claude-code-plugin', 'Plugin instructions')}.`, `<pre><code>/plugin marketplace add Vortx-AI/emem
/plugin install emem@emem</code></pre><p>Direct MCP setup:</p><pre><code>claude mcp add --transport http emem https://emem.dev/mcp</code></pre>`],
  ['Visual Studio Code', `${link('vscode', 'Install the MCP integration')} for Copilot agent mode, or search <code>@mcp emem</code> in the MCP gallery.`, `<pre><code>code --add-mcp '{"name":"emem","type":"http","url":"https://emem.dev/mcp"}'</code></pre>`],
  ['Dify', `${link('dify-marketplace', 'Install the Marketplace plugin')}, then import a workflow template.`, `<ul><li>${link('dify-template-lite', 'Referent Lock Lite')}</li><li>${link('dify-template-full', 'Referent Lock Full')}</li><li>${link('dify-template-eudr', 'EUDR Evidence Studio')}</li></ul><p class="note">The EUDR template is an evidence pre-screen; it does not itself establish legal compliance.</p>`],
  ['Salesforce MuleSoft', `${link('mulesoft-exchange', 'Open Vortx AI MCP Server on Anypoint Exchange')}. The asset describes the emem MCP server for flow builders.`, '<pre><code>https://emem.dev/mcp</code></pre><p class="note">A published MCP asset. A MuleSoft flow was not executed in this study.</p>'],
];
w('use/index.html', page('use', 'CONNECT AND BUILD · EMEM', 'Use emem from ChatGPT, Claude, Visual Studio Code, Dify or Salesforce MuleSoft. Copy a token, check the record and try a handoff.', 'connect and build', `
<h1>Bring the evidence into your workflow.</h1>
<p class="lead">Choose a plugin, a workflow or your own code. Start with the saved observation below, then hand its reference to another agent. Public emem reads need no API key. The implementation is Apache-2.0.</p>
<p><a class="btn" href="../demo/">Try the browser demo</a> · <a href="../methods/">Methods and reproduction</a> · <a href="../methods/#recovered">Recovered demonstrations</a></p>
<h2>1 · Connect your tool</h2>
<div class="setup-grid">${connectCards.map(([name,how,detail]) => `<section class="setup"><h3>${name}</h3><p>${how}</p><div>${detail}</div></section>`).join('')}</div>
<h2>2 · Copy a real handoff</h2>
<p>Paste this into a connected agent. Give the same token to a second agent or a new session. Compare the record identity and the checks performed.</p>
<label for="handoff" class="note">Prompt and unchanged token</label>
<textarea id="handoff" rows="8" spellcheck="false">${esc(prompt)}</textarea>
<p><button id="copy-handoff" class="btn" type="button">Copy prompt and token</button> <span id="copy-status" role="status" aria-live="polite"></span></p>
${table(['Compare', 'Expected from the saved record'], [
 ['Exact value', `<code>${esc(String(rec.value))}</code>`],
 ['Band and unit', `<code>${esc(rec.band)}</code>; dimensionless`],
 ['Place', `<code>${esc(tok.cell)}</code>; Keylong, Lahaul, India`],
 ['Observation', '25 Sep 2026; Sentinel-2 L2A'],
 ['Content identity', `<code>${esc(CID)}</code>`],
 ['Checks', 'Re-hash the canonical record; bind its place, band and time; verify the receipt or batch under the expected key. A source re-read is a further check.'],
])}
<p><b>Success means:</b> the next agent recovers the same record and exact value, preserves the citation and reports the checks it performed. Asking for a new “latest” observation is a different task. If a tool call fails, report that failure; the <a href="../demo/">saved offline demo</a> still lets you inspect and verify the example.</p>
<details><summary>What was checked in this round?</summary><p>The public ChatGPT emem listing (Developer Vortx.ai), Dify plugin and three templates, GitHub MCP, MuleSoft Exchange and ClawHub pages returned HTTP 200 on 2 October 2026. ChatGPT's plugin and resolve tool are also connected in this workspace; two resolve attempts returned a connector-level “Unexpected response type” error. They are not counted as successful agent runs. VS Code configuration and the Claude plugin install commands were checked against the source. No new VS Code, Claude, Dify or MuleSoft host execution is claimed. ${src('research/v13/evidence/community/listing_checks.json', 'Link checks')} · ${src('research/v13/evidence/community/chatgpt_plugin_check.json', 'Connected plugin check')}.</p></details>
<h2>3 · Build with the same reference</h2>
${table(['Route', 'Start here'], [
 ['MCP', '<code>https://emem.dev/mcp</code>'],
 ['Agent2Agent', link('a2a', 'Read the A2A agent card')],
 ['REST', `<a href="https://emem.dev/openapi.json">OpenAPI</a> · <a href="https://emem.dev/v1/facts/${CID}">Read the example record</a>`],
 ['Python', '<code>pip install ememdev</code>'],
 ['TypeScript', '<code>npm i @vortxai/emem</code>'],
 ['LangGraph memory', '<code>pip install emem-langmem</code>'],
 ['Self-host', '<code>docker run -p 5051:5051 ghcr.io/vortx-ai/emem:latest</code>'],
 ['Other clients', `${link('cursor', 'Cursor')} · <a href="#gemini-cli">Gemini CLI setup</a> · <a href="https://github.com/Vortx-AI/emem/tree/main/examples">Framework examples</a>`],
])}
<h2>Questions the poster opens</h2>
<p><a href="../questions/">Read the conference Q&amp;A</a>: invention, prior art, trust, model scope and next experiments.</p>
<details><summary>What is in the token, and what stays upstream?</summary><p>The fact token carries a lookup cell and a full content identifier. The record behind it contains the value, time, derivation and source references. Large source scenes remain upstream. Cell, product and time find candidate observations; the fact CID identifies the exact record used.</p></details>
<details><summary>What do a hash, signature and source check establish?</summary><p>The hash checks record identity. Binding checks that the record answers the requested place, product and time. A receipt or batch attestation checks a statement under a particular key. A declared derivation can be recomputed, and the named upstream source can be re-read. These checks do not establish a sensor's accuracy, an entity's meaning or the correctness of a downstream decision.</p></details>
<details><summary>What happens when data is missing or later changes?</summary><p>A typed absence can name a coverage or quality reason instead of inventing a value. New records can coexist with earlier content addresses. Recall can bound both observation time and signing time. The archived Bengaluru example answers 918.0 m as of 15 June, before a later provider returned 915.07 m; that difference alone is not ground movement.</p></details>
<details><summary>Can I carry more than one reading or resume an investigation?</summary><p>The archived bundle groups eight fact references in one 38-character handle. The member records have their own identities and checks. Reasoning stages can also carry state addresses: the saved located, routed, recalled and scored states reproduce from their published fields. Signed agent notes can preserve working context separately from source observations. ${src('research/v13/evidence/community/recovery_checks.json', 'Offline reproduction')}.</p></details>
<details><summary>Can I use the foundation-model embeddings?</summary><p>The poster includes stored Prithvi and TESSERA vectors. Those deployed encoders are retired: the old records remain addressable, while new embedding generation is not demonstrated. Prithvi records a checkpoint digest; the archived TESSERA example records a product year. Preserve that distinction when comparing models.</p></details>
<details><summary>Can verification work offline? What if the server disappears?</summary><p>Keep the record bytes, expected signer key, receipt or attestation and required log proofs. The saved browser demo checks its retained evidence locally; it does not need the live responder. A content address establishes identity, not future availability. Retain the evidence you need and choose your own storage and trust policy.</p></details>
<details><summary>Who can write, and how does this relate to other EO tools?</summary><p>Public reads do not grant authority to publish canonical observations. Writes follow signer and admission rules; agent-authored notes remain distinct from observations. STAC discovers assets, openEO describes processing, and PROV/C2PA carry provenance. EMEM adds the observation reference that can pass between agents. The methods explain the verification boundary.</p></details>
<h2>What the community can test next</h2>
<ul><li><b>Independent host handoff:</b> run the same saved token through ChatGPT, Claude, Dify and another separately operated host. Record exact values, CIDs, checks, failures and latency.</li><li><b>Attribution:</b> vary the scene, pixel, sensor or encoder separately; compare the drift score with the known cause. The decomposition is a model, not an already fitted numeric split.</li><li><b>Long-lived evidence:</b> retain records, receipts and log proofs; replay them after a context reset, provider update or endpoint outage.</li></ul>
<p><a class="btn" href="../methods/">Read and reproduce the research</a> · <a href="${GH}">Poster source</a> · <a href="https://github.com/Vortx-AI/emem">Build or contribute to emem</a></p>
${xrt}
<h2>Complete integration directory</h2>
<p class="note">Plugins, connectors, packages, listings and repository examples have different setup paths. Expand a group for its source, current status and compatibility notes. Framework adapters may require the versions or fixes documented there.</p>
${GROUPS.map(([g,rs])=>{const rows=ECO.filter((r)=>rs.includes(r.role));return `<details><summary>${esc(g)} (${rows.length})</summary><ul class="ints">${rows.map(item).join('')}</ul></details>`}).join('')}
<script>document.getElementById('copy-handoff').addEventListener('click',async()=>{const t=document.getElementById('handoff');try{await navigator.clipboard.writeText(t.value);document.getElementById('copy-status').textContent='Copied.';}catch{t.focus();t.select();document.getElementById('copy-status').textContent='Select and copy the highlighted prompt.';}});</script>`, {
  head: `<style>.setup-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}.setup{border:1px solid var(--rule);border-radius:10px;padding:16px;background:var(--card)}.setup h3{margin-top:0}.setup p{margin:8px 0}.setup pre{white-space:pre-wrap;overflow-wrap:anywhere}#handoff{width:100%;padding:12px;border:1px solid var(--rule);border-radius:8px;font:14px/1.5 var(--mono)}.ints{list-style:none;padding:0}.int{border-top:1px solid var(--rule);padding:12px 0}.int p{margin:0 0 6px}details{padding:10px 0;border-bottom:1px solid var(--rule)}summary{cursor:pointer;font-weight:600}details details{border:0}code{overflow-wrap:anywhere}</style>` }));

const QA = rj('research/v13/conference_questions.json');
for (const q of QA.questions) {
  if (!q.status || !q.sources.length) throw new Error('Reviewer answer without status/source: '+q.question);
  for (const s of q.sources) {
    const prefix='https://github.com/Vortx-AI/esa_poster/blob/main/';
    if (s.url.startsWith(prefix) && !fs.existsSync(path.join(ROOT,s.url.slice(prefix.length)))) throw new Error('Missing reviewer evidence: '+s.url);
  }
}
w('questions/index.html', page('questions', 'Conference questions · EMEM', 'Short answers about evidence handoffs, prior art and the limits of the EMEM experiments.', 'conference questions', `
<h1>What does this result establish?</h1>
<p class="lead">EMEM preserves the cited observation across an agent handoff and gives the receiver concrete checks. These short answers connect the contribution, comparisons and limitations to their evidence.</p>
<p><a class="btn" href="../demo/">Try the 12-second demonstration</a> · <a href="../methods/#prior">Compare the layers</a> · <a href="../use/">Connect your tool</a></p>
<p><b>The quick comparison:</b> STAC finds assets. C2PA carries media provenance. GeoGuard checks claims against external evidence. EMEM carries the addressable observation an agent cited. The approaches can be composed; composition is not claimed as an experiment here.</p>
${QA.questions.map((q,i)=>`<section id="q${i+1}"><h2>${esc(q.question)}</h2><p>${esc(q.answer)}</p><p class="note">${esc(q.status)} · ${q.sources.map(s=>`<a href="${esc(s.url)}">${esc(s.label)}</a>`).join(' · ')}</p></section>`).join('')}
<p class="note">Evidence reviewed ${esc(QA.date)}. ${src('research/v13/20_CONFERENCE_QUESTIONS.md','Printable rehearsal text')}.</p>`));

for (const [source,name] of [['eo_keylong','keylong'],['eo_rondonia','rondonia'],['sat042','sat042']]) {
  w(`assets/recovered_${name}.svg`,rd(`poster/fig/v12/${source}.svg`));
}
w('.nojekyll', '');
console.log(JSON.stringify({ wrote: ['index.html', 't/', 'r/', 'test/', 'methods/', 'use/', '.nojekyll'], integrations: ECO.length, status_counts: counts }));

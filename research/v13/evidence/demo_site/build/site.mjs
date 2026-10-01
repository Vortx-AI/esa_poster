// The rest of the QR site: landing page, record page, integrations page, and one-hop redirect pages.
// node site.mjs <repo_root> <site_dir>
import fs from 'fs'; import path from 'path';
import { blake3 } from '@noble/hashes/blake3';
import * as V from './verify.mjs';
const [, , ROOT = '/home/user/esa_poster', OUTD = '../site'] = process.argv;
const here = path.dirname(new URL(import.meta.url).pathname), out = path.resolve(here, OUTD);
const w = (p, s) => { fs.mkdirSync(path.dirname(path.join(out, p)), { recursive: true }); fs.writeFileSync(path.join(out, p), s); };
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const bundle = V.cbor(new Uint8Array(fs.readFileSync(path.join(ROOT, 'research/repro/v8/proof_bundle_ndvi.cbor'))));
const tok = V.parseToken(bundle.token), entry = V.bytesOf(bundle.entry), att = V.cbor(entry);
const fact = V.factsRaw(entry).find((x) => V.b32e(blake3(x)) === tok.cid), rec = V.cbor(fact);
const TOKEN_URL = 'https://emem.dev/verify?q=' + encodeURIComponent(bundle.token);
const GH = 'https://github.com/Vortx-AI/esa_poster';
const CSS = `:root{--ink:#16181b;--ink2:#3b3f45;--mute:#6b6f76;--rule:#d9d8d2;--paper:#faf9f6;--card:#fff;--blue:#0F5FA8;--red:#D2481E;--amber:#E8A317;--grey:#9C9A92;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;--sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
@media (prefers-color-scheme:dark){:root{--ink:#ecebe6;--ink2:#c9c8c2;--mute:#9a9a94;--rule:#34363a;--paper:#121315;--card:#1b1d20;--blue:#5b9be0;--red:#ef7a52;--amber:#f0b73d}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}main{max-width:720px;margin:0 auto;padding:16px 16px 48px}
.eyebrow{font:600 12px/1.4 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin:0 0 6px}h1{font-size:28px;line-height:1.15;margin:4px 0 10px}h2{font-size:18px;margin:24px 0 8px}
p{margin:0 0 10px}a{color:var(--blue)}code,pre{font-family:var(--mono);font-size:12.5px;overflow-wrap:anywhere;word-break:break-word}
.cta{display:block;border:1.5px solid var(--ink);border-radius:10px;padding:12px 14px;margin:10px 0;text-decoration:none;color:var(--ink);background:var(--card)}
.cta b{display:block;font:700 14px/1.3 var(--mono);letter-spacing:.04em}.cta span{font-size:14px;color:var(--ink2)}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-top:1px solid var(--rule);padding:6px 4px;vertical-align:top;text-align:left}th{width:34%;color:var(--mute);font-weight:600}
.st{font:700 11px/1 var(--mono);padding:3px 5px;border-radius:4px;border:1.5px solid currentColor;white-space:nowrap}.LIVE{color:var(--blue)}.PROTOCOL{color:var(--ink2)}.REGISTRY{color:var(--mute)}.EXAMPLE{color:#8a5d00}.EXPERIMENTAL{color:var(--red)}
li{margin:6px 0}pre{background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:8px;max-height:240px;overflow:auto;white-space:pre-wrap}
footer{margin-top:24px;border-top:1px solid var(--rule);padding-top:10px;font-size:13px;color:var(--mute)}`;
const page = (title, desc, body) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><style>${CSS}</style></head><body><main>${body}
<footer>EMEM · Jaya Kumari, Avijeet Singh · Vortx AI · Agentic AI for Earth Observation, Berlin, 19 Oct 2026 · <a href="${GH}">source of these pages</a></footer></main></body></html>`;
const redirect = (title, to, why) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta http-equiv="refresh" content="0; url=${esc(to)}"><link rel="canonical" href="${esc(to)}"><script>location.replace(${JSON.stringify(to)})</script></head>
<body style="font:16px/1.5 system-ui;margin:16px"><p>${esc(why)}</p><p><a href="${esc(to)}">${esc(to)}</a></p></body></html>`;

// ---- landing: the six CTAs, same words as on the board
const CTAS = [
  ['VIEW THE DEMO', './demo/', 'Your phone becomes Agent B: one paraphrase accepted unchecked, three corruptions refused, the genuine record accepted, the source pixel re-read. About 10 s, no sign-in.'],
  ['TRY A TOKEN', './t/', 'emem.dev/verify resolves the Keylong token and checks its bytes, its cell and the responder\'s signature. Paste any other token.'],
  ['INSPECT THE RECORD', './r/', 'The exact 1,115-byte record behind the board\'s main example: every field, its name, its signature and its log position.'],
  ['RE-RUN THE TEST', './test/', 'The mutation suite and the agent handoff experiment: data, scripts and one command to re-run them.'],
  ['READ THE METHODS', './methods/', 'Definitions, denominators, models, and which parts the authors\' own tools generated.'],
  ['DISCOVER INTEGRATIONS', './use/', 'Where emem runs today, each surface labelled LIVE, PROTOCOL, REGISTRY or EXAMPLE, with the date it was checked.'],
];
w('index.html', page('EMEM at Agentic AI for EO 2026', 'Six links from the EMEM poster: demo, token, record, test, methods, integrations.',
  `<p class="eyebrow">EMEM · poster links</p><h1>Agents hand each other evidence references, not paraphrases.</h1>
<p>EMEM: a content-addressed, verifiable Earth-memory protocol for AI agents. Poster Session 1, Agentic AI for Earth Observation (ESA Φ-lab and BIFOLD), Berlin, 19 Oct 2026.</p>
${CTAS.map(([k, u, d]) => `<a class="cta" href="${u}"><b>${k} →</b><span>${esc(d)}</span></a>`).join('\n')}
<h2>Media</h2><ul><li><a href="./media/">poster PDF, slide, 20 s and 60 s videos, handout, manifest</a></li></ul>`));

// ---- record page (MASTER §5, §15)
const a = rec.derivation.args, src = rec.sources[0], files = src.id.split(' ; ');
const S = bundle.sth, W = bundle.witness;
const rows = [
  ['token Agent A hands over', `<code>${bundle.token}</code>`],
  ['place (cell, about 10 m)', `<code>${rec.cell}</code> · centre ${a[0].toFixed(5)}° N, ${a[1].toFixed(5)}° E (near Keylong, Lahaul, India)`],
  ['band / product', `<code>${rec.band}</code> · ${esc(a[4])}`],
  ['valid time (capture)', `${src.captured_at} · scene <code>${a[2]}</code> · cloud ${a[6]} %`],
  ['value', `<b>${rec.value}</b> · confidence ${rec.confidence.toFixed(2)}`],
  ['inputs (signed in the record)', `B08 DN ${a[5][0]}, B04 DN ${a[5][1]}, offset ${a[12]} → recomputes to ${V.ndvi(a[5][0], a[5][1], a[12])}`],
  ['source files (named, not hashed)', files.map((f) => `<code>${esc(f.split('/').pop())}</code>`).join('<br>') + `<br>scheme <code>${src.scheme}</code>; the record carries no hash of these files`],
  ['derivation', `<code>${rec.derivation.fn_key}</code>`],
  ['name of the record', `<code>${tok.cid}</code> = base32(BLAKE3-256(the ${fact.length} bytes below)). It names this record, not the satellite file.`],
  ['signed', `${rec.signed_at} by key <code>${V.b32e(V.bytesOf(rec.signer))}</code>; batch of 1, root <code>${V.b32e(V.bytesOf(att.batch_root))}</code>, attested ${att.attested_at}`],
  ['logged', `entry ${bundle.leaf_index.toLocaleString('en')} of the public log; checked under head ${S.tree_size.toLocaleString('en')} (${S.signed_at}); co-signed by witness <code>${V.b32e(V.bytesOf(W.pubkey)).slice(0, 12)}…</code> at ${W.tree_size.toLocaleString('en')}`],
];
w('r/index.html', page('The record behind the EMEM poster', 'One signed Sentinel-2 NDVI record, field by field.',
  `<p class="eyebrow">EMEM · inspect the record</p><h1>The record Agent A handed over</h1>
<p>One signed observation: NDVI ${rec.value.toFixed(4)} at one 10 m cell on 25 Sep 2026. Every field below is read from its ${fact.length.toLocaleString('en')} bytes.</p>
<table>${rows.map(([k, v]) => `<tr><th>${k}</th><td>${v}</td></tr>`).join('')}</table>
<h2>Check it yourself</h2><ul><li><a href="../demo/">VIEW THE DEMO</a>: your browser re-hashes these bytes, checks the signature and the log, and re-reads the pixel.</li>
<li><a href="${TOKEN_URL}">emem.dev/verify</a> with this token.</li>
<li>The raw bytes: <a href="https://emem.dev/v1/facts/${tok.cid}">emem.dev/v1/facts/${tok.cid.slice(0, 8)}…</a> (send <code>accept: application/cbor</code> for CBOR); <code>b3sum</code> of them is the name above.</li></ul>
<h2>The ${fact.length.toLocaleString('en')} bytes (hex)</h2><pre>${V.hex(fact).replace(/(.{64})/g, '$1\n')}</pre>
<p>A signature fixes these bytes. It does not make the measurement true: whether the cell is the field you meant, and whether the sensor was right, are outside what this record can show.</p>`));

// ---- integrations (from the ecosystem manifest; only rows allowed to print, status as labelled there)
const M = JSON.parse(fs.readFileSync(path.join(ROOT, 'research/v13/ecosystem_manifest.json'), 'utf8'));
const ok = (r) => r.print && (r.print === true || r.print.allowed === true);
const groups = {}; for (const r of M.filter(ok)) (groups[r.poster_group] ||= []).push(r);
w('use/index.html', page('Where EMEM runs', 'Every integration surface, labelled by evidence status.',
  `<p class="eyebrow">EMEM · discover integrations</p><h1>One evidence protocol, multiple agent runtimes.</h1>
<p>Status: <span class="st LIVE">LIVE</span> run or confirmed by us · <span class="st PROTOCOL">PROTOCOL</span> open surface, client not run by us · <span class="st REGISTRY">REGISTRY</span> a listing, not an integration · <span class="st EXAMPLE">EXAMPLE</span> repo code, tool list checked. Checked ${M[0].verified_utc ? M[0].verified_utc.slice(0, 10) : '2026-10-01'}.</p>
${Object.entries(groups).map(([g, rs]) => `<h2>${esc(g.toLowerCase())}</h2><ul>${rs.map((r) => `<li><span class="st ${r.status}">${r.status}</span> <a href="${esc(r.url)}">${esc(r.platform.split(' (')[0])}</a> · ${esc((r.print && r.print.text) || r.mechanism.split(';')[0]).slice(0, 160)}</li>`).join('')}</ul>`).join('\n')}`));

// ---- one-hop redirects (short QR payloads; targets can be corrected after print)
w('t/index.html', redirect('TRY A TOKEN', TOKEN_URL, 'Opening emem.dev/verify with the Keylong token…'));
w('test/index.html', redirect('RE-RUN THE TEST', `${GH}/tree/main/research/repro/v13`, 'Opening the experiment folder on GitHub…'));
w('methods/index.html', redirect('READ THE METHODS', `${GH}/blob/main/research/repro/v13/METHODS.md`, 'Opening the methods on GitHub…'));
w('.nojekyll', '');
console.log(JSON.stringify({ wrote: ['index.html', 'r/', 'use/', 't/', 'test/', 'methods/'], integrations_rows: Object.values(groups).flat().length }));

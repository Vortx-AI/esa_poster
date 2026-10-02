import fs from 'fs';
import { blake3 } from '@noble/hashes/blake3';
import { ed25519 } from '@noble/curves/ed25519';
import * as V from './verify.mjs';
const bundleBytes = new Uint8Array(fs.readFileSync(new URL('../../research/repro/v8/proof_bundle_ndvi.cbor', import.meta.url)));
const bundle = V.cbor(bundleBytes);
const edVerify = (sig, msg, pk) => { try { return ed25519.verify(sig, msg, pk); } catch { return false; } };
const receive = V.makeReceiver({ blake3, edVerify, bundle });
const t0 = performance.now();
const fact = V.factsRaw(V.bytesOf(bundle.entry)).find((x) => V.b32e(blake3(x)) === V.parseToken(bundle.token).cid);
const M = V.mutations(fact, bundle.token);
const tok = bundle.token, cell = M.t.cell, cid = M.t.cid;
const cases = [
  ['prose', { kind: 'prose', text: 'NDVI is about 0.47 at the Keylong field, late September.' }],
  ['M3', { kind: 'ref', token: tok, bytes: M.m3 }],
  ['M4', { kind: 'ref', token: `emem:fact:${M.otherCell}:${cid}`, bytes: fact }],
  ['M8', { kind: 'ref', token: `emem:fact:${cell}:${V.b32e(blake3(M.m8))}`, bytes: M.m8 }],
  ['G0', { kind: 'ref', token: tok, bytes: fact }],
];
for (const [n, h] of cases) { const r = receive(h); console.log(n, r.verdict, '|', r.why); for (const s of r.steps) console.log('   ', s.layer, s.ok, s.text); }
console.log('ms', (performance.now() - t0).toFixed(1));
console.log('value offset', M.off, 'm3 cid', V.b32e(blake3(M.m3)), 'm8 cid', V.b32e(blake3(M.m8)));

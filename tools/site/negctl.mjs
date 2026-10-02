// Negative controls. Note (report 09 appendix C): the first case here is void (its byte search missed the CBOR uint-array signature and flipped a fact byte); negctl2.mjs replaces it.
import fs from 'fs'; import { blake3 } from '@noble/hashes/blake3'; import { ed25519 } from '@noble/curves/ed25519'; import * as V from './verify.mjs';
const edVerify = (s, m, p) => { try { return ed25519.verify(s, m, p); } catch { return false; } };
const bb = new Uint8Array(fs.readFileSync(new URL('../../research/repro/v8/proof_bundle_ndvi.cbor', import.meta.url)));
const run = (bundle, label) => { const tok = V.parseToken(bundle.token); const fact = V.factsRaw(V.bytesOf(bundle.entry)).find((x) => V.b32e(blake3(x)) === tok.cid) || V.factsRaw(V.bytesOf(bundle.entry))[0];
  const r = V.makeReceiver({ blake3, edVerify, bundle })({ kind: 'ref', token: bundle.token, bytes: fact }); console.log(label, r.verdict, '|', r.steps.filter((s) => s.ok === false).map((s) => s.text).join('; ')); };
const B = V.cbor(bb); run(B, 'genuine bundle:');
// 1) attestation signature: flip one bit of the 64-byte signature inside the entry (entry bytes change -> log leaf also changes)
const att = V.cbor(V.bytesOf(B.entry)); const sig = V.bytesOf(att.signature); const e = V.bytesOf(B.entry).slice();
const at = (() => { for (let i = 0; i < e.length - 64; i++) if (sig.every((x, j) => e[i + j] === x)) return i; return -1; })(); e[at + 10] ^= 1;
run({ ...B, entry: e }, 'attestation sig bit flipped:');
// 2) STH signature bit flipped
const S = { ...B.sth, sig: V.bytesOf(B.sth.sig).slice() }; S.sig[5] ^= 1; run({ ...B, sth: S }, 'STH sig bit flipped:');
// 3) inclusion path element changed
const S2 = { ...B.sth, inclusion_path: B.sth.inclusion_path.map((p, i) => { const q = V.bytesOf(p).slice(); if (i === 3) q[0] ^= 1; return q; }) }; run({ ...B, sth: S2 }, 'inclusion path tampered:');

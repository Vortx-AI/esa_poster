import fs from 'fs'; import { blake3 } from '@noble/hashes/blake3'; import { ed25519 } from '@noble/curves/ed25519'; import * as V from './verify.mjs';
const bb = new Uint8Array(fs.readFileSync(new URL('../../research/repro/v8/proof_bundle_ndvi.cbor', import.meta.url))); const B = V.cbor(bb);
const tok = V.parseToken(B.token); const fact = V.factsRaw(V.bytesOf(B.entry)).find((x) => V.b32e(blake3(x)) === tok.cid);
let n = 0; const flipFirst = (s, m, p) => { n++; const t = s.slice(); if (n === 1) t[7] ^= 1; try { return ed25519.verify(t, m, p); } catch { return false; } };
let r = V.makeReceiver({ blake3, edVerify: flipFirst, bundle: B })({ kind: 'ref', token: B.token, bytes: fact }); console.log('attestation signature bit flipped:', r.verdict, '|', r.steps.filter((s) => !s.ok).map((s) => s.text).join('; '));
const att = V.cbor(V.bytesOf(B.entry)); console.log('signature field type in entry:', Array.isArray(att.signature) ? 'array of uint' : att.signature.constructor.name);

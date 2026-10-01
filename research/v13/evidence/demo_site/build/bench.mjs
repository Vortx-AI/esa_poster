import fs from 'fs'; import { blake3 } from '@noble/hashes/blake3'; import { ed25519 } from '@noble/curves/ed25519'; import * as V from './verify.mjs';
const B = V.cbor(new Uint8Array(fs.readFileSync('/home/user/esa_poster/research/repro/v8/proof_bundle_ndvi.cbor')));
const tok = V.parseToken(B.token); const fact = V.factsRaw(V.bytesOf(B.entry)).find((x) => V.b32e(blake3(x)) === tok.cid);
const rcv = V.makeReceiver({ blake3, edVerify: (s, m, p) => ed25519.verify(s, m, p), bundle: B });
for (let i = 0; i < 5; i++) rcv({ kind: 'ref', token: B.token, bytes: fact });
const N = 50, t = performance.now(); for (let i = 0; i < N; i++) rcv({ kind: 'ref', token: B.token, bytes: fact }); console.log('G0 full receiver check (L0-L2, 4 Ed25519 verifies, 2 inclusion + 1 consistency proof):', ((performance.now() - t) / N).toFixed(2), 'ms, Node', process.version);

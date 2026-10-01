// Agent B, the receiver: checks an emem fact handoff with stock primitives only (BLAKE3, Ed25519, CBOR, RFC 6962).
// No emem code. Ported line by line from research/repro/v8/verify_bundle.py and research/repro/v12/scripts/verify_lib.py.
// Every function is pure; the crypto is injected so Node (build, transcript, tests) and the browser run the same code.

export const PINNED_KEY_B32 = '777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka'; // emem.dev key (DNS TXT, did.json, jwks.json)
const A32 = 'abcdefghijklmnopqrstuvwxyz234567';
export function b32e(u) { let bits = 0, v = 0, o = ''; for (const x of u) { v = (v << 8) | x; bits += 8; while (bits >= 5) { o += A32[(v >>> (bits - 5)) & 31]; bits -= 5; } } if (bits) o += A32[(v << (5 - bits)) & 31]; return o; }
export function b32d(s) { let bits = 0, v = 0; const o = []; for (const c of s.toLowerCase()) { v = (v << 5) | A32.indexOf(c); bits += 5; if (bits >= 8) { o.push((v >>> (bits - 8)) & 255); bits -= 8; } } return new Uint8Array(o); }
export const hex = (u) => [...u].map((x) => x.toString(16).padStart(2, '0')).join('');
export const eq = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
const cat = (...p) => { const n = p.reduce((s, x) => s + x.length, 0), o = new Uint8Array(n); let i = 0; for (const x of p) { o.set(x, i); i += x.length; } return o; };
const te = new TextEncoder();
const u32le = (n) => new Uint8Array([n & 255, (n >>> 8) & 255, (n >>> 16) & 255, (n >>> 24) & 255]);
const u64be = (n) => { const o = new Uint8Array(8); let v = BigInt(n); for (let i = 7; i >= 0; i--) { o[i] = Number(v & 255n); v >>= 8n; } return o; };
const pre = (d) => { const b = te.encode(d); return cat(te.encode('emem.preimage.v1\x00'), u32le(b.length), b); };
const seg = (t, b) => cat(new Uint8Array([t]), u32le(b.length), b);
export const bytesOf = (v) => (v instanceof Uint8Array ? v : new Uint8Array(v));

// ---------------------------------------------------------------- minimal CBOR (RFC 8949) reader
function half(h) { const s = h >> 15 ? -1 : 1, e = (h >> 10) & 31, f = h & 1023; return e === 0 ? s * 2 ** -14 * (f / 1024) : e === 31 ? (f ? NaN : s * Infinity) : s * 2 ** (e - 15) * (1 + f / 1024); }
export function itemEnd(b, i) {
  const ib = b[i], mt = ib >> 5, ai = ib & 31; i += 1; let val = ai;
  if (ai >= 24 && ai <= 27) { const k = 1 << (ai - 24); val = 0; for (let j = 0; j < k; j++) val = val * 256 + b[i + j]; i += k; }
  if (mt === 0 || mt === 1 || mt === 7) return i;
  if (mt === 2 || mt === 3) return i + val;
  if (mt === 6) return itemEnd(b, i);
  for (let n = 0; n < (mt === 4 ? val : 2 * val); n++) i = itemEnd(b, i);
  return i;
}
export function decode(b, i = 0) {
  const ib = b[i], mt = ib >> 5, ai = ib & 31; let p = i + 1, val = ai;
  if (mt === 7) {
    const dv = new DataView(b.buffer, b.byteOffset + p);
    if (ai === 25) return [half(dv.getUint16(0)), p + 2]; if (ai === 26) return [dv.getFloat32(0), p + 4]; if (ai === 27) return [dv.getFloat64(0), p + 8];
    return [ai === 20 ? false : ai === 21 ? true : null, p];
  }
  if (ai >= 24 && ai <= 27) { const k = 1 << (ai - 24); val = 0; for (let j = 0; j < k; j++) val = val * 256 + b[p + j]; p += k; }
  if (mt === 0) return [val, p]; if (mt === 1) return [-1 - val, p];
  if (mt === 2) return [b.slice(p, p + val), p + val];
  if (mt === 3) return [new TextDecoder().decode(b.slice(p, p + val)), p + val];
  if (mt === 6) return decode(b, p);
  if (mt === 4) { const a = []; for (let n = 0; n < val; n++) { const [x, q] = decode(b, p); a.push(x); p = q; } return [a, p]; }
  const m = {}; for (let n = 0; n < val; n++) { const [k, q] = decode(b, p); const [x, r] = decode(b, q); m[k] = x; p = r; } return [m, p];
}
export const cbor = (b) => decode(b)[0];
// raw bytes of each element of the "facts" array inside an attestation entry (never re-encoded)
export function factsRaw(entry) {
  const ai = entry[0] & 31; let i = ai < 24 ? 1 : 1 + (1 << (ai - 24)); const n = ai < 24 ? ai : entry[1];
  for (let k = 0; k < n; k++) {
    const ke = itemEnd(entry, i), key = cbor(entry.slice(i, ke)), ve = itemEnd(entry, ke);
    if (key === 'facts') { const arr = entry.slice(ke, ve), aj = arr[0] & 31; let j = aj < 24 ? 1 : 1 + (1 << (aj - 24)); const m = aj < 24 ? aj : arr[1]; const out = [];
      for (let q = 0; q < m; q++) { const e = itemEnd(arr, j); out.push(arr.slice(j, e)); j = e; } return out; }
    i = ve;
  }
  return [];
}

// ---------------------------------------------------------------- RFC 6962 proofs
export function makeLog(H) {
  const node = (l, r) => H(cat(new Uint8Array([1]), l, r));
  function vIncl(idx, size, leaf, path, root) {
    if (idx >= size) return false; let fn = idx, sn = size - 1, r = leaf;
    for (const p of path) { if (sn === 0) return false;
      if ((fn & 1) || fn === sn) { r = node(p, r); if (!(fn & 1)) while (!(fn & 1) && fn !== 0) { fn >>= 1; sn >>= 1; } } else r = node(r, p);
      fn >>= 1; sn >>= 1; }
    return sn === 0 && eq(r, root);
  }
  function vCons(n1, n2, r1, r2, path) {
    if (n1 === n2) return eq(r1, r2) && !path.length;
    if ((n1 & (n1 - 1)) === 0) path = [r1, ...path];
    let fn = n1 - 1, sn = n2 - 1; while (fn & 1) { fn >>= 1; sn >>= 1; }
    let fr = path[0], sr = path[0];
    for (const c of path.slice(1)) { if (sn === 0) return false;
      if ((fn & 1) || fn === sn) { fr = node(c, fr); sr = node(c, sr); if (!(fn & 1)) while (!(fn & 1) && fn !== 0) { fn >>= 1; sn >>= 1; } } else sr = node(sr, c);
      fn >>= 1; sn >>= 1; }
    return eq(fr, r1) && eq(sr, r2) && sn === 0;
  }
  function batchRoot(leaves, v) {
    let L = leaves.map((l) => (v ? H(cat(new Uint8Array([0]), l)) : H(cat(l, l))));
    while (L.length > 1) { const nx = []; for (let i = 0; i < L.length; i += 2) { const r = i + 1 < L.length ? L[i + 1] : L[i]; nx.push(v ? node(L[i], r) : H(cat(L[i], r))); } L = nx; }
    return L[0];
  }
  return { vIncl, vCons, batchRoot };
}

// ---------------------------------------------------------------- the record, the token, the derivation
export function parseToken(t) { const m = /^emem:fact:([^:]+):([a-z2-7]{52})$/.exec(t.trim()); return m ? { cell: m[1], cid: m[2] } : null; }
export function valueOffset(fact) { const n = [0x65, 0x76, 0x61, 0x6c, 0x75, 0x65, 0xfb]; for (let i = 0; i + n.length <= fact.length; i++) if (n.every((x, j) => fact[i + j] === x)) return i + n.length; return -1; }
// emem's NDVI rule (research/repro/v10/algorithms.md, emem lib.rs:52771-52778, :51726-51748): rho = (DN + o) * 1e-4
export const ndvi = (b08, b04, o) => { const r8 = (b08 + o) * 1e-4, r4 = (b04 + o) * 1e-4; return (r8 - r4) / (r8 + r4); };
export function recompute(f) { const a = (f.derivation || {}).args || []; const dn = a[5], o = a[12]; if (!Array.isArray(dn) || typeof o !== 'number') return null;
  const v = ndvi(dn[0], dn[1], o); return { b08: dn[0], b04: dn[1], offset: o, value: v, equal: v === f.value }; }

// ---------------------------------------------------------------- mutations (named as in research/repro/v11/mutation_suite.py)
export function mutations(fact, token) {
  const off = valueOffset(fact), t = parseToken(token);
  const m3 = fact.slice(); const dv3 = new DataView(m3.buffer); dv3.setBigUint64(off, dv3.getBigUint64(off) + 1n); // one ULP
  const m8 = fact.slice(); new DataView(m8.buffer).setFloat64(off, 0.45);
  return { off, t, m3, m8, otherCell: 'defi.zb493.xuqA.zcb5f' /* Bengaluru, the cell v12 used for the relabelled token */ };
}

// ---------------------------------------------------------------- Agent B: one handoff, one verdict, every check listed
// handoff = { kind:'prose', text } | { kind:'ref', token, bytes }
export function makeReceiver({ blake3, edVerify, bundle }) {
  const H = (b) => blake3(b), { vIncl, vCons, batchRoot } = makeLog(H), pinned = b32d(PINNED_KEY_B32);
  const entry = bytesOf(bundle.entry), att = cbor(entry), fr = factsRaw(entry), pv = att.preimage_version || 0;
  const S = bundle.sth, W = bundle.witness;
  return function receive(h) {
    const steps = []; const step = (layer, ok, text) => { steps.push({ layer, ok, text }); return ok; };
    if (h.kind === 'prose') { step('—', null, 'a sentence carries no name to resolve, no bytes to re-hash, no signature to check');
      return { verdict: 'ACCEPTED', checked: false, steps, why: 'nothing could be checked, so nothing was refused' }; }
    const t = parseToken(h.token); if (!t) { step('L0', false, 'not an emem:fact token'); return { verdict: 'REFUSED', steps, why: 'malformed token' }; }
    const name = b32e(H(h.bytes));
    if (!step('L0', name === t.cid, name === t.cid ? `the ${h.bytes.length.toLocaleString('en')} bytes hash to the name in the token (${t.cid.slice(0, 8)}…)` : `the bytes hash to ${name.slice(0, 8)}…, not to ${t.cid.slice(0, 8)}… named in the token`))
      return { verdict: 'REFUSED', steps, why: 'the bytes are not the bytes the token names' };
    let f; try { f = cbor(h.bytes); } catch { step('L0', false, 'the bytes are not a CBOR record'); return { verdict: 'REFUSED', steps, why: 'unreadable record' }; }
    if (!step('L1', f.cell === t.cell, f.cell === t.cell ? `the record's own cell is the token's cell (${f.cell})` : `the token says ${t.cell}; the record says ${f.cell}`))
      return { verdict: 'REFUSED', steps, why: 'the token names a place the record is not about' };
    const inBatch = fr.some((x) => eq(x, h.bytes));
    const leaves = fr.map((x) => H(x)).sort((a, b) => { for (let i = 0; i < 32; i++) if (a[i] !== b[i]) return a[i] - b[i]; return 0; });
    const rootOk = eq(batchRoot(leaves, pv), bytesOf(att.batch_root));
    const msg = pv ? H(cat(pre('attestation'), seg(1, bytesOf(att.batch_root)), seg(2, te.encode(att.registry_cid)), seg(3, te.encode(att.schema_cid))))
      : H(cat(bytesOf(att.batch_root), te.encode(att.registry_cid), te.encode(att.schema_cid)));
    const sigOk = eq(bytesOf(att.attester), pinned) && edVerify(bytesOf(att.signature), msg, pinned);
    if (!step('L0', inBatch && rootOk && sigOk, inBatch && rootOk && sigOk
      ? `the bytes sit in a batch of ${fr.length}; its Merkle root recomputes; Ed25519 accepts the signature of key ${PINNED_KEY_B32.slice(0, 8)}…`
      : !inBatch ? `no batch signed by key ${PINNED_KEY_B32.slice(0, 8)}… contains these bytes; the signed batch for this observation holds the genuine ones` : 'the batch signature does not check'))
      return { verdict: 'REFUSED', steps, why: 'nothing the signer signed contains these bytes' };
    const leaf = H(cat(new Uint8Array([0]), H(entry)));
    const sthm = H(cat(pre('emem.translog.sth.v1'), seg(1, u64be(S.tree_size)), seg(2, bytesOf(S.root)), seg(3, te.encode(S.signed_at)), seg(4, bytesOf(S.pubkey))));
    const sthOk = eq(bytesOf(S.pubkey), pinned) && edVerify(bytesOf(S.sig), sthm, pinned);
    const incl = vIncl(bundle.leaf_index, S.tree_size, leaf, S.inclusion_path.map(bytesOf), bytesOf(S.root));
    let wit = null;
    if (W) { const wm = H(cat(pre('emem.translog.witness.v1'), seg(1, u64be(W.tree_size)), seg(2, bytesOf(W.root)), seg(3, bytesOf(W.pubkey))));
      wit = { key: b32e(bytesOf(W.pubkey)), sig: edVerify(bytesOf(W.sig), wm, bytesOf(W.pubkey)), incl: vIncl(bundle.leaf_index, W.tree_size, leaf, W.inclusion_path.map(bytesOf), bytesOf(W.root)),
        cons: vCons(W.tree_size, S.tree_size, bytesOf(W.root), bytesOf(S.root), W.consistency_to_sth.map(bytesOf)), size: W.tree_size }; }
    const logOk = sthOk && incl && (!wit || (wit.sig && wit.incl && wit.cons));
    if (!step('L0', logOk, logOk ? `the batch is log entry ${bundle.leaf_index.toLocaleString('en')} under a signed head of ${S.tree_size.toLocaleString('en')} entries` + (wit ? `; a second key (${wit.key.slice(0, 8)}…) co-signed head ${wit.size.toLocaleString('en')}, a prefix of it` : '') : 'the log proofs do not check'))
      return { verdict: 'REFUSED', steps, why: 'not in the public log' };
    const rc = recompute(f);
    if (rc) step('L2', rc.equal, rc.equal ? `NDVI recomputes from the signed inputs: B08 ${rc.b08}, B04 ${rc.b04}, offset ${rc.offset} → ${rc.value}` : `recomputing from B08 ${rc.b08}, B04 ${rc.b04} gives ${rc.value}, not ${f.value}`);
    if (rc && !rc.equal) return { verdict: 'REFUSED', steps, why: 'the value does not follow from its own inputs' };
    return { verdict: 'ACCEPTED', checked: true, steps, record: f, why: 'every check this page can run passed (L0, L1, L2)' };
  };
}

// ---------------------------------------------------------------- L3: re-read the named pixel from the named file (live, optional)
// COG = classic TIFF, 512 x 512 tiles, deflate (8), 15-bit samples, no predictor (measured on these two files, 2026-10-01).
export async function rereadPixel({ url, col, row, fetchRange, inflate, H, expectTileB3 }) {
  const head = await fetchRange(url, 0, 65535); const dv = new DataView(head.buffer, head.byteOffset);
  const le = head[0] === 0x49; const u16 = (o) => dv.getUint16(o, le), u32 = (o) => dv.getUint32(o, le);
  if (u16(2) !== 42) throw new Error('not a classic TIFF');
  const ifd = u32(4), n = u16(ifd), tags = {};
  for (let i = 0; i < n; i++) { const e = ifd + 2 + 12 * i, tag = u16(e), typ = u16(e + 2), cnt = u32(e + 4), sz = { 3: 2, 4: 4, 16: 8 }[typ] || 1;
    const at = sz * cnt <= 4 ? e + 8 : u32(e + 8); const rd = (k) => (typ === 3 ? u16(at + 2 * k) : typ === 4 ? u32(at + 4 * k) : Number(dv.getBigUint64(at + 8 * k, le)));
    tags[tag] = { cnt, rd }; }
  const W = tags[256].rd(0), tw = tags[322].rd(0), bps = tags[258].rd(0), comp = tags[259].rd(0);
  const ti = Math.floor(row / tw) * Math.ceil(W / tw) + Math.floor(col / tw);
  const off = tags[324].rd(ti), len = tags[325].rd(ti);
  const tile = await fetchRange(url, off, off + len - 1);
  const tileB3 = hex(H(tile));
  if (comp !== 8) throw new Error('compression ' + comp + ' not handled');
  const raw = await inflate(tile), rb = (tw * bps) / 8;
  const px = (c, r) => { const bit = c * bps, b0 = r * rb + (bit >> 3); const v = (raw[b0] << 16) | (raw[b0 + 1] << 8) | raw[b0 + 2]; return (v >> (24 - bps - (bit & 7))) & ((1 << bps) - 1); };
  const lc = col % tw, lr = row % tw, win = [];
  for (let dr = -2; dr <= 2; dr++) { const rr = []; for (let dc = -2; dc <= 2; dc++) rr.push(px(lc + dc, lr + dr)); win.push(rr); }
  return { dn: px(lc, lr), win, tile_index: ti, tile_offset: off, tile_length: len, tile_blake3: tileB3, tile_matches_trace: expectTileB3 ? tileB3 === expectTileB3 : null, bps, tw };
}

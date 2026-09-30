"""Verify emem's transparency log offline: signed tree head, an inclusion proof,
and a consistency proof. Written from RFC 9162 with blake3, independent of emem code.
    pip install blake3 pynacl ; python verify_log.py [leaf_index] [old_size]
"""
import urllib.request
import json,base64,blake3,struct,sys
from nacl.signing import VerifyKey
def b32(s): return base64.b32decode(s.upper()+'='*((8-len(s)%8)%8))
H=lambda b: blake3.blake3(b).digest()
node=lambda l,r: H(b'\x01'+l+r)
def pre(d): d=d.encode(); return b"emem.preimage.v1\x00"+struct.pack('<I',len(d))+d
seg=lambda t,b: bytes([t])+struct.pack('<I',len(b))+b
def sth_ok(s):
    m=H(pre("emem.translog.sth.v1")+seg(1,struct.pack('>Q',s['tree_size']))+seg(2,b32(s['root_b32']))+seg(3,s['signed_at'].encode())+seg(4,b32(s['responder_pubkey_b32'])))
    try: VerifyKey(b32(s['responder_pubkey_b32'])).verify(m,b32(s['signature_b32'])); return True
    except Exception: return False
# RFC 9162 s2.1.3.2
def v_incl(idx,size,leaf,path,root):
    if idx>=size: return False
    fn,sn,r=idx,size-1,leaf
    for p in path:
        if sn==0: return False
        if fn&1 or fn==sn:
            r=node(p,r)
            if not fn&1:
                while not fn&1 and fn!=0: fn>>=1; sn>>=1
        else: r=node(r,p)
        fn>>=1; sn>>=1
    return sn==0 and r==root
# RFC 9162 s2.1.4.2
def v_cons(n1,n2,r1,r2,path):
    if n1==n2: return r1==r2 and not path
    if n1&(n1-1)==0: path=[r1]+path
    fn,sn=n1-1,n2-1
    while fn&1: fn>>=1; sn>>=1
    fr=sr=path[0]
    for c in path[1:]:
        if sn==0: return False
        if fn&1 or fn==sn:
            fr=node(c,fr); sr=node(c,sr)
            if not fn&1:
                while not fn&1 and fn!=0: fn>>=1; sn>>=1
        else: sr=node(sr,c)
        fn>>=1; sn>>=1
    return fr==r1 and sr==r2 and sn==0
def get(path):
    return json.load(urllib.request.urlopen("https://emem.dev"+path, timeout=60))
if __name__=='__main__':
    idx=int(sys.argv[1]) if len(sys.argv)>1 else 1234567
    old=int(sys.argv[2]) if len(sys.argv)>2 else 1000000
    sth=get("/v1/log/sth")['sth']; n=sth['tree_size']
    print("STH sig valid:",sth_ok(sth),"size",n)
    inc=get(f"/v1/log/inclusion?leaf_index={idx}&tree_size={n}")
    ent=get(f"/v1/log/entries?start={idx}&end={idx+1}")['entries'][0]
    cbor=b32(ent['attestation_cbor_b32']); eh=H(cbor)
    print("entry: blake3(cbor)==entry_hash:", eh==b32(inc['entry_hash_b32']), "cbor bytes",len(cbor))
    leaf=H(b'\x00'+eh); print("leaf_hash matches:",leaf==b32(inc['leaf_hash_b32']))
    path=[b32(x) for x in inc['audit_path_b32']]
    print("inclusion of leaf",idx,"under signed STH:",v_incl(idx,n,leaf,path,b32(sth['root_b32'])),"path len",len(path))
    bad=bytearray(leaf); bad[0]^=1
    print("inclusion with 1-bit flipped leaf:",v_incl(idx,n,bytes(bad),path,b32(sth['root_b32'])))
    c=get(f"/v1/log/consistency?first={old}&second={n}")
    print("consistency",c['first_size'],"->",c['second_size'],":",v_cons(c['first_size'],c['second_size'],b32(c['first_root_b32']),b32(sth['root_b32']),[b32(x) for x in c['consistency_proof_b32']]))

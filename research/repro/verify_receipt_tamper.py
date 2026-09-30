import json,struct,blake3,sys
from nacl.signing import VerifyKey
def seg(t,b): return bytes([t])+struct.pack('<I',len(b))+b
def seglist(t,items):
    body=b''.join(struct.pack('<I',len(i.encode()))+i.encode() for i in items)
    return bytes([t])+struct.pack('<I',len(items))+body
def pre(domain): d=domain.encode(); return b"emem.preimage.v1\x00"+struct.pack('<I',len(d))+d
def ctext(s):
    b=s.encode(); return (bytes([0x60+len(b)]) if len(b)<24 else bytes([0x78,len(b)]))+b
def cbor_map(m):
    ks=sorted(m); return bytes([0xa0+len(ks)])+b''.join(ctext(k)+ctext(m[k]) for k in ks)
def merkle_binding(p):
    s=pre("merkle")
    if p is None: s+=seg(5,b'')
    else:
        s+=seg(1,bytes(p['root']))+seg(2,struct.pack('<I',p['leaf_index']))+seg(3,b''.join(bytes(x) for x in p['path']))+seg(4,bytes([p['version']]))
    return blake3.blake3(s).digest()
def digest(r,ver):
    s=pre("receipt")+seg(1,r['request_id'].encode())+seg(2,r['served_at'].encode())
    if r.get('source_versions'): s+=seg(6,blake3.blake3(cbor_map(r['source_versions'])).hexdigest().encode())
    s+=seg(7,r['primitive'].encode())+seglist(8,r['cells'])+seglist(9,r['fact_cids'])
    if ver>=2: s+=seg(0x0b,merkle_binding(r.get('merkle_proof')).hex().encode())
    return blake3.blake3(s).digest()
r=json.load(open(sys.argv[1]))['receipt']
vk=VerifyKey(bytes(r['responder']))
for label,rr in [("as-served",r),("proof stripped",{k:v for k,v in r.items() if k!='merkle_proof'})]:
    m=digest(rr,rr.get('preimage_version',0))
    try: vk.verify(m,bytes(r['signature'])); ok=True
    except Exception: ok=False
    print(f"{label:15s} v{rr['preimage_version']} preimage={m.hex()} sig_valid={ok}")
m=digest({k:v for k,v in r.items() if k!='merkle_proof'},1)
try: vk.verify(m,bytes(r['signature'])); ok=True
except Exception: ok=False
print(f"downgrade->v1    preimage={m.hex()} sig_valid={ok}")

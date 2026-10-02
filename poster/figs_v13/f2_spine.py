"""Earth-to-agent mechanism followed by the existing controlled handoff results.
The record and every result are loaded from committed evidence. R5 uses the same
final/preregistration gate as the poster; the R1 fallback stays available.
"""
import json
import sys
from pathlib import Path
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S
sys.path.insert(0, str(Path(S.ROOT) / 'poster'))
from build_v13 import r5_mode
sys.path.insert(0, str(Path(S.ROOT) / 'research/repro/v11'))
import mutation_suite as MS
W, H = 801, 118
fig = S.fig_mm(W, H)
ax = fig.add_axes([0,0,1,1]); ax.set(xlim=(0,W), ylim=(H,0)); ax.axis('off')
labels=[]
def T(x,y,s,claim='U.flow',size=20,color=None,weight=400,**kw):
    labels.append(dict(text=s,claim=claim,pt=size))
    return ax.text(x,y,s,fontsize=size,color=color or S.C['ink'],fontweight=weight,va='center',**kw)
C=S.C
T(0,4,'EARTH DATA',size=17,color=C['emem'],weight=700)
T(347,4,'AGENT REASONING',size=17,color=C['emem'],weight=700)
steps=[
 ('OBSERVE','Read the source','Optical · radar · terrain','source observations'),
 ('LOCATE','Name the lookup','cell · product · time','observation family'),
 ('RECORD','Canonicalise the record','value · derivation · sources','content address'),
 ('HAND OFF','Agent A passes a reference','emem:fact:<cell>:<cid>','reference in context'),
 ('RESOLVE','Agent B retrieves it','the exact addressed record','same cited observation'),
 ('CHECK','Bind and re-hash','attestation · recipe · source','checked evidence'),
 ('CONTINUE','Use the checked record','compare · reason · act','next reasoning step'),
]
w,gap=107.57,8
for i,(verb,action,detail,base) in enumerate(steps):
    x=i*(w+gap); dark=i in (2,3,5)
    fc=C['emem'] if dark else C['emem_tint']
    tc='white' if dark else C['ink']
    ax.add_patch(FancyBboxPatch((x,12),w,51,boxstyle='round,pad=0,rounding_size=2',fc=fc,ec='none'))
    T(x+5,22,verb,size=30,color=tc,weight=700)
    T(x+5,36,action,size=20,color=tc,weight=600)
    T(x+5,46,detail,size=17,color=tc)
    T(x+5,57,base,size=14,color=tc)
    if i<6:
        ax.add_patch(FancyArrowPatch((x+w+.8,37),(x+w+gap-.8,37),arrowstyle='-|>',mutation_scale=16,color=C['emem'],lw=2))
T(0,73,'Lookup identity: where / product / time',claim='U.identities',size=22,weight=600)
T(347,73,'Content address: BLAKE3 of the canonical record',claim='U.identities',size=22,weight=600,color=C['emem'])
ax.plot([0,W],[82,82],color=C['rule'],lw=1)
r5,data,info=r5_mode()
if r5:
    lanes=[('prose','A'),('JSON','B'),('retrieved text','C'),('opaque id','D'),('checked reference','E')]
    vals=[(name,data['primary'][code]['pooled_claude']['false_accept'],f'R5.{code}.pooled') for name,code in lanes]
else:
    mm=json.loads((Path(S.ROOT)/'research/repro/v11/out/mutation_matrix.json').read_text())
    # Counts are independently checked against the source by the claims gate.
    vals=[]
    for name,code,cid in [('prose','A','S.R1.A'),('JSON','B','S.R1.B'),('opaque id','C','S.R1.C'),('checked reference','I','S.R1.I')]:
        row=mm['summary'][code]
        vals.append((name,{'k':row['false_accepts'],'n':row['applicable']},cid))
T(0,88,'CONTROLLED HANDOFF TEST: ACTED ON CORRUPTED EVIDENCE',claim='U.benchmark',size=14,color=C['ink2'],weight=600)
for i,(name,v,cid) in enumerate(vals):
    x=i*W/len(vals)
    T(x+2,100,name,claim='U.benchmark',size=20,weight=600)
    T(x+101,106,f"{v['k']} / {v['n']}",claim=cid,size=34,weight=700,color=C['emem'] if v['k']==0 else C['harm'])
S.save(fig,'f2_spine')
Path(S.OUT,'f2_spine.labels.json').write_text(json.dumps({'figure':'f2_spine','size_mm':[W,H],'mode':info['mode'],'labels':labels},indent=1)+'\n')

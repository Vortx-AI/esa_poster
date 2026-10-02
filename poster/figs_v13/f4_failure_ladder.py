"""Implemented drift score, with thresholds pinned by upstream Rust tests."""
import json,sys
from pathlib import Path
from matplotlib.patches import Rectangle
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,100
fig=S.fig_mm(W,H);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off');labels=[]
source=(Path(S.ROOT)/'research/v13/evidence/formalism/source/crates/emem-trace/src/drift.rs').read_text()
assert 'let z = delta / (3.0 * sigma);' in source and 'z / (1.0 + z)' in source
assert 'fn pinned_points()' in source and 'fn missing_sigma_is_strict()' in source
raw=(Path(S.ROOT)/'research/repro/v12/trace/emem_trace_tests.txt').read_text()
assert 'test drift::tests::pinned_points ... ok' in raw
assert 'test drift::tests::missing_sigma_is_strict ... ok' in raw
def T(x,y,s,size=17,color=None,weight=400,**kw):
 labels.append(dict(text=s,claim='DF.score',pt=size));ax.text(x,y,s,fontsize=size,color=color or S.C['ink'],fontweight=weight,va='center',**kw)
T(0,4,'IMPLEMENTED · DRIFT-ANCHOR SCORE',14,S.C['emem'],700)
T(4,18,'u = |x − a| / (3σ)',26)
T(4,32,'s = u / (1 + u)',30,S.C['emem'],600)
T(4,44,'x: output · a: anchor · σ: anchor uncertainty',16)
for lo,hi,col in [(0,.5,'emem'),(.5,.75,'incident'),(.75,1,'harm')]:
 ax.add_patch(Rectangle((lo*W,62),(hi-lo)*W,7,fc=S.C[col],ec='none'))
T(3,55,'consistent',17);T(100,55,'tension',17);T(151,55,'contradicted',17)
for x,t,ha in [(0,'0','left'),(W*.5,'0.50','center'),(W*.75,'0.75','center'),(W,'1','right')]:T(x,75,t,17,ha=ha)
T(0,86,'Tests pin 3σ → 0.50 and 9σ → 0.75.',17,weight=600)
T(0,96,'Missing or invalid σ: exact agreement required.',15,S.C['ink2'])
S.save(fig,'f4_failure_ladder')
Path(S.OUT,'f4_failure_ladder.labels.json').write_text(json.dumps({'figure':'f4_failure_ladder','size_mm':[W,H],'labels':labels},indent=1)+'\n')

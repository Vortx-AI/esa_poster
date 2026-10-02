"""Recover concrete bundle and reasoning-state demonstrations from v7/v11."""
import json,sys
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,86
r=Path(S.ROOT)
b=json.loads((r/'research/repro/v8/bundle_mint.json').read_text())
checks=json.loads((r/'research/v13/evidence/community/recovery_checks.json').read_text())
assert b['members']==b['resolved']==len(b['citations'])==8
assert len(b['bundle_token'])==38 and checks['state_hashes_reproduced']==4
fig=S.fig_mm(W,H);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off');labels=[]
groups=[
 ('EARTH DATA','raster → cube → rasterset','Fields and dated stacks; retain the scene.','TF.family'),
 ('COLLECT EVIDENCE','8 facts → one bundle handle','38 characters; members resolve separately.','CM.bundle'),
 ('REASONING CHECKPOINTS','located → routed → recalled → scored','4 stage addresses re-hashed offline.','CM.state'),
 ('FILES, IDENTITY AND EXECUTION','tree · entity · trace · track','Address chunks, subjects and recorded runs.','TF.family')]
for i,(head,kinds,why,claim) in enumerate(groups):
 y=i*21.5
 ax.add_patch(FancyBboxPatch((0,y+.5),W,20,boxstyle='round,pad=0,rounding_size=1',fc=S.C['emem_tint'] if i%2==0 else S.C['oos_bg'],ec='none'))
 for yy,s,pt,wt,col in [(y+4.1,head,14,700,S.C['emem']),(y+10,kinds,20,600,S.C['ink']),(y+16.5,why,15,400,S.C['ink2'])]:
  ax.text(4,yy,s,fontsize=pt,fontweight=wt,color=col,va='center');labels.append(dict(text=s,claim=claim,pt=pt))
S.save(fig,'f14_token_family')
Path(S.OUT,'f14_token_family.labels.json').write_text(json.dumps({'figure':'f14_token_family','size_mm':[W,H],'labels':labels},indent=2)+'\n')

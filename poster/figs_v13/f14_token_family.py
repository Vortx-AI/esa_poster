"""Purpose-led token families. Exact grammars and hash rules stay in the detail figure."""
import json,sys
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,86
fig=S.fig_mm(W,H);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off');labels=[]
groups=[('OBSERVATIONS','fact · derived value · absence','Recover a value and its derivation.'),
('EARTH DATA','raster · cube · rasterset','Recover a field or a series of fields.'),
('COLLECTIONS','bundle · tree','Group facts or address file chunks.'),
('IDENTITY AND PROCESS','entity · state · trace · track','Name an object, a reasoning stage or a run.')]
for i,(head,kinds,why) in enumerate(groups):
 y=i*21.5
 ax.add_patch(FancyBboxPatch((0,y+.5),W,20,boxstyle='round,pad=0,rounding_size=1',fc=S.C['emem_tint'] if i%2==0 else S.C['oos_bg'],ec='none'))
 for yy,s,pt,wt,col in [(y+4.1,head,14,700,S.C['emem']),(y+10,kinds,20,600,S.C['ink']),(y+16.5,why,15,400,S.C['ink2'])]:
  ax.text(4,yy,s,fontsize=pt,fontweight=wt,color=col,va='center');labels.append(dict(text=s,claim='TF.family',pt=pt))
S.save(fig,'f14_token_family')
Path(S.OUT,'f14_token_family.labels.json').write_text(json.dumps({'figure':'f14_token_family','size_mm':[W,H],'labels':labels},indent=1)+'\n')

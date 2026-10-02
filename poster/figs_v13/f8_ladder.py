"""What each verification layer establishes; detailed quantitative ladder in methods."""
import json,sys
from pathlib import Path
from matplotlib.patches import Rectangle
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,65
fig=S.fig_mm(W,H);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off')
labels=[]
rows=[('RECORD','Exact addressed bytes'),('BINDING','Requested place, time and product'),('ATTESTATION','Signature under the pinned key'),('DERIVATION','Declared computation reproduces'),('SOURCE READ','Named source supports the value')]
for i,(name,meaning) in enumerate(rows):
 y=i*13
 ax.add_patch(Rectangle((0,y),W,11.8,fc=S.C['emem_tint'] if i%2==0 else S.C['oos_bg'],ec='none'))
 for x,yy,s,pt,wt,col in [(3,y+6,name,14,700,S.C['emem']),(48,y+6,meaning,17,400,S.C['ink'])]:
  ax.text(x,yy,s,fontsize=pt,fontweight=wt,color=col,va='center');labels.append(dict(text=s,claim='U.boundary',pt=pt))
S.save(fig,'f8_ladder')
Path(S.OUT,'f8_ladder.labels.json').write_text(json.dumps({'figure':'f8_ladder','size_mm':[W,H],'labels':labels},indent=1)+'\n')

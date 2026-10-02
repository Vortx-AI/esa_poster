"""A drift taxonomy tied to the original examples and their checking layers.
Detailed incidents, fixes and precedents remain in the research evidence.
"""
import json,sys
from pathlib import Path
from matplotlib.patches import Rectangle
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,190
fig=S.fig_mm(W,H); ax=fig.add_axes([0,0,1,1]); ax.set(xlim=(0,W),ylim=(H,0)); ax.axis('off')
labels=[]
def T(x,y,s,claim='U.drift',size=17,color=None,weight=400):
    labels.append(dict(text=s,claim=claim,pt=size))
    ax.text(x,y,s,fontsize=size,color=color or S.C['ink'],fontweight=weight,va='center')
rows=[
 ('PLACE','Compare the requested cell','Coordinates keep the question anchored.','U.drift'),
 ('TIME','Bind the observation time','Requested day and returned day remain visible.','U.drift'),
 ('PRODUCT','Inspect the band and convention','Keep the product, grid and units explicit.','U.drift'),
 ('SOURCE PIXEL / SCENE','Re-read the named source','Test the scene and the containing pixel.','U.drift'),
 ('DERIVATION','Recompute from the recipe','Check inputs, parameters and offset rules.','U.drift'),
 ('VALUE REPRESENTATION','Resolve the exact record','0.47 and 0.4709 lead to different test decisions.','F.lost'),
 ('REFERENT','Retain the application identity','The place record accompanies the object meant.','U.drift'),
]
T(4,5,'WHAT MOVED',size=14,weight=600,color=S.C['ink2'])
T(94,5,'WHAT TO CHECK',size=14,weight=600,color=S.C['ink2'])
for i,(name,check,example,claim) in enumerate(rows):
    y=13+i*25
    ax.add_patch(Rectangle((0,y),W,23,fc=S.C['emem_tint'] if i%2==0 else S.C['oos_bg'],ec='none'))
    ax.add_patch(Rectangle((0,y),1.6,23,fc=S.C['emem'],ec='none'))
    T(5,y+5,name,size=17,weight=700,color=S.C['emem'])
    T(5,y+12,check,size=20,weight=600)
    T(5,y+19,example,claim,size=15)
S.save(fig,'f4_failure_ladder')
Path(S.OUT,'f4_failure_ladder.labels.json').write_text(json.dumps({'figure':'f4_failure_ladder','size_mm':[W,H],'labels':labels},indent=1)+'\n')

"""One transaction-time example, recomputed from the recorded Bengaluru history."""
import json,sys
from pathlib import Path
from datetime import datetime
from matplotlib.patches import Rectangle,FancyArrowPatch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,82
fig=S.fig_mm(W,H);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off');labels=[]
J=json.loads((Path(S.ROOT)/'research/repro/data/contra_bengaluru.json').read_text())['contradictions'][0]
AT=sorted(J['attestations'],key=lambda a:a['signed_at']);old=AT[0];new=next(a for a in AT if a['value']!=old['value'])
probe=[a for a in AT if a['signed_at']<='2026-06-15T00:00:00Z'][-1]
assert probe['value']==old['value']==918.0 and round(new['value'],2)==915.07
assert old['signed_at'].startswith('2026-05-28') and new['signed_at'].startswith('2026-08-11')
assert J['providers'][0]['fn_key'].startswith('open_meteo_copdem90m')
assert all(p['fn_key'].startswith('copernicus_dem_30m') for p in J['providers'][1:])
def T(x,y,s,size=17,color=None,weight=400,**kw):
 labels.append(dict(text=s,claim='MF.example',pt=size));ax.text(x,y,s,fontsize=size,color=color or S.C['ink'],fontweight=weight,va='center',**kw)
T(0,4,'BENGALURU · SAME CELL AND BAND · 2026',14,S.C['ink2'],600)
# One lookup branches to two immutable records; the query selects the older citation.
assert old['fact_cid'] != new['fact_cid']
T(W/2,13,'same place + band',16,S.C['emem'],600,ha='center')
for x in [45.75,147.75]:
 ax.add_patch(FancyArrowPatch((W/2,16.5),(x,21),arrowstyle='-|>',mutation_scale=10,color=S.C['emem'],lw=1.1))
for x,rec,date,provider,identity in [(0,old,'signed 28 May','Open-Meteo / DEM90','earlier CID'),(102,new,'signed 11 Aug','Copernicus DEM30','later CID')]:
 ax.add_patch(Rectangle((x,22),91.5,33,fc=S.C['oos_bg'] if x==0 else S.C['emem_tint'],ec='none'))
 T(x+4,27,date,14)
 T(x+4,37,f"{rec['value']:.1f} m" if x==0 else f"{rec['value']:.2f} m",26,S.C['emem'],600)
 T(x+4,46,provider,14)
 T(x+4,52,identity,14,S.C['ink2'])
ax.add_patch(Rectangle((0,59),W,12,fc=S.C['emem_tint'],ec='none'))
T(4,65,f"as of 15 Jun → {probe['value']:.1f} m",20,S.C['emem'],600)
T(0,78,'The next agent can recover the earlier citation.',17)
S.save(fig,'f9_timeline')
Path(S.OUT,'f9_timeline.labels.json').write_text(json.dumps({'figure':'f9_timeline','size_mm':[W,H],'labels':labels},indent=1)+'\n')

"""Compact EO history recovered from v12; observations, not an inferred vegetation trend."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,70
src=Path(S.ROOT)/'research/repro/v12/data/case_keylong_ndvi.json'
data=json.loads(src.read_text());rows=sorted([r for r in data['rows'] if '2025-01-01'<=r['observed_at']<'2027-01-01'],key=lambda r:r['observed_at'])
assert len(rows)==141 and len({r['fact_cid'] for r in rows})==141
assert all(r['verified'] and r['band']=='indices.ndvi' and r['scene'] for r in rows)
assert data['cell']=='defi.zb572.xoso.zb1ec'
selected=next(r for r in rows if r['fact_cid'].startswith('oj5cecci'))
assert selected['value']==0.4708994708994709 and selected['date']=='2026-09-25'
counts={p:sum(r['platform']==p for r in rows) for p in ['S2A','S2B','S2C']}
assert counts=={'S2A':15,'S2B':61,'S2C':65}
fig=S.fig_mm(W,H);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off');labels=[]
def T(x,y,s,size=14,col=None,weight=400,**kw):
 labels.append(dict(text=s,claim='V8.history',pt=size));ax.text(x,y,s,fontsize=size,color=col or S.C['ink'],fontweight=weight,va='center',**kw)
def ts(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
t0,t1=ts('2025-01-01T00:00:00Z'),ts('2026-10-01T00:00:00Z')
def X(r):return 18+171*(ts(r['observed_at'])-t0)/(t1-t0)
def Y(v):return 22+35*(.85-v)/.97
T(0,4,'KEYLONG · SENTINEL-2 L2A · 141 RECORDS',14,S.C['emem'],700)
styles={'S2A':('o','emem_light'),'S2B':('s','emem'),'S2C':('^','navy')}
for x,(p,(mk,c)) in zip([3,35,67],styles.items()):
 ax.scatter([x],[13],s=35,marker=mk,color=S.C[c]);T(x+5,13,p,14)
ax.scatter([108],[13],s=55,facecolor='none',edgecolor=S.C['incident'],lw=1.5)
T(113,13,'0.4709: handoff record',14,S.C['incident_text'])
for v in [0,.4,.8]:
 ax.plot([18,189],[Y(v)]*2,color=S.C['rule'],lw=.7)
 T(13,Y(v),f'{v:.1f}',14,S.C['ink2'],ha='right')
ax.plot([X(r) for r in rows],[Y(r['value']) for r in rows],color=S.C['oos'],lw=.7,zorder=1)
for p,(mk,c) in styles.items():
 rr=[r for r in rows if r['platform']==p]
 ax.scatter([X(r) for r in rr],[Y(r['value']) for r in rr],s=18,marker=mk,color=S.C[c],zorder=3)
ax.scatter([X(selected)],[Y(selected['value'])],s=105,facecolor='none',edgecolor=S.C['incident'],lw=1.7,zorder=4)
for date,label,ha in [('2025-01-01','Jan 2025','left'),('2025-07-01','Jul','center'),('2026-01-01','Jan 2026','center'),('2026-09-01','Sep','center')]:
 x=18+171*(ts(date+'T00:00:00Z')-t0)/(t1-t0);T(x,65,label,14,S.C['ink2'],ha=ha)
S.save(fig,'f17_ndvi_history')
Path(S.OUT,'f17_ndvi_history.labels.json').write_text(json.dumps({'figure':'f17_ndvi_history','size_mm':[W,H],'labels':labels},indent=2)+'\n')
evidence={'source':str(src.relative_to(S.ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'records':len(rows),'platform_counts':counts,'first_observation':rows[0]['observed_at'],'last_observation':rows[-1]['observed_at'],'highlighted_cid':selected['fact_cid'],'highlighted_value':selected['value'],'scope':'Retained records read on 30 September 2026. No new acquisition, cloud/snow mask, processing harmonisation or vegetation-trend attribution. Existing verified flags are retained evidence, not a fresh verification run.'}
Path(S.ROOT,'research/v13/evidence/v138/eo_history.json').write_text(json.dumps(evidence,indent=2)+'\n')

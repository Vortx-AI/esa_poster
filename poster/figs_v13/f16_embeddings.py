"""Archived foundation-model vectors, drawn directly from retained records."""
import json,sys
from pathlib import Path
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,53
fig=S.fig_mm(W,H);fig.set_dpi(300);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off');labels=[]
F={f['band']:f for f in json.loads((Path(S.ROOT)/'research/v13/evidence/critic/cell.json').read_text())['facts']}
p,g=F['prithvi_eo2'],F['geotessera']
assert len(p['value'])==1024 and p['served_via']['model_blake2b_hex']==p['derivation']['args']['args'][4]
assert len(g['value'])==128 and '/npy/v1/2024/' in g['sources'][0]['id']
cmap=LinearSegmentedColormap.from_list('record',['#FFFFFF',S.C['emem']])
def T(x,y,s,claim,size=17,weight=400,**kw):
 labels.append(dict(text=s,claim=claim,pt=size));ax.text(x,y,s,fontsize=size,fontweight=weight,va='center',**kw)
for i,(name,rec,foot,cid) in enumerate([('Prithvi',p,'checkpoint digest inside the record','V.prithvi'),('TESSERA',g,'product year 2024; no checkpoint digest','V.tessera')]):
 y=i*27
 T(0,y+4,name,cid,20,600);T(W,y+4,f"{len(rec['value']):,} values",cid,17,ha='right')
 a=np.asarray(rec['value']);lo,hi=np.percentile(a,[2,98]);z=np.clip((a-lo)/(hi-lo),0,1)[None,:]
 z=np.repeat(np.repeat(z,max(1,int(np.ceil(300*(W/25.4)/z.shape[1]))),axis=1),72,axis=0)
 ax.imshow(z,cmap=cmap,aspect='auto',interpolation='none',extent=(0,W,y+17,y+10))
 T(0,y+22,foot,cid,14)
S.save(fig,'f16_embeddings')
Path(S.OUT,'f16_embeddings.labels.json').write_text(json.dumps({'figure':'f16_embeddings','size_mm':[W,H],'labels':labels},indent=1)+'\n')

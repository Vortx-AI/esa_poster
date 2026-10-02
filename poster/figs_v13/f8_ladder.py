"""Two-sided boundary: checkable record properties and unestablished world claims."""
import json,sys
from pathlib import Path
from matplotlib.patches import Rectangle
sys.path.insert(0,str(Path(__file__).resolve().parent))
import style as S
W,H=193.5,65
fig=S.fig_mm(W,H);ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off')
labels=[]
for x,width,head,color,claim,lines in [
    (0,96,'CHECKABLE','emem_tint','V6.checkable',[
        'Record bytes + content identity','Declared cell, band, time','Attestation signature',
        'Declared derivation','Recorded history / as-of']),
    (99,94.5,'NOT ESTABLISHED','oos_bg','V6.limits',[
        'Sensor accuracy','Entity identity','Physical truth','Decision correctness','Source quality: inherited']),
]:
    ax.add_patch(Rectangle((x,0),width,58,fc=S.C[color],ec='none'))
    for y,text,pt,weight in [(7,head,17,700)]+[(18+i*8.4,line,16,400) for i,line in enumerate(lines)]:
        ax.text(x+3,y,text,fontsize=pt,fontweight=weight,color=S.C['ink'],va='center')
        labels.append(dict(text=text,claim=claim,pt=pt))
text='Run the corresponding checks; a content address alone is insufficient.'
ax.text(0,62,text,fontsize=14,color=S.C['ink2'],va='center')
labels.append(dict(text=text,claim='V6.checkable',pt=14))
S.save(fig,'f8_ladder')
Path(S.OUT,'f8_ladder.labels.json').write_text(json.dumps({'figure':'f8_ladder','size_mm':[W,H],'labels':labels},indent=1)+'\n')

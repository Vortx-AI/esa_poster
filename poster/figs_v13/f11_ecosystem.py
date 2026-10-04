"""A0 contribution-to-deployment bridge, generated entirely from evidenced routes."""
import json, sys
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ecosystem as E
W, H = 726, 65
rows = E.read_manifest()
errors = E.validate(rows)
assert not errors, '\n'.join(errors)
labels = E.labels_for(rows)
fig=S.fig_mm(W,H); ax=fig.add_axes([0,0,1,1]); ax.set(xlim=(0,W),ylim=(H,0)); ax.axis('off')
cards = sorted((r for r in rows if r.get('panel', {}).get('kind') == 'card'), key=lambda r: r['panel']['order'])
# v13.10 (issue #58): cards quote the real listings; the screenshots are kept as evidence, not printed (too small to read at A0)
for i,r in enumerate(cards):
    ax.add_patch(FancyBboxPatch((i*146,0),142,37.8,boxstyle='round,pad=0,rounding_size=1.5',
        fc=S.C['oos_bg' if r['status']=='REGISTRY' else 'emem_tint'],ec='none'))
for label in labels:
    ax.text(label['x'],label['y'],label['text'],fontsize=label['pt'],fontweight=label['weight'],fontstyle=label.get('style','normal'),color=S.C[label['color']],va='center')
S.save(fig,'f11_ecosystem')
Path(S.OUT,'f11_ecosystem.labels.json').write_text(json.dumps({'figure':'f11_ecosystem','size_mm':[W,H],'labels':labels},indent=2)+'\n')

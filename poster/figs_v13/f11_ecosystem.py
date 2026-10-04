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
# v13.10 (issue #58): the real listings, cropped from the authors' screenshots and drawn 1:1 at 300 ppi or more
import numpy as np
from PIL import Image
LIST = Path(S.ROOT) / 'research/v13/evidence/listings'
SHOT = {'chatgpt': ('chatgpt.png', (135, 0, 1300, 340)), 'claude-code-plugin': ('claude.png', (20, 0, 1700, 340)),
        'dify-marketplace': ('dify.png', (318, 190, 1870, 530)),
        'github-mcp-registry': ('github_mcp_registry.png', (520, 122, 1920, 462)),
        'clawhub': ('clawhub.png', (30, 20, 1700, 360))}
PPMM = 300 / 25.4
IMG_Y, IMG_H = 1.2, 23.0
for i,r in enumerate(cards):
    ax.add_patch(FancyBboxPatch((i*146,0),142,37.8,boxstyle='round,pad=0,rounding_size=1.5',
        fc=S.C['oos_bg' if r['status']=='REGISTRY' else 'emem_tint'],ec='none'))
    f, box = SHOT[r['id']]
    im = np.asarray(Image.open(LIST / f).convert('RGB').crop(box))
    h_px, w_px = im.shape[:2]
    assert h_px / IMG_H >= PPMM - 0.01, (f, h_px / IMG_H * 25.4)
    w_mm = w_px / (h_px / IMG_H)
    assert w_mm <= 139.6, (f, w_mm)
    x0 = i * 146 + (142 - w_mm) / 2
    ax.add_patch(FancyBboxPatch((x0 - 0.4, IMG_Y - 0.4), w_mm + 0.8, IMG_H + 0.8, boxstyle='round,pad=0,rounding_size=0.8',
                                fc='white', ec=S.C['rule'], lw=0.6, zorder=2))
    ax.imshow(im, extent=(x0, x0 + w_mm, IMG_Y + IMG_H, IMG_Y), interpolation='none', zorder=3)
ax.set(xlim=(0,W),ylim=(H,0))
for label in labels:
    ax.text(label['x'],label['y'],label['text'],fontsize=label['pt'],fontweight=label['weight'],color=S.C[label['color']],va='center')
S.save(fig,'f11_ecosystem')
Path(S.OUT,'f11_ecosystem.labels.json').write_text(json.dumps({'figure':'f11_ecosystem','size_mm':[W,H],'labels':labels},indent=2)+'\n')

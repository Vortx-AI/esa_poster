"""The seven-step EO workflow, drawn at its A0 print size (801 x 49 mm)."""
import json
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
import style as S

W, H = 801, 49
fig = S.fig_mm(W, H)
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=(0, W), ylim=(H, 0))
ax.axis('off')
labels = []

def text(x, y, value, pt, weight=400, color='ink'):
    labels.append(dict(text=value, claim='V9.workflow', x_mm=x, y_mm=y, pt=pt))
    ax.text(x, y, value, fontsize=pt, fontweight=weight, color='#FFFFFF' if color == 'white' else S.C[color], va='center')

text(0, 5, 'From observation to the next agent', 24, 600)
steps = [
    ('Observe', 'Satellite or sensor', 'Keep the source scene.'),
    ('Locate', 'Location · product · time', 'Lookup identity'),
    ('Record', 'Canonical record + CID', 'Batch attestation'),
    ('Hand off', 'Pass the reference', 'MCP · REST · A2A'),
    ('Resolve', 'Retrieve the same record', 'Recover its provenance.'),
    ('Check', 'Hash · binding · signature', 'Re-read source if needed.'),
    ('Continue', 'Reason with cited evidence', 'Carry the reference onward.'),
]
gap = 8
width = (W - gap * 6) / 7
for i, (verb, detail, scope) in enumerate(steps):
    x = i * (width + gap)
    ax.add_patch(FancyBboxPatch((x, 13), width, 35,
        boxstyle='round,pad=0,rounding_size=1.5',
        fc=S.C['emem' if verb == 'Hand off' else 'oos_bg' if i < 2 else 'emem_tint'], ec='none'))
    hand = verb == 'Hand off'   # v13.10: the handoff is the step emem exists for; it carries the strongest fill
    text(x + 4, 21, verb, 28, 700 if hand else 600, 'white' if hand else 'emem' if i >= 2 else 'ink')
    text(x + 4, 32, detail, 17, 500, 'white' if hand else 'ink')
    text(x + 4, 41, scope, 17, 400, 'white' if hand else 'ink2')

S.save(fig, 'f18_workflow')
Path(S.OUT, 'f18_workflow.labels.json').write_text(json.dumps({
    'figure': 'f18_workflow', 'size_mm': [W, H], 'labels': labels
}, indent=2) + '\n')

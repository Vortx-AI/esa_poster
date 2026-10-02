"""A0 community routes: names and useful actions at 24-28 pt.

Availability belongs to the manifest; experimental results belong to the
caption and linked client-path table. A listing is not a benchmark result.
"""
import json, sys
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S

W, H = 801, 91
root = Path(S.ROOT)
manifest = {r['id']: r for r in json.loads((root/'research/v13/ecosystem_manifest.json').read_text())}
cards = [
    ('chatgpt', 'ChatGPT', '@emem plugin', 'Enable emem; paste a token.'),
    ('claude-code-plugin', 'Claude', 'Code plugin · MCP connector', 'Resolve from a chat or terminal.'),
    ('vscode', 'Visual Studio Code', 'MCP gallery: @mcp emem', 'Install for Copilot agent mode.'),
    ('dify-marketplace', 'Dify', 'Marketplace plugin', 'Referent Lock · EUDR workflows'),
    ('mulesoft-exchange', 'Salesforce MuleSoft', 'Anypoint Exchange', 'Vortx AI MCP Server listing'),
]
fig=S.fig_mm(W,H); ax=fig.add_axes([0,0,1,1]); ax.set(xlim=(0,W),ylim=(H,0)); ax.axis('off'); labels=[]
def text(x,y,s,pt=20,weight=400,col='ink',claim='CM.routes'):
    ax.text(x,y,s,fontsize=pt,fontweight=weight,color=S.C[col],va='center')
    labels.append(dict(text=s,pt=pt,claim=claim))
gap=5; cw=(W-gap*4)/5
for i,(mid,name,how,why) in enumerate(cards):
    assert manifest[mid]['print']['allowed'] is True,mid
    x=i*(cw+gap)
    ax.add_patch(FancyBboxPatch((x,.5),cw,36,boxstyle='round,pad=0,rounding_size=1.5',fc=S.C['emem_tint'],ec='none'))
    text(x+5,8,name,28,600)
    text(x+5,20,how,22,500,'emem')
    text(x+5,30,why,18,400,'ink2')
for x,head,lines in [
    (0,'CONNECT', ['MCP · A2A · REST', 'Cursor · Gemini CLI']),
    (267,'BUILD', ['Python · TypeScript · self-hosted Docker', 'LangGraph · LlamaIndex · AutoGen · CrewAI · Mastra']),
    (534,'DISCOVER', ['GitHub MCP · Official MCP Registry', 'Glama · Smithery · Hugging Face · Context7 · ClawHub']),
]:
    text(x,47,head,17,600,'emem')
    text(x,57,lines[0],22,500)
    text(x,67,lines[1],18,400,'ink2')
ax.plot([0,W],[76,76],color=S.C['rule'],lw=1)
text(0,84,'Carry the token → resolve the record → check the evidence → continue in another agent.',24,600,'emem','CM.exercise')
S.save(fig,'f11_ecosystem')
Path(S.OUT,'f11_ecosystem.labels.json').write_text(json.dumps({'figure':'f11_ecosystem','size_mm':[W,H],'labels':labels},indent=2)+'\n')

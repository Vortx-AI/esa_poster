"""Manifest-backed A0 ecosystem copy and fail-closed release checks (stdlib only)."""
import datetime as dt
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'research/v13/ecosystem_manifest.json'
STATUSES = {'LIVE', 'PROTOCOL', 'REGISTRY', 'EXAMPLE', 'EXPERIMENTAL', 'ROADMAP', 'NOT FOUND'}
REQUIRED = {'chatgpt', 'claude-code-plugin', 'dify-marketplace', 'a2a', 'mcp-core',
            'official-mcp-registry', 'github-mcp-registry', 'github-repo', 'glama',
            'vscode', 'cursor', 'cline', 'gemini-cli', 'python-sdk', 'ts-sdk',
            'rest-openapi', 'docker', 'langchain', 'llamaindex', 'crewai', 'autogen',
            'mastra', 'agno', 'semantic-kernel'}
GROUPS = [('clients', 'MORE CLIENTS', 0), ('protocols', 'PROTOCOLS', 116),
          ('developer', 'DEVELOPER', 248), ('examples', 'FRAMEWORK EXAMPLES', 410),
          ('discovery', 'DISCOVERY / MIRRORS', 562)]


def read_manifest():
    return json.loads(MANIFEST.read_text())


def labels_for(rows):
    labels = []
    def add(text, x, y, pt, weight=400, color='ink', ids=(), claim='CM.routes'):
        labels.append(dict(text=text, x=x, y=y, pt=pt, weight=weight, color=color,
                           integrations=list(ids), claim=claim))
    cards = sorted((r for r in rows if r.get('panel', {}).get('kind') == 'card'), key=lambda r: r['panel']['order'])
    for i, r in enumerate(cards):
        # v13.10: each card carries the real listing as a cropped screenshot (research/v13/evidence/listings/);
        # the printed copy below it is one name line and one action line
        p = r['panel']; x = i * 146 + 3
        add(f"{p['label']} · {p['mechanism']}", x, 28.8, 17, 600, 'emem' if r['status'] != 'REGISTRY' else 'ink', [r['id']])
        add(p['action'], x, 34.6, 14, 400, 'ink2', [r['id']])
    for group, title, x in GROUPS:
        add(title, x, 42.8, 17, 600, 'emem')
        for line in (0, 1, 2):
            rs = sorted((r for r in rows if r.get('panel', {}).get('group') == group and r['panel']['line'] == line), key=lambda r: r['panel']['order'])
            if rs:
                add(' · '.join(r['panel']['label'] for r in rs), x, 50.8 + 8.0 * line,
                    16 if group == 'discovery' else 18, ids=[r['id'] for r in rs])
    return labels


def validate(rows, today=None, svg_texts=None):
    today = today or dt.date.today()
    errors = []
    ids = [r.get('id') for r in rows]
    if len(ids) != len(set(ids)):
        errors.append('duplicate integration id')
    for missing in sorted(REQUIRED - set(ids)):
        errors.append('required integration missing: ' + missing)
    for r in rows:
        rid = str(r.get('id'))
        for field in ('platform', 'mechanism', 'url', 'status', 'verified_utc', 'user_can', 'evidence'):
            if not r.get(field):
                errors.append(f'{rid}: missing {field}')
        if r.get('status') not in STATUSES:
            errors.append(f'{rid}: unknown status')
        if not str(r.get('url', '')).startswith('https://'):
            errors.append(f'{rid}: URL must be an explicit HTTPS destination')
        try:
            age = (today - dt.date.fromisoformat(r['verified_utc'][:10])).days
            if age < 0 or age > 28:
                errors.append(f'{rid}: verification age {age} days; refresh within 28 days')
        except (KeyError, TypeError, ValueError):
            errors.append(f'{rid}: invalid verification date')
        p = r.get('panel')
        if not p:
            continue
        if r.get('print', {}).get('allowed') is not True:
            errors.append(f'{rid}: panel row is not approved for print')
        if r.get('status') in {'EXPERIMENTAL', 'ROADMAP', 'NOT FOUND'}:
            errors.append(f'{rid}: unready integration belongs in the qualified companion directory')
        if p.get('kind') == 'card':
            for field in ('label', 'mechanism', 'action', 'order'):
                if field not in p or p[field] == '':
                    errors.append(f'{rid}: card missing {field}')
            if r.get('status') == 'REGISTRY' and 'listing' not in p.get('mechanism', '').lower():
                errors.append(f'{rid}: directory card must say listing')
        elif p.get('kind') == 'line':
            if p.get('group') not in {g for g, _, _ in GROUPS} or p.get('line') not in (0, 1, 2) or not p.get('label'):
                errors.append(f'{rid}: invalid group/line/label')
            if r.get('status') == 'EXAMPLE' and p.get('group') != 'examples':
                errors.append(f'{rid}: example must be under FRAMEWORK EXAMPLES')
            if r.get('status') == 'REGISTRY' and p.get('group') != 'discovery':
                errors.append(f'{rid}: directory must be under DISCOVERY / MIRRORS')
        else:
            errors.append(f'{rid}: unknown panel kind')
    cards = [r['panel']['order'] for r in rows if r.get('panel', {}).get('kind') == 'card']
    if sorted(cards) != list(range(5)):
        errors.append('primary cards must have unique positions 0 to 4')
    if not errors and svg_texts is not None:
        expected = [l['text'] for l in labels_for(rows)]
        if svg_texts != expected:
            errors.append('ecosystem SVG text differs from manifest-generated labels; regenerate the figure')
    return errors


def svg_texts(path):
    return [''.join(e.itertext()) for e in ET.parse(path).getroot().iter() if e.tag.endswith('}text')]


def check_release():
    rows = read_manifest()
    errors = validate(rows, svg_texts=svg_texts(ROOT / 'poster/fig/v13/f11_ecosystem.svg'))
    if errors:
        raise ValueError('\n'.join(errors))
    return f'{len(rows)} evidenced routes; {sum(bool(r.get("panel")) for r in rows)} printed; dates, types and exact SVG copy checked'


if __name__ == '__main__':
    print(check_release())

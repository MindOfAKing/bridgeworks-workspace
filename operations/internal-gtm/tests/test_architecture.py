from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8'))

def test_roles():
    d=load('role-registry.yaml')
    assert d['version']==1
    assert len(d['roles'])>=12
    ids=[r['id'] for r in d['roles']]
    assert len(ids)==len(set(ids))
    for r in d['roles']:
        for k in ('name','mission','inputs','outputs','authority','kpis','capabilities'):
            assert k in r

def test_routing():
    d=load('routing-policy.yaml')
    assert any(r['task']=='skill_agent_engineering' and r['default']=='claude_code' for r in d['routes'])
    assert any(r['task']=='browser_shutdown_or_console_action' and r.get('approval_required') for r in d['routes'])

def test_geo_reuse():
    d=load('role-registry.yaml')
    refs={c for r in d['roles'] for c in r['capabilities']}
    assert 'geo-audit' in refs

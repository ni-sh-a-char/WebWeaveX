from __future__ import annotations

def build_architecture_knowledge(arch: dict):
    styles=sorted(set(arch.get('styles',[])))
    rels=[{"from":e.get('from',''),"to":e.get('to','')} for e in arch.get('relationships',[]) if isinstance(e,dict) and e.get('from') and e.get('to')]
    return {"nodes":styles+sorted(set([x for e in rels for x in (e['from'],e['to'])])),"edges":sorted(rels,key=lambda e:(e['from'],e['to']))}

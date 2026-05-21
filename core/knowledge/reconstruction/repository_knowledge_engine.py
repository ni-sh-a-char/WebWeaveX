from __future__ import annotations

def build_repository_knowledge(repo: dict):
    nodes=sorted(set(repo.get('symbols',[])+repo.get('dependencies',[])+repo.get('frameworks',[])))
    edges=[{"from":nodes[i],"to":nodes[i+1]} for i in range(max(0,len(nodes)-1))]
    return {"nodes":nodes,"edges":edges}

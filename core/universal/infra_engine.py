from __future__ import annotations

def parse_infra(text: str):
    src = (text or '').lower()
    infra = []
    for k in ['terraform', 'kubernetes', 'helm', 'dockerfile', 'compose']:
        if k in src:
            infra.append(k)
    return {"infra_components": sorted(set(infra))}

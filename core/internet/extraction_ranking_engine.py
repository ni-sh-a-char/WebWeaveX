from __future__ import annotations

def rank_extractions(results: list[dict]):
    def score(r: dict):
        txt = r.get('raw_text', '') or ''
        g = r.get('relationships', {}).get('execution_graph', {}) if isinstance(r, dict) else {}
        return (-(len(txt)), -(len(g.get('edges', []))), str(r.get('source_url', '')))
    return sorted(results or [], key=score)

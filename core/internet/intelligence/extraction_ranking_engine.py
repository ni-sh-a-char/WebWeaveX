from __future__ import annotations

def rank_extraction_results(results: list[dict]):
    def key(r: dict):
        txt = len((r or {}).get('raw_text',''))
        edges = len((r or {}).get('relationships',{}).get('execution_graph',{}).get('edges',[]))
        return (-txt, -edges, str((r or {}).get('source_url','')))
    return sorted(results or [], key=key)

from __future__ import annotations

def extraction_diagnostics(result: dict):
    return {
        'raw_text_bytes': len((result.get('raw_text','') or '').encode('utf-8')),
        'graph_edges': len(result.get('relationships',{}).get('execution_graph',{}).get('edges',[])),
        'has_repository': bool(result.get('content',{}).get('repository')),
        'has_documents': bool(result.get('content',{}).get('documents')),
    }

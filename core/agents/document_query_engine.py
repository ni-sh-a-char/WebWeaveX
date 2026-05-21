from __future__ import annotations

def query_document(result: dict, key: str = ''):
    docs=result.get('content',{}).get('documents',{})
    return docs if not key else docs.get(key)

from __future__ import annotations

def query_repository(result: dict, key: str = ''):
    repo=result.get('content',{}).get('repository',{})
    return repo if not key else repo.get(key)

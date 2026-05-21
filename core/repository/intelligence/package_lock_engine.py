from __future__ import annotations

def detect_locks(text: str):
    src=(text or '').lower()
    locks=[]
    for k in ['package-lock.json','pnpm-lock.yaml','yarn.lock','poetry.lock','cargo.lock','pubspec.lock']:
        if k in src: locks.append(k)
    return sorted(set(locks))

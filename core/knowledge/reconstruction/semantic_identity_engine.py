from __future__ import annotations
import hashlib

def build_semantic_identity(name: str):
    n=(name or '').strip().lower()
    return {"name": n, "identity": hashlib.sha256(n.encode('utf-8')).hexdigest()[:24]}

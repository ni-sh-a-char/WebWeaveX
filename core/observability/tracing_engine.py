from __future__ import annotations
import hashlib

def deterministic_trace(seed: str):
    s=seed or 'webweavex'
    return {'trace_id': hashlib.sha256(s.encode('utf-8')).hexdigest()[:32]}

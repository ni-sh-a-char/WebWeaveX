from __future__ import annotations
def freshness_score(old_hash:str,new_hash:str):
    return 0 if old_hash==new_hash else 1

from __future__ import annotations
def dedup_contents(items:list):
    seen=set(); out=[]
    for i in items or []:
        if i not in seen: seen.add(i); out.append(i)
    return out

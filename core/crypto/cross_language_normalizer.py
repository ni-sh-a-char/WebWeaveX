from __future__ import annotations

def normalize_value(v):
    if isinstance(v,float): return float(f"{v:.12g}")
    if isinstance(v,list): return [normalize_value(x) for x in v]
    if isinstance(v,dict): return {k: normalize_value(v[k]) for k in sorted(v.keys())}
    return v

from __future__ import annotations

def parse_robots(text: str):
    allow=[]; deny=[]
    for ln in (text or '').splitlines():
        x=ln.strip()
        lx=x.lower()
        if lx.startswith('allow:'): allow.append(x.split(':',1)[1].strip())
        if lx.startswith('disallow:'): deny.append(x.split(':',1)[1].strip())
    return {"allow": sorted(set(allow)), "deny": sorted(set(deny))}

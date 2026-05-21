from __future__ import annotations

def semantic_priority(url: str):
    u=(url or '').lower(); score=0
    if '/docs' in u: score+=3
    if 'api' in u: score+=2
    if 'github.com' in u: score+=2
    return {"score": score}

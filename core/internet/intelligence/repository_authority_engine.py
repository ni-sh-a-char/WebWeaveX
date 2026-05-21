from __future__ import annotations

def score_repository_authority(url: str, stars: int = 0, forks: int = 0):
    u = (url or '').lower()
    base = 0.2
    if 'github.com' in u: base += 0.2
    score = base + min(0.3, stars / 100000.0) + min(0.3, forks / 50000.0)
    return {"score": round(min(1.0, score), 6)}

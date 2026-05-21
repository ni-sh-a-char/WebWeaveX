from __future__ import annotations

from typing import Dict, List


_AUTHORITY_DOMAINS = (
    "github.com",
    "docs.python.org",
    "kubernetes.io",
    "pypi.org",
    "npmjs.com",
    "stackoverflow.com",
    "readthedocs.io",
)


def score_authority(url: str) -> Dict[str, object]:
    u = (url or "").lower()
    score = 0.4
    evidence = ["baseline"]
    if u.startswith("https://"):
        score += 0.15
        evidence.append("tls")
    matched = [d for d in _AUTHORITY_DOMAINS if d in u]
    if matched:
        score += 0.35
        evidence.append("known_authority_domain")
    if "localhost" in u or "127.0.0.1" in u:
        score = 0.0
        evidence = ["blocked_local"]
    authority_score = round(min(1.0, max(0.0, score)), 3)
    return {
        "url": url,
        "authority_score": authority_score,
        "score": authority_score,
        "evidence": evidence,
        "basis": {"tls": u.startswith("https://"), "known_domain": bool(matched)},
        "deterministic_inputs": sorted([f"url={u[:80]}", f"matched_domains={matched}"]),
    }


def rank_by_authority(urls: List[str]) -> List[Dict[str, object]]:
    scored = [score_authority(u) for u in urls or []]
    return sorted(scored, key=lambda x: (-x["authority_score"], x["url"]))

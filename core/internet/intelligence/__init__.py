"""Compatibility shim — canonical internet intelligence is core.internet."""

from core.internet import (
    canonicalize_sources as canonicalize_source_set,
    compute_freshness as score_freshness,
    compute_trust as score_trust,
    merge_sources as merge_semantic_sources,
    prioritize_sources as rank_crawl_priority,
    resolve_duplicates as resolve_duplicate_sources,
    semantic_similarity,
)
from core.internet.authority_engine import rank_by_authority
from core.internet.extraction_ranking_engine import rank_extractions as rank_extraction_results

score_repository_authority = lambda url: rank_by_authority([url])[0] if url else {"authority_score": 0.0}

__all__ = [
    "canonicalize_source_set",
    "score_trust",
    "score_freshness",
    "resolve_duplicate_sources",
    "semantic_similarity",
    "merge_semantic_sources",
    "rank_crawl_priority",
    "rank_extraction_results",
    "score_repository_authority",
]

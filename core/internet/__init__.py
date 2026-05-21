from .authority_engine import rank_by_authority, score_authority
from .canonical_source_engine import canonicalize_sources
from .citation_chain_engine import extract_citation_chain
from .contradiction_engine import detect_contradictions
from .crawl_priority_engine import prioritize_sources
from .duplicate_resolution_engine import resolve_duplicates
from .evidence_weight_engine import weight_evidence
from .extraction_ranking_engine import rank_extractions
from .semantic_similarity_engine import semantic_similarity
from .freshness_engine import compute_freshness
from .generated_content_detection_engine import detect_generated_content
from .lineage_engine import build_source_lineage
from .merge_engine import merge_sources
from .mirror_detection_engine import detect_mirrors
from .semantic_dedup_engine import semantic_dedup
from .source_clustering_engine import cluster_sources
from .source_ranking_engine import rank_sources
from .trust_engine import compute_trust

__all__ = [
    "canonicalize_sources",
    "rank_sources",
    "resolve_duplicates",
    "semantic_dedup",
    "compute_freshness",
    "compute_trust",
    "prioritize_sources",
    "rank_extractions",
    "score_authority",
    "rank_by_authority",
    "detect_contradictions",
    "cluster_sources",
    "detect_mirrors",
    "build_source_lineage",
    "merge_sources",
    "detect_generated_content",
    "extract_citation_chain",
    "weight_evidence",
    "semantic_similarity",
]

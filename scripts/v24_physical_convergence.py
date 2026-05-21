#!/usr/bin/env python3
"""V24 physical convergence: flatten version namespaces into canonical trees."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"

# (src_rel, dst_rel) — copy if dst missing
REPOSITORY_MOVES = [
    ("repository/architecture_v2/event_topology_engine.py", "repository/event_topology_engine.py"),
    ("repository/architecture_v2/distributed_graph_engine.py", "repository/distributed_graph_engine.py"),
    ("repository/architecture_v2/domain_reconstruction_engine.py", "repository/domain_reconstruction_engine.py"),
    ("repository/architecture_v2/ownership_engine.py", "repository/ownership_inference_engine.py"),
    ("repository/architecture_v2/infrastructure_mapping_engine.py", "repository/infra_topology_engine.py"),
]

DOCUMENT_MOVES = [
    ("documents/intelligence_v4/semantic_section_engine.py", "documents/semantic_section_engine.py"),
    ("documents/intelligence_v4/tutorial_flow_engine.py", "documents/tutorial_reasoning_engine.py"),
    ("documents/intelligence_v4/concept_dependency_engine.py", "documents/concept_graph_engine.py"),
    ("documents/intelligence_v4/reference_resolution_engine.py", "documents/entity_resolution_engine.py"),
    ("documents/intelligence_v4/semantic_chunk_engine.py", "documents/semantic_chunk_engine.py"),
    ("documents/intelligence_v4/code_context_engine.py", "documents/code_reference_engine.py"),
    ("documents/intelligence_v4/architecture_docs_engine.py", "documents/architecture_document_engine.py"),
    ("documents/intelligence_v4/api_contract_engine.py", "documents/api_documentation_engine.py"),
    ("documents/intelligence_v4/knowledge_synthesis_engine.py", "documents/knowledge_synthesis_engine.py"),
]

UNIVERSAL_FLATTEN = [
    ("universal/v2/universal_parser_engine.py", "universal/universal_parser_engine.py"),
    ("universal/v2/binary_metadata_engine.py", "universal/binary_metadata_engine.py"),
    ("universal/v2/archive_intelligence_engine.py", "universal/archive_intelligence_engine.py"),
    ("universal/v2/package_intelligence_engine.py", "universal/package_intelligence_engine.py"),
    ("universal/v2/api_surface_engine_v2.py", "universal/api_surface_engine.py"),
    ("universal/v2/protocol_intelligence_engine.py", "universal/protocol_intelligence_engine.py"),
    ("universal/v2/media_structure_engine.py", "universal/media_structure_engine.py"),
    ("universal/v2/structured_payload_engine.py", "universal/structured_payload_engine.py"),
    ("universal/v3/adaptive_parser_engine.py", "universal/adaptive_parser_engine.py"),
    ("universal/v3/binary_boundary_engine.py", "universal/binary_boundary_engine.py"),
    ("universal/v3/format_router_engine.py", "universal/format_router_engine.py"),
    ("universal/v3/semantic_payload_engine.py", "universal/semantic_payload_engine.py"),
    ("universal/v3/structured_payload_engine.py", "universal/structured_payload_v3_engine.py"),
    ("universal/v4/openapi_engine.py", "universal/openapi_engine.py"),
    ("universal/v4/graphql_engine.py", "universal/graphql_engine.py"),
    ("universal/v4/protobuf_engine.py", "universal/protobuf_engine.py"),
    ("universal/v4/notebook_engine.py", "universal/notebook_engine.py"),
    ("universal/v4/cicd_engine.py", "universal/cicd_engine.py"),
    ("universal/v4/infra_engine.py", "universal/infra_engine.py"),
    ("universal/v4/archive_engine.py", "universal/archive_inspection_engine.py"),
    ("universal/v4/binary_boundary_engine.py", "universal/binary_boundary_v4_engine.py"),
]

DISTRIBUTED_FLATTEN = [
    ("distributed/v2/distributed_frontier_v2_engine.py", "distributed/distributed_frontier_v2_engine.py"),
    ("distributed/v2/crawl_priority_engine.py", "distributed/crawl_priority_engine.py"),
    ("distributed/v2/crawl_diff_v2_engine.py", "distributed/crawl_diff_v2_engine.py"),
    ("distributed/v2/freshness_v2_engine.py", "distributed/freshness_v2_engine.py"),
    ("distributed/v2/shard_balancer_engine.py", "distributed/shard_balancer_engine.py"),
    ("distributed/v2/recursive_dedup_engine.py", "distributed/recursive_dedup_engine.py"),
    ("distributed/v2/crawl_checkpoint_v2_engine.py", "distributed/crawl_checkpoint_v2_engine.py"),
    ("distributed/v2/crawl_resume_v2_engine.py", "distributed/crawl_resume_v2_engine.py"),
    ("distributed/v2/crawl_persistence_v2_engine.py", "distributed/crawl_persistence_v2_engine.py"),
]

CRAWLING_FLATTEN = [
    ("crawling/v3/semantic_recursion_engine.py", "crawling/semantic_recursion_engine.py"),
    ("crawling/v3/bounded_recursion_engine.py", "crawling/bounded_recursion_engine.py"),
    ("crawling/v3/traversal_priority_engine.py", "crawling/traversal_priority_engine.py"),
    ("crawling/v3/crawl_persistence_engine.py", "crawling/crawl_persistence_v3_engine.py"),
    ("crawling/v3/crawl_checkpoint_engine.py", "crawling/crawl_checkpoint_v3_engine.py"),
    ("crawling/v3/crawl_resume_engine.py", "crawling/crawl_resume_v3_engine.py"),
]

SHIM_ONLY_DIRS = [
    "graph/v6", "graph/v7", "serialize/v4", "serialize/v5",
    "crypto/v2", "crypto/v3", "llm/v2", "llm/v3", "llm/v4",
    "repository/architecture_v2", "documents/intelligence_v4",
    "universal/v2", "universal/v3", "universal/v4",
    "distributed/v2", "crawling/v3", "knowledge/v2",
]

SHIM_CONTENT = {
    "repository/architecture_v2": '''"""Shim — canonical repository engines."""
from core.repository.service_boundary_engine import infer_service_boundaries
from core.repository.event_topology_engine import infer_event_topology
from core.repository.runtime_topology_engine import infer_runtime_topology
from core.repository.distributed_graph_engine import build_distributed_graph
from core.repository.domain_reconstruction_engine import reconstruct_domain_model
from core.repository.ownership_inference_engine import infer_ownership
from core.repository.infra_topology_engine import map_infrastructure
__all__ = [
    "infer_service_boundaries", "infer_event_topology", "infer_runtime_topology",
    "build_distributed_graph", "reconstruct_domain_model", "infer_ownership", "map_infrastructure",
]
''',
    "documents/intelligence_v4": '''"""Shim — canonical document engines."""
from core.documents.semantic_section_engine import extract_semantic_sections
from core.documents.tutorial_reasoning_engine import extract_tutorial_flow
from core.documents.concept_graph_engine import build_concept_dependencies
from core.documents.entity_resolution_engine import resolve_references
from core.documents.semantic_chunk_engine import build_semantic_chunks
from core.documents.code_reference_engine import extract_code_context
from core.documents.architecture_document_engine import extract_architecture_docs
from core.documents.api_documentation_engine import extract_api_contract_docs
from core.documents.knowledge_synthesis_engine import synthesize_knowledge
__all__ = [
    "extract_semantic_sections", "extract_tutorial_flow", "build_concept_dependencies",
    "resolve_references", "build_semantic_chunks", "extract_code_context",
    "extract_architecture_docs", "extract_api_contract_docs", "synthesize_knowledge",
]
''',
    "universal/v2": '''"""Shim — core.universal canonical."""
from core.universal.universal_parser_engine import parse_universal_payload
from core.universal.binary_metadata_engine import extract_binary_metadata
from core.universal.archive_intelligence_engine import extract_archive_intelligence
from core.universal.package_intelligence_engine import extract_package_intelligence
from core.universal.api_surface_engine import extract_api_surface_v2
from core.universal.protocol_intelligence_engine import detect_protocol_intelligence
from core.universal.media_structure_engine import extract_media_structure
from core.universal.structured_payload_engine import extract_structured_payload
''',
    "universal/v3": '''"""Shim — core.universal canonical."""
from core.universal.adaptive_parser_engine import parse_adaptive
from core.universal.binary_boundary_engine import detect_binary_boundary
from core.universal.format_router_engine import route_format
from core.universal.semantic_payload_engine import parse_semantic_payload
from core.universal.structured_payload_v3_engine import parse_structured_payload
''',
    "universal/v4": '''"""Shim — core.universal canonical."""
from core.universal.archive_inspection_engine import inspect_archive
from core.universal.binary_boundary_v4_engine import inspect_binary_boundary
from core.universal.cicd_engine import parse_cicd
from core.universal.graphql_engine import parse_graphql
from core.universal.infra_engine import parse_infra
from core.universal.notebook_engine import parse_notebook
from core.universal.openapi_engine import parse_openapi
from core.universal.protobuf_engine import parse_protobuf
''',
    "distributed/v2": '''"""Shim — core.distributed canonical."""
from core.distributed.distributed_frontier_v2_engine import build_distributed_frontier_v2
from core.distributed.crawl_priority_engine import prioritize_crawl_frontier
from core.distributed.crawl_diff_v2_engine import compute_crawl_diff_v2
from core.distributed.freshness_v2_engine import compute_freshness_v2
from core.distributed.shard_balancer_engine import balance_shards_deterministically
from core.distributed.recursive_dedup_engine import recursive_dedup
from core.distributed.crawl_checkpoint_v2_engine import create_crawl_checkpoint_v2
from core.distributed.crawl_resume_v2_engine import resume_crawl_v2
from core.distributed.crawl_persistence_v2_engine import serialize_crawl_state_v2
''',
    "crawling/v3": '''"""Shim — core.crawling canonical."""
from core.crawling.semantic_recursion_engine import recursive_extract_v3
from core.crawling.bounded_recursion_engine import recursion_guard_v3
from core.crawling.traversal_priority_engine import prioritize_traversal_v3
from core.crawling.crawl_persistence_v3_engine import persist_crawl_state_v3
from core.crawling.crawl_checkpoint_v3_engine import checkpoint_crawl_v3
from core.crawling.crawl_resume_v3_engine import resume_crawl_v3
''',
    "knowledge/v2": '''"""Shim — core.knowledge canonical."""
from core.knowledge.reconstruction.entity_resolution_engine import resolve_entities
from core.knowledge.reconstruction.concept_graph_engine import build_concept_graph
from core.knowledge.v2.semantic_relationship_engine import build_semantic_relationships
from core.knowledge.v2.repository_knowledge_engine import build_repository_knowledge_v2
from core.knowledge.v2.document_knowledge_engine import build_document_knowledge_v2
from core.knowledge.v2.internet_knowledge_engine import build_internet_knowledge_v2
from core.knowledge.v2.architecture_knowledge_engine import build_architecture_knowledge_v2
''',
}


def copy_if_missing(src_rel: str, dst_rel: str, moved: list[str]) -> None:
    src = CORE / src_rel
    dst = CORE / dst_rel
    if not src.exists():
        return
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    moved.append(dst_rel)


def delete_dir_bodies(rel: str, keep_init: bool = True) -> list[str]:
    removed = []
    d = CORE / rel
    if not d.exists():
        return removed
    for py in d.glob("*.py"):
        if keep_init and py.name == "__init__.py":
            continue
        py.unlink()
        removed.append(str(py.relative_to(ROOT)))
    return removed


def main() -> None:
    moved: list[str] = []
    for src, dst in REPOSITORY_MOVES + DOCUMENT_MOVES + UNIVERSAL_FLATTEN + DISTRIBUTED_FLATTEN + CRAWLING_FLATTEN:
        copy_if_missing(src, dst, moved)

    removed: list[str] = []
    for rel in SHIM_ONLY_DIRS:
        removed.extend(delete_dir_bodies(rel))
        shim = SHIM_CONTENT.get(rel)
        if shim:
            (CORE / rel / "__init__.py").write_text(shim, encoding="utf-8")

    # graph v6 bodies
    for rel in ["graph/v6", "graph/v7"]:
        removed.extend(delete_dir_bodies(rel))

    # knowledge v2 bodies except shim will reference reconstruction — copy relationship engines first
    for src, dst in [
        ("knowledge/v2/semantic_relationship_engine.py", "knowledge/semantic_relationship_v2_engine.py"),
        ("knowledge/v2/repository_knowledge_engine.py", "knowledge/repository_knowledge_v2_engine.py"),
        ("knowledge/v2/document_knowledge_engine.py", "knowledge/document_knowledge_v2_engine.py"),
        ("knowledge/v2/internet_knowledge_engine.py", "knowledge/internet_knowledge_v2_engine.py"),
        ("knowledge/v2/architecture_knowledge_engine.py", "knowledge/architecture_knowledge_v2_engine.py"),
    ]:
        copy_if_missing(src, dst, moved)

    # update knowledge v2 shim imports
    SHIM_CONTENT["knowledge/v2"] = '''"""Shim — core.knowledge canonical."""
from core.knowledge.reconstruction.entity_resolution_engine import resolve_entities
from core.knowledge.reconstruction.concept_graph_engine import build_concept_graph
from core.knowledge.semantic_relationship_v2_engine import build_semantic_relationships
from core.knowledge.repository_knowledge_v2_engine import build_repository_knowledge_v2
from core.knowledge.document_knowledge_v2_engine import build_document_knowledge_v2
from core.knowledge.internet_knowledge_v2_engine import build_internet_knowledge_v2
from core.knowledge.architecture_knowledge_v2_engine import build_architecture_knowledge_v2
'''
    (CORE / "knowledge/v2/__init__.py").write_text(SHIM_CONTENT["knowledge/v2"], encoding="utf-8")
    delete_dir_bodies("knowledge/v2")

    print(f"moved/copied {len(moved)} modules")
    print(f"removed {len(removed)} files")


if __name__ == "__main__":
    main()

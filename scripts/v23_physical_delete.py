#!/usr/bin/env python3
"""Physically remove obsolete duplicate module bodies (keep shim __init__.py)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"

# (directory relative to core, keep __init__.py only)
SHIM_DIRS = [
    "graph/v6",
    "graph/v7",
    "serialize/v4",
    "serialize/v5",
    "crypto/v2",
    "crypto/v3",
    "performance/v2",
    "security/v4",
]

# delete all .py except listed keep files
PARTIAL_DELETE = {
    "documents/intelligence_v3": ["__init__.py"],
    "repository/intelligence_v3": ["__init__.py", "ast_normalization_engine.py"],
}

DOCUMENTS_V3_SHIM = '''"""Shim — canonical document intelligence in core.documents."""
from core.documents.intelligence.semantic_outline_engine import extract_semantic_outline as semantic_hierarchy
from core.documents.intelligence.toc_engine import build_toc
from core.documents.intelligence.citation_engine import extract_citations
from core.documents.intelligence.cross_reference_engine import extract_cross_refs as extract_cross_references
from core.documents.intelligence_v4.semantic_section_engine import extract_semantic_sections
from core.documents.intelligence_v4.semantic_chunk_engine import build_semantic_chunks

__all__ = [
    "semantic_hierarchy",
    "build_toc",
    "extract_citations",
    "extract_cross_references",
    "extract_semantic_sections",
    "build_semantic_chunks",
]
'''

# entire package -> replace with shim __init__ only
REPLACE_WITH_SHIM = {
    "graph_intelligence": '''"""Shim — use core.graph."""
from core.graph import (
    compress_graph,
    export_graph,
    query_edges,
    query_nodes,
    reason_topology,
    reconstruct_graph,
)
from core.graph.topology_reasoning_engine import reason_topology as graph_reasoning
from core.graph.graph_reconstruction_engine import reconstruct_graph as graph_clustering

graph_similarity = reason_topology
__all__ = ["graph_reasoning", "graph_similarity", "graph_clustering", "reconstruct_graph"]
''',
}


def partial_delete(rel: str, keep: list[str], removed: list[str]) -> None:
    d = CORE / rel
    if not d.exists():
        return
    for py in d.glob("*.py"):
        if py.name in keep:
            continue
        py.unlink()
        removed.append(str(py.relative_to(ROOT)))


def main():
    removed = []
    for rel, keep in PARTIAL_DELETE.items():
        partial_delete(rel, keep, removed)
        if rel == "documents/intelligence_v3":
            (CORE / rel / "__init__.py").write_text(DOCUMENTS_V3_SHIM, encoding="utf-8")

    for rel in SHIM_DIRS:
        d = CORE / rel.replace("/", "\\") if "\\" in str(CORE) else CORE / rel
        if not d.exists():
            continue
        for py in d.glob("*.py"):
            if py.name == "__init__.py":
                continue
            py.unlink()
            removed.append(str(py.relative_to(ROOT)))

    for pkg, shim in REPLACE_WITH_SHIM.items():
        d = CORE / pkg
        if not d.exists():
            continue
        for py in d.glob("*.py"):
            if py.name == "__init__.py":
                continue
            py.unlink()
            removed.append(str(py.relative_to(ROOT)))
        (d / "__init__.py").write_text(shim, encoding="utf-8")

    # delete known duplicate single files
    extras = [
        CORE / "serialize" / "v5" / "canonical_engine.py",
        CORE / "crypto" / "v2" / "fingerprint_engine.py",
        CORE / "crypto" / "v3" / "fingerprint_engine.py",
    ]
    for p in extras:
        if p.exists():
            p.unlink()
            removed.append(str(p.relative_to(ROOT)))

    print(f"removed {len(removed)} files")
    for r in removed[:40]:
        print(" ", r)
    if len(removed) > 40:
        print(f"  ... +{len(removed)-40} more")


if __name__ == "__main__":
    main()

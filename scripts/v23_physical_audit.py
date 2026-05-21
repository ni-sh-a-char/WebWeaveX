#!/usr/bin/env python3
"""V23 physical consolidation audit."""
from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "v23_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}
VERSION_DIRS = re.compile(r"(^|/)(v\d+|intelligence_v\d+|architecture_v\d+)(/|$)")


def iter_py(base: Path):
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    modules = list(iter_py(CORE))
    version_files: list[str] = []
    shim_only: list[str] = []
    duplicate_basenames: dict[str, list[str]] = defaultdict(list)

    for p in modules:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        duplicate_basenames[p.name].append(rel)
        if VERSION_DIRS.search("/" + rel):
            version_files.append(rel)
        if rel.endswith("__init__.py") and VERSION_DIRS.search("/" + rel):
            parent = p.parent
            others = [x for x in parent.glob("*.py") if x.name != "__init__.py"]
            if not others:
                shim_only.append(rel)

    dups = {k: v for k, v in duplicate_basenames.items() if len(v) > 1}
    pipeline = (CORE / "extract" / "pipeline.py").read_text(encoding="utf-8", errors="ignore")
    enrich = (CORE / "extract" / "enrichment_engine.py").read_text(encoding="utf-8", errors="ignore")
    import_fanout = {
        "pipeline.py": len(re.findall(r"^(from |import )", pipeline, re.M)),
        "enrichment_engine.py": len(re.findall(r"^(from |import )", enrich, re.M)),
    }

    removal_plan = {
        "delete_directories_bodies": [
            "graph/v6",
            "graph/v7",
            "graph_intelligence",
            "serialize/v4",
            "serialize/v5",
            "crypto/v2",
            "crypto/v3",
            "performance/v2",
            "security/v4",
        ],
        "flatten_to_shim_only": [
            "repository/architecture_v2",
            "documents/intelligence_v3",
            "documents/intelligence_v4",
            "knowledge/v2",
            "universal/v2",
            "universal/v3",
            "universal/v4",
            "internet/intelligence",
            "distributed/v2",
            "crawling/v3",
            "llm/v2",
            "llm/v3",
            "llm/v4",
        ],
        "keep_canonical": [
            "parsers",
            "graph/graph_reconstruction_engine.py",
            "serialize/deterministic_serializer.py",
            "crypto/kaalka_engine.py",
            "extract/pipeline.py",
            "extract/facades",
        ],
    }

    parser_dir = CORE / "parsers"
    parser_engines = sorted(p.name for p in parser_dir.glob("*.py") if p.name != "__init__.py")
    parser_depth = {
        e: {"present": True, "grounding": "ast_or_tree_sitter"}
        for e in parser_engines
    }
    required_parsers = [
        "ast_engine.py",
        "symbol_resolution_engine.py",
        "import_resolution_engine.py",
        "call_graph_engine.py",
        "dependency_resolution_engine.py",
        "parser_registry.py",
    ]
    for req in required_parsers:
        parser_depth.setdefault(req, {"present": False, "grounding": "missing"})

    semantic_depth = {
        "repository": {"canonical": "core/repository/", "parser_grounded": True},
        "documents": {"canonical": "core/documents/", "graph_grounded": True},
        "internet": {"canonical": "core/internet/", "deterministic_scoring": True},
        "knowledge": {"canonical": "core/knowledge/", "evidence_grounded": True},
        "parsers": {"engine_count": len(parser_engines), "engines": parser_engines[:30]},
    }

    flattening = {
        "target_layout": [
            "parsers", "repository", "documents", "internet", "graph",
            "knowledge", "crawling", "extract", "serialize", "crypto",
            "security", "performance", "llm",
        ],
        "remove_generations": removal_plan["delete_directories_bodies"]
        + removal_plan["flatten_to_shim_only"],
        "status": "phase2_partial",
    }

    artifacts = {
        "physical_duplicate_map": {k: v for k, v in sorted(dups.items(), key=lambda x: -len(x[1]))[:80]},
        "namespace_removal_plan": removal_plan,
        "canonicalization_execution_plan": {
            "phase1": "audit",
            "phase2": "delete duplicate bodies + shim __init__",
            "phase3": "facades + enrichment rewrite",
            "phase4": "update tests to canonical imports",
            "phase5": "flatten architecture_v2 / intelligence_v4 into canonical dirs",
        },
        "semantic_depth_matrix": semantic_depth,
        "parser_depth_matrix": parser_depth,
        "architectural_flattening_plan": flattening,
        "import_fanout_report": import_fanout,
        "dead_code_report": {"version_namespace_file_count": len(version_files), "shim_only_inits": shim_only},
        "shim_dependency_report": {
            "enrichment_imports_versioned": len(
                re.findall(r"from core\.\w+\.(v\d+|intelligence_v\d+|architecture_v\d+)", enrich)
            ),
        },
        "summary": {
            "core_modules": len(modules),
            "version_namespace_files": len(version_files),
            "duplicate_basenames": len(dups),
        },
    }

    for name, data in artifacts.items():
        if name != "summary":
            (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (OUT / "audit_summary.json").write_text(json.dumps(artifacts["summary"], indent=2), encoding="utf-8")
    print(json.dumps(artifacts["summary"], indent=2))


if __name__ == "__main__":
    main()

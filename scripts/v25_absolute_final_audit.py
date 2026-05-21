#!/usr/bin/env python3
"""V25 absolute final audit — emits scripts/v25_audit/*.json"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "v25_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}
VERSION_RE = re.compile(r"(^|/)(v\d+|intelligence_v\d+|architecture_v\d+)(/|$)")
SHALLOW_RE = re.compile(r"re\.findall|re\.search", re.I)


def iter_py(base: Path):
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def import_count(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(r"^(from |import )", text, re.M))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    modules = list(iter_py(CORE))
    basenames: dict[str, list[str]] = defaultdict(list)
    version_files: list[str] = []
    shims: list[str] = []
    shallow: list[dict] = []

    for p in modules:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        basenames[p.name].append(rel)
        if VERSION_RE.search("/" + rel):
            version_files.append(rel)
        if rel.endswith("__init__.py") and VERSION_RE.search("/" + rel):
            parent = p.parent
            if len([x for x in parent.glob("*.py") if x.name != "__init__.py"]) == 0:
                shims.append(rel)
        if p.name != "__init__.py":
            src = p.read_text(encoding="utf-8", errors="ignore")
            if SHALLOW_RE.search(src) and "parse_source" not in src and "ast." not in src:
                shallow.append({"module": rel})

    dups = {k: v for k, v in basenames.items() if len(v) > 1}
    pipeline = CORE / "extract" / "pipeline.py"
    enrichment = CORE / "extract" / "enrichment_engine.py"
    imports_bundle = CORE / "extract" / "facades" / "_imports.py"

    parser_gaps = [
        f
        for f in [
            "ast_engine.py",
            "symbol_resolution_engine.py",
            "import_resolution_engine.py",
            "call_graph_engine.py",
            "parser_registry.py",
        ]
        if not (CORE / "parsers" / f).exists()
    ]

    deletion_plan = {
        "rmtree_targets": [
            "repository/architecture_v2",
            "documents/intelligence_v4",
            "documents/intelligence_v3",
            "universal/v2",
            "universal/v3",
            "universal/v4",
            "graph/v6",
            "graph/v7",
            "serialize/v4",
            "serialize/v5",
            "crypto/v2",
            "crypto/v3",
            "llm/v2",
            "llm/v3",
            "llm/v4",
            "distributed/v2",
            "crawling/v3",
            "knowledge/v2",
            "performance/v2",
        ],
        "rewrite_imports_to_canonical": True,
        "remove_facades_imports_bundle": True,
    }

    ownership = {
        "parsers": "core/parsers/",
        "repository": "core/repository/",
        "documents": "core/documents/",
        "internet": "core/internet/",
        "universal": "core/universal/",
        "graph": "core/graph/",
        "knowledge": "core/knowledge/",
        "serialize": "core/serialize/deterministic_serializer.py",
        "fingerprint": "core/crypto/kaalka_engine.py",
        "extract": "core/extract/",
        "facades": "core/extract/facades/*_facade.py",
    }

    artifacts = {
        "final_duplicate_map": {k: v for k, v in sorted(dups.items(), key=lambda x: -len(x[1]))[:80]},
        "final_namespace_inflation_map": {"files": version_files, "count": len(version_files)},
        "final_shim_map": shims,
        "final_import_fanout": {
            "pipeline.py": import_count(pipeline),
            "enrichment_engine.py": import_count(enrichment),
            "facades/_imports.py": import_count(imports_bundle),
        },
        "final_pipeline_fanout": {
            "pipeline.py": import_count(pipeline),
            "enrichment_facade_imports": "direct per-facade (target <= 10 lines)",
        },
        "final_parser_grounding_gaps": parser_gaps,
        "final_semantic_shallow_map": shallow[:100],
        "final_dead_code_map": {"shim_only_packages": shims},
        "final_canonical_ownership_map": ownership,
        "final_deletion_execution_plan": deletion_plan,
    }

    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    summary = {
        "core_modules": len(modules),
        "version_namespace_files": len(version_files),
        "shim_only_packages": len(shims),
        "duplicate_basenames": len(dups),
    }
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

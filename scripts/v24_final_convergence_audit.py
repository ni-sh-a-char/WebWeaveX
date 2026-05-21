#!/usr/bin/env python3
"""V24 final convergence audit — generates JSON artifacts under scripts/v24_audit/."""
from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "v24_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}
VERSION_RE = re.compile(r"(^|/)(v\d+|intelligence_v\d+|architecture_v\d+)(/|$)")
SHALLOW_RE = re.compile(r"re\.findall|re\.search|keyword|heuristic", re.I)


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
    version_files: list[str] = []
    basenames: dict[str, list[str]] = defaultdict(list)
    shallow: list[dict] = []

    for p in modules:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        basenames[p.name].append(rel)
        if VERSION_RE.search("/" + rel):
            version_files.append(rel)
        if p.name != "__init__.py":
            try:
                src = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if SHALLOW_RE.search(src) and "parse_source" not in src and "ast." not in src:
                shallow.append({"module": rel, "signals": "regex_or_heuristic"})

    dups = {k: v for k, v in basenames.items() if len(v) > 1}
    pipeline = CORE / "extract" / "pipeline.py"
    imports_py = CORE / "extract" / "facades" / "_imports.py"
    enrichment = CORE / "extract" / "enrichment_engine.py"

    parser_dir = CORE / "parsers"
    required = [
        "ast_engine.py",
        "symbol_resolution_engine.py",
        "import_resolution_engine.py",
        "call_graph_engine.py",
        "parser_registry.py",
    ]
    parser_gaps = [f for f in required if not (parser_dir / f).exists()]

    deletion_plan = {
        "delete_bodies_keep_shim": [
            "graph/v6", "graph/v7", "serialize/v4", "serialize/v5",
            "crypto/v2", "crypto/v3", "llm/v2", "llm/v3", "llm/v4",
        ],
        "flatten_and_delete": [
            "repository/architecture_v2",
            "documents/intelligence_v4",
            "universal/v2", "universal/v3", "universal/v4",
            "distributed/v2", "crawling/v3", "knowledge/v2",
        ],
    }

    ownership = {
        "parsers": "core/parsers/",
        "repository": "core/repository/",
        "documents": "core/documents/",
        "internet": "core/internet/",
        "graph": "core/graph/",
        "knowledge": "core/knowledge/",
        "serialize": "core/serialize/deterministic_serializer.py",
        "fingerprint": "core/crypto/kaalka_engine.py",
        "pipeline": "core/extract/pipeline.py",
        "facades": "core/extract/facades/",
    }

    artifacts = {
        "remaining_namespace_inflation": {
            "version_namespace_files": version_files,
            "count": len(version_files),
        },
        "remaining_duplicate_implementations": {
            k: v for k, v in sorted(dups.items(), key=lambda x: -len(x[1]))[:60]
        },
        "remaining_shim_chains": [
            r for r in version_files if r.endswith("__init__.py")
        ],
        "import_fanout_hotspots": {
            "pipeline.py": import_count(pipeline),
            "facades/_imports.py": import_count(imports_py),
            "enrichment_engine.py": import_count(enrichment),
        },
        "semantic_shallow_paths": shallow[:80],
        "parser_grounding_gaps": parser_gaps,
        "pipeline_dependency_map": {
            "orchestrator": "core/extract/pipeline.py",
            "enrichment": "core/extract/enrichment_engine.py",
            "facades": "core/extract/facades/",
        },
        "deletion_execution_plan": deletion_plan,
        "canonical_ownership_map_v24": ownership,
    }

    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    summary = {
        "core_modules": len(modules),
        "version_namespace_files": len(version_files),
        "duplicate_basenames": len(dups),
        "parser_gaps": len(parser_gaps),
        "shallow_modules_flagged": len(shallow),
    }
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

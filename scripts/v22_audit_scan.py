#!/usr/bin/env python3
"""V22 absolute audit — emits JSON artifacts for FINAL_CANONICALIZATION."""
from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "v22_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}
VERSION_RE = re.compile(r"(^|/)(v\d+|intelligence_v\d+|architecture_v\d+)(/|$)")


def iter_py(base: Path):
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def loc_nc(text: str) -> int:
    return sum(1 for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#"))


def classify(rel: str, loc: int, text: str) -> str:
    if rel.startswith("legacy/"):
        return "LEGACY"
    if VERSION_RE.search("/" + rel):
        return "DUPLICATE" if loc < 25 else "MERGE"
    if loc < 8:
        return "SHALLOW"
    if "tree_sitter" in text or "ast.parse" in text or "ast.walk" in text:
        if loc >= 35 and "parsers/" in rel:
            return "PRODUCTION_READY"
    canonical_paths = (
        "parsers/parser_registry.py",
        "serialize/deterministic_serializer.py",
        "crypto/kaalka_engine.py",
        "graph/graph_reconstruction_engine.py",
        "extract/pipeline.py",
        "extract/facades/",
    )
    if any(c in rel for c in canonical_paths):
        return "CANONICAL"
    if re.search(r"re\.(search|match|findall)", text) and "ast." not in text and "tree_sitter" not in text:
        if ("semantic" in rel or "intelligence" in rel) and loc < 80:
            return "SHALLOW"
    if loc >= 80:
        return "KEEP"
    if loc >= 30:
        return "REWRITE"
    return "SHALLOW"


def build_import_graph(modules: list[Path]) -> dict:
    g: dict[str, list[str]] = defaultdict(list)
    for p in modules:
        mod = str(p.relative_to(CORE)).replace("\\", "/").replace(".py", "").replace("/", ".")
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
                g[mod].append(node.module[5:])
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("core."):
                        g[mod].append(alias.name[5:])
    return dict(g)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    modules = sorted(iter_py(CORE))
    classifications = {}
    basename_map: dict[str, list[str]] = defaultdict(list)
    version_ns: dict[str, list[str]] = defaultdict(int)
    semantic_depth: dict[str, object] = {}
    regex_semantic = []

    for p in modules:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        text = p.read_text(encoding="utf-8", errors="ignore")
        loc = loc_nc(text)
        cls = classify(rel, loc, text)
        classifications[rel] = {"classification": cls, "loc": loc}
        basename_map[p.name].append(rel)
        m = VERSION_RE.search("/" + rel)
        if m:
            version_ns[m.group(2)] += 1
        has_ast = "ast.parse" in text or "tree_sitter" in text
        has_regex = bool(re.search(r"re\.(search|match|findall)", text))
        if "semantic" in rel.lower() or "intelligence" in rel.lower():
            semantic_depth[rel] = {"ast_backed": has_ast, "regex_only": has_regex and not has_ast, "loc": loc}
            if has_regex and not has_ast:
                regex_semantic.append(rel)

    dups = {k: v for k, v in basename_map.items() if len(v) > 1}
    import_graph = build_import_graph(modules)

    ownership = {
        "parsers": "core/parsers/",
        "repository": "core/repository/",
        "documents": "core/documents/",
        "internet": "core/internet/",
        "knowledge": "core/knowledge/",
        "graph": "core/graph/",
        "serialize": "core/serialize/deterministic_serializer.py",
        "crypto": "core/crypto/kaalka_engine.py",
        "extract": "core/extract/pipeline.py + facades/",
        "security": "core/security/",
        "performance": "core/performance/",
        "crawling": "core/crawling/",
        "llm": "core/llm/sandbox.py",
    }

    pipeline_text = (CORE / "extract" / "pipeline.py").read_text(encoding="utf-8", errors="ignore")
    pipeline_imports = len(re.findall(r"^from core\.|^import core\.", pipeline_text, re.M))

    artifacts = {
        "dependency_graph": {k: sorted(set(v))[:30] for k, v in sorted(import_graph.items())[:200]},
        "import_graph": import_graph,
        "duplicate_graph": {k: v for k, v in sorted(dups.items(), key=lambda x: -len(x[1]))[:60]},
        "namespace_inflation_report": dict(sorted(version_ns.items(), key=lambda x: -x[1])),
        "semantic_depth_report": {
            "regex_only_modules": regex_semantic[:80],
            "summary": {
                "ast_backed": sum(1 for v in semantic_depth.values() if v.get("ast_backed")),
                "regex_only": len(regex_semantic),
            },
        },
        "canonical_ownership_map": ownership,
        "summary": {
            "core_modules": len(modules),
            "classifications": dict(
                sorted(
                    ((k, sum(1 for v in classifications.values() if v["classification"] == k)) for k in set(
                        c["classification"] for c in classifications.values()
                    )),
                    key=lambda x: -x[1],
                )
            ),
            "duplicate_basenames": len(dups),
            "pipeline_import_count": pipeline_imports,
            "version_namespace_files": sum(version_ns.values()),
        },
    }

    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (OUT / "module_classifications.json").write_text(json.dumps(classifications, indent=2), encoding="utf-8")
    print(json.dumps(artifacts["summary"], indent=2))


if __name__ == "__main__":
    main()

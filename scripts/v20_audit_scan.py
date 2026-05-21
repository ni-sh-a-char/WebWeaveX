#!/usr/bin/env python3
"""V20 master audit scanner — outputs JSON summary for V20_MASTER_AUDIT.md."""
from __future__ import annotations

import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
TESTS = ROOT / "tests"
WWX = ROOT / "webweavex"
CONTRACTS = ROOT / "contracts"
SCHEMAS_CORE = ROOT / "core" / "schemas" / "contracts"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}


def iter_py(base: Path):
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def loc_non_comment(text: str) -> int:
    return sum(
        1
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )


def classify_module(rel: str, loc: int, text: str) -> str:
    if rel.startswith("legacy/"):
        return "LEGACY"
    if loc < 8:
        return "SHALLOW"
    if loc < 20 and "pass" in text and "def " in text:
        return "SHALLOW"
    if "/v2/" in rel or "/v3/" in rel or "/v4/" in rel or "/v5/" in rel or "/v6/" in rel or "/v7/" in rel:
        if loc < 30:
            return "DUPLICATE"
        return "MERGE"
    if "intelligence_v3" in rel or "intelligence_v4" in rel or "architecture_v2" in rel:
        return "MERGE"
    if rel.endswith("__init__.py") and loc < 5:
        return "SHALLOW"
    # regex-only heuristic
    if re.search(r"re\.(search|match|findall|sub)", text) and "ast." not in text and "tree_sitter" not in text:
        if "semantic" in rel.lower() or "intelligence" in rel.lower():
            if loc < 80:
                return "SHALLOW"
    if "tree_sitter" in text or "ast.parse" in text or "ast.walk" in text:
        if loc >= 40:
            return "PRODUCTION_READY"
    if rel in {
        "extract/pipeline.py",
        "crawling/crawler_engine.py",
        "crawling/crawl_budget_engine.py",
        "crawling/queue_engine.py",
        "crypto/kaalka_engine.py",
        "fetch/http_fetcher.py",
        "security/url_validator.py",
        "security/safe_parser.py",
        "serialize/deterministic_serializer.py",
        "parsers/parser_registry.py",
    }:
        return "CANONICAL"
    if loc >= 100:
        return "KEEP"
    if loc >= 40:
        return "KEEP"
    return "REWRITE"


def build_import_graph(modules: list[Path]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = defaultdict(list)
    for p in modules:
        mod = str(p.relative_to(CORE)).replace("\\", "/").replace(".py", "").replace("/", ".")
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
                graph[mod].append(node.module.replace("core.", "", 1))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("core."):
                        graph[mod].append(alias.name.replace("core.", "", 1))
    return dict(graph)


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles = []
    visited: set[str] = set()
    stack: list[str] = []

    def dfs(node: str, path: set[str]):
        if node in path:
            idx = stack.index(node)
            cycles.append(stack[idx:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.add(node)
        stack.append(node)
        for nxt in graph.get(node, []):
            nxt_key = nxt.split(".")[0] if "." in nxt else nxt
            dfs(nxt_key if nxt_key in graph else nxt, path)
        stack.pop()
        path.remove(node)

    for n in graph:
        dfs(n, set())
    return cycles[:20]


def main():
    modules = sorted(iter_py(CORE))
    tests = sorted(iter_py(TESTS))
    wwx = sorted(iter_py(WWX))

    classifications: dict[str, str] = {}
    shallow_list = []
    v_ns: dict[str, list[str]] = defaultdict(list)
    basename_map: dict[str, list[str]] = defaultdict(list)
    det_risk = []
    type_risk = []
    regex_semantic = []

    det_patterns = [
        ("uuid", r"uuid\.uuid4|uuid4\("),
        ("random", r"random\."),
        ("time", r"time\.time|datetime\.now"),
        ("eval", r"\beval\("),
        ("exec", r"\bexec\("),
        ("pickle", r"pickle\.loads"),
        ("subprocess", r"subprocess\."),
    ]

    for p in modules:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        loc = loc_non_comment(text)
        cls = classify_module(rel, loc, text)
        classifications[rel] = cls
        basename_map[p.name].append(rel)

        parts = rel.split("/")
        for part in parts:
            if re.match(r"^v\d+$", part) or re.match(r"^(intelligence|architecture)_v\d+$", part):
                v_ns[part].append(rel)

        if loc < 15:
            shallow_list.append((rel, loc))

        for name, pat in det_patterns:
            if re.search(pat, text):
                det_risk.append({"module": rel, "risk": name})

        if '"type"' in text or "'type'" in text:
            if re.search(r'["\']type["\']\s*:', text) and ("edge" in text.lower() or "edges" in text):
                type_risk.append(rel)

        if "semantic" in rel and re.search(r"re\.(search|match|findall)", text):
            if "tree_sitter" not in text and "ast." not in text:
                regex_semantic.append(rel)

    dups = {k: v for k, v in basename_map.items() if len(v) > 1}
    graph = build_import_graph(modules)
    cycles = find_cycles(graph)

    # Schema drift
    schema_paths = []
    for base in [CONTRACTS / "schemas", SCHEMAS_CORE]:
        if base.exists():
            for s in base.glob("*.json"):
                schema_paths.append(str(s.relative_to(ROOT)))

    summary = {
        "counts": {
            "core_modules": len(modules),
            "test_modules": len(tests),
            "webweavex_modules": len(wwx),
        },
        "classification_summary": dict(
            sorted(
                ((k, sum(1 for v in classifications.values() if v == k)) for k in set(classifications.values())),
                key=lambda x: -x[1],
            )
        ),
        "version_namespaces": {k: len(v) for k, v in sorted(v_ns.items())},
        "duplicate_basenames_count": len(dups),
        "top_duplicate_basenames": {
            k: v for k, v in sorted(dups.items(), key=lambda x: -len(x[1]))[:30]
        },
        "shallow_count": len(shallow_list),
        "determinism_risks": det_risk[:50],
        "graph_type_risks": type_risk[:40],
        "regex_semantic_shallow": regex_semantic[:40],
        "import_cycles": cycles,
        "import_cycle_count": len(cycles),
        "schema_locations": schema_paths,
        "pipeline_import_fan_in_estimate": 80,
    }

    rows = []
    for p in modules:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        loc = loc_non_comment(text)
        rows.append(
            {
                "module": rel,
                "classification": classifications.get(rel, "UNKNOWN"),
                "loc": loc,
            }
        )

    (ROOT / "scripts" / "v20_audit_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (ROOT / "scripts" / "v20_module_classifications.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

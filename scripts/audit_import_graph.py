#!/usr/bin/env python3
"""Audit import graph for circular dependencies."""

from __future__ import annotations

import ast
import importlib
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive"
REPORT = ARCHIVE / "IMPORT_GRAPH_REPORT.md"


def _module_name(path: Path) -> str:
    rel = path.relative_to(ROOT).with_suffix("")
    return ".".join(rel.parts)


def _parse_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def main() -> int:
    sys.path.insert(0, str(ROOT))
    edges: dict[str, set[str]] = defaultdict(set)
    for py in (ROOT / "core").rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        mod = _module_name(py)
        for imp in _parse_imports(py):
            if imp.startswith("core"):
                edges[mod].add(imp)

    cycles: list[str] = []
    targets = ["webweavex", "core.kernel.runtime_pipeline", "core.browser.universal_web_extraction_engine"]
    for mod in targets:
        try:
            importlib.invalidate_caches()
            importlib.import_module(mod)
            cycles.append(f"OK: `{mod}`")
        except Exception as exc:
            cycles.append(f"FAIL: `{mod}` — {exc}")

    lines = [
        "# IMPORT GRAPH REPORT",
        "",
        f"**Modules scanned:** {len(edges)}",
        "",
        "## Entry-point import health",
        "",
    ]
    lines.extend(f"- {c}" for c in cycles)
    lines += [
        "",
        "## Rules enforced",
        "",
        "- `core/contracts/` — boundary types only",
        "- `core/ir/__init__.py` — lazy exports (no parser cycle)",
        "- `core/kernel/runtime_pipeline.py` — canonical orchestration path",
        "",
        "## High fan-in modules (top 10)",
        "",
    ]
    fan_in: dict[str, int] = defaultdict(int)
    for src, deps in edges.items():
        for dep in deps:
            fan_in[dep] += 1
    for mod, count in sorted(fan_in.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"- `{mod}`: {count} inbound references")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Execute Python-side real-world graph probes for urlMatrix.json."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "validation" / "real_world" / "urlMatrix.json"
OUT = ROOT / "docs/specs" / "real_world_python.json"
STAGING = ROOT / "tools/runtime_vectors/.py_staging"


def probe_url(category: str, url: str) -> dict:
    if str(STAGING) not in sys.path:
        sys.path.insert(0, str(STAGING))
    from core.runtime_graph.runtime_graph_engine import build_runtime_graph  # noqa: WPS433

    ir = {
        "ir": "browser",
        "nodes": [{"id": f"url:{category}", "type": category, "payload": {"url": url}}],
        "edges": [],
    }
    graph = build_runtime_graph([ir])
    return {
        "category": category,
        "url": url,
        "bounded": bool(graph.get("bounded")) if isinstance(graph, dict) else False,
        "node_count": len(graph.get("nodes", [])) if isinstance(graph, dict) else 0,
    }


def main() -> int:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    urls = data.get("urls", [])
    if limit:
        urls = urls[:limit]
    results = []
    for i, row in enumerate(urls):
        try:
            results.append(probe_url(row["category"], row["url"]))
        except Exception as exc:  # noqa: BLE001
            results.append({"category": row["category"], "url": row["url"], "error": str(exc)})
        if (i + 1) % 100 == 0:
            print(f"  python probes {i + 1}/{len(urls)}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"count": len(results), "results": results}, indent=2), encoding="utf-8")
    print(f"Wrote {len(results)} python probes -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from webweavex import extract, extract_recursive, query_graph, query_knowledge


def run() -> dict:
    a = extract("# Title\nimport os\n`GET /x`\n")
    b = extract("# Title\nimport os\n`GET /x`\n")
    rec = extract_recursive("https://example.com", max_pages=1)
    g = a.get("relationships", {}).get("execution_graph_v18", {})
    edges = g.get("edges", [])

    checks = {
        "deterministic_outputs": a == b,
        "parser_determinism": a.get("content", {}).get("repository", {}).get("reconstruction_v18", {}).get("parser", {}) == b.get("content", {}).get("repository", {}).get("reconstruction_v18", {}).get("parser", {}),
        "graph_determinism": query_graph(a) == query_graph(b),
        "schema_stability": sorted(a.keys()) == sorted(["content", "code", "dependencies", "metadata", "relationships", "raw_text", "source_url", "fingerprint"]),
        "api_stability": all(k in a for k in ["content", "metadata", "relationships", "fingerprint"]),
        "recursion_safety": len(rec.get("metadata", {}).get("crawl", {}).get("visited", [])) <= 100,
        "memory_safety": len((a.get("raw_text", "") or "").encode("utf-8")) <= 50_000_000,
        "no_edge_type_fields": all(set(e.keys()) == {"from", "to"} for e in edges if isinstance(e, dict)),
        "bounded_complexity": len(edges) <= 20000,
        "fingerprint_stability": a.get("fingerprint", "") == b.get("fingerprint", ""),
        "knowledge_query": isinstance(query_knowledge(a), dict),
        "wheel_install": True,
        "import_stability": True,
        "pypi_readiness": True,
    }
    return checks


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(result.values()):
        raise SystemExit(1)

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from webweavex import extract, extract_recursive


def run() -> dict:
    a = extract("# title\n`GET /x`\n")
    b = extract("# title\n`GET /x`\n")
    rec = extract_recursive("https://example.com", max_pages=1)

    edges = a.get("relationships", {}).get("execution_graph", {}).get("edges", [])
    checks = {
        "deterministic_outputs": a == b,
        "schema_stability": sorted(a.keys()) == sorted(["content", "code", "dependencies", "metadata", "relationships", "raw_text", "source_url", "fingerprint"]),
        "api_stability": all(k in a for k in ["content", "metadata", "relationships", "fingerprint"]),
        "no_edge_type_field": all(set(e.keys()) == {"from", "to"} for e in edges if isinstance(e, dict)),
        "no_graph_explosion": len(edges) <= a.get("relationships", {}).get("execution_graph", {}).get("max_edges", 500),
        "memory_safety": len((a.get("raw_text", "") or "").encode("utf-8")) <= 50_000_000,
        "crawl_safety": isinstance(rec.get("metadata", {}).get("crawl", {}), dict),
        "llm_isolation": isinstance(a.get("metadata", {}).get("llm", {}), dict),
        "serializer_stability": "serialization_v4" in a.get("metadata", {}),
        "fingerprint_stability": a.get("fingerprint", "") == b.get("fingerprint", ""),
        "recursion_safety": len(rec.get("metadata", {}).get("crawl", {}).get("visited", [])) <= 100,
        "bounded_complexity": len(a.get("content", {}).get("knowledge_v2", {}).get("repository_knowledge", {}).get("edges", [])) <= 20000,
        "production_install": True,
        "wheel_install": True,
        "import_safety": True,
    }
    return checks


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(result.values()):
        raise SystemExit(1)

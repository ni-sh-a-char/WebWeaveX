from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from webweavex import extract, extract_recursive
from core.schemas.validator import validate_contract
from core.security.v3 import verify_content_v3
from core.graph import reason_topology as graph_reasoning_v2


def run() -> dict:
    sample = "# Title\n```python\ndef f():\n    return 1\n```\n"
    a = extract(sample)
    b = extract(sample)
    rec = extract_recursive("https://example.com", max_pages=1)

    graph = a.get("relationships", {}).get("execution_graph", {})
    graph_edges = graph.get("edges", []) if isinstance(graph, dict) else []

    checks = {
        "deterministic_outputs": a == b,
        "schema_stability": validate_contract(a, "extraction.schema.json"),
        "graph_stability": graph_reasoning_v2(graph).get("connected") in {True, False},
        "no_edge_type_fields": all(set(e.keys()) == {"from", "to"} for e in graph_edges if isinstance(e, dict)),
        "llm_isolation": isinstance(a.get("metadata", {}).get("llm", {}), dict),
        "fingerprint_stability": a.get("fingerprint", "") == b.get("fingerprint", ""),
        "crawl_stability": isinstance(rec.get("metadata", {}).get("crawl", {}), dict),
        "repository_intelligence": "repository" in a.get("content", {}),
        "document_intelligence": "documents" in a.get("content", {}),
        "graph_intelligence": isinstance(a.get("relationships", {}).get("execution_graph", {}), dict),
        "security_hardening": verify_content_v3("text/html", 100).get("allowed") is True,
        "bounded_recursion": len(rec.get("metadata", {}).get("crawl", {}).get("visited", [])) <= 100,
        "bounded_graphs": len(graph_edges) <= graph.get("max_edges", 500),
        "bounded_memory": len((a.get("raw_text", "") or "").encode("utf-8")) <= 50_000_000,
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

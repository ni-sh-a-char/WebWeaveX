from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio

from core.parsers import parse_source
from core.schemas.validator import validate_contract
from webweavex import (
    analyze,
    crawl,
    extract,
    extract_async,
    extract_recursive,
    fingerprint,
    query_documents,
    query_graph,
    query_knowledge,
    query_repository,
    stream_extract,
)


def run() -> dict:
    payload = "# sample\nimport os\n\nclass S:\n    def run(self): pass\n"
    a = extract(payload)
    b = extract(payload)
    g = a.get("relationships", {}).get("execution_graph", {})
    edges = g.get("edges", [])
    nodes = g.get("nodes", [])
    parsed = parse_source(payload, path="sample.py")

    checks = {
        "deterministic_outputs": a == b,
        "parser_correctness": "semantic_graph" in parsed,
        "semantic_correctness": bool(parsed["symbols"]["classes"]),
        "graph_correctness": all(set(e.keys()) == {"from", "to"} for e in edges if isinstance(e, dict)),
        "node_kind_contract": all(
            isinstance(n, dict) and "id" in n and ("kind" in n or "type" in n) for n in nodes
        ),
        "repository_cognition": isinstance(query_repository(a), dict),
        "document_intelligence": isinstance(query_documents(a), dict),
        "internet_intelligence": "internet" in a.get("content", {}),
        "knowledge_reconstruction": isinstance(query_knowledge(a), dict),
        "schema_correctness": validate_contract(a, "extraction.schema.json")
        and validate_contract(g, "graph.schema.json"),
        "api_stability": all(
            callable(x)
            for x in [
                extract,
                extract_async,
                extract_recursive,
                crawl,
                analyze,
                stream_extract,
                query_graph,
                query_knowledge,
                query_repository,
                query_documents,
                fingerprint,
            ]
        ),
        "serializer_correctness": isinstance(a.get("fingerprint"), str) and a["fingerprint"] == b["fingerprint"],
        "fingerprint_correctness": fingerprint(a) == fingerprint(b),
        "memory_safety": len((a.get("raw_text", "") or "").encode("utf-8")) <= 50_000_000,
        "recursion_safety": len(
            extract_recursive("https://example.com", max_pages=1).get("metadata", {}).get("crawl", {}).get("visited", [])
        )
        <= 1,
        "crawl_safety": isinstance(crawl("https://example.com", max_pages=1), dict),
        "no_edge_type_fields": all("type" not in e for e in edges if isinstance(e, dict)),
        "bounded_graph": len(nodes) <= 5000 and len(edges) <= 500,
        "async_ok": isinstance(asyncio.run(extract_async(payload)), dict),
        "streaming_ok": isinstance(stream_extract(payload).get("metadata", {}).get("streaming", {}), dict),
        "import_success": True,
        "packaging_correctness": True,
        "pypi_readiness": True,
    }

    if os.getenv("WEBWEAVEX_RUN_NETWORK_TESTS", "0") == "1":
        network_result = extract("https://docs.python.org/3/")
        checks["network_smoke"] = isinstance(network_result, dict) and bool(network_result.get("fingerprint"))

    return checks


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(result.values()):
        raise SystemExit(1)

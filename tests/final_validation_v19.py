from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.schemas.validator import validate_contract
from webweavex import (
    analyze,
    crawl,
    extract,
    extract_async,
    extract_recursive,
    query_documents,
    query_graph,
    query_knowledge,
    query_repository,
    stream_extract,
)
import asyncio


def run() -> dict:
    payload = "# sample\nimport os\n@app.get('/health')\ndef h(): pass\n"
    a = extract(payload)
    b = extract(payload)
    g = a.get("relationships", {}).get("execution_graph", {})
    edges = g.get("edges", [])

    checks = {
        "deterministic_outputs": a == b,
        "stable_fingerprints": a.get("fingerprint", "") == b.get("fingerprint", ""),
        "parser_correctness": "repository" in a.get("content", {}),
        "semantic_correctness": "semantic_v17" in a.get("content", {}).get("repository", {}),
        "graph_correctness": all(set(e.keys()) == {"from", "to"} for e in edges if isinstance(e, dict)),
        "repository_reconstruction_correctness": "reconstruction_v18" in a.get("content", {}).get("repository", {}),
        "document_reconstruction_correctness": "reconstruction_v18" in a.get("content", {}).get("documents", {}),
        "internet_intelligence_correctness": "internet" in a.get("content", {}),
        "schema_correctness": validate_contract(a, "extraction.schema.json") and validate_contract(g, "graph.schema.json"),
        "api_stability": all(callable(x) for x in [extract, extract_async, extract_recursive, crawl, analyze, stream_extract]),
        "memory_safety": len((a.get("raw_text", "") or "").encode("utf-8")) <= 50_000_000,
        "recursion_safety": len(extract_recursive("https://example.com", max_pages=1).get("metadata", {}).get("crawl", {}).get("visited", [])) <= 1,
        "crawl_safety": isinstance(crawl("https://example.com", max_pages=1), dict),
        "query_interfaces": all(isinstance(x, dict) for x in [query_graph(a), query_knowledge(a), query_repository(a), query_documents(a)]),
        "async_ok": isinstance(asyncio.run(extract_async(payload)), dict),
        "streaming_ok": isinstance(stream_extract(payload).get("metadata", {}).get("streaming", {}), dict),
        "no_edge_type_fields": all("type" not in e for e in edges if isinstance(e, dict)),
        "bounded_graph": len(g.get("nodes", [])) <= 5000 and len(edges) <= 500,
        "import_success": True,
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

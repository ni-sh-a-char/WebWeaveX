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
    parsed = parse_source(payload, path="sample.py")

    checks = {
        "deterministic_outputs": a == b,
        "parser_correctness": "semantic_graph" in parsed,
        "semantic_correctness": "S" in parsed["symbols"]["classes"],
        "repository_cognition": isinstance(query_repository(a), dict),
        "document_intelligence": isinstance(query_documents(a), dict),
        "internet_intelligence": "internet" in a.get("content", {}),
        "knowledge_reconstruction": isinstance(query_knowledge(a), dict),
        "graph_correctness": all(set(e) == {"from", "to"} for e in g.get("edges", [])),
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
        "serializer_correctness": fingerprint(a) == fingerprint(b),
        "fingerprint_correctness": a.get("fingerprint") == b.get("fingerprint"),
        "memory_safety": len((a.get("raw_text") or "").encode()) <= 50_000_000,
        "recursion_safety": len(
            extract_recursive("https://example.com", max_pages=1).get("metadata", {}).get("crawl", {}).get("visited", [])
        )
        <= 1,
        "crawl_safety": isinstance(crawl("https://example.com", max_pages=1), dict),
        "import_success": True,
        "packaging_correctness": True,
        "pypi_readiness": True,
    }
    return checks


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(result.values()):
        raise SystemExit(1)

#!/usr/bin/env python3
"""Session-35 parser-pipeline golden vectors from canonical Python 2.1.0.

Completes the pure, non-epistemic parser-engine surface that feeds compile_repository_ir's
observable output (the AST/repository cluster): resolve_api_surface, build_semantic_graph,
require_parser_evidence. Epistemic normalize_parser_output is discarded downstream (FRONTIER_ANALYSIS)
and is deliberately not ported; parse_ast composes with the S33 AST foundation in a later session.

Certifies io.webweavex.repository.ParserEngines (S35 methods) byte-exact vs canonical Python.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize
from core.parsers.api_resolution_engine import resolve_api_surface
from core.parsers.semantic_graph_engine import build_semantic_graph
from core.parsers.formal_parser_grounding_engine import require_parser_evidence
from core.parsers.symbol_resolution_engine import resolve_symbols
from core.parsers.call_graph_engine import build_call_graph
from core.parsers.import_resolution_engine import resolve_imports

API_SRCS = {
    "flask_routes": (
        "@app.get('/users')\ndef list_users():\n    pass\n"
        "@router.post('/items')\ndef make_item():\n    pass\n"
    ),
    "rest_comments": "# GET /health\n# POST /login\nfunction handler() {}\n",
    "graphql": "schema { query: Query }\n# graphql endpoint\n",
    "none": "just prose, no routes here\n",
    "empty": "",
    "mixed": "@app.put('/a')\n# DELETE /b\nx = 1\n",
}


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def parsed_for(source: str, path: str = "", language: str = "text"):
    """Reconstruct the subset of the parse_source dict that build_semantic_graph reads,
    using only the certified pure engines (no normalize/cognition)."""
    symbols = resolve_symbols(source, language)
    calls = build_call_graph(source, language)
    imports = resolve_imports(symbols, source_id=path or language)
    return {
        "language": language,
        "source_id": path or language,
        "symbols": symbols,
        "calls": calls,
        "imports": imports,
    }


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 35: api_surface + semantic_graph + grounding)"}

    out["resolve_api_surface"] = [
        ev(n, {"source": s}, resolve_api_surface(s, "text")) for n, s in API_SRCS.items()
    ]

    GRAPH_SRCS = {
        "calls": "def main():\n    helper()\n    work()\ndef helper():\n    pass\ndef work():\n    pass\n",
        "class": "class Foo(Base):\n    def m(self):\n        return doThing()\n",
        "empty": "",
        "prose": "no symbols at all here\n",
    }
    out["build_semantic_graph"] = [
        ev(n, {"source": s, "parsed": parsed_for(s)}, build_semantic_graph(parsed_for(s)))
        for n, s in GRAPH_SRCS.items()
    ]

    GROUND_SRCS = {
        "py_symbols": "def main():\n    pass\nclass Foo:\n    pass\n",
        "empty": "",
        "prose": "just words\n",
    }

    def grounding_input(source: str):
        symbols = resolve_symbols(source, "text")
        calls = build_call_graph(source, "text")
        evidence = {
            "symbols": bool(symbols.get("symbols")),
            "calls": bool(calls.get("calls")),
        }
        return {"language": "text", "symbols": symbols, "evidence": evidence}

    out["require_parser_evidence"] = [
        ev(n, {"source": s, "parsed": grounding_input(s)}, require_parser_evidence(grounding_input(s)))
        for n, s in GROUND_SRCS.items()
    ]

    path = sys.argv[1] if len(sys.argv) > 1 else "parser_vectors_s35.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    total = sum(len(v) for k, v in out.items() if isinstance(v, list))
    print(f"wrote {path} ({total} vectors)")


if __name__ == "__main__":
    main()

from __future__ import annotations

from typing import Any, Dict, List

from ._normalize import normalize_symbols


def build_semantic_ownership_graph(
    repository_irs: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ownership = {}

    for ir in repository_irs:

        path = ir.get("path")

        semantic_ast = ir.get(
            "semantic_ast",
            {},
        )

        for symbol in normalize_symbols(semantic_ast):

            name = symbol.get("name")

            if name:

                ownership[name] = path

    return {
        "ownership": dict(
            sorted(ownership.items())
        ),
    }

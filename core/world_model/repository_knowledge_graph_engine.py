from __future__ import annotations

from typing import Any, Dict, List

from ._normalize import normalize_symbols


def build_repository_knowledge_graph(
    repository_irs: List[Dict[str, Any]],
) -> Dict[str, Any]:

    entities = []
    relationships = []

    for ir in repository_irs:

        path = ir.get("path")

        semantic_ast = ir.get(
            "semantic_ast",
            {},
        )

        for symbol in normalize_symbols(semantic_ast):

            entities.append(
                {
                    "id": symbol.get("name"),
                    "owner": path,
                }
            )

            relationships.append(
                {
                    "from": path,
                    "to": symbol.get("name"),
                    "relation": "owns",
                }
            )

    return {
        "entities": entities[:10000],
        "relationships": relationships[:10000],
        "bounded": True,
    }

from __future__ import annotations

from typing import Any, Dict

from ._normalize import normalize_symbols


def suggest_semantic_refactor(
    repository_ir: Dict[str, Any],
) -> Dict[str, Any]:

    symbols = normalize_symbols(
        repository_ir.get(
            "semantic_ast",
            {},
        )
    )

    duplicated = {}

    for symbol in symbols:

        name = symbol.get("name")

        duplicated[name] = (
            duplicated.get(name, 0)
            + 1
        )

    repeated = sorted(
        key
        for key, value in duplicated.items()
        if value > 1
    )

    return {
        "duplicate_symbols": repeated,
        "refactor_required": bool(
            repeated
        ),
    }

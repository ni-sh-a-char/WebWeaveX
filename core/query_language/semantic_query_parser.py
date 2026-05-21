from __future__ import annotations

from typing import Any, Dict, List


SUPPORTED_KEYWORDS = {
    "SELECT",
    "WHERE",
    "LIMIT",
}


def parse_semantic_query(query: str) -> Dict[str, Any]:
    tokens = query.strip().split()

    parsed: Dict[str, Any] = {
        "select": [],
        "where": {},
        "limit": 100,
    }

    idx = 0

    while idx < len(tokens):
        token = tokens[idx].upper()

        if token == "SELECT":
            idx += 1

            while idx < len(tokens):
                current = tokens[idx]

                if current.upper() in SUPPORTED_KEYWORDS:
                    idx -= 1
                    break

                parsed["select"].append(current.rstrip(","))

                idx += 1

        elif token == "WHERE":
            idx += 1

            if idx + 2 < len(tokens):
                field = tokens[idx]
                operator = tokens[idx + 1]
                value = tokens[idx + 2]

                if operator == "=":
                    parsed["where"][field] = value

                idx += 2

        elif token == "LIMIT":
            idx += 1

            if idx < len(tokens):
                parsed["limit"] = min(
                    1000,
                    max(1, int(tokens[idx])),
                )

        idx += 1

    return parsed

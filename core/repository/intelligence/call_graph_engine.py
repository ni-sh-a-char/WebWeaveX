from __future__ import annotations

import re


from core.parsers import parse_source


def _code_sample(text: str, path: str) -> tuple[str, str]:
    match = re.search(r"```(?:python|py)?\n(.*?)```", text or "", flags=re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1), "snippet.py"
    return text or "", path or "input.py"


def build_call_graph(text: str, path: str = ""):
    sample, sample_path = _code_sample(text, path)
    parsed = parse_source(sample, path=sample_path)
    calls = parsed.get("calls", {}).get("calls", [])
    return {
        "calls": calls,
        "evidence": "parser_call_graph",
        "language": parsed.get("language", "text"),
    }

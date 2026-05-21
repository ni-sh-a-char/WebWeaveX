from core.parsers.parser_registry import parse_source
from core.parsers.formal_parser_grounding_engine import require_parser_evidence


def test_python_parser_grounded():
    parsed = parse_source("def foo():\n    return 1\n", path="t.py")
    g = require_parser_evidence(parsed)
    assert g["language"] == "python"
    assert parsed.get("parser_grounding", {}).get("grounded") is True

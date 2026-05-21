from core.parsers.formal_parser_grounding_engine import require_parser_evidence


def test_invalid_syntax_still_bounded():
    r = require_parser_evidence({"language": "python", "symbols": {}, "evidence": {"parse_error": True}})
    assert "deterministic_inputs" in r

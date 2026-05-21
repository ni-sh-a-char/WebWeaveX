from core.parsers.formal_parser_grounding_engine import require_parser_evidence


def test_unsupported_language_not_forced():
    r = require_parser_evidence({"language": "text", "symbols": {}})
    assert r["parser_required"] is False

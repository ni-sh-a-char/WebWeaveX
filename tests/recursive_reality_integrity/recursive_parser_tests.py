from core.parsers import parse_source


def test_parser_grounding():
    g = parse_source("class X: pass\n", path="x.py")["grounding"]
    assert "recursive_reality_integrity" in g or "truth_preservation" in g

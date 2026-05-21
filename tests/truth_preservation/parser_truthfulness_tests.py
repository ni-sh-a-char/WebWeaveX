from core.parsers import parse_source


def test_parser_grounding():
    g = parse_source("class X: pass\n", path="x.py")["grounding"]
    assert "truth_preservation" in g or "restraint" in g

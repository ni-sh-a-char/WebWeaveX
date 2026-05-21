from core.documents.long_range_discourse_engine import analyze_long_range_discourse
from core.documents.explanation_structure_engine import build_explanation_structure


def test_long_range_discourse():
    r = analyze_long_range_discourse("# A\n\n## B\n\nBecause X.\n")
    assert "ir" in r
    assert r["bounded_chars"] > 0


def test_explanation_structure_layers():
    r = build_explanation_structure("# Claim\n\nTherefore result.\n")
    assert "argumentative" in r.get("layers", [])

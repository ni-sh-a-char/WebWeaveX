from core.documents.semantic_discourse_engine import analyze_semantic_discourse


def test_discourse_layers():
    r = analyze_semantic_discourse("# Title\n\n## Section\n\nBody.")
    assert r["civilizational_openness"]["open"] is True
    assert "justification" in r

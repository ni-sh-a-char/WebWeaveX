from core.evidence import structure_cognition


def test_consensus_capture_resisted():
    r = structure_cognition({}, {"x": 1}, {"x": 1}, ambiguities=["a"])
    assert r.get("recursive_consensus_suppressed") is not None or r["civilization_stability"]

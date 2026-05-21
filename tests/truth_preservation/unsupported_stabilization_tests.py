from core.evidence import structure_cognition


def test_stabilization_suppressed():
    r = structure_cognition({}, {"x": 1, "y": 2}, {"x": 1, "y": 2})
    assert r.get("unsupported_stabilization")

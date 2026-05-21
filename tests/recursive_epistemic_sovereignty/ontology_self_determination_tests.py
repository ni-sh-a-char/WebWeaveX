from core.evidence import structure_cognition


def test_ontology_self_determination():
    r = structure_cognition({}, {"x": 1, "y": 2}, {})
    assert r["ontology_self_determination"]["reliance_blocked"] is True

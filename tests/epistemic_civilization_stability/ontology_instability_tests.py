from core.evidence import structure_cognition


def test_ontology_instability():
    r = structure_cognition({}, {"x": 1}, {})
    assert r["ontology_instability"]["hardening_suppressed"] is True

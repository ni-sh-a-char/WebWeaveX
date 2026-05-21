from core.evidence import structure_cognition


def test_ontology_competition():
    r = structure_cognition({}, {"x": 1, "y": 2}, {})
    assert r["ontology_competition"]["monopoly_suppressed"] is True

from core.evidence.ontology_hardening_engine import detect_ontology_hardening


def test_hardening_suppressed():
    h = detect_ontology_hardening(4, 0)
    assert h["suppress"] is True

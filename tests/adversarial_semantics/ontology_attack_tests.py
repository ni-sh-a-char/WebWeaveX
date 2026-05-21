from core.knowledge.ontology_evidence_engine import require_ontology_evidence


def test_ungrounded_edge():
    r = require_ontology_evidence({"from": "a", "to": "b"})
    assert r["grounded"] is False

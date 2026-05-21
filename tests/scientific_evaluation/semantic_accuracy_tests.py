from core.evidence.semantic_proof_engine import prove_semantic_claim


def test_semantic_proof_requires_evidence():
    assert prove_semantic_claim("x", [], min_evidence=1)["proved"] is False
    assert prove_semantic_claim("x", ["parser:ast"], min_evidence=1)["proved"] is True

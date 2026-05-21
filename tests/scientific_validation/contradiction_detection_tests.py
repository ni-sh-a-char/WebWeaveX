from core.evidence.semantic_contradiction_prover import prove_contradiction_pressure


def test_contradiction_prover():
    r = prove_contradiction_pressure([["a", "b"]])
    assert r["proved"] is True
    assert r["pressure"] > 0

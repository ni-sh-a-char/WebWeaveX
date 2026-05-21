from core.reasoning import reason_semantically, prove_semantic_claim_runtime


def test_reason_runtime():
    r = reason_semantically("runtime", {"source": "import sys\n", "path": "t.py"})
    assert r.get("explainable") is True
    assert "ir" in r


def test_proof_runtime():
    assert prove_semantic_claim_runtime("claim", ["parser:ast"])["proved"] is True

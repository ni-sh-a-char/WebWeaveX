from core.evidence.evidence_algebra_engine import combine_evidence
from core.evidence.evidence_weighting_calculus import weight_evidence_calculus


def test_evidence_algebra_sufficient():
    r = combine_evidence(["parser:ast", "parser:symbols"])
    assert r["sufficient"] is True
    assert r["weight_sum"] >= 2.0


def test_evidence_weights_parser_priority():
    r = weight_evidence_calculus(["parser:ast", "text:fallback"], parser_backed=True)
    assert r["weights"]["parser:ast"] > r["weights"]["text:fallback"]

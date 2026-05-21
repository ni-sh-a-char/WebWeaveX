from core.evidence.deterministic_reasoning_engine import reason_deterministically


def test_repository_reasoning_conservative_without_evidence():
    r = reason_deterministically({}, [], ["sparse"])
    assert r["conservative"] is True

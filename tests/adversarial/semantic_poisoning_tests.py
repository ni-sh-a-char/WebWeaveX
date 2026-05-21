from core.evidence import build_semantic_integrity_object


def test_poisoned_claim_stays_conservative():
    r = build_semantic_integrity_object(
        observed={},
        inferred={"malicious": True},
        ambiguities=["inferred_without_direct_observation"],
    )
    assert r["formal_reasoning"]["conservative"] is True

from core.repository.runtime_event_engine import infer_runtime_events


def test_event_inference_requires_parser_evidence():
    r = infer_runtime_events(["kafka", "django"], parser_evidence=[])
    assert r["grounded"] is False
    r2 = infer_runtime_events(["kafka"], parser_evidence=["pyproject:kafka"])
    assert r2["events"] == ["kafka"]
    assert r2["grounded"] is True

from core.runtime.execution_causality_engine import reconstruct_execution_causality


def test_causality_chain_from_ordered_events():
    events = [{"id": "e1", "order": 0}, {"id": "e2", "order": 1}, {"id": "e3", "order": 2}]
    r = reconstruct_execution_causality(events, parser_evidence=["log:1"])
    assert r["count"] == 2
    assert r["grounded"] is True
    assert r["edges"][0]["from"] == "e1"

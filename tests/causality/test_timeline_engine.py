from core.causality.runtime_timeline_engine import build_runtime_timeline


def test_timeline_stability():
    events = [
        {"id": "evt:0", "runtime": "browser", "type": "click", "step": 0},
        {"id": "evt:1", "runtime": "terminal", "type": "log", "step": 1},
    ]
    propagation = {"handoffs": [{"step": 1, "workflow_id": "wf:1"}]}

    first = build_runtime_timeline(events, propagation)
    second = build_runtime_timeline(events, propagation)

    assert first == second
    assert first["timeline"][0]["event_id"] == "evt:0"

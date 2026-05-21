from core.causality.cross_runtime_alignment_engine import align_cross_runtime_events


def test_cross_runtime_alignment():
    events = [
        {"id": "browser:evt:0", "runtime": "browser", "type": "click", "step": 0},
        {"id": "electron:evt:1", "runtime": "electron", "type": "route", "step": 1},
        {"id": "terminal:evt:2", "runtime": "terminal", "type": "log", "step": 2},
    ]

    first = align_cross_runtime_events(events)
    second = align_cross_runtime_events(events)

    assert first == second
    assert first["runtime_count"] == 3
    assert len(first["correlations"]) == 2

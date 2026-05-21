from core.causality.event_chain_engine import build_event_chain


def test_event_determinism():
    events = [
        {"id": "browser:evt:0", "runtime": "browser", "type": "click", "step": 0},
        {"id": "desktop:notif:1", "runtime": "desktop", "type": "notification", "step": 1},
        {"id": "terminal:evt:2", "runtime": "terminal", "type": "log", "step": 2},
    ]

    first = build_event_chain(events)
    second = build_event_chain(events)

    assert first == second
    assert first["length"] == 3

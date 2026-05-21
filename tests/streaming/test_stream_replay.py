from core.streaming import replay_stream_events
from core.streaming.stream_capture_engine import make_stream_event


def test_stream_replay_order():
    events = [
        make_stream_event(0, "websocket", "incoming", "a", "ws1"),
        make_stream_event(1, "websocket", "incoming", "b", "ws1"),
    ]

    page = type("Page", (), {})()
    page._test_replay_log = []

    first = replay_stream_events(page, events)
    second = replay_stream_events(type("Page", (), {"_test_replay_log": []})(), events)

    assert first["replay"][0]["event"] == second["replay"][0]["event"]
    assert first["replay"][1]["event"]["payload"] == "b"

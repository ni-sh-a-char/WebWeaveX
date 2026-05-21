from core.streaming import build_stream_timeline
from core.streaming.stream_capture_engine import make_stream_event


def test_stream_timeline_ordering():
    events = [
        make_stream_event(1, "sse", "incoming", "second", "sse"),
        make_stream_event(0, "websocket", "incoming", "first", "ws"),
    ]

    timeline = build_stream_timeline(events)

    assert timeline["events"][0]["payload"] == "first"
    assert timeline["events"][1]["payload"] == "second"
    assert len(timeline["edges"]) == 1

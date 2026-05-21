from core.streaming import (
    create_stream_checkpoint,
    restore_stream_checkpoint,
)
from core.streaming.stream_capture_engine import make_stream_event


def test_stream_checkpoint_restore():
    events = [
        make_stream_event(0, "websocket", "incoming", "a", "ws"),
        make_stream_event(1, "websocket", "incoming", "b", "ws"),
    ]

    runtime = {
        "events": events,
        "runtime_state": {"cursor": 2},
    }

    checkpoint = create_stream_checkpoint(runtime, 1)
    restored = restore_stream_checkpoint(checkpoint)

    assert restored["position"] == 1
    assert len(restored["events"]) == 1
    assert restored["events"][0]["payload"] == "a"
    assert restored["checkpoint_hash"] == checkpoint["checkpoint_hash"]

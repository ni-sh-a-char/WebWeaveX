from core.streaming import load_stream_runtime, save_stream_runtime
from core.streaming.stream_capture_engine import make_stream_event


def test_stream_persistence_roundtrip(tmp_path):
    runtime = {
        "events": [
            make_stream_event(0, "websocket", "incoming", "secret", "ws1"),
        ],
        "runtime_state": {"cursor": 1},
        "bounded": True,
    }

    path = tmp_path / "stream.enc"
    save_stream_runtime(str(path), runtime, "stream-key")

    raw = path.read_text(encoding="utf-8")

    assert "secret" not in raw

    loaded = load_stream_runtime(str(path), "stream-key")

    assert loaded["available"] is True
    assert loaded["events"][0]["payload"] == "secret"

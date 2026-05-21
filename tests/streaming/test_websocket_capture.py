from core.streaming import capture_websocket_frames, track_websocket_connections


class _Page:
    _test_websocket_frames = [
        {
            "connection_id": "ws1",
            "url": "wss://example.com/socket",
            "direction": "incoming",
            "payload": "hello",
        },
        {
            "connection_id": "ws1",
            "direction": "outgoing",
            "payload": "ack",
        },
    ]


def test_websocket_ordering():
    page = _Page()

    frames = capture_websocket_frames(page)
    connections = track_websocket_connections(page)

    assert frames["events"][0]["payload"] == "hello"
    assert frames["events"][1]["payload"] == "ack"
    assert connections["connections"][0]["connection_id"] == "ws1"

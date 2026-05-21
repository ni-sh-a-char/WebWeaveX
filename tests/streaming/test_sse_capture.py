from core.streaming import capture_server_sent_events


def test_sse_ordering():
    page = type("Page", (), {})()
    page._test_sse_events = [
        {"event_type": "message", "payload": "one"},
        {"event_type": "update", "payload": "two"},
    ]

    result = capture_server_sent_events(page)

    assert result["events"][0]["payload"] == "one"
    assert result["events"][1]["payload"] == "two"

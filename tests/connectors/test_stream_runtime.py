from core.connectors import extract_runtime_streams, run_live_runtime


def test_stream_replay():
    snapshot = {
        "kafka": {
            "topics": ["events"],
            "lineage": ["evt:0", "evt:1"],
            "offsets": {"events": 42},
        },
    }

    first = run_live_runtime(snapshot=snapshot, tick=1)
    second = run_live_runtime(snapshot=snapshot, tick=1)

    assert first["replay"] == second["replay"]
    streams = extract_runtime_streams(["kafka"], snapshot)
    assert streams["streams"][0]["topics"] == ["events"]

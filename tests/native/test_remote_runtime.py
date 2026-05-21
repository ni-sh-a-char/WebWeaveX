from core.native.native_remote_session_engine import extract_remote_runtime


def test_remote_runtime_ssh():
    remote = extract_remote_runtime(
        "ssh",
        {
            "session_id": "sess-1",
            "host": "10.0.0.1",
            "port": 22,
            "authenticated": True,
        },
    )

    assert remote["protocol"] == "ssh"
    assert remote["authenticated"] is True

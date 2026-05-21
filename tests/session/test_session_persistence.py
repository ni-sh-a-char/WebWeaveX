from core.session.encrypted_session_store import (
    load_encrypted_session,
    save_encrypted_session,
)


def test_session_roundtrip(tmp_path):
    session = {
        "cookies": [{"name": "sid", "value": "abc123"}],
        "headers": {"Authorization": "Bearer token"},
        "auth_tokens": [{"type": "bearer", "value": "token"}],
        "local_storage": {"auth": "1"},
        "session_storage": {},
        "authenticated": True,
    }

    path = tmp_path / "session.enc"

    save_encrypted_session(str(path), session, "test-key")
    loaded = load_encrypted_session(str(path), "test-key")

    assert loaded["available"] is True
    assert loaded["session"] == session

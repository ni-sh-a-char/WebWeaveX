from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)


def test_session_serialization_stable():
    session = {
        "cookies": [{"name": "sid", "value": "abc"}],
        "headers": {"Authorization": "Bearer token"},
        "local_storage": {},
        "auth_tokens": ["t1"],
        "replay_state": {"step": 1},
    }

    first = encrypt_session_state(session, "session-key")
    second = encrypt_session_state(session, "session-key")

    assert first["encrypted"] == second["encrypted"]

    restored = decrypt_session_state(first, "session-key")

    assert restored["session"] == session

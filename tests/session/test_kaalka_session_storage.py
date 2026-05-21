from core.session.encrypted_session_store import save_encrypted_session


def test_encryption_validation(tmp_path):
    session = {
        "cookies": [{"name": "secret_cookie", "value": "super-secret-value"}],
        "headers": {"Authorization": "Bearer super-secret-token"},
        "auth_tokens": [{"type": "bearer", "value": "super-secret-token"}],
    }

    path = tmp_path / "session.enc"

    save_encrypted_session(str(path), session, "kaalka-key")

    raw = path.read_text(encoding="utf-8")

    assert "super-secret-value" not in raw
    assert "super-secret-token" not in raw
    assert "secret_cookie" not in raw

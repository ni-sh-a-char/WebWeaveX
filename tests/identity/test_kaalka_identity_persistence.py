from core.identity import (
    build_browser_identity,
    load_browser_identity,
    save_browser_identity,
)


def test_kaalka_identity_persistence(tmp_path):
    identity = build_browser_identity("default")
    path = tmp_path / "identity.enc"

    save_browser_identity(str(path), identity, "identity-key")

    raw = path.read_text(encoding="utf-8")

    assert identity["user_agent"] not in raw

    loaded = load_browser_identity(str(path), "identity-key")

    assert loaded["available"] is True
    assert loaded["identity"] == identity

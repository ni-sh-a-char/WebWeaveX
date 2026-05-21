from core.identity import build_browser_identity, replay_browser_identity


def test_replay_stability():
    identity = build_browser_identity("default")

    first = replay_browser_identity(identity)
    second = replay_browser_identity(identity)

    assert (
        first["identity"]["fingerprint_hash"]
        == second["identity"]["fingerprint_hash"]
    )
    assert first["identity"]["canvas_fingerprint"] == (
        second["identity"]["canvas_fingerprint"]
    )

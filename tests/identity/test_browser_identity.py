from core.identity import build_browser_identity


def test_identity_stability():
    first = build_browser_identity("default")
    second = build_browser_identity("default")

    assert first["fingerprint_hash"] == second["fingerprint_hash"]
    assert first["canvas_fingerprint"] == second["canvas_fingerprint"]
    assert first["user_agent"] == second["user_agent"]

from core.identity import build_browser_identity, rotate_browser_identity


def test_identity_rotation_bounded():
    identity = build_browser_identity("default")

    rotated = rotate_browser_identity(identity)

    assert rotated["profile_id"] != identity["profile_id"]
    assert rotated["rotation_index"] == 1

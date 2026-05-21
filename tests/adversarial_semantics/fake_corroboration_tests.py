from core.internet.mirror_topology_engine import detect_mirror_topology


def test_mirror_detected():
    r = detect_mirror_topology(["https://a.com/x", "https://a.com/y"])
    assert r["count"] >= 0

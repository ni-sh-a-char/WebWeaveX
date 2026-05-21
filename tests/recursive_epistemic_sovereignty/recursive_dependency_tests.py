from core.evidence.recursive_dependency_engine import detect_recursive_dependency


def test_dependency_suppressed():
    d = detect_recursive_dependency(3, 1, 0)
    assert d["dependent"] is True
    assert d["suppressed"]

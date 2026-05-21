from core.evidence.recursive_consensus_engine import detect_recursive_consensus


def test_consensus_suppressed():
    c = detect_recursive_consensus(True, 3, 0)
    assert c["suppress"] is True

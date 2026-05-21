from core.evidence import structure_cognition


def test_streaming_chunks():
    chunks = [{"a": i} for i in range(3)]
    results = [structure_cognition(c, {}, c) for c in chunks]
    assert all(r["civilizational_openness"]["open"] for r in results)

from core.evidence import structure_cognition


def test_no_code_execution_in_bundle():
    r = structure_cognition({"__import__": "os"}, {}, {})
    assert isinstance(r, dict)
    assert r["civilizational_openness"]["open"] is True

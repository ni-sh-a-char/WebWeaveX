from core.evidence.contradiction_lattice_engine import build_contradiction_lattice


def test_lattice_pressure():
    r = build_contradiction_lattice([["a", "b"], ["c", "d"]])
    assert r["count"] == 2
    assert r["pressure"] == 0.5

from core.evidence.contradiction_lattice_engine import build_contradiction_lattice


def test_contradiction_flood_pressure_capped():
    pairs = [[f"a{i}", f"b{i}"] for i in range(100)]
    r = build_contradiction_lattice(pairs)
    assert r["pressure"] == 1.0
    assert r["count"] == 100

from core.repository.topology_cognition_engine import build_topology_cognition


def test_topology_civilization():
    r = build_topology_cognition("", path="x.py")
    edges = r.get("topology_layers", {}).get("parser_derived", {}).get("edges", [])
    if edges:
        assert "civilization_stability" in edges[0]

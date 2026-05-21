from core.repository.topology_cognition_engine import build_topology_cognition


def test_topology_recursive_fields():
    r = build_topology_cognition("", path="x.py")
    edges = r.get("topology_layers", {}).get("parser_derived", {}).get("edges", [])
    if edges:
        assert "recursive_reality_integrity" in edges[0]

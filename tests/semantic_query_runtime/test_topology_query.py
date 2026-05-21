from core.query.topology_query_engine import query_topology


def test_topology_query_returns_bfs_order():
    adj = {"a": ["b", "c"], "b": ["d"], "c": [], "d": []}
    r = query_topology(adj, "a")
    assert r["order"][0] == "a"
    assert "b" in r["order"] and "c" in r["order"]

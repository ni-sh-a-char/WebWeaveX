from core.graph.graph_invariant_engine import check_graph_invariants
from core.graph.topology_proof_engine import prove_topology


def test_graph_invariant_and_proof():
    g = {"nodes": [{"id": "a", "kind": "n"}, {"id": "b", "kind": "n"}], "edges": [{"from": "a", "to": "b", "evidence": ["e"]}]}
    assert check_graph_invariants(g)["valid"] is True
    assert prove_topology(g)["proved"] is True

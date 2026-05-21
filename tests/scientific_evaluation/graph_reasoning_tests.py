from core.graph.graph_consistency_prover import prove_graph_consistency
from core.graph.semantic_cycle_analysis_engine import detect_cycles


def test_cycle_and_consistency():
    cyclic = {
        "nodes": [{"id": "a", "kind": "n"}, {"id": "b", "kind": "n"}],
        "edges": [{"from": "a", "to": "b", "evidence": ["e"]}, {"from": "b", "to": "a", "evidence": ["e"]}],
    }
    assert detect_cycles(cyclic)["cycle_count"] >= 1
    acyclic = {
        "nodes": [{"id": "a", "kind": "n"}, {"id": "b", "kind": "n"}],
        "edges": [{"from": "a", "to": "b", "evidence": ["e"]}],
    }
    assert prove_graph_consistency(acyclic)["proved"] is True

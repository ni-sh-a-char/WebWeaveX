from core.internet.corroboration_graph_engine import build_corroboration_graph
from core.internet.semantic_consensus_graph_engine import build_semantic_consensus_graph


def test_corroboration_graph():
    g = build_corroboration_graph([{"url": "https://a.com"}, {"url": "https://b.com"}])
    assert len(g["nodes"]) == 2


def test_consensus_graph():
    g = build_semantic_consensus_graph([{"url": "u1"}], [{"text": "same"}, {"text": "same"}])
    assert g["strength"] >= 0

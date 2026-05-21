from core.documents.tutorial_causality_engine import reconstruct_tutorial_causality


def test_tutorial_prerequisite_edges_follow_order():
    sections = [
        {"id": "a", "order": 2},
        {"id": "b", "order": 0},
        {"id": "c", "order": 1},
    ]
    r = reconstruct_tutorial_causality(sections)
    assert r["count"] == 2
    assert r["tutorial_edges"][0]["from"] == "b"

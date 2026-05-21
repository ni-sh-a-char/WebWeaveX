from core.adaptive import compute_dom_similarity


def test_dom_similarity_score():
    left = [{"tag": "div", "text": "a", "depth": 1}]
    right = [{"tag": "div", "text": "a", "depth": 1}]

    result = compute_dom_similarity(left, right)

    assert result["score"] == 1.0

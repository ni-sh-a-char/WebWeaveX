from core.streaming import capture_dom_mutations


def test_dom_mutation_stability():
    page = type("Page", (), {})()
    page._test_html = "<html><body>one</body></html>"
    page._test_dom_mutations = [
        {"type": "add", "node_id": "n1", "payload": "<div>a</div>"},
        {"type": "text", "node_id": "n1", "payload": "updated"},
    ]

    first = capture_dom_mutations(page)
    second = capture_dom_mutations(page)

    assert first["dom_hash"] == second["dom_hash"]
    assert len(first["events"]) == 2

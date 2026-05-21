from core.adaptive import heal_selector


def test_selector_recovery():
    dom_nodes = [
        {
            "tag": "button",
            "text": "Next Page",
            "attrs": {"aria-label": "Next"},
        }
    ]
    html = '<button aria-label="Next">Next Page</button>'

    result = heal_selector("#broken-next", dom_nodes, html)

    assert result["healed_selector"]
    assert result["strategy"] in {
        "semantic_anchor",
        "text_anchor",
        "attribute_anchor",
        "structural_fallback",
    }

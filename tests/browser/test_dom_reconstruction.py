from core.dom.dom_reconstruction_engine import reconstruct_dom


def test_reconstruct_dom():
    html = "<html><body><p>hello</p><div>world</motion></div></body></html>"
    result = reconstruct_dom(html)

    assert result["node_count"] >= 2
    assert result["bounded"] is True

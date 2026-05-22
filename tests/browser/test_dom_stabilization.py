from core.browser.dom_stabilization_engine import stabilize_dom_html


def test_stabilize_dom_removes_uuid():
    html = '<div id="a" data-id="550e8400-e29b-41d4-a716-446655440000">x</div>'
    stable, meta = stabilize_dom_html(html)
    assert "550e8400" not in stable
    assert meta["replacements"]["uuids"] >= 1


def test_stabilize_dom_deterministic():
    html = '<p data-reactid="1">Hi</p><time>2026-05-22T12:00:00Z</time>'
    s1, _ = stabilize_dom_html(html)
    s2, _ = stabilize_dom_html(html)
    assert s1 == s2

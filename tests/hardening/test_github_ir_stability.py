import pytest

from core.browser.spa_runtime_stabilizer import build_spa_stabilization
from core.browser.universal_web_extraction_engine import extract_web
from core.ir.browser_ir import compile_browser_ir


@pytest.mark.integration
def test_github_same_html_produces_stable_fingerprint():
    """Same HTML bytes must yield identical SPA and browser IR identity."""
    result = extract_web("https://github.com")
    runtime = result.get("runtime", {})
    if not runtime.get("available"):
        pytest.skip("playwright unavailable")
    html = runtime.get("html", "")
    url = runtime.get("url", "https://github.com")

    s1 = build_spa_stabilization(html, url)
    s2 = build_spa_stabilization(html, url)
    assert s1["spa_fingerprint"] == s2["spa_fingerprint"]
    assert s1["stable_dom_hash"] == s2["stable_dom_hash"]

    ir1 = compile_browser_ir(
        runtime={**runtime, "spa_stabilization": s1, "dom_stabilization": s1["dom_stabilization"]},
        dom=result.get("dom", {}),
        extraction=result.get("extraction", {}),
        network=result.get("network", {}),
    )
    ir2 = compile_browser_ir(
        runtime={**runtime, "spa_stabilization": s2, "dom_stabilization": s2["dom_stabilization"]},
        dom=result.get("dom", {}),
        extraction=result.get("extraction", {}),
        network=result.get("network", {}),
    )
    assert ir1["runtime_identity"] == ir2["runtime_identity"]

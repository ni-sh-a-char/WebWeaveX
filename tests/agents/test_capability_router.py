from core.agents import route_semantic_capability


def test_capability_router_selects_agent():
    r = route_semantic_capability(
        "run",
        [{"id": "b", "capabilities": []}, {"id": "a", "capabilities": ["run"]}],
    )
    assert r["selected"] == "a"

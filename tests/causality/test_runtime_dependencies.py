from core.causality.runtime_dependency_engine import build_runtime_dependencies


def test_runtime_dependencies_chain():
    events = [
        {"id": "a", "runtime": "browser", "step": 0},
        {"id": "b", "runtime": "desktop", "step": 1},
        {"id": "c", "runtime": "terminal", "step": 2},
    ]

    deps = build_runtime_dependencies(events, {"handoffs": []})

    assert len(deps["dependencies"]) == 2
    assert deps["dependencies"][0]["relation"] == "depends_on"

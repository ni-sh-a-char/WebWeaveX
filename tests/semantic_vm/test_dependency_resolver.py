from core.runtime.semantic_dependency_resolver import resolve_dependencies


def test_resolve_dependencies():
    tasks = [
        {"id": "a", "depends_on": []},
        {"id": "b", "depends_on": ["a"]},
    ]
    r = resolve_dependencies(tasks)
    assert len(r["resolved"]) == 2
    assert r["unresolved"] == []

from core.reconstruction.runtime_clone_engine import clone_runtime_environment


def test_runtime_clone_consistency():
    source = {
        "runtime_graph": {"nodes": [{"id": "n1"}], "edges": []},
        "browser": {"tabs": [{"id": "tab:0"}]},
        "workflows": [{"id": "wf:1"}],
    }

    first = clone_runtime_environment(source)
    second = clone_runtime_environment(source)

    assert first == second
    assert first["cloned"] is True
    assert source["browser"] == {"tabs": [{"id": "tab:0"}]}

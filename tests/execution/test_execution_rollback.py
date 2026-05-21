from core.execution.runtime_rollback_engine import rollback_runtime_state


def test_rollback_consistency():
    prior = {
        "browser": {"url": "https://example.com"},
        "workflow": {"step": 1},
    }
    current = {
        "browser": {"url": "https://changed.example.com"},
        "workflow": {"step": 2},
    }

    first = rollback_runtime_state(prior, current)
    second = rollback_runtime_state(prior, current)

    assert first == second
    assert first["restored_state"]["browser"] == prior["browser"]

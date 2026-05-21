from core.causality import run_causality_runtime
from core.causality.causal_replay_engine import replay_causal_runtime


def test_causal_replay_identical():
    result = run_causality_runtime(
        interactions=[
            {"action": "click", "selector": "#btn"},
            {"action": "navigate", "to": "/dashboard"},
        ],
        native_cognition={
            "runtime": "desktop",
            "interactions": [{"action": "focus"}],
            "terminal": {"output": ["$ ls", "ok"]},
            "electron": {"routes": ["/app"]},
            "desktop": {"notifications": ["update"]},
            "processes": {"processes": [{"name": "node"}]},
        },
    )

    memory = result["memory"]
    first = replay_causal_runtime(memory)
    second = replay_causal_runtime(memory)

    assert first == second
    assert result["replay"] == first

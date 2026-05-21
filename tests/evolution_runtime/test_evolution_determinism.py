from core.evolution_runtime import run_evolution_runtime


def test_evolution_determinism_full():
    kwargs = {
        "adaptive_memory": {
            "healed_selectors": {"#login": "[data-test='login']"},
            "selectors": {"#dashboard": ".dashboard"},
        },
        "workflow_result": {
            "workflow": {
                "plan": {"steps": [{"id": "step:0", "priority": 0}]},
                "execution": {"executed": [{"step_id": "step:0"}]},
            },
        },
        "tick": 5,
    }

    first = run_evolution_runtime(**kwargs)
    second = run_evolution_runtime(**kwargs)

    assert first["evolution"] == second["evolution"]
    assert first["selector"] == second["selector"]
    assert first["workflow"] == second["workflow"]

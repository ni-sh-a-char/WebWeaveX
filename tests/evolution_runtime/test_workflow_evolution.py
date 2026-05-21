from core.evolution_runtime.workflow_evolution_engine import evolve_workflow_runtime


def test_workflow_evolution_ordering():
    plan = {
        "steps": [
            {"id": "step:1", "priority": 1},
            {"id": "step:0", "priority": 0},
        ],
    }
    execution = {"executed": [{"step_id": "step:0"}, {"step_id": "step:1"}]}

    first = evolve_workflow_runtime(plan, execution, [])
    second = evolve_workflow_runtime(plan, execution, [])

    assert first == second
    assert first["execution_ordering"][0] == "step:1"

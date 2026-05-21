from core.workflows.objective_engine import build_runtime_objective
from core.workflows.workflow_planner_engine import build_workflow_plan


def test_objective_determinism():
    first_obj = build_runtime_objective("extract_dashboard")
    second_obj = build_runtime_objective("extract_dashboard")

    first_plan = build_workflow_plan("extract_dashboard")
    second_plan = build_workflow_plan("extract_dashboard")

    assert first_obj == second_obj
    assert first_plan == second_plan

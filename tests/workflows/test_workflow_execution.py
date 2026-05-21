from core.workflows.workflow_execution_engine import execute_workflow_plan
from core.workflows.workflow_planner_engine import build_workflow_plan


def test_workflow_execution_replay_index():
    plan = build_workflow_plan("extract_invoices")
    result = execute_workflow_plan(plan, tick=10)

    assert result["completed_count"] == len(plan["steps"])
    assert all(step["replay_index"] == index for index, step in enumerate(result["executed"]))

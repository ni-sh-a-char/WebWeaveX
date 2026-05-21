from core.workflows.workflow_planner_engine import build_workflow_plan


def test_workflow_plan_steps():
    plan = build_workflow_plan("monitor_metrics")

    assert plan["objective"] == "monitor_metrics"
    assert len(plan["steps"]) >= 3

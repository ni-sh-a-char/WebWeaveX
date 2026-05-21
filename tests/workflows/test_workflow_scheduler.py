from core.workflows.workflow_scheduler_engine import schedule_workflow_execution
from core.workflows.objective_engine import build_runtime_objective


def test_distributed_ordering():
    plans = [
        {**build_runtime_objective("monitor_metrics", priority=2), "priority": 2},
        {**build_runtime_objective("extract_dashboard", priority=0), "priority": 0},
        {**build_runtime_objective("extract_invoices", priority=1), "priority": 1},
    ]

    first = schedule_workflow_execution(plans, tick=0)
    second = schedule_workflow_execution(plans, tick=0)

    assert first == second
    assert first["schedule"][0]["objective"] == "extract_dashboard"

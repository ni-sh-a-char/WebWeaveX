from core.application import execute_runtime_objective
from core.application.workflow_graph_engine import build_workflow_graph


def test_objective_execution():
    workflow = build_workflow_graph(
        [{"route": "/"}],
        [],
        [],
    )

    result = execute_runtime_objective(
        objective="extract_dashboard",
        workflow_graph=workflow,
        action_graph={"nodes": [], "edges": []},
        navigation={"routes": [{"path": "/dashboard"}]},
    )

    assert result["objective"] == "extract_dashboard"
    assert len(result["executed"]) == 3
    assert all(step["completed"] for step in result["executed"])

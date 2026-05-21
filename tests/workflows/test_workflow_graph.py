from core.workflows import run_autonomous_workflow


def test_workflow_graph_stability():
    first = run_autonomous_workflow(objective="extract_dashboard")
    second = run_autonomous_workflow(objective="extract_dashboard")

    assert first["workflow_graph"] == second["workflow_graph"]
    assert first["execution"] == second["execution"]

from core.workflows.workflow_federation_engine import federate_workflow_runtime


def test_workflow_federation_stable():
    workers = [{"worker_id": "w1"}, {"worker_id": "w2"}]

    first = federate_workflow_runtime(
        browser={"url": "https://example.com"},
        distributed={"workers": workers},
        workers=workers,
    )
    second = federate_workflow_runtime(
        browser={"url": "https://example.com"},
        distributed={"workers": workers},
        workers=workers,
    )

    assert first == second
    assert first["extraction_agents"] == 2

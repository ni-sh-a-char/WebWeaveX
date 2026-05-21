from core.execution.runtime_federation_engine import federate_runtime_execution


def test_federation_stability():
    workers = [
        {"worker_id": "browser-1", "runtime": "browser"},
        {"worker_id": "native-1", "runtime": "native"},
    ]

    first = federate_runtime_execution(workers)
    second = federate_runtime_execution(workers)

    assert first == second
    assert first["federated"] is True
    assert len(first["execution_routes"]) == 2

from core.connectors import extract_kubernetes_runtime


def test_kubernetes_consistency():
    snapshot = {
        "namespaces": ["default"],
        "pods": [{"name": "api-0"}, {"name": "worker-0"}],
        "deployments": [{"name": "api"}, {"name": "worker"}],
        "services": [{"name": "api-svc"}],
    }

    first = extract_kubernetes_runtime(snapshot)
    second = extract_kubernetes_runtime(snapshot)

    assert first == second
    assert len(first["deployments"]) == 2

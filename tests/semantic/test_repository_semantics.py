from core.semantic.repository_semantics_engine import extract_repository_semantics


def test_repository_api_surface():
    semantics = extract_repository_semantics(
        ["api/routes.py", "services/worker.py", "docker-compose.yml"],
        "fastapi service deploy",
    )

    assert semantics["api_ownership"] is True
    assert "deployment_topology" in semantics["architecture_roles"]

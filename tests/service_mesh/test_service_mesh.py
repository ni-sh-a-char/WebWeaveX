from core.distributed.semantic_service_mesh_engine import (
    build_semantic_service_mesh,
)


def test_service_mesh():
    result = build_semantic_service_mesh(
        [{"id": "api"}, {"id": "db"}]
    )

    assert len(result["links"]) == 1

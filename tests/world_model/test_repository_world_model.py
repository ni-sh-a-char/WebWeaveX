from core.world_model import (
    build_repository_world_model,
)


def test_repository_world_model():

    irs = [
        {
            "path": "a.py",
            "semantic_ast": {
                "symbols": [
                    {"name": "run"},
                ],
                "imports": [],
            },
        }
    ]

    result = (
        build_repository_world_model(
            irs
        )
    )

    assert result["file_count"] == 1

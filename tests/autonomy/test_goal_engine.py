from core.autonomy import (
    resolve_semantic_goal,
)


def test_goal_engine():

    result = resolve_semantic_goal(
        {
            "goal": "analyze repository",
        }
    )

    assert result["resolved"] is True

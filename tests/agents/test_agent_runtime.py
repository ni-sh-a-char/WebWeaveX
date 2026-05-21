from core.agents import (
    SemanticAgent,
    SemanticAgentRuntime,
)


def test_agent_runtime():
    runtime = SemanticAgentRuntime()

    runtime.register(
        SemanticAgent(
            agent_id="a1",
            capabilities=["run"],
        )
    )

    result = runtime.execute(
        "a1",
        {"x": 1},
    )

    assert result["status"] == "completed"

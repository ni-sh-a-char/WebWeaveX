from __future__ import annotations

from typing import Any, Dict

from .semantic_agent_engine import SemanticAgent


class SemanticAgentRuntime:
    def __init__(self) -> None:
        self._agents: Dict[str, SemanticAgent] = {}

    def register(
        self,
        agent: SemanticAgent,
    ) -> None:

        self._agents[agent.agent_id] = agent

    def execute(
        self,
        agent_id: str,
        task: Dict[str, Any],
    ) -> Dict[str, Any]:

        agent = self._agents[agent_id]

        return agent.execute(task)

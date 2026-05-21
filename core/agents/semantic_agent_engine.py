from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


MAX_AGENT_TASKS = 1000


@dataclass
class SemanticAgent:
    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)

    def execute(
        self,
        task: Dict[str, Any],
    ) -> Dict[str, Any]:

        bounded_task = {
            k: task[k]
            for k in sorted(task.keys())[:MAX_AGENT_TASKS]
        }

        return {
            "agent_id": self.agent_id,
            "task": bounded_task,
            "status": "completed",
        }

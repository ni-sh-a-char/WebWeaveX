from __future__ import annotations

from typing import Any, Dict, List


MAX_AGENTS = 1024


def coordinate_semantic_agents(
    agents: List[Dict[str, Any]],
    tasks: List[Dict[str, Any]],
) -> Dict[str, Any]:

    bounded_agents = agents[:MAX_AGENTS]

    assignments = []

    for idx, task in enumerate(tasks):

        if not bounded_agents:
            break

        agent = bounded_agents[
            idx % len(bounded_agents)
        ]

        assignments.append(
            {
                "agent": agent.get("id"),
                "task": task.get("id"),
            }
        )

    return {
        "assignments": assignments,
        "bounded": True,
    }

from __future__ import annotations

from typing import Any, Dict, List, Optional


def schedule_runtime_execution(
    actions: List[Dict[str, Any]],
    priorities: Optional[Dict[str, int]] = None,
    cooldown_ticks: int = 0,
    worker_id: str = "worker:0",
    tick: int = 0,
) -> Dict[str, Any]:
    priorities = priorities or {}
    scheduled: List[Dict[str, Any]] = []

    for index, action in enumerate(actions[:10000]):
        action_id = str(action.get("id", f"action:{index}"))
        priority = int(priorities.get(action_id, 0))
        scheduled.append({
            "action": action,
            "priority": priority,
            "worker_id": worker_id,
            "tick": tick + (index * max(cooldown_ticks, 0)),
            "retry": 0,
            "paced": True,
        })

    scheduled = sorted(scheduled, key=lambda item: (-item["priority"], item["tick"], str(item["action"].get("id", ""))))

    return {
        "scheduled": scheduled,
        "worker_id": worker_id,
        "cooldown_ticks": cooldown_ticks,
        "deterministic": True,
        "bounded": True,
    }

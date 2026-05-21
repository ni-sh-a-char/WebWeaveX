from __future__ import annotations

from core.orchestration.extraction_planner import plan_extraction
from core.orchestration.extraction_scheduler import schedule
from core.orchestration.extraction_state_engine import initial_state
from core.orchestration.extraction_strategy_engine import strategy_for


def orchestrate(seed: str):
    plan = plan_extraction(seed)
    return {
        "plan": plan,
        "schedule": schedule(plan),
        "state": initial_state(seed),
        "strategy": strategy_for(seed),
    }


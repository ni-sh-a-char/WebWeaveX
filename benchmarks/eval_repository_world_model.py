from __future__ import annotations

from typing import Any, Dict

from core.world_model import build_repository_world_model


def eval_repository_world_model(case: Dict[str, Any]) -> Dict[str, Any]:
    result = build_repository_world_model(case.get("repository_irs", []))
    pred = result.get("file_count") == case.get("expected_file_count")
    return {
        "predicted": pred,
        "actual": {"file_count": result.get("file_count")},
        "expected": case.get("expected_file_count"),
    }

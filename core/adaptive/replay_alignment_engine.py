from __future__ import annotations

from typing import Any, Dict, List


def align_replay_state(
    expected: List[Dict[str, Any]],
    actual: List[Dict[str, Any]],
) -> Dict[str, Any]:
    aligned = []

    for index, item in enumerate(expected):
        actual_item = actual[index] if index < len(actual) else {}
        aligned.append({
            "step": index,
            "expected": item,
            "actual": actual_item,
            "matched": item == actual_item,
        })

    return {
        "aligned": aligned,
        "fully_aligned": all(step["matched"] for step in aligned),
        "bounded": True,
    }

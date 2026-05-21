from __future__ import annotations

from typing import Any, Dict, List


MAX_WAVES = 10000


def propagate_runtime_waves(
    propagation_paths: List[Dict[str, Any]],
) -> Dict[str, Any]:
    waves = []
    for idx, path in enumerate(
        propagation_paths[:MAX_WAVES]
    ):
        waves.append(
            {
                "wave": idx,
                "source": path.get("source"),
                "target": path.get("target"),
            }
        )
    return {
        "waves": waves,
        "wave_count": len(waves),
        "bounded": True,
    }

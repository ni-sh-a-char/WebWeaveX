from __future__ import annotations

from typing import Any, Dict


def preserve_recursive_autonomy(autonomous: bool) -> Dict[str, Any]:
    return {"preserved": autonomous, "centrality_blocked": not autonomous}

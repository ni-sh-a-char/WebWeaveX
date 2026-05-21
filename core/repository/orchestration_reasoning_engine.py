from __future__ import annotations

from typing import Dict, List


def reason_orchestration(services: List[str], dependencies: List[str]) -> Dict[str, object]:
    svc = sorted(set(str(s) for s in (services or []) if s))
    deps = sorted(set(str(d) for d in (dependencies or []) if d))
    edges = [{"from": svc[i], "to": svc[i + 1]} for i in range(len(svc) - 1)]
    return {"services": svc, "dependencies": deps, "flow_edges": edges}

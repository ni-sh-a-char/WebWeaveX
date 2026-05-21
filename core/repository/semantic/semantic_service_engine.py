from __future__ import annotations

from typing import Dict, List


def infer_semantic_services(topology: Dict[str, List[str]], imports: List[str], routes: List[str], dependencies: List[str]) -> Dict[str, List[str]]:
    modules = sorted(set((topology or {}).get("modules", [])))
    services = sorted({m for m in modules if "/" in m or "\\" in m})
    apis = sorted(set(r.split()[0] if " " in r else r for r in routes or []))
    queues = sorted([d for d in (dependencies or []) if d.lower() in {"celery", "rq", "kafka", "rabbitmq"}])
    gateways = sorted([imp for imp in (imports or []) if imp.lower().endswith(("gateway", "client"))])
    databases = sorted([d for d in (dependencies or []) if d.lower() in {"sqlalchemy", "psycopg2", "mongoose", "typeorm"}])
    return {
        "services": services,
        "apis": apis,
        "workers": sorted([s for s in services if s.lower().endswith(("worker", "job"))]),
        "schedulers": sorted([s for s in services if s.lower().endswith(("scheduler", "cron"))]),
        "queues": queues,
        "gateways": gateways,
        "databases": databases,
    }

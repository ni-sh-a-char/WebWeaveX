from __future__ import annotations

from typing import Any, Dict, Optional

from core.connectors.mysql_connector_engine import extract_mysql_runtime
from core.connectors.postgres_connector_engine import extract_postgres_runtime
from core.connectors.redis_connector_engine import extract_redis_runtime
from core.connectors.sqlite_connector_engine import extract_sqlite_runtime


def extract_database_runtime(
    database_type: str = "postgresql",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    normalized = database_type.lower()

    try:
        if normalized in ("postgres", "postgresql"):
            return extract_postgres_runtime(snapshot)
        if normalized == "mysql":
            return extract_mysql_runtime(snapshot)
        if normalized == "sqlite":
            return extract_sqlite_runtime(snapshot)
        if normalized == "redis":
            return extract_redis_runtime(snapshot)
    except Exception:
        return _degraded_database(normalized)

    return _degraded_database(normalized)


def _degraded_database(database_type: str) -> Dict[str, Any]:
    return {
        "database_type": database_type,
        "schemas": [],
        "tables": [],
        "metrics": {},
        "degraded": True,
        "reason": "connector_unavailable",
        "bounded": True,
    }

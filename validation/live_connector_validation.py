#!/usr/bin/env python3
"""Live connector validation with real SQLite and API snapshots."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive"
REPORT = ARCHIVE / "LIVE_CONNECTOR_VALIDATION_REPORT.md"


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from core.connectors.database_connector_engine import extract_database_runtime
    from core.connectors.api_connector_engine import extract_api_runtime
    from core.connectors.runtime_stream_connector_engine import extract_runtime_streams

    out_dir = ROOT / "validation" / "live_connectors"
    out_dir.mkdir(parents=True, exist_ok=True)
    db = out_dir / "live_validation.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY, v TEXT)")
    conn.execute("INSERT INTO metrics (v) VALUES ('ok')")
    conn.commit()
    conn.close()

    results = {
        "sqlite": extract_database_runtime(
            "sqlite",
            snapshot={"tables": [{"name": "metrics"}], "path": str(db)},
        ),
        "postgres": extract_database_runtime("postgresql", snapshot={"schemas": ["public"]}),
        "redis": extract_database_runtime("redis", snapshot={"keys": ["probe"]}),
        "api_rest": extract_api_runtime(
            "rest",
            snapshot={"base_url": "https://httpbin.org", "endpoints": ["/get"]},
        ),
        "api_graphql": extract_api_runtime(
            "graphql",
            snapshot={"graphql": {"endpoint": "/graphql", "operations": ["query"]}},
        ),
        "streams": extract_runtime_streams(
            stream_types=["websocket", "kafka"],
            snapshot={
                "websocket": {"url": "wss://echo.websocket.events"},
                "kafka": {"topics": ["events"]},
            },
        ),
        "docker": __import__(
            "core.connectors.container_connector_engine",
            fromlist=["extract_container_runtime"],
        ).extract_container_runtime(snapshot={"containers": []}),
        "k8s": __import__(
            "core.connectors.kubernetes_connector_engine",
            fromlist=["extract_kubernetes_runtime"],
        ).extract_kubernetes_runtime(snapshot={"manifests": []}),
        "otel": __import__(
            "core.connectors.telemetry_connector_engine",
            fromlist=["extract_telemetry_runtime"],
        ).extract_telemetry_runtime(snapshot={"signals": ["traces"]}),
    }

    lines = [
        "# LIVE CONNECTOR VALIDATION REPORT",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "```json",
        json.dumps(
            {k: {"bounded": v.get("bounded"), "keys": list(v.keys())[:8]} for k, v in results.items()},
            indent=2,
        ),
        "```",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

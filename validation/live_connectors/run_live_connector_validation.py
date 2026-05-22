#!/usr/bin/env python3
"""Live connector smoke tests (SQLite + API snapshots)."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.connectors.database_connector_engine import extract_database_runtime
from core.connectors.api_connector_engine import extract_api_runtime
from core.connectors.runtime_stream_connector_engine import extract_runtime_streams


def main() -> int:
    db = ROOT / "validation" / "live_connectors" / "live.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE IF NOT EXISTS probe (k TEXT PRIMARY KEY, v TEXT)")
    conn.execute("INSERT OR REPLACE INTO probe VALUES ('ok', 'webweavex')")
    conn.commit()
    conn.close()

    results = {
        "sqlite": extract_database_runtime(
            "sqlite",
            snapshot={"tables": [{"name": "probe"}], "path": str(db)},
        ),
        "api": extract_api_runtime(
            "rest",
            snapshot={"base_url": "https://httpbin.org", "endpoints": ["/get"]},
        ),
        "streams": extract_runtime_streams(
            stream_types=["websocket"],
            snapshot={"websocket": {"url": "wss://echo.websocket.events"}},
        ),
    }
    for name, payload in results.items():
        print(name, payload.get("bounded"), list(payload.keys())[:6])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.connectors.kafka_connector_engine import extract_kafka_runtime
from core.connectors.redis_connector_engine import extract_redis_runtime
from core.connectors.websocket_connector_engine import extract_websocket_runtime


def extract_runtime_streams(
    stream_types: Optional[List[str]] = None,
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    stream_types = stream_types or ["kafka", "redis", "websocket"]
    snap = snapshot or {}
    streams: List[Dict[str, Any]] = []

    for stream_type in sorted(stream_types):
        try:
            if stream_type == "kafka":
                streams.append(extract_kafka_runtime(snap.get("kafka")))
            elif stream_type == "redis":
                redis = extract_redis_runtime(snap.get("redis"))
                streams.append({
                    "stream_type": "redis_streams",
                    "topics": redis.get("streams", []),
                    "offsets": {},
                    "event_lineage": [],
                    "bounded": True,
                })
            elif stream_type == "websocket":
                ws = extract_websocket_runtime(snap.get("websocket"))
                streams.append({
                    "stream_type": "websocket",
                    "topics": ws.get("connections", []),
                    "offsets": {},
                    "event_lineage": [],
                    "bounded": True,
                })
            elif stream_type in ("sse", "queue"):
                streams.append({
                    "stream_type": stream_type,
                    "topics": list(snap.get(stream_type, {}).get("topics", [])),
                    "offsets": {},
                    "event_lineage": [],
                    "bounded": True,
                })
        except Exception:
            streams.append({
                "stream_type": stream_type,
                "degraded": True,
                "bounded": True,
            })

    return {
        "streams": streams,
        "count": len(streams),
        "bounded": True,
    }

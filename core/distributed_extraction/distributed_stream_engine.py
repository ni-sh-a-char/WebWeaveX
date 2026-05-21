from __future__ import annotations

from typing import Any, Dict, List

from core.streaming.stream_persistence_engine import merge_stream_runtimes


def federate_stream_runtimes(
    streams: List[Dict[str, Any]],
) -> Dict[str, Any]:
    payloads = []

    for index, stream in enumerate(streams):
        events = stream.get("events", [])
        if not events and stream.get("stream_runtime"):
            events = stream["stream_runtime"].get("events", [])

        payloads.append({
            "source": str(stream.get("worker_id", f"worker_{index}")),
            "events": list(events),
        })

    merged = merge_stream_runtimes(payloads)

    return {
        "events": merged.get("events", []),
        "stream_count": merged.get("stream_count", 0),
        "bounded": True,
    }

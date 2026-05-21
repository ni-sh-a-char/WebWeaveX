from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload
from core.crypto.kaalka_session_engine import (
    decrypt_session_state,
    encrypt_session_state,
)
from core.streaming.stream_capture_engine import normalize_stream_events

MAX_STREAMS = 1000


def save_stream_runtime(
    path: str,
    runtime: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    payload = {
        "runtime": runtime,
        "events": normalize_stream_events(
            list(runtime.get("events", []))
        ),
        "bounded": True,
    }

    encrypted = encrypt_session_state(payload, key)

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(encrypted, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "saved": True,
        "path": str(target),
        "algorithm": "kaalka",
        "bounded": True,
    }


def load_stream_runtime(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)

    if not target.exists():
        return {
            "available": False,
            "runtime": {"events": [], "bounded": True},
            "bounded": True,
        }

    encrypted = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_session_state(encrypted, key)
    session_payload = decrypted.get("session", {})

    return {
        "available": True,
        "runtime": session_payload.get("runtime", {}),
        "events": session_payload.get("events", []),
        "algorithm": "kaalka",
        "bounded": True,
    }


def create_stream_checkpoint(
    runtime: Dict[str, Any],
    position: int,
) -> Dict[str, Any]:
    events = list(runtime.get("events", []))
    bounded_position = min(max(int(position), 0), len(events))

    checkpoint = {
        "position": bounded_position,
        "events": events[:bounded_position],
        "runtime_state": dict(runtime.get("runtime_state", {})),
        "checkpoint_hash": compute_kaalka_hash_payload({
            "position": bounded_position,
            "events": events[:bounded_position],
            "runtime_state": runtime.get("runtime_state", {}),
        }),
        "bounded": True,
    }

    return checkpoint


def restore_stream_checkpoint(
    checkpoint: Dict[str, Any],
) -> Dict[str, Any]:
    events = list(checkpoint.get("events", []))

    return {
        "position": int(checkpoint.get("position", 0)),
        "events": events,
        "runtime_state": dict(checkpoint.get("runtime_state", {})),
        "checkpoint_hash": checkpoint.get("checkpoint_hash", ""),
        "bounded": True,
    }


def merge_stream_runtimes(
    streams: List[Dict[str, Any]],
) -> Dict[str, Any]:
    merged_events: List[Dict[str, Any]] = []

    for stream_index, stream in enumerate(streams[:MAX_STREAMS]):
        source = str(stream.get("source", f"stream_{stream_index}"))
        events = normalize_stream_events(list(stream.get("events", [])))

        for event in events:
            enriched = dict(event)
            enriched["stream_source"] = source
            merged_events.append(enriched)

    merged_events = sorted(
        merged_events,
        key=lambda item: (
            int(item.get("timestamp", 0)),
            str(item.get("stream_source", "")),
            str(item.get("id", "")),
        ),
    )

    return {
        "events": merged_events,
        "stream_count": min(len(streams), MAX_STREAMS),
        "bounded": True,
    }

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional


def capture_terminal_runtime(
    lines: Optional[List[str]] = None,
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    output = list(lines or snap.get("output", []))[:50000]
    commands = list(snap.get("commands", []))[:10000]
    prompts = list(snap.get("prompts", []))[:1000]

    ansi_state = _parse_ansi_state(output)

    stream_id = str(snap.get("stream_id", "terminal:0"))

    return {
        "stream_id": stream_id,
        "output": output,
        "commands": commands,
        "prompts": prompts,
        "ansi_state": ansi_state,
        "replay_token": _terminal_replay_token(output, commands),
        "bounded": True,
    }


def _parse_ansi_state(lines: List[str]) -> Dict[str, Any]:
    bold = False
    color = "default"

    for line in lines[:5000]:
        if "\x1b[1m" in line:
            bold = True
        if "\x1b[32m" in line:
            color = "green"
        elif "\x1b[31m" in line:
            color = "red"

    return {"bold": bold, "color": color, "bounded": True}


def _terminal_replay_token(
    output: List[str],
    commands: List[str],
) -> str:
    parts = "|".join(commands[:100]) + "::" + "\n".join(output[:500])
    return hashlib.sha256(parts.encode("utf-8")).hexdigest()[:32]

from __future__ import annotations

from typing import Any, Dict, List, Optional


def extract_electron_ipc(
    channels: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    channel_list = sorted(
        channels
        or [
            {"channel": "ipc:renderer", "direction": "bidirectional"},
            {"channel": "ipc:preload", "direction": "main_to_renderer"},
        ],
        key=lambda c: str(c.get("channel", "")),
    )
    return {
        "channels": channel_list,
        "preload_metadata": sorted(
            [c for c in channel_list if "preload" in str(c.get("channel", ""))],
            key=lambda c: str(c.get("channel", "")),
        ),
        "bounded": True,
    }

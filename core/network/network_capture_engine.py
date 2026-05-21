from __future__ import annotations

from typing import Any, Dict, List

MAX_REQUESTS = 5000


def attach_network_capture(page: Any) -> Dict[str, Any]:
    requests: List[Dict[str, Any]] = []

    def on_request(req: Any) -> None:
        if len(requests) >= MAX_REQUESTS:
            return

        requests.append({
            "url": str(req.url)[:5000],
            "method": str(req.method),
            "resource_type": str(req.resource_type),
        })

    page.on("request", on_request)

    return {
        "requests": requests,
        "bounded": True,
    }

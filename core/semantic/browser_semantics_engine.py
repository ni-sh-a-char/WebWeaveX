from __future__ import annotations

from typing import Any, Dict, Optional


def extract_browser_semantics(
    url: str = "",
    html: str = "",
    extraction: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    extraction = extraction or {}

    return {
        "origin": url,
        "page_role": "web_application",
        "network_artifacts": len(extraction.get("requests", [])),
        "bounded": True,
    }

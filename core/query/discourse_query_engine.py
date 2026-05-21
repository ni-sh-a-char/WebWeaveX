from __future__ import annotations

from typing import Any, Dict, List


def query_discourse_sections(sections: List[Dict[str, Any]], section_id: str) -> Dict[str, Any]:
    match = next((s for s in sections if s.get("id") == section_id), None)
    return {"section": match, "found": match is not None, "deterministic": True}

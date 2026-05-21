from __future__ import annotations

from typing import Any, Dict, List


MAX_DISCOURSE = 200


class DiscourseMemory:
    def __init__(self) -> None:
        self._sections: List[Dict[str, Any]] = []

    def remember(self, section: Dict[str, Any]) -> None:
        if len(self._sections) < MAX_DISCOURSE:
            self._sections.append(section)

    def snapshot(self) -> Dict[str, Any]:
        ordered = sorted(self._sections, key=lambda s: int(s.get("order", 0)))
        return {"sections": ordered, "count": len(ordered), "deterministic": True}

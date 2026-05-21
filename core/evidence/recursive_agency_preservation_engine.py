from __future__ import annotations

from typing import Any, Dict


def preserve_recursive_agency(agency_ok: bool) -> Dict[str, Any]:
    return {"preserved": agency_ok, "weakening_blocked": True}

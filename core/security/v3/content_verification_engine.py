from __future__ import annotations

from .mime_validation_engine import validate_mime_v3
from .resource_limit_engine import check_resource_limits_v3


def verify_content_v3(content_type: str, payload_size: int):
    mime = validate_mime_v3(content_type)
    limits = check_resource_limits_v3(bytes_used=payload_size, memory_used=0)
    return {"allowed": bool(mime["allowed"] and limits["bytes_ok"]), "mime": mime, "limits": limits}

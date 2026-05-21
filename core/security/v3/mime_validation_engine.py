from __future__ import annotations


def validate_mime_v3(content_type: str, allowed: list[str] | None = None):
    allowed_types = sorted(set(allowed or ["text/html", "text/plain", "application/json", "application/xml", "text/markdown", "application/pdf"]))
    value = (content_type or "").split(";")[0].strip().lower()
    return {"allowed": value in allowed_types, "content_type": value, "allowed_types": allowed_types}

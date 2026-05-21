from __future__ import annotations

def malformed_payload_guard(text: str):
    src=(text or '').lower()
    blocked='<!entity' in src or '<!doctype' in src
    return {"ok": not blocked}

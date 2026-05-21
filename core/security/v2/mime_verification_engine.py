from __future__ import annotations
def verify_mime(expected:str, actual:str):
    return (expected or "") == (actual or "")

from __future__ import annotations

from core.repository.api_surface_engine import extract_api_surface


def extract_api_v2(text: str):
    return extract_api_surface(text)

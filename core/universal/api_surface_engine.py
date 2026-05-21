from __future__ import annotations

from core.repository.semantic.semantic_api_engine import reconstruct_semantic_api


def extract_api_surface_v2(text: str):
    return reconstruct_semantic_api(text)

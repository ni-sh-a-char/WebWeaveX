from __future__ import annotations

from core.repository.repository_intelligence import analyze_repository


def extract_architecture_v2(text: str, source_url: str = ""):
    repo = analyze_repository(text, source_url=source_url)
    return repo.get("architecture", {"layers": [], "components": [], "relationships": []})

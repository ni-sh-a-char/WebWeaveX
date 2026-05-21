from __future__ import annotations

from typing import Any, Dict

from core.documents.document_intelligence import analyze_document
from core.extract.architecture_extractor import extract_architecture
from core.extract.code_extractor import extract_code_features
from core.extract.dependency_extractor import extract_dependencies
from core.extract.html_extractor import extract_html
from core.extract.markdown_extractor import extract_markdown
from core.extract.metadata_extractor import extract_metadata
from core.extract.repository_extractor import extract_repository_data
from core.extract.repository_intelligence import extract_repository_intelligence
from core.extract.advanced.api_extractor import extract_api_v2
from core.extract.advanced.architecture_extractor_v2 import extract_architecture_v2
from core.extract.advanced.dependency_extractor_v2 import extract_dependencies_v2
from core.extract.advanced.docs_extractor_v2 import extract_docs_v2
from core.extract.advanced.repository_extractor_v2 import extract_repository_v2
from core.repository.repository_intelligence import analyze_repository


def _merge(*parts: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for part in parts:
        for key, value in part.items():
            if key not in out:
                out[key] = value
            elif isinstance(out[key], dict) and isinstance(value, dict):
                out[key] = {**out[key], **value}
    return out


def extract_base_layers(safe_text: str, source_url: str) -> Dict[str, Any]:
    merged = _merge(
        extract_html(safe_text),
        extract_markdown(safe_text),
        {"code": extract_code_features(safe_text)},
        {"dependencies": extract_dependencies(safe_text)},
        {"relationships": extract_architecture(safe_text)},
        {"content": extract_repository_data(safe_text, source_url=source_url)},
        {"metadata": extract_metadata(safe_text, source_url=source_url)},
        extract_repository_intelligence(safe_text, source_url=source_url),
        {"content": {"repository_v2": extract_repository_v2(safe_text)}},
        {"content": {"api_surface_v2": extract_api_v2(safe_text)}},
        {"dependencies": {"graph_v2": extract_dependencies_v2(safe_text)}},
        {"content": {"docs_v2": extract_docs_v2(safe_text)}},
        {"relationships": {"architecture_v2": extract_architecture_v2(safe_text, source_url=source_url)}},
        {"content": {"repository_intelligence_v12": analyze_repository(safe_text, source_url=source_url)}},
        {"content": {"document_intelligence_v12": analyze_document(safe_text)}},
    )
    return merged


__all__ = ["extract_base_layers", "_merge"]

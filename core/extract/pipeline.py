from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Union

from core.extract.architecture_extractor import extract_architecture
from core.extract.code_extractor import extract_code_features
from core.extract.dependency_extractor import extract_dependencies
from core.extract.enrichment_engine import _merge, enrich_extraction
from core.extract.html_extractor import extract_html
from core.extract.markdown_extractor import extract_markdown
from core.extract.metadata_extractor import extract_metadata
from core.extract.repository_extractor import extract_repository_data
from core.extract.repository_intelligence import extract_repository_intelligence
from core.extract.advanced.repository_extractor_v2 import extract_repository_v2
from core.extract.advanced.api_extractor import extract_api_v2
from core.extract.advanced.dependency_extractor_v2 import extract_dependencies_v2
from core.extract.advanced.docs_extractor_v2 import extract_docs_v2
from core.extract.advanced.architecture_extractor_v2 import extract_architecture_v2
from core.fetch.http_fetcher import fetch_async, fetch_sync
from core.fetch.raw_fetcher import fetch_raw
from core.llm.groq_adapter import complete as groq_complete
from core.llm.sandbox import isolate_llm
from core.normalize.normalize_output import normalize_output
from core.security.payload_limits import MAX_HTML_SIZE, enforce_text_limit
from core.security.safe_parser import safe_html_text
from core.security.url_validator import is_safe_url
from core.security.hardening import sandbox_text
from core.documents.document_intelligence import analyze_document
from core.repository.repository_intelligence import analyze_repository


def _is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def _extract_core(text: str, source_url: str) -> Dict[str, Any]:
    safe_text = sandbox_text(enforce_text_limit(text or "", MAX_HTML_SIZE))
    html_text = safe_html_text(safe_text)
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
    merged["raw_text"] = html_text or safe_text
    merged["source_url"] = source_url
    normalized = normalize_output(merged, source_url=source_url)
    return enrich_extraction(normalized, safe_text, source_url, merged)


def extract(input_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    cfg = input_data if isinstance(input_data, dict) else {"source": input_data}
    source = str(cfg.get("source", "") or "")
    llm = str(cfg.get("llm", "") or "").lower()
    if _is_url(source):
        if not is_safe_url(source):
            core = _extract_core("", source_url=source)
            core["metadata"]["fetch"] = {"status_code": 0, "content_type": "text/plain", "ok": False, "error": "unsafe_url"}
            return core
        fetched = fetch_sync(source)
    else:
        fetched = fetch_raw(source, source_url="")
    core = _extract_core(str(fetched.get("text", "") or ""), source_url=source if _is_url(source) else "")
    core["metadata"]["fetch"] = {k: fetched.get(k) for k in ("status_code", "content_type", "ok", "error")}
    if llm == "groq":
        llm_result = groq_complete(prompt=core["raw_text"][:4000], task="extraction enhancement")
        isolated = isolate_llm(core, llm_result)
        core["metadata"]["llm"] = deepcopy(isolated["llm"])
    return core


async def extract_async(input_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    cfg = input_data if isinstance(input_data, dict) else {"source": input_data}
    source = str(cfg.get("source", "") or "")
    llm = str(cfg.get("llm", "") or "").lower()
    if _is_url(source):
        if not is_safe_url(source):
            core = _extract_core("", source_url=source)
            core["metadata"]["fetch"] = {"status_code": 0, "content_type": "text/plain", "ok": False, "error": "unsafe_url"}
            return core
        fetched = await fetch_async(source)
    else:
        fetched = fetch_raw(source, source_url="")
    core = _extract_core(str(fetched.get("text", "") or ""), source_url=source if _is_url(source) else "")
    core["metadata"]["fetch"] = {k: fetched.get(k) for k in ("status_code", "content_type", "ok", "error")}
    if llm == "groq":
        llm_result = groq_complete(prompt=core["raw_text"][:4000], task="extraction enhancement")
        isolated = isolate_llm(core, llm_result)
        core["metadata"]["llm"] = deepcopy(isolated["llm"])
    return core


def extract_docs(source: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    return extract(source)


def extract_repo(source: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    return extract(source)

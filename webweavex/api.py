"""
WebWeaveX - Universal Extraction Library
Deterministic, context-driven extraction system
"""

from concurrent.futures import ThreadPoolExecutor

from core.extractor_engine import ExtractionEngine
from core.extractor_registry import register_extractor, get_extractors
from core.intelligent_extraction import build_intelligence
from core.knowledge_graph import extract_and_add_entities, extract_and_add_relations
from core.ai_adapter import get_ai_adapter
from core.fetcher import fetch_url
from core.context_schema import init_context
from extractors.generic_html_extractor import GenericHTMLExtractor
from extractors.github_extractor import GitHubExtractor
from extractors.stackoverflow_extractor import StackOverflowExtractor


CONFIG = {
    "ai_mode": "off",
    "intelligence": True,
    "max_depth": 1,
    "max_links_per_page": 5,
    "deterministic_mode": True,
    "mode": "balanced",
    "use_headless": False,
    "fail_safe": True,
}


register_extractor("stackoverflow", StackOverflowExtractor)
register_extractor("github", GitHubExtractor)
register_extractor("generic", GenericHTMLExtractor)


def _create_extraction_engine():
    engine = ExtractionEngine()
    for extractor in get_extractors():
        engine.register(extractor)
    return engine


_extraction_engine = _create_extraction_engine()


def _get_html_from_input(url, html, options, context):
    if html:
        return html

    if not url and options:
        itype = options.get("input_type")
        if itype == "text":
            return f"<html><body><pre>{options.get('text', '')}</pre></body></html>"
        if itype == "json":
            return f"<html><body><pre>{options.get('json', {})}</pre></body></html>"
        if itype == "markdown":
            return f"<html><body><pre>{options.get('markdown', '')}</pre></body></html>"
        if itype == "code":
            return f"<html><body><code>{options.get('code', '')}</code></body></html>"
        return None

    if url:
        return fetch_url(url, context)

    return None


def _fallback_extract_text(html_content):
    """Extract text from HTML as fallback."""
    import re
    if not html_content:
        return ""
    
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def _should_process_intelligence(cfg):
    mode = cfg.get("mode", "balanced")
    if mode == "fast":
        return False
    if mode == "balanced":
        return cfg.get("intelligence", True)
    return True


def _should_process_knowledge(cfg):
    return cfg.get("mode", "balanced") != "fast"


def extract(url=None, html=None, options=None, context=None):
    """Safe extract - auto-creates context if not provided."""
    if context is None:
        from core.memory_context import MemoryContext
        context = MemoryContext()
    
    return _extract_strict(url=url, html=html, options=options, context=context)


def _extract_strict(url=None, html=None, options=None, *, context):
    """Strict extract - context is required (keyword-only)."""
    if context is None:
        raise ValueError("context is required")

    init_context(context)

    cfg = {**CONFIG, **(options or {})}
    context["meta"]["deterministic_mode"] = cfg.get("deterministic_mode", True)

    result = {"content": {}, "intelligence": {}, "knowledge": {}, "ai": {}, "meta": {}}

    html_content = _get_html_from_input(url, html, options, context)
    if not html_content:
        return result

    extraction = _extraction_engine.extract(url or "", html_content, {})
    content_data = extraction.get("content") or {}
    
    extracted_text = content_data.get("text", "")
    if not extracted_text:
        extracted_text = _fallback_extract_text(html_content)
    content_data["text"] = extracted_text
    
    result["content"] = content_data

    if _should_process_intelligence(cfg):
        result["intelligence"] = build_intelligence(content_data, context) or {}

    if _should_process_knowledge(cfg):
        text_for_kg = content_data.get("text", "") or ""
        entities = extract_and_add_entities(text_for_kg, context=context) or []
        relations = extract_and_add_relations(text_for_kg, max_relations=10, context=context) or []
        result["knowledge"] = {"entities": entities, "relations": relations}
    else:
        result["knowledge"] = {"entities": [], "relations": []}

    if cfg.get("mode") == "ai":
        adapter = get_ai_adapter(cfg.get("ai_mode"))
        result["ai"] = adapter.process(content_data) or {"mode": "disabled", "result": None}
    else:
        result["ai"] = {"mode": "disabled", "result": None}

    itype = options.get("input_type") if options else None
    source_type = "url" if url else (itype if itype else "html")

    result["meta"] = {
        "url": url,
        "mode": cfg.get("mode"),
        "ai_mode": cfg.get("ai_mode"),
        "intelligence_enabled": _should_process_intelligence(cfg),
        "source_type": source_type,
    }

    kg = context.get("knowledge", {})
    kg_entities = kg.get("entities", []) if kg else []
    kg_graph = kg.get("graph", {}) if kg else {}
    result["knowledge_graph"] = {
        "nodes": len(kg_entities),
        "edges": len(kg_graph),
    }

    result = {
        "content": result.get("content") or {"text": "", "code": [], "structured": {}},
        "intelligence": result.get("intelligence") or {},
        "knowledge": result.get("knowledge") or {"entities": [], "relations": []},
        "ai": result.get("ai") or {"mode": "disabled", "result": None},
        "meta": result.get("meta") or {},
        "knowledge_graph": result.get("knowledge_graph") or {"nodes": 0, "edges": 0},
    }

    return result


def extract_batch(urls, options=None):
    return [extract(url=url, options=options) for url in urls]


def extract_with_context(url=None, html=None, options=None, *, context):
    """Explicit extract - context required (keyword-only)."""
    return _extract_strict(url=url, html=html, options=options, context=context)


def extract_batch_with_context(urls, options=None, *, context):
    """Explicit batch extract - context required."""
    return [_extract_strict(url=url, options=options, context=context) for url in urls]


def extract_batch_parallel(urls, options=None, max_workers=5):
    from core.memory_context import MemoryContext
    
    def worker(url):
        ctx = MemoryContext()
        return _extract_strict(url=url, options=options, context=ctx)
    
    results = [None] * len(urls)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, url) for url in urls]
        for i, future in enumerate(futures):
            results[i] = future.result()
    return results


def extract_batch_parallel_with_context(urls, options=None, *, context, max_workers=5):
    """Explicit parallel extract - context must be provided and used."""
    if context is None:
        raise ValueError("context is required")
    
    import copy
    from core.memory_context import MemoryContext
    
    def worker(url):
        ctx = MemoryContext()
        
        base = context.get_all() if hasattr(context, "get_all") else dict(context)
        ctx_data = copy.deepcopy(base)
        
        for k, v in ctx_data.items():
            ctx[k] = v
        
        return _extract_strict(url=url, options=options, context=ctx)
    
    results = [None] * len(urls)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, url) for url in urls]
        for i, future in enumerate(futures):
            results[i] = future.result()
    return results


def get_config():
    return CONFIG.copy()


def set_config(key, value):
    CONFIG[key] = value


def register_custom_extractor(name, extractor_cls):
    register_extractor(name, extractor_cls)

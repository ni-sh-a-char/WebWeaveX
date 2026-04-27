"""
WebWeaveX - Universal Extraction Library
Deterministic, context-driven extraction system with AI integration
"""

from concurrent.futures import ThreadPoolExecutor

from core.extractor_engine import ExtractionEngine
from core.extractor_registry import register_extractor, get_extractors
from core.intelligent_extraction import build_intelligence
from core.knowledge_graph import extract_and_add_entities, extract_and_add_relations
from core.ai_adapter import get_ai_adapter
from core.ai_provider import create_provider, AIProvider
from core.security import secure_store, secure_get, encrypt_dict, decrypt_dict
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
    "ai": {
        "enabled": False,
        "provider": None,
        "model": None,
    }
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


def _setup_ai_context(context, cfg):
    """Setup AI in context from options. Uses encrypted storage."""
    ai_config = cfg.get("ai", {})
    
    if not ai_config:
        context["ai"] = {"enabled": False, "provider": None, "model": None}
        return
    
    from core.security import validate_ai_config, secure_store, secure_get
    is_valid, error = validate_ai_config(ai_config)
    
    if not is_valid:
        context["ai"] = {"enabled": False, "provider": None, "model": None, "error": error}
        return
    
    provider_type = ai_config.get("provider")
    api_key = ai_config.get("api_key")
    endpoint = ai_config.get("endpoint")
    
    secure_store(context, f"api_key_{provider_type}", api_key)
    decrypted_key = secure_get(context, f"api_key_{provider_type}")
    
    provider_config = {
        "api_key": decrypted_key,
        "model": ai_config.get("model"),
        "endpoint": endpoint,
    }
    
    provider = create_provider(provider_type, provider_config)
    
    context["ai"] = {
        "enabled": True,
        "provider": provider,
        "model": ai_config.get("model"),
        "provider_type": provider_type,
    }


def run_ai_pipeline(text, context, cfg):
    """Centralized AI execution - MUST NOT break pipeline."""
    ai_data = context.get("ai", {})
    provider = ai_data.get("provider")
    
    if not provider:
        raise RuntimeError("AI provider not configured")
    
    result = {"mode": ai_data.get("provider_type", "unknown"), "result": {}}
    
    try:
        if hasattr(provider, "summarize"):
            summary = provider.summarize(text, {"goal": cfg.get("goal", "")})
            if not isinstance(summary, str) or len(summary) <= 50:
                raise RuntimeError(f"Summary invalid: len={len(summary) if isinstance(summary, str) else 'not string'}")
            result["result"]["summary"] = summary[:500]
    except Exception as e:
        raise RuntimeError(f"AI summarize failed: {e}")
    
    try:
        if hasattr(provider, "extract_entities"):
            entities = provider.extract_entities(text)
            if not isinstance(entities, list) or len(entities) < 2:
                raise RuntimeError(f"Entities invalid: count={len(entities) if isinstance(entities, list) else 'not list'}")
            result["result"]["entities"] = entities
    except Exception as e:
        raise RuntimeError(f"AI entity extraction failed: {e}")
    
    try:
        if hasattr(provider, "score"):
            score = provider.score(text, cfg.get("goal", ""))
            if not isinstance(score, (int, float)) or score < 0.0 or score > 1.0:
                raise RuntimeError(f"Score invalid: {score}")
            result["result"]["score"] = score
    except RuntimeError as e:
        if "429" in str(e):
            raise RuntimeError("AI rate limit: score unavailable")
        raise
    
    required_keys = ["summary", "entities", "score"]
    for k in required_keys:
        if k not in result["result"]:
            raise RuntimeError(f"AI pipeline incomplete: missing {k}")
    
    return result


def _finalize_result(result, cfg, context, url, html, options):
    """Finalize and return result."""
    content_data = result.get("content") or {}
    
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
    total_edges = sum(len(rels) for rels in kg_graph.values())
    result["knowledge_graph"] = {
        "nodes": len(kg_entities),
        "edges": total_edges,
    }

    result = {
        "content": result.get("content") or {"text": "", "code": [], "structured": {}},
        "intelligence": result.get("intelligence") or {},
        "knowledge": result.get("knowledge") or {"entities": [], "relations": []},
        "ai": result.get("ai") or {"mode": "disabled", "result": None},
        "meta": result.get("meta") or {},
        "knowledge_graph": result.get("knowledge_graph") or {"nodes": 0, "edges": 0},
    }
    
    result["meta"]["signature"] = {
        "powered_by": "WebWeaveX",
        "creator": "Piyush Mishra",
        "github": "PIYUSH-MISHRA-00"
    }
    
    return result


def extract(url=None, html=None, options=None, context=None):
    """Safe extract - auto-creates context if not provided."""
    try:
        if context is None:
            from core.memory_context import MemoryContext
            context = MemoryContext()
        
        return _extract_strict(url=url, html=html, options=options, context=context)
    except Exception as e:
        return {
            "content": {"text": "", "code": [], "structured": {}},
            "intelligence": {},
            "knowledge": {"entities": [], "relations": []},
            "ai": {"mode": "disabled", "result": {"ai_error": str(e)}},
            "meta": {"error": str(e)},
            "knowledge_graph": {"nodes": 0, "edges": 0},
        }


def _extract_strict(url=None, html=None, options=None, *, context):
    """Strict extract - context is required (keyword-only)."""
    if context is None:
        raise ValueError("context is required")

    init_context(context)

    cfg = {**CONFIG, **(options or {})}
    context["meta"]["deterministic_mode"] = cfg.get("deterministic_mode", True)

    _setup_ai_context(context, cfg)

    result = {"content": {}, "intelligence": {}, "knowledge": {}, "ai": {}, "meta": {}}

    is_deterministic = cfg.get("deterministic_mode", True)
    ai_config = cfg.get("ai", {})
    can_use_ai = (
        not is_deterministic and 
        ai_config.get("enabled", False) and 
        ai_config.get("provider") and 
        ai_config.get("api_key")
    )
    
    if can_use_ai and context.get("ai", {}).get("provider"):
        ai = context["ai"]["provider"]
        if hasattr(ai, "is_available") and not ai.is_available():
            can_use_ai = False

    if is_deterministic:
        result["ai"] = {"mode": "disabled", "result": None}

    html_content = _get_html_from_input(url, html, options, context)
    if not html_content:
        return _finalize_result(result, cfg, context, url, html, options)

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
    
    if can_use_ai and context.get("ai", {}).get("provider"):
        if not extracted_text or len(extracted_text.strip()) < 50:
            raise RuntimeError("AI skipped: insufficient text")
        try:
            result["ai"] = run_ai_pipeline(extracted_text, context, cfg)
        except Exception as e:
            raise RuntimeError(f"AI pipeline failed: {e}")
    elif not result.get("ai"):
        result["ai"] = {"mode": "disabled", "result": None}

    return _finalize_result(result, cfg, context, url, html, options)


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

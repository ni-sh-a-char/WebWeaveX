"""
WebWeaveX Core (PRIVATE INTERNAL MODULE)

This module is for internal use only.
All public APIs are exposed through webweavex package.
"""

from .intent_engine import resolve_intent
from .source_orchestrator import build_source_plan
from .query_builder import build_queries
from .fetch_engine import fetch_all
from .extraction_engine import extract_content
from .adaptive_engine import adaptive_extract
from .ranking_engine import rank_results
from .execution_engine import execute_result
from .output_engine import build_output
from .cache_engine import (
    generate_cache_key,
    load_cache,
    save_cache,
    clear_cache,
    generate_cache_signature,
    should_cache,
    validate_cache_engine,
)
from .full_pipeline import run_pipeline
from .code_reconstruction import reconstruct_project, is_code_expected
from .version import ENGINE_VERSION, VERSION_INFO

__all__ = [
    "resolve_intent",
    "build_source_plan",
    "build_queries",
    "fetch_all",
    "extract_content",
    "adaptive_extract",
    "rank_results",
    "execute_result",
    "build_output",
    "generate_cache_key",
    "load_cache",
    "save_cache",
    "clear_cache",
    "generate_cache_signature",
    "should_cache",
    "validate_cache_engine",
    "run_pipeline",
    "reconstruct_project",
    "is_code_expected",
    "ENGINE_VERSION",
    "VERSION_INFO",
]
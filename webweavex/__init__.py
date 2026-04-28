"""
WebWeaveX - Universal Extraction Library
"""

from .api import (
    extract,
    extract_batch,
    extract_batch_parallel,
    extract_with_context,
    extract_batch_with_context,
    extract_batch_parallel_with_context,
    get_config,
    set_config,
    CONFIG,
    register_custom_extractor,
)

__version__ = "1.0.2"
__all__ = [
    "extract",
    "extract_batch",
    "extract_batch_parallel",
    "extract_with_context",
    "extract_batch_with_context",
    "extract_batch_parallel_with_context",
    "get_config",
    "set_config",
    "CONFIG",
    "register_custom_extractor",
]
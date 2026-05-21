from core.adaptive.adaptive_runtime_orchestrator import run_adaptive_extraction
from core.adaptive.dom_similarity_engine import compute_dom_similarity
from core.adaptive.extraction_memory_engine import (
    load_adaptive_memory,
    remember_extraction_runtime,
    restore_extraction_runtime,
    save_adaptive_memory,
)
from core.adaptive.modal_recovery_engine import recover_modal_runtime
from core.adaptive.pagination_recovery_engine import recover_pagination_flow
from core.adaptive.schema_stability_engine import stabilize_extraction_schema
from core.adaptive.selector_healing_engine import heal_selector

__all__ = [
    "heal_selector",
    "compute_dom_similarity",
    "recover_modal_runtime",
    "recover_pagination_flow",
    "stabilize_extraction_schema",
    "remember_extraction_runtime",
    "restore_extraction_runtime",
    "save_adaptive_memory",
    "load_adaptive_memory",
    "run_adaptive_extraction",
]

"""
Persistence is intentionally disabled for Phase 4B deterministic execution.
"""


def persistence_disabled(*args, **kwargs):
    raise RuntimeError("Persistent global memory is disabled in context-only mode")

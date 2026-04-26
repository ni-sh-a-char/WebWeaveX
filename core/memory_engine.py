"""
Legacy module kept as a compatibility placeholder.
WebWeaveX Phase 4B runs exclusively on injected MemoryContext state.
"""


def context_snapshot(context):
    return context.get_all() if hasattr(context, "get_all") else dict(context)

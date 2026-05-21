from core.security.remote_target import is_safe_remote_target
from core.security.resource_budget import enforce_resource_budget
from core.security.hardening import (
    decompression_guard,
    malformed_payload_guard,
    memory_guard,
    recursion_guard,
    redirect_guard,
    sandbox_text,
    ssrf_guard,
    timeout_guard,
)
from core.performance import budgeted_chunks, incremental_parse, lazy_extract, memory_budget, parser_pool, stream_parse

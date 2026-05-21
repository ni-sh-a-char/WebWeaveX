from __future__ import annotations

from typing import Any, Dict, List

from core.repository.runtime_event_engine import infer_runtime_events
from core.repository.infra_execution_engine import infer_infra_execution


def compile_runtime_semantic_ir(
    dependencies: List[str],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    events = infer_runtime_events(dependencies, parser_evidence)
    infra = infer_infra_execution(dependencies, parser_evidence)
    return {
        "events": events,
        "infra": infra,
        "dependencies": sorted(dependencies),
        "deterministic": True,
    }

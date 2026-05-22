from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional

from core.contracts.extraction_contracts import ExtractionResult
from core.contracts.graph_contracts import RuntimeGraphContract
from core.contracts.runtime_contracts import RuntimePhase, UniversalInput
from core.ingestion.universal_ingestion_engine import ingest_input
from core.kernel.runtime_kernel import RuntimeKernel
from core.runtime_graph.runtime_graph_engine import build_runtime_graph


def _hash_payload(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _detect_kind(inp: UniversalInput) -> str:
    if inp.source_type != "auto":
        return inp.source_type
    src = inp.source or inp.url or inp.path
    if src.startswith("http://") or src.startswith("https://"):
        return "web"
    if any(src.endswith(ext) for ext in (".pdf", ".docx", ".md", ".html", ".txt")):
        return "document"
    from pathlib import Path

    if Path(src).exists() and Path(src).is_dir():
        return "repository"
    if Path(src).exists():
        return "multimodal"
    return "text"


def run_canonical_pipeline(
    inp: UniversalInput,
    *,
    phases: Optional[List[str]] = None,
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Single canonical extraction path:

    UniversalInput → ingestion → runtime phases → unified graph
    """
    options = options or {}
    kind = _detect_kind(inp)
    target = inp.url or inp.path or inp.source

    if kind == "web" or target.startswith("http"):
        ingested = {
            "path": target,
            "type": "web",
            "input_type": "url",
            "supported": True,
            "bounded": True,
        }
    else:
        ingested = ingest_input(target)

    extraction_payload: Dict[str, Any] = {"ingestion": ingested, "bounded": True}

    if kind == "web":
        from core.browser.universal_web_extraction_engine import extract_web

        extraction_payload = extract_web(
            target,
            session=inp.session,
            authenticated=bool(options.get("authenticated")),
            session_path=str(options.get("session_path", "")),
            encryption_key=str(options.get("encryption_key", "")),
            stream_runtime=bool(options.get("stream_runtime")),
            federated_memory=bool(options.get("federated_memory")),
            execution_runtime=bool(options.get("execution_runtime")),
            reconstruction_runtime=bool(options.get("reconstruction_runtime")),
            semantic_runtime=bool(options.get("semantic_runtime")),
            synchronized_runtime=bool(options.get("synchronized_runtime")),
            autonomous_workflow=bool(options.get("autonomous_workflow")),
        )
    elif kind == "repository":
        from core.repository.universal_repository_extraction_engine import (
            extract_repository,
        )

        extraction_payload = extract_repository(target)
    elif kind == "document":
        from core.documents.universal_document_extraction_engine import (
            extract_document_runtime,
        )
        from pathlib import Path

        text = Path(target).read_text(encoding="utf-8", errors="replace")
        extraction_payload = extract_document_runtime(text)
    elif kind == "multimodal":
        from core.multimodal.universal_multimodal_extraction_engine import (
            extract_multimodal,
        )

        extraction_payload = extract_multimodal(target)
    else:
        from core.extract.pipeline import extract

        extraction_payload = extract({"source": target})

    runtime_type = "browser" if kind == "web" else kind
    kernel = RuntimeKernel(runtime_type=runtime_type)
    phase_out = kernel.run_pipeline(
        sources={"extraction": extraction_payload, "ingestion": ingested},
        tick=inp.tick,
        phases=phases,
        options=options.get("kernel", {}),
    )

    graph_src = extraction_payload.get("unified_runtime_graph")
    if not graph_src:
        irs: List[Dict[str, Any]] = []
        for key in ("browser_ir", "repository_ir", "document_ir", "multimodal_ir"):
            if key in extraction_payload:
                irs.append(extraction_payload[key])
        graph_src = build_runtime_graph(irs) if irs else phase_out.get("graph", {})

    graph = RuntimeGraphContract.normalize(graph_src or {})
    result = ExtractionResult(
        kind=kind,
        payload=extraction_payload,
        graph_nodes=graph.get("nodes", []),
        graph_edges=graph.get("edges", []),
        deterministic_hash=_hash_payload(
            {"kind": kind, "nodes": graph.get("nodes"), "edges": graph.get("edges")}
        ),
    )

    return {
        "input": inp.to_dict(),
        "kind": kind,
        "phases_run": [p.value for p in RuntimePhase],
        "ingestion": ingested,
        "extraction": extraction_payload,
        "kernel": phase_out,
        "unified_runtime_graph": graph,
        "result": result.to_dict(),
        "pipeline_hash": result.deterministic_hash,
        "bounded": True,
    }

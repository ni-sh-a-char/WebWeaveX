from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.semantic_runtime_ir import (
    compile_semantic_runtime_ir,
    semantic_runtime_ir_to_graph,
)
from core.semantic.application_semantics_engine import extract_application_semantics
from core.semantic.browser_semantics_engine import extract_browser_semantics
from core.semantic.causality_semantics_engine import extract_causality_semantics
from core.semantic.document_semantics_engine import extract_document_semantics
from core.semantic.domain_classification_engine import classify_semantic_domain
from core.semantic.entity_extraction_engine import extract_semantic_entities
from core.semantic.entity_resolution_engine import resolve_semantic_entities
from core.semantic.ontology_engine import build_semantic_ontology
from core.semantic.repository_semantics_engine import extract_repository_semantics
from core.semantic.runtime_semantics_engine import extract_runtime_semantics
from core.semantic.semantic_alignment_engine import align_semantic_runtimes
from core.semantic.semantic_diff_engine import diff_semantic_runtime
from core.semantic.semantic_graph_engine import build_semantic_graph
from core.semantic.semantic_memory_engine import load_semantic_memory
from core.semantic.semantic_memory_engine import remember_semantic_runtime
from core.semantic.semantic_memory_engine import save_semantic_memory
from core.semantic.semantic_replay_engine import replay_semantic_runtime
from core.semantic.table_semantics_engine import extract_table_semantics
from core.semantic.ui_semantics_engine import extract_ui_semantics
from core.semantic.workflow_semantics_engine import extract_workflow_semantics


def run_semantic_runtime(
    url: str = "",
    html: str = "",
    text: str = "",
    interactions: Optional[List[Dict[str, Any]]] = None,
    application_result: Optional[Dict[str, Any]] = None,
    causality_result: Optional[Dict[str, Any]] = None,
    native_cognition: Optional[Dict[str, Any]] = None,
    repository_files: Optional[List[str]] = None,
    runtime_graph: Optional[Dict[str, Any]] = None,
    memory: Optional[Dict[str, Any]] = None,
    objective: str = "",
) -> Dict[str, Any]:
    memory = dict(memory or {})
    interactions = list(interactions or [])
    combined_text = f"{text} {html}"[:100000]

    structure = {
        "actions": [
            {"label": ix.get("action", ""), "type": ix.get("action", "")}
            for ix in interactions
        ],
        "artifacts": [
            str(native_cognition.get("runtime", ""))
        ] if native_cognition else [],
    }

    entities_raw = extract_semantic_entities(combined_text, structure)
    resolved = resolve_semantic_entities(entities_raw["entities"])
    entities_raw["entities"] = resolved["entities"]

    domain = classify_semantic_domain(
        combined_text,
        signals=[objective] if objective else [],
    )
    ontology = build_semantic_ontology(entities_raw["entities"], domain["domain"])
    entities_raw["ontology"] = ontology

    ui = extract_ui_semantics(html, interactions)
    tables = extract_table_semantics(html)
    document = extract_document_semantics(combined_text)
    repository = extract_repository_semantics(repository_files, combined_text)
    application = extract_application_semantics(application_result)
    causality = extract_causality_semantics(causality_result)
    workflow = extract_workflow_semantics(
        (application_result or {}).get("workflow"),
        objective,
    )
    browser = extract_browser_semantics(url, html)
    runtime = extract_runtime_semantics(
        runtime_graph,
        {
            "browser": bool(browser),
            "native": bool(native_cognition),
            "application": bool(application_result),
        },
    )

    semantic_graph = build_semantic_graph(
        entities_raw["entities"],
        entities_raw["relations"],
    )

    alignment = align_semantic_runtimes(
        browser={**browser, "domain": domain["domain"]},
        native=native_cognition,
        repository=repository,
        document=document,
        runtime=runtime,
    )

    diff = {}
    if memory.get("entities"):
        diff = diff_semantic_runtime(memory, {"entities": entities_raw, "domain": domain, "ontology": ontology, "workflow": workflow})

    payload = {
        "entities": entities_raw,
        "domain": domain,
        "ontology": ontology,
        "ui": ui,
        "tables": tables,
        "document": document,
        "repository": repository,
        "application": application,
        "causality": causality,
        "workflow": workflow,
        "browser": browser,
        "runtime": runtime,
        "semantic_graph": semantic_graph,
        "alignment": alignment,
        "diff": diff,
        "bounded": True,
    }

    updated_memory = remember_semantic_runtime(
        memory,
        {
            "ontology": ontology,
            "semantic_graph": semantic_graph,
            "entity_mappings": resolved.get("canonical_map", {}),
            "semantic_workflows": workflow,
            "runtime_semantics": runtime,
            "entities": entities_raw,
            "domain": domain,
        },
    )
    payload["memory"] = updated_memory
    payload["replay"] = replay_semantic_runtime(updated_memory)
    payload["semantic_ir"] = compile_semantic_runtime_ir(payload)
    return payload


def run_semantic_for_extraction(
    semantic_runtime: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    url: str = "",
    html: str = "",
    interactions: Optional[List[Dict[str, Any]]] = None,
    application_result: Optional[Dict[str, Any]] = None,
    causality_result: Optional[Dict[str, Any]] = None,
    native_cognition: Optional[Dict[str, Any]] = None,
    runtime_graph: Optional[Dict[str, Any]] = None,
    objective: str = "",
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not semantic_runtime:
        return {"enabled": False, "bounded": True}

    memory: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_semantic_memory(memory_path, memory_key)
        if loaded.get("available"):
            memory = loaded.get("memory", memory)

    result = run_semantic_runtime(
        url=url,
        html=html,
        interactions=interactions,
        application_result=application_result,
        causality_result=causality_result,
        native_cognition=native_cognition,
        runtime_graph=runtime_graph,
        memory=memory,
        objective=objective,
    )

    persisted = False
    if memory_path and memory_key:
        save_semantic_memory(memory_path, result.get("memory", {}), memory_key)
        persisted = True

    graph_ir = semantic_runtime_ir_to_graph(result.get("semantic_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "semantic": result,
        "semantic_ir": result.get("semantic_ir", {}),
        "semantic_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "memory_persisted": persisted,
        "bounded": True,
    }

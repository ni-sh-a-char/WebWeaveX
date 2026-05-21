from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.causality.browser_native_bridge_engine import bridge_browser_native_runtime
from core.causality.causal_graph_engine import build_causal_graph
from core.causality.causal_memory_engine import load_causal_memory
from core.causality.causal_memory_engine import remember_causal_runtime
from core.causality.causal_memory_engine import save_causal_memory
from core.causality.causal_recovery_engine import recover_causal_runtime
from core.causality.causal_replay_engine import replay_causal_runtime
from core.causality.cross_runtime_alignment_engine import align_cross_runtime_events
from core.causality.distributed_causality_engine import build_distributed_causality
from core.causality.electron_terminal_bridge_engine import bridge_electron_terminal_runtime
from core.causality.event_chain_engine import build_event_chain
from core.causality.notification_causality_engine import track_notification_causality
from core.causality.process_causality_engine import track_process_causality
from core.causality.runtime_causality_engine import build_runtime_causality
from core.causality.runtime_correlation_engine import correlate_runtime_mutations
from core.causality.runtime_dependency_engine import build_runtime_dependencies
from core.causality.runtime_sequence_engine import build_runtime_sequence
from core.causality.runtime_timeline_engine import build_runtime_timeline
from core.causality.state_transition_engine import build_state_transitions
from core.causality.workflow_propagation_engine import build_workflow_propagation
from core.ir.causal_runtime_ir import (
    causal_runtime_ir_to_graph,
    compile_causal_runtime_ir,
)


def _normalize_interaction_events(
    interactions: List[Dict[str, Any]],
    runtime: str = "browser",
) -> List[Dict[str, Any]]:
    events = []
    for index, interaction in enumerate(interactions[:10000]):
        events.append({
            "id": f"{runtime}:evt:{index}",
            "runtime": runtime,
            "type": str(interaction.get("action", interaction.get("type", "mutation"))),
            "step": index,
            "source": str(interaction.get("from", interaction.get("selector", ""))),
            "target": str(interaction.get("to", "")),
            "state": str(interaction.get("state", "")),
        })
    return events


def _events_from_native_cognition(
    cognition: Dict[str, Any],
) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    step = 0

    for interaction in cognition.get("interactions", []):
        events.append({
            "id": f"native:evt:{step}",
            "runtime": cognition.get("runtime", "desktop"),
            "type": str(interaction.get("action", "interaction")),
            "step": step,
        })
        step += 1

    terminal = cognition.get("terminal", {})
    for line in terminal.get("output", [])[:1000]:
        events.append({
            "id": f"terminal:evt:{step}",
            "runtime": "terminal",
            "type": "log",
            "step": step,
            "state": line,
        })
        step += 1

    electron = cognition.get("electron", {})
    for route in electron.get("routes", []):
        events.append({
            "id": f"electron:evt:{step}",
            "runtime": "electron",
            "type": "route",
            "step": step,
            "state": route,
        })
        step += 1

    for notification in cognition.get("desktop", {}).get("notifications", []):
        events.append({
            "id": f"desktop:notif:{step}",
            "runtime": "desktop",
            "type": "notification",
            "step": step,
            "state": str(notification),
        })
        step += 1

    return events


def run_causality_runtime(
    browser_events: Optional[List[Dict[str, Any]]] = None,
    native_cognition: Optional[Dict[str, Any]] = None,
    application_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    memory: Optional[Dict[str, Any]] = None,
    interactions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    memory = dict(memory or {})
    browser_events = list(browser_events or _normalize_interaction_events(interactions or [], "browser"))

    native_events = _events_from_native_cognition(native_cognition or {})

    if application_result:
        for index, _ in enumerate(application_result.get("workflow", {}).get("nodes", [])[:100]):
            browser_events.append({
                "id": f"application:evt:{index}",
                "runtime": "application",
                "type": "workflow",
                "step": len(browser_events) + index,
            })

    all_events = browser_events + native_events
    all_events = sorted(all_events, key=lambda item: int(item.get("step", 0)))

    origins = {
        "browser": len(browser_events),
        "native": len(native_events),
        "distributed": bool(distributed_result),
    }

    causality = build_runtime_causality(all_events, origins)
    event_chain = build_event_chain(all_events)
    alignment = align_cross_runtime_events(all_events)
    dependencies = build_runtime_dependencies(all_events, {"synchronization_chains": []})
    propagation = build_workflow_propagation(alignment, dependencies)
    dependencies = build_runtime_dependencies(all_events, propagation)
    causal_graph = build_causal_graph(all_events, causality)
    transitions = build_state_transitions(all_events)
    sequence = build_runtime_sequence(all_events)
    timeline = build_runtime_timeline(all_events, propagation)
    correlation = correlate_runtime_mutations(
        browser_events=browser_events,
        native_events=native_events,
        notifications=(native_cognition or {}).get("desktop", {}).get("notifications", []),
        terminal_lines=(native_cognition or {}).get("terminal", {}).get("output", []),
        process_events=(native_cognition or {}).get("processes", {}).get("processes", []),
    )
    distributed = build_distributed_causality(distributed_result)
    browser_bridge = bridge_browser_native_runtime(browser_events, native_events)
    electron_events = [e for e in native_events if e.get("runtime") == "electron"]
    terminal_events = [e for e in native_events if e.get("runtime") == "terminal"]
    electron_bridge = bridge_electron_terminal_runtime(electron_events, terminal_events)
    notification_causality = track_notification_causality(
        (native_cognition or {}).get("desktop", {}).get("notifications", []),
        all_events,
    )
    process_causality = track_process_causality(
        (native_cognition or {}).get("processes", {}).get("processes", []),
        all_events,
    )
    recovery = recover_causal_runtime(causality, all_events)

    payload = {
        "causality": causality,
        "event_chain": event_chain,
        "alignment": alignment,
        "propagation": propagation,
        "dependencies": dependencies,
        "causal_graph": causal_graph,
        "transitions": transitions,
        "sequence": sequence,
        "timeline": timeline,
        "correlation": correlation,
        "distributed": distributed,
        "browser_bridge": browser_bridge,
        "electron_bridge": electron_bridge,
        "notification_causality": notification_causality,
        "process_causality": process_causality,
        "recovery": recovery,
        "bounded": True,
    }

    updated_memory = remember_causal_runtime(
        memory,
        {
            "event_chains": event_chain,
            "runtime_propagation": causality,
            "causal_graphs": causal_graph,
            "distributed_workflows": distributed,
            "synchronization_state": alignment,
            "alignment": alignment,
            "timeline": timeline,
        },
    )
    payload["memory"] = updated_memory
    payload["replay"] = replay_causal_runtime(updated_memory)
    payload["causal_ir"] = compile_causal_runtime_ir(payload)
    return payload


def run_causality_for_extraction(
    causality_runtime: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    browser_events: Optional[List[Dict[str, Any]]] = None,
    native_cognition: Optional[Dict[str, Any]] = None,
    application_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    interactions: Optional[List[Dict[str, Any]]] = None,
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not causality_runtime:
        return {"enabled": False, "bounded": True}

    memory: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_causal_memory(memory_path, memory_key)
        if loaded.get("available"):
            memory = loaded.get("memory", memory)

    result = run_causality_runtime(
        browser_events=browser_events,
        native_cognition=native_cognition,
        application_result=application_result,
        distributed_result=distributed_result,
        memory=memory,
        interactions=interactions,
    )

    persisted = False
    if memory_path and memory_key:
        save_causal_memory(memory_path, result.get("memory", {}), memory_key)
        persisted = True

    graph_ir = causal_runtime_ir_to_graph(result.get("causal_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "causality": result,
        "causal_ir": result.get("causal_ir", {}),
        "causal_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "memory_persisted": persisted,
        "bounded": True,
    }

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.application.application_cognition_orchestrator import (
    run_application_cognition,
)
from core.ir.native_runtime_ir import (
    compile_native_runtime_ir,
    native_runtime_ir_to_graph,
)
from core.native.accessibility_tree_engine import extract_accessibility_tree
from core.native.desktop_runtime_engine import build_desktop_runtime
from core.native.electron_runtime_engine import extract_electron_runtime
from core.native.native_focus_engine import resolve_native_focus
from core.native.native_interaction_engine import build_interaction_sequence
from core.native.native_memory_engine import load_native_runtime
from core.native.native_memory_engine import remember_native_runtime
from core.native.native_memory_engine import save_native_runtime
from core.native.native_navigation_engine import build_native_navigation
from core.native.native_process_engine import enumerate_native_processes
from core.native.native_remote_session_engine import extract_remote_runtime
from core.native.native_replay_engine import replay_native_runtime
from core.native.native_state_engine import build_native_state
from core.native.native_stream_engine import capture_native_streams
from core.native.native_terminal_engine import capture_terminal_runtime
from core.native.native_ui_graph_engine import build_native_ui_graph
from core.native.native_vm_engine import extract_vm_runtime
from core.native.native_window_engine import extract_native_windows
from core.native.native_runtime_alignment_engine import align_native_runtime
from core.runtime_graph.runtime_graph_engine import build_runtime_graph
from core.causality.causality_orchestrator import run_causality_for_extraction
from core.ir.causal_runtime_ir import causal_runtime_ir_to_graph
from core.semantic.semantic_orchestrator import run_semantic_for_extraction
from core.ir.semantic_runtime_ir import semantic_runtime_ir_to_graph
from core.workflows.workflow_orchestrator import run_workflow_for_extraction
from core.ir.workflow_runtime_ir import workflow_runtime_ir_to_graph
from core.synchronization.runtime_sync_orchestrator import run_sync_for_extraction
from core.ir.synchronization_runtime_ir import synchronization_runtime_ir_to_graph
from core.evolution_runtime.runtime_evolution_orchestrator import run_evolution_for_extraction
from core.ir.evolution_runtime_ir import evolution_runtime_ir_to_graph
from core.connectors.live_runtime_orchestrator import run_live_for_extraction
from core.ir.live_runtime_ir import live_runtime_ir_to_graph
from core.memory.runtime_memory_orchestrator import run_memory_for_extraction
from core.ir.runtime_memory_ir import runtime_memory_ir_to_graph
from core.execution.runtime_execution_orchestrator import run_execution_for_extraction
from core.ir.execution_runtime_ir import execution_runtime_ir_to_graph
from core.reconstruction.runtime_reconstruction_orchestrator import run_reconstruction_for_extraction
from core.ir.reconstruction_runtime_ir import reconstruction_runtime_ir_to_graph


def _fixture_for_application(application: str) -> Dict[str, Any]:
    app = application.lower()
    return {
        "windows": [
            {
                "id": f"win:{app}",
                "title": f"{app.title()} — Main",
                "application": app,
                "bounds": {"x": 0, "y": 0, "width": 1280, "height": 720},
                "visible": True,
                "z_order": 1,
                "focused": True,
            },
        ],
        "focused_window": f"{app.title()} — Main",
        "nodes": [
            {"id": "btn:login", "role": "button", "name": "Login"},
            {"id": "input:user", "role": "textbox", "name": "Username"},
            {"id": "dlg:settings", "role": "dialog", "name": "Settings"},
        ],
        "active_apps": [{"name": app}],
        "routes": ["/"],
        "output": ["$ echo hello", "hello"],
        "commands": ["echo hello"],
        "prompts": ["$"],
    }


def run_native_cognition(
    runtime: str = "desktop",
    application: str = "",
    snapshot: Optional[Dict[str, Any]] = None,
    memory: Optional[Dict[str, Any]] = None,
    interactions: Optional[List[Dict[str, Any]]] = None,
    application_cognition: bool = False,
    adaptive_runtime: Optional[Dict[str, Any]] = None,
    application_memory: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    memory = dict(memory or {})
    interactions = list(interactions or [])
    snap = dict(snapshot or _fixture_for_application(application or "desktop"))

    import sys

    platform_probe: Dict[str, Any] = {"bounded": True}
    if sys.platform == "win32":
        from core.native.platform.windows_uia_runtime import extract_windows_uia_snapshot

        platform_probe = extract_windows_uia_snapshot(snap)
    elif sys.platform == "darwin":
        from core.native.platform.macos_ax_runtime import extract_macos_ax_snapshot

        platform_probe = extract_macos_ax_snapshot(snap)
    elif sys.platform == "linux":
        from core.native.platform.linux_atspi_runtime import extract_linux_atspi_snapshot

        platform_probe = extract_linux_atspi_snapshot(snap)

    windows = extract_native_windows(snap)
    accessibility = extract_accessibility_tree(snap)
    desktop = build_desktop_runtime(windows, accessibility, snap)
    electron = extract_electron_runtime(application, snap)
    if runtime == "electron":
        from core.native.electron import (
            extract_electron_cdp,
            extract_electron_ipc,
            extract_electron_routes,
            extract_electron_storage,
        )

        from core.native.electron.electron_hash_engine import stable_electron_runtime_hash

        electron = {
            **electron,
            "cdp": extract_electron_cdp(target_url=f"electron://{application}"),
            "storage": extract_electron_storage(snap),
            "routes": extract_electron_routes(snap.get("routes")),
            "ipc": extract_electron_ipc(snap.get("ipc_channels")),
            "bounded": True,
        }
        electron["runtime_hash"] = stable_electron_runtime_hash(electron)
    terminal = capture_terminal_runtime(snapshot=snap)
    vm = extract_vm_runtime(snapshot=snap.get("vm"))
    remote = extract_remote_runtime(
        protocol=snap.get("remote_protocol", "ssh"),
        snapshot=snap.get("remote"),
    )
    processes = enumerate_native_processes(snap)
    focus = resolve_native_focus(windows, accessibility)
    navigation = build_native_navigation(desktop, electron)
    ui_graph = build_native_ui_graph(windows, accessibility, interactions)
    interaction_log = build_interaction_sequence(interactions)
    streams = capture_native_streams(terminal, desktop, electron)
    state = build_native_state(runtime, windows, desktop, focus.get("control"))

    app_cognition = {}
    if application_cognition and application:
        app_cognition = run_application_cognition(
            url=f"native://{application}",
            html="<html></html>",
            memory=application_memory,
            objective="extract_dashboard",
        )

    alignment = align_native_runtime(
        state,
        adaptive_runtime=adaptive_runtime,
        application_memory=application_memory or app_cognition.get("memory"),
    )

    updated_memory = remember_native_runtime(
        memory,
        {
            "windows": windows,
            "accessibility_trees": accessibility,
            "runtime_graphs": ui_graph,
            "electron_state": electron,
            "terminal_streams": terminal,
            "workflows": navigation,
            "interactions": interaction_log,
            "vm": vm,
            "remote": remote,
            "processes": processes,
            "streams": streams,
            "native_state": state,
        },
    )

    cognition_payload = {
        "runtime": runtime,
        "application": application,
        "platform_probe": platform_probe,
        "windows": windows,
        "accessibility": accessibility,
        "desktop": desktop,
        "electron": electron,
        "terminal": terminal,
        "vm": vm,
        "remote": remote,
        "processes": processes,
        "navigation": navigation,
        "ui_graph": ui_graph,
        "interactions": interaction_log,
        "streams": streams,
        "native_state": state,
        "application_cognition": app_cognition,
        "alignment": alignment,
        "memory": updated_memory,
        "bounded": True,
    }

    cognition_payload["native_ir"] = compile_native_runtime_ir(cognition_payload)
    return cognition_payload


def extract_native(
    runtime: str = "desktop",
    application: str = "discord",
    application_cognition: bool = True,
    persistent_runtime: bool = True,
    runtime_path: str = "native.enc",
    runtime_key: str = "master-key",
    snapshot: Optional[Dict[str, Any]] = None,
    interactions: Optional[List[Dict[str, Any]]] = None,
    adaptive_runtime: Optional[Dict[str, Any]] = None,
    application_memory: Optional[Dict[str, Any]] = None,
    merge_runtime_graph: bool = True,
    causality_runtime: bool = False,
    causal_memory_path: str = "",
    causal_memory_key: str = "",
    semantic_runtime: bool = False,
    semantic_memory_path: str = "",
    semantic_memory_key: str = "",
    autonomous_workflow: bool = False,
    workflow_memory_path: str = "",
    workflow_memory_key: str = "",
    workflow_objective: str = "capture_notifications",
    synchronized_runtime: bool = False,
    sync_memory_path: str = "",
    sync_memory_key: str = "",
    sync_tick: int = 0,
    evolving_runtime: bool = False,
    evolution_memory_path: str = "",
    evolution_memory_key: str = "",
    live_runtime: bool = False,
    live_memory_path: str = "",
    live_memory_key: str = "",
    live_snapshot: Optional[Dict[str, Any]] = None,
    federated_memory: bool = False,
    federated_memory_path: str = "",
    federated_memory_key: str = "",
    execution_runtime: bool = False,
    execution_memory_path: str = "",
    execution_memory_key: str = "",
    simulate_execution: bool = False,
    rollback_enabled: bool = True,
    reconstruction_runtime: bool = False,
    reconstruction_memory_path: str = "",
    reconstruction_memory_key: str = "",
    fabricate_runtime: bool = False,
    clone_runtime: bool = False,
) -> Dict[str, Any]:
    memory: Dict[str, Any] = {
        "accessibility_trees": {},
        "windows": {},
        "workflows": {},
        "runtime_graphs": {},
        "electron_state": {},
        "terminal_streams": {},
        "bounded": True,
    }

    if persistent_runtime and runtime_path and runtime_key:
        loaded = load_native_runtime(runtime_path, runtime_key)
        if loaded.get("available"):
            memory = loaded.get("runtime", memory)

    snap = snapshot
    terminal = None
    vm = None
    remote = None
    electron = None

    if runtime == "terminal":
        terminal = capture_terminal_runtime(snapshot=snap)
        cognition = run_native_cognition(
            runtime=runtime,
            application=application,
            snapshot=snap or {"output": ["$"], "commands": [], "prompts": ["$"]},
            memory=memory,
            interactions=interactions,
            application_cognition=application_cognition,
            adaptive_runtime=adaptive_runtime,
            application_memory=application_memory,
        )
    elif runtime == "electron":
        cognition = run_native_cognition(
            runtime=runtime,
            application=application,
            snapshot=snap,
            memory=memory,
            interactions=interactions,
            application_cognition=application_cognition,
            adaptive_runtime=adaptive_runtime,
            application_memory=application_memory,
        )
        electron = cognition.get("electron")
    elif runtime == "vm":
        vm = extract_vm_runtime(snapshot=snap)
        cognition = run_native_cognition(
            runtime=runtime,
            application=application,
            snapshot={"vm": snap or {}},
            memory=memory,
            interactions=interactions,
            application_cognition=application_cognition,
        )
    elif runtime == "remote":
        remote = extract_remote_runtime(
            protocol=(snap or {}).get("protocol", "ssh"),
            snapshot=snap,
        )
        cognition = run_native_cognition(
            runtime=runtime,
            application=application,
            snapshot={"remote": snap or {}, "remote_protocol": "ssh"},
            memory=memory,
            interactions=interactions,
            application_cognition=application_cognition,
        )
    else:
        cognition = run_native_cognition(
            runtime="desktop",
            application=application,
            snapshot=snap,
            memory=memory,
            interactions=interactions,
            application_cognition=application_cognition,
            adaptive_runtime=adaptive_runtime,
            application_memory=application_memory,
        )

    runtime_persisted = False
    if persistent_runtime and runtime_path and runtime_key:
        save_native_runtime(
            runtime_path,
            cognition.get("memory", {}),
            runtime_key,
        )
        runtime_persisted = True

    native_ir = cognition.get("native_ir", {})
    runtime_irs = [native_runtime_ir_to_graph(native_ir)]
    causality_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    causal_ir: Dict[str, Any] = {"ir": "causal_runtime", "bounded": True}
    causal_memory_persisted = False
    semantic_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    semantic_ir: Dict[str, Any] = {"ir": "semantic_runtime", "bounded": True}
    semantic_memory_persisted = False
    workflow_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    workflow_ir: Dict[str, Any] = {"ir": "workflow_runtime", "bounded": True}
    workflow_memory_persisted = False
    sync_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    sync_ir: Dict[str, Any] = {"ir": "synchronization_runtime", "bounded": True}
    sync_memory_persisted = False
    evolution_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    evolution_ir: Dict[str, Any] = {"ir": "evolution_runtime", "bounded": True}
    evolution_memory_persisted = False
    live_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    live_ir: Dict[str, Any] = {"ir": "live_runtime", "bounded": True}
    live_memory_persisted = False
    memory_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    memory_ir: Dict[str, Any] = {"ir": "runtime_memory", "bounded": True}
    federated_memory_persisted = False
    execution_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    execution_ir: Dict[str, Any] = {"ir": "execution_runtime", "bounded": True}
    execution_persisted = False
    reconstruction_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    reconstruction_ir: Dict[str, Any] = {"ir": "reconstruction_runtime", "bounded": True}
    reconstruction_persisted = False

    if causality_runtime:
        causality_result = run_causality_for_extraction(
            causality_runtime=True,
            memory_path=causal_memory_path,
            memory_key=causal_memory_key,
            native_cognition=cognition,
            interactions=interactions,
            merge_graph=False,
        )
        causal_ir = causality_result.get("causal_ir", causal_ir)
        causal_memory_persisted = causality_result.get("memory_persisted", False)
        runtime_irs.append(causal_runtime_ir_to_graph(causal_ir))

    if semantic_runtime:
        semantic_result = run_semantic_for_extraction(
            semantic_runtime=True,
            memory_path=semantic_memory_path,
            memory_key=semantic_memory_key,
            native_cognition=cognition,
            causality_result=causality_result,
            interactions=interactions,
            merge_graph=False,
        )
        semantic_ir = semantic_result.get("semantic_ir", semantic_ir)
        semantic_memory_persisted = semantic_result.get("memory_persisted", False)
        runtime_irs.append(semantic_runtime_ir_to_graph(semantic_ir))

    if autonomous_workflow:
        workflow_result = run_workflow_for_extraction(
            autonomous_workflow=True,
            objective=workflow_objective,
            memory_path=workflow_memory_path,
            memory_key=workflow_memory_key,
            native_cognition=cognition,
            semantic_runtime=semantic_result,
            causality_result=causality_result,
            merge_graph=False,
        )
        workflow_ir = workflow_result.get("workflow_ir", workflow_ir)
        workflow_memory_persisted = workflow_result.get("memory_persisted", False)
        runtime_irs.append(workflow_runtime_ir_to_graph(workflow_ir))

    if synchronized_runtime:
        sync_result = run_sync_for_extraction(
            synchronized_runtime=True,
            memory_path=sync_memory_path,
            memory_key=sync_memory_key,
            tick=sync_tick,
            native=cognition,
            semantic_result=semantic_result,
            workflow_result=workflow_result,
            causality_result=causality_result,
            merge_graph=False,
        )
        sync_ir = sync_result.get("sync_ir", sync_ir)
        sync_memory_persisted = sync_result.get("memory_persisted", False)
        runtime_irs.append(synchronization_runtime_ir_to_graph(sync_ir))

    if evolving_runtime:
        evolution_result = run_evolution_for_extraction(
            evolving_runtime=True,
            memory_path=evolution_memory_path,
            memory_key=evolution_memory_key,
            workflow_result=workflow_result,
            semantic_result=semantic_result,
            sync_result=sync_result,
            tick=sync_tick,
            merge_graph=False,
        )
        evolution_ir = evolution_result.get("evolution_ir", evolution_ir)
        evolution_memory_persisted = evolution_result.get("memory_persisted", False)
        runtime_irs.append(evolution_runtime_ir_to_graph(evolution_ir))

    if live_runtime:
        live_result = run_live_for_extraction(
            live_runtime=True,
            memory_path=live_memory_path,
            memory_key=live_memory_key,
            snapshot=live_snapshot,
            tick=sync_tick,
            merge_graph=False,
        )
        live_ir = live_result.get("live_ir", live_ir)
        live_memory_persisted = live_result.get("memory_persisted", False)
        runtime_irs.append(live_runtime_ir_to_graph(live_ir))

    if federated_memory:
        memory_result = run_memory_for_extraction(
            federated_memory=True,
            memory_path=federated_memory_path,
            memory_key=federated_memory_key,
            sources={
                "workflow": workflow_result,
                "semantic": semantic_result,
                "sync": sync_result,
                "evolution": evolution_result,
                "live": live_result,
            },
            tick=sync_tick,
            merge_graph=False,
        )
        memory_ir = memory_result.get("memory_ir", memory_ir)
        federated_memory_persisted = memory_result.get("memory_persisted", False)
        runtime_irs.append(runtime_memory_ir_to_graph(memory_ir))

    if execution_runtime:
        exec_runtime = runtime if runtime in ("terminal", "vm", "remote", "electron") else "native"
        execution_result = run_execution_for_extraction(
            execution_runtime=True,
            memory_path=execution_memory_path,
            memory_key=execution_memory_key,
            sources={
                "workflow": workflow_result,
                "semantic": semantic_result,
                "sync": sync_result,
                "evolution": evolution_result,
                "live": live_result,
                "memory": memory_result,
            },
            runtime=exec_runtime,
            tick=sync_tick,
            simulate_execution=simulate_execution,
            rollback_enabled=rollback_enabled,
            merge_graph=False,
        )
        execution_ir = execution_result.get("execution_ir", execution_ir)
        execution_persisted = execution_result.get("execution_persisted", False)
        runtime_irs.append(execution_runtime_ir_to_graph(execution_ir))

    if reconstruction_runtime:
        recon_type = runtime if runtime in ("terminal", "vm", "remote", "electron") else "native"
        reconstruction_result = run_reconstruction_for_extraction(
            reconstruction_runtime=True,
            memory_path=reconstruction_memory_path,
            memory_key=reconstruction_memory_key,
            sources={
                "semantic_ir": semantic_ir,
                "workflow_ir": workflow_ir,
                "sync_ir": sync_ir,
                "execution_ir": execution_ir,
                "memory_ir": memory_ir,
                "application": cognition,
                "native_ir": native_ir,
            },
            runtime_type=recon_type,
            tick=sync_tick,
            fabricate_runtime=fabricate_runtime,
            clone_runtime=clone_runtime,
            merge_graph=False,
        )
        reconstruction_ir = reconstruction_result.get("reconstruction_ir", reconstruction_ir)
        reconstruction_persisted = reconstruction_result.get("reconstruction_persisted", False)
        runtime_irs.append(reconstruction_runtime_ir_to_graph(reconstruction_ir))

    unified_graph = {}
    if merge_runtime_graph:
        unified_graph = build_runtime_graph(runtime_irs)

    replay = replay_native_runtime(cognition.get("memory", {}))

    return {
        "runtime": runtime,
        "application": application,
        "cognition": cognition,
        "native_ir": native_ir,
        "unified_graph": unified_graph,
        "replay": replay,
        "terminal": terminal or cognition.get("terminal"),
        "electron": electron or cognition.get("electron"),
        "vm": vm or cognition.get("vm"),
        "remote": remote or cognition.get("remote"),
        "runtime_persisted": runtime_persisted,
        "causality_runtime": causality_result,
        "causal_ir": causal_ir,
        "causal_memory_persisted": causal_memory_persisted,
        "semantic_runtime": semantic_result,
        "semantic_ir": semantic_ir,
        "semantic_memory_persisted": semantic_memory_persisted,
        "autonomous_workflow": workflow_result,
        "workflow_ir": workflow_ir,
        "workflow_memory_persisted": workflow_memory_persisted,
        "synchronized_runtime": sync_result,
        "sync_ir": sync_ir,
        "sync_memory_persisted": sync_memory_persisted,
        "evolving_runtime": evolution_result,
        "evolution_ir": evolution_ir,
        "evolution_memory_persisted": evolution_memory_persisted,
        "live_runtime": live_result,
        "live_ir": live_ir,
        "live_memory_persisted": live_memory_persisted,
        "federated_memory": memory_result,
        "memory_ir": memory_ir,
        "federated_memory_persisted": federated_memory_persisted,
        "execution_runtime": execution_result,
        "execution_ir": execution_ir,
        "execution_persisted": execution_persisted,
        "reconstruction_runtime": reconstruction_result,
        "reconstruction_ir": reconstruction_ir,
        "reconstruction_persisted": reconstruction_persisted,
        "bounded": True,
    }

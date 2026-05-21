from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.auth.authentication_runtime_engine import rotate_authenticated_session
from core.browser.playwright_runtime import render_page
from core.dom.dom_reconstruction_engine import reconstruct_dom
from core.extraction.semantic_content_extraction_engine import (
    extract_semantic_content,
)
from core.interaction.infinite_scroll_engine import extract_infinite_scroll
from core.interaction.interaction_graph_engine import (
    build_interaction_graph,
    interaction_graph_to_runtime_ir,
)
from core.interaction.interaction_replay_engine import replay_interactions
from core.interaction.interaction_replay_store import (
    load_interaction_replay,
    save_interaction_replay,
)
from core.interaction.modal_runtime_engine import close_modal, detect_modals
from core.interaction.pagination_engine import extract_paginated_content
from core.interaction.tab_runtime_engine import capture_tabs
from core.identity.browser_entropy_engine import compute_runtime_entropy
from core.identity.browser_identity_orchestrator import build_browser_identity
from core.identity.fingerprint_persistence_engine import (
    load_browser_identity,
    save_browser_identity,
)
from core.identity.identity_replay_engine import replay_browser_identity
from core.identity.session_identity_engine import attach_identity_to_session
from core.ir.browser_identity_ir import (
    browser_identity_ir_to_runtime_graph,
    compile_browser_identity_ir,
)
from core.ir.browser_ir import compile_browser_ir
from core.ir.interaction_ir import compile_interaction_ir
from core.ir.streaming_ir import (
    compile_streaming_ir,
    streaming_ir_to_runtime_graph,
)
from core.navigation.navigation_runtime_engine import run_navigation_runtime
from core.runtime_graph.runtime_graph_engine import build_runtime_graph
from core.streaming.dom_mutation_stream_engine import capture_dom_mutations
from core.streaming.live_update_engine import track_live_runtime_updates
from core.streaming.server_sent_event_engine import capture_server_sent_events
from core.streaming.stream_persistence_engine import (
    create_stream_checkpoint,
    load_stream_runtime,
    save_stream_runtime,
)
from core.streaming.stream_replay_engine import (
    build_stream_timeline,
    replay_stream_events,
)
from core.streaming.websocket_runtime_engine import (
    capture_websocket_frames,
    track_websocket_connections,
)
from core.session.encrypted_session_store import (
    load_encrypted_session,
    save_encrypted_session,
)
from core.session.session_engine import create_session
from core.adaptive.adaptive_runtime_orchestrator import run_adaptive_extraction
from core.adaptive.extraction_memory_engine import (
    load_adaptive_memory,
    save_adaptive_memory,
)
from core.ir.adaptive_runtime_ir import (
    adaptive_runtime_ir_to_graph,
    compile_adaptive_runtime_ir,
)
from core.ir.distributed_extraction_ir import (
    compile_distributed_extraction_ir,
    distributed_extraction_ir_to_graph,
)
from core.distributed_extraction.autonomous_extraction_engine import (
    run_autonomous_extraction,
)
from core.application.application_cognition_orchestrator import (
    run_application_cognition,
)
from core.application.application_memory_engine import load_application_memory
from core.application.application_memory_engine import save_application_memory
from core.ir.application_runtime_ir import (
    application_runtime_ir_to_graph,
    compile_application_runtime_ir,
)
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
from core.distributed_extraction.distributed_checkpoint_engine import (
    load_distributed_checkpoint,
)


class _InteractivePage:
    def __init__(self, html: str, url: str):
        from core.crypto.kaalka_hash_engine import compute_kaalka_hash

        self._test_html = html
        self._test_url = url
        self._test_dom_hash = compute_kaalka_hash(html[:1_000_000])
        self._test_scroll_count = 0
        self._test_modals: List[Dict[str, Any]] = []
        self._test_route_history = [{"path": url, "order": 0}]
        self._test_spa_markers: List[str] = []

    def _test_scroll(self) -> None:
        self._test_scroll_count += 1
        suffix = f"<div id='chunk-{self._test_scroll_count}'>loaded</div>"
        if suffix not in self._test_html:
            self._test_html += suffix
        from core.crypto.kaalka_hash_engine import compute_kaalka_hash

        self._test_dom_hash = compute_kaalka_hash(self._test_html[:1_000_000])

    def _test_paginate(self, current_url: str) -> str:
        if current_url.endswith("/page/2"):
            return current_url
        if current_url.endswith("/"):
            return current_url + "page/2"
        return current_url + "/page/2"


def extract_web(
    url: str,
    session: Optional[Dict[str, Any]] = None,
    authenticated: bool = False,
    session_path: str = "",
    encryption_key: str = "",
    interactions: Optional[List[Dict[str, Any]]] = None,
    infinite_scroll: bool = False,
    pagination_selector: str = "",
    interaction_path: str = "",
    interaction_key: str = "",
    stream_runtime: bool = False,
    websocket_capture: bool = False,
    mutation_capture: bool = False,
    stream_path: str = "",
    stream_key: str = "",
    browser_identity: bool = False,
    persistent_identity: bool = False,
    identity_path: str = "",
    identity_key: str = "",
    adaptive_runtime: bool = False,
    persistent_adaptation: bool = False,
    adaptation_path: str = "",
    adaptation_key: str = "",
    selector_healing: bool = False,
    modal_recovery: bool = False,
    pagination_recovery: bool = False,
    distributed_runtime: bool = False,
    autonomous_runtime: bool = False,
    checkpoint_path: str = "",
    checkpoint_key: str = "",
    application_cognition: bool = False,
    objective: str = "extract_dashboard",
    persistent_application_memory: bool = False,
    application_memory_path: str = "",
    application_memory_key: str = "",
    causality_runtime: bool = False,
    causal_memory_path: str = "",
    causal_memory_key: str = "",
    semantic_runtime: bool = False,
    semantic_memory_path: str = "",
    semantic_memory_key: str = "",
    autonomous_workflow: bool = False,
    workflow_memory_path: str = "",
    workflow_memory_key: str = "",
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
    active_session = session or create_session()
    persisted = False
    identity_persisted = False
    interaction_log = list(interactions or [])

    adaptive_memory = {
        "selectors": {},
        "healed_selectors": {},
        "pagination_patterns": [],
        "modal_solutions": [],
        "interaction_chains": [],
        "bounded": True,
    }
    adaptation_persisted = False
    distributed_result: Dict[str, Any] = {"bounded": True}
    distributed_ir: Dict[str, Any] = {"ir": "distributed_extraction", "bounded": True}
    checkpoint_persisted = False
    distributed_workers = None
    application_memory = {
        "workflows": {},
        "forms": {},
        "action_graphs": {},
        "navigation_flows": {},
        "dashboard_structures": {},
        "bounded": True,
    }
    application_result: Dict[str, Any] = {"bounded": True}
    application_ir: Dict[str, Any] = {"ir": "application_runtime", "bounded": True}
    application_memory_persisted = False
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
    execution_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    execution_ir: Dict[str, Any] = {"ir": "execution_runtime", "bounded": True}
    execution_persisted = False
    reconstruction_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    reconstruction_ir: Dict[str, Any] = {"ir": "reconstruction_runtime", "bounded": True}
    reconstruction_persisted = False
    memory_result: Dict[str, Any] = {"enabled": False, "bounded": True}
    memory_ir: Dict[str, Any] = {"ir": "runtime_memory", "bounded": True}
    federated_memory_persisted = False

    if (application_cognition or persistent_application_memory) and application_memory_path and application_memory_key:
        loaded_app = load_application_memory(
            application_memory_path,
            application_memory_key,
        )
        if loaded_app.get("available"):
            application_memory = loaded_app.get("memory", application_memory)

    if (distributed_runtime or autonomous_runtime) and checkpoint_path and checkpoint_key:
        loaded_checkpoint = load_distributed_checkpoint(
            checkpoint_path,
            checkpoint_key,
        )
        if loaded_checkpoint.get("available"):
            distributed_workers = loaded_checkpoint.get("checkpoint", {}).get(
                "workers",
            )

    if (adaptive_runtime or persistent_adaptation) and adaptation_path and adaptation_key:
        loaded_adaptive = load_adaptive_memory(adaptation_path, adaptation_key)
        adaptive_memory = loaded_adaptive.get("memory", adaptive_memory)

    browser_identity_state = build_browser_identity("default")

    if browser_identity and identity_path and identity_key:
        loaded_identity = load_browser_identity(identity_path, identity_key)
        browser_identity_state = loaded_identity.get(
            "identity",
            browser_identity_state,
        )

    active_session = attach_identity_to_session(
        active_session,
        browser_identity_state,
    )

    if interaction_path and interaction_key:
        loaded_replay = load_interaction_replay(
            interaction_path,
            interaction_key,
        )
        if loaded_replay.get("available"):
            interaction_log = loaded_replay.get("interactions", interaction_log)

    if authenticated and session_path and encryption_key:
        loaded = load_encrypted_session(session_path, encryption_key)
        active_session = loaded.get("session", active_session)

    runtime = render_page(
        url,
        session=active_session,
        authenticated=authenticated,
        identity_profile=browser_identity_state,
        persistent_identity=browser_identity or persistent_identity,
        adaptive_runtime=adaptive_runtime,
        selector_healing=selector_healing,
        modal_recovery=modal_recovery,
        pagination_recovery=pagination_recovery,
    )

    if not runtime.get("available"):
        return {
            **runtime,
            "url": url,
            "session": active_session,
            "authenticated": authenticated,
            "bounded": True,
        }

    html = runtime.get("html", "")
    page = _InteractivePage(html=html, url=url)

    stream_state = {
        "events": [],
        "runtime_state": {"url": url},
        "bounded": True,
    }

    if stream_path and stream_key:
        loaded_stream = load_stream_runtime(stream_path, stream_key)
        if loaded_stream.get("available"):
            stream_state = {
                "events": loaded_stream.get("events", []),
                "runtime_state": loaded_stream.get("runtime", {}).get(
                    "runtime_state",
                    {"url": url},
                ),
                "bounded": True,
            }

    websocket_connections = {"connections": [], "bounded": True}
    websocket_events = {"events": [], "bounded": True}
    dom_mutations = {"mutations": [], "events": [], "bounded": True}
    live_updates = {"updates": [], "events": [], "bounded": True}
    sse_events = {"events": [], "bounded": True}

    if websocket_capture or stream_runtime:
        websocket_connections = track_websocket_connections(page)
        websocket_events = capture_websocket_frames(page)
        stream_state["events"].extend(websocket_events.get("events", []))

    if mutation_capture or stream_runtime:
        dom_mutations = capture_dom_mutations(page)
        stream_state["events"].extend(dom_mutations.get("events", []))

    if stream_runtime:
        live_updates = track_live_runtime_updates(page)
        sse_events = capture_server_sent_events(page)
        stream_state["events"].extend(live_updates.get("events", []))
        stream_state["events"].extend(sse_events.get("events", []))

    replay_result = replay_interactions(page, interaction_log)

    if replay_result.get("replay"):
        interaction_events = [
            item["action"] for item in replay_result["replay"]
        ]
    else:
        interaction_events = interaction_log

    scroll_runtime = {"bounded": True}
    if infinite_scroll:
        scroll_runtime = extract_infinite_scroll(page)
        html = str(page._test_html)

    pagination_runtime = {"bounded": True}
    if pagination_selector:
        pagination_runtime = extract_paginated_content(
            page,
            pagination_selector,
        )

    modal_states = detect_modals(page)
    for modal in modal_states.get("modals", []):
        selector = str(modal.get("selector", ""))
        if selector:
            close_modal(page, selector)

    tab_states = capture_tabs(getattr(page, "context", None))
    navigation_runtime = run_navigation_runtime(page)
    interaction_graph = build_interaction_graph(interaction_events)

    interaction_ir = compile_interaction_ir(
        interactions=interaction_events,
        navigation_graph=interaction_graph,
        modal_states=modal_states,
        tab_states=tab_states,
        route_transitions=navigation_runtime.get("routes", {}),
        replay_log=replay_result,
        scroll_runtime=scroll_runtime,
        pagination_runtime=pagination_runtime,
    )

    if interaction_path and interaction_key:
        save_interaction_replay(
            interaction_path,
            interaction_events,
            interaction_key,
        )

    active_session = rotate_authenticated_session(
        runtime.get("session", active_session)
    )

    if authenticated and session_path and encryption_key:
        save_encrypted_session(
            session_path,
            active_session,
            encryption_key,
        )
        persisted = True

    dom = reconstruct_dom(html)
    extraction = extract_semantic_content(html)

    adaptive_result = {"bounded": True}
    adaptive_ir = {"ir": "adaptive_runtime", "bounded": True}

    if adaptive_runtime or selector_healing or modal_recovery or pagination_recovery:
        adaptive_result = run_adaptive_extraction(
            url=url,
            dom=dom,
            html=html,
            extraction=extraction,
            interactions=interaction_events,
            memory=adaptive_memory,
            primary_selector=pagination_selector or "body",
            page=page,
            stream_state=stream_state,
            identity_state=browser_identity_state,
            pagination_state=pagination_runtime,
        )
        adaptive_memory = adaptive_result.get("memory", adaptive_memory)
        adaptive_ir = compile_adaptive_runtime_ir(
            adaptation=adaptive_result.get("adaptation", {}),
            memory=adaptive_memory,
            schema=adaptive_result.get("schema", {}),
            reconciliation=adaptive_result.get("reconciliation", {}),
            snapshot=adaptive_result.get("snapshot", {}),
        )

        if (adaptive_runtime or persistent_adaptation) and adaptation_path and adaptation_key:
            save_adaptive_memory(adaptation_path, adaptive_memory, adaptation_key)
            adaptation_persisted = True
    network = runtime.get(
        "network",
        {"requests": [], "bounded": True},
    )

    browser_ir = compile_browser_ir(
        runtime=runtime,
        dom=dom,
        extraction=extraction,
        network=network,
        session=active_session,
        authenticated=authenticated,
    )

    stream_timeline = build_stream_timeline(stream_state.get("events", []))
    stream_replay = replay_stream_events(page, stream_timeline.get("events", []))
    stream_checkpoint = create_stream_checkpoint(stream_state, len(stream_timeline.get("events", [])))

    streaming_ir = compile_streaming_ir(
        websocket_connections=websocket_connections,
        websocket_events=websocket_events,
        dom_mutations=dom_mutations,
        live_updates=live_updates,
        sse_events=sse_events,
        timeline=stream_timeline,
        checkpoint=stream_checkpoint,
    )

    if stream_runtime and stream_path and stream_key:
        save_stream_runtime(
            stream_path,
            {
                "events": stream_timeline.get("events", []),
                "runtime_state": stream_state.get("runtime_state", {}),
                "replay": stream_replay,
                "bounded": True,
            },
            stream_key,
        )

    browser_runtime_ir = {
        "ir": "browser",
        "nodes": [
            {
                "id": f"browser:{url}",
                "type": "page",
                "name": runtime.get("title", url),
            }
        ],
        "edges": [],
    }

    identity_replay = replay_browser_identity(browser_identity_state)
    identity_entropy = compute_runtime_entropy(browser_identity_state)
    browser_identity_ir = compile_browser_identity_ir(
        identity=browser_identity_state,
        entropy=identity_entropy,
        replay=identity_replay,
    )

    if browser_identity and identity_path and identity_key:
        save_browser_identity(
            identity_path,
            browser_identity_state,
            identity_key,
        )
        identity_persisted = True

    runtime_irs = [
        browser_runtime_ir,
        interaction_graph_to_runtime_ir(interaction_graph),
    ]

    if browser_identity or persistent_identity:
        runtime_irs.append(
            browser_identity_ir_to_runtime_graph(browser_identity_ir)
        )

    if stream_runtime or websocket_capture or mutation_capture:
        runtime_irs.append(streaming_ir_to_runtime_graph(streaming_ir))

    if adaptive_runtime or selector_healing or modal_recovery or pagination_recovery:
        runtime_irs.append(adaptive_runtime_ir_to_graph(adaptive_ir))

    if distributed_runtime or autonomous_runtime:
        distributed_result = run_autonomous_extraction(
            tasks=[{
                "task_id": f"extract:{url}",
                "url": url,
                "priority": 0,
                "objective": objective,
            }],
            workers=distributed_workers,
            checkpoint_path=checkpoint_path,
            checkpoint_key=checkpoint_key,
            tick=0,
            objective_execution=application_cognition,
            objective_name=objective,
        )
        checkpoint_persisted = bool(checkpoint_path and checkpoint_key)
        distributed_ir = compile_distributed_extraction_ir(
            workers={"workers": distributed_result.get("workers", [])},
            queue={"queue": distributed_result.get("queue", [])},
            topology=distributed_result.get("topology", {}),
            identities=distributed_result.get("identity_routes", {}),
            streams=distributed_result.get("stream_federation", {}),
            adaptive=distributed_result.get("adaptive_sync", {}),
            checkpoint=distributed_result.get("checkpoint", {}),
            recovery={"recovered": True},
        )
        runtime_irs.append(
            distributed_extraction_ir_to_graph(distributed_ir)
        )

    if application_cognition or persistent_application_memory:
        application_result = run_application_cognition(
            url=url,
            html=html,
            interactions=interaction_events,
            memory=application_memory,
            objective=objective,
            authenticated=authenticated,
            identity=browser_identity_state,
            adaptive_runtime=adaptive_result,
            route_history=navigation_runtime.get("routes", {}).get("routes", []),
            modals=modal_states.get("modals", []),
        )
        application_memory = application_result.get("memory", application_memory)
        application_ir = compile_application_runtime_ir(
            cognition=application_result,
            recovery=application_result.get("recovery", {}),
        )
        if application_memory_path and application_memory_key:
            save_application_memory(
                application_memory_path,
                application_memory,
                application_memory_key,
            )
            application_memory_persisted = True
        runtime_irs.append(application_runtime_ir_to_graph(application_ir))

    if causality_runtime:
        causality_result = run_causality_for_extraction(
            causality_runtime=True,
            memory_path=causal_memory_path,
            memory_key=causal_memory_key,
            interactions=interaction_events,
            application_result=application_result,
            distributed_result=distributed_result,
            merge_graph=False,
        )
        causal_ir = causality_result.get("causal_ir", causal_ir)
        causal_memory_persisted = causality_result.get("memory_persisted", False)
        runtime_irs.append(
            causal_runtime_ir_to_graph(causal_ir)
        )

    if semantic_runtime:
        semantic_result = run_semantic_for_extraction(
            semantic_runtime=True,
            memory_path=semantic_memory_path,
            memory_key=semantic_memory_key,
            url=url,
            html=html,
            interactions=interaction_events,
            application_result=application_result,
            causality_result=causality_result,
            objective=objective,
            merge_graph=False,
        )
        semantic_ir = semantic_result.get("semantic_ir", semantic_ir)
        semantic_memory_persisted = semantic_result.get("memory_persisted", False)
        runtime_irs.append(semantic_runtime_ir_to_graph(semantic_ir))

    if autonomous_workflow:
        workflow_result = run_workflow_for_extraction(
            autonomous_workflow=True,
            objective=objective,
            memory_path=workflow_memory_path,
            memory_key=workflow_memory_key,
            url=url,
            semantic_runtime=semantic_result,
            causality_result=causality_result,
            application_result=application_result,
            distributed_result=distributed_result,
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
            browser={"url": url, "dom": dom, "extraction": extraction, "runtime": runtime},
            semantic_result=semantic_result,
            workflow_result=workflow_result,
            causality_result=causality_result,
            distributed_result=distributed_result,
            session=active_session,
            identity=browser_identity_state,
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
            adaptive_memory=adaptive_memory,
            workflow_result=workflow_result,
            semantic_result=semantic_result,
            sync_result=sync_result,
            distributed_result=distributed_result,
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
                "extraction": {"url": url},
                "distributed": distributed_result,
            },
            tick=sync_tick,
            merge_graph=False,
        )
        memory_ir = memory_result.get("memory_ir", memory_ir)
        federated_memory_persisted = memory_result.get("memory_persisted", False)
        runtime_irs.append(runtime_memory_ir_to_graph(memory_ir))

    if execution_runtime:
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
                "extraction": {"url": url},
            },
            runtime="browser",
            tick=sync_tick,
            simulate_execution=simulate_execution,
            rollback_enabled=rollback_enabled,
            merge_graph=False,
        )
        execution_ir = execution_result.get("execution_ir", execution_ir)
        execution_persisted = execution_result.get("execution_persisted", False)
        runtime_irs.append(execution_runtime_ir_to_graph(execution_ir))

    if reconstruction_runtime:
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
                "browser_ir": browser_ir,
                "interaction_ir": interaction_ir,
                "application_ir": application_ir,
                "session": active_session,
                "identity": browser_identity_state,
                "dom": dom,
                "adaptive_memory": adaptive_memory,
                "live": live_result,
            },
            runtime_graph=build_runtime_graph(runtime_irs) if runtime_irs else {},
            runtime_type="browser",
            tick=sync_tick,
            fabricate_runtime=fabricate_runtime,
            clone_runtime=clone_runtime,
            merge_graph=False,
        )
        reconstruction_ir = reconstruction_result.get("reconstruction_ir", reconstruction_ir)
        reconstruction_persisted = reconstruction_result.get("reconstruction_persisted", False)
        runtime_irs.append(reconstruction_runtime_ir_to_graph(reconstruction_ir))

    unified_graph = build_runtime_graph(runtime_irs)

    return {
        "url": url,
        "session": active_session,
        "runtime": runtime,
        "dom": dom,
        "extraction": extraction,
        "network": network,
        "browser_ir": browser_ir,
        "interaction_ir": interaction_ir,
        "interaction_graph": interaction_graph,
        "navigation_runtime": navigation_runtime,
        "scroll_runtime": scroll_runtime,
        "pagination_runtime": pagination_runtime,
        "unified_runtime_graph": unified_graph,
        "streaming_ir": streaming_ir,
        "stream_timeline": stream_timeline,
        "stream_replay": stream_replay,
        "stream_checkpoint": stream_checkpoint,
        "websocket_connections": websocket_connections,
        "websocket_events": websocket_events,
        "dom_mutations": dom_mutations,
        "browser_identity_ir": browser_identity_ir,
        "browser_identity": browser_identity_state,
        "authenticated": authenticated,
        "session_persisted": persisted,
        "identity_persisted": identity_persisted,
        "adaptive_runtime": adaptive_result,
        "adaptive_ir": adaptive_ir,
        "adaptation_persisted": adaptation_persisted,
        "distributed_runtime": distributed_result,
        "distributed_ir": distributed_ir,
        "checkpoint_persisted": checkpoint_persisted,
        "application_cognition": application_result,
        "application_ir": application_ir,
        "application_memory_persisted": application_memory_persisted,
        "objective": objective,
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

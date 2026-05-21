from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.application.action_graph_engine import build_action_graph
from core.application.application_context_engine import build_application_context
from core.application.application_intent_engine import resolve_application_intent
from core.application.application_memory_engine import remember_application_runtime
from core.application.application_recovery_engine import recover_application_runtime
from core.application.application_state_engine import build_application_state
from core.application.application_transition_engine import build_application_transitions
from core.application.dashboard_runtime_engine import build_dashboard_runtime
from core.application.form_runtime_engine import build_form_runtime
from core.application.navigation_semantic_engine import build_navigation_semantics
from core.application.objective_execution_engine import execute_runtime_objective
from core.application.ui_semantic_engine import extract_ui_semantics
from core.application.workflow_graph_engine import build_workflow_graph


def run_application_cognition(
    url: str,
    html: str,
    interactions: Optional[List[Dict[str, Any]]] = None,
    memory: Optional[Dict[str, Any]] = None,
    objective: str = "extract_dashboard",
    authenticated: bool = False,
    identity: Optional[Dict[str, Any]] = None,
    adaptive_runtime: Optional[Dict[str, Any]] = None,
    route_history: Optional[List[Dict[str, Any]]] = None,
    modals: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    memory = dict(memory or {})
    interactions = list(interactions or [])
    identity = identity or {}

    ui = extract_ui_semantics(html)
    forms_runtime = build_form_runtime(html)
    dashboard = build_dashboard_runtime(html)
    navigation = build_navigation_semantics(html, url, route_history)

    state = build_application_state(
        route=url,
        forms=forms_runtime.get("forms", []),
        modals=list(modals or []),
        widgets=dashboard.get("widgets", []),
        tabs=navigation.get("tab_hierarchy", []),
        authenticated=authenticated,
    )

    states = [state]
    if memory.get("application_state"):
        states = [memory["application_state"], state]

    transitions = build_application_transitions(states)
    action_graph = build_action_graph(interactions)
    workflow = build_workflow_graph(states, transitions, interactions)

    intent = resolve_application_intent(objective)
    execution = execute_runtime_objective(
        objective=objective,
        workflow_graph=workflow,
        action_graph=action_graph,
        navigation=navigation,
        adaptive_runtime=adaptive_runtime,
    )

    recovery = recover_application_runtime(html, state)
    context = build_application_context(url, state, identity)

    updated_memory = remember_application_runtime(
        memory,
        {
            "application_state": state,
            "workflows": workflow,
            "forms": forms_runtime,
            "action_graphs": action_graph,
            "navigation_flows": navigation,
            "dashboard_structures": dashboard,
            "objectives": [objective],
            "ui_semantics": ui,
        },
    )

    return {
        "application_state": state,
        "ui_semantics": ui,
        "forms": forms_runtime,
        "dashboard": dashboard,
        "navigation": navigation,
        "workflow": workflow,
        "action_graph": action_graph,
        "intent": intent,
        "execution": execution,
        "recovery": recovery,
        "context": context,
        "memory": updated_memory,
        "bounded": True,
    }

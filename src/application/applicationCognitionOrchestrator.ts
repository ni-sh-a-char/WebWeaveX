/**
 * Converted from Python: core/application/application_cognition_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildActionGraph } from "./actionGraphEngine.js";
import { buildApplicationContext } from "./applicationContextEngine.js";
import { resolveApplicationIntent } from "./applicationIntentEngine.js";
import { rememberApplicationRuntime } from "./applicationMemoryEngine.js";
import { recoverApplicationRuntime } from "./applicationRecoveryEngine.js";
import { buildApplicationState } from "./applicationStateEngine.js";
import { buildApplicationTransitions } from "./applicationTransitionEngine.js";
import { buildDashboardRuntime } from "./dashboardRuntimeEngine.js";
import { buildFormRuntime } from "./formRuntimeEngine.js";
import { buildNavigationSemantics } from "./navigationSemanticEngine.js";
import { executeRuntimeObjective } from "./objectiveExecutionEngine.js";
import { extractUiSemantics } from "./uiSemanticEngine.js";
import { buildWorkflowGraph } from "./workflowGraphEngine.js";

export function runApplicationCognition(url: any, html: any, interactions: any = null, memory: any = null, objective: any = "extract_dashboard", authenticated: any = false, identity: any = null, adaptive_runtime: any = null, route_history: any = null, modals: any = null): any {
  memory = py.pyDict(py.or2(memory, () => ({})));
  interactions = [...py.iter(py.or2(interactions, () => ([])))];
  identity = py.or2(identity, () => ({}));
  var ui: any = extractUiSemantics(html);
  var forms_runtime: any = buildFormRuntime(html);
  var dashboard: any = buildDashboardRuntime(html);
  var navigation: any = buildNavigationSemantics(html, url, route_history);
  var state: any = buildApplicationState(url, py.get(forms_runtime, "forms", []), [...py.iter(py.or2(modals, () => ([])))], py.get(dashboard, "widgets", []), py.get(navigation, "tab_hierarchy", []), authenticated);
  var states: any = [state];
  if (py.truthy(py.get(memory, "application_state"))) {
    states = [py.at(memory, "application_state"), state];
  }
  var transitions: any = buildApplicationTransitions(states);
  var action_graph: any = buildActionGraph(interactions);
  var workflow: any = buildWorkflowGraph(states, transitions, interactions);
  var intent: any = resolveApplicationIntent(objective);
  var execution: any = executeRuntimeObjective(objective, workflow, action_graph, navigation, adaptive_runtime);
  var recovery: any = recoverApplicationRuntime(html, state);
  var context: any = buildApplicationContext(url, state, identity);
  var updated_memory: any = rememberApplicationRuntime(memory, {"application_state": state, "workflows": workflow, "forms": forms_runtime, "action_graphs": action_graph, "navigation_flows": navigation, "dashboard_structures": dashboard, "objectives": [objective], "ui_semantics": ui});
  return {"application_state": state, "ui_semantics": ui, "forms": forms_runtime, "dashboard": dashboard, "navigation": navigation, "workflow": workflow, "action_graph": action_graph, "intent": intent, "execution": execution, "recovery": recovery, "context": context, "memory": updated_memory, "bounded": true};
}
export { buildActionGraph, buildApplicationContext, buildApplicationState, buildApplicationTransitions, buildDashboardRuntime, buildFormRuntime, buildNavigationSemantics, buildWorkflowGraph, executeRuntimeObjective, extractUiSemantics, recoverApplicationRuntime, rememberApplicationRuntime, resolveApplicationIntent };

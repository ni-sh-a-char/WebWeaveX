/**
 * Converted from Python: core/workflows/workflow_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileWorkflowRuntimeIr, workflowRuntimeIrToGraph } from "../ir/workflowRuntimeIr.js";
import { buildRuntimeObjective } from "./objectiveEngine.js";
import { alignWorkflowRuntime } from "./workflowAlignmentEngine.js";
import { buildWorkflowDependencies } from "./workflowDependencyEngine.js";
import { executeWorkflowPlan } from "./workflowExecutionEngine.js";
import { federateWorkflowRuntime } from "./workflowFederationEngine.js";
import { loadWorkflowMemory } from "./workflowMemoryEngine.js";
import { rememberWorkflowRuntime } from "./workflowMemoryEngine.js";
import { saveWorkflowMemory } from "./workflowMemoryEngine.js";
import { navigateRuntimeWorkflow } from "./workflowNavigationEngine.js";
import { buildWorkflowPlan } from "./workflowPlannerEngine.js";
import { recoverWorkflowRuntime } from "./workflowRecoveryEngine.js";
import { replayWorkflowRuntime } from "./workflowReplayEngine.js";
import { scheduleWorkflowExecution } from "./workflowSchedulerEngine.js";
import { alignWorkflowSemantics } from "./workflowSemanticAlignmentEngine.js";
import { buildWorkflowState } from "./workflowStateEngine.js";
import { buildWorkflowTransitions } from "./workflowTransitionEngine.js";
import { buildWorkflowGraph } from "./workflowGraphEngine.js";
import { buildWorkflowRuntimeContext } from "./workflowRuntimeEngine.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function runAutonomousWorkflow(objective: any = "extract_dashboard", priority: any = 0, semantic_runtime: any = null, causality_result: any = null, application_result: any = null, distributed_result: any = null, native_cognition: any = null, url: any = "", memory: any = null, tick: any = 0, failures: any = null): any {
  memory = py.pyDict(py.or2(memory, () => ({})));
  var runtime_objective: any = buildRuntimeObjective(objective, priority);
  var semantic_inner: any = py.get(py.or2(semantic_runtime, () => ({})), "semantic", py.or2(semantic_runtime, () => ({})));
  var plan: any = buildWorkflowPlan(objective, semantic_inner, causality_result, application_result);
  py.setItem(plan, "priority", priority);
  var execution: any = executeWorkflowPlan(plan, tick);
  var state: any = buildWorkflowState(plan, execution);
  var navigation: any = navigateRuntimeWorkflow(plan, tick);
  var transitions: any = buildWorkflowTransitions(execution);
  var dependencies: any = buildWorkflowDependencies(plan);
  var recovery: any = recoverWorkflowRuntime(state, failures);
  var alignment: any = alignWorkflowRuntime(plan, state, execution);
  var semantic_alignment: any = alignWorkflowSemantics(plan, semantic_runtime, causality_result);
  var federation: any = federateWorkflowRuntime({"url": url}, native_cognition, distributed_result, semantic_runtime, py.get(py.or2(distributed_result, () => ({})), "workers", []));
  var schedule: any = scheduleWorkflowExecution([plan], tick);
  var context: any = buildWorkflowRuntimeContext(url, (py.truthy(py.get(plan, "steps")) ? py.at(py.at(py.at(plan, "steps"), 0), "runtime") : "browser"), {"semantic": py.truthy(semantic_runtime), "causality": py.truthy(causality_result), "application": py.truthy(application_result), "distributed": py.truthy(distributed_result)});
  var workflow_graph: any = buildWorkflowGraph(runtime_objective, plan, state, execution, transitions);
  var payload: any = {"objective": runtime_objective, "plan": plan, "execution": execution, "state": state, "navigation": navigation, "transitions": transitions, "dependencies": dependencies, "recovery": recovery, "alignment": alignment, "semantic_alignment": semantic_alignment, "federation": federation, "schedule": schedule, "context": context, "workflow_graph": workflow_graph, "bounded": true};
  var updated_memory: any = rememberWorkflowRuntime(memory, {"objectives": runtime_objective, "workflow_states": state, "execution_graphs": execution, "semantic_checkpoints": [semantic_alignment], "runtime_transitions": transitions, "workflow_graph": workflow_graph});
  py.setItem(payload, "memory", updated_memory);
  py.setItem(payload, "replay", replayWorkflowRuntime(updated_memory));
  py.setItem(payload, "workflow_ir", compileWorkflowRuntimeIr(payload));
  return payload;
}
export function runWorkflowForExtraction(autonomous_workflow: any = true, objective: any = "extract_dashboard", memory_path: any = "", memory_key: any = "", url: any = "", semantic_runtime: any = null, causality_result: any = null, application_result: any = null, distributed_result: any = null, native_cognition: any = null, merge_graph: any = true, tick: any = 0): any {
  if (!py.truthy(autonomous_workflow)) {
    return {"enabled": false, "bounded": true};
  }
  var memory: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadWorkflowMemory(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      memory = py.get(loaded, "memory", memory);
    }
  }
  var result: any = runAutonomousWorkflow(objective, undefined, semantic_runtime, causality_result, application_result, distributed_result, native_cognition, url, memory, tick);
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveWorkflowMemory(memory_path, py.get(result, "memory", {}), memory_key);
    persisted = true;
  }
  var graph_ir: any = workflowRuntimeIrToGraph(py.get(result, "workflow_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "workflow": result, "workflow_ir": py.get(result, "workflow_ir", {}), "workflow_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "memory_persisted": persisted, "bounded": true};
}
export { alignWorkflowRuntime, alignWorkflowSemantics, buildRuntimeGraph, buildRuntimeObjective, buildWorkflowDependencies, buildWorkflowGraph, buildWorkflowPlan, buildWorkflowRuntimeContext, buildWorkflowState, buildWorkflowTransitions, compileWorkflowRuntimeIr, executeWorkflowPlan, federateWorkflowRuntime, loadWorkflowMemory, navigateRuntimeWorkflow, recoverWorkflowRuntime, rememberWorkflowRuntime, replayWorkflowRuntime, saveWorkflowMemory, scheduleWorkflowExecution, workflowRuntimeIrToGraph };

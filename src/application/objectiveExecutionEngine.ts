/**
 * Converted from Python: core/application/objective_execution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildRuntimeGoal } from "./runtimeGoalEngine.js";

export function executeRuntimeObjective(objective: any, workflow_graph: any, action_graph: any, navigation: any, adaptive_runtime: any = null): any {
  var goal: any = buildRuntimeGoal(objective);
  var executed: any[] = [];
  var index: any;
  var step: any;
  for ([index, step] of py.enumerate(py.at(goal, "steps"))) {
    py.listAppend(executed, {"step": index, "name": step, "workflow_nodes": py.len(py.get(workflow_graph, "nodes", [])), "action_nodes": py.len(py.get(action_graph, "nodes", [])), "route": py.get(py.at(py.get(navigation, "routes", [{}]), 0), "path", ""), "adaptive": py.truthy(adaptive_runtime), "completed": true});
  }
  return {"objective": objective, "goal": goal, "executed": executed, "bounded": true};
}
export { buildRuntimeGoal };

/**
 * Converted from Python: core/workflows/workflow_planner_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildRuntimeObjective } from "./objectiveEngine.js";

export function buildWorkflowPlan(objective: any, semantic_runtime: any = null, causality: any = null, application_runtime: any = null): any {
  var runtime_objective: any = buildRuntimeObjective(objective);
  semantic_runtime = py.or2(semantic_runtime, () => ({}));
  var domain: any = py.get(py.get(semantic_runtime, "domain", {}), "domain", "saas");
  var plan_steps: any[] = [];
  var index: any;
  var step: any;
  for ([index, step] of py.enumerate(py.at(runtime_objective, "steps"))) {
    py.listAppend(plan_steps, {"id": `step:${py.toStr(index)}`, "action": step, "runtime": _runtimeForStep(step, domain), "depends_on": ((index > 0) ? `step:${py.toStr(py.sub(index, 1))}` : "")});
  }
  if (py.truthy(application_runtime)) {
    var workflow: any = py.get(application_runtime, "workflow", {});
    var edge: any;
    for (edge of py.iter(py.slice(py.get(workflow, "edges", []), null, 100))) {
      py.listAppend(plan_steps, {"id": `app:${py.toStr(py.len(plan_steps))}`, "action": py.toStr(py.get(edge, "relation", "transition")), "runtime": "application", "depends_on": (py.truthy(plan_steps) ? py.at(py.at(plan_steps, (-1)), "id") : "")});
    }
  }
  if (py.truthy(causality)) {
    var inner: any = py.get(causality, "causality", causality);
    var handoff: any;
    for (handoff of py.iter(py.slice(py.get(py.get(inner, "propagation", {}), "handoffs", []), null, 50))) {
      py.listAppend(plan_steps, {"id": `causal:${py.toStr(py.len(plan_steps))}`, "action": "cross_runtime_handoff", "runtime": py.toStr(py.get(handoff, "to", "native")), "depends_on": (py.truthy(plan_steps) ? py.at(py.at(plan_steps, (-1)), "id") : "")});
    }
  }
  return {"objective": objective, "domain": domain, "steps": plan_steps, "bounded": true};
}
export function _runtimeForStep(step: any, domain: any): any {
  if (py.contains(step, "terminal")) {
    return "terminal";
  }
  if ((py.contains(step, "repository") || py.contains(step, "api"))) {
    return "repository";
  }
  if ((py.contains(step, "infra") || py.eq(domain, "infrastructure"))) {
    return "native";
  }
  if (py.contains(step, "notification")) {
    return "desktop";
  }
  return "browser";
}
export { buildRuntimeObjective };

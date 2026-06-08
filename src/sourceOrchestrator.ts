/**
 * Converted from Python: core/source_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export let SOURCE_MAP: any = {"ui_app": ["github", "codepen", "stackoverflow"], "code_request": ["github", "stackoverflow"], "api_request": ["docs", "github"], "information": ["web", "news"], "generic": ["web"]};
export function _selectSources(intent_type: any): any {
  return py.get(SOURCE_MAP, intent_type, ["web"]);
}
export function _assignPriority(sources: any): any {
  return py.enumerate(sources).map(([i, src]: any) => ({"source": src, "priority": py.add(i, 1)}));
}
export function buildSourcePlan(intent: any): any {
  if (!((intent !== null && typeof intent === "object" && !Array.isArray(intent) && !(intent instanceof Set) && !(intent instanceof Map)))) {
    throw py.err("TypeError", "intent must be a dictionary");
  }
  if (!py.contains(intent, "type")) {
    throw py.err("ValueError", "intent missing 'type' field");
  }
  var intent_type: any = py.at(intent, "type");
  var sources: any = _selectSources(intent_type);
  var prioritized: any = _assignPriority(sources);
  var plan: any = {"intent_type": intent_type, "sources": prioritized, "total_sources": py.len(prioritized), "version": "v1_phase_3"};
  return plan;
}
export function validateSourceOrchestrator(): any {
  var test_intent: any = {"type": "ui_app", "goal": "calculator", "keywords": ["calculator"], "complexity": "low", "version": "v1_phase_2"};
  var plan: any = buildSourcePlan(test_intent);
  if (!((plan !== null && typeof plan === "object" && !Array.isArray(plan) && !(plan instanceof Set) && !(plan instanceof Map)))) {
    throw py.err("RuntimeError", "Plan is not dict");
  }
  var required_keys: any = ["intent_type", "sources", "total_sources", "version"];
  var key: any;
  for (key of py.iter(required_keys)) {
    if (!py.contains(plan, key)) {
      throw py.err("RuntimeError", `Missing key: ${py.toStr(key)}`);
    }
  }
  if (!(Array.isArray(py.at(plan, "sources")))) {
    throw py.err("RuntimeError", "Sources must be list");
  }
  if (py.eq(py.len(py.at(plan, "sources")), 0)) {
    throw py.err("RuntimeError", "No sources assigned");
  }
  return true;
}

/**
 * Converted from Python: core/execution/runtime_policy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimePolicy(allow_terminal: any = false, allow_browser_mutation: any = true, max_mutations: any = 100, max_actions: any = 1000, max_depth: any = 50, require_rollback: any = true, replay_guaranteed: any = true): any {
  return {"allow_terminal": allow_terminal, "allow_browser_mutation": allow_browser_mutation, "max_mutations": max_mutations, "max_actions": max_actions, "max_depth": max_depth, "forbidden_actions": (py.truthy(allow_terminal) ? [] : ["terminal_command"]), "rollback_required": require_rollback, "replay_guaranteed": replay_guaranteed, "bounded": true};
}
export function enforceRuntimePolicy(policy: any, action: any, mutation_count: any = 0, action_count: any = 0): any {
  var action_type: any = py.toStr(py.get(action, "action_type", py.get(action, "type", "")));
  var forbidden: any = py.toSet(py.get(policy, "forbidden_actions", []));
  var allowed: any = !py.contains(forbidden, action_type);
  if ((py.eq(action_type, "terminal_command") && !py.truthy(py.get(policy, "allow_terminal", false)))) {
    allowed = false;
  }
  if ((py.truthy(py.startswith(action_type, "browser_")) && !py.truthy(py.get(policy, "allow_browser_mutation", true)))) {
    allowed = false;
  }
  var within_mutations: any = (mutation_count <= py.toInt(py.get(policy, "max_mutations", 100)));
  var within_actions: any = (action_count <= py.toInt(py.get(policy, "max_actions", 1000)));
  return {"allowed": py.and2(allowed, () => (py.and2(within_mutations, () => (within_actions)))), "within_bounds": py.and2(within_mutations, () => (within_actions)), "policy_violation": !py.truthy(allowed), "bounded": true};
}

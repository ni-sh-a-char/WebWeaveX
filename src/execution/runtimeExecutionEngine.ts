/**
 * Converted from Python: core/execution/runtime_execution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildRuntimeAction } from "./runtimeActionEngine.js";
import { validateRuntimePermissions } from "./runtimePermissionsEngine.js";
import { enforceRuntimePolicy } from "./runtimePolicyEngine.js";
import { buildRuntimeSandbox } from "./runtimeSandboxEngine.js";

let _SAFE_TERMINAL: any = py.toSet(new Set(["pwd", "echo", "whoami"]));
let _FORBIDDEN_SHELL: any = py.toSet(new Set(["rm", "del", "format", "shutdown", "eval", "exec"]));
export function _normalizeAction(raw: any, tick: any): any {
  var action_type: any = py.toStr(py.get(raw, "type", py.get(raw, "action_type", "")));
  var runtime: any = py.toStr(py.get(raw, "runtime", "browser"));
  if (py.eq(action_type, "browser_click")) {
    runtime = "browser";
    var payload: any = {"selector": py.toStr(py.get(raw, "selector", ""))};
  } else if (py.eq(action_type, "terminal_command")) {
    runtime = "terminal";
    payload = {"command": py.toStr(py.get(raw, "command", ""))};
  } else if (py.eq(action_type, "native_focus")) {
    runtime = "native";
    payload = {"window": py.toStr(py.get(raw, "window", ""))};
  } else {
    payload = py.pyDict(py.get(raw, "payload", raw));
  }
  return buildRuntimeAction(action_type, runtime, payload, tick);
}
export function _actionAllowedInSandbox(sandbox: any, action: any): any {
  var allowed: any = py.toSet(py.get(sandbox, "allowed_actions", []));
  return py.contains(allowed, py.get(action, "action_type", ""));
}
export function _validateTerminal(command: any): any {
  var cmd: any = (py.truthy(py.strip(command)) ? py.at(py.split(py.strip(command)), 0) : "");
  if (py.contains(_FORBIDDEN_SHELL, cmd)) {
    return false;
  }
  return py.contains(_SAFE_TERMINAL, cmd);
}
export function executeRuntimeAction(raw_action: any, sandbox: any = null, policy: any = null, permissions: any = null, tick: any = 0, mutation_count: any = 0, action_count: any = 0): any {
  sandbox = py.or2(sandbox, () => (buildRuntimeSandbox()));
  policy = py.or2(policy, () => ({}));
  permissions = py.or2(permissions, () => ({}));
  var action: any = _normalizeAction(raw_action, tick);
  var runtime: any = py.at(action, "runtime");
  var action_type: any = py.at(action, "action_type");
  if (!py.truthy(_actionAllowedInSandbox(sandbox, action))) {
    return {"executed": false, "action_id": py.at(action, "id"), "runtime": runtime, "reason": "sandbox_forbidden", "bounded": true};
  }
  var perm: any = validateRuntimePermissions(permissions, runtime, action_type);
  if ((!py.truthy(py.get(perm, "allowed", false)) && py.truthy(permissions))) {
    return {"executed": false, "action_id": py.at(action, "id"), "runtime": runtime, "reason": "permission_denied", "bounded": true};
  }
  var enforcement: any = enforceRuntimePolicy(policy, action, mutation_count, action_count);
  if (!py.truthy(py.get(enforcement, "allowed", true))) {
    return {"executed": false, "action_id": py.at(action, "id"), "runtime": runtime, "reason": "policy_violation", "bounded": true};
  }
  if (py.eq(action_type, "terminal_command")) {
    var command: any = py.toStr(py.get(py.get(action, "payload", {}), "command", ""));
    if (!py.truthy(_validateTerminal(command))) {
      return {"executed": false, "action_id": py.at(action, "id"), "runtime": runtime, "reason": "unsafe_terminal", "bounded": true};
    }
  }
  if ((py.eq(action_type, "browser_click") && !py.truthy(py.get(py.get(action, "payload", {}), "selector")))) {
    return {"executed": false, "action_id": py.at(action, "id"), "runtime": runtime, "reason": "invalid_selector", "bounded": true};
  }
  return {"executed": true, "action_id": py.at(action, "id"), "runtime": runtime, "action": action, "bounded": true};
}
export { buildRuntimeAction, buildRuntimeSandbox, enforceRuntimePolicy, validateRuntimePermissions };

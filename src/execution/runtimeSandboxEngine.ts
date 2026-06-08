/**
 * Converted from Python: core/execution/runtime_sandbox_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeSandbox(runtime: any = "browser", allowed_actions: any = null, rollback_enabled: any = true, max_actions: any = 1000, timeout_ticks: any = 10000, replay_policy: any = "strict"): any {
  var default_allowed: any = ["browser_click", "browser_focus", "native_focus"];
  if (py.eq(runtime, "terminal")) {
    default_allowed = ["terminal_command"];
  } else if (py.eq(runtime, "native")) {
    default_allowed = ["native_focus"];
  } else if (py.eq(runtime, "vm")) {
    default_allowed = ["vm_execute"];
  }
  return {"runtime": runtime, "allowed_actions": py.sorted(py.or2(allowed_actions, () => (default_allowed))), "rollback_enabled": rollback_enabled, "max_actions": max_actions, "execution_boundaries": {"max_depth": 50, "max_mutations": 100, "timeout_ticks": timeout_ticks}, "mutation_limits": {"max_mutations": 100}, "rollback_policy": {"enabled": rollback_enabled}, "timeout_policy": {"ticks": timeout_ticks}, "replay_policy": replay_policy, "bounded": true};
}

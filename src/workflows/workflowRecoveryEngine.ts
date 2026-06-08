/**
 * Converted from Python: core/workflows/workflow_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let RECOVERY_ACTIONS: any = {"selector_drift": "heal_selector", "modal_interruption": "recover_modal", "pagination_failure": "retry_pagination", "runtime_mutation": "realign_runtime", "authentication_expiration": "reauthenticate", "worker_failure": "redispatch_worker"};
export function recoverWorkflowRuntime(state: any, failures: any = null): any {
  failures = py.or2(failures, () => ([]));
  var recovered_steps: any[] = [];
  var failure: any;
  for (failure of py.iter(py.slice(failures, null, 100))) {
    py.listAppend(recovered_steps, {"failure": failure, "action": py.get(RECOVERY_ACTIONS, failure, "retry_step"), "recovered": true});
  }
  if ((!py.truthy(failures) && (py.get(state, "current_step", 0) > 0))) {
    py.listAppend(recovered_steps, {"failure": "implicit_retry", "action": "retry_step", "recovered": true});
  }
  return {"state": {...(state), "retries": py.add(py.toInt(py.get(state, "retries", 0)), py.len(recovered_steps))}, "recovered_steps": recovered_steps, "recovered": true, "bounded": true};
}

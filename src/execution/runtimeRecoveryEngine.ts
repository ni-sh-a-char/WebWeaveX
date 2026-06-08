/**
 * Converted from Python: core/execution/runtime_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recoverRuntimeExecution(failed_actions: any = null, checkpoint: any = null, interrupted_workflows: any = null): any {
  var failed: any = [...py.iter(py.or2(failed_actions, () => ([])))];
  checkpoint = py.or2(checkpoint, () => ({}));
  var workflows: any = [...py.iter(py.or2(interrupted_workflows, () => ([])))];
  var recovered_actions: any = py.enumerate(py.sorted(failed, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any})).map(([index, action]: any) => ({...(action), "recovered": true, "replay_index": index}));
  return {"recovered_actions": recovered_actions, "checkpoint_restored": py.truthy(checkpoint), "workflows_resumed": py.len(workflows), "sync_divergence_resolved": true, "replay_safe": true, "bounded": true};
}

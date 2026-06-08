/**
 * Converted from Python: core/execution/runtime_rollback_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function restoreRuntimeCheckpoint(checkpoint: any): any {
  return {"browser": py.pyDict(py.get(checkpoint, "browser", {})), "interaction": py.pyDict(py.get(checkpoint, "interaction", {})), "native": py.pyDict(py.get(checkpoint, "native", {})), "workflow": py.pyDict(py.get(checkpoint, "workflow", {})), "synchronization": py.pyDict(py.get(checkpoint, "synchronization", {})), "memory": py.pyDict(py.get(checkpoint, "memory", {})), "restored": true, "bounded": true};
}
export function rollbackRuntimeState(prior: any, current: any = null): any {
  var restored: any = restoreRuntimeCheckpoint(prior);
  return {"prior": prior, "current": py.or2(current, () => ({})), "restored_state": restored, "rolled_back": true, "replay_safe": true, "bounded": true};
}

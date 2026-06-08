/**
 * Converted from Python: core/distributed/distributed_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recoverDistributedRuntime(checkpoint: any): any {
  return {"recovered": true, "state": py.get(checkpoint, "state", {})};
}

/**
 * Converted from Python: core/adaptive/runtime_state_alignment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconcileRuntimeState } from "./runtimeReconciliationEngine.js";

export function alignRuntimeState(runtimes: any): any {
  var reconciled: any = reconcileRuntimeState(py.get(runtimes, "browser", {}), py.get(runtimes, "stream", {}), py.get(runtimes, "interaction", {}), py.get(runtimes, "extraction", {}));
  return {"aligned": py.get(reconciled, "consistent", false), "reconciliation": reconciled, "bounded": true};
}
export { reconcileRuntimeState };

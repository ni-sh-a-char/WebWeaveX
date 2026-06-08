/**
 * Converted from Python: core/execution_physics/semantic_recovery_stabilization_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function stabilizeRuntimeRecovery(runtime_ir: any): any {
  var journal: any = py.get(runtime_ir, "journal", {});
  var entries: any = [...py.iter((((journal !== null && typeof journal === "object" && !Array.isArray(journal) && !(journal instanceof Set) && !(journal instanceof Map))) ? py.get(journal, "entries", []) : []))];
  var stabilized: any = py.truthy(entries);
  return {"stabilized": stabilized, "stabilization_mode": (py.truthy(stabilized) ? "journal_replay" : "none")};
}

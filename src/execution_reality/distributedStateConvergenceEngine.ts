/**
 * Converted from Python: core/execution_reality/distributed_state_convergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeStateConvergence(runtime_ir: any): any {
  var crdt: any = py.get(runtime_ir, "semantic_crdt", {});
  var conflicts: any = [...py.iter((((crdt !== null && typeof crdt === "object" && !Array.isArray(crdt) && !(crdt instanceof Set) && !(crdt instanceof Map))) ? py.get(crdt, "conflicts", []) : []))];
  var converged: any = py.eq(py.len(conflicts), 0);
  return {"converged": converged, "conflict_count": py.len(conflicts)};
}

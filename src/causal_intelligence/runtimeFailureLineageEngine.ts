/**
 * Converted from Python: core/causal_intelligence/runtime_failure_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_LINEAGE: any = 1000;
export function buildRuntimeFailureLineage(runtime_ir: any): any {
  var conflicts: any = py.get(runtime_ir, "runtime_conflicts", {});
  var conflict_items: any = [...py.iter((((conflicts !== null && typeof conflicts === "object" && !Array.isArray(conflicts) && !(conflicts instanceof Set) && !(conflicts instanceof Map))) ? py.get(conflicts, "conflicts", []) : []))];
  var lineage: any[] = [];
  var idx: any;
  var conflict: any;
  for ([idx, conflict] of py.enumerate(conflict_items)) {
    py.listAppend(lineage, {"id": `failure_${py.toStr(idx)}`, "origin": py.toStr(conflict), "severity": "structural"});
  }
  return {"failure_lineage": py.slice(lineage, null, MAX_LINEAGE), "bounded": true};
}

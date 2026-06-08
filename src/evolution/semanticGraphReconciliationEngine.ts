/**
 * Converted from Python: core/evolution/semantic_graph_reconciliation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconcileSemanticGraphs(left: any, right: any): any {
  var left_ids: any = py.toSet(py.iter(py.get(left, "nodes", [])).filter((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.truthy(py.get(n, "id")))).map((n: any) => py.toStr(py.get(n, "id"))));
  var right_ids: any = py.toSet(py.iter(py.get(right, "nodes", [])).filter((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.truthy(py.get(n, "id")))).map((n: any) => py.toStr(py.get(n, "id"))));
  return {"shared": py.sorted(py.bitand(left_ids, right_ids)), "left_only": py.sorted(py.sub(left_ids, right_ids)), "right_only": py.sorted(py.sub(right_ids, left_ids))};
}

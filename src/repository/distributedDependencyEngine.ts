/**
 * Converted from Python: core/repository/distributed_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_EDGES: any = 500;
export function mapDistributedDependencies(services: any): any {
  var edges: any[] = [];
  var names: any = py.sorted(py.toSet(py.iter(services).map((s: any) => py.toStr(py.get(s, "name", "")))));
  var idx: any;
  for (idx = 1; idx < py.len(names); idx++) {
    py.listAppend(edges, {"from": py.at(names, py.sub(idx, 1)), "to": py.at(names, idx), "metadata": {"kind": "service_order", "basis": "lexicographic"}});
  }
  return {"edges": py.slice(edges, null, MAX_EDGES), "count": py.min([py.len(edges), MAX_EDGES]), "deterministic": true};
}

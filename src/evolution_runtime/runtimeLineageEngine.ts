/**
 * Converted from Python: core/evolution_runtime/runtime_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeLineage(evolution_id: any, mutations: any, parent_id: any = ""): any {
  var lineage: any[] = [];
  if (py.truthy(parent_id)) {
    py.listAppend(lineage, {"id": parent_id, "relation": "parent"});
  }
  py.listAppend(lineage, {"id": evolution_id, "relation": "current"});
  var mutation: any;
  for (mutation of py.iter(py.slice(mutations, null, 1000))) {
    py.listAppend(lineage, {"id": `${py.toStr(py.get(mutation, "kind", ""))}:${py.toStr(py.get(mutation, "target", ""))}`, "relation": "mutation", "ancestor": evolution_id});
  }
  return py.sorted(lineage, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any});
}

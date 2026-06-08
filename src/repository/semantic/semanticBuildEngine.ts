/**
 * Converted from Python: core/repository/semantic/semantic_build_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function inferSemanticBuildGraph(package_managers: any): any {
  var nodes: any = py.sorted(py.toSet(py.or2(package_managers, () => ([]))));
  var edges: any[] = [];
  var i: any;
  for (i = 0; i < py.sub(py.len(nodes), 1); i++) {
    py.listAppend(edges, {"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1))});
  }
  return {"nodes": nodes, "edges": edges};
}

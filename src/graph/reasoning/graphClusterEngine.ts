/**
 * Converted from Python: core/graph/reasoning/graph_cluster_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { nodeIds } from "./_helpers.js";

export function graphCluster(graph: any): any {
  var groups: Record<string, any> = {};
  var n: any;
  for (n of py.iter(nodeIds(graph))) {
    var key: any = (py.contains(n, "/") ? py.at(py.split(n, "/"), 0) : py.at(py.split(n, "."), 0));
    py.listAppend(py.setdefault(groups, key, []), n);
  }
  return {"clusters": py.iter(py.sorted(py.items(groups))).map(([k, v]: any) => ({"id": k, "nodes": py.sorted(v)}))};
}
export { nodeIds };

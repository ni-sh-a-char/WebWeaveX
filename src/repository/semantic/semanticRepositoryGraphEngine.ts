/**
 * Converted from Python: core/repository/semantic/semantic_repository_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildSemanticRepositoryGraph(parts: any): any {
  var p: any = py.or2(parts, () => ({}));
  var nodes: Set<any> = new Set();
  var key: any;
  for (key of py.iter(["symbols", "frameworks", "dependencies", "services", "routes"])) {
    var values: any = py.get(p, key, []);
    if (((values !== null && typeof values === "object" && !Array.isArray(values) && !(values instanceof Set) && !(values instanceof Map)))) {
      values = [...py.iter(py.values(values))];
    }
    if ((Array.isArray(values))) {
      var v: any;
      for (v of py.iter(values)) {
        if ((typeof v === "string")) {
          py.setAdd(nodes, v);
        }
      }
    }
  }
  var ordered_nodes: any = py.sorted(nodes);
  var edges: any = py.range(py.max([0, py.sub(py.len(ordered_nodes), 1)])).map((i: any) => ({"from": py.at(ordered_nodes, i), "to": py.at(ordered_nodes, py.add(i, 1))}));
  return {"nodes": ordered_nodes, "edges": edges};
}

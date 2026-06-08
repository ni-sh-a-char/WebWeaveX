/**
 * Converted from Python: core/graph/graph_reconciliation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructGraph } from "./graphReconstructionEngine.js";

export function reconcileGraphs(...graphs: any[]): any {
  var merged_nodes: any[] = [];
  var merged_edges: any[] = [];
  var seen_edges: Set<any> = new Set();
  var g: any;
  for (g of py.iter(graphs)) {
    if (!((g !== null && typeof g === "object" && !Array.isArray(g) && !(g instanceof Set) && !(g instanceof Map)))) {
      continue;
    }
    py.extend(merged_nodes, py.or2(py.get(g, "nodes", []), () => ([])));
    var e: any;
    for (e of py.iter(py.or2(py.get(g, "edges", []), () => ([])))) {
      if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
        continue;
      }
      var key: any = [py.toStr(py.get(e, "from", "")), py.toStr(py.get(e, "to", ""))];
      if (py.contains(seen_edges, key)) {
        continue;
      }
      py.setAdd(seen_edges, key);
      py.listAppend(merged_edges, {"from": py.at(key, 0), "to": py.at(key, 1)});
    }
  }
  return reconstructGraph({"nodes": merged_nodes, "edges": merged_edges});
}
export { reconstructGraph };

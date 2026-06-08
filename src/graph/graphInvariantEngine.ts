/**
 * Converted from Python: core/graph/graph_invariant_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function checkGraphInvariants(graph: any): any {
  var nodes: any = py.or2(py.get(graph, "nodes", []), () => ([]));
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var node_ids: any = py.toSet(py.iter(nodes).filter((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.truthy(py.get(n, "id")))).map((n: any) => py.get(n, "id")));
  var violations: any[] = [];
  var e: any;
  for (e of py.iter(edges)) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    if (py.contains(e, "type")) {
      py.listAppend(violations, {"rule": "no_edge_type", "edge": py.toStr(py.get(e, "from"))});
    }
    if ((!py.contains(node_ids, py.get(e, "from")) || !py.contains(node_ids, py.get(e, "to")))) {
      if (py.truthy(node_ids)) {
        py.listAppend(violations, {"rule": "dangling_edge", "from": py.toStr(py.get(e, "from")), "to": py.toStr(py.get(e, "to"))});
      }
    }
  }
  return {"valid": py.eq(py.len(violations), 0), "violations": violations, "node_count": py.len(nodes), "edge_count": py.len(edges), "deterministic_inputs": [`violations=${py.toStr(py.len(violations))}`]};
}

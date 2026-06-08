/**
 * Converted from Python: core/typed_ir/typed_topology_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildDistributedTopology } from "../runtime/distributedTopologyEngine.js";
import { SemanticNode, SemanticEdge } from "./schemaTypes.js";

export function compileTypedTopologyIr(services: any): any {
  var topo: any = buildDistributedTopology(py.sorted(services));
  var nodes: any[] = [];
  var edges: any[] = [];
  var n: any;
  for (n of py.iter(py.get(topo, "nodes", []))) {
    py.listAppend(nodes, new SemanticNode(py.toStr(py.get(n, "id", "")), py.toStr(py.get(n, "type", "service"))));
  }
  var e: any;
  for (e of py.iter(py.get(topo, "edges", []))) {
    py.listAppend(edges, new SemanticEdge(py.toStr(py.get(e, "from", "")), py.toStr(py.get(e, "to", "")), py.toStr(py.get(e, "relation", "distributed_dependency")), ["distributed_topology"]));
  }
  return {"nodes": nodes, "edges": edges, "topology": topo, "typed": true, "deterministic": true};
}
export { SemanticEdge, SemanticNode, buildDistributedTopology };

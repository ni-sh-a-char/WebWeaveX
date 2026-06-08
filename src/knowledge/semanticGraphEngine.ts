/**
 * Converted from Python: core/knowledge/semantic_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSemanticGraph(parts: any): any {
  var nodes: any = py.sorted(py.toSet(py.get(parts, "nodes", [])));
  var edges: any = py.sorted(py.toSet(py.iter(py.get(parts, "edges", [])).filter((e: any) => (((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "from")) && py.truthy(py.get(e, "to")))).map((e: any) => [py.get(e, "from", ""), py.get(e, "to", "")])));
  return {"nodes": nodes, "edges": py.iter(edges).map(([f, t]: any) => ({"from": f, "to": t}))};
}

/**
 * Converted from Python: core/graph/graph_entropy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelGraphEntropy(graph: any): any {
  var nodes: any = py.or2(py.get(graph, "nodes", []), () => ([]));
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var kinds: any = py.toSet(py.iter(nodes).filter((n: any) => ((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map)))).map((n: any) => py.get(n, "kind")));
  var entropy: any = py.round(py.min([py.F(1.0), py.add(py.add(py.mul(py.len(nodes), py.F(0.02)), py.mul(py.len(edges), py.F(0.03))), py.mul(py.len(kinds), py.F(0.05)))]), 3);
  return {"entropy": entropy, "kind_diversity": py.len(kinds), "deterministic_inputs": [`H=${py.floatStr(entropy)}`]};
}

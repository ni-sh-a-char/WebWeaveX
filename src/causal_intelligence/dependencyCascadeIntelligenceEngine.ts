/**
 * Converted from Python: core/causal_intelligence/dependency_cascade_intelligence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CASCADE: any = 10000;
export function analyzeDependencyCascade(runtime_ir: any): any {
  var graph: any = py.get(runtime_ir, "runtime_causality_graph", {});
  var edges: any = py.slice([...py.iter(py.get(graph, "edges", []))], null, MAX_CASCADE);
  var cascade: any = py.enumerate(edges).map(([idx, edge]: any) => ({"from": py.get(edge, "from"), "to": py.get(edge, "to"), "depth": idx}));
  return {"cascade": cascade, "cascade_length": py.len(cascade), "bounded": true};
}

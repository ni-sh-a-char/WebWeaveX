/**
 * Converted from Python: core/knowledge/execution_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildExecutionFlow(calls: any): any {
  var pairs: any = py.sorted(py.toSet(py.iter(py.or2(calls, () => ([]))).filter((c: any) => ((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map)))).map((c: any) => [py.get(c, "from", ""), py.get(c, "to", "")])));
  var edges: any = py.iter(pairs).filter(([f, t]: any) => (py.truthy(f) && py.truthy(t))).map(([f, t]: any) => ({"from": f, "to": t}));
  var nodes: any = py.sorted(py.toSet(py.iter(edges).flatMap((e: any) => py.iter([py.at(e, "from"), py.at(e, "to")]).map((x: any) => x))));
  return {"nodes": nodes, "edges": edges};
}

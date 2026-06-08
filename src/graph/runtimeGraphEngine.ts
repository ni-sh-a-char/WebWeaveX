/**
 * Converted from Python: core/graph/runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeGraph(runtime_hints: any): any {
  var runtimes: any = (((runtime_hints !== null && typeof runtime_hints === "object" && !Array.isArray(runtime_hints) && !(runtime_hints instanceof Set) && !(runtime_hints instanceof Map))) ? py.get(runtime_hints, "runtimes", []) : []);
  var frameworks: any = (((runtime_hints !== null && typeof runtime_hints === "object" && !Array.isArray(runtime_hints) && !(runtime_hints instanceof Set) && !(runtime_hints instanceof Map))) ? py.get(runtime_hints, "frameworks", []) : []);
  var nodes: any = py.iter(py.sorted(py.toSet(py.iter(runtimes).map((r: any) => py.toStr(r))))).map((r: any) => ({"id": r, "kind": "runtime", "metadata": {}}));
  var edges: any[] = [];
  var fw: any;
  for (fw of py.iter(py.sorted(py.toSet(py.iter(frameworks).map((f: any) => py.toStr(f)))))) {
    py.listAppend(nodes, {"id": fw, "kind": "framework", "metadata": {}});
    if (py.truthy(runtimes)) {
      py.listAppend(edges, {"from": py.toStr(py.at(runtimes, 0)), "to": fw});
    }
  }
  return {"nodes": nodes, "edges": edges, "max_edges": py.len(edges)};
}

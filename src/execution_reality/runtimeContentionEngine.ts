/**
 * Converted from Python: core/execution_reality/runtime_contention_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_HOTSPOTS: any = 1000;
export function analyzeRuntimeContention(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var edges: any = [...py.iter(py.get(topology, "edges", []))];
  var contention: Record<string, any> = {};
  var edge: any;
  for (edge of py.iter(edges)) {
    var target: any = py.toStr(py.get(edge, "to"));
    py.setItem(contention, target, py.add(py.get(contention, target, 0), 1));
  }
  return {"contention": py.pyDict(py.sorted(py.items(contention))), "hotspots": py.slice(py.sorted(py.keys(contention)), null, MAX_HOTSPOTS)};
}

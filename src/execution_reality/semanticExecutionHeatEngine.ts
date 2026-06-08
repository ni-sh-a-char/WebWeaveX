/**
 * Converted from Python: core/execution_reality/semantic_execution_heat_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_HEATMAP: any = 1000;
export function computeExecutionHeat(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var nodes: any = py.get(topology, "nodes", []);
  var heat: any[] = [];
  var idx: any;
  var node: any;
  for ([idx, node] of py.enumerate(py.sorted(nodes, {key: ((x: any) => py.toStr(py.get(x, "id"))) as (item: any) => any}))) {
    py.listAppend(heat, {"node": py.get(node, "id"), "heat": py.add(idx, 1)});
  }
  return {"heatmap": py.slice(heat, null, MAX_HEATMAP)};
}

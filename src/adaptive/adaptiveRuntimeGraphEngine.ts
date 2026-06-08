/**
 * Converted from Python: core/adaptive/adaptive_runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildAdaptiveRuntimeGraph(adaptation: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var fallback: any = py.get(py.get(adaptation, "fallback", {}), "chain", []);
  var step: any;
  for (step of py.iter(fallback)) {
    var node_id: any = `fallback_${py.toStr(py.get(step, "step", 0))}`;
    py.listAppend(nodes, {"id": node_id, "type": "fallback", "strategy": py.get(step, "strategy")});
    var step_index: any = py.toInt(py.get(step, "step", 0));
    if ((step_index > 0)) {
      py.listAppend(edges, {"from": `fallback_${py.toStr(py.sub(step_index, 1))}`, "to": node_id, "relation": "fallback_next"});
    }
  }
  return {"ir": "adaptive_runtime_graph", "nodes": nodes, "edges": edges, "bounded": true};
}

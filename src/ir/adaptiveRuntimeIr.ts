/**
 * Converted from Python: core/ir/adaptive_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileAdaptiveRuntimeIr(adaptation: any, memory: any, schema: any, reconciliation: any, snapshot: any): any {
  return {"ir": "adaptive_runtime", "healed_selectors": py.get(memory, "healed_selectors", {}), "fallback_chains": py.get(adaptation, "fallback", {}), "adaptation_history": {"modal_recovery": py.get(adaptation, "modal_recovery", {}), "pagination_recovery": py.get(adaptation, "pagination_recovery", {}), "interaction_recovery": py.get(adaptation, "interaction_recovery", {})}, "schema_stabilization": schema, "runtime_reconciliation": reconciliation, "snapshot": snapshot, "bounded": true};
}
export function adaptiveRuntimeIrToGraph(adaptive_ir: any): any {
  var chain: any = py.get(py.get(adaptive_ir, "fallback_chains", {}), "chain", []);
  var nodes: any[] = [];
  var edges: any[] = [];
  var step: any;
  for (step of py.iter(chain)) {
    var node_id: any = `adaptive:${py.toStr(py.get(step, "step", 0))}`;
    py.listAppend(nodes, {"id": node_id, "type": "adaptive_fallback", "name": py.get(step, "strategy", "")});
  }
  var index: any;
  for (index = 0; index < py.sub(py.len(chain), 1); index++) {
    py.listAppend(edges, {"from": `adaptive:${py.toStr(index)}`, "to": `adaptive:${py.toStr(py.add(index, 1))}`, "relation": "fallback_next"});
  }
  return {"ir": "adaptive_runtime_graph", "nodes": nodes, "edges": edges, "bounded": true};
}

/**
 * Converted from Python: core/compiler/semantic_execution_planner.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSemanticExecutionPlan(ir: any): any {
  var edges: any = [...py.iter(py.get(ir, "optimized_edges", []))];
  var ordered: any = py.sorted(edges, {key: ((x: any) => [py.toStr(py.get(x, "source")), py.toStr(py.get(x, "target"))]) as (item: any) => any});
  var plan: any[] = [];
  var idx: any;
  var edge: any;
  for ([idx, edge] of py.enumerate(ordered)) {
    py.listAppend(plan, {"step": idx, "action": "LINK", "source": py.get(edge, "source"), "target": py.get(edge, "target")});
  }
  return {"plan": plan, "steps": py.len(plan), "deterministic": true};
}

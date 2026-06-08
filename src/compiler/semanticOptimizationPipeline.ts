/**
 * Converted from Python: core/compiler/semantic_optimization_pipeline.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_OPT_PASSES: any = 10;
export function optimizeSemanticPipeline(ir: any): any {
  var edges: any = [...py.iter(py.get(ir, "lowered_edges", []))];
  var optimized: any[] = [];
  var seen: Set<any> = new Set();
  var edge: any;
  for (edge of py.iter(edges)) {
    var key: any = [py.toStr(py.get(edge, "source")), py.toStr(py.get(edge, "target")), py.toStr(py.get(edge, "relationship"))];
    if (py.contains(seen, key)) {
      continue;
    }
    py.setAdd(seen, key);
    py.listAppend(optimized, edge);
  }
  return {"optimized_edges": optimized, "optimization_passes": 1, "deterministic": true};
}

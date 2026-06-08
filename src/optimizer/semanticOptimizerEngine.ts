/**
 * Converted from Python: core/optimizer/semantic_optimizer_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_OPTIMIZATION_PASSES: any = 10;
export function optimizeSemanticIr(ir: any): any {
  var optimizations: any[] = [];
  if (py.contains(ir, "execution_paths")) {
    var paths: any = py.get(py.at(ir, "execution_paths"), "paths", []);
    var deduped: any[] = [];
    var seen: Set<any> = new Set();
    var p: any;
    for (p of py.iter(paths)) {
      var key: any = [...py.iter(p)];
      if (!py.contains(seen, key)) {
        py.listAppend(deduped, p);
        py.setAdd(seen, key);
      }
    }
    py.listAppend(optimizations, {"type": "deduplicate_execution_paths", "before": py.len(paths), "after": py.len(deduped)});
    py.setItem(py.at(ir, "execution_paths"), "paths", deduped);
  }
  return {"optimized_ir": ir, "optimizations": py.slice(optimizations, null, MAX_OPTIMIZATION_PASSES), "deterministic": true};
}

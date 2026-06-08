/**
 * Converted from Python: core/world_model/semantic_impact_analysis_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function analyzeSemanticImpact(target_file: any, graph: any): any {
  var affected: any[] = [];
  var edge: any;
  for (edge of py.iter(py.get(graph, "edges", []))) {
    if (py.eq(py.get(edge, "to"), target_file)) {
      py.listAppend(affected, py.get(edge, "from"));
    }
  }
  return {"target": target_file, "affected": py.sorted(affected), "impact_size": py.len(affected)};
}

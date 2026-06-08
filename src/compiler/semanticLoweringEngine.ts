/**
 * Converted from Python: core/compiler/semantic_lowering_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_LOWERED_EDGES: any = 10000;
export function lowerSemanticIr(ir: any): any {
  var edges: any = py.slice([...py.iter(py.get(ir, "edges", []))], null, MAX_LOWERED_EDGES);
  var lowered: any[] = [];
  var edge: any;
  for (edge of py.iter(edges)) {
    py.listAppend(lowered, {"source": py.get(edge, "from"), "target": py.get(edge, "to"), "relationship": py.get(edge, "type", "semantic_link")});
  }
  return {"lowered_edges": lowered, "bounded": true, "count": py.len(lowered)};
}

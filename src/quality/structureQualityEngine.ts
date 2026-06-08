/**
 * Converted from Python: core/quality/structure_quality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function scoreStructureQuality(graph: any): any {
  var n: any = py.len(py.get(py.or2(graph, () => ({})), "nodes", []));
  var e: any = py.len(py.get(py.or2(graph, () => ({})), "edges", []));
  if (py.eq(n, 0)) {
    return {"score": py.F(0.0)};
  }
  return {"score": py.round(py.min([py.F(1.0), py.div(e, py.max([1, py.mul(n, 2)]))]), 6)};
}

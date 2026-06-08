/**
 * Converted from Python: core/intelligence/complexity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeComplexity(nodes: any, edges: any): any {
  var n: any = py.len(nodes);
  var e: any = py.len(edges);
  if (py.eq(n, 0)) {
    return py.F(0.0);
  }
  return py.min([py.F(1.0), py.div(e, py.add(py.mul(n, n), 1))]);
}

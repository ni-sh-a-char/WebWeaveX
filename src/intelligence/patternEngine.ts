/**
 * Converted from Python: core/intelligence/pattern_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectPatterns(analysis: any): any {
  var signals: any[] = [];
  var density: any = py.get(analysis, "density", 0);
  var n: any = py.get(analysis, "node_count", 0);
  var e: any = py.get(analysis, "edge_count", 0);
  if (((py.F(0.3) < density) && (density < py.F(0.8)))) {
    py.listAppend(signals, "balanced_graph");
  }
  if ((density >= py.F(0.8))) {
    py.listAppend(signals, "dense_graph");
  }
  if ((n >= 10)) {
    py.listAppend(signals, "large_graph");
  }
  if (py.lt(e, n)) {
    py.listAppend(signals, "sparse_graph");
  }
  return py.sorted(signals);
}

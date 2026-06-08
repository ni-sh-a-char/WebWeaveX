/**
 * Converted from Python: core/quality/extraction_score_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function scoreExtraction(result: any): any {
  var txt: any = py.or2(py.get(result, "raw_text", ""), () => (""));
  var edges: any = py.get(py.get(py.get(result, "relationships", {}), "execution_graph", {}), "edges", []);
  return {"score": py.round(py.min([py.F(1.0), py.add(py.div(py.len(txt), py.F(5000.0)), py.div(py.len(edges), py.F(1000.0)))]), 6)};
}

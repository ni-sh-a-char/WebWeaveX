/**
 * Converted from Python: core/quality/semantic_confidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function scoreSemanticConfidence(result: any): any {
  var has_repo: any = py.truthy(py.get(py.get(result, "content", {}), "repository"));
  var has_docs: any = py.truthy(py.get(py.get(result, "content", {}), "documents"));
  var has_graph: any = py.truthy(py.get(py.get(py.get(result, "relationships", {}), "execution_graph", {}), "edges", []));
  var score: any = py.add(py.add((py.truthy(has_repo) ? 1 : 0), (py.truthy(has_docs) ? 1 : 0)), (py.truthy(has_graph) ? 1 : 0));
  return {"confidence": py.round(py.div(score, py.F(3.0)), 6)};
}

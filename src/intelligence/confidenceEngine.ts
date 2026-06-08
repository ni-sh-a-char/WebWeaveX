/**
 * Converted from Python: core/intelligence/confidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _ratio(num: any, den: any): any {
  if ((den <= 0)) {
    return py.F(0.0);
  }
  return py.max([py.F(0.0), py.min([py.F(1.0), py.div(num, den)])]);
}
export function computeConfidence(result: any): any {
  var content: any = py.get(result, "content", {});
  var deps: any = py.get(result, "dependencies", {});
  var rel: any = py.get(result, "relationships", {});
  var meta: any = py.get(result, "metadata", {});
  var completeness: any = (py.truthy(py.get(result, "raw_text", "")) ? py.F(1.0) : py.F(0.0));
  var metadata_score: any = _ratio(py.len(py.items(meta).filter(([k, v]: any) => !py.contains([null, "", {}, []], v)).map(([k, v]: any) => k)), py.max([py.len(meta), 1]));
  var dep_score: any = (py.truthy(py.get(deps, "packages")) ? py.F(1.0) : py.F(0.5));
  var graph_score: any = (py.truthy(rel) ? py.F(1.0) : py.F(0.5));
  var consistency: any = ((((content !== null && typeof content === "object" && !Array.isArray(content) && !(content instanceof Set) && !(content instanceof Map))) && ((deps !== null && typeof deps === "object" && !Array.isArray(deps) && !(deps instanceof Set) && !(deps instanceof Map))) && ((rel !== null && typeof rel === "object" && !Array.isArray(rel) && !(rel instanceof Set) && !(rel instanceof Map)))) ? py.F(1.0) : py.F(0.0));
  var score: any = py.add(py.add(py.add(py.add(py.mul(py.F(0.25), completeness), py.mul(py.F(0.2), metadata_score)), py.mul(py.F(0.2), dep_score)), py.mul(py.F(0.2), graph_score)), py.mul(py.F(0.15), consistency));
  return py.round(py.max([py.F(0.0), py.min([py.F(1.0), score])]), 6);
}

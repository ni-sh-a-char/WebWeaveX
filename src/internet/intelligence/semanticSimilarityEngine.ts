/**
 * Converted from Python: core/internet/intelligence/semantic_similarity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function semanticSimilarity(a: any, b: any): any {
  var sa: any = py.toSet(py.split(String(py.or2(a, () => (""))).toLowerCase()));
  var sb: any = py.toSet(py.split(String(py.or2(b, () => (""))).toLowerCase()));
  if ((!py.truthy(sa) && !py.truthy(sb))) {
    return {"score": py.F(1.0)};
  }
  return {"score": py.round(py.div(py.len(py.bitand(sa, sb)), py.max([1, py.len(py.bitor(sa, sb))])), 6)};
}

/**
 * Converted from Python: core/graph/reasoning/graph_similarity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { nodeIds } from "./_helpers.js";

export function graphSimilarity(a: any, b: any): any {
  var an: any = py.toSet(nodeIds(a));
  var bn: any = py.toSet(nodeIds(b));
  var ae: any = py.toSet(py.iter(py.get(py.or2(a, () => ({})), "edges", [])).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => [py.get(e, "from"), py.get(e, "to")]));
  var be: any = py.toSet(py.iter(py.get(py.or2(b, () => ({})), "edges", [])).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => [py.get(e, "from"), py.get(e, "to")]));
  var ns: any = (!py.truthy(py.bitor(an, bn)) ? py.F(1.0) : py.div(py.len(py.bitand(an, bn)), py.len(py.bitor(an, bn))));
  var es: any = (!py.truthy(py.bitor(ae, be)) ? py.F(1.0) : py.div(py.len(py.bitand(ae, be)), py.len(py.bitor(ae, be))));
  return {"node": ns, "edge": es, "score": py.round(py.div(py.add(ns, es), 2), 6)};
}
export { nodeIds };

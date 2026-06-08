/**
 * Converted from Python: core/graph/reasoning/graph_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function graphDiff(a: any, b: any): any {
  var ae: any = py.toSet(py.iter(py.get(py.or2(a, () => ({})), "edges", [])).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => [py.get(e, "from"), py.get(e, "to")]));
  var be: any = py.toSet(py.iter(py.get(py.or2(b, () => ({})), "edges", [])).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => [py.get(e, "from"), py.get(e, "to")]));
  return {"added_edges": py.iter(py.sorted(py.sub(be, ae))).map(([f, t]: any) => ({"from": f, "to": t})), "removed_edges": py.iter(py.sorted(py.sub(ae, be))).map(([f, t]: any) => ({"from": f, "to": t}))};
}

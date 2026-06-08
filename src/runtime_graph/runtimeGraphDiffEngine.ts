/**
 * Converted from Python: core/runtime_graph/runtime_graph_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffRuntimeGraphs(left: any, right: any): any {
  var left_ids: any = py.toSet(py.iter(py.get(left, "nodes", [])).map((x: any) => py.toStr(py.get(x, "id", ""))));
  var right_ids: any = py.toSet(py.iter(py.get(right, "nodes", [])).map((x: any) => py.toStr(py.get(x, "id", ""))));
  var added: any = py.sorted(py.sub(right_ids, left_ids));
  var removed: any = py.sorted(py.sub(left_ids, right_ids));
  return {"added_nodes": added, "removed_nodes": removed, "bounded": true};
}

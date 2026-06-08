/**
 * Converted from Python: core/graph/reasoning/_helpers.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function nodeIds(graph: any): any {
  var ids: any[] = [];
  var raw: any;
  for (raw of py.iter(py.or2(py.get(py.or2(graph, () => ({})), "nodes", []), () => ([])))) {
    if (((raw !== null && typeof raw === "object" && !Array.isArray(raw) && !(raw instanceof Set) && !(raw instanceof Map)))) {
      var nid: any = py.strip(py.toStr(py.get(raw, "id", "")));
    } else {
      nid = py.strip(py.toStr(py.or2(raw, () => (""))));
    }
    if (py.truthy(nid)) {
      py.listAppend(ids, nid);
    }
  }
  return py.sorted(py.toSet(ids));
}

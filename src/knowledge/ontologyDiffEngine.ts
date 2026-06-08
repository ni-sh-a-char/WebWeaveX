/**
 * Converted from Python: core/knowledge/ontology_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffOntologyEdges(before: any, after: any): any {
  function key(e: any): any {
    return [py.get(e, "from"), py.get(e, "to")];
  }
  var bk: any = py.toSet(py.iter(before).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => key(e)));
  var ak: any = py.toSet(py.iter(after).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => key(e)));
  return {"added": py.len(py.sub(ak, bk)), "removed": py.len(py.sub(bk, ak)), "stable": py.len(py.bitand(bk, ak))};
}

/**
 * Converted from Python: core/documents/tutorial_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructTutorialCausality(sections: any): any {
  var edges: any[] = [];
  var ordered: any = py.sorted(sections, {key: ((s: any) => py.toInt(py.get(s, "order", 0))) as (item: any) => any});
  var idx: any;
  for (idx = 1; idx < py.len(ordered); idx++) {
    var previous: any = py.at(ordered, py.sub(idx, 1));
    var current: any = py.at(ordered, idx);
    py.listAppend(edges, {"from": py.get(previous, "id"), "to": py.get(current, "id"), "metadata": {"kind": "tutorial_prerequisite", "basis": "document_order"}});
  }
  return {"tutorial_edges": edges, "count": py.len(edges), "deterministic": true};
}

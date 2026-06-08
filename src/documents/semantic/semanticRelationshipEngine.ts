/**
 * Converted from Python: core/documents/semantic/semantic_relationship_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildSemanticRelationships(sections: any, references: any): any {
  var sec: any = py.sorted(py.toSet(py.or2(sections, () => ([]))));
  var ref: any = py.sorted(py.toSet(py.or2(references, () => ([]))));
  var edges: any = py.iter(sec).flatMap((s: any) => py.iter(py.slice(ref, null, 5)).map((r: any) => ({"from": s, "to": r})));
  return {"nodes": py.sorted(py.toSet(py.add(sec, ref))), "edges": py.sorted(edges, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any})};
}

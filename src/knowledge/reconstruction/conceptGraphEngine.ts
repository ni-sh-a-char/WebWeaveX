/**
 * Converted from Python: core/knowledge/reconstruction/concept_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildConceptGraph(concepts: any): any {
  var c: any = py.sorted(py.toSet(py.or2(concepts, () => ([]))));
  return {"nodes": c, "edges": py.range(py.max([0, py.sub(py.len(c), 1)])).map((i: any) => ({"from": py.at(c, i), "to": py.at(c, py.add(i, 1))}))};
}

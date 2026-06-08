/**
 * Converted from Python: core/documents/reconstruction/concept_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildConceptGraph(text: any): any {
  var concepts: any = py.sorted(py.toSet(py.reFindall("`([^`]+)`", py.or2(text, () => ("")), "")));
  var edges: any = py.range(py.max([0, py.sub(py.len(concepts), 1)])).map((i: any) => ({"from": py.at(concepts, i), "to": py.at(concepts, py.add(i, 1))}));
  return {"nodes": concepts, "edges": edges};
}

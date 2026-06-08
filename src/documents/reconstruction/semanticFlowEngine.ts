/**
 * Converted from Python: core/documents/reconstruction/semantic_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildSemanticFlow(text: any): any {
  var headings: any = py.iter(py.reFinditer("^#{1,6}\\s+(.+)$", py.or2(text, () => ("")), "m")).map((m: any) => py.strip(m.group(1)));
  var edges: any = py.range(py.max([0, py.sub(py.len(headings), 1)])).map((i: any) => ({"from": py.at(headings, i), "to": py.at(headings, py.add(i, 1))}));
  return {"nodes": headings, "edges": edges};
}

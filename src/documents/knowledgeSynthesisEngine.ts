/**
 * Converted from Python: core/documents/knowledge_synthesis_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function synthesizeKnowledge(parts: any): any {
  var nodes: any = py.sorted(py.keys(py.or2(parts, () => ({}))));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1))}));
  return {"nodes": nodes, "edges": edges};
}

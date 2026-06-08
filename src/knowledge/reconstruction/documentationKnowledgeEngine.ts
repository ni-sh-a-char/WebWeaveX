/**
 * Converted from Python: core/knowledge/reconstruction/documentation_knowledge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildDocumentationKnowledge(docs: any): any {
  var sections: any = py.iter(py.get(docs, "sections", [])).map((s: any) => py.toStr(s));
  var refs_raw: any = py.get(docs, "references", []);
  var refs: any[] = [];
  var r: any;
  for (r of py.iter(refs_raw)) {
    if (((r !== null && typeof r === "object" && !Array.isArray(r) && !(r instanceof Set) && !(r instanceof Map)))) {
      py.listAppend(refs, py.strip(`${py.toStr(py.get(r, "method", ""))} ${py.toStr(py.get(r, "path", ""))}`));
    } else {
      py.listAppend(refs, py.toStr(r));
    }
  }
  var nodes: any = py.sorted(py.toSet(py.iter(py.add(sections, refs)).filter((x: any) => py.truthy(x)).map((x: any) => x)));
  var edges: any = py.iter(nodes).map((n: any) => ({"from": "doc", "to": n}));
  return {"nodes": nodes, "edges": edges};
}

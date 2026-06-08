/**
 * Converted from Python: core/documents/concept_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractSections } from "./sectionEngine.js";
import { structureCognition } from "../evidence/index.js";
import { parseSource } from "../parsers/index.js";

export function buildConceptDependencies(text: any, path: any = ""): any {
  var sections: any = extractSections(py.or2(text, () => ("")));
  var hierarchy: any = py.get(sections, "hierarchy", []);
  var lexical: any = {"sections": py.get(sections, "sections", []), "hierarchy": hierarchy};
  var discourse: any = {"headings": py.iter(hierarchy).map((h: any) => py.get(h, "title", "")), "flow_edges": py.range(py.max([0, py.sub(py.len(hierarchy), 1)])).filter((i: any) => (py.truthy(py.get(py.at(hierarchy, i), "title")) && py.truthy(py.get(py.at(hierarchy, py.add(i, 1)), "title")))).map((i: any) => ({"from": py.get(py.at(hierarchy, i), "title", ""), "to": py.get(py.at(hierarchy, py.add(i, 1)), "title", "")}))};
  var concepts: any = py.iter(hierarchy).filter((h: any) => py.truthy(py.get(h, "title"))).map((h: any) => py.get(h, "title", ""));
  var parsed: any = null;
  if ((!py.truthy(concepts) && py.truthy(py.endswith(path, [".py", ".js", ".ts", ".go", ".rs", ".java", ".kt", ".dart"])))) {
    parsed = parseSource(py.or2(text, () => ("")), path);
    var sym: any = py.get(parsed, "symbols", []);
    if ((Array.isArray(sym))) {
      concepts = py.slice(sym, null, 20);
    } else {
      concepts = (((sym !== null && typeof sym === "object" && !Array.isArray(sym) && !(sym instanceof Set) && !(sym instanceof Map))) ? [...py.iter(py.slice(py.get(sym, "classes", []), null, 20))] : []);
    }
  }
  concepts = py.sorted(py.toSet(py.iter(concepts).filter((c: any) => py.truthy(c)).map((c: any) => c)));
  var conceptual: any = {"concepts": concepts, "edges": py.range(py.max([0, py.sub(py.len(concepts), 1)])).map((i: any) => ({"from": py.at(concepts, i), "to": py.at(concepts, py.add(i, 1))}))};
  var semantic: any = {"concepts": concepts};
  var observed: any = {"lexical": lexical, "syntactic": {"hierarchy": hierarchy}, "discourse": discourse};
  var inferred: any = {"semantic": semantic, "conceptual": conceptual};
  var reconciled: any = {"concepts": concepts, "edges": py.at(conceptual, "edges"), "discourse": discourse};
  var out: any = structureCognition(observed, inferred, reconciled, parsed);
  py.setItem(out, "concepts", py.get(reconciled, "concepts", []));
  py.setItem(out, "edges", py.get(reconciled, "edges", []));
  return out;
}
export { extractSections, parseSource, structureCognition };

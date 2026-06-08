/**
 * Converted from Python: core/documents/semantic_section_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractSections } from "./sectionEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructSemanticSections(text: any): any {
  var sections: any = extractSections(py.or2(text, () => ("")));
  var hierarchy: any = py.get(sections, "hierarchy", []);
  var lexical: any = {"sections": py.get(sections, "sections", []), "titles": py.iter(hierarchy).map((h: any) => py.get(h, "title", ""))};
  var syntactic: any = {"levels": py.iter(hierarchy).map((h: any) => py.get(h, "level", 1)), "depth": py.max(py.iter(hierarchy).map((h: any) => py.get(h, "level", 1)), {dflt: 0, hasDefault: true})};
  var semantic: any = {"introduces": py.iter(hierarchy).filter((h: any) => py.eq(py.get(h, "level", 1), 1)).map((h: any) => py.at(h, "title")), "explains": py.range(py.max([0, py.sub(py.len(hierarchy), 1)])).filter((i: any) => (py.truthy(py.get(py.at(hierarchy, i), "title")) && py.truthy(py.get(py.at(hierarchy, py.add(i, 1)), "title")))).map((i: any) => ({"from": py.get(py.at(hierarchy, i), "title", ""), "to": py.get(py.at(hierarchy, py.add(i, 1)), "title", "")}))};
  var discourse: any = {"flow": py.at(semantic, "explains")};
  var conceptual: any = {"dependencies": py.at(semantic, "explains")};
  var observed: any = {"lexical": lexical, "syntactic": syntactic};
  var inferred: any = {"semantic": semantic, "discourse": discourse, "conceptual": conceptual};
  var reconciled: any = {"sections": hierarchy, "structure": semantic};
  return structureCognition(observed, inferred, reconciled, null);
}
export { extractSections, structureCognition };

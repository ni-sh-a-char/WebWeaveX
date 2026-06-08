/**
 * Converted from Python: core/documents/discourse_structure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractSections } from "./sectionEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructDiscourse(text: any): any {
  var sections: any = extractSections(py.or2(text, () => ("")));
  var hierarchy: any = py.get(sections, "hierarchy", []);
  var lexical: any = {"sections": py.get(sections, "sections", []), "heading_count": py.len(hierarchy)};
  var syntactic: any = {"hierarchy_depth": py.max(py.iter(hierarchy).map((h: any) => py.get(h, "level", 1)), {dflt: 0, hasDefault: true})};
  var discourse: any = {"introduces": py.iter(hierarchy).filter((h: any) => (py.get(h, "level", 1) <= 2)).map((h: any) => py.get(h, "title", "")), "extends": py.range(py.max([0, py.sub(py.len(hierarchy), 1)])).filter((i: any) => (py.truthy(py.get(py.at(hierarchy, i), "title")) && py.truthy(py.get(py.at(hierarchy, py.add(i, 1)), "title")))).map((i: any) => ({"from": py.get(py.at(hierarchy, i), "title", ""), "to": py.get(py.at(hierarchy, py.add(i, 1)), "title", "")}))};
  var observed: any = {"lexical": lexical, "syntactic": syntactic};
  var inferred: any = {"discourse": discourse};
  var reconciled: any = {"structure": discourse, "sections": hierarchy};
  return structureCognition(observed, inferred, reconciled, null);
}
export { extractSections, structureCognition };

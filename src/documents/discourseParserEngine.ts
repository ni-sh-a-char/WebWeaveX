/**
 * Converted from Python: core/documents/discourse_parser_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractSections } from "./sectionEngine.js";

export function parseDiscourseStructure(text: any): any {
  var sections: any = extractSections(py.or2(text, () => ("")));
  var hierarchy: any = py.get(sections, "hierarchy", []);
  return {"lexical": {"section_count": py.len(py.get(sections, "sections", []))}, "syntactic": {"max_depth": py.max(py.iter(hierarchy).map((h: any) => py.get(h, "level", 1)), {dflt: 0, hasDefault: true})}, "discourse": {"headings": py.iter(py.slice(hierarchy, null, 50)).map((h: any) => py.get(h, "title", ""))}, "conceptual": {"nodes": py.len(hierarchy)}};
}
export { extractSections };

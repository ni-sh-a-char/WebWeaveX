/**
 * Converted from Python: core/documents/semantic_section_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractSections } from "./sectionEngine.js";

export function extractSemanticSections(text: any): any {
  var sections: any = extractSections(py.or2(text, () => ("")));
  return {"sections": py.get(sections, "sections", []), "hierarchy": py.get(sections, "hierarchy", []), "count": py.len(py.get(sections, "sections", [])), "evidence": "section_structure"};
}
export { extractSections };

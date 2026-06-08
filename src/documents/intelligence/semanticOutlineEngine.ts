/**
 * Converted from Python: core/documents/intelligence/semantic_outline_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { extractSections } from "../sectionEngine.js";

export function extractSemanticOutline(text: any): any {
  var s: any = extractSections(text);
  return {"sections": py.get(s, "sections", []), "hierarchy": py.get(s, "hierarchy", [])};
}
export { extractSections };

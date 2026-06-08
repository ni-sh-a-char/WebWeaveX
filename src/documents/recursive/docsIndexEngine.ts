/**
 * Converted from Python: core/documents/recursive/docs_index_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { extractSections } from "../sectionEngine.js";

export function buildDocsIndex(text: any): any {
  var sec: any = extractSections(text);
  return {"index": py.get(sec, "sections", [])};
}
export { extractSections };

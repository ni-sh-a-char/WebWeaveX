/**
 * Converted from Python: core/documents/intelligence/cross_reference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { extractReferences } from "../referenceEngine.js";

export function extractCrossRefs(text: any): any {
  var refs: any = extractReferences(text);
  return {"cross_links": py.sorted(py.toSet(py.add(py.get(refs, "internal_links", []), py.get(refs, "repo_references", []))))};
}
export { extractReferences };

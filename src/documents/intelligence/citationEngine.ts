/**
 * Converted from Python: core/documents/intelligence/citation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { extractReferences } from "../referenceEngine.js";

export function extractCitations(text: any): any {
  var refs: any = extractReferences(text);
  return {"citations": py.get(refs, "citations", [])};
}
export { extractReferences };

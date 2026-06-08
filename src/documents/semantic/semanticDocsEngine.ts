/**
 * Converted from Python: core/documents/semantic/semantic_docs_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { extractSemanticOutline as _v14Outline } from "../intelligence/semanticOutlineEngine.js";
import { extractSemanticReferences } from "./semanticReferenceEngine.js";
import { extractSemanticExamples } from "./semanticExampleEngine.js";
import { extractSemanticTables } from "./semanticTableEngine.js";

export function analyzeSemanticDocs(text: any): any {
  var outline: any = _v14Outline(text);
  var refs: any = extractSemanticReferences(text);
  var examples: any = extractSemanticExamples(text);
  var tables: any = extractSemanticTables(text);
  return {"hierarchy": outline, "references": refs, "examples": examples, "tables": tables};
}
export { extractSemanticExamples, extractSemanticReferences, extractSemanticTables };

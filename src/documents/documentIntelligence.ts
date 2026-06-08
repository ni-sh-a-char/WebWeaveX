/**
 * Converted from Python: core/documents/document_intelligence.py
 * @generated — WebWeaveX python→javascript library port
 */

import { extractSections } from "./sectionEngine.js";
import { extractStructuralBlocks } from "./semanticStructureEngine.js";
import { extractReferences } from "./referenceEngine.js";

export function analyzeDocument(text: any): any {
  return {"sections": extractSections(text), "structure": extractStructuralBlocks(text), "references": extractReferences(text)};
}
export { extractReferences, extractSections, extractStructuralBlocks };

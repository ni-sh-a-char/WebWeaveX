/**
 * Converted from Python: core/knowledge/document_knowledge_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDocumentKnowledgeV2(docs: any): any {
  if (!((docs !== null && typeof docs === "object" && !Array.isArray(docs) && !(docs instanceof Set) && !(docs instanceof Map)))) {
    return {"sections": 0, "evidence": "empty"};
  }
  var sections: any = py.get(docs, "sections", {});
  var count: any = (((sections !== null && typeof sections === "object" && !Array.isArray(sections) && !(sections instanceof Set) && !(sections instanceof Map))) ? py.get(sections, "count", py.len(py.get(sections, "sections", []))) : 0);
  return {"section_count": count, "has_tutorial": py.truthy(py.get(docs, "tutorial_flow")), "has_chunks": py.truthy(py.get(docs, "chunks")), "evidence": "document_payload"};
}

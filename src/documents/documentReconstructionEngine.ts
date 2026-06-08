/**
 * Converted from Python: core/documents/document_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseSource } from "../parsers/index.js";
import { buildConceptGraph, buildSemanticFlow, chunkSemantic, extractApiContracts, extractArchitectureSections, reconstructTutorial } from "./reconstruction/index.js";

export function reconstructDocument(text: any, source_url: any = ""): any {
  var parsed: any = parseSource(text, py.or2(source_url, () => ("document.md")));
  return {"parser": parsed, "semantic_flow": buildSemanticFlow(text), "tutorial": reconstructTutorial(text), "concept_graph": buildConceptGraph(text), "chunks": chunkSemantic(text), "api_contracts": extractApiContracts(text), "architecture_docs": extractArchitectureSections(text)};
}
export { buildConceptGraph, buildSemanticFlow, chunkSemantic, extractApiContracts, extractArchitectureSections, parseSource, reconstructTutorial };

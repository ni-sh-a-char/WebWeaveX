/**
 * Converted from Python: core/documents/document_semantic_ir_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildArgumentDependencies } from "./argumentDependencyEngine.js";
import { modelConceptProgression } from "./conceptProgressionEngine.js";
import { buildCoreferenceGraph } from "./coreferenceGraphEngine.js";
import { buildDocumentDependencyGraph } from "./documentDependencyGraphEngine.js";
import { parseRhetoricalStructure } from "./rhetoricalParserEngine.js";
import { inferTutorialPrerequisites } from "./tutorialPrerequisiteEngine.js";

export function buildDocumentSemanticIr(text: any): any {
  return {"rhetorical": parseRhetoricalStructure(text), "argument": buildArgumentDependencies(text), "progression": modelConceptProgression(text), "prerequisites": inferTutorialPrerequisites(text), "coreference": buildCoreferenceGraph(text), "dependency_graph": buildDocumentDependencyGraph(text), "evidence": ["discourse:rhetorical", "discourse:argument", "discourse:progression", "discourse:prerequisites"]};
}
export { buildArgumentDependencies, buildCoreferenceGraph, buildDocumentDependencyGraph, inferTutorialPrerequisites, modelConceptProgression, parseRhetoricalStructure };

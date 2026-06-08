/**
 * Converted from Python: core/extract/facades/document_facade.py
 * @generated — WebWeaveX python→javascript library port
 */

import { analyzeDocument } from "../../documents/documentIntelligence.js";
import { extractSemanticOutline } from "../../documents/intelligence/semanticOutlineEngine.js";
import { buildToc } from "../../documents/intelligence/tocEngine.js";
import { extractCitations } from "../../documents/intelligence/citationEngine.js";
import { extractCodeBlocks } from "../../documents/intelligence/codeBlockEngine.js";
import { extractCrossRefs } from "../../documents/intelligence/crossReferenceEngine.js";
import { extractDiagramRefs } from "../../documents/intelligence/diagramReferenceEngine.js";
import { extractKnowledgeBlocks } from "../../documents/intelligence/knowledgeBlockEngine.js";
import { extractTables } from "../../documents/intelligence/tableEngine.js";
import { extractSemanticSections } from "../../documents/semanticSectionEngine.js";
import { extractTutorialFlow } from "../../documents/tutorialReasoningEngine.js";
import { buildConceptDependencies } from "../../documents/conceptGraphEngine.js";
import { resolveReferences as resolveDocReferencesV4 } from "../../documents/entityResolutionEngine.js";
import { buildSemanticChunks } from "../../documents/semanticChunkEngine.js";
import { extractCodeContext } from "../../documents/codeReferenceEngine.js";
import { extractArchitectureDocs } from "../../documents/architectureDocumentEngine.js";
import { extractApiContractDocs } from "../../documents/apiDocumentationEngine.js";
import { synthesizeKnowledge } from "../../documents/knowledgeSynthesisEngine.js";
import { buildConceptGraph as buildDocConceptGraphV18, buildSemanticFlow as buildDocSemanticFlowV18, chunkSemantic as chunkSemanticV18, extractApiContracts as extractApiContractsV18, extractArchitectureSections as extractArchitectureSectionsV18, extractDependencyReferences as extractDependencyReferencesV18, extractMigrationGuides as extractMigrationGuidesV18, reconstructTutorial as reconstructTutorialV18 } from "../../documents/reconstruction/index.js";
import { buildReferenceGraph } from "../../documents/recursive/referenceGraphEngine.js";
import { analyzeSemanticDocs, buildSemanticRelationships, extractSemanticApiDocs, extractSemanticCodeReferences, extractSemanticDiagrams, extractSemanticExamples, extractSemanticOutline as extractSemanticOutlineV16, extractSemanticReferences, extractSemanticSpecs, extractSemanticTables, extractSemanticTutorials } from "../../documents/semantic/index.js";

export { analyzeDocument, analyzeSemanticDocs, buildConceptDependencies, buildDocConceptGraphV18, buildDocSemanticFlowV18, buildReferenceGraph, buildSemanticChunks, buildSemanticRelationships, buildToc, chunkSemanticV18, extractApiContractDocs, extractApiContractsV18, extractArchitectureDocs, extractArchitectureSectionsV18, extractCitations, extractCodeBlocks, extractCodeContext, extractCrossRefs, extractDependencyReferencesV18, extractDiagramRefs, extractKnowledgeBlocks, extractMigrationGuidesV18, extractSemanticApiDocs, extractSemanticCodeReferences, extractSemanticDiagrams, extractSemanticExamples, extractSemanticOutline, extractSemanticOutlineV16, extractSemanticReferences, extractSemanticSections, extractSemanticSpecs, extractSemanticTables, extractSemanticTutorials, extractTables, extractTutorialFlow, reconstructTutorialV18, resolveDocReferencesV4, synthesizeKnowledge };

/**
 * Converted from Python: core/documents/universal_document_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildDocumentStructure } from "./documentStructureEngine.js";
import { buildDocumentHierarchy } from "./documentHierarchyEngine.js";
import { extractCitations } from "./citationExtractionEngine.js";
import { extractReferences } from "./referenceExtractionEngine.js";
import { extractDocumentTables } from "./documentTableEngine.js";
import { buildDocumentKnowledgeGraph } from "../knowledge/documentKnowledgeGraphEngine.js";
import { extractPresentationStructure } from "../presentation/presentationExtractionEngine.js";
import { extractSpreadsheetStructure } from "../spreadsheets/spreadsheetExtractionEngine.js";
import { compileDocumentRuntimeIr } from "../ir/documentRuntimeIr.js";

export function extractDocumentRuntime(text: any, slides: any = null, workbook: any = null): any {
  var structure: any = buildDocumentStructure(text);
  var hierarchy: any = buildDocumentHierarchy(structure);
  var citations: any = extractCitations(text);
  var references: any = extractReferences(structure);
  var tables: any = extractDocumentTables(text);
  var knowledge_graph: any = buildDocumentKnowledgeGraph(structure);
  var slide_payload: any = extractPresentationStructure(py.or2(slides, () => ([])));
  var worksheet_payload: any = extractSpreadsheetStructure(py.or2(workbook, () => ({})));
  var document_ir: any = compileDocumentRuntimeIr(structure, hierarchy, citations, references, tables, knowledge_graph, slide_payload, worksheet_payload);
  return {"structure": structure, "hierarchy": hierarchy, "citations": citations, "references": references, "tables": tables, "slides": slide_payload, "worksheets": worksheet_payload, "knowledge_graph": knowledge_graph, "document_ir": document_ir, "bounded": true};
}
export { buildDocumentHierarchy, buildDocumentKnowledgeGraph, buildDocumentStructure, compileDocumentRuntimeIr, extractCitations, extractDocumentTables, extractPresentationStructure, extractReferences, extractSpreadsheetStructure };

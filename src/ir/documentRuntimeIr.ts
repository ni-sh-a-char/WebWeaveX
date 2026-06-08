/**
 * Converted from Python: core/ir/document_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileDocumentRuntimeIr(structure: any, hierarchy: any, citations: any, references: any, tables: any, knowledge_graph: any, slides: any = null, worksheets: any = null): any {
  slides = py.or2(slides, () => ({"slides": [], "bounded": true}));
  worksheets = py.or2(worksheets, () => ({"worksheets": [], "bounded": true}));
  return {"ir": "document_runtime", "document_structure": structure, "sections": py.get(structure, "sections", []), "hierarchy": hierarchy, "tables": tables, "slides": slides, "worksheets": worksheets, "citations": citations, "references": references, "knowledge_graph": knowledge_graph, "structure": structure, "bounded": true};
}

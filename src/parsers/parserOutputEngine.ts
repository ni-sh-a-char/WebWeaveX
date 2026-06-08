/**
 * Converted from Python: core/parsers/parser_output_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { groundParserOutput } from "../evidence/groundingEngine.js";
import { buildParserCognitionEvidence } from "./parserCognitionEngine.js";

export function normalizeParserOutput(parsed: any): any {
  var sym: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
  var cognition: any = buildParserCognitionEvidence(parsed);
  return {"symbol_names": py.sorted(py.or2(py.get(sym, "symbols", []), () => ([]))), "import_names": py.sorted(py.or2(py.get(sym, "imports", []), () => ([]))), "export_names": py.sorted(py.or2(py.get(sym, "exports", []), () => ([]))), "function_names": py.sorted(py.or2(py.get(sym, "functions", []), () => ([]))), "class_names": py.sorted(py.or2(py.get(sym, "classes", []), () => ([]))), "interface_names": py.sorted(py.or2(py.get(sym, "interfaces", []), () => ([]))), "trait_names": py.sorted(py.or2(py.get(sym, "traits", []), () => ([]))), "decorator_names": py.sorted(py.or2(py.get(sym, "decorators", []), () => ([]))), "annotation_names": py.sorted(py.or2(py.get(sym, "annotations", []), () => ([]))), "dependency_names": py.sorted(py.or2(py.get(py.or2(py.get(parsed, "dependencies", {}), () => ({})), "dependencies", []), () => ([]))), "call_graph": py.get(parsed, "calls", {}), "semantic_graph": py.get(parsed, "semantic_graph", {}), "runtime_evidence": py.get(parsed, "runtime", {}), "framework_evidence": py.get(parsed, "frameworks", {}), "api_evidence": py.get(parsed, "api_surface", {}), "parser_evidence": py.get(parsed, "evidence", {}), "grounding": groundParserOutput(parsed), "parser_evidence_list": py.get(cognition, "parser_evidence", []), "semantic_evidence_list": py.get(cognition, "semantic_evidence", []), "graph_evidence_list": py.get(cognition, "graph_evidence", []), "cognition_lineage": py.get(cognition, "lineage", {}), "language": py.get(parsed, "language", "text"), "source_id": py.get(parsed, "source_id", "")};
}
export { buildParserCognitionEvidence, groundParserOutput };

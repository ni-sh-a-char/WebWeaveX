/**
 * Converted from Python: core/ir/document_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildDocumentSemanticIr } from "../documents/documentSemanticIrEngine.js";
import { emptyConfidence, emptyLineage, mergeEvidence } from "./_base.js";

export let DocumentIR: any = py.at(Object, [py.toStr, Object]);
export function emptyDocumentIr(): any {
  return {"concepts": [], "claims": [], "arguments": [], "tutorial_steps": [], "dependencies": [], "references": [], "contradictions": [], "rhetorical_units": [], "semantic_roles": [], "explanation_chains": [], "concept_progressions": [], "instructional_flows": [], "semantic_graph": {}, "lineage": emptyLineage("document_ir"), "confidence": emptyConfidence()};
}
export function compileDocumentIr(text: any): any {
  var raw: any = buildDocumentSemanticIr(text);
  var ir: any = emptyDocumentIr();
  var rhet: any = py.get(raw, "rhetorical", {});
  var arg: any = py.get(raw, "argument", {});
  py.setItem(ir, "rhetorical_units", py.get(rhet, "units", []));
  py.setItem(ir, "semantic_roles", py.get(rhet, "roles", []));
  py.setItem(ir, "claims", py.get(arg, "nodes", []));
  py.setItem(ir, "arguments", py.get(arg, "dependencies", []));
  py.setItem(ir, "tutorial_steps", py.get(py.get(raw, "prerequisites", {}), "chain", []));
  py.setItem(ir, "concept_progressions", py.get(py.get(raw, "progression", {}), "progression", []));
  py.setItem(ir, "instructional_flows", py.get(py.get(raw, "prerequisites", {}), "prerequisites", []));
  py.setItem(ir, "explanation_chains", py.get(py.get(raw, "dependency_graph", {}), "edges", []));
  py.setItem(ir, "semantic_graph", py.get(raw, "dependency_graph", {}));
  py.setItem(ir, "semantic_evidence", mergeEvidence(py.get(raw, "evidence", [])));
  py.setItem(ir, "lineage", emptyLineage("document_semantic_ir"));
  py.setItem(ir, "confidence", {"score": (py.truthy(py.at(ir, "rhetorical_units")) ? py.F(0.7) : py.F(0.3)), "basis": py.get(raw, "evidence", []), "deterministic": true});
  py.setItem(ir, "_raw", raw);
  return ir;
}
export { buildDocumentSemanticIr, emptyConfidence, emptyLineage, mergeEvidence };

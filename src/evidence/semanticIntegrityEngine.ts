/**
 * Converted from Python: core/evidence/semantic_integrity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildExplainability } from "./explainabilityEngine.js";
import { buildLineage } from "./lineageEngine.js";
import { buildProvenance } from "./provenanceEngine.js";
import { scoreSemanticConfidence } from "./semanticConfidenceEngine.js";
import { attachEpistemicState } from "./epistemicEvidenceEngine.js";
import { applyFormalSemanticFoundation } from "./formalSemanticFoundationEngine.js";
import { buildTraceability } from "./traceabilityEngine.js";

export function _groundParser(parsed: any): any {
  var flags: any = py.get(parsed, "parser_evidence", py.get(parsed, "evidence", {}));
  if (!((flags !== null && typeof flags === "object" && !Array.isArray(flags) && !(flags instanceof Set) && !(flags instanceof Map)))) {
    flags = {};
  }
  var symbols: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
  var grounding: any = {"language": py.get(parsed, "language", "text"), "symbol_count": py.add(py.len(py.or2(py.get(symbols, "classes", []), () => ([]))), py.len(py.or2(py.get(symbols, "functions", []), () => ([])))), "flags": flags};
  var evidence: any = py.iter(py.sorted(py.items(flags))).filter(([k, v]: any) => py.truthy(v)).map(([k, v]: any) => `parser:${py.toStr(k)}`);
  return buildProvenance(evidence, undefined, grounding);
}
export function buildSemanticIntegrityObject(observed: any = null, parsed_facts: any = null, inferred: any = null, reconciled: any = null, contradicted: any = null, derived: any = null, ambiguities: any = null, parser_payload: any = null, lineage_stages: any = null): any {
  observed = (((observed !== null && typeof observed === "object" && !Array.isArray(observed) && !(observed instanceof Set) && !(observed instanceof Map))) ? observed : {});
  parsed_facts = (((parsed_facts !== null && typeof parsed_facts === "object" && !Array.isArray(parsed_facts) && !(parsed_facts instanceof Set) && !(parsed_facts instanceof Map))) ? parsed_facts : {});
  inferred = (((inferred !== null && typeof inferred === "object" && !Array.isArray(inferred) && !(inferred instanceof Set) && !(inferred instanceof Map))) ? inferred : {});
  reconciled = (((reconciled !== null && typeof reconciled === "object" && !Array.isArray(reconciled) && !(reconciled instanceof Set) && !(reconciled instanceof Map))) ? reconciled : {});
  contradicted = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? contradicted : {});
  derived = (((derived !== null && typeof derived === "object" && !Array.isArray(derived) && !(derived instanceof Set) && !(derived instanceof Map))) ? derived : {});
  ambiguities = py.sorted(py.toSet(py.iter(py.or2(ambiguities, () => ([]))).filter((a: any) => py.truthy(a)).map((a: any) => py.toStr(a))));
  var prov: any = (py.truthy(parser_payload) ? _groundParser(parser_payload) : buildProvenance(["no_parser"]));
  var confidence: any = scoreSemanticConfidence(parser_payload);
  var lineage: any = buildLineage(py.or2(lineage_stages, () => ([{"stage": "semantic_integrity", "inputs": py.get(prov, "sources", []), "outputs": []}])));
  var explain: any = buildExplainability(parser_payload, confidence, prov);
  var evidence_list: any = py.get(prov, "evidence", []);
  var traceability: any = buildTraceability(evidence_list, lineage, py.iter(py.or2(lineage_stages, () => ([]))).filter((s: any) => ((s !== null && typeof s === "object" && !Array.isArray(s) && !(s instanceof Set) && !(s instanceof Map)))).map((s: any) => py.get(s, "stage", "")));
  var out: any = {"observed": observed, "parsed": parsed_facts, "inferred": inferred, "reconciled": reconciled, "contradicted": contradicted, "derived": derived, "ambiguities": ambiguities, "evidence": evidence_list, "sources": py.get(prov, "sources", []), "grounding": py.get(prov, "grounding", {}), "lineage": lineage, "confidence_basis": confidence, "why": explain, "parser_basis": py.get(explain, "parser_basis", {}), "graph_basis": py.get(explain, "graph_basis", {}), "semantic_basis": py.get(explain, "semantic_basis", {}), "traceability": traceability, "contradictions": contradicted};
  return attachEpistemicState(applyFormalSemanticFoundation(out));
}
export { applyFormalSemanticFoundation, attachEpistemicState, buildExplainability, buildLineage, buildProvenance, buildTraceability, scoreSemanticConfidence };

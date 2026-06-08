/**
 * Converted from Python: core/evidence/grounding_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { applySemanticConservatism } from "./semanticConservatismEngine.js";
import { buildSemanticIntegrityObject } from "./semanticIntegrityEngine.js";
import { buildProvenance } from "./provenanceEngine.js";
import { applySemanticUncertainty } from "../semantic/semanticUncertaintyEngine.js";

export function groundParserOutput(parsed: any): any {
  if (!((parsed !== null && typeof parsed === "object" && !Array.isArray(parsed) && !(parsed instanceof Set) && !(parsed instanceof Map)))) {
    return buildProvenance([], undefined, {});
  }
  var flags: any = py.get(parsed, "parser_evidence", py.get(parsed, "evidence", {}));
  if (!((flags !== null && typeof flags === "object" && !Array.isArray(flags) && !(flags instanceof Set) && !(flags instanceof Map)))) {
    flags = {};
  }
  var symbols: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
  var parsed_facts: any = {"language": py.get(parsed, "language", "text"), "classes": py.slice([...py.iter(py.or2(py.get(symbols, "classes", []), () => ([])))], null, 50), "functions": py.slice([...py.iter(py.or2(py.get(symbols, "functions", []), () => ([])))], null, 50), "imports": py.slice([...py.iter(py.or2(py.get(symbols, "imports", []), () => ([])))], null, 50)};
  return buildSemanticIntegrityObject(undefined, parsed_facts, undefined, undefined, undefined, undefined, undefined, parsed, [{"stage": "parser", "inputs": [], "outputs": py.iter(py.sorted(py.items(flags))).filter(([k, v]: any) => py.truthy(v)).map(([k, v]: any) => `parser:${py.toStr(k)}`)}]);
}
export function structureCognition(observed: any, inferred: any, reconciled: any, parsed: any = null, contradicted: any = null, ambiguities: any = null): any {
  var derived: any = {"structure": "cognition_bundle"};
  if ((py.truthy(parsed) && !py.eq(reconciled, observed))) {
    py.setItem(derived, "reconciliation_applied", true);
  }
  var amb: any = [...py.iter(py.or2(ambiguities, () => ([])))];
  if ((py.truthy(inferred) && !py.truthy(observed))) {
    py.listAppend(amb, "inferred_without_direct_observation");
  }
  var parsed_facts: Record<string, any> = {};
  if (py.truthy(parsed)) {
    var sym: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
    parsed_facts = {"language": py.get(parsed, "language", "text"), "classes": py.slice([...py.iter(py.or2(py.get(sym, "classes", []), () => ([])))], null, 30), "functions": py.slice([...py.iter(py.or2(py.get(sym, "functions", []), () => ([])))], null, 30)};
  }
  var bundle: any = buildSemanticIntegrityObject(observed, parsed_facts, inferred, reconciled, py.or2(contradicted, () => ({})), derived, amb, parsed, [{"stage": "observe", "inputs": [], "outputs": py.sorted(py.keys(observed))}, {"stage": "infer", "inputs": py.sorted(py.keys(observed)), "outputs": py.sorted(py.keys(inferred))}, {"stage": "reconcile", "inputs": py.sorted(py.keys(inferred)), "outputs": py.sorted(py.keys(reconciled))}]);
  return applySemanticUncertainty(applySemanticConservatism(bundle));
}
export { applySemanticConservatism, applySemanticUncertainty, buildProvenance, buildSemanticIntegrityObject };

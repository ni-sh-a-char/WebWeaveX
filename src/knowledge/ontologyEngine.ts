/**
 * Converted from Python: core/knowledge/ontology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { structureCognition } from "../evidence/index.js";
import { scoreEpistemicConfidence } from "../evidence/epistemicConfidenceEngine.js";
import { assessEvidenceSufficiency } from "../evidence/evidenceSufficiencyEngine.js";
import { buildSupport } from "../evidence/semanticSupportEngine.js";
import { buildWeaknesses } from "../evidence/semanticWeaknessEngine.js";
import { assessOntologyEdgeFragility } from "./ontologyFragilityEngine.js";
import { restrainOntologyEdge } from "./ontologyRestraintEngine.js";

export function _normalizeEdge(r: any): any {
  var ev: any = py.get(r, "evidence", []);
  if ((typeof ev === "string")) {
    ev = [ev];
  } else if (!(Array.isArray(ev))) {
    ev = [];
  }
  var support: any = buildSupport(ev);
  var weaknesses: any = buildWeaknesses(ev, py.get(r, "ambiguities", []));
  var sufficiency: any = assessEvidenceSufficiency(ev);
  var epistemic_confidence: any = scoreEpistemicConfidence(ev, undefined, undefined, py.get(r, "ambiguities", []));
  var observed: any = {"from": py.get(r, "from"), "to": py.get(r, "to"), "stated": py.truthy(ev)};
  var inferred: any = (py.truthy(ev) ? {} : {"from": py.get(r, "from"), "to": py.get(r, "to"), "relation": "inferred_weak"});
  var fragility: any = assessOntologyEdgeFragility({"evidence": ev, "ambiguities": py.get(r, "ambiguities", [])});
  var cap: any = py.get(py.get(fragility, "confidence_limits", {}), "max_score", py.F(1.0));
  py.setItem(epistemic_confidence, "score", py.round(py.min([py.at(epistemic_confidence, "score"), cap]), 3));
  var edge: any = {"from": py.get(r, "from"), "to": py.get(r, "to"), "observed": observed, "inferred": inferred, "reconciled": {"from": py.get(r, "from"), "to": py.get(r, "to"), "evidence": py.sorted(py.toSet(py.iter(ev).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))))}, "evidence": py.sorted(py.toSet(py.iter(ev).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e)))), "lineage": py.get(r, "lineage", {"stage": "ontology_edge"}), "confidence_basis": epistemic_confidence, "confidence_limits": py.get(fragility, "confidence_limits", {}), "grounding": py.get(r, "grounding", {"method": (py.truthy(ev) ? "stated_relation" : "inferred_weak")}), "contradictions": py.get(r, "contradictions", {}), "ambiguities": py.sorted(py.toSet(py.or2(py.get(r, "ambiguities", []), () => ((py.truthy(ev) ? [] : ["missing_edge_evidence"]))))), "support": support, "weaknesses": weaknesses, "fragility": fragility, "uncertainties": {"insufficient": !py.truthy(py.at(sufficiency, "sufficient"))}, "unsupported_dimensions": py.get(fragility, "missing_support", []), "evidence_sufficiency": sufficiency, "epistemic_state": {"sufficient": py.at(sufficiency, "sufficient"), "unsupported": !py.truthy(ev), "confidence": py.at(epistemic_confidence, "score")}};
  return restrainOntologyEdge(edge);
}
export function buildOntology(entities: any, relations: any): any {
  var ents: any = py.sorted(py.toSet(py.iter(py.or2(entities, () => ([]))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var observed: any = {"entities": py.iter(ents).map((e: any) => ({"id": e, "kind": "symbol"}))};
  var rels: any = py.iter(py.or2(relations, () => ([]))).filter((r: any) => (((r !== null && typeof r === "object" && !Array.isArray(r) && !(r instanceof Set) && !(r instanceof Map))) && py.truthy(py.get(r, "from")) && py.truthy(py.get(r, "to")))).map((r: any) => _normalizeEdge(r));
  rels = py.sorted(rels, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any});
  var inferred: any = {"relations": rels};
  var reconciled: any = {"entities": py.at(observed, "entities"), "relations": rels};
  var ambiguities: any[] = [];
  if (py.any(py.iter(rels).map((edge: any) => !py.truthy(py.at(edge, "evidence"))))) {
    py.listAppend(ambiguities, "ontology_edges_without_evidence");
  }
  return structureCognition(observed, inferred, reconciled, null, undefined, ambiguities);
}
export { assessEvidenceSufficiency, assessOntologyEdgeFragility, buildSupport, buildWeaknesses, restrainOntologyEdge, scoreEpistemicConfidence, structureCognition };

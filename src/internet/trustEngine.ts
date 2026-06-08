/**
 * Converted from Python: core/internet/trust_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { scoreEpistemicConfidence } from "../evidence/epistemicConfidenceEngine.js";
import { scoreSemanticConfidence } from "../evidence/semanticConfidenceEngine.js";
import { scoreAuthority } from "./authorityEngine.js";
import { reconstructCitationLineage } from "./citationLineageEngine.js";
import { analyzeSemanticConsistency } from "./semanticConsistencyEngine.js";
import { preserveContradictions } from "../semantic/contradictionPreservationEngine.js";

export function computeTrust(url: any, corroboration_count: any = 0, html_text: any = "", claims: any = null): any {
  var authority: any = scoreAuthority(url);
  var contradictions: any = preserveContradictions((py.truthy(html_text) ? [py.slice(html_text, null, 500)] : []));
  var extra: any = py.add([...py.iter(py.get(authority, "evidence", []))], [`corroboration:${py.toStr(corroboration_count)}`]);
  var confidence: any = scoreSemanticConfidence(undefined, undefined, extra);
  var epistemic: any = scoreEpistemicConfidence(extra, undefined, undefined, (py.truthy(py.get(py.get(contradictions, "contradicted", {}), "preserved")) ? ["contradiction"] : []), 0);
  var corroboration: any = {"count": corroboration_count, "evidence": [`corroboration:${py.toStr(corroboration_count)}`]};
  var semantic_agreement: any = analyzeSemanticConsistency(py.or2(claims, () => ([])));
  var citation_lineage: any = (py.truthy(html_text) ? reconstructCitationLineage(html_text) : {"citations": [], "evidence": []});
  var score: any = py.round(py.min([py.F(1.0), py.add(py.add(py.mul(py.at(epistemic, "score"), py.F(0.5)), py.mul(py.at(authority, "authority_score"), py.F(0.35))), py.min([py.F(0.15), py.mul(corroboration_count, py.F(0.05))]))]), 3);
  if (py.truthy(py.get(py.get(contradictions, "contradicted", {}), "preserved"))) {
    score = py.round(py.min([score, py.F(0.5)]), 3);
  }
  var deterministic_inputs: any = py.sorted(py.bitor(py.bitor(py.toSet(py.get(confidence, "deterministic_inputs", [])), py.toSet(py.get(authority, "deterministic_inputs", []))), new Set([`corroboration=${py.toStr(corroboration_count)}`, `citations=${py.toStr(py.get(citation_lineage, "citation_count", 0))}`])));
  return {"url": url, "trust_score": score, "authority": authority, "score": score, "basis": {"authority": py.at(authority, "authority_score"), "corroboration": corroboration_count, "citation_count": py.get(citation_lineage, "citation_count", 0), ...(py.get(confidence, "basis", {}))}, "evidence": py.sorted(py.toSet(py.add(py.add([...py.iter(py.get(authority, "evidence", []))], [...py.iter(py.get(confidence, "evidence", []))]), py.get(citation_lineage, "evidence", [])))), "deterministic_inputs": deterministic_inputs, "contradictions": py.get(contradictions, "contradicted", {}), "corroboration": corroboration, "semantic_agreement": py.get(semantic_agreement, "semantic_agreement", {}), "lineage": {"stage": "trust_scoring", "citation_lineage": py.get(citation_lineage, "lineage", {})}, "confidence_basis": epistemic, "supporting_evidence": py.get(epistemic, "supporting_evidence", []), "contradicting_evidence": py.get(epistemic, "contradicting_evidence", []), "uncertainty_factors": py.get(epistemic, "uncertainty_factors", []), "sources": (py.truthy(url) ? [url] : []), "grounding": {"method": "authority_corroboration_citation"}};
}
export function rankTrust(urls: any): any {
  return py.sorted(py.iter(py.or2(urls, () => ([]))).map((u: any) => computeTrust(u)), {key: ((x: any) => [(-py.at(x, "trust_score")), py.at(x, "url")]) as (item: any) => any});
}
export { analyzeSemanticConsistency, preserveContradictions, reconstructCitationLineage, scoreAuthority, scoreEpistemicConfidence, scoreSemanticConfidence };

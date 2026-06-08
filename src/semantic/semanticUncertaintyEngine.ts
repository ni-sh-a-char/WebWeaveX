/**
 * Converted from Python: core/semantic/semantic_uncertainty_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelUncertainty } from "../evidence/uncertaintyEngine.js";
import { applySemanticConservatism } from "../evidence/semanticConservatismEngine.js";

export function applySemanticUncertainty(bundle: any): any {
  var evidence: any = py.or2(py.get(bundle, "evidence", []), () => ([]));
  var ambiguities: any = py.or2(py.get(bundle, "ambiguities", []), () => ([]));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => ({}));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var uncertainty: any = modelUncertainty(py.len(evidence), py.len(ambiguities), py.len(pairs));
  py.setItem(bundle, "uncertainty", uncertainty);
  bundle = applySemanticConservatism(bundle);
  var cb: any = py.get(bundle, "confidence_basis", {});
  py.setItem(cb, "score", py.round(py.min([py.toFloat(py.get(cb, "score", py.F(0.5))), py.at(uncertainty, "confidence_score")]), 3));
  py.setItem(bundle, "confidence_basis", cb);
  return bundle;
}
export { applySemanticConservatism, modelUncertainty };

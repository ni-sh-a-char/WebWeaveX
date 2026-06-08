/**
 * Converted from Python: core/evidence/semantic_uncertainty_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelUncertainty } from "./uncertaintyEngine.js";

export function propagateUncertainty(bundle: any): any {
  var evidence: any = py.or2(py.get(bundle, "evidence", []), () => ([]));
  var ambiguities: any = py.or2(py.get(bundle, "ambiguities", []), () => ([]));
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => ({}));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var model: any = modelUncertainty(py.len(evidence), py.len(ambiguities), py.len(pairs));
  var uncertainties: any = {...(model), "factors": py.sorted(py.toSet(py.add(ambiguities, (py.truthy(pairs) ? [`contradiction:${py.toStr(py.len(pairs))}`] : []))))};
  py.setItem(bundle, "uncertainties", uncertainties);
  return bundle;
}
export { modelUncertainty };

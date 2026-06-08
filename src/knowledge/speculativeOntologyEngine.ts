/**
 * Converted from Python: core/knowledge/speculative_ontology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { suppressSpeculativeInference } from "../evidence/speculativeInferenceEngine.js";
import { suppressOntologySelfConfirmation } from "./ontologySelfConfirmationEngine.js";
import { suppressRecursiveOntologyLock } from "./recursiveOntologyLockEngine.js";
import { applyCivilizationOntology } from "./civilizationOntologyEngine.js";
import { applyAntiCaptureOntology } from "./antiCaptureOntologyEngine.js";
import { applySovereigntyOntology } from "./sovereigntyOntologyEngine.js";
import { applyOpennessOntology } from "./opennessOntologyEngine.js";

export function suppressSpeculativeOntologyEdge(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var spec: any = suppressSpeculativeInference("ontology_edge", ev, py.truthy(py.get(edge, "inferred")));
  var fragility: any = py.get(edge, "fragility", {});
  var uncertainty: any = py.get(edge, "uncertainty", {"visible": !py.truthy(ev)});
  var ambiguity: any = py.get(edge, "ambiguity", {"visible": false});
  var caps: any = py.get(edge, "confidence_caps", py.get(edge, "confidence_limits", {}));
  var suppressed: any = py.or2(py.get(spec, "suppressed", false), () => (!py.truthy(ev)));
  var reality: any = {"aligned": py.and2(py.truthy(ev), () => (!py.truthy(py.get(spec, "suppressed")))), "parser_bounded": py.truthy(ev)};
  var base: any = {...(edge), "reality_alignment": reality, "boundary_pressure": {"edge": py.get(spec, "suppressed", false)}, "stability": {"stable": py.truthy(ev), "level": (py.truthy(ev) ? "high" : "low")}, "supported": {"stated": py.truthy(ev), "evidence_count": py.len(ev)}, "unsupported": {"edge": suppressed, "speculative": py.get(spec, "suppressed", false)}, "suppressed": {"inheritance": suppressed, "equivalence": suppressed, "merge": suppressed}, "fragility": (py.truthy(fragility) ? fragility : {"level": "medium"}), "uncertainty": uncertainty, "ambiguity": ambiguity, "confidence_caps": caps, "speculative_suppression": py.get(spec, "record")};
  return applyOpennessOntology(applySovereigntyOntology(applyAntiCaptureOntology(applyCivilizationOntology(suppressRecursiveOntologyLock(suppressOntologySelfConfirmation(base))))));
}
export { applyAntiCaptureOntology, applyCivilizationOntology, applyOpennessOntology, applySovereigntyOntology, suppressOntologySelfConfirmation, suppressRecursiveOntologyLock, suppressSpeculativeInference };

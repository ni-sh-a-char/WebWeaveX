/**
 * Converted from Python: core/repository/speculative_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { suppressSpeculativeInference } from "../evidence/speculativeInferenceEngine.js";
import { suppressTopologySelfConfirmation } from "./topologySelfConfirmationEngine.js";
import { suppressRecursiveTopologyLock } from "./recursiveTopologyLockEngine.js";
import { applyCivilizationTopology } from "./civilizationTopologyEngine.js";
import { applyAntiCaptureTopology } from "./antiCaptureTopologyEngine.js";
import { applySovereigntyTopology } from "./sovereigntyTopologyEngine.js";
import { applyOpennessTopology } from "./opennessTopologyEngine.js";

export function suppressSpeculativeTopologyEdge(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var spec: any = suppressSpeculativeInference("topology_edge", ev, py.truthy(py.get(edge, "inferred")));
  var suppressed: any = py.get(spec, "suppressed", false);
  var reality: any = {"aligned": py.and2(py.truthy(ev), () => (!py.truthy(suppressed))), "parser_bounded": py.truthy(ev)};
  var base: any = {...(edge), "reality_alignment": reality, "boundary_pressure": {"edge": py.or2(suppressed, () => (!py.truthy(ev)))}, "stability": {"stable": py.truthy(ev), "level": (py.truthy(ev) ? "high" : "low")}, "supported": {"stated": py.truthy(ev)}, "unsupported": {"edge": py.or2(suppressed, () => (!py.truthy(ev))), "speculative": py.get(spec, "suppressed", false)}, "suppressed": {"edge": suppressed, "reason": (py.truthy(py.get(spec, "record")) ? py.get(py.get(spec, "record", {}), "reason") : null)}, "fragility": py.get(edge, "fragility", {"level": (!py.truthy(ev) ? "medium" : "low")}), "uncertainty": py.get(edge, "uncertainty", {"visible": !py.truthy(ev)}), "ambiguity": py.get(edge, "ambiguity", {"visible": false}), "confidence_caps": py.get(edge, "confidence_caps", py.get(edge, "confidence_limits", {})), "evidence": ev, "speculative_suppression": py.get(spec, "record")};
  return applyOpennessTopology(applySovereigntyTopology(applyAntiCaptureTopology(applyCivilizationTopology(suppressRecursiveTopologyLock(suppressTopologySelfConfirmation(base))))));
}
export { applyAntiCaptureTopology, applyCivilizationTopology, applyOpennessTopology, applySovereigntyTopology, suppressRecursiveTopologyLock, suppressSpeculativeInference, suppressTopologySelfConfirmation };

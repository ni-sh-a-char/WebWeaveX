/**
 * Converted from Python: core/repository/topology_self_confirmation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { _stabilizationRecord } from "../evidence/unsupportedStabilizationEngine.js";

export function suppressTopologySelfConfirmation(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var inferred: any = py.truthy(py.get(edge, "inferred"));
  var self_confirm: any = py.and2(inferred, () => ((py.len(ev) < 1)));
  var record: any = (py.truthy(self_confirm) ? _stabilizationRecord("topology_self_confirmation", {"required": 1, "actual": py.len(ev)}) : null);
  return {...(edge), "truth_preservation": {"preserved": !py.truthy(self_confirm), "self_confirmation_blocked": self_confirm}, "instability": {"unstable": py.or2(self_confirm, () => (!py.truthy(ev))), "preserved": true}, "entropy": {"level": (py.truthy(self_confirm) ? py.F(0.5) : py.F(0.1))}, "truth_boundaries": {"propagation_allowed": py.truthy(ev)}, "confidence_collapse": (py.truthy(self_confirm) ? {"max": py.F(0.35)} : py.get(edge, "confidence_caps", {})), "stabilization_suppressed": record};
}

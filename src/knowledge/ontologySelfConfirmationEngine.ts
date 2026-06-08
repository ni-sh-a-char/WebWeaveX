/**
 * Converted from Python: core/knowledge/ontology_self_confirmation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { _stabilizationRecord } from "../evidence/unsupportedStabilizationEngine.js";

export function suppressOntologySelfConfirmation(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var inferred: any = py.truthy(py.get(edge, "inferred"));
  var self_confirm: any = py.and2(inferred, () => ((py.len(ev) < 2)));
  var record: any = (py.truthy(self_confirm) ? _stabilizationRecord("ontology_self_confirmation", {"required": 2, "actual": py.len(ev)}) : null);
  var collapse: any = (py.truthy(self_confirm) ? {"max": py.F(0.35)} : py.get(edge, "confidence_caps", {}));
  var entropy: any = {"level": (py.truthy(self_confirm) ? py.F(0.6) : py.F(0.1))};
  return {...(edge), "truth_preservation": {"preserved": !py.truthy(self_confirm), "self_confirmation_blocked": self_confirm}, "instability": {"unstable": self_confirm, "preserved": true}, "entropy": entropy, "truth_boundaries": {"equivalence_allowed": (py.len(ev) >= 2)}, "confidence_collapse": collapse, "stabilization_suppressed": record};
}

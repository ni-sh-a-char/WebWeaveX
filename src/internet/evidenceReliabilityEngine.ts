/**
 * Converted from Python: core/internet/evidence_reliability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { weightEvidenceCalculus } from "../evidence/evidenceWeightingCalculus.js";

export function scoreEvidenceReliability(evidence: any, parser_backed: any = false): any {
  var w: any = weightEvidenceCalculus(evidence, parser_backed);
  var reliability: any = py.round(py.min([py.F(1.0), py.div(py.at(w, "total"), py.max([1, py.len(py.or2(py.at(w, "weights"), () => ({})))]))]), 3);
  return {"reliability": reliability, "weights": py.at(w, "weights"), "deterministic_inputs": py.at(w, "deterministic_inputs")};
}
export { weightEvidenceCalculus };

/**
 * Converted from Python: core/evidence/semantic_speculation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { collectSuppressedSpeculation } from "./speculativeInferenceEngine.js";

export function detectSemanticSpeculation(evidence: any, inferred: any, reconciled: any): any {
  var suppressed: any = collectSuppressedSpeculation(evidence, inferred, reconciled);
  return {"speculative": (py.len(suppressed) > 0), "suppressed_speculation": suppressed, "density": py.round(py.div(py.len(suppressed), py.max([1, py.add(py.len(inferred), 1)])), 3)};
}
export { collectSuppressedSpeculation };

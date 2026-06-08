/**
 * Converted from Python: core/identity/runtime_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeRuntimeEntropy } from "./browserEntropyEngine.js";

export function verifyRuntimeConsistency(identity: any, observed: any): any {
  var entropy: any = computeRuntimeEntropy(identity, observed);
  return {"consistent": py.get(entropy, "stable", false), "entropy": entropy, "bounded": true};
}
export { computeRuntimeEntropy };

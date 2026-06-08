/**
 * Converted from Python: core/autonomy/semantic_safety_envelope_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_RUNTIME_SIZE: any = 100000;
export function enforceSemanticSafetyEnvelope(runtime: any): any {
  return {"safe": (py.len(runtime) <= MAX_RUNTIME_SIZE), "runtime_size": py.len(runtime)};
}

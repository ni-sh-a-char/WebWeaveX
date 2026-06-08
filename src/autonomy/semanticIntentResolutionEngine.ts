/**
 * Converted from Python: core/autonomy/semantic_intent_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_INTENT_LEN: any = 4096;
export function resolveSemanticIntent(payload: any): any {
  var intent: any = py.slice(py.toStr(py.get(payload, "intent", py.get(payload, "goal", ""))), null, MAX_INTENT_LEN);
  var tokens: any = py.sorted(py.iter(py.split(intent)).filter((t: any) => py.truthy(py.strip(t))).map((t: any) => String(py.strip(t)).toLowerCase()));
  return {"intent": intent, "tokens": tokens, "resolved": py.truthy(intent)};
}

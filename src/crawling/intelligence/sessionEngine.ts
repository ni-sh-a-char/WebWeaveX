/**
 * Converted from Python: core/crawling/intelligence/session_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { dumpsDeterministic } from "../../utils/deterministicSerializer.js";

export function checkpointSession(state: any): any {
  return {"checkpoint": dumpsDeterministic(py.or2(state, () => ({})))};
}
export function resumeSession(checkpoint: any): any {
  var raw: any = py.get(py.or2(checkpoint, () => ({})), "checkpoint", "{}");
  try {
    var obj: any = py.jsonLoads(raw);
    return (((obj !== null && typeof obj === "object" && !Array.isArray(obj) && !(obj instanceof Set) && !(obj instanceof Map))) ? obj : {});
  } catch (_e: any) {
    return {};
  }
}
export { dumpsDeterministic };

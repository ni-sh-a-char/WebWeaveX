/**
 * Converted from Python: core/identity/canvas_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";

export function buildCanvasRuntime(profile_id: any = "default"): any {
  var payload: any = {"profile_id": profile_id, "canvas_seed": `webweavex-canvas:${py.toStr(profile_id)}`};
  var fingerprint: any = computeKaalkaHashPayload(payload);
  return {"canvas_fingerprint": fingerprint, "canvas_seed": py.at(payload, "canvas_seed"), "bounded": true};
}
export { computeKaalkaHashPayload };

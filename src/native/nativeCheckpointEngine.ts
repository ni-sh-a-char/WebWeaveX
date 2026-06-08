/**
 * Converted from Python: core/native/native_checkpoint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";

export function saveNativeCheckpoint(path: any, checkpoint: any, key: any): any {
  var encrypted: any = encryptSessionState(checkpoint, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(encrypted, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadNativeCheckpoint(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "checkpoint": _emptyCheckpoint(), "bounded": true};
  }
  var encrypted: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptSessionState(encrypted, key);
  return {"available": true, "checkpoint": py.get(decrypted, "session", _emptyCheckpoint()), "algorithm": "kaalka", "bounded": true};
}
export function _emptyCheckpoint(): any {
  return {"runtime_state": {}, "windows": {}, "streams": {}, "terminals": {}, "workflows": {}, "adaptive_state": {}, "bounded": true};
}
export { decryptSessionState, encryptSessionState };

/**
 * Converted from Python: core/identity/fingerprint_persistence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";
import { buildBrowserIdentity } from "./browserIdentityOrchestrator.js";

export function saveBrowserIdentity(path: any, identity: any, key: any): any {
  var encrypted: any = encryptSessionState(identity, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(encrypted, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadBrowserIdentity(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "identity": buildBrowserIdentity("default"), "bounded": true};
  }
  var encrypted: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptSessionState(encrypted, key);
  return {"available": true, "identity": py.get(decrypted, "session", {}), "algorithm": "kaalka", "bounded": true};
}
export { buildBrowserIdentity, decryptSessionState, encryptSessionState };

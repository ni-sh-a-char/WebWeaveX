/**
 * Converted from Python: core/identity/session_identity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function attachIdentityToSession(session: any, identity: any): any {
  var merged: any = py.pyDict(session);
  py.setItem(merged, "browser_identity", py.pyDict(identity));
  py.setItem(merged, "identity_attached", true);
  py.setItem(merged, "bounded", true);
  return merged;
}
export function restoreIdentitySession(session: any): any {
  var identity: any = py.pyDict(py.get(session, "browser_identity", {}));
  return {"session": session, "identity": identity, "restored": py.truthy(identity), "bounded": true};
}

/**
 * Converted from Python: core/reconstruction/runtime_identity_reconstruction.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _identityHash(payload: any): any {
  var canonical: any = py.jsonDumps(payload, {sortKeys: true});
  return py.slice(py.hashNew("sha256", py.encode(canonical, "utf-8")).hexdigest(), null, 32);
}
export function reconstructRuntimeIdentity(browser_identity: any = null, session: any = null, runtime_id: any = "", execution_id: any = "", worker_id: any = ""): any {
  var browser: any = py.pyDict(py.or2(browser_identity, () => ({})));
  var session_body: any = py.pyDict(py.or2(session, () => ({})));
  var browser_hash: any = _identityHash({"browser": browser});
  var session_hash: any = _identityHash({"session": session_body});
  var runtime_hash: any = _identityHash({"runtime_id": runtime_id});
  var execution_hash: any = _identityHash({"execution_id": execution_id});
  var worker_hash: any = _identityHash({"worker_id": worker_id});
  return {"browser_identity": {...(browser), "identity_hash": browser_hash}, "session_identity": {...(session_body), "identity_hash": session_hash}, "runtime_identity": {"runtime_id": runtime_id, "identity_hash": runtime_hash}, "execution_identity": {"execution_id": execution_id, "identity_hash": execution_hash}, "worker_identity": {"worker_id": worker_id, "identity_hash": worker_hash}, "continuity_hashes": py.sorted([browser_hash, session_hash, runtime_hash]), "bounded": true};
}

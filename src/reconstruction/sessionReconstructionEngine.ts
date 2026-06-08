/**
 * Converted from Python: core/reconstruction/session_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructRuntimeSession(session: any = null, identity: any = null, sync_state: any = null, adaptive_memory: any = null): any {
  session = py.or2(session, () => ({}));
  identity = py.or2(identity, () => ({}));
  sync_state = py.or2(sync_state, () => ({}));
  adaptive_memory = py.or2(adaptive_memory, () => ({}));
  var cookies: any = py.sorted(py.get(session, "cookies", []), {key: ((c: any) => py.toStr(py.get(c, "name", ""))) as (item: any) => any});
  return {"authenticated_session": {"authenticated": py.truthy(py.get(session, "authenticated", false)), "session_id": py.toStr(py.get(session, "session_id", py.get(identity, "identity_id", "")))}, "cookies": cookies, "csrf_state": py.pyDict(py.get(session, "csrf", py.get(session, "csrf_state", {}))), "browser_identity": py.pyDict(identity), "synchronization_state": py.pyDict(sync_state), "adaptive_memory": py.pyDict(adaptive_memory), "replay_safe": true, "bounded": true};
}

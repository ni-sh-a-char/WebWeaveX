/**
 * Converted from Python: core/native/native_remote_session_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let REMOTE_PROTOCOLS: any = ["rdp", "vnc", "ssh", "browser_remote"];
export function extractRemoteRuntime(protocol: any = "ssh", snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  var normalized: any = String(protocol).toLowerCase();
  if (!py.contains(REMOTE_PROTOCOLS, normalized)) {
    normalized = "ssh";
  }
  return {"protocol": normalized, "session_id": py.toStr(py.get(snap, "session_id", "")), "host": py.toStr(py.get(snap, "host", "")), "port": py.toInt(py.get(snap, "port", 0)), "terminal": py.get(snap, "terminal", {}), "window_stream": py.get(snap, "window_stream", {}), "authenticated": py.truthy(py.get(snap, "authenticated", false)), "bounded": true};
}

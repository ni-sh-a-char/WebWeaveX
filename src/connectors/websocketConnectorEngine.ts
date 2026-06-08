/**
 * Converted from Python: core/connectors/websocket_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractWebsocketRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"protocol": "websocket", "connections": [...py.iter(py.get(snap, "connections", []))], "frames": py.toInt(py.get(snap, "frames", 0)), "bounded": true};
}

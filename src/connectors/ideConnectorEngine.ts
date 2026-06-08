/**
 * Converted from Python: core/connectors/ide_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractIdeRuntime(ide: any = "vscode", snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"ide": ide, "open_files": py.sorted(py.get(snap, "open_files", []), {key: (py.toStr) as (item: any) => any}), "terminals": [...py.iter(py.get(snap, "terminals", []))], "tabs": [...py.iter(py.get(snap, "tabs", []))], "workspace_topology": py.pyDict(py.get(snap, "workspace", {})), "debug_sessions": [...py.iter(py.get(snap, "debug_sessions", []))], "degraded": py.get(snap, "degraded", false), "bounded": true};
}

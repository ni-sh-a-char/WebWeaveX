/**
 * Converted from Python: core/connectors/docker_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractDockerRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"runtime": "docker", "containers": [...py.iter(py.get(snap, "containers", []))], "images": py.sorted(py.get(snap, "images", []), {key: (py.toStr) as (item: any) => any}), "volumes": [...py.iter(py.get(snap, "volumes", []))], "networks": [...py.iter(py.get(snap, "networks", []))], "states": py.pyDict(py.get(snap, "states", {})), "health": py.pyDict(py.get(snap, "health", {})), "degraded": py.get(snap, "degraded", false), "bounded": true};
}

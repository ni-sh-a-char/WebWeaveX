/**
 * Converted from Python: core/connectors/container_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractDockerRuntime } from "./dockerConnectorEngine.js";

export function extractContainerRuntime(runtime: any = "docker", snapshot: any = null): any {
  var normalized: any = String(runtime).toLowerCase();
  var snap: any = py.or2(snapshot, () => ({}));
  try {
    if (py.contains(["docker", "podman", "oci"], normalized)) {
      var result: any = extractDockerRuntime(snap);
      py.setItem(result, "runtime", normalized);
      return result;
    }
  } catch (_e: any) {
  }
  return {"runtime": normalized, "containers": [], "images": [], "volumes": [], "networks": [], "degraded": true, "bounded": true};
}
export { extractDockerRuntime };

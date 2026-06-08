/**
 * Converted from Python: core/repository/service_lifecycle_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildServiceRuntimeGraph } from "./serviceRuntimeGraphEngine.js";

export function modelServiceLifecycle(source: any, path: any = "", files: any = null): any {
  var g: any = buildServiceRuntimeGraph(source, path, files);
  var lifecycle: any = py.iter(py.slice(py.get(g, "nodes", []), null, 50)).map((n: any) => ({"service": n, "phase": "running"}));
  return {"lifecycle": lifecycle, "evidence": py.get(g, "evidence", [])};
}
export { buildServiceRuntimeGraph };
